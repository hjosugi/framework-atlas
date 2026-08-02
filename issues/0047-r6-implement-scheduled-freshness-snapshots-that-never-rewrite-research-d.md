# #47 R6 implement scheduled freshness snapshots that never rewrite research decisions

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/47
- Updated: 2026-08-02T05:43:40Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: C1-C5, D3-D4, R3

## Artifacts
scheduled/manual workflow、freshness report、review artifact schema。

## Implementation
topic snapshots、repo redirect/archive、official version/source availability、review_due unresolved pointsを検出する。workflowはreport artifactまたはdraft changeを作るだけで、approved data/decisionを直接変更しない。

## Acceptance
- [ ] minimal read permissions/token。
- [ ] partial/rate-limit時にsuccess/freshを主張しない。
- [ ] last successful/attempted snapshotを区別。
- [ ] changed sourceをclaim id単位で表示。
- [ ] deleted/unreachableをhistorical recordから消さない。
- [ ] user reviewなしにadopt/reject edgeを更新しない。

## Non-goals
自動merge、自動Issue大量生成、daily noise。
