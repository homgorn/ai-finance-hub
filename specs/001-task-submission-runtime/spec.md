# 001 — Reliable task submission runtime

**Status:** Implemented  
**Owner:** AI Finance Hub maintainers  
**Last updated:** 2026-10-31

## Problem

Submitting a financial task must be safe to retry and must produce an
unambiguous processing operation. Local SQLite adapters must also work on
Windows, where an open database handle prevents cleanup and test isolation.

## Scope

- Route a valid task and queue it for processing.
- Treat the same tenant and task payload as an idempotent retry.
- Process the next queued task through an endpoint whose name reflects that
  behaviour.
- Persist and read queue/event data through SQLite without leaking file handles.

## Acceptance criteria

1. Repeating an identical submission for the same tenant returns the original
   task ID, reports `reason: duplicate`, and does not consume another quota.
2. `POST /tasks/process-next` processes one queued task; it does not pretend to
   process a client-supplied task ID.
3. A task follows `submitted → routed → queued → processing → completed`, or a
   documented retry/failure path.
4. SQLite queue and event-store tests leave no open database handles after each
   operation.
5. Keyword routing preserves tax variants such as `taxes` and `taxation` while
   avoiding arbitrary substring matches.
6. Production startup fails without separate client and worker secrets; task and
   worker routes reject invalid credentials.

## Non-goals

- Distributed idempotency across separate service instances.
- A production broker, worker pool, authentication, or durable task registry.
- Financial advice or execution of external financial actions.
- Full identity management, RBAC, and multi-tenant authorization.

## Verification

Run `python -m unittest discover -s tests -v` from the repository root.
