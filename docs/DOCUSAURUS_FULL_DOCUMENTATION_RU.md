# Полная документация на базе Docusaurus для AI Finance Hub

> Цель: превратить текущий набор Markdown-файлов в управляемую, версионируемую и расширяемую документационную платформу в стиле Docusaurus.

## 1. Scope документации

Эта документация покрывает:
- продуктовый контекст и позиционирование,
- пользовательские и операционные сценарии,
- архитектуру платформы и API,
- безопасность/OpenClaw-контуры,
- надежность, highload и roadmap,
- процессы release/change management.

## 2. Информационная архитектура (IA)

Рекомендуемая структура Docusaurus-сайта:

1. **Getting Started**
   - START HERE
   - Quickstart
   - FAQ
2. **User Docs**
   - User Guide
   - Кейсы и best practices
3. **Operations / Owner**
   - Owner Runbook
   - Admin Architecture
   - CMS options
4. **Platform Engineering**
   - Architecture
   - Swarm orchestration
   - OpenClaw layer
   - API Overview
   - TRIZ innovation
5. **Reliability & Delivery**
   - Highload readiness
   - Implementation status
   - Reliability review
6. **Strategy & Research**
   - Product positioning
   - SWOT
   - Negative feedback map
   - Research backlog
   - Architecture enhancements
   - Source log

## 3. Стандарты страниц

Для каждой страницы рекомендуется единый шаблон:
1. Цель страницы
2. Для кого
3. Ключевые термины
4. Основной контент (шаги/диаграммы/таблицы)
5. Чек-лист верификации
6. Связанные страницы
7. История изменений

## 4. Навигация и sidebars

Ниже пример структуры `sidebars.ts` для Docusaurus:

```ts
const sidebars = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: ['START_HERE', 'getting_started', 'faq'],
    },
    {
      type: 'category',
      label: 'User Docs',
      items: ['USER_GUIDE_RU'],
    },
    {
      type: 'category',
      label: 'Operations / Owner',
      items: ['OWNER_RUNBOOK_RU', 'ADMIN_ARCHITECTURE_RU', 'CMS_OPTIONS_RU'],
    },
    {
      type: 'category',
      label: 'Platform Engineering',
      items: ['architecture', 'swarm_orchestration', 'openclaw_layer', 'api_overview', 'triz_innovation'],
    },
    {
      type: 'category',
      label: 'Reliability & Delivery',
      items: ['HIGHLOAD_READINESS_RU', 'IMPLEMENTATION_STATUS_RU', 'RELIABILITY_REVIEW_RU'],
    },
    {
      type: 'category',
      label: 'Strategy & Research',
      items: [
        'PRODUCT_POSITIONING_RU',
        'SWOT_COMPETITORS_RU',
        'NEGATIVE_FEEDBACK_MAP_RU',
        'RESEARCH_BACKLOG_RU',
        'ARCHITECTURE_ENHANCEMENTS',
        'SOURCE_LOG',
      ],
    },
  ],
};

export default sidebars;
```

## 5. Governance (Docs-as-Code)

- Все изменения документации идут через PR.
- Для больших изменений обязательны:
  - owner (бизнес/продукт),
  - tech reviewer (архитектура/API),
  - security reviewer (если затрагивается OpenClaw/PII).
- В каждом PR-дескрипшене по docs:
  - что поменялось,
  - зачем,
  - затронутые аудитории,
  - как проверяли актуальность.

## 6. Версионирование документации

Рекомендуемая схема:
- `current` — текущая активная версия,
- `v0.x` — исторические снапшоты по релизам.

При breaking changes API:
1. фиксируем changelog,
2. обновляем `api_overview.md`,
3. добавляем migration notes,
4. публикуем release notes в docs.

## 7. Quality Gates для docs

Перед merge:
1. Проверка ссылок (внутренние/якоря).
2. Проверка терминологии (единый глоссарий).
3. Проверка runnable-команд в Quickstart/Runbook.
4. Проверка согласованности с текущим кодом (`src/backend`, `src/frontend`).

## 8. Безопасность документации

- Не публиковать секреты/токены/внутренние URL с доступом.
- Для security-docs использовать redaction-подход.
- Любые примеры с PII должны быть анонимизированы.

## 9. Roadmap внедрения Docusaurus

### Фаза 1 (быстро)
- Подготовить единый `docs/index.md` как карту.
- Упорядочить файлы по категориям.
- Добавить шаблон страницы и чек-листы.

### Фаза 2 (продуктив)
- Поднять Docusaurus сайт (`website/`).
- Настроить sidebars + navbar.
- Добавить поиск (local/Algolia).

### Фаза 3 (enterprise)
- Версионирование docs.
- Автопроверка ссылок/фронтматтеров в CI.
- Метрики docs health (покрытие, freshness, broken links).

## 10. Definition of Done (документация)

Документация считается «полной», когда:
1. Есть путь для всех ролей: user / owner / dev / security.
2. Все core-модули покрыты: routing, policy, orchestration, API.
3. Есть эксплуатационные runbook’и и reliability-материалы.
4. Есть продуктово-стратегический слой (позиционирование/исследования).
5. Навигация консистентна и не ведет в «битые» разделы.

---

Если нужно, следующим шагом можно подготовить отдельный `website/` пакет Docusaurus (config, sidebars, navbar, search, versioning) как инфраструктурный PR.
