# #39 S3 implement the interactive directed lineage graph with evidence inspection

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/39
- Updated: 2026-08-02T07:01:25Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: S1, P8

## Artifacts
vanilla SVG graph renderer、graph controls、layout fixtures。

## Implementation
arrow付き有向graph、relation type/confidence/official-inference/cohort filters、node/edge detailを実装する。edge選択でsource URL、observed date、rationaleを表示する。

## Acceptance
- [x] officialとinferenceを色だけでなくtext/shapeで区別。
- [x] keyboardでnode/edge選択。
- [x] cycle/isolated node/large catalogでも操作可能。
- [x] deterministic initial layout。
- [x] reduced-motion対応。
- [x] external graph libraryなし。

## Non-goals
force-layoutの物理精度、根拠なし自動edge。
