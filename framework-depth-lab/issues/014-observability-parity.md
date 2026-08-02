---
title: "Implement observability parity for the three examples"
labels: [engineering, observability]
priority: high
---

## Context

Add equivalent request metrics, traces, structured logs, and correlation behavior.

## Acceptance criteria

- Use the same OpenTelemetry semantic conventions.
- Confirm propagation through async/background work.
- Redact sensitive fields.
- Measure instrumentation overhead.

## Evidence

Official OpenTelemetry integrations and captured telemetry.
