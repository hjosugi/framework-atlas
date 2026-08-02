---
title: "Extend Gin router benchmark to an end-to-end API"
labels: [research, gin, performance]
priority: high
---

## Context

Measure TLS, JSON validation, auth, tracing, logging, and database rather than router alone.

## Acceptance criteria

- Preserve equivalent features across frameworks.
- Publish configuration and raw results.
- Report CPU, RSS, error, p50/p95/p99.
- Explain differences from official router benchmark.

## Evidence

Official benchmark as baseline plus reproducible application data.
