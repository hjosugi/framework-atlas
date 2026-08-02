---
title: "router topic の語義衝突を全件分類する"
labels: "research,taxonomy,router,priority/p0"
---

# router topic の語義衝突を全件分類する

## 背景

Web router/navigation、HTTP proxy、network router firmware、VPN、security framework、application を分類する。現在の user snapshot では 7,267 repositories が表示されているため自動 rule と manual review queue を併用する。

## 完了条件

- [ ] classification rule が test で固定される
- [ ] low-confidence candidate が review queue に出る
- [ ] network product を framework catalog の既定表示から除外する

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R002 -->
