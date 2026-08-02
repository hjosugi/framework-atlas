# #28 M2 implement DDD bounded-context, module, aggregate, and schema-boundary mappings

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/28
- Updated: 2026-08-02T07:01:05Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M1

## Artifacts
DDD/module boundary matrix、domain model data、failure-mode records。

## Implementation
bounded context、module API、aggregate/value object/domain event、persistence ignorance、module-private DB schema、integration-event-only dependencyを抽出し、framework-neutral ports/capabilitiesへ正規化する。

## Acceptance
- [x] tactical/strategic DDDとcaseのout-of-scopeを区別。
- [x] class encapsulationを言語非依存のinvariantへ変換。
- [x] shared databaseとshared schemaを区別。
- [x] aggregate transaction boundaryを明記。
- [x] module分割コストと単純CRUDでの過剰設計riskを記録。
- [x] Spring/FastAPI/Gin/Kofun mapping用interfaceを定義。

## Non-goals
全domain要件の転載、OOP inheritance必須化。
