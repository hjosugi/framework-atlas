# #33 M7 implement the modular-monolith mapping for Spring Boot and Spring Modulith

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/33
- Updated: 2026-08-02T05:42:14Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M2-M6, P1

## Artifacts
Spring Boot mapping table、module/package skeleton、conformance gate specification。

## Implementation
bounded context→application module、composition root→explicit configuration、command/query pipeline、Spring Data/raw SQL、events/outbox、Actuator/observability、Spring Modulith testsへの対応を示す。

## Acceptance
- [ ] auto-configとmodule-owned configを分離。
- [ ] bean containerをdomain modelへ漏らさない。
- [ ] transaction/event publication boundaryを明示。
- [ ] Spring Modulithをcaseと同一物と扱わない。
- [ ] architecture test例をartifact pathまで指定。
- [ ] adopt/adapt/rejectと理由を各patternに持つ。

## Non-goals
動くSpring application全実装。
