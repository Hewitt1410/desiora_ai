from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime, timezone
from typing import Optional, Dict, Any
import httpx
import jwt
from app.repositories.user_repository import UserRepository
from app.models.user import OAuthProvider
from app.schemas.auth import Token
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from fastapi import HTTPException, status


class OAuthService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def authenticate_google(self, code: str, redirect_uri: Optional[str] = None) -> Token:
        """Authenticate user with Google OAuth."""
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google OAuth not configured"
            )

        redirect_uri = redirect_uri or settings.GOOGLE_REDIRECT_URI
        if not redirect_uri:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Redirect URI is required"
            )

        # Exchange code for token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )

            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to exchange Google OAuth code"
                )

            token_data = token_response.json()
            access_token = token_data["access_token"]

            # Get user info
            user_info_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if user_info_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to get Google user info"
                )

            user_info = user_info_response.json()
            google_id = user_info["id"]
            email = user_info["email"]
            full_name = user_info.get("name")
            given_name = user_info.get("given_name", "")
            family_name = user_info.get("family_name", "")

        # Check if user exists
        user = await self.user_repo.get_by_oauth(google_id, OAuthProvider.GOOGLE)
        
        if not user:
            # Check if email already exists
            existing_user = await self.user_repo.get_by_email(email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered with different provider"
                )
            
            # Create new user
            username = email.split("@")[0] if email else None
            user = await self.user_repo.create_oauth_user(
                email=email,
                oauth_id=google_id,
                provider=OAuthProvider.GOOGLE,
                full_name=full_name or f"{given_name} {family_name}".strip(),
                username=username,
            )

        # Generate JWT tokens
        jwt_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_refresh_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return Token(access_token=jwt_token, refresh_token=refresh_token)

    async def authenticate_apple(self, code: str, redirect_uri: Optional[str] = None) -> Token:
        """Authenticate user with Apple OAuth."""
        if not all([
            settings.APPLE_CLIENT_ID,
            settings.APPLE_TEAM_ID,
            settings.APPLE_KEY_ID,
            settings.APPLE_PRIVATE_KEY,
        ]):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Apple OAuth not configured"
            )

        redirect_uri = redirect_uri or settings.APPLE_REDIRECT_URI
        if not redirect_uri:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Redirect URI is required"
            )

        # Create client secret (JWT)
        client_secret = self._create_apple_client_secret()

        # Exchange code for token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://appleid.apple.com/auth/token",
                data={
                    "code": code,
                    "client_id": settings.APPLE_CLIENT_ID,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )

            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to exchange Apple OAuth code"
                )

            token_data = token_response.json()
            id_token = token_data.get("id_token")

            if not id_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No ID token received from Apple"
                )

            # Decode ID token (Apple doesn't verify, we just decode)
            # In production, you should verify the token signature
            try:
                decoded_token = jwt.decode(
                    id_token,
                    options={"verify_signature": False}  # Apple tokens need special verification
                )
            except jwt.DecodeError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Apple ID token"
                )

            apple_id = decoded_token.get("sub")
            email = decoded_token.get("email")
            full_name = decoded_token.get("name")

            if not apple_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No user ID in Apple token"
                )

        # Check if user exists
        user = await self.user_repo.get_by_oauth(apple_id, OAuthProvider.APPLE)

        if not user:
            # Check if email already exists
            if email:
                existing_user = await self.user_repo.get_by_email(email)
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered with different provider"
                    )

            # Create new user
            username = email.split("@")[0] if email else None
            user = await self.user_repo.create_oauth_user(
                email=email or f"{apple_id}@apple.oauth",  # Apple may not provide email
                oauth_id=apple_id,
                provider=OAuthProvider.APPLE,
                full_name=full_name,
                username=username,
            )

        # Generate JWT tokens
        jwt_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_refresh_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return Token(access_token=jwt_token, refresh_token=refresh_token)

    def _create_apple_client_secret(self) -> str:
        """Create Apple client secret JWT."""
        headers = {
            "kid": settings.APPLE_KEY_ID,
            "alg": "ES256",
        }

        now = datetime.now(timezone.utc)
        payload = {
            "iss": settings.APPLE_TEAM_ID,
            "iat": int(now.timestamp()),
            "exp": int(now.timestamp()) + 3600,  # 1 hour expiration
            "aud": "https://appleid.apple.com",
            "sub": settings.APPLE_CLIENT_ID,
        }

        # Load private key
        private_key = settings.APPLE_PRIVATE_KEY
        if private_key.startswith("-----BEGIN"):
            # Already formatted
            key = private_key
        else:
            # Format the key
            key = f"-----BEGIN PRIVATE KEY-----\n{private_key}\n-----END PRIVATE KEY-----"

        try:
            token = jwt.encode(payload, key, algorithm="ES256", headers=headers)
            return token
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create Apple client secret: {str(e)}"
            )

