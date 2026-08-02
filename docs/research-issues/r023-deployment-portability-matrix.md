---
title: "Deployment portability matrix を追加する"
labels: "research,deployment,edge,priority/p2"
---

# Deployment portability matrix を追加する

## 背景

process、container、serverless、edge、WASI、mobile store、desktop bundle、SSH/TUI の deployment target と adapter lock-in を記録する。

## 完了条件

- [ ] runtime standard と vendor adapter を分離
- [ ] cold start claim は測定条件を付与
- [ ] same code の制約を明記

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R023 -->
