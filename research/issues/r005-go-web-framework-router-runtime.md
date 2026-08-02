---
title: "Go Web framework 系譜を router/runtime 単位で精密化する"
labels: "research,go,router,priority/p1"
---

# Go Web framework 系譜を router/runtime 単位で精密化する

## 背景

net/http、httprouter、Martini、Gin、chi、Echo、fasthttp、Fiber、GoFrame、CloudWeGo の関係を API、router、context、middleware、runtime の各層に分ける。

## 完了条件

- [ ] built-on と API-inspired を分離
- [ ] standard http.Handler compatibility を記録
- [ ] benchmark claim は独立 issue に分離

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R005 -->
