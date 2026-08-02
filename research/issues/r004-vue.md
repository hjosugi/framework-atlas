---
title: "Vue の設計影響源を一次・準一次資料で検証する"
labels: "research,frontend,influence-graph,priority/p1"
---

# Vue の設計影響源を一次・準一次資料で検証する

## 背景

AngularJS、React、Knockout 等との関係について creator talk/interview/release note を調べ、direct influence、convergent design、shared-era pattern を区別する。

## 完了条件

- [ ] 各 edge に quote-free summary と URL
- [ ] confidence を high/medium/low で更新
- [ ] 推測を official claim と混同しない

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R004 -->
