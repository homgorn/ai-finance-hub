from enum import Enum

from pydantic import BaseModel, Field

from ..core.lifecycle import TaskStatus
from ..core.routing import TaskDomain


class TaskPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class TaskRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=4000)
    priority: TaskPriority = TaskPriority.normal
    domain_hint: TaskDomain | None = None
    contains_pii: bool = False
    requires_browser: bool = False
    tenant_id: str = Field(default="default", min_length=2, max_length=100)
    estimated_cost: float = Field(default=1.0, ge=0.0)


class TaskRecord(BaseModel):
    task_id: str
    tenant_id: str
    status: TaskStatus
    idempotency_key: str
    agent: str | None = None
