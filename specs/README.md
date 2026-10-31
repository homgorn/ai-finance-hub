# Specification-driven development (SDD)

`specs/` is the source of truth for changes to runtime behaviour. Every feature
folder contains three small, reviewable documents:

1. `spec.md` — user-visible behaviour and acceptance criteria;
2. `plan.md` — technical design and constraints;
3. `tasks.md` — implementation and verification checklist.

## Workflow

1. Create the next numbered feature directory, for example `002-agent-registry`.
2. Agree the acceptance criteria in `spec.md` before changing production code.
3. Record the design decisions and non-goals in `plan.md`.
4. Add or update tests with the matching task items.
5. Mark tasks complete only after the automated checks pass.

The current implemented baseline is documented in
[`001-task-submission-runtime`](001-task-submission-runtime/spec.md).
