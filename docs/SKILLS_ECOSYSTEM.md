# Skills Ecosystem and Logical Map

## Goal
Create a mini-ecosystem where finance workflows are composed from Claude/OpenAI skills and continuously updated from upstream repositories.

## Skill groups

### Claude-oriented domain skills
- `FINANCIAL_ADVISOR_TAX`
- `PORTFOLIO_REBALANCE`
- `RISK_COMPLIANCE_KYC_AML`
- `CLIENT_ONBOARDING_PACK`
- `FINANCIAL_REPORT_QA`

### OpenAI-oriented execution skills
- `FUNCTION_CALLING_TOOL_ROUTER`
- `RETRIEVAL_GROUNDED_ANALYST`
- `REASONING_MODEL_ORCHESTRATOR`
- `EVALS_REGRESSION_GUARD`

### Ecosystem/automation skill
- `SKILL_REGISTRY_SYNC` for discovery and synchronization.

## Logical chain (example)
1. Task intake + domain detection.
2. Domain skill selected (tax/compliance/portfolio).
3. Tool routing and retrieval grounding applied.
4. Policy gate evaluates risk/PII constraints.
5. Evals regression guard validates output quality.
6. Audit record captured.

## Auto-update pipeline
- Source definitions: `config/skill_sources/sources.yaml`
- Sync script: `scripts/sync_skills_catalog.py`
- Lock file: `data/skills/catalog.lock.json`
- GitHub schedule workflow: `.github/workflows/skills-sync.yml`

## Design notes
- The sync job captures **catalog metadata** first; it does not auto-import executable code.
- Human review remains mandatory before promoting new upstream assets into active runtime modules.
