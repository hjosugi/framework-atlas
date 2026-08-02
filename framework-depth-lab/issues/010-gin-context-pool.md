---
title: "Test Gin Context pooling and goroutine safety"
labels: [research, gin, concurrency]
priority: high
---

## Context

Demonstrate request lifetime, `Context.Copy`, response writer limits, cancellation, and race risks.

## Acceptance criteria

- Pin v1.12.0 context/engine source.
- Add race-detector tests for unsafe and safe patterns.
- Document objects that may cross request lifetime.
- Verify cancellation propagation.

## Evidence

Tagged source, official docs, `go test -race` output.
