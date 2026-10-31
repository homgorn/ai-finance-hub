# Delivery checklist — 001

- [x] Preserve plural/derived tax keyword routing with a prefix rule.
- [x] Close SQLite connections after schema, read, write, and lag operations.
- [x] Make duplicate submission return the original task without a second quota charge.
- [x] Rename the queue worker endpoint to `POST /tasks/process-next`.
- [x] Add API integration tests for duplicate submission and queue processing.
- [x] Run the full test suite locally.
- [x] Execute the full test suite in GitHub Actions.

## Follow-up (not implemented)

- [ ] Make idempotency atomic and durable across multiple processes.
- [ ] Add authentication and tenant authorization before exposing task APIs.
- [ ] Add a real worker/broker and observability export.
