# Highload Readiness: что упущено и что делать сейчас

## 1) Что уже сделано правильно
- Модульная архитектура skills.
- Отдельный core слой маршрутизации/политик.
- Базовые unit tests.

## 2) Что критично упущено для масштабирования

1. **Идемпотентность запросов**
   - Нужна защита от дублей (ретраи, повторная отправка).

2. **Очередь задач и backpressure**
   - Нужен асинхронный pipeline (Kafka/Rabbit/SQS + worker pool).

3. **SLO/SLI и наблюдаемость**
   - p95 latency, error budget, queue lag, tool-failure rate.

4. **Многотенантность и quota**
   - per-tenant rate limits, budget caps, isolation.

5. **Хранилище аудита**
   - immutable audit trail (route, policy, tool calls).

6. **Версионирование промптов/скиллов/политик**
   - нужна reproducibility (какая версия отвечала клиенту).

7. **План деградации**
   - circuit breakers, fallback model/provider, graceful degradation.

## 3) Как сделать так, чтобы потом минимум переписывать

### Кодинг-подход
- Ports & Adapters (Hexagonal): core без привязки к FastAPI/Redis/Kafka.
- Контракты данных: Pydantic схемы на boundary, dataclass/Typed core внутри.
- Строгая идемпотентность на входе и на уровне worker.
- Событийная модель: `TaskSubmitted -> Routed -> PolicyChecked -> Executed -> Audited`.

### Масштабирование
- Горизонтально: stateless API pods + worker autoscaling.
- Вертикально: model-tier selection (cheap/fast vs reasoning/deep).
- Кэширование: policy decisions, retrieval chunks, provider metadata.
- Партиционирование: tenant/domain based partitions.

### Данные и надежность
- Outbox pattern для надежной публикации событий.
- Retry с jitter + dead-letter queue.
- Exactly-once на уровне бизнес-эффекта (через idempotency key), не транспорта.

## 4) Что можно делать уже сейчас (практично)

1. Ввести `idempotency_key` в orchestration (минимум in-memory + далее Redis).
2. Добавить `task_status` state-machine и event log table.
3. Добавить metrics endpoint и tracing correlation id.
4. Вынести provider adapters за интерфейсы.
5. Ввести нагрузочные smoke-тесты (k6/Locust).

## 5) Целевая дорожная карта
- Sprint 1: idempotency + task lifecycle + metrics.
- Sprint 2: queue workers + retries + DLQ.
- Sprint 3: tenant quotas + audit store + policy decision ids.
- Sprint 4: autoscaling, chaos tests, cost-optimization loops.
