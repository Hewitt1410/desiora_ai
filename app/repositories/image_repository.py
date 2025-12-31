from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models.image import Image, ImageStatus
from app.schemas.image import ImageCreateRequest


class ImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, image_id: int) -> Optional[Image]:
        """Get image by ID."""
        result = await self.session.execute(select(Image).where(Image.id == image_id))
        return result.scalar_one_or_none()

    async def get_by_s3_key(self, s3_key: str) -> Optional[Image]:
        """Get image by S3 key."""
        result = await self.session.execute(select(Image).where(Image.s3_key == s3_key))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int, limit: int = 100, offset: int = 0) -> List[Image]:
        """Get images by user ID."""
        result = await self.session.execute(
            select(Image)
            .where(Image.user_id == user_id)
            .order_by(Image.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, user_id: int, image_data: ImageCreateRequest, s3_key: str, s3_bucket: str) -> Image:
        """Create a new image record."""
        from app.models.image import ImageType
        
        # Determine file type from content type
        content_type_lower = image_data.content_type.lower()
        if content_type_lower in ["image/jpeg", "image/jpg"]:
            file_type = ImageType.JPEG
        elif content_type_lower == "image/png":
            file_type = ImageType.PNG
        elif content_type_lower in ["image/heic", "image/heif"]:
            file_type = ImageType.HEIC
        else:
            file_type = ImageType.JPEG  # Default

        import json
        metadata_json = json.dumps(image_data.metadata) if image_data.metadata else None

        image = Image(
            user_id=user_id,
            filename=image_data.filename,
            original_filename=image_data.original_filename,
            content_type=image_data.content_type,
            file_type=file_type,
            file_size=image_data.file_size,
            s3_key=s3_key,
            s3_bucket=s3_bucket,
            status=ImageStatus.PENDING,
            metadata=metadata_json,
        )
        self.session.add(image)
        await self.session.commit()
        await self.session.refresh(image)
        return image

    async def update_status(self, image: Image, status: ImageStatus, s3_url: Optional[str] = None) -> Image:
        """Update image status and optionally S3 URL."""
        image.status = status
        if s3_url:
            image.s3_url = s3_url
        await self.session.commit()
        await self.session.refresh(image)
        return image

    async def delete(self, image: Image) -> None:
        """Delete an image record."""
        await self.session.delete(image)
        await self.session.commit()

