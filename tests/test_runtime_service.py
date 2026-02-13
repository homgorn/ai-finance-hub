import unittest
from types import SimpleNamespace

from src.backend.app.core.lifecycle import TaskStatus
from src.backend.app.services.runtime import RuntimeService


class RuntimeServiceTests(unittest.TestCase):
    def test_submit_and_process(self):
        runtime = RuntimeService()
        req = SimpleNamespace(
            title="Tax filing",
            description="Need help with IRS",
            tenant_id="t1",
            estimated_cost=1.0,
            domain_hint=None,
            contains_pii=False,
        )
        result = runtime.submit_task(req)
        self.assertTrue(result.accepted)
        self.assertEqual(result.record.status, TaskStatus.queued)
        self.assertGreater(runtime.queue.lag(), 0)
        self.assertGreaterEqual(runtime.events.count(), 3)

        processed = runtime.process_next()
        self.assertIsNotNone(processed)
        assert processed is not None
        self.assertEqual(processed.status, TaskStatus.completed)
        self.assertEqual(processed.attempts, 1)

    def test_retry_then_fail(self):
        runtime = RuntimeService(max_attempts=2)
        req = SimpleNamespace(
            title="Tax filing",
            description="Need help with IRS",
            tenant_id="t1",
            estimated_cost=1.0,
            domain_hint=None,
            contains_pii=False,
        )
        result = runtime.submit_task(req)
        task_id = result.record.task_id

        def broken(_record):
            raise RuntimeError("temporary upstream failure")

        first = runtime.process_next(handler=broken)
        self.assertIsNotNone(first)
        assert first is not None
        self.assertEqual(first.status, TaskStatus.queued)
        self.assertEqual(first.attempts, 1)
        self.assertIn("upstream", first.last_error or "")

        second = runtime.process_next(handler=broken)
        self.assertIsNotNone(second)
        assert second is not None
        self.assertEqual(second.status, TaskStatus.failed)
        self.assertEqual(second.attempts, 2)
        self.assertEqual(runtime.get_task(task_id).status, TaskStatus.failed)

    def test_reject_on_quota(self):
        runtime = RuntimeService()
        runtime.quotas.set_quota("t1", runtime.quotas.default_quota.__class__(max_tasks_per_window=0, max_budget_per_window=0.0))
        req = SimpleNamespace(
            title="Tax filing",
            description="Need help with IRS",
            tenant_id="t1",
            estimated_cost=1.0,
            domain_hint=None,
            contains_pii=False,
        )
        result = runtime.submit_task(req)
        self.assertFalse(result.accepted)
        self.assertEqual(result.record.status, TaskStatus.rejected)


if __name__ == "__main__":
    unittest.main()
