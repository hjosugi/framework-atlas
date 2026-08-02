---
title: "Apply an equivalent API security baseline"
labels: [engineering, security]
priority: high
---

## Context

Compare OIDC validation, authorization, input limits, proxy trust, CORS, and safe errors.

## Acceptance criteria

- Use one issuer/audience contract.
- Add negative tests for token and ownership failures.
- Document reverse-proxy assumptions.
- Run dependency and container scans.

## Evidence

Official framework security docs and current standards.
