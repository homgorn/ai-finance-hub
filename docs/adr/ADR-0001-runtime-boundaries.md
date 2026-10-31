# ADR-0001: Keep the current task runtime explicitly single-process

**Status:** Accepted  
**Date:** 2026-10-31

## Context

The project has in-memory and SQLite development adapters plus optional
Redis-ready idempotency code. These do not form a distributed job runtime.

## Decision

Document and test the existing runtime as a single-process baseline. Expose a
clear `process-next` worker simulation API, and do not claim durable,
multi-worker exactly-once processing.

## Consequences

- Local development and tests have predictable semantics.
- Production deployment requires a durable task store, atomic idempotency claim,
  authenticated tenants, and a broker/worker adapter before horizontal scaling.
