---
title: "Measure Spring Boot JVM versus AOT native image trade-offs"
labels: [research, spring-boot, performance]
priority: medium
---

## Context

Quantify cold start, RSS, build time, image size, peak throughput, and reflection constraints.

## Acceptance criteria

- Pin GraalVM and Boot versions.
- Use identical application features.
- Save native hints and build logs.
- Report warm and cold measurements separately.

## Evidence

Official native image documentation and raw benchmark artifacts.
