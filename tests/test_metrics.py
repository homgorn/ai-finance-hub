import unittest

from src.backend.app.core.metrics import MetricsCollector


class MetricsTests(unittest.TestCase):
    def test_snapshot(self):
        m = MetricsCollector()
        m.observe_request(10.0)
        m.observe_request(20.0, error=True)
        m.observe_request(30.0)
        snap = m.snapshot(queue_lag=2)
        self.assertEqual(snap.requests_total, 3)
        self.assertEqual(snap.errors_total, 1)
        self.assertGreaterEqual(snap.p95_latency_ms, 20.0)
        self.assertEqual(snap.queue_lag, 2)


if __name__ == "__main__":
    unittest.main()
