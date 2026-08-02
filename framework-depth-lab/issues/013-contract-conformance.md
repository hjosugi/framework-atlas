---
title: "Automate OpenAPI contract conformance across all examples"
labels: [engineering, contract-testing]
priority: high
---

## Context

The three examples should return the same status and normalized problem schema.

## Acceptance criteria

- Validate requests/responses against OpenAPI 3.1.
- Normalize 404 and 422 response bodies.
- Run the same black-box suite against three base URLs.
- Add CI matrix.

## Evidence

OpenAPI contract and test reports.
