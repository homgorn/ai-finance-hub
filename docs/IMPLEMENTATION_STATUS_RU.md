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
- Подменить in-memory queue на RabbitMQ/SQS/Kafka adapter.
- Подменить in-memory idempotency на Redis в runtime wiring.
- Добавить persistent event store (PostgreSQL) + retention.
- Добавить integration tests (FastAPI TestClient) и нагрузочные тесты (k6/Locust).
