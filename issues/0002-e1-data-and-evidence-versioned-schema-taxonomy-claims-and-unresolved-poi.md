# #2 E1 data and evidence: versioned schema, taxonomy, claims, and unresolved points

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/2
- Updated: 2026-08-02T07:01:54Z

## Metadata
- State: complete
- Tracker role: execution lane
- Parent: [A0 #1](https://github.com/hjosugi/framework-atlas/issues/1)
- Blocked on: nothing

## Outcome

Atlas の全表示を駆動する versioned data model を実装する。Markdown を source-of-truth にしない。

## Artifacts

- `schema/atlas-v1.schema.json`
- `data/entities.v1.json`
- `data/relations.v1.json`
- `data/claims.v1.json`
- `data/unresolved.v1.json`
- `data/taxonomy.v1.json`
- `scripts/validate.py` と破壊 fixture

## Required fields

entity は stable id、kind、cohort、profile level、language、first release evidence、official repo/docs、observed revision/date、design traits、strengths、trade-offs、topic disposition を持つ。claim/edge は subject、predicate/type、source URL、evidence kind (`official|primary-code|inference`)、confidence、observed date を持つ。metric は evidence pointer または `unmeasured`。

## Gates

- [x] 不明 field、欠落 source/date、dangling relation、重複 alias を拒否。
- [x] official と inference を同一 enum に潰さない。
- [x] framework/router/library/platform/case-study を区別。
- [x] deep/standard/seed の必須 field が段階別に検証される。
- [x] 未解決点は owner entity、status、last reviewed、resolution issue を持つ。
- [x] 同じ入力の normalized JSON が byte-identical。

## Non-goals

UI、network collection、人気 score、framework固有 profile本文。

## Children

- [x] [#8](https://github.com/hjosugi/framework-atlas/issues/8) D1 schema/validator
- [x] [#9](https://github.com/hjosugi/framework-atlas/issues/9) D2 taxonomy/aliases
- [x] [#10](https://github.com/hjosugi/framework-atlas/issues/10) D3 claims/metrics evidence
- [x] [#11](https://github.com/hjosugi/framework-atlas/issues/11) D4 unresolved points
- [x] [#12](https://github.com/hjosugi/framework-atlas/issues/12) D5 initial catalog/quarantine
