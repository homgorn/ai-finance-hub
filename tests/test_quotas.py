import unittest

from src.backend.app.core.quotas import QuotaManager, TenantQuota


class QuotaTests(unittest.TestCase):
    def test_task_quota_exceeded(self):
        mgr = QuotaManager()
        mgr.set_quota("t1", TenantQuota(max_tasks_per_window=1, max_budget_per_window=100.0))
        self.assertTrue(mgr.check_and_consume("t1", 1.0).allowed)
        d = mgr.check_and_consume("t1", 1.0)
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "task_quota_exceeded")

    def test_budget_cap_exceeded(self):
        mgr = QuotaManager()
        mgr.set_quota("t1", TenantQuota(max_tasks_per_window=10, max_budget_per_window=2.0))
        self.assertTrue(mgr.check_and_consume("t1", 1.5).allowed)
        d = mgr.check_and_consume("t1", 0.6)
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "budget_cap_exceeded")


if __name__ == "__main__":
    unittest.main()
