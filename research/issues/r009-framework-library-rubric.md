---
title: "framework と library の判定 rubric を検証する"
labels: "research,taxonomy,methodology,priority/p1"
---

# framework と library の判定 rubric を検証する

## 背景

lifecycle inversion、application skeleton、extension points、scope、opinionated defaults の点数化が React、Rich、chi、path-to-regexp、HTMX、TensorFlow に妥当か review する。

## 完了条件

- [ ] ambiguous case を最低20件評価
- [ ] single score だけでなく判定理由を保持
- [ ] community feedback 用の issue template を更新

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R009 -->
