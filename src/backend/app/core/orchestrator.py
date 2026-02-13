from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .policy import OpenClawPolicy, RiskLevel, evaluate_tool_access
from .routing import RoutingDecision, TaskContext, TaskDomain, infer_domain, route_task


@dataclass
class OrchestratedTask:
    idempotency_key: str
    routing: RoutingDecision
    policy: OpenClawPolicy
    domain: TaskDomain


class InMemoryIdempotencyStore:
    """Simple deterministic idempotency store.

    Keep this as a local adapter for now; later swap with Redis/DynamoDB
    without changing orchestration code.
    """

    def __init__(self) -> None:
        self._seen: set[str] = set()

    def exists(self, key: str) -> bool:
        return key in self._seen

    def put(self, key: str) -> None:
        self._seen.add(key)


class TaskOrchestrator:
    def __init__(self, idempotency_store: InMemoryIdempotencyStore) -> None:
        self.idempotency_store = idempotency_store

    @staticmethod
    def build_idempotency_key(task: TaskContext, tenant_id: str = "default") -> str:
        payload = f"{tenant_id}|{task.title}|{task.description}|{task.domain_hint}"
        return sha256(payload.encode("utf-8")).hexdigest()

    def orchestrate(
        self,
        task: TaskContext,
        *,
        tenant_id: str = "default",
        risk_level: RiskLevel = RiskLevel.medium,
        contains_pii: bool = False,
    ) -> OrchestratedTask:
        key = self.build_idempotency_key(task, tenant_id)
        if not self.idempotency_store.exists(key):
            self.idempotency_store.put(key)

        domain = infer_domain(task)
        decision = route_task(task)
        policy = evaluate_tool_access(risk_level, contains_pii)
        return OrchestratedTask(
            idempotency_key=key,
            routing=decision,
            policy=policy,
            domain=domain,
        )
