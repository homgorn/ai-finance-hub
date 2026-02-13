import unittest

from src.backend.app.core.idempotency import InMemoryIdempotencyStore


class IdempotencyStoreTests(unittest.TestCase):
    def test_exists_and_put(self):
        store = InMemoryIdempotencyStore()
        self.assertFalse(store.exists("k1"))
        store.put("k1", ttl_seconds=10)
        self.assertTrue(store.exists("k1"))


if __name__ == "__main__":
    unittest.main()
