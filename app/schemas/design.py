from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.design_job import JobStatus


class DesignJobCreateRequest(BaseModel):
    job_type: str = Field(..., description="Type of design job (e.g., 'room_design', 'product_design')")
    prompt: str = Field(..., min_length=1, max_length=5000, description="Design prompt/description")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional job parameters")


class DesignJobResponse(BaseModel):
    id: int
    user_id: int
    job_type: str
    prompt: str
    status: JobStatus
    parameters: Optional[Dict[str, Any]]
    result_urls: Optional[List[str]]
    result_metadata: Optional[Dict[str, Any]]
    error_message: Optional[str]
    retry_count: int
    max_retries: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    processing_time_seconds: Optional[int]
    queue_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class DesignJobListResponse(BaseModel):
    jobs: List[DesignJobResponse]
    total: int
    page: int = 1
    page_size: int = 20


