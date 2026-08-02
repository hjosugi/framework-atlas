# #5 E4 production architecture: modular monolith DDD case study and framework mappings

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/5
- Updated: 2026-08-02T05:45:11Z

## Metadata
- State: ready
- Tracker role: execution lane
- Parent: [A0 #1](https://github.com/hjosugi/framework-atlas/issues/1)
- Primary case: https://github.com/kgrzybek/modular-monolith-with-ddd
- Blocked on: E1 schema

## Outcome

framework 機能比較だけでなく、その上に本番級 application architecture をどう構成するかを実装対応表にする。

## Extracted patterns

bounded context/module、composition root、DDD tactical model、CQRS、decorator cross-cutting concerns、module-private schema、integration events、Outbox/Inbox、eventual consistency、event sourcing、migration、architecture tests、integration/system tests、mutation tests、C4/ADR。

## Artifacts

- case-study profile with current revision/date
- pattern inventory with benefits, costs, failure modes
- Spring Boot / FastAPI / Gin / kofun-boot mapping tables
- “copy / adapt / reject” decision per mapping
- sequence diagrams as data/text
- architecture conformance checks specification

## Gates

- [ ] case repositoryが主張するものとAtlasの評価を分離。
- [ ] OOP固有実装を普遍パターンとして扱わない。
- [ ] FastAPI/Ginにcontainer/mediatorを無理に移植しない。
- [ ] Outbox/Inboxのat-least-once、idempotency、ordering、transaction boundaryを明記。
- [ ] event sourcingとaudit logを区別。
- [ ] kofun-boot mappingは capability、closed ADT、replay gateへ具体的に着地。
- [ ] 古いsecurity/auth例は現行推奨として転載せず historical caveat にする。

## Non-goals

case repositoryのfork、完全アプリ再実装、特定architectureの万能化。

## Children

- [ ] [#27](https://github.com/hjosugi/framework-atlas/issues/27) M1 pinned case inventory
- [ ] [#28](https://github.com/hjosugi/framework-atlas/issues/28) M2 DDD/module boundaries
- [ ] [#29](https://github.com/hjosugi/framework-atlas/issues/29) M3 CQRS/decorators
- [ ] [#30](https://github.com/hjosugi/framework-atlas/issues/30) M4 Outbox/Inbox
- [ ] [#31](https://github.com/hjosugi/framework-atlas/issues/31) M5 event sourcing/migrations
- [ ] [#32](https://github.com/hjosugi/framework-atlas/issues/32) M6 architecture/testing gates
- [ ] [#33](https://github.com/hjosugi/framework-atlas/issues/33) M7 Spring mapping
- [ ] [#34](https://github.com/hjosugi/framework-atlas/issues/34) M8 FastAPI mapping
- [ ] [#35](https://github.com/hjosugi/framework-atlas/issues/35) M9 Gin mapping
- [ ] [#36](https://github.com/hjosugi/framework-atlas/issues/36) M10 kofun-boot mapping
