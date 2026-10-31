import unittest

from fastapi.testclient import TestClient

from src.backend.app.dependencies import get_runtime
from src.backend.app.main import app
from src.backend.app.services.runtime import RuntimeService


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        self.runtime = RuntimeService()
        app.dependency_overrides[get_runtime] = lambda: self.runtime
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_submit_duplicate_and_process_next(self):
        payload = {
            "title": "Tax filing",
            "description": "Need help with IRS forms",
            "tenant_id": "tenant-a",
        }
        first = self.client.post("/tasks/submit", json=payload)
        duplicate = self.client.post("/tasks/submit", json=payload)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(duplicate.status_code, 200)
        self.assertEqual(duplicate.json()["reason"], "duplicate")
        self.assertEqual(duplicate.json()["task_id"], first.json()["task_id"])

        processed = self.client.post("/tasks/process-next")
        self.assertEqual(processed.status_code, 200)
        self.assertEqual(processed.json()["processed_task_id"], first.json()["task_id"])

    def test_process_next_returns_not_found_when_queue_is_empty(self):
        response = self.client.post("/tasks/process-next")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "queue_empty")
