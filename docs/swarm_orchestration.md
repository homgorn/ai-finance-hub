# Swarm Orchestration

## Overview

Routing pipeline:
1. `infer_domain` computes domain signal from `domain_hint` or tokenized keyword rules.
2. `route_task` maps the resolved domain to an execution agent profile.
3. OpenClaw/policy layer enforces execution constraints and approval gates.

## Domain inference

Current supported domains:
- `tax`
- `insurance`
- `portfolio`
- `compliance`
- fallback: `general`

### Matching rules

- Input text is normalized to lowercase and tokenized via regex word boundaries.
- Keywords can be:
  - exact tokens (`tax`, `irs`, `compliance`),
  - prefix wildcards with `*` suffix (`deduction*`, `налог*`, `санкц*`).
- Matching is token-safe (no raw substring scanning across the entire sentence), which avoids false positives such as `syntax` => `tax`.
- If tokenization produces no tokens (empty/punctuation-only input), routing falls back to `general`.
- Rule precedence is deterministic: the first matching rule in `KEYWORD_RULES` wins.
- Keyword definitions are normalized to lowercase and duplicate wildcard prefixes are deduplicated at compile time.

## Routing decisions

Resolved domain maps to specialist routing:
- `tax` -> `tax_specialist`
- `insurance` -> `insurance_specialist`
- `portfolio` -> `portfolio_specialist`
- `compliance` -> `compliance_guard`
- `general` -> `general_finance_agent`

Each route returns:
- `agent_id`
- `reason`
- `required_skills`

Implementation note: routing templates are centralized in a domain->decision map and cloned per request to avoid accidental shared mutable state.

## Extension checklist

When adding a new domain:
1. Add a `TaskDomain` enum value.
2. Add keyword rules in `KEYWORD_RULES`.
3. Add route template in `ROUTING_BY_DOMAIN`.
4. Add tests for:
   - positive routing,
   - negative false-positive case,
   - domain-hint priority path.
5. Update this document and API docs if outward behavior changes.


## Configuration safety checks

- Routing configuration is validated at module load: every non-`general` `TaskDomain` must have a template in `ROUTING_BY_DOMAIN`.
- Validation is strict: unexpected extra route entries also fail fast.
- Every non-`general` domain must also have exactly one entry in `KEYWORD_RULES` (no duplicate domain rule blocks).
- Exact keywords are validated for cross-domain collisions (same exact token cannot belong to multiple domains).
- Each keyword rule must remain non-empty after normalization (guards against broken/blank config entries).
- Every routing decision must define a non-empty, duplicate-free `required_skills` list.
- Every routing decision (including fallback `general`) must include `PROMPT_SECURITY_AUDIT` as a baseline security skill.
- This fail-fast guard prevents silent regressions when adding or refactoring domains.
- Tests assert map/domain and keyword/domain consistency to keep these invariants locked in CI.
