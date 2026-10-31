from secrets import compare_digest

from fastapi import Header, HTTPException, status

from .config import settings
from .core.events import InMemoryEventStore, SQLiteEventStore
from .core.idempotency import build_idempotency_store
from .core.queueing import build_task_queue
from .core.quotas import QuotaManager, TenantQuota
from .services.runtime import RuntimeService


def _build_event_store():
    if settings.event_store_backend == "sqlite":
        return SQLiteEventStore(settings.event_store_sqlite_path)
    if settings.event_store_backend == "inmemory":
        return InMemoryEventStore()
    raise ValueError(f"Unsupported event store backend: {settings.event_store_backend}")


def _build_queue():
    return build_task_queue(settings.queue_backend, settings.queue_sqlite_path)


runtime_service = RuntimeService(
    event_store=_build_event_store(),
    task_queue=_build_queue(),
    idempotency_store=build_idempotency_store(settings.idempotency_backend, settings.redis_url),
    quota_manager=QuotaManager(
        default_quota=TenantQuota(
            max_tasks_per_window=settings.default_tenant_task_quota,
            max_budget_per_window=settings.default_tenant_budget_cap,
        )
    ),
)


def get_runtime() -> RuntimeService:
    return runtime_service


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Protect public task APIs when the application is deployed in production."""
    if settings.environment != "production":
        return
    if not settings.api_key or not x_api_key or not compare_digest(x_api_key, settings.api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_api_key")


def require_worker_api_key(x_worker_api_key: str | None = Header(default=None)) -> None:
    """Keep queue consumption separate from ordinary client access."""
    if settings.environment != "production":
        return
    if (
        not settings.worker_api_key
        or not x_worker_api_key
        or not compare_digest(x_worker_api_key, settings.worker_api_key)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_worker_api_key")
