---
title: "Archived/EOL/maintenance 状態を自動監査する"
labels: "research,maintenance,automation,priority/p1"
---

# Archived/EOL/maintenance 状態を自動監査する

## 背景

GitHub archived flag、latest release、default branch push、official EOL announcement を別 signal として保存する。単純な最終 commit 日だけで dead 判定しない。

## 完了条件

- [ ] status evidence と observed_at を保存
- [ ] AngularJS/Truffle 等の known EOL を test fixture 化
- [ ] active-but-stable project を誤判定しない

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R010 -->
