---
title: "GitHub Topics 全件収集を初回実行し snapshot を固定する"
labels: "research,automation,github-topics,priority/p0"
---

# GitHub Topics 全件収集を初回実行し snapshot を固定する

## 背景

scripts/collect_github_topics.py を GITHUB_TOKEN 付きで実行し、framework/router/orm/tui 等の全 topic を created date で再帰分割して取得する。重複を canonical repository ID で統合し、取得時刻と query を保存する。

## 完了条件

- [ ] 各 topic の total_count と取得件数が記録される
- [ ] 1000件制限を超える query が分割される
- [ ] 途中再開可能な checkpoint が残る

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R001 -->
