from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from app.repositories.subscription_repository import SubscriptionRepository
from app.models.subscription import (
    Subscription,
    SubscriptionPlan,
    SubscriptionStatus,
    BillingProvider,
    PLAN_QUOTAS,
)
from app.schemas.subscription import SubscriptionResponse, SubscriptionStatusResponse
from fastapi import HTTPException, status


class SubscriptionService:
    def __init__(self, session: AsyncSession):
        self.subscription_repo = SubscriptionRepository(session)

    async def get_or_create_subscription(self, user_id: int) -> Subscription:
        """Get user's subscription or create a free one if doesn't exist."""
        subscription = await self.subscription_repo.get_by_user_id(user_id)
        if not subscription:
            # Create free subscription by default
            subscription = await self.subscription_repo.create(
                user_id=user_id,
                plan=SubscriptionPlan.FREE,
                status=SubscriptionStatus.ACTIVE,
            )
        return subscription

    async def get_subscription_status(self, user_id: int) -> SubscriptionStatusResponse:
        """Get current subscription status with quota information."""
        subscription = await self.get_or_create_subscription(user_id)
        
        # Check if subscription period has expired
        if subscription.current_period_end and subscription.current_period_end < datetime.utcnow():
            if subscription.status == SubscriptionStatus.ACTIVE:
                subscription.status = SubscriptionStatus.EXPIRED
                await self.subscription_repo.update(subscription)
        
        # Calculate remaining quota
        remaining = max(0, subscription.ai_job_quota - subscription.ai_jobs_used)
        can_use = (
            subscription.status == SubscriptionStatus.ACTIVE
            and remaining > 0
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
            ai_jobs_remaining=remaining,
            metadata=subscription.metadata,
            created_at=subscription.created_at,
            updated_at=subscription.updated_at,
        )

        quota_info = {
            "quota": subscription.ai_job_quota,
            "used": subscription.ai_jobs_used,
            "remaining": remaining,
            "percentage_used": (
                (subscription.ai_jobs_used / subscription.ai_job_quota * 100)
                if subscription.ai_job_quota > 0
                else 0
            ),
        }

        return SubscriptionStatusResponse(
            subscription=subscription_response,
            can_use_ai_job=can_use,
            quota_info=quota_info,
        )

    async def cancel_subscription(self, user_id: int, reason: Optional[str] = None) -> Subscription:
        """Cancel user's subscription."""
        subscription = await self.subscription_repo.get_by_user_id(user_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        if subscription.status == SubscriptionStatus.CANCELED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subscription is already canceled"
            )

        subscription = await self.subscription_repo.cancel(subscription, reason)
        return subscription

    async def check_quota(self, user_id: int) -> bool:
        """Check if user has available quota for AI job."""
        subscription = await self.get_or_create_subscription(user_id)
        
        # Check if subscription is active
        if subscription.status != SubscriptionStatus.ACTIVE:
            return False
        
        # Check if period has expired
        if subscription.current_period_end and subscription.current_period_end < datetime.utcnow():
            return False
        
        # Check quota
        remaining = subscription.ai_job_quota - subscription.ai_jobs_used
        return remaining > 0

    async def use_quota(self, user_id: int, amount: int = 1) -> bool:
        """Use quota for AI job. Returns True if successful, False if quota exceeded."""
        subscription = await self.get_or_create_subscription(user_id)
        
        # Check quota first
        if not await self.check_quota(user_id):
            return False
        
        # Update usage
        new_used = subscription.ai_jobs_used + amount
        if new_used > subscription.ai_job_quota:
            return False
        
        await self.subscription_repo.update_quota_usage(subscription, new_used)
        return True

    async def update_subscription_from_webhook(
        self,
        provider_subscription_id: str,
        status: Optional[SubscriptionStatus] = None,
        plan: Optional[SubscriptionPlan] = None,
        period_end: Optional[datetime] = None,
    ) -> Optional[Subscription]:
        """Update subscription from webhook event."""
        subscription = await self.subscription_repo.get_by_provider_id(provider_subscription_id)
        if not subscription:
            return None

        if status:
            subscription.status = status
        if plan:
            from app.models.subscription import PLAN_QUOTAS
            quota = PLAN_QUOTAS.get(plan, {}).get("ai_job_quota", 0)
            subscription.plan = plan
            subscription.ai_job_quota = quota
        if period_end:
            subscription.current_period_end = period_end

        await self.subscription_repo.update(subscription)
        return subscription


