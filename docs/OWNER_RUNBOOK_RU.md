# Owner Runbook (RU)

## Цель
Документ для владельца/оператора платформы.

## Ежедневный контроль
1. Проверить health endpoint и queue lag.
2. Проверить ошибки выполнения задач.
3. Проверить потребление квот tenant.
4. Проверить рост event store.

## Еженедельный контроль
1. Просмотреть reliability incidents.
2. Проверить retry/failure ratio.
3. Обновить skills catalog sync status.
4. Актуализировать roadmap и технический долг.

## Что делать при деградации
1. Включить safe-mode (ограничить сложные маршруты).
2. Уменьшить нагрузку на дорогие/медленные providers.
3. Временно ужесточить quotas.
4. Проверить event store + queue consistency.

## KPI (минимум)
- p95 latency
- error rate
- queue lag
- completion rate
- retry-to-fail ratio
