# #14 C2 implement pagination, rate-limit handling, checkpoints, and raw snapshot manifests

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/14
- Updated: 2026-08-02T07:00:39Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E2 #3](https://github.com/hjosugi/framework-atlas/issues/3)
- Blocked on: C1

## Artifacts
checkpoint format、snapshot manifest、resume/rate-limit tests。

## Implementation
per_page=100 pagination、rate-limit headers、bounded retry、Retry-After、途中checkpoint、atomic snapshot completionを実装する。不完全取得はcompleteに見せない。

## Acceptance
- [x] interruption後に最後の確定pageからresume。
- [x] 403 rate-limitと5xxを区別。
- [x] retry回数/待機上限をCLI設定。
- [x] raw recordsとmanifestのdigestを保存。
- [x] partial/rate_limited/truncated/complete stateを区別。
- [x] secret sanitization test。

## Non-goals
無限retry、判断dataの自動更新。
