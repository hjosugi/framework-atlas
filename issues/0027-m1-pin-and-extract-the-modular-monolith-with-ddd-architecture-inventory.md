# #27 M1 pin and extract the modular-monolith-with-ddd architecture inventory

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/27
- Updated: 2026-08-02T05:42:08Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Source: https://github.com/kgrzybek/modular-monolith-with-ddd
- Blocked on: D1-D3

## Artifacts
pinned case-study entity、source manifest、pattern inventory、scope/caveat record。

## Implementation
観測commit/dateを固定し、module boundaries、composition roots、DDD、CQRS、decorators、events、Outbox/Inbox、event sourcing、migrations、tests、C4/ADR/CIを章/コード位置へ結ぶ。

## Acceptance
- [ ] README claimとcode evidenceを別pointerで保持。
- [ ] current revision/maintenance stateを記録。
- [ ] out-of-scopeと作者のdisclaimerを保持。
- [ ] 使用技術のversion/obsolete security exampleをhistorical caveat化。
- [ ] 長文転載せず要約とdeep link。
- [ ] pattern inventoryがE1 schemaを通る。

## Non-goals
fork、code copy、caseを唯一解とすること。
