# #40 S4 implement generation timeline, comparison matrices, unresolved tracker, and DDD case view

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/40
- Updated: 2026-08-02T05:43:33Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: P8-P9, M1-M10

## Artifacts
timeline、matrix、unresolved、case-study views。

## Implementation
世代をdesign shiftとして表示し、比較matrix cellをclaimへ、未解決点をresolution issueへ、DDD patternをSpring/FastAPI/Gin/kofun列へlinkする。

## Acceptance
- [ ] timeline eventにsource/date/uncertainty。
- [ ] matrixのunknown/absent/not-applicable/unmeasuredを区別。
- [ ] cellからevidenceへ到達。
- [ ] strengths/costsを対で表示。
- [ ] resolved itemにdecision link。
- [ ] caseのhistorical caveatを明示。

## Non-goals
総合score、年代だけの進歩物語。
