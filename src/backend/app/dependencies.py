from .config import settings
from .core.events import InMemoryEventStore, SQLiteEventStore
from .core.idempotency import build_idempotency_store
from .core.queueing import InMemoryTaskQueue
from .services.runtime import RuntimeService


def _build_event_store():
    if settings.event_store_backend == "sqlite":
        return SQLiteEventStore(settings.event_store_sqlite_path)
    return InMemoryEventStore()


def _build_queue():
    # Batch-2: in-memory implementation, interface ready for external brokers.
    _ = settings.queue_backend
    return InMemoryTaskQueue()


runtime_service = RuntimeService(
    event_store=_build_event_store(),
    task_queue=_build_queue(),
    idempotency_store=build_idempotency_store(settings.idempotency_backend, settings.redis_url),
)


def get_runtime() -> RuntimeService:
    return runtime_service
