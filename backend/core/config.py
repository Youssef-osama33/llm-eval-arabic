"""
Application configuration — loaded from environment variables / .env file.
All secrets must be configured via environment — nothing is hardcoded.
"""

from functools import lru_cache
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────
    APP_NAME: str = "LLM-Eval-Arabic"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # ── Server ───────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://llm-eval-arabic.dev",
    ]

    # ── Database ─────────────────────────────────────
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:password@localhost:5432/llm_eval"
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO: bool = False

    # ── Redis ────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL_SECONDS: int = 3600

    # ── Security ─────────────────────────────────────
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    API_KEY_LENGTH: int = 32
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # ── LLM Provider Keys ────────────────────────────
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""

    # ── Evaluation ───────────────────────────────────
    DEFAULT_MAX_TOKENS: int = 1024
    DEFAULT_TEMPERATURE: float = 0.3
    EVALUATION_TIMEOUT_SECONDS: int = 120
    MAX_PARALLEL_MODELS: int = 6

    # ── Judge ────────────────────────────────────────
    JUDGE_MODEL: str = "gpt-4o"
    JUDGE_TEMPERATURE: float = 0.0

    # ── Rate Limiting ────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_EVALS_PER_HOUR: int = 100

    # ── Logging ──────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def sync_database_url(self) -> str:
        """Synchronous URL used only by Alembic."""
        return self.DATABASE_URL.replace("+asyncpg", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
