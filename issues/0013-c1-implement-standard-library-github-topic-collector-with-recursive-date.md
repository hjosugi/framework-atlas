# #13 C1 implement standard-library GitHub Topic collector with recursive date splitting

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/13
- Updated: 2026-08-02T07:00:36Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E2 #3](https://github.com/hjosugi/framework-atlas/issues/3)
- Blocked on: nothing

## Artifacts
`scripts/collect_github.py` とquery split unit tests。

## Implementation
GitHub Search APIをtopic + created rangeで取得し、`total_count > 1000`なら範囲を再帰二分する。1日範囲でも上限超過ならtruncatedを隠さずmanifestへ記録する。

## Acceptance
- [x] argparseでtopic/from/to/output。
- [x] Python標準ライブラリのみ。
- [x] Accept/API-Version/User-Agentを明示。
- [x] query/range/pageをmanifestへ保存。
- [x] simulated 999/1001件fixtureでsplit境界検証。
- [x] tokenを出力/ログへ書かない。

## Non-goals
HTML scraping、分類、profile生成。
