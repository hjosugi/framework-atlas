---
title: "Framework benchmark claim の evidence policy を作る"
labels: "research,performance,methodology,priority/p2"
---

# Framework benchmark claim の evidence policy を作る

## 背景

公式 README の「N倍高速」等をそのまま比較値にせず、hardware、version、workload、serialization、TLS、DB を記録した reproducible benchmark のみ chart に採用する。

## 完了条件

- [ ] marketing claim と independent benchmark を分離
- [ ] TechEmpower 等の limitation を説明
- [ ] 日付と commit SHA を保存

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R018 -->
