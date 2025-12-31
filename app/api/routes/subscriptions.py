from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.subscription_service import SubscriptionService
from app.schemas.subscription import (
    SubscriptionStatusResponse,
    CancelSubscriptionRequest,
    CancelSubscriptionResponse,
    SubscriptionResponse,
)
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current subscription status and quota information.
    
    Returns:
    - Current subscription details
    - Whether user can use AI job (based on quota)
    - Quota information (quota, used, remaining, percentage)
    """
    subscription_service = SubscriptionService(db)
    return await subscription_service.get_subscription_status(current_user.id)


@router.post("/cancel", response_model=CancelSubscriptionResponse)
async def cancel_subscription(
    request: CancelSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Cancel current subscription.
    
    This will mark the subscription as canceled. The subscription will remain
    active until the end of the current billing period.
    """
    subscription_service = SubscriptionService(db)
    subscription = await subscription_service.cancel_subscription(
        current_user.id,
        reason=request.reason,
    )

    subscription_response = SubscriptionResponse(
        id=subscription.id,
        user_id=subscription.user_id,
        plan=subscription.plan,
        status=subscription.status,
        billing_provider=subscription.billing_provider,
        provider_subscription_id=subscription.provider_subscription_id,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        canceled_at=subscription.canceled_at,
        trial_end=subscription.trial_end,
        ai_job_quota=subscription.ai_job_quota,
        ai_jobs_used=subscription.ai_jobs_used,
        ai_jobs_remaining=max(0, subscription.ai_job_quota - subscription.ai_jobs_used),
        metadata=subscription.metadata,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at,
    )

    return CancelSubscriptionResponse(
        message="Subscription canceled successfully",
        subscription=subscription_response,
    )

