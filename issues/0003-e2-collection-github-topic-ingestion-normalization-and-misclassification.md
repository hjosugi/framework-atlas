# #3 E2 collection: GitHub Topic ingestion, normalization, and misclassification quarantine

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/3
- Updated: 2026-08-02T07:01:56Z

## Metadata
- State: complete
- Tracker role: execution lane
- Parent: [A0 #1](https://github.com/hjosugi/framework-atlas/issues/1)
- Blocked on: E1 schema for final normalized output; collector core can start

## Outcome

GitHub Search API から topic candidates を再現可能に取得し、1000件上限を created-date range 分割で回避し、raw snapshot と normalized catalog candidate を生成する。

## Topics in scope

`framework`, `web-framework`, `router`, `middleware`, `dependency-injection`, `orm`, `state-management`, `runtime`。mobile/desktop/testing/AI/data は別 cohort として保持する。

## Artifacts

- standard-library-only `scripts/collect_github.py`
- `scripts/normalize_snapshot.py`
- `data/rules/classification.v1.json`
- raw snapshot manifest
- offline API fixtures and unit tests
- quarantine output with reason codes

## Gates

- [x] query、time range、page、API revision、observed time を manifest に保存。
- [x] `total_count > 1000` は日付 range を再帰分割。
- [x] pagination、rate-limit、retry-after、resume checkpoint を実装。
- [x] repo alias/fork/archived/renamed を決定的に正規化。
- [x] VPN、router OS、security exploit、Android navigation等を黙って削除せず reason付き quarantine。
- [x] token/secret/raw authorization header を一切保存しない。
- [x] CI は offline fixture、network refresh は明示的 scheduled/manual job。

## Non-goals

GitHub HTML scraping、星数による採用判断、自動でdeep profileへ昇格。

## Children

- [x] [#13](https://github.com/hjosugi/framework-atlas/issues/13) C1 topic collector/splitting
- [x] [#14](https://github.com/hjosugi/framework-atlas/issues/14) C2 pagination/checkpoints
- [x] [#15](https://github.com/hjosugi/framework-atlas/issues/15) C3 normalization/deduplication
- [x] [#16](https://github.com/hjosugi/framework-atlas/issues/16) C4 classifier/quarantine
- [x] [#17](https://github.com/hjosugi/framework-atlas/issues/17) C5 offline contract tests
