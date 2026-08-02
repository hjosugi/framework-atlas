# #34 M8 implement the modular-monolith mapping for FastAPI

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/34
- Updated: 2026-08-02T05:42:15Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M2-M6, P2

## Artifacts
FastAPI mapping table、Python package skeleton、conformance gate specification。

## Implementation
APIRouter/package boundary、lifespan composition root、Depends graph、Pydantic boundary DTO、pure domain model、command/query functions、SQL transaction/outbox worker、architecture import gatesへ対応させる。

## Acceptance
- [ ] request modelをdomain/DB modelと同一化しない案を示す。
- [ ] Dependsをdomain ambient dependencyにしない。
- [ ] async session/task lifetimeを明示。
- [ ] background tasksをdurable outboxと同一視しない。
- [ ] import/layer architecture gateを定義。
- [ ] adopt/adapt/rejectと理由を各patternに持つ。

## Non-goals
MediatR/IoCをPythonへ模倣、動く全アプリ。
