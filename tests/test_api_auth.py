import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.backend.app.config import settings
from src.backend.app.main import app


class ApiAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.settings_patch = patch.multiple(
            settings,
            environment="production",
            api_key="client-secret",
            worker_api_key="worker-secret",
        )
        self.settings_patch.start()

    def tearDown(self):
        self.settings_patch.stop()

    def test_task_routes_require_api_key_in_production(self):
        payload = {"title": "Tax filing", "description": "Need help with IRS forms"}
        self.assertEqual(self.client.post("/tasks/route", json=payload).status_code, 401)
        self.assertEqual(
            self.client.post("/tasks/route", json=payload, headers={"x-api-key": "client-secret"}).status_code,
            200,
        )

    def test_worker_route_requires_dedicated_worker_key_in_production(self):
        self.assertEqual(
            self.client.post("/tasks/process-next", headers={"x-api-key": "client-secret"}).status_code,
            401,
        )
        self.assertEqual(
            self.client.post(
                "/tasks/process-next",
                headers={"x-api-key": "client-secret", "x-worker-api-key": "worker-secret"},
            ).status_code,
            404,
        )
