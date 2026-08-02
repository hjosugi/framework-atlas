---
title: "Test Outbox and Inbox failure matrix"
labels: [research, modular-monolith, reliability]
priority: high
---

## Context

At-least-once behavior needs evidence under crash, retry, duplicate, reorder, and poison messages.

## Acceptance criteria

- Define producer/consumer failure points.
- Verify idempotency and checkpoint recovery.
- Add backlog, retry, DLQ telemetry.
- Record expected delivery semantics.

## Evidence

Integration tests and database/broker traces.
