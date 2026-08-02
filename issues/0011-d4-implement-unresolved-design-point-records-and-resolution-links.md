# #11 D4 implement unresolved-design-point records and resolution links

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/11
- Updated: 2026-08-02T07:00:33Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E1 #2](https://github.com/hjosugi/framework-atlas/issues/2)
- Blocked on: D1 schema

## Artifacts
`data/unresolved.v1.json`, validator、generated unresolved index.

## Implementation
未解決点をentity、dimension、problem、known options、trade-off、status、last_reviewed、resolution issueへ結ぶ。例: implicit DI visibility、async cancellation、router ambiguity、ORM leakage、SSR/CSR境界、native/edge portability。

## Acceptance
- [x] owner entityとimplementation issueが必須。
- [x] resolved時にdecision/evidence linkが必須。
- [x] 放置項目をfreshness reportが検出。
- [x] profile本文との孤立を拒否。
- [x] UIでcohort/dimension/status filter可能なdataになる。

## Non-goals
議論だけのissue、期限なしTODO文字列。
