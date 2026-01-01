from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class SubscriptionPlan(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    FREE = "free"  # Default free tier


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"
    TRIAL = "trial"
    PAST_DUE = "past_due"  # Payment failed but still active


class BillingProvider(str, enum.Enum):
    STRIPE = "stripe"
    APP_STORE = "app_store"
    GOOGLE_PLAY = "google_play"
    MANUAL = "manual"  # Admin/manual subscription


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    plan = Column(SQLEnum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False)
    
    # Billing information
    billing_provider = Column(SQLEnum(BillingProvider), nullable=True)
    provider_subscription_id = Column(String, nullable=True, index=True)  # Stripe subscription ID, etc.
    provider_customer_id = Column(String, nullable=True)  # Stripe customer ID, etc.
    
    # Subscription dates
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    canceled_at = Column(DateTime(timezone=True), nullable=True)
    trial_end = Column(DateTime(timezone=True), nullable=True)
    
    # Quota limits (AI jobs per period)
    ai_job_quota = Column(Integer, default=0, nullable=False)  # Total quota for current period
    ai_jobs_used = Column(BigInteger, default=0, nullable=False)  # Jobs used in current period
    
    # Metadata
    subscription_metadata = Column(String, nullable=True)  # JSON string for additional data
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user = relationship("User", backref="subscription", uselist=False)


# Plan configurations
PLAN_QUOTAS = {
    SubscriptionPlan.FREE: {
        "ai_job_quota": 10,  # 10 AI jobs per month
        "price": 0,
    },
    SubscriptionPlan.WEEKLY: {
        "ai_job_quota": 100,  # 100 AI jobs per week
        "price": 9.99,
    },
    SubscriptionPlan.MONTHLY: {
        "ai_job_quota": 500,  # 500 AI jobs per month
        "price": 29.99,
    },
    SubscriptionPlan.YEARLY: {
        "ai_job_quota": 6000,  # 6000 AI jobs per year (500/month)
        "price": 299.99,
    },
}


