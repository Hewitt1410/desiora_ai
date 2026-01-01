from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.services.plan_service import PlanService
from app.schemas.plan import PlanResponse, PlanListResponse

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("", response_model=PlanListResponse)
async def get_plans(
    active_only: bool = Query(True, description="Filter active plans only"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all subscription plans (Public endpoint).
    
    Returns list of available subscription plans for public viewing.
    """
    plan_service = PlanService(db)
    plans = await plan_service.get_all_plans(active_only=active_only)
    
    plan_responses = [
        PlanResponse(
            id=plan.id,
            name=plan.name,
            display_name=plan.display_name,
            description=plan.description,
            price=plan.price,
            currency=plan.currency,
            ai_job_quota=plan.ai_job_quota,
            period_days=plan.period_days,
            is_active=plan.is_active,
            is_default=plan.is_default,
            sort_order=plan.sort_order,
            features=plan.features,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
        )
        for plan in plans
    ]
    
    return PlanListResponse(plans=plan_responses, total=len(plan_responses))

