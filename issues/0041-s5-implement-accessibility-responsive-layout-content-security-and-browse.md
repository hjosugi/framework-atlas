# #41 S5 implement accessibility, responsive layout, content security, and browser smoke gates

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/41
- Updated: 2026-08-02T07:01:29Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: S2-S4

## Artifacts
accessibility checklist/gates、responsive fixtures、browser smoke script、CSP-ready markup。

## Acceptance
- [x] semantic headings/landmarks/labels/focus order。
- [x] keyboard-onlyでsearch/filter/profile/graph。
- [x] contrastとprefers-reduced-motion。
- [x] 320px幅で横overflowを必要部分table/graphに限定。
- [x] JS無効時にmethodology/data/ZIP link。
- [x] no inline event handlers/eval/dynamic script。
- [x] missing/corrupt dataのuser-facing error。
- [x] local static server smokeがCIで通る。

## Non-goals
WCAG認証claim、browser analytics。
