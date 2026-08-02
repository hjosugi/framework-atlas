# #3 E2 collection: GitHub Topic ingestion, normalization, and misclassification quarantine

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/3
- Updated: 2026-08-02T05:45:07Z

## Metadata
- State: ready
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

- [ ] query、time range、page、API revision、observed time を manifest に保存。
- [ ] `total_count > 1000` は日付 range を再帰分割。
- [ ] pagination、rate-limit、retry-after、resume checkpoint を実装。
- [ ] repo alias/fork/archived/renamed を決定的に正規化。
- [ ] VPN、router OS、security exploit、Android navigation等を黙って削除せず reason付き quarantine。
- [ ] token/secret/raw authorization header を一切保存しない。
- [ ] CI は offline fixture、network refresh は明示的 scheduled/manual job。

## Non-goals

GitHub HTML scraping、星数による採用判断、自動でdeep profileへ昇格。

## Children

- [ ] [#13](https://github.com/hjosugi/framework-atlas/issues/13) C1 topic collector/splitting
- [ ] [#14](https://github.com/hjosugi/framework-atlas/issues/14) C2 pagination/checkpoints
- [ ] [#15](https://github.com/hjosugi/framework-atlas/issues/15) C3 normalization/deduplication
- [ ] [#16](https://github.com/hjosugi/framework-atlas/issues/16) C4 classifier/quarantine
- [ ] [#17](https://github.com/hjosugi/framework-atlas/issues/17) C5 offline contract tests
