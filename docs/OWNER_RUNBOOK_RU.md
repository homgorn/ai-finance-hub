# Owner Runbook (RU)

## Цель
Документ для владельца/оператора платформы.

## Граница допуска к production

Текущий runtime можно запускать для внутреннего, single-process сценария только
после задания `AI_FINANCE_HUB_ENVIRONMENT=production`,
`AI_FINANCE_HUB_API_KEY` и `AI_FINANCE_HUB_WORKER_API_KEY`. При отсутствии
ключей приложение не стартует. Ключи передаются соответственно в заголовках
`X-API-Key` и `X-Worker-API-Key`.

Это не даёт готовую multi-tenant финансовую платформу: до работы с данными
клиентов необходимы identity provider, RBAC, tenant authorization, ротация
секретов, durable storage и независимый security review.

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
1. Остановить worker/внешний ingress: отдельного автоматического safe-mode ещё нет.
2. Уменьшить нагрузку на дорогие/медленные providers.
3. Временно ужесточить quotas и перезапустить runtime с нужной конфигурацией.
4. Проверить event store + queue consistency; для SQLite — целостность локального файла.

## KPI (минимум)
- p95 latency
- error rate
- queue lag
- completion rate
- retry-to-fail ratio
