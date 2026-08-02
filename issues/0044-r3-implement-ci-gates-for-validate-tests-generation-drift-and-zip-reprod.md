# #44 R3 implement CI gates for validate, tests, generation drift, and ZIP reproducibility

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/44
- Updated: 2026-08-02T07:01:34Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: D1, S1, R2

## Artifacts
GitHub Actions workflow と local one-command gate。

## Pipeline
validate schema/data → unit tests → build site → drift check → build ZIP twice → hash compare → extract/smoke。

## Acceptance
- [x] local commandとCIが同じscriptを呼ぶ。
- [x] networkなしでPR gate。
- [x] least permissions、pinned action major/version policy。
- [x] generated drift/metric source/issue digest failureを個別表示。
- [x] artifact uploadは検証後。
- [x] branch/PR triggersを明記。

## Non-goals
collector live APIを必須gateにすること。
