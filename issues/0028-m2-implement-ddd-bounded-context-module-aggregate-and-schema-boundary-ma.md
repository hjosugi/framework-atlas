# #28 M2 implement DDD bounded-context, module, aggregate, and schema-boundary mappings

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/28
- Updated: 2026-08-02T05:42:09Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M1

## Artifacts
DDD/module boundary matrix、domain model data、failure-mode records。

## Implementation
bounded context、module API、aggregate/value object/domain event、persistence ignorance、module-private DB schema、integration-event-only dependencyを抽出し、framework-neutral ports/capabilitiesへ正規化する。

## Acceptance
- [ ] tactical/strategic DDDとcaseのout-of-scopeを区別。
- [ ] class encapsulationを言語非依存のinvariantへ変換。
- [ ] shared databaseとshared schemaを区別。
- [ ] aggregate transaction boundaryを明記。
- [ ] module分割コストと単純CRUDでの過剰設計riskを記録。
- [ ] Spring/FastAPI/Gin/Kofun mapping用interfaceを定義。

## Non-goals
全domain要件の転載、OOP inheritance必須化。
