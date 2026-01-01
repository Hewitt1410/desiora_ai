from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import OAuthProvider, UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = None  # Optional for OAuth users


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: str = UserRole.USER.value
    oauth_provider: OAuthProvider
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

