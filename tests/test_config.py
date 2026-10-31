import unittest
from unittest.mock import patch

from pydantic import ValidationError

from src.backend.app.config import Settings, _settings_from_environment


class SettingsTests(unittest.TestCase):
    def test_rejects_unimplemented_queue_backend(self):
        with self.assertRaises(ValidationError):
            Settings(queue_backend="kafka")

    def test_rejects_unimplemented_event_store_backend(self):
        with self.assertRaises(ValidationError):
            Settings(event_store_backend="postgres")

    def test_production_requires_client_and_worker_keys(self):
        with self.assertRaises(ValidationError):
            Settings(environment="production")

    def test_production_accepts_both_keys(self):
        settings = Settings(environment="production", api_key="client", worker_api_key="worker")
        self.assertEqual(settings.environment, "production")

    def test_reads_prefixed_environment_variables(self):
        with patch.dict(
            "os.environ",
            {
                "AI_FINANCE_HUB_ENVIRONMENT": "production",
                "AI_FINANCE_HUB_API_KEY": "client",
                "AI_FINANCE_HUB_WORKER_API_KEY": "worker",
                "AI_FINANCE_HUB_QUEUE_BACKEND": "sqlite",
            },
            clear=True,
        ):
            settings = _settings_from_environment()
        self.assertEqual(settings.environment, "production")
        self.assertEqual(settings.queue_backend, "sqlite")


if __name__ == "__main__":
    unittest.main()
