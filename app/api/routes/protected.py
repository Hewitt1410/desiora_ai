from fastapi import APIRouter, Depends, Request
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from pydantic import BaseModel

router = APIRouter(prefix="/protected", tags=["protected"])


class ProtectedResponse(BaseModel):
    message: str
    user_id: int
    user_email: str


@router.get("/example", response_model=ProtectedResponse)
async def protected_example(
    current_user: User = Depends(get_current_user)
):
    """
    Example protected route using dependency injection.
    Requires valid JWT token in Authorization header.
    """
    return ProtectedResponse(
        message="This is a protected route",
        user_id=current_user.id,
        user_email=current_user.email
    )


@router.get("/middleware-example", response_model=ProtectedResponse)
async def middleware_protected_example(request: Request):
    """
    Example protected route using middleware.
    The user is available in request.state.user
    """
    user = request.state.user
    return ProtectedResponse(
        message="This route is protected by middleware",
        user_id=user.id,
        user_email=user.email
    )


@router.get("/user-profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile (protected route example)."""
    return current_user

