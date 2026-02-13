from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any
from uuid import uuid4

from ..core.events import InMemoryEventStore
from ..core.idempotency import InMemoryIdempotencyStore
from ..core.lifecycle import TaskStatus, can_transition
from ..core.metrics import MetricsCollector
from ..core.orchestrator import TaskOrchestrator
from ..core.policy import RiskLevel
from ..core.queueing import InMemoryTaskQueue, TaskMessage
from ..core.quotas import QuotaManager
from ..core.routing import TaskContext


@dataclass
class TaskRecord:
    task_id: str
    tenant_id: str
    status: TaskStatus
    idempotency_key: str
    agent: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class SubmitResult:
    accepted: bool
    reason: str
    record: TaskRecord


class RuntimeService:
    def __init__(self) -> None:
        self.events = InMemoryEventStore()
        self.queue = InMemoryTaskQueue()
        self.metrics = MetricsCollector()
        self.quotas = QuotaManager()
        self.orchestrator = TaskOrchestrator(InMemoryIdempotencyStore())
        self.tasks: dict[str, TaskRecord] = {}

    def submit_task(self, task: Any) -> SubmitResult:
        quota = self.quotas.check_and_consume(task.tenant_id, task.estimated_cost)
        task_id = str(uuid4())

        if not quota.allowed:
            rec = TaskRecord(
                task_id=task_id,
                tenant_id=task.tenant_id,
                status=TaskStatus.rejected,
                idempotency_key="",
            )
            self.tasks[task_id] = rec
            self.events.append(task_id, task.tenant_id, "task_rejected", {"reason": quota.reason})
            return SubmitResult(False, quota.reason, rec)

        orchestration = self.orchestrator.orchestrate(
            TaskContext(title=task.title, description=task.description, domain_hint=task.domain_hint),
            tenant_id=task.tenant_id,
            risk_level=RiskLevel.high if task.contains_pii else RiskLevel.medium,
            contains_pii=task.contains_pii,
        )
        rec = TaskRecord(
            task_id=task_id,
            tenant_id=task.tenant_id,
            status=TaskStatus.submitted,
            idempotency_key=orchestration.idempotency_key,
            agent=orchestration.routing.agent_id,
        )
        self.tasks[task_id] = rec
        self.events.append(task_id, task.tenant_id, "task_submitted", {"agent": rec.agent})

        self._transition(task_id, TaskStatus.routed)
        self.queue.publish(TaskMessage(task_id=task_id, tenant_id=task.tenant_id, idempotency_key=rec.idempotency_key))
        self._transition(task_id, TaskStatus.queued)

        return SubmitResult(True, "accepted", self.tasks[task_id])

    def process_next(self) -> TaskRecord | None:
        msg = self.queue.consume_nowait()
        if not msg:
            return None
        self._transition(msg.task_id, TaskStatus.processing)
        self._transition(msg.task_id, TaskStatus.completed)
        return self.tasks[msg.task_id]

    def _transition(self, task_id: str, new_status: TaskStatus) -> None:
        rec = self.tasks[task_id]
        if can_transition(rec.status, new_status):
            rec.status = new_status
            self.events.append(task_id, rec.tenant_id, "status_changed", {"status": new_status.value})

    def get_task(self, task_id: str) -> TaskRecord | None:
        return self.tasks.get(task_id)
