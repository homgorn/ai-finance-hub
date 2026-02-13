# API Overview

Current endpoints:
- `GET /health`
- `GET /agents`
- `POST /tasks/route`
- `POST /tasks/submit`
- `POST /tasks/{task_id}/process`
- `GET /tasks/{task_id}`
- `GET /security/policy?risk=medium&contains_pii=false`

Runtime behavior now includes:
- idempotency key generation,
- task lifecycle (`submitted -> routed -> queued -> processing -> completed`),
- in-memory queue worker entrypoint,
- tenant quota and budget-cap rejection path,
- metrics snapshot in health endpoint.

- Queue backend can now be configured as `inmemory|sqlite` (broker adapters next).
