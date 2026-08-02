---
title: "Build Gin 1.12 binding and content negotiation matrix"
labels: [research, gin, validation]
priority: medium
---

## Context

Cover JSON, XML, form, query, header, URI, BSON, TextUnmarshaler, and protobuf negotiation.

## Acceptance criteria

- List content types and method behavior.
- Compare `Bind` and `ShouldBind` failure semantics.
- Add security limits for body and nesting.
- Provide tests for custom types.

## Evidence

Gin 1.12 release notes, tagged source, table-driven tests.
