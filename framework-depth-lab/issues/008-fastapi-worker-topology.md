---
title: "Document FastAPI worker topology and graceful shutdown"
labels: [research, fastapi, operations]
priority: high
---

## Context

Clarify process count, memory isolation, readiness, drain, background work, and Kubernetes termination.

## Acceptance criteria

- Provide single and multi-worker diagrams.
- Test SIGTERM during active requests.
- Demonstrate why memory state is not shared.
- Add an operations checklist.

## Evidence

Official deployment docs and observed process traces.
