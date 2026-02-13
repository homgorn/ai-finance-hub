from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TenantQuota:
    max_tasks_per_window: int
    max_budget_per_window: float


@dataclass
class TenantUsage:
    tasks_used: int = 0
    budget_used: float = 0.0


@dataclass
class QuotaDecision:
    allowed: bool
    reason: str


@dataclass
class QuotaManager:
    default_quota: TenantQuota = field(default_factory=lambda: TenantQuota(100, 1000.0))

    def __post_init__(self) -> None:
        self._usage: dict[str, TenantUsage] = {}
        self._quotas: dict[str, TenantQuota] = {}

    def set_quota(self, tenant_id: str, quota: TenantQuota) -> None:
        self._quotas[tenant_id] = quota

    def check_and_consume(self, tenant_id: str, task_cost: float) -> QuotaDecision:
        usage = self._usage.setdefault(tenant_id, TenantUsage())
        quota = self._quotas.get(tenant_id, self.default_quota)

        if usage.tasks_used + 1 > quota.max_tasks_per_window:
            return QuotaDecision(False, "task_quota_exceeded")
        if usage.budget_used + task_cost > quota.max_budget_per_window:
            return QuotaDecision(False, "budget_cap_exceeded")

        usage.tasks_used += 1
        usage.budget_used += task_cost
        return QuotaDecision(True, "ok")

    def get_usage(self, tenant_id: str) -> TenantUsage:
        return self._usage.setdefault(tenant_id, TenantUsage())
