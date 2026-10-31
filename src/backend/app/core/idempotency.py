from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class IdempotencyStore(Protocol):
    def exists(self, key: str) -> bool: ...

    def put(self, key: str, ttl_seconds: int | None = None) -> None: ...


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def exists(self, key: str) -> bool:
        return key in self._seen

    def put(self, key: str, ttl_seconds: int | None = None) -> None:
        _ = ttl_seconds
        self._seen.add(key)


@dataclass
class RedisIdempotencyStore:
    redis_url: str = "redis://localhost:6379/0"
    key_prefix: str = "idem:"

    def _client(self):
        import redis  # type: ignore

        return redis.Redis.from_url(self.redis_url, decode_responses=True)

    def exists(self, key: str) -> bool:
        client = self._client()
        return bool(client.exists(self.key_prefix + key))

    def put(self, key: str, ttl_seconds: int | None = None) -> None:
        client = self._client()
        full_key = self.key_prefix + key
        if ttl_seconds:
            client.setex(full_key, ttl_seconds, "1")
            return
        client.set(full_key, "1")


def build_idempotency_store(backend: str, redis_url: str) -> IdempotencyStore:
    if backend == "redis":
        return RedisIdempotencyStore(redis_url=redis_url)
    if backend == "inmemory":
        return InMemoryIdempotencyStore()
    raise ValueError(f"Unsupported idempotency backend: {backend}")
