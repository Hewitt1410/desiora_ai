from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import OAuthProvider


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class OAuthTokenRequest(BaseModel):
    code: str
    provider: OAuthProvider
    redirect_uri: Optional[str] = None

