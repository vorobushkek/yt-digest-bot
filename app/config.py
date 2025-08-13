"""Application configuration settings."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # FastAPI Configuration
    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    FASTAPI_DEBUG: bool = False
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN: str
    
    # YouTube API Configuration
    YT_API_KEY: str
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/yt_digest_bot"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Security
    SECRET_KEY: str = "your_secret_key_change_this_in_production"
    
    # Digest Settings
    MAX_VIDEOS_PER_DIGEST: int = 10
    DIGEST_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()
