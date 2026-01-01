from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.services.admin_service import AdminService
from app.schemas.admin import (
    UserListResponse,
    SubscriptionListResponse,
    DesignJobListResponse,
    UsageStatsResponse,
    AdminStatsResponse,
)
from app.schemas.user import UserResponse
from app.schemas.subscription import SubscriptionResponse
from app.schemas.design import DesignJobResponse
from app.api.dependencies import get_admin_user
from app.models.user import User, UserRole
from app.models.subscription import SubscriptionPlan, SubscriptionStatus
from app.models.design_job import JobStatus

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    role: Optional[UserRole] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get users list (Admin only).
    
    Returns paginated list of users with optional filters.
    """
    admin_service = AdminService(db)
    users, total = await admin_service.get_users(
        page=page,
        page_size=page_size,
        role=role,
        is_active=is_active,
    )
    
    user_responses = [
        UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role,
            oauth_provider=user.oauth_provider,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]
    
    return UserListResponse(
        users=user_responses,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/subscriptions", response_model=SubscriptionListResponse)
async def get_subscriptions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    plan: Optional[SubscriptionPlan] = Query(None, description="Filter by plan"),
    status: Optional[SubscriptionStatus] = Query(None, description="Filter by status"),
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get subscriptions list (Admin only).
    
    Returns paginated list of subscriptions with optional filters.
    """
    admin_service = AdminService(db)
    subscriptions, total = await admin_service.get_subscriptions(
        page=page,
        page_size=page_size,
        plan=plan,
        status=status,
    )
    
    subscription_responses = [
        SubscriptionResponse(
            id=sub.id,
            user_id=sub.user_id,
            plan=sub.plan,
            status=sub.status,
            billing_provider=sub.billing_provider,
            provider_subscription_id=sub.provider_subscription_id,
            current_period_start=sub.current_period_start,
            current_period_end=sub.current_period_end,
            canceled_at=sub.canceled_at,
            trial_end=sub.trial_end,
            ai_job_quota=sub.ai_job_quota,
            ai_jobs_used=sub.ai_jobs_used,
            ai_jobs_remaining=max(0, sub.ai_job_quota - sub.ai_jobs_used),
            subscription_metadata=sub.subscription_metadata,
            created_at=sub.created_at,
            updated_at=sub.updated_at,
        )
        for sub in subscriptions
    ]
    
    return SubscriptionListResponse(
        subscriptions=subscription_responses,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/jobs", response_model=DesignJobListResponse)
async def get_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[JobStatus] = Query(None, description="Filter by status"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get design jobs list (Admin only).
    
    Returns paginated list of design jobs with optional filters.
    """
    admin_service = AdminService(db)
    jobs, total = await admin_service.get_design_jobs(
        page=page,
        page_size=page_size,
        status=status,
        user_id=user_id,
    )
    
    job_responses = [
        DesignJobResponse(
            id=job.id,
            user_id=job.user_id,
            job_type=job.job_type,
            prompt=job.prompt,
            status=job.status,
            parameters=job.parameters,
            result_urls=job.result_urls,
            result_metadata=job.result_metadata,
            error_message=job.error_message,
            retry_count=job.retry_count,
            max_retries=job.max_retries,
            started_at=job.started_at,
            completed_at=job.completed_at,
            processing_time_seconds=job.processing_time_seconds,
            queue_id=job.queue_id,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        for job in jobs
    ]
    
    return DesignJobListResponse(
        jobs=job_responses,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/stats", response_model=AdminStatsResponse)
async def get_stats(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get comprehensive admin statistics (Admin only).
    
    Returns usage statistics including:
    - User statistics
    - Subscription statistics
    - Job statistics
    - Usage metrics
    """
    admin_service = AdminService(db)
    stats = await admin_service.get_comprehensive_stats()
    
    return AdminStatsResponse(**stats)


@router.get("/stats/usage", response_model=UsageStatsResponse)
async def get_usage_stats(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get detailed usage statistics (Admin only).
    
    Returns detailed usage metrics including top users.
    """
    admin_service = AdminService(db)
    stats = await admin_service.get_usage_statistics()
    
    return UsageStatsResponse(**stats)

