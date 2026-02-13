# Reliability Review (самокритика и улучшения)

## Что уже улучшили технически
- Появились pluggable adapters (idempotency/event store/queue).
- Есть state machine и базовый event trail.
- Есть tenant quotas и базовые runtime metrics.

## Слабые места (честно)
1. **Нет distributed locking для multi-worker processing**
   - SQLite/in-memory достаточно для dev, но для прод нужно broker + lock/lease model.

2. **Нет durable retry policy с backoff/jitter**
   - Сейчас retry есть, но без экспоненциального backoff и DLQ-хранилища.

3. **Отсутствует end-to-end contract testing API**
   - Много unit tests, но мало интеграционных сценариев с FastAPI client.

4. **Нет outbox/inbox паттерна**
   - Для exactly-once бизнес-эффекта нужно согласование event publication.

5. **Недостаточная observability глубина**
   - Нужны per-tenant latency/error dashboards + tracing spans.

## Что улучшено в этом батче
- Добавлен retry-aware processing c ограничением max attempts.
- Добавлен capture `last_error` и счетчик `attempts` в task record.
- Добавлены переходы статусов для requeue сценария.

## Что делать следующим батчем
1. RabbitMQ/SQS adapter + visibility timeout.
2. Redis-backed distributed idempotency with TTL and collision metrics.
3. Dead-letter queue + retry policy (exp backoff + jitter).
4. Integration tests (FastAPI TestClient + sqlite backends).
5. Prometheus/OpenTelemetry export.
