from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime
from app.repositories.design_job_repository import DesignJobRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.subscription_service import SubscriptionService
from app.models.design_job import DesignJob, JobStatus
from app.schemas.design import DesignJobCreateRequest, DesignJobResponse
from fastapi import HTTPException, status
import uuid


class DesignJobService:
    def __init__(self, session: AsyncSession):
        self.design_job_repo = DesignJobRepository(session)
        self.subscription_service = SubscriptionService(session)

    async def create_job(
        self,
        user_id: int,
        job_data: DesignJobCreateRequest,
    ) -> DesignJob:
        """Create a new design job."""
        # Check subscription quota
        can_use = await self.subscription_service.check_quota(user_id)
        if not can_use:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Quota exceeded. Please upgrade your subscription."
            )

        # Create job
        job = await self.design_job_repo.create(
            user_id=user_id,
            job_type=job_data.job_type,
            prompt=job_data.prompt,
            parameters=job_data.parameters,
        )

        # Use quota
        quota_used = await self.subscription_service.use_quota(user_id, amount=1)
        if not quota_used:
            # If quota check passed but use failed, mark job as failed
            await self.design_job_repo.update_status(
                job,
                JobStatus.FAILED,
                error_message="Quota exceeded during job creation"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Quota exceeded. Please upgrade your subscription."
            )

        # Queue job for processing (async)
        await self._queue_job_for_processing(job)

        return job

    async def _queue_job_for_processing(self, job: DesignJob) -> None:
        """Queue job for async processing."""
        # Generate queue ID
        queue_id = str(uuid.uuid4())
        await self.design_job_repo.set_queue_id(job, queue_id)

        # In production, this would enqueue to Celery, RQ, or other queue system
        # For now, we'll use a simple background task approach
        # You can integrate with Celery like this:
        # from app.core.celery_app import process_design_job_task
        # process_design_job_task.delay(job.id)

        # For demonstration, we'll process immediately in background
        # In production, use a proper queue system
        from fastapi import BackgroundTasks
        # This will be handled by the endpoint using BackgroundTasks

    async def get_job(self, job_id: int, user_id: Optional[int] = None) -> DesignJob:
        """Get design job by ID."""
        job = await self.design_job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Design job not found"
            )

        # Check authorization if user_id provided
        if user_id and job.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this job"
            )

        return job

    async def get_user_jobs(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
        status_filter: Optional[JobStatus] = None,
    ) -> tuple[List[DesignJob], int]:
        """Get user's design jobs with pagination."""
        offset = (page - 1) * page_size
        jobs, total = await self.design_job_repo.get_by_user_id(
            user_id=user_id,
            limit=page_size,
            offset=offset,
            status=status_filter,
        )
        return jobs, total

    async def process_job(self, job_id: int) -> DesignJob:
        """Process a design job (called by queue worker)."""
        job = await self.design_job_repo.get_by_id(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        if job.status not in [JobStatus.PENDING, JobStatus.RETRYING]:
            return job

        # Update status to processing
        await self.design_job_repo.update_status(job, JobStatus.PROCESSING)

        try:
            # Simulate AI design processing
            # In production, this would call your AI service
            result_urls = await self._process_design(job)

            # Update job with results
            await self.design_job_repo.update_results(job, result_urls)
            await self.design_job_repo.update_status(job, JobStatus.COMPLETED)

        except Exception as e:
            # Handle failure
            error_message = str(e)
            await self.design_job_repo.update_status(
                job,
                JobStatus.FAILED,
                error_message=error_message
            )

            # Retry if possible
            if job.retry_count < job.max_retries:
                await self.design_job_repo.increment_retry(job)
                # Re-queue for retry
                await self._queue_job_for_processing(job)

        return job

    async def _process_design(self, job: DesignJob) -> List[str]:
        """
        Process the design job using AI worker (Celery task).
        """
        from app.core.celery_app import celery_app
        
        # Get image URL from parameters or job data
        image_url = job.parameters.get("image_url") if job.parameters else None
        if not image_url:
            raise ValueError("image_url is required in job parameters")
        
        # Get style from parameters
        style = job.parameters.get("style", "modern") if job.parameters else "modern"
        
        # Queue Celery task
        task = celery_app.send_task(
            "process_room_design",
            args=[job.id, image_url, style, job.parameters],
        )
        
        # Store queue ID
        await self.design_job_repo.set_queue_id(job, task.id)
        
        # Note: In production, you might want to wait for result or use callbacks
        # For now, the task will update the job status via database
        
        # Return empty list - URLs will be updated by the worker
        return []

    async def retry_failed_jobs(self, limit: int = 10) -> List[DesignJob]:
        """Retry failed jobs that haven't exceeded max retries."""
        failed_jobs = await self.design_job_repo.get_failed_jobs_for_retry(limit=limit)
        retried = []

        for job in failed_jobs:
            await self.design_job_repo.increment_retry(job)
            await self._queue_job_for_processing(job)
            retried.append(job)

        return retried

