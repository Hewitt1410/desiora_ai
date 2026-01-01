from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from app.models.subscription_plan import SubscriptionPlanModel
import json


class PlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, active_only: bool = False) -> List[SubscriptionPlanModel]:
        """Get all plans, optionally filtered by active status."""
        query = select(SubscriptionPlanModel)
        if active_only:
            query = query.where(SubscriptionPlanModel.is_active == True)
        query = query.order_by(SubscriptionPlanModel.sort_order, SubscriptionPlanModel.name)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, plan_id: int) -> Optional[SubscriptionPlanModel]:
        """Get plan by ID."""
        result = await self.session.execute(
            select(SubscriptionPlanModel).where(SubscriptionPlanModel.id == plan_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[SubscriptionPlanModel]:
        """Get plan by name."""
        result = await self.session.execute(
            select(SubscriptionPlanModel).where(SubscriptionPlanModel.name == name)
        )
        return result.scalar_one_or_none()

    async def create(self, plan_data: dict) -> SubscriptionPlanModel:
        """Create a new plan."""
        # Convert features dict to JSON string if provided
        if "features" in plan_data and isinstance(plan_data["features"], dict):
            plan_data["features"] = json.dumps(plan_data["features"])
        
        plan = SubscriptionPlanModel(**plan_data)
        self.session.add(plan)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def update(self, plan: SubscriptionPlanModel, plan_data: dict) -> SubscriptionPlanModel:
        """Update an existing plan."""
        # Convert features dict to JSON string if provided
        if "features" in plan_data and isinstance(plan_data["features"], dict):
            plan_data["features"] = json.dumps(plan_data["features"])
        
        for key, value in plan_data.items():
            if value is not None:
                setattr(plan, key, value)
        
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def delete(self, plan: SubscriptionPlanModel) -> None:
        """Delete a plan."""
        await self.session.delete(plan)
        await self.session.commit()

    async def count(self) -> int:
        """Get total count of plans."""
        result = await self.session.execute(
            select(func.count()).select_from(SubscriptionPlanModel)
        )
        return result.scalar_one()

