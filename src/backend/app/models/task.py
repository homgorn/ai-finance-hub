from enum import Enum

from pydantic import BaseModel, Field

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
