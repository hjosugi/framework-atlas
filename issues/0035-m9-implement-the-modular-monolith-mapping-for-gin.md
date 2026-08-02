# #35 M9 implement the modular-monolith mapping for Gin

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/35
- Updated: 2026-08-02T05:42:17Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M2-M6, P3

## Artifacts
Gin mapping table、Go package skeleton、conformance gate specification。

## Implementation
route groups→thin adapters、explicit constructor wiring、Context→boundary DTO、domain package、command/query functions、sql.Tx/outbox worker、internal packages、dependency import gatesへ対応させる。

## Acceptance
- [ ] Gin Contextをdomain/applicationへ渡さない。
- [ ] frameworkなしconstructor wiringを第一案にする。
- [ ] goroutine/request lifetimeとshutdownを明示。
- [ ] transaction/outbox atomicityを具体化。
- [ ] Go internal/import cycle/static checksをarchitecture gateへ使う。
- [ ] adopt/adapt/rejectと理由を各patternに持つ。

## Non-goals
DI container/mediator導入の目的化、動く全アプリ。
