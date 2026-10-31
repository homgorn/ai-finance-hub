from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable
from uuid import uuid4

from ..core.events import EventStore, InMemoryEventStore
from ..core.idempotency import IdempotencyStore, InMemoryIdempotencyStore
from ..core.lifecycle import TaskStatus, can_transition
from ..core.metrics import MetricsCollector
from ..core.orchestrator import TaskOrchestrator
from ..core.policy import RiskLevel
from ..core.queueing import InMemoryTaskQueue, TaskMessage, TaskQueue
from ..core.quotas import QuotaManager
from ..core.routing import TaskContext


@dataclass
class TaskRecord:
    task_id: str
    tenant_id: str
    status: TaskStatus
    idempotency_key: str
    agent: str | None = None
    attempts: int = 0
    last_error: str | None = None

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
    def __init__(
        self,
        *,
        event_store: EventStore | None = None,
        task_queue: TaskQueue | None = None,
        idempotency_store: IdempotencyStore | None = None,
        quota_manager: QuotaManager | None = None,
        max_attempts: int = 3,
    ) -> None:
        self.events = event_store or InMemoryEventStore()
        self.queue = task_queue or InMemoryTaskQueue()
        self.metrics = MetricsCollector()
        self.quotas = quota_manager or QuotaManager()
        self.orchestrator = TaskOrchestrator(idempotency_store or InMemoryIdempotencyStore())
        self.max_attempts = max_attempts
        self.tasks: dict[str, TaskRecord] = {}
        self._tasks_by_idempotency_key: dict[str, str] = {}

    def submit_task(self, task: Any) -> SubmitResult:
        context = TaskContext(title=task.title, description=task.description, domain_hint=task.domain_hint)
        idempotency_key = self.orchestrator.build_idempotency_key(context, task.tenant_id)
        existing_task_id = self._tasks_by_idempotency_key.get(idempotency_key)
        if existing_task_id:
            return SubmitResult(True, "duplicate", self.tasks[existing_task_id])

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
            context,
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
        self._tasks_by_idempotency_key[orchestration.idempotency_key] = task_id
        self.events.append(task_id, task.tenant_id, "task_submitted", {"agent": rec.agent})

        self._transition(task_id, TaskStatus.routed)
        self.queue.publish(TaskMessage(task_id=task_id, tenant_id=task.tenant_id, idempotency_key=rec.idempotency_key))
        self._transition(task_id, TaskStatus.queued)

        return SubmitResult(True, "accepted", self.tasks[task_id])

    def process_next(self, handler: Callable[[TaskRecord], None] | None = None) -> TaskRecord | None:
        msg = self.queue.consume_nowait()
        if not msg:
            return None

        record = self.tasks[msg.task_id]
        self._transition(msg.task_id, TaskStatus.processing)
        record.attempts += 1

        try:
            if handler:
                handler(record)
            self._transition(msg.task_id, TaskStatus.completed)
            record.last_error = None
        except Exception as exc:  # deterministic retry path
            record.last_error = str(exc)
            self.events.append(record.task_id, record.tenant_id, "task_processing_error", {"error": record.last_error})
            if record.attempts >= self.max_attempts:
                self._transition(msg.task_id, TaskStatus.failed)
            else:
                self._transition(msg.task_id, TaskStatus.queued)
                self.queue.publish(msg)
        return record

    def _transition(self, task_id: str, new_status: TaskStatus) -> None:
        rec = self.tasks[task_id]
        if can_transition(rec.status, new_status):
            rec.status = new_status
            self.events.append(task_id, rec.tenant_id, "status_changed", {"status": new_status.value})

    def get_task(self, task_id: str) -> TaskRecord | None:
        return self.tasks.get(task_id)
