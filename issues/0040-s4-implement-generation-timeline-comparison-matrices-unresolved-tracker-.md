# #40 S4 implement generation timeline, comparison matrices, unresolved tracker, and DDD case view

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/40
- Updated: 2026-08-02T07:01:27Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: P8-P9, M1-M10

## Artifacts
timeline、matrix、unresolved、case-study views。

## Implementation
世代をdesign shiftとして表示し、比較matrix cellをclaimへ、未解決点をresolution issueへ、DDD patternをSpring/FastAPI/Gin/kofun列へlinkする。

## Acceptance
- [x] timeline eventにsource/date/uncertainty。
- [x] matrixのunknown/absent/not-applicable/unmeasuredを区別。
- [x] cellからevidenceへ到達。
- [x] strengths/costsを対で表示。
- [x] resolved itemにdecision link。
- [x] caseのhistorical caveatを明示。

## Non-goals
総合score、年代だけの進歩物語。
