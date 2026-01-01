from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.subscription import SubscriptionResponse
from app.schemas.design import DesignJobResponse
from app.models.user import UserRole
from app.models.subscription import SubscriptionPlan, SubscriptionStatus
from app.models.design_job import JobStatus


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int = 1
    page_size: int = 20


class SubscriptionListResponse(BaseModel):
    subscriptions: List[SubscriptionResponse]
    total: int
    page: int = 1
    page_size: int = 20


class DesignJobListResponse(BaseModel):
    jobs: List[DesignJobResponse]
    total: int
    page: int = 1
    page_size: int = 20


class UsageStatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_subscriptions: int
    subscriptions_by_plan: Dict[str, int]
    subscriptions_by_status: Dict[str, int]
    total_jobs: int
    jobs_by_status: Dict[str, int]
    total_ai_jobs_used: int
    total_ai_jobs_quota: int
    average_jobs_per_user: float
    top_users_by_jobs: List[Dict[str, Any]]


class AdminStatsResponse(BaseModel):
    users: Dict[str, int]
    subscriptions: Dict[str, Any]
    jobs: Dict[str, Any]
    usage: Dict[str, Any]
    generated_at: datetime


