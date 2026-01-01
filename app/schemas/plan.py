from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal


class PlanCreate(BaseModel):
    """Schema for creating a subscription plan."""
    name: str = Field(..., description="Plan identifier (e.g., 'weekly', 'monthly')")
    display_name: str = Field(..., description="Display name (e.g., 'Weekly Plan')")
    description: Optional[str] = Field(None, description="Plan description")
    price: Decimal = Field(..., ge=0, description="Price in USD")
    currency: str = Field("USD", description="Currency code")
    ai_job_quota: int = Field(..., ge=0, description="AI jobs quota per period")
    period_days: int = Field(..., ge=1, description="Billing period in days")
    is_active: bool = Field(True, description="Whether plan is available")
    is_default: bool = Field(False, description="Whether this is the default plan")
    sort_order: int = Field(0, description="Display order")
    features: Optional[Dict[str, Any]] = Field(None, description="Additional features")


class PlanUpdate(BaseModel):
    """Schema for updating a subscription plan."""
    display_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = None
    ai_job_quota: Optional[int] = Field(None, ge=0)
    period_days: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    sort_order: Optional[int] = None
    features: Optional[Dict[str, Any]] = None


class PlanResponse(BaseModel):
    """Schema for subscription plan response."""
    id: int
    name: str
    display_name: str
    description: Optional[str]
    price: Decimal
    currency: str
    ai_job_quota: int
    period_days: int
    is_active: bool
    is_default: bool
    sort_order: int
    features: Optional[str]  # JSON string
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PlanListResponse(BaseModel):
    """Schema for list of plans."""
    plans: list[PlanResponse]
    total: int

