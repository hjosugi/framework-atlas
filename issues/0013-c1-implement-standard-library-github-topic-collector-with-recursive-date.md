# #13 C1 implement standard-library GitHub Topic collector with recursive date splitting

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/13
- Updated: 2026-08-02T05:39:01Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E2 #3](https://github.com/hjosugi/framework-atlas/issues/3)
- Blocked on: nothing

## Artifacts
`scripts/collect_github.py` とquery split unit tests。

## Implementation
GitHub Search APIをtopic + created rangeで取得し、`total_count > 1000`なら範囲を再帰二分する。1日範囲でも上限超過ならtruncatedを隠さずmanifestへ記録する。

## Acceptance
- [ ] argparseでtopic/from/to/output。
- [ ] Python標準ライブラリのみ。
- [ ] Accept/API-Version/User-Agentを明示。
- [ ] query/range/pageをmanifestへ保存。
- [ ] simulated 999/1001件fixtureでsplit境界検証。
- [ ] tokenを出力/ログへ書かない。

## Non-goals
HTML scraping、分類、profile生成。
