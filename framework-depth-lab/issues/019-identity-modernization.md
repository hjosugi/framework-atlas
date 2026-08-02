---
title: "Replace IdentityServer4 and password grant in the case study"
labels: [research, modular-monolith, security]
priority: high
---

## Context

IdentityServer4 is archived and Resource Owner Password Credentials is unsuitable for new deployments.

## Acceptance criteria

- Select maintained OIDC provider options.
- Map browser, machine, and test-user flows.
- Preserve permission-based authorization.
- Add key rotation, issuer, audience, and expiry tests.

## Evidence

Current OAuth/OIDC guidance and provider documentation.
