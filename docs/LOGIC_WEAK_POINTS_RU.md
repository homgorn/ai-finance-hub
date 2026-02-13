# Логический аудит проекта: слабые места и приоритеты

## TL;DR
Проект движется в правильную сторону (модульность, очереди, адаптеры, тесты), но для production остаются критические точки: консистентность данных, надежность очереди, безопасность административных действий, и наблюдаемость end-to-end.

## 1) Критические слабые места (P0)

### 1.1 Exactly-once не гарантирован
- Есть idempotency и retry, но нет полноценной outbox/inbox модели.
- Риск: дублирование бизнес-эффектов при ретраях/перезапусках.

Что делать:
1. Ввести `event_id` + dedup key в event store.
2. Outbox table + фонового паблишера.
3. Детерминированные replay правила.

### 1.2 Нет брокерной семантики очереди в прод
- SQLite queue годится для local/dev, но не для multi-worker highload.
- Риск: race conditions, ограниченная отказоустойчивость.

Что делать:
1. RabbitMQ/SQS adapter.
2. Visibility timeout / ack / dead-letter queue.
3. Poison-message policy.

### 1.3 Ограниченная observability
- Есть базовые метрики, но нет трассировки по lifecycle задачи.
- Риск: сложно расследовать деградации и инциденты.

Что делать:
1. Correlation ID в каждом event.
2. OpenTelemetry spans: submit->route->queue->process.
3. Дашборд SLI/SLO (p95, error rate, retry ratio, queue lag).

## 2) Существенные слабые места (P1)

### 2.1 Governance/Policy
- Нужен policy versioning и signed decisions.
- Нужна история изменений policy и rollout control.

### 2.2 Multi-tenant isolation
- Сейчас есть quotas, но слабое разграничение noisy-neighbor.
- Нужны tenant-aware partitions и hard limits по ресурсам.

### 2.3 Admin security
- Для Platform Admin нужна усиленная модель:
  - MFA,
  - break-glass account,
  - immutable audit trail действий администратора.

## 3) Технический долг (P2)

1. Интеграционные тесты API (FastAPI TestClient).
2. Нагрузочные тесты (k6/Locust) по очереди и обработке.
3. Контрактные тесты адаптеров (redis/rabbit/sqs).
4. Автоматические миграции БД для event/queue storage.

## 4) Рекомендуемый план батчей

### Batch 4
- Broker adapter (RabbitMQ/SQS) + DLQ.
- Outbox/inbox foundations.
- Integration tests.

### Batch 5
- OTel + Prometheus + alerting.
- Policy versioning + decision signatures.
- Tenant isolation hardening.

### Batch 6
- Chaos testing (queue/provider failures).
- Cost guardrails + adaptive routing by budget/latency.
- Admin security hardening package.

## 5) Что уже хорошо (не потерять)
- Ports/adapters подход.
- Постепенные батчи и автотесты.
- Документация по ролям.
- Четкий вектор на надежность и traceability.
