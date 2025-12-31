from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple
import uuid
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from datetime import timedelta
from app.repositories.image_repository import ImageRepository
from app.schemas.image import PresignUploadRequest, PresignUploadResponse, ImageCreateRequest
from app.core.config import settings
from fastapi import HTTPException, status


class ImageService:
    def __init__(self, session: AsyncSession):
        self.image_repo = ImageRepository(session)
        self._s3_client = None

    @property
    def s3_client(self):
        """Lazy initialization of S3 client."""
        if self._s3_client is None:
            config = Config(
                region_name=settings.AWS_REGION,
                signature_version="s3v4",
            )

            if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                self._s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION,
                    endpoint_url=settings.S3_ENDPOINT_URL,
                    config=config,
                )
            else:
                # Use default credentials (IAM role, environment variables, etc.)
                self._s3_client = boto3.client(
                    "s3",
                    region_name=settings.AWS_REGION,
                    endpoint_url=settings.S3_ENDPOINT_URL,
                    config=config,
                )
        return self._s3_client

    def _validate_image_type(self, content_type: str, filename: str) -> Tuple[str, str]:
        """Validate image type and return normalized content type and file extension."""
        content_type_lower = content_type.lower()
        filename_lower = filename.lower()

        # Map content types to allowed types
        type_mapping = {
            "image/jpeg": ("image/jpeg", "jpg"),
            "image/jpg": "image/jpeg",
            "image/png": ("image/png", "png"),
            "image/heic": ("image/heic", "heic"),
            "image/heif": ("image/heic", "heic"),
        }

        # Check content type
        if content_type_lower in type_mapping:
            if isinstance(type_mapping[content_type_lower], tuple):
                return type_mapping[content_type_lower]
            else:
                # Handle jpg -> jpeg mapping
                return ("image/jpeg", "jpg")

        # Fallback: check file extension
        if filename_lower.endswith((".jpg", ".jpeg")):
            return ("image/jpeg", "jpg")
        elif filename_lower.endswith(".png"):
            return ("image/png", "png")
        elif filename_lower.endswith((".heic", ".heif")):
            return ("image/heic", "heic")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported image type. Allowed types: JPG, PNG, HEIC"
        )

    def _validate_file_size(self, file_size: int) -> None:
        """Validate file size."""
        max_size = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_IMAGE_SIZE_MB}MB"
            )

    def _generate_s3_key(self, user_id: int, filename: str, extension: str) -> str:
        """Generate unique S3 key for image."""
        unique_id = str(uuid.uuid4())
        return f"images/{user_id}/{unique_id}.{extension}"

    async def generate_presigned_upload_url(
        self,
        user_id: int,
        request: PresignUploadRequest,
    ) -> PresignUploadResponse:
        """Generate presigned S3 upload URL."""
        if not settings.S3_BUCKET_NAME:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="S3 bucket not configured"
            )

        # Validate image type
        content_type, extension = self._validate_image_type(request.content_type, request.filename)

        # Validate file size
        self._validate_file_size(request.file_size)

        # Generate unique S3 key
        s3_key = self._generate_s3_key(user_id, request.filename, extension)

        try:
            # Generate presigned URL
            presigned_url = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": settings.S3_BUCKET_NAME,
                    "Key": s3_key,
                    "ContentType": content_type,
                },
                ExpiresIn=3600,  # 1 hour
            )

            # Create image record with PENDING status
            image_data = ImageCreateRequest(
                s3_key=s3_key,
                filename=f"{uuid.uuid4()}.{extension}",
                original_filename=request.filename,
                content_type=content_type,
                file_size=request.file_size,
            )

            image = await self.image_repo.create(
                user_id=user_id,
                image_data=image_data,
                s3_key=s3_key,
                s3_bucket=settings.S3_BUCKET_NAME,
            )

            return PresignUploadResponse(
                upload_url=presigned_url,
                s3_key=s3_key,
                image_id=image.id,
                expires_in=3600,
            )

        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate presigned URL: {str(e)}"
            )

    async def confirm_upload(self, user_id: int, s3_key: str) -> None:
        """Confirm image upload and update status."""
        image = await self.image_repo.get_by_s3_key(s3_key)
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )

        if image.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this image"
            )

        # Verify file exists in S3
        try:
            self.s3_client.head_object(Bucket=image.s3_bucket, Key=s3_key)
            
            # Generate public URL (if bucket is public) or presigned URL
            s3_url = f"https://{image.s3_bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
            if settings.S3_ENDPOINT_URL:
                # For S3-compatible services
                s3_url = f"{settings.S3_ENDPOINT_URL}/{image.s3_bucket}/{s3_key}"

            await self.image_repo.update_status(image, image.status, s3_url)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found in S3"
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to verify upload: {str(e)}"
            )

    async def create_image_record(
        self,
        user_id: int,
        image_data: ImageCreateRequest,
    ):
        """Create image record after upload."""
        if not settings.S3_BUCKET_NAME:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="S3 bucket not configured"
            )

        # Validate
        self._validate_image_type(image_data.content_type, image_data.original_filename)
        self._validate_file_size(image_data.file_size)

        # Verify file exists in S3
        try:
            self.s3_client.head_object(Bucket=settings.S3_BUCKET_NAME, Key=image_data.s3_key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found in S3"
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to verify upload: {str(e)}"
            )

        # Generate S3 URL
        s3_url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{image_data.s3_key}"
        if settings.S3_ENDPOINT_URL:
            s3_url = f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{image_data.s3_key}"

        # Create image record
        from app.models.image import ImageStatus
        image = await self.image_repo.create(
            user_id=user_id,
            image_data=image_data,
            s3_key=image_data.s3_key,
            s3_bucket=settings.S3_BUCKET_NAME,
        )

        # Update status to uploaded
        await self.image_repo.update_status(image, ImageStatus.UPLOADED, s3_url)

        return image

