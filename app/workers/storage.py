"""
Storage utilities for saving processed images.
"""
import io
from PIL import Image
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def save_to_storage(image: Image.Image, path: str) -> str:
    """
    Save image to storage (S3 or local).
    
    Args:
        image: PIL Image object
        path: Storage path
    
    Returns:
        URL of saved image
    """
    if settings.STORAGE_BACKEND == "s3":
        return _save_to_s3(image, path)
    else:
        return _save_to_local(image, path)


def _save_to_s3(image: Image.Image, path: str) -> str:
    """Save image to S3."""
    try:
        import boto3
        from app.core.config import settings
        
        # Convert image to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="JPEG", quality=95)
        img_buffer.seek(0)
        
        # Upload to S3
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL,
        )
        
        s3_client.upload_fileobj(
            img_buffer,
            settings.S3_BUCKET_NAME,
            path,
            ExtraArgs={"ContentType": "image/jpeg"},
        )
        
        # Generate URL
        if settings.S3_ENDPOINT_URL:
            url = f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{path}"
        else:
            url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{path}"
        
        logger.info(f"Saved image to S3: {url}")
        return url
    
    except Exception as e:
        logger.error(f"Failed to save to S3: {e}")
        raise


def _save_to_local(image: Image.Image, path: str) -> str:
    """Save image to local storage."""
    try:
        from pathlib import Path
        from app.core.config import settings
        
        # Determine storage path
        if settings.STORAGE_LOCAL_PATH:
            storage_path = Path(settings.STORAGE_LOCAL_PATH)
        else:
            storage_path = Path(settings.AI_WORKER_OUTPUT_DIR)
        
        # Create full path
        full_path = storage_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save image
        image.save(full_path, format="JPEG", quality=95)
        
        # Return local URL (in production, this would be a public URL)
        url = f"/storage/{path}"
        logger.info(f"Saved image to local storage: {full_path}")
        return url
    
    except Exception as e:
        logger.error(f"Failed to save to local storage: {e}")
        raise

