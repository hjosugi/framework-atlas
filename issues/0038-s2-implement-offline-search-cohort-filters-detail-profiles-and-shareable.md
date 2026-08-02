# #38 S2 implement offline search, cohort filters, detail profiles, and shareable URLs

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/38
- Updated: 2026-08-02T05:43:31Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: S1

## Artifacts
`docs/index.html`, search/filter/detail components in vanilla JS/CSS。

## Implementation
name/description/traits/language/topic検索、cohort/kind/profile/evidence/disposition filter、profile detail、source drill-downを実装し、URL query/hashに状態を保存する。

## Acceptance
- [ ] zero-result/invalid query/unknown profile。
- [ ] browser reload/back-forwardで状態維持。
- [ ] quarantineは明示filterでのみ表示。
- [ ] search resultがsource/evidence statusを示す。
- [ ] user dataをinnerHTMLへ入れない。
- [ ] 外部search/CDNなし。

## Non-goals
fuzzy rankingサービス、analytics。
