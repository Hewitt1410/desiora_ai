from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
from app.repositories.user_repository import UserRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.design_job_repository import DesignJobRepository
from app.models.user import User, UserRole
from app.models.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from app.models.design_job import DesignJob, JobStatus


class AdminService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.subscription_repo = SubscriptionRepository(session)
        self.design_job_repo = DesignJobRepository(session)
        self.session = session

    async def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
    ) -> Tuple[List[User], int]:
        """Get users with pagination and filters."""
        offset = (page - 1) * page_size
        
        query = select(User)
        count_query = select(func.count()).select_from(User)
        
        # Apply filters
        conditions = []
        if role:
            role_value = role.value if hasattr(role, 'value') else role
            conditions.append(User.role == role_value)
        if is_active is not None:
            conditions.append(User.is_active == is_active)
        
        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))
        
        # Get total count
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()
        
        # Get paginated results
        query = query.order_by(User.created_at.desc()).limit(page_size).offset(offset)
        result = await self.session.execute(query)
        users = list(result.scalars().all())
        
        return users, total

    async def get_subscriptions(
        self,
        page: int = 1,
        page_size: int = 20,
        plan: Optional[SubscriptionPlan] = None,
        status: Optional[SubscriptionStatus] = None,
    ) -> Tuple[List[Subscription], int]:
        """Get subscriptions with pagination and filters."""
        offset = (page - 1) * page_size
        
        query = select(Subscription)
        count_query = select(func.count()).select_from(Subscription)
        
        # Apply filters
        conditions = []
        if plan:
            conditions.append(Subscription.plan == plan)
        if status:
            conditions.append(Subscription.status == status)
        
        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))
        
        # Get total count
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()
        
        # Get paginated results
        query = query.order_by(Subscription.created_at.desc()).limit(page_size).offset(offset)
        result = await self.session.execute(query)
        subscriptions = list(result.scalars().all())
        
        return subscriptions, total

    async def get_design_jobs(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[JobStatus] = None,
        user_id: Optional[int] = None,
    ) -> Tuple[List[DesignJob], int]:
        """Get design jobs with pagination and filters."""
        offset = (page - 1) * page_size
        
        query = select(DesignJob)
        count_query = select(func.count()).select_from(DesignJob)
        
        # Apply filters
        conditions = []
        if status:
            conditions.append(DesignJob.status == status)
        if user_id:
            conditions.append(DesignJob.user_id == user_id)
        
        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))
        
        # Get total count
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()
        
        # Get paginated results
        query = query.order_by(DesignJob.created_at.desc()).limit(page_size).offset(offset)
        result = await self.session.execute(query)
        jobs = list(result.scalars().all())
        
        return jobs, total

    async def get_usage_statistics(self) -> Dict[str, Any]:
        """Get comprehensive usage statistics."""
        # User statistics
        total_users_result = await self.session.execute(
            select(func.count()).select_from(User)
        )
        total_users = total_users_result.scalar_one()
        
        active_users_result = await self.session.execute(
            select(func.count()).select_from(User).where(User.is_active == True)
        )
        active_users = active_users_result.scalar_one()
        
        # Subscription statistics
        total_subscriptions_result = await self.session.execute(
            select(func.count()).select_from(Subscription)
        )
        total_subscriptions = total_subscriptions_result.scalar_one()
        
        # Subscriptions by plan
        subscriptions_by_plan = {}
        for plan in SubscriptionPlan:
            plan_value = plan.value
            # Cast enum to text for comparison (database may still use enum type)
            from sqlalchemy import cast, String as SQLString
            count_result = await self.session.execute(
                select(func.count()).select_from(Subscription).where(
                    cast(Subscription.plan, SQLString) == plan_value
                )
            )
            subscriptions_by_plan[plan_value] = count_result.scalar_one()
        
        # Subscriptions by status
        subscriptions_by_status = {}
        for sub_status in SubscriptionStatus:
            status_value = sub_status.value
            # Cast enum to text for comparison
            from sqlalchemy import cast, String as SQLString
            count_result = await self.session.execute(
                select(func.count()).select_from(Subscription).where(
                    cast(Subscription.status, SQLString) == status_value
                )
            )
            subscriptions_by_status[status_value] = count_result.scalar_one()
        
        # Job statistics
        total_jobs_result = await self.session.execute(
            select(func.count()).select_from(DesignJob)
        )
        total_jobs = total_jobs_result.scalar_one()
        
        # Jobs by status
        jobs_by_status = {}
        for job_status in JobStatus:
            status_value = job_status.value
            # Cast enum to text for comparison (database may still use enum type)
            from sqlalchemy import cast, String as SQLString
            count_result = await self.session.execute(
                select(func.count()).select_from(DesignJob).where(
                    cast(DesignJob.status, SQLString) == status_value
                )
            )
            jobs_by_status[status_value] = count_result.scalar_one()
        
        # AI jobs usage statistics
        total_ai_jobs_used_result = await self.session.execute(
            select(func.sum(Subscription.ai_jobs_used))
        )
        total_ai_jobs_used = total_ai_jobs_used_result.scalar_one() or 0
        
        total_ai_jobs_quota_result = await self.session.execute(
            select(func.sum(Subscription.ai_job_quota))
        )
        total_ai_jobs_quota = total_ai_jobs_quota_result.scalar_one() or 0
        
        # Average jobs per user
        average_jobs_per_user = total_jobs / total_users if total_users > 0 else 0
        
        # Top users by jobs
        top_users_query = (
            select(
                DesignJob.user_id,
                func.count(DesignJob.id).label("job_count")
            )
            .group_by(DesignJob.user_id)
            .order_by(func.count(DesignJob.id).desc())
            .limit(10)
        )
        top_users_result = await self.session.execute(top_users_query)
        top_users_data = top_users_result.all()
        
        top_users = []
        for user_id, job_count in top_users_data:
            user = await self.user_repo.get_by_id(user_id)
            if user:
                top_users.append({
                    "user_id": user_id,
                    "email": user.email,
                    "username": user.username,
                    "job_count": job_count,
                })
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_subscriptions": total_subscriptions,
            "subscriptions_by_plan": subscriptions_by_plan,
            "subscriptions_by_status": subscriptions_by_status,
            "total_jobs": total_jobs,
            "jobs_by_status": jobs_by_status,
            "total_ai_jobs_used": int(total_ai_jobs_used),
            "total_ai_jobs_quota": int(total_ai_jobs_quota),
            "average_jobs_per_user": round(average_jobs_per_user, 2),
            "top_users_by_jobs": top_users,
        }

    async def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive admin statistics."""
        usage_stats = await self.get_usage_statistics()
        
        return {
            "users": {
                "total": usage_stats["total_users"],
                "active": usage_stats["active_users"],
                "inactive": usage_stats["total_users"] - usage_stats["active_users"],
            },
            "subscriptions": {
                "total": usage_stats["total_subscriptions"],
                "by_plan": usage_stats["subscriptions_by_plan"],
                "by_status": usage_stats["subscriptions_by_status"],
            },
            "jobs": {
                "total": usage_stats["total_jobs"],
                "by_status": usage_stats["jobs_by_status"],
                "average_per_user": usage_stats["average_jobs_per_user"],
            },
            "usage": {
                "ai_jobs_used": usage_stats["total_ai_jobs_used"],
                "ai_jobs_quota": usage_stats["total_ai_jobs_quota"],
                "usage_percentage": (
                    (usage_stats["total_ai_jobs_used"] / usage_stats["total_ai_jobs_quota"] * 100)
                    if usage_stats["total_ai_jobs_quota"] > 0
                    else 0
                ),
                "top_users": usage_stats["top_users_by_jobs"],
            },
            "generated_at": datetime.utcnow(),
        }

