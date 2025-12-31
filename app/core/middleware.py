from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Optional
from app.core.security import decode_access_token
from app.core.database import AsyncSessionLocal
from app.repositories.user_repository import UserRepository

security = HTTPBearer(auto_error=False)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to protect routes by validating JWT tokens.
    Can be applied globally or to specific routes.
    """
    
    def __init__(self, app, exclude_paths: Optional[list] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/api/health",
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/oauth/google",
            "/api/auth/oauth/apple",
            "/api/auth/refresh",
            "/docs",
            "/redoc",
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and validate authentication if needed."""
        # Skip authentication for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Extract token from Authorization header
        authorization: Optional[str] = request.headers.get("Authorization")
        if not authorization:
            return Response(
                content='{"detail":"Not authenticated"}',
                status_code=status.HTTP_401_UNAUTHORIZED,
                media_type="application/json",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Parse Bearer token
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise ValueError()
        except ValueError:
            return Response(
                content='{"detail":"Invalid authentication scheme"}',
                status_code=status.HTTP_401_UNAUTHORIZED,
                media_type="application/json",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Decode and validate token
        payload = decode_access_token(token)
        if payload is None:
            return Response(
                content='{"detail":"Invalid or expired token"}',
                status_code=status.HTTP_401_UNAUTHORIZED,
                media_type="application/json",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify user exists and is active
        user_id: int = payload.get("user_id")
        if user_id is None:
            return Response(
                content='{"detail":"Invalid token payload"}',
                status_code=status.HTTP_401_UNAUTHORIZED,
                media_type="application/json",
            )

        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_id(user_id)
            
            if user is None:
                return Response(
                    content='{"detail":"User not found"}',
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    media_type="application/json",
                )

            if not user.is_active:
                return Response(
                    content='{"detail":"User account is inactive"}',
                    status_code=status.HTTP_403_FORBIDDEN,
                    media_type="application/json",
                )

            # Attach user to request state for use in route handlers
            request.state.user = user
            request.state.user_id = user_id

        return await call_next(request)

