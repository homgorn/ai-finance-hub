# Implementation Status (step-by-step)

## Выполнено в этом шаге
1. Redis-ready контракт для idempotency store:
   - `IdempotencyStore` protocol,
   - `InMemoryIdempotencyStore`,
   - `RedisIdempotencyStore` adapter.

2. Очередь задач и worker-pool foundation:
   - `InMemoryTaskQueue` + `TaskMessage`,
   - `RuntimeService.process_next()` как worker entrypoint.

3. Task lifecycle + event store:
   - `TaskStatus` state machine,
   - transition rules,
   - `InMemoryEventStore`.

4. Correlation IDs + runtime metrics:
   - middleware in `main.py`,
   - metrics collector (requests/errors/p95/queue lag),
   - health snapshot endpoint.

5. Tenant quotas and budget caps:
   - `QuotaManager` with early reject path.

## Что дальше (следующий шаг)
- Ввести identity provider, RBAC и tenant authorization вместо shared-secret bootstrap слоя.
- Подменить локальную очередь на broker с visibility timeout/DLQ.
- Добавить durable task registry/event store (PostgreSQL) + retention.
- Добавить нагрузочные тесты (k6/Locust) и контрактные тесты для публичных клиентов.


## Batch 2 (completed)
- Added pluggable backend wiring in `dependencies.py` (idempotency + event store + queue).
- Added SQLite event store adapter for persistent local audit trail.
- Added idempotency backend factory (`inmemory|redis`).


## Batch 3 (completed)
- Added persistent SQLite queue adapter and queue factory (`inmemory|sqlite`).
- Wired queue backend selection via `Settings` + `dependencies.py`.
- Added queue adapter/factory tests.

## Batch 4 (completed)
- Added SDD structure in `specs/` (specification, technical plan, delivery checklist).
- Fixed SQLite connection cleanup so Windows test runs do not retain database file locks.
- Made in-process task submission idempotent: retries return the original task without a second quota charge.
- Replaced the misleading task-id processing route with `POST /tasks/process-next`.
- Added FastAPI integration tests and made the full unit test suite mandatory in CI.

## Batch 5 (completed)
- Added strict backend configuration validation: unimplemented adapters no longer silently fall back to in-memory storage.
- Made SQLite queue claiming atomic for local concurrent workers and reject negative task cost at the domain boundary.
- Added environment-driven production configuration, separate client/worker API keys, and fail-closed startup checks.
- Added `.env.example`, OpenAPI security-scheme documentation, auth/configuration tests, and frontend build verification.
