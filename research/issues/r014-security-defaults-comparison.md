---
title: "Security defaults comparison を追加する"
labels: "research,security,comparison,priority/p1"
---

# Security defaults comparison を追加する

## 背景

CSRF、XSS escaping、session cookie、CORS、request size、dependency advisory、secret/config handling の既定値を重点 Web frameworks で比較する。

## 完了条件

- [ ] official security docs のみを根拠にする
- [ ] default と optional middleware を区別
- [ ] version/as-of date を明記

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R014 -->
