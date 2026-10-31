import tempfile
import threading
import unittest
from pathlib import Path

from src.backend.app.core.queueing import SQLiteTaskQueue, TaskMessage


class SQLiteQueueTests(unittest.TestCase):
    def test_publish_consume_and_lag(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "queue.db"
            q = SQLiteTaskQueue(str(db))
            self.assertEqual(q.lag(), 0)

            q.publish(TaskMessage(task_id="t1", tenant_id="tenant1", idempotency_key="k1"))
            q.publish(TaskMessage(task_id="t2", tenant_id="tenant1", idempotency_key="k2"))
            self.assertEqual(q.lag(), 2)

            msg = q.consume_nowait()
            self.assertIsNotNone(msg)
            assert msg is not None
            self.assertEqual(msg.task_id, "t1")
            self.assertEqual(q.lag(), 1)

    def test_only_one_worker_claims_a_message(self):
        with tempfile.TemporaryDirectory() as td:
            q = SQLiteTaskQueue(str(Path(td) / "queue.db"))
            q.publish(TaskMessage(task_id="t1", tenant_id="tenant1", idempotency_key="k1"))
            start = threading.Barrier(2)
            results: list[TaskMessage | None] = []

            def consume() -> None:
                start.wait()
                results.append(q.consume_nowait())

            workers = [threading.Thread(target=consume) for _ in range(2)]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join()

            self.assertEqual(sum(result is not None for result in results), 1)
            self.assertEqual(q.lag(), 0)


if __name__ == "__main__":
    unittest.main()
