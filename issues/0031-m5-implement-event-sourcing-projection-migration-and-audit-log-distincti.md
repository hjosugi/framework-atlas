# #31 M5 implement event-sourcing, projection, migration, and audit-log distinctions

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/31
- Updated: 2026-08-02T05:42:12Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M1

## Artifacts
event store/projection/checkpoint flow、migration matrix、terminology gates。

## Implementation
aggregate rehydration、optimistic stream version、projection subscription、checkpoint、eventual consistency、snapshot未実装、DB migration/current schema versioningを抽出する。

## Acceptance
- [ ] event sourcingとaudit logをvalidator ruleで区別。
- [ ] event schema/version/upcasting未解決点を記録。
- [ ] projection replay/idempotency/checkpoint transaction境界を明示。
- [ ] snapshot absentをfeatureとして誤記しない。
- [ ] migration rollback/destructive change policyを比較。
- [ ] framework mappingでstorage libraryをcore requirementにしない。

## Non-goals
EventStore実装、case library推奨の現行性を無検証で断定。
