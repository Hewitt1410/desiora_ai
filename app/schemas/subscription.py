from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.subscription import (
    SubscriptionPlan,
    SubscriptionStatus,
    BillingProvider,
    PLAN_QUOTAS,
)


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan: SubscriptionPlan
    status: SubscriptionStatus
    billing_provider: Optional[BillingProvider]
    provider_subscription_id: Optional[str]
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    canceled_at: Optional[datetime]
    trial_end: Optional[datetime]
    ai_job_quota: int
    ai_jobs_used: int
    ai_jobs_remaining: int
    metadata: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class SubscriptionStatusResponse(BaseModel):
    subscription: SubscriptionResponse
    can_use_ai_job: bool = Field(..., description="Whether user can use AI job based on quota")
    quota_info: dict = Field(..., description="Quota information")


class CancelSubscriptionRequest(BaseModel):
    reason: Optional[str] = Field(None, description="Optional cancellation reason")


class CancelSubscriptionResponse(BaseModel):
    message: str
    subscription: SubscriptionResponse


class WebhookEvent(BaseModel):
    """Base webhook event model"""
    event_type: str
    provider: BillingProvider
    data: dict


class StripeWebhookEvent(WebhookEvent):
    """Stripe webhook event"""
    provider: BillingProvider = BillingProvider.STRIPE
    stripe_event_id: str
    stripe_subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None


class AppStoreWebhookEvent(WebhookEvent):
    """App Store webhook event"""
    provider: BillingProvider = BillingProvider.APP_STORE
    original_transaction_id: Optional[str] = None
    product_id: Optional[str] = None


class GooglePlayWebhookEvent(WebhookEvent):
    """Google Play webhook event"""
    provider: BillingProvider = BillingProvider.GOOGLE_PLAY
    purchase_token: Optional[str] = None
    product_id: Optional[str] = None

