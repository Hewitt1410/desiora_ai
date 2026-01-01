from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class ImageType(str, enum.Enum):
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    HEIC = "heic"


class ImageStatus(str, enum.Enum):
    PENDING = "pending"  # Presigned URL generated, upload not completed
    UPLOADED = "uploaded"  # Successfully uploaded to S3
    FAILED = "failed"  # Upload failed


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    file_type = Column(SQLEnum(ImageType), nullable=False)
    file_size = Column(BigInteger, nullable=False)  # Size in bytes
    s3_key = Column(String, nullable=False, unique=True, index=True)
    s3_bucket = Column(String, nullable=False)
    s3_url = Column(String, nullable=True)  # Public URL if bucket is public
    status = Column(SQLEnum(ImageStatus), default=ImageStatus.PENDING, nullable=False)
    image_metadata = Column(String, nullable=True)  # JSON string for additional metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user = relationship("User", backref="images")


