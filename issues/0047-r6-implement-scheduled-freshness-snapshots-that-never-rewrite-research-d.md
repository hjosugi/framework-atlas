# #47 R6 implement scheduled freshness snapshots that never rewrite research decisions

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/47
- Updated: 2026-08-02T07:04:12Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: C1-C5, D3-D4, R3

## Artifacts
scheduled/manual workflow、freshness report、review artifact schema。

## Implementation
topic snapshots、repo redirect/archive、official version/source availability、review_due unresolved pointsを検出する。workflowはreport artifactまたはdraft changeを作るだけで、approved data/decisionを直接変更しない。

## Acceptance
- [x] minimal read permissions/token。
- [x] partial/rate-limit時にsuccess/freshを主張しない。
- [x] last successful/attempted snapshotを区別。
- [x] changed sourceをclaim id単位で表示。
- [x] deleted/unreachableをhistorical recordから消さない。
- [x] user reviewなしにadopt/reject edgeを更新しない。

## Non-goals
自動merge、自動Issue大量生成、daily noise。
