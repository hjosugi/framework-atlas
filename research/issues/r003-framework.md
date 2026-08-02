---
title: "重点 framework の一次資料レビューを完了する"
labels: "research,sources,deep-profile,priority/p0"
---

# 重点 framework の一次資料レビューを完了する

## 背景

Spring Boot、Laravel、Rails、React、Vue、Gin、Django、Textual の history、problem statement、influence edge を公式文書と repository history で再確認する。

## 完了条件

- [ ] 各 deep profile に最低2件の一次資料
- [ ] 断定 edge は official evidence を持つ
- [ ] 推定 edge は needs-evidence のまま表示される

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R003 -->
