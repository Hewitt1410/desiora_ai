from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base


class SubscriptionPlanModel(Base):
    """Database model for subscription plans."""
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)  # e.g., "weekly", "monthly", "yearly", "free"
    display_name = Column(String, nullable=False)  # e.g., "Weekly Plan", "Monthly Plan"
    description = Column(String, nullable=True)
    
    # Pricing
    price = Column(Numeric(10, 2), default=0, nullable=False)  # Price in USD
    currency = Column(String, default="USD", nullable=False)
    
    # Quota
    ai_job_quota = Column(Integer, default=0, nullable=False)  # AI jobs per period
    period_days = Column(Integer, nullable=False)  # Billing period in days (7 for weekly, 30 for monthly, etc.)
    
    # Features
    is_active = Column(Boolean, default=True, nullable=False)  # Whether plan is available for purchase
    is_default = Column(Boolean, default=False, nullable=False)  # Default plan (usually free)
    sort_order = Column(Integer, default=0, nullable=False)  # Display order
    
    # Metadata
    features = Column(String, nullable=True)  # JSON string for additional features
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

