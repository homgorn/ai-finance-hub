from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .idempotency import IdempotencyStore
from .policy import OpenClawPolicy, RiskLevel, evaluate_tool_access
from .routing import RoutingDecision, TaskContext, TaskDomain, infer_domain, route_task


@dataclass
class OrchestratedTask:
    idempotency_key: str
    routing: RoutingDecision
    policy: OpenClawPolicy
    domain: TaskDomain


class TaskOrchestrator:
    def __init__(self, idempotency_store: IdempotencyStore) -> None:
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
        idem_ttl_seconds: int | None = 3600,
    ) -> OrchestratedTask:
        key = self.build_idempotency_key(task, tenant_id)
        if not self.idempotency_store.exists(key):
            self.idempotency_store.put(key, ttl_seconds=idem_ttl_seconds)

        domain = infer_domain(task)
        decision = route_task(task)
        policy = evaluate_tool_access(risk_level, contains_pii)
        return OrchestratedTask(
            idempotency_key=key,
            routing=decision,
            policy=policy,
            domain=domain,
        )
