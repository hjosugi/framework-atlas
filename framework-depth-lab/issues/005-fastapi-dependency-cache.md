---
title: "Instrument FastAPI dependency resolution and request cache"
labels: [research, fastapi, internals]
priority: high
---

## Context

Show recursive dependency resolution, cache keys, `use_cache=False`, generator cleanup, and exception paths.

## Acceptance criteria

- Pin FastAPI 0.141.1 source lines.
- Add nested dependency tests.
- Record call and cleanup order.
- Explain thread-pool transitions.

## Evidence

Tagged source, official dependency documentation, executable tests.
