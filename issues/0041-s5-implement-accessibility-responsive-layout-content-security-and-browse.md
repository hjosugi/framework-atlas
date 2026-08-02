# #41 S5 implement accessibility, responsive layout, content security, and browser smoke gates

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/41
- Updated: 2026-08-02T05:43:34Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: S2-S4

## Artifacts
accessibility checklist/gates、responsive fixtures、browser smoke script、CSP-ready markup。

## Acceptance
- [ ] semantic headings/landmarks/labels/focus order。
- [ ] keyboard-onlyでsearch/filter/profile/graph。
- [ ] contrastとprefers-reduced-motion。
- [ ] 320px幅で横overflowを必要部分table/graphに限定。
- [ ] JS無効時にmethodology/data/ZIP link。
- [ ] no inline event handlers/eval/dynamic script。
- [ ] missing/corrupt dataのuser-facing error。
- [ ] local static server smokeがCIで通る。

## Non-goals
WCAG認証claim、browser analytics。
