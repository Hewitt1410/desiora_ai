from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from app.models.design_job import DesignJob, JobStatus


class DesignJobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, job_id: int) -> Optional[DesignJob]:
        """Get design job by ID."""
        result = await self.session.execute(
            select(DesignJob).where(DesignJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
        status: Optional[JobStatus] = None,
    ) -> tuple[List[DesignJob], int]:
        """Get design jobs by user ID with pagination."""
        query = select(DesignJob).where(DesignJob.user_id == user_id)
        
        if status:
            query = query.where(DesignJob.status == status)
        
        # Get total count
        count_query = select(func.count()).select_from(DesignJob).where(DesignJob.user_id == user_id)
        if status:
            count_query = count_query.where(DesignJob.status == status)
        
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()
        
        # Get paginated results
        query = query.order_by(DesignJob.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(query)
        jobs = list(result.scalars().all())
        
        return jobs, total

    async def get_pending_jobs(self, limit: int = 10) -> List[DesignJob]:
        """Get pending jobs for processing."""
        result = await self.session.execute(
            select(DesignJob)
            .where(DesignJob.status == JobStatus.PENDING)
            .order_by(DesignJob.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_failed_jobs_for_retry(self, limit: int = 10) -> List[DesignJob]:
        """Get failed jobs that can be retried."""
        result = await self.session.execute(
            select(DesignJob)
            .where(
                and_(
                    DesignJob.status == JobStatus.FAILED,
                    DesignJob.retry_count < DesignJob.max_retries
                )
            )
            .order_by(DesignJob.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(
        self,
        user_id: int,
        job_type: str,
        prompt: str,
        parameters: Optional[dict] = None,
        max_retries: int = 3,
    ) -> DesignJob:
        """Create a new design job."""
        job = DesignJob(
            user_id=user_id,
            job_type=job_type,
            prompt=prompt,
            parameters=parameters,
            status=JobStatus.PENDING,
            max_retries=max_retries,
            retry_count=0,
        )
        self.session.add(job)
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def update(self, job: DesignJob) -> DesignJob:
        """Update design job."""
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def update_status(
        self,
        job: DesignJob,
        status: JobStatus,
        error_message: Optional[str] = None,
    ) -> DesignJob:
        """Update job status."""
        job.status = status
        if error_message:
            job.error_message = error_message
        
        if status == JobStatus.PROCESSING and not job.started_at:
            from datetime import datetime
            job.started_at = datetime.utcnow()
        elif status in [JobStatus.COMPLETED, JobStatus.FAILED]:
            from datetime import datetime
            job.completed_at = datetime.utcnow()
            if job.started_at:
                delta = job.completed_at - job.started_at
                job.processing_time_seconds = int(delta.total_seconds())
        
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def update_results(
        self,
        job: DesignJob,
        result_urls: List[str],
        result_metadata: Optional[dict] = None,
    ) -> DesignJob:
        """Update job results."""
        job.result_urls = result_urls
        job.result_metadata = result_metadata
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def increment_retry(self, job: DesignJob) -> DesignJob:
        """Increment retry count."""
        job.retry_count += 1
        if job.retry_count < job.max_retries:
            job.status = JobStatus.RETRYING
        else:
            job.status = JobStatus.FAILED
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def set_queue_id(self, job: DesignJob, queue_id: str) -> DesignJob:
        """Set queue task ID."""
        job.queue_id = queue_id
        await self.session.commit()
        await self.session.refresh(job)
        return job


