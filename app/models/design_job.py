from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"  # Job is being retried after failure


class DesignJob(Base):
    __tablename__ = "design_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Job information
    job_type = Column(String, nullable=False)  # e.g., "room_design", "product_design", etc.
    prompt = Column(Text, nullable=False)  # User's design prompt/description
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False, index=True)
    
    # Job parameters (stored as JSON)
    parameters = Column(JSON, nullable=True)  # Additional parameters for the job
    
    # Results
    result_urls = Column(JSON, nullable=True)  # List of result image URLs
    result_metadata = Column(JSON, nullable=True)  # Additional result data
    
    # Error handling
    error_message = Column(Text, nullable=True)  # Error message if job failed
    retry_count = Column(Integer, default=0, nullable=False)  # Number of retry attempts
    max_retries = Column(Integer, default=3, nullable=False)  # Maximum retry attempts
    
    # Processing information
    started_at = Column(DateTime(timezone=True), nullable=True)  # When processing started
    completed_at = Column(DateTime(timezone=True), nullable=True)  # When job completed
    processing_time_seconds = Column(Integer, nullable=True)  # Time taken to process
    
    # Queue information
    queue_id = Column(String, nullable=True, index=True)  # Queue task ID (Celery, RQ, etc.)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user = relationship("User", backref="design_jobs")


