import unittest

from src.backend.app.core.queueing import InMemoryTaskQueue, SQLiteTaskQueue, build_task_queue


class QueueFactoryTests(unittest.TestCase):
    def test_build_inmemory(self):
        q = build_task_queue("inmemory", ".runtime/queue.db")
        self.assertIsInstance(q, InMemoryTaskQueue)

    def test_build_sqlite(self):
        q = build_task_queue("sqlite", ".runtime/queue.db")
        self.assertIsInstance(q, SQLiteTaskQueue)

    def test_rejects_unknown_backend(self):
        with self.assertRaisesRegex(ValueError, "Unsupported queue backend"):
            build_task_queue("kafka", ".runtime/queue.db")


if __name__ == "__main__":
    unittest.main()
