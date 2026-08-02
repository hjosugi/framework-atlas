# #39 S3 implement the interactive directed lineage graph with evidence inspection

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/39
- Updated: 2026-08-02T05:43:32Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: S1, P8

## Artifacts
vanilla SVG graph renderer、graph controls、layout fixtures。

## Implementation
arrow付き有向graph、relation type/confidence/official-inference/cohort filters、node/edge detailを実装する。edge選択でsource URL、observed date、rationaleを表示する。

## Acceptance
- [ ] officialとinferenceを色だけでなくtext/shapeで区別。
- [ ] keyboardでnode/edge選択。
- [ ] cycle/isolated node/large catalogでも操作可能。
- [ ] deterministic initial layout。
- [ ] reduced-motion対応。
- [ ] external graph libraryなし。

## Non-goals
force-layoutの物理精度、根拠なし自動edge。
