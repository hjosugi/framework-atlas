# #10 D3 implement evidence claims, metric provenance, and official-vs-inference rules

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/10
- Updated: 2026-08-02T07:00:31Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E1 #2](https://github.com/hjosugi/framework-atlas/issues/2)
- Blocked on: D1 schema

## Artifacts
`data/claims.v1.json`, evidence policy, claim validator, destructive fixtures.

## Implementation
設計/歴史/性能claimをsubject-predicate-objectで表し、source URL、source kind、observed_at、revision、confidenceを必須にする。数値claimはraw evidence + method + environment、または `unmeasured`。

## Acceptance
- [x] marketing claimとAtlas measurementを別kindで保持。
- [x] official influenceと類似推論を相互変換不可。
- [x] sourceなし数値を拒否。
- [x] sourceの最大引用量ではなく要約とpointerだけを保存。
- [x] stale evidenceを削除せずreview_dueへ移す。

## Non-goals
benchmark実行、factの自動承認。
