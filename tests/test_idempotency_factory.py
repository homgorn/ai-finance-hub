import unittest

from src.backend.app.core.idempotency import InMemoryIdempotencyStore, RedisIdempotencyStore, build_idempotency_store


class IdempotencyFactoryTests(unittest.TestCase):
    def test_build_inmemory(self):
        store = build_idempotency_store("inmemory", "redis://localhost:6379/0")
        self.assertIsInstance(store, InMemoryIdempotencyStore)

    def test_build_redis(self):
        store = build_idempotency_store("redis", "redis://localhost:6379/0")
        self.assertIsInstance(store, RedisIdempotencyStore)

    def test_rejects_unknown_backend(self):
        with self.assertRaisesRegex(ValueError, "Unsupported idempotency backend"):
            build_idempotency_store("typo", "redis://localhost:6379/0")


if __name__ == "__main__":
    unittest.main()
