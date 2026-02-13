from fastapi import APIRouter

from ..core.routing import TaskContext, route_task
from ..models.task import TaskRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/route")
def route(task: TaskRequest):
    decision = route_task(
        TaskContext(
            title=task.title,
            description=task.description,
            domain_hint=task.domain_hint,
        )
    )
    return {
        "agent": decision.agent_id,
        "reason": decision.reason,
        "required_skills": decision.required_skills,
    }
