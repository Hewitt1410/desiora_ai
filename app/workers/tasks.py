from celery import Task
from app.core.celery_app import celery_app
from app.workers.room_design_pipeline import RoomDesignPipeline
from app.workers.callbacks import update_job_status
from app.core.config import settings
from app.models.design_job import JobStatus
import logging
import traceback
import asyncio

logger = logging.getLogger(__name__)


class RoomDesignTask(Task):
    """Custom task class with model loading."""
    _pipeline = None

    @property
    def pipeline(self):
        """Lazy load pipeline (models loaded once per worker)."""
        if self._pipeline is None:
            logger.info("Loading AI models for room design pipeline...")
            self._pipeline = RoomDesignPipeline(
                device=settings.AI_WORKER_DEVICE,
                model_cache_dir=settings.AI_WORKER_MODEL_CACHE_DIR,
            )
            logger.info("AI models loaded successfully")
        return self._pipeline


@celery_app.task(
    bind=True,
    base=RoomDesignTask,
    name="process_room_design",
    max_retries=3,
    default_retry_delay=60,
)
def process_room_design_task(
    self,
    job_id: int,
    image_url: str,
    style: str,
    parameters: dict = None,
):
    """
    Celery task to process room design.
    
    Args:
        job_id: Design job ID
        image_url: URL of the original room image
        style: Design style (e.g., 'modern', 'minimalist', 'rustic')
        parameters: Additional parameters (optional)
    
    Returns:
        dict: Result URLs and metadata
    """
    try:
        logger.info(f"Starting room design job {job_id} with style: {style}")
        
        # Get pipeline instance
        pipeline = self.pipeline
        
        # Run pipeline
        result = pipeline.process(
            image_url=image_url,
            style=style,
            parameters=parameters or {},
        )
        
        logger.info(f"Room design job {job_id} completed successfully")
        
        # Update job status in database
        asyncio.run(update_job_status(
            job_id,
            JobStatus.COMPLETED,
            result_urls=result["result_urls"]
        ))
        
        return {
            "job_id": job_id,
            "result_urls": result["result_urls"],
            "metadata": result.get("metadata", {}),
            "status": "completed",
        }
    
    except Exception as exc:
        logger.error(
            f"Room design job {job_id} failed: {str(exc)}\n{traceback.format_exc()}"
        )
        
        # Retry if not exceeded max retries
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying room design job {job_id} (attempt {self.request.retries + 1})")
            raise self.retry(exc=exc)
        
        # Max retries exceeded - update job status
        asyncio.run(update_job_status(
            job_id,
            JobStatus.FAILED,
            error_message=str(exc)
        ))
        
        return {
            "job_id": job_id,
            "status": "failed",
            "error": str(exc),
        }

