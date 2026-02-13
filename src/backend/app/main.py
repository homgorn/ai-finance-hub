import time
import uuid

from fastapi import FastAPI, Request

from .config import settings
from .dependencies import get_runtime
from .routers import agents, health, security, tasks

app = FastAPI(title=settings.app_name)


@app.middleware("http")
async def correlation_and_metrics_middleware(request: Request, call_next):
    runtime = get_runtime()
    correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
    start = time.perf_counter()
    error = False
    try:
        response = await call_next(request)
        return response
    except Exception:
        error = True
        raise
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        runtime.metrics.observe_request(elapsed_ms, error=error)
        # expose correlation id in response path when available
        if 'response' in locals():
            response.headers["x-correlation-id"] = correlation_id


app.include_router(health.router)
app.include_router(agents.router)
app.include_router(tasks.router)
app.include_router(security.router)
