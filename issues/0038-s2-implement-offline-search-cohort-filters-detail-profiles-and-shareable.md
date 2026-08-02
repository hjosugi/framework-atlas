# #38 S2 implement offline search, cohort filters, detail profiles, and shareable URLs

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/38
- Updated: 2026-08-02T07:01:24Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: S1

## Artifacts
`docs/index.html`, search/filter/detail components in vanilla JS/CSS。

## Implementation
name/description/traits/language/topic検索、cohort/kind/profile/evidence/disposition filter、profile detail、source drill-downを実装し、URL query/hashに状態を保存する。

## Acceptance
- [x] zero-result/invalid query/unknown profile。
- [x] browser reload/back-forwardで状態維持。
- [x] quarantineは明示filterでのみ表示。
- [x] search resultがsource/evidence statusを示す。
- [x] user dataをinnerHTMLへ入れない。
- [x] 外部search/CDNなし。

## Non-goals
fuzzy rankingサービス、analytics。
