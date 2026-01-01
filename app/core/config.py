from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Desiora AI"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    REFRESH_SECRET_KEY: Optional[str] = None  # If not set, uses SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None
    
    # Apple OAuth
    APPLE_CLIENT_ID: Optional[str] = None
    APPLE_TEAM_ID: Optional[str] = None
    APPLE_KEY_ID: Optional[str] = None
    APPLE_PRIVATE_KEY: Optional[str] = None
    APPLE_REDIRECT_URI: Optional[str] = None
    
    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = None  # For S3-compatible services (e.g., DigitalOcean Spaces)
    
    # Image Upload
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: list = ["jpg", "jpeg", "png", "heic"]
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # AI Worker
    AI_WORKER_DEVICE: str = "cuda"  # or "cpu"
    AI_WORKER_MODEL_CACHE_DIR: str = "/app/models"
    AI_WORKER_OUTPUT_DIR: str = "/app/outputs"
    
    # Storage
    STORAGE_BACKEND: str = "s3"  # or "local"
    STORAGE_LOCAL_PATH: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

