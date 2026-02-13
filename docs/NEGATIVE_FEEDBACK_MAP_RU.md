# NEGATIVE FEEDBACK MAP (RU)

> Цель: не «хейт конкурентов», а карта реальных болей пользователей, которые нужно закрыть архитектурой продукта.

## Частые классы негативной обратной связи в AI-сервисах

1. **Непредсказуемость качества**
   - «Иногда идеально, иногда мимо».
   - Что делаем: policy + deterministic skills + route explainability.

2. **Слабая поддержка и операционка**
   - Долгие ответы, неясные SLA.
   - Что делаем: отдельный support layer и runbook-инциденты.

3. **Высокая цена enterprise-пакетов**
   - SMB не может зайти на рынок.
   - Что делаем: tiered pricing + open-core модули.

4. **Проблемы с приватностью/данными**
   - Страх утечки PII/секретов.
   - Что делаем: PII-aware policy, локальный runtime, ограничение external network.

5. **Сложная интеграция**
   - Много ручной настройки и нестабильные коннекторы.
   - Что делаем: capability registry + шаблоны модулей + validation tests.

## Product improvements, вытекающие из карты

- добавить `policy_decision_id` и immutable audit events;
- добавить риск-профили per tenant;
- добавить режим "safe execution" по умолчанию;
- добавить red-team сценарии против prompt injection.
