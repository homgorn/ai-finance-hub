import os
from typing import Literal

from pydantic import BaseModel, model_validator


class Settings(BaseModel):
    app_name: str = "AI Finance Hub API"
    environment: Literal["dev", "test", "production"] = "dev"
    api_key: str | None = None
    worker_api_key: str | None = None

    idempotency_backend: Literal["inmemory", "redis"] = "inmemory"
    redis_url: str = "redis://localhost:6379/0"

    queue_backend: Literal["inmemory", "sqlite"] = "inmemory"
    queue_sqlite_path: str = ".runtime/queue.db"

    event_store_backend: Literal["inmemory", "sqlite"] = "inmemory"
    event_store_sqlite_path: str = ".runtime/events.db"

    default_tenant_task_quota: int = 100
    default_tenant_budget_cap: float = 1000.0

    @model_validator(mode="after")
    def require_production_keys(self) -> "Settings":
        if self.environment == "production" and (not self.api_key or not self.worker_api_key):
            raise ValueError("api_key and worker_api_key are required in production")
        return self


def _settings_from_environment() -> Settings:
    values = {
        name: value
        for name in Settings.model_fields
        if (value := os.getenv(f"AI_FINANCE_HUB_{name.upper()}")) is not None
    }
    return Settings(**values)


settings = _settings_from_environment()
