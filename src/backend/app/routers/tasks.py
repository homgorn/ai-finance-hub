from fastapi import APIRouter, Depends, HTTPException

from ..core.routing import TaskContext, route_task
from ..dependencies import get_runtime
from ..models.task import TaskRequest
from ..services.runtime import RuntimeService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/submit")
def submit(task: TaskRequest, runtime: RuntimeService = Depends(get_runtime)):
    result = runtime.submit_task(task)
    return {
        "accepted": result.accepted,
        "reason": result.reason,
        "task_id": result.record.task_id,
        "status": result.record.status.value,
        "agent": result.record.agent,
        "idempotency_key": result.record.idempotency_key,
    }


@router.post("/process-next")
def process_next(runtime: RuntimeService = Depends(get_runtime)):
    record = runtime.process_next()
    if not record:
        raise HTTPException(status_code=404, detail="queue_empty")
    return {"processed_task_id": record.task_id, "status": record.status.value}


@router.get("/{task_id}")
def get_task(task_id: str, runtime: RuntimeService = Depends(get_runtime)):
    record = runtime.get_task(task_id)
    if not record:
        raise HTTPException(status_code=404, detail="task_not_found")
    return record.to_dict()


@router.post("/route")
def route(task: TaskRequest):
    decision = route_task(TaskContext(title=task.title, description=task.description, domain_hint=task.domain_hint))
    return {"agent": decision.agent_id, "reason": decision.reason, "required_skills": decision.required_skills}
