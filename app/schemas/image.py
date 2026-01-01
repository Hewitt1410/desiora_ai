from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from app.models.image import ImageType, ImageStatus


class PresignUploadRequest(BaseModel):
    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="MIME type (e.g., image/jpeg)")
    file_size: int = Field(..., description="File size in bytes", gt=0)

    @validator("content_type")
    def validate_content_type(cls, v):
        allowed_types = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/heic",
            "image/heif",
        ]
        if v.lower() not in allowed_types:
            raise ValueError(f"Content type must be one of: {', '.join(allowed_types)}")
        return v.lower()

    @validator("file_size")
    def validate_file_size(cls, v):
        max_size = 10 * 1024 * 1024  # 10MB
        if v > max_size:
            raise ValueError(f"File size must not exceed 10MB (got {v / 1024 / 1024:.2f}MB)")
        return v


class PresignUploadResponse(BaseModel):
    upload_url: str
    s3_key: str
    image_id: int
    expires_in: int = Field(default=3600, description="URL expiration time in seconds")


class ImageCreateRequest(BaseModel):
    s3_key: str = Field(..., description="S3 key from presigned upload")
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    metadata: Optional[dict] = None


class ConfirmUploadRequest(BaseModel):
    s3_key: str = Field(..., description="S3 key from presigned upload")


class ImageResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    original_filename: str
    content_type: str
    file_type: ImageType
    file_size: int
    s3_key: str
    s3_bucket: str
    s3_url: Optional[str]
    status: ImageStatus
    metadata: Optional[str] = Field(None, alias="image_metadata")
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

