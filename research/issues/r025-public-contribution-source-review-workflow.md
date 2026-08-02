---
title: "Public contribution 用 source review workflow を整備する"
labels: "documentation,contributing,sources,priority/p3"
---

# Public contribution 用 source review workflow を整備する

## 背景

新規 profile/edge を追加する pull request template、source quality checklist、JSON schema validation、preview screenshot を整備する。

## 完了条件

- [ ] PR で validation が必須
- [ ] needs-evidence edge を自動検出
- [ ] content license と quote limit を明記

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R025 -->
