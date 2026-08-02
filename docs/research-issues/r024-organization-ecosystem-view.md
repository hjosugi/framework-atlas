---
title: "Organization ecosystem view を追加拡張する"
labels: "research,ecosystem,organization,priority/p2"
---

# Organization ecosystem view を追加拡張する

## 背景

Textualize、Spring、Rails、Laravel、Vue、Charmbracelet、TanStack、Tokio、CloudWeGo など organization 単位で core、component、tool、application を表示する。

## 完了条件

- [ ] repository owner と governance owner を分離
- [ ] fork/archive を重複排除
- [ ] dependency edge と marketing bundle を区別

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R024 -->
