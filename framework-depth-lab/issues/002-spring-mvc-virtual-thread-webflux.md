---
title: "Benchmark MVC platform threads, virtual threads, and WebFlux"
labels: [research, spring-boot, performance]
priority: high
---

## Context

Compare concurrency models under blocking DB, non-blocking I/O, and mixed workloads.

## Acceptance criteria

- Use identical contract and downstream latency.
- Record startup, p50/p95/p99, CPU, RSS, errors.
- Verify context propagation and cancellation.
- Publish raw results and environment.

## Evidence

Official Spring guidance plus reproducible measurements.
