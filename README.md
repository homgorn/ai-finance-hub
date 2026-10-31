# AI Finance Hub

Security-first platform architecture for financial AI automation with modular agent skills (Claude/OpenAI), OpenClaw control layer, and scalable orchestration.

## What this service is (core idea)
AI Finance Hub is an orchestration platform, not a single chatbot:
1. receives a finance task,
2. classifies domain/risk,
3. routes to a specialist agent,
4. applies OpenClaw policy guardrails,
5. returns traceable output with required skills.

## Implemented in this iteration
- Typed task model (`priority`, `domain_hint`, PII/browser flags).
- Domain inference + explicit routing decision payload (`agent`, `reason`, `required_skills`).
- Stronger OpenClaw policy model with `max_tool_calls`, network toggle, human-approval gate.
- Basic backend tests for routing and policy behavior.

## Key folders
- `src/backend` — FastAPI backend with orchestration and policy stubs.
- `src/frontend` — React + TypeScript skeleton.
- `modules/skills` — Claude/OpenAI/community skill modules.
- `openclaw` — architecture, threat model, hardening docs.
- `docs` — GitHub Pages-ready documentation.
- `specs` — SDD specifications, design plans, and delivery checklists.

## Local verification

From the repository root:

```bash
python -m unittest discover -s tests -v
python -m compileall src/backend/app
```

The current implemented runtime contract is in
[`specs/001-task-submission-runtime`](specs/001-task-submission-runtime/spec.md).

## Deployment safety baseline

Copy `.env.example` to a non-versioned environment file or configure the same
`AI_FINANCE_HUB_*` variables in the deployment platform. In `production`, the
application refuses to start unless both `AI_FINANCE_HUB_API_KEY` and
`AI_FINANCE_HUB_WORKER_API_KEY` are set. Send the former in `X-API-Key` for
`/tasks/*`; queue processing additionally requires `X-Worker-API-Key`.

This is a bootstrap shared-secret control, not tenant-level authentication or
authorization. Do not expose the service to untrusted users until an identity
provider, RBAC, audit retention, and durable distributed runtime are in place.

## Next steps
1. Replace keyword routing with scored classifier + agent capability registry.
2. Add persistent audit logs and signed execution traces.
3. Add policy simulation endpoint for preflight task safety checks.
4. Integrate observability (Sentry/PostHog/OpenTelemetry).

## Strategic docs added
- `docs/PRODUCT_POSITIONING_RU.md`
- `docs/SWOT_COMPETITORS_RU.md`
- `docs/NEGATIVE_FEEDBACK_MAP_RU.md`
- `docs/RESEARCH_BACKLOG_RU.md`
- `docs/ARCHITECTURE_ENHANCEMENTS.md`
- `docs/SOURCE_LOG.md`

- `docs/SKILLS_ECOSYSTEM.md`
- `docs/HIGHLOAD_READINESS_RU.md`
- `docs/IMPLEMENTATION_STATUS_RU.md`
- `docs/RELIABILITY_REVIEW_RU.md`


## Documentation map
- `docs/START_HERE.md` — быстрый вход в документацию
- `docs/USER_GUIDE_RU.md` — документация для пользователей
- `docs/OWNER_RUNBOOK_RU.md` — документация для владельца/оператора
- `docs/ADMIN_ARCHITECTURE_RU.md` — модель разделения Platform Admin vs Tenant Admin
- `docs/CMS_OPTIONS_RU.md` — open-source варианты админки/CMS
- `docs/LOGIC_WEAK_POINTS_RU.md`
