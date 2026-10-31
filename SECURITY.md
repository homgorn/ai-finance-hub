# Security Policy

## Supported versions
This repository is in active bootstrap stage; security updates apply to `main`.

## Reporting a vulnerability
- Do not open public issues for critical vulnerabilities.
- Report privately to repository maintainers.

## Baseline controls
- Least-privilege tools for agents.
- No plaintext secrets in repository.
- Mandatory review for changes in `openclaw/`, `src/backend/app/services/`, and `config/`.
- Production startup fails if distinct client and worker API secrets are absent.
- The task API and queue-processing endpoint use separate shared-secret checks in production.

## Current security boundary

The current shared-secret layer is suitable only as a bootstrap deployment
control. It does **not** provide users, sessions, RBAC, tenant authorization,
secret rotation, rate limiting, or tamper-evident audit trails. These controls
are mandatory before the service handles customer financial data or performs
actions with external financial systems.
