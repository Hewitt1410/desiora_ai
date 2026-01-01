from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user import User, OAuthProvider
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_oauth(self, oauth_id: str, provider: OAuthProvider) -> Optional[User]:
        """Get user by OAuth ID and provider."""
        result = await self.session.execute(
            select(User).where(
                User.oauth_id == oauth_id,
                User.oauth_provider == provider
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate, hashed_password: Optional[str] = None) -> User:
        """Create a new user."""
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_oauth_user(
        self,
        email: str,
        oauth_id: str,
        provider: OAuthProvider,
        full_name: Optional[str] = None,
        username: Optional[str] = None
    ) -> User:
        """Create a new OAuth user."""
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            oauth_provider=provider,
            oauth_id=oauth_id,
            is_verified=True,  # OAuth users are typically verified
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        """Update an existing user."""
        await self.session.commit()
        await self.session.refresh(user)
        return user




