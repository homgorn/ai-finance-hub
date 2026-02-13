from fastapi import APIRouter, Depends

from ..dependencies import get_runtime
from ..services.runtime import RuntimeService

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check(runtime: RuntimeService = Depends(get_runtime)):
    snap = runtime.metrics.snapshot(queue_lag=runtime.queue.lag())
    return {
        "status": "ok",
        "queue_lag": snap.queue_lag,
        "requests_total": snap.requests_total,
        "errors_total": snap.errors_total,
        "p95_latency_ms": snap.p95_latency_ms,
    }
