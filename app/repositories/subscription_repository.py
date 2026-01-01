from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from datetime import datetime, timedelta


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
        """Get subscription by user ID."""
        result = await self.session.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_provider_id(self, provider_subscription_id: str) -> Optional[Subscription]:
        """Get subscription by provider subscription ID."""
        result = await self.session.execute(
            select(Subscription).where(
                Subscription.provider_subscription_id == provider_subscription_id
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: int,
        plan: SubscriptionPlan,
        status: SubscriptionStatus = SubscriptionStatus.ACTIVE,
        billing_provider: Optional[str] = None,
        provider_subscription_id: Optional[str] = None,
        provider_customer_id: Optional[str] = None,
        period_days: Optional[int] = None,
    ) -> Subscription:
        """Create a new subscription."""
        from app.models.subscription import PLAN_QUOTAS
        
        quota = PLAN_QUOTAS.get(plan, {}).get("ai_job_quota", 0)
        
        # Get enum values as strings
        plan_value = plan.value if hasattr(plan, 'value') else str(plan)
        status_value = status.value if hasattr(status, 'value') else str(status)
        
        # Calculate period dates
        now = datetime.now(timezone.utc)
        if period_days:
            period_end = now + timedelta(days=period_days)
        else:
            # Default periods based on plan
            if plan == SubscriptionPlan.WEEKLY:
                period_end = now + timedelta(days=7)
            elif plan == SubscriptionPlan.MONTHLY:
                period_end = now + timedelta(days=30)
            elif plan == SubscriptionPlan.YEARLY:
                period_end = now + timedelta(days=365)
            else:
                period_end = now + timedelta(days=30)  # Default to monthly

        subscription = Subscription(
            user_id=user_id,
            plan=plan_value,  # Use string value
            status=status_value,  # Use string value
            billing_provider=billing_provider,
            provider_subscription_id=provider_subscription_id,
            provider_customer_id=provider_customer_id,
            current_period_start=now,
            current_period_end=period_end,
            ai_job_quota=quota,
            ai_jobs_used=0,
        )
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def update(self, subscription: Subscription) -> Subscription:
        """Update subscription."""
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def cancel(self, subscription: Subscription, reason: Optional[str] = None) -> Subscription:
        """Cancel subscription."""
        subscription.status = SubscriptionStatus.CANCELED.value
        subscription.canceled_at = datetime.now(timezone.utc)
        
        import json
        metadata = {}
        if subscription.subscription_metadata:
            try:
                metadata = json.loads(subscription.subscription_metadata)
            except:
                pass
        metadata["cancellation_reason"] = reason
        subscription.subscription_metadata = json.dumps(metadata)
        
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def update_quota_usage(self, subscription: Subscription, jobs_used: int) -> Subscription:
        """Update AI job quota usage."""
        subscription.ai_jobs_used = jobs_used
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def reset_period(self, subscription: Subscription, period_days: Optional[int] = None) -> Subscription:
        """Reset subscription period and quota usage."""
        from app.models.subscription import PLAN_QUOTAS
        
        quota = PLAN_QUOTAS.get(subscription.plan, {}).get("ai_job_quota", 0)
        
        now = datetime.now(timezone.utc)
        if period_days:
            period_end = now + timedelta(days=period_days)
        else:
            if subscription.plan == SubscriptionPlan.WEEKLY:
                period_end = now + timedelta(days=7)
            elif subscription.plan == SubscriptionPlan.MONTHLY:
                period_end = now + timedelta(days=30)
            elif subscription.plan == SubscriptionPlan.YEARLY:
                period_end = now + timedelta(days=365)
            else:
                period_end = now + timedelta(days=30)

        subscription.current_period_start = now
        subscription.current_period_end = period_end
        subscription.ai_job_quota = quota
        subscription.ai_jobs_used = 0
        
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription


