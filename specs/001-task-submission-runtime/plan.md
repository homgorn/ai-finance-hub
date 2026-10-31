# Technical plan — 001

## Design

- `RuntimeService` owns the in-process mapping from idempotency key to task ID.
  The key includes tenant ID, title, description, and domain hint.
- Duplicate detection happens before quota consumption and queue publication.
- The worker endpoint is explicitly named `/tasks/process-next` because the
  queue abstraction only supports consuming the next available message.
- SQLite adapters wrap every connection in a closing context manager. This is
  required for deterministic cleanup on Windows.

## Consequences

- Idempotency is correct within one running process. Production multi-instance
  deployments must select the Redis adapter and add an atomic durable task
  record before claiming the same guarantee.
- The legacy misleading `/{task_id}/process` operation is intentionally absent;
  clients must call the explicit process-next endpoint.

## Test layers

- Unit: routing, quotas, lifecycle, idempotency, queue/event adapters.
- API integration: submission, duplicate retry, queue processing, empty queue.
- CI: bytecode compilation and the complete `unittest` suite.
