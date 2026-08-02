---
title: "非英語圏 framework ecosystem を拡充する"
labels: "research,global,coverage,priority/p2"
---

# 非英語圏 framework ecosystem を拡充する

## 背景

中国、日本、韓国、東欧、南米などで広く使われる Go/PHP/Java/Android/mini-app frameworks を公式資料から追加する。

## 完了条件

- [ ] 地域 popularity を star 数だけで判断しない
- [ ] 原語名と英語 alias を保持
- [ ] governance と documentation language を記録

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R016 -->
