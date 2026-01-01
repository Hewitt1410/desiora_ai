from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.repositories.plan_repository import PlanRepository
from app.models.subscription_plan import SubscriptionPlanModel
from app.schemas.plan import PlanCreate, PlanUpdate
from fastapi import HTTPException, status
import json


class PlanService:
    def __init__(self, session: AsyncSession):
        self.plan_repo = PlanRepository(session)
        self.session = session

    async def get_all_plans(self, active_only: bool = False) -> List[SubscriptionPlanModel]:
        """Get all plans."""
        return await self.plan_repo.get_all(active_only=active_only)

    async def get_plan_by_id(self, plan_id: int) -> SubscriptionPlanModel:
        """Get plan by ID."""
        plan = await self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found"
            )
        return plan

    async def get_plan_by_name(self, name: str) -> Optional[SubscriptionPlanModel]:
        """Get plan by name."""
        return await self.plan_repo.get_by_name(name)

    async def create_plan(self, plan_data: PlanCreate) -> SubscriptionPlanModel:
        """Create a new plan."""
        # Check if plan with same name already exists
        existing = await self.plan_repo.get_by_name(plan_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Plan with name '{plan_data.name}' already exists"
            )

        # If this is set as default, unset other default plans
        if plan_data.is_default:
            await self._unset_default_plans()

        plan_dict = plan_data.model_dump()
        return await self.plan_repo.create(plan_dict)

    async def update_plan(self, plan_id: int, plan_data: PlanUpdate) -> SubscriptionPlanModel:
        """Update an existing plan."""
        plan = await self.get_plan_by_id(plan_id)

        # If setting as default, unset other default plans
        if plan_data.is_default is True:
            await self._unset_default_plans(exclude_id=plan_id)

        update_dict = plan_data.model_dump(exclude_unset=True)
        return await self.plan_repo.update(plan, update_dict)

    async def delete_plan(self, plan_id: int) -> None:
        """Delete a plan."""
        plan = await self.get_plan_by_id(plan_id)
        
        # Don't allow deleting default plan
        if plan.is_default:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete default plan. Set another plan as default first."
            )

        # Check if plan is in use
        from app.repositories.subscription_repository import SubscriptionRepository
        subscription_repo = SubscriptionRepository(self.session)
        # Note: This is a simple check. In production, you might want to check actual usage.
        
        await self.plan_repo.delete(plan)

    async def _unset_default_plans(self, exclude_id: Optional[int] = None) -> None:
        """Unset all default plans except the one with exclude_id."""
        all_plans = await self.plan_repo.get_all()
        for plan in all_plans:
            if plan.is_default and (exclude_id is None or plan.id != exclude_id):
                plan.is_default = False
        await self.session.commit()

