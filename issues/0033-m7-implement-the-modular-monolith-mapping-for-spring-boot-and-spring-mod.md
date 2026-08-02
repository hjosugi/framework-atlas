# #33 M7 implement the modular-monolith mapping for Spring Boot and Spring Modulith

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/33
- Updated: 2026-08-02T07:01:15Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M2-M6, P1

## Artifacts
Spring Boot mapping table、module/package skeleton、conformance gate specification。

## Implementation
bounded context→application module、composition root→explicit configuration、command/query pipeline、Spring Data/raw SQL、events/outbox、Actuator/observability、Spring Modulith testsへの対応を示す。

## Acceptance
- [x] auto-configとmodule-owned configを分離。
- [x] bean containerをdomain modelへ漏らさない。
- [x] transaction/event publication boundaryを明示。
- [x] Spring Modulithをcaseと同一物と扱わない。
- [x] architecture test例をartifact pathまで指定。
- [x] adopt/adapt/rejectと理由を各patternに持つ。

## Non-goals
動くSpring application全実装。
