import unittest

from src.backend.app.core.orchestrator import InMemoryIdempotencyStore, TaskOrchestrator
from src.backend.app.core.policy import RiskLevel
from src.backend.app.core.routing import TaskContext, TaskDomain


class OrchestratorTests(unittest.TestCase):
    def test_idempotency_key_is_stable(self):
        orch = TaskOrchestrator(InMemoryIdempotencyStore())
        task = TaskContext(title="Tax help", description="Need IRS checklist")
        a = orch.build_idempotency_key(task, tenant_id="t1")
        b = orch.build_idempotency_key(task, tenant_id="t1")
        self.assertEqual(a, b)

    def test_orchestrate_returns_route_policy_and_key(self):
        orch = TaskOrchestrator(InMemoryIdempotencyStore())
        task = TaskContext(
            title="KYC review",
            description="Need compliance screening",
            domain_hint=TaskDomain.compliance,
        )
        result = orch.orchestrate(task, risk_level=RiskLevel.high, contains_pii=True)
        self.assertEqual(result.routing.agent_id, "compliance_guard")
        self.assertFalse(result.policy.allow_browser)
        self.assertTrue(result.policy.require_human_approval)
        self.assertTrue(len(result.idempotency_key) >= 32)


if __name__ == "__main__":
    unittest.main()
