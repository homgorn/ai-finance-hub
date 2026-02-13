# Open-source admin/CMS options (RU)

Ниже pragmatic shortlist для админок (надежные и популярные опции):

## 1) Appsmith (open-source)
**Плюсы:** быстро собирать админ-панели, готовые data connectors.
**Минусы:** для сложной UX-логики может быть ограничивающим.

## 2) ToolJet (open-source)
**Плюсы:** low-code админки, self-hosted, быстрое время до MVP.
**Минусы:** иногда нужны обходные решения для продвинутых сценариев.

## 3) Directus / Strapi (headless CMS)
**Плюсы:** удобны как content/config layer + RBAC.
**Минусы:** это больше CMS, чем operational runtime console.

## 4) React Admin + свой backend
**Плюсы:** максимальная гибкость и контроль.
**Минусы:** дольше разработка.

## Рекомендация для этого проекта
- На старте: **ToolJet/Appsmith** для внутренней Platform Admin.
- Параллельно: проектировать **кастомную Tenant Admin UI** в React.
- Для контента/настроек: Directus/Strapi как опциональный слой.

## Минимальный набор экранов (Platform Admin)
1. Dashboard (queue lag, p95, errors)
2. Tasks explorer (status, attempts, last_error)
3. Tenant quotas/budgets
4. Skills & policies
5. Audit log viewer
