from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.services.oauth_service import OAuthService
from app.schemas.auth import LoginRequest, OAuthTokenRequest, Token, RefreshTokenRequest
from app.schemas.user import UserCreate, UserResponse
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user with email/password."""
    auth_service = AuthService(db)
    return await auth_service.register(user_data)


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login with email/password."""
    auth_service = AuthService(db)
    return await auth_service.login(login_data.email, login_data.password)


@router.post("/oauth/google", response_model=Token)
async def google_oauth(
    oauth_data: OAuthTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate with Google OAuth."""
    oauth_service = OAuthService(db)
    return await oauth_service.authenticate_google(
        code=oauth_data.code,
        redirect_uri=oauth_data.redirect_uri
    )


@router.post("/oauth/apple", response_model=Token)
async def apple_oauth(
    oauth_data: OAuthTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate with Apple OAuth."""
    oauth_service = OAuthService(db)
    return await oauth_service.authenticate_apple(
        code=oauth_data.code,
        redirect_uri=oauth_data.redirect_uri
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token."""
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(refresh_data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information."""
    return current_user

