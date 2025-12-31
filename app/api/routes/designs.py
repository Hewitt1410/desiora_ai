from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.services.design_job_service import DesignJobService
from app.schemas.design import (
    DesignJobCreateRequest,
    DesignJobResponse,
    DesignJobListResponse,
)
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.design_job import JobStatus

router = APIRouter(prefix="/designs", tags=["designs"])


async def process_design_job_background(job_id: int):
    """Background task to process design job."""
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        design_service = DesignJobService(session)
        await design_service.process_job(job_id)


@router.post("", response_model=DesignJobResponse, status_code=status.HTTP_201_CREATED)
async def create_design_job(
    job_data: DesignJobCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new AI design job.
    
    The job will be queued for async processing. Use GET /designs/{id} to check status.
    """
    design_service = DesignJobService(db)
    job = await design_service.create_job(current_user.id, job_data)

    # Queue job for background processing
    # In production, use Celery or other queue system
    background_tasks.add_task(process_design_job_background, job.id)

    return job


@router.get("/{job_id}", response_model=DesignJobResponse)
async def get_design_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get design job by ID.
    
    Returns job details including status and results if completed.
    """
    design_service = DesignJobService(db)
    job = await design_service.get_job(job_id, user_id=current_user.id)
    return job


@router.get("", response_model=DesignJobListResponse)
async def list_design_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[JobStatus] = Query(None, description="Filter by status"),
    user_id: Optional[int] = Query(None, description="Filter by user ID (admin only)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List design jobs.
    
    Returns paginated list of design jobs. Users can only see their own jobs.
    Admins can filter by user_id.
    """
    design_service = DesignJobService(db)

    # If user_id is provided and user is admin, use that user_id
    # Otherwise, use current user's ID
    target_user_id = user_id if user_id and current_user.is_active else current_user.id

    jobs, total = await design_service.get_user_jobs(
        user_id=target_user_id,
        page=page,
        page_size=page_size,
        status_filter=status,
    )

    return DesignJobListResponse(
        jobs=jobs,
        total=total,
        page=page,
        page_size=page_size,
    )

