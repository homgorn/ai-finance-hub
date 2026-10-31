# START HERE (главная точка входа)

Если теряется нить — начни с этого файла.

## 1) Кто ты в системе?

### Я владелец/админ продукта
1. Прочитай `OWNER_RUNBOOK_RU.md`.
2. Прочитай `ADMIN_ARCHITECTURE_RU.md`.
3. Потом `HIGHLOAD_READINESS_RU.md`.

### Я пользователь платформы
1. Прочитай `USER_GUIDE_RU.md`.
2. Прочитай `FAQ.md`.

### Я разработчик
1. `architecture.md`
2. `api_overview.md`
3. `IMPLEMENTATION_STATUS_RU.md`
4. `RELIABILITY_REVIEW_RU.md`
5. `../specs/README.md` — SDD-процесс и принятые контракты

## 2) Мини-карта системы
- Backend API: `src/backend`
- Frontend (скелет): `src/frontend`
- Skills/Modules: `modules/skills`
- OpenClaw/security docs: `openclaw/`
- Документация: `docs/`

## 3) Что уже работает
- Task routing + policy check
- Queue lifecycle (inmemory/sqlite)
- Event store (inmemory/sqlite)
- Idempotency adapters (inmemory/redis-ready)
- Retry-aware processing
- API integration tests и production frontend build в CI
- Fail-closed shared-secret защита task/worker API в production

## 4) Что дальше
- Identity provider + RBAC/tenant authorization
- Broker/worker и durable distributed idempotency
- Админ- и пользовательский UI с разделением ролей
