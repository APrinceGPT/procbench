"""
Configuration management for ProcBench backend.
Loads settings from environment variables.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server settings
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8080, alias="PORT")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    
    # AI Configuration (OpenAI-compatible)
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        alias="OPENAI_BASE_URL"
    )
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", alias="OPENAI_MODEL")
    
    # Rate limiting
    ai_rate_limit_requests: int = Field(default=10, alias="AI_RATE_LIMIT_REQUESTS")
    ai_batch_size: int = Field(default=15, alias="AI_BATCH_SIZE")
    ai_timeout_seconds: int = Field(default=30, alias="AI_TIMEOUT_SECONDS")
    ai_max_retries: int = Field(default=3, alias="AI_MAX_RETRIES")
    
    # File limits
    max_file_size_mb: int = Field(default=500, alias="MAX_FILE_SIZE_MB")
    max_concurrent_analyses: int = Field(default=10, alias="MAX_CONCURRENT_ANALYSES")
    
    # Paths
    rules_path: Path = Field(
        default=Path(__file__).parent.parent / "rules",
        alias="RULES_PATH"
    )
    
    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        alias="CORS_ORIGINS"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    @property
    def max_file_size_bytes(self) -> int:
        """Get max file size in bytes."""
        return self.max_file_size_mb * 1024 * 1024


def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
