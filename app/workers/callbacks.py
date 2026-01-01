"""
Callbacks for updating job status from Celery tasks.
"""
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings
from app.repositories.design_job_repository import DesignJobRepository
from app.models.design_job import JobStatus

logger = logging.getLogger(__name__)

# Create async engine for callbacks
_engine = create_async_engine(settings.DATABASE_URL, echo=False)
_AsyncSessionLocal = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)


async def update_job_status(job_id: int, status: JobStatus, result_urls: list = None, error_message: str = None):
    """Update job status from Celery task."""
    async with _AsyncSessionLocal() as session:
        try:
            job_repo = DesignJobRepository(session)
            job = await job_repo.get_by_id(job_id)
            
            if not job:
                logger.error(f"Job {job_id} not found for status update")
                return
            
            await job_repo.update_status(job, status, error_message)
            
            if result_urls:
                await job_repo.update_results(job, result_urls)
            
            logger.info(f"Updated job {job_id} status to {status}")
        
        except Exception as e:
            logger.error(f"Failed to update job {job_id} status: {e}")


def on_task_success(sender=None, result=None, **kwargs):
    """Callback when task succeeds."""
    import asyncio
    
    job_id = result.get("job_id")
    if job_id:
        asyncio.run(update_job_status(
            job_id,
            JobStatus.COMPLETED,
            result_urls=result.get("result_urls", [])
        ))


def on_task_failure(sender=None, task_id=None, exception=None, **kwargs):
    """Callback when task fails."""
    import asyncio
    
    # Extract job_id from task kwargs if available
    # This would need to be passed through task context
    logger.error(f"Task {task_id} failed: {exception}")




