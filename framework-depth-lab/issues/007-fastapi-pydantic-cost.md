---
title: "Profile Pydantic validation and serialization cost"
labels: [research, fastapi, performance]
priority: high
---

## Context

Measure small, nested, large-list, response-filtered, and invalid payloads.

## Acceptance criteria

- Fix Python/FastAPI/Pydantic versions.
- Compare validation and serialization separately.
- Capture CPU profiles and allocations.
- Retain validation equivalence across variants.

## Evidence

Official APIs and reproducible raw results.
