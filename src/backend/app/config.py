from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "AI Finance Hub API"
    environment: str = "dev"
    redis_url: str = "redis://localhost:6379/0"
    queue_backend: str = "inmemory"  # future: rabbitmq|sqs|kafka
    default_tenant_task_quota: int = 100
    default_tenant_budget_cap: float = 1000.0


settings = Settings()
