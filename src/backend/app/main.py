from fastapi import FastAPI

from .config import settings
from .routers import agents, health, security, tasks

app = FastAPI(title=settings.app_name)
app.include_router(health.router)
app.include_router(agents.router)
app.include_router(tasks.router)
app.include_router(security.router)
