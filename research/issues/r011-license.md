---
title: "License と商用条件を監査する"
labels: "research,license,governance,priority/p1"
---

# License と商用条件を監査する

## 背景

repository license、dual license、commercial license、source-available、plugin license を記録し、framework adoption の制約を比較する。

## 完了条件

- [ ] SPDX expression を優先
- [ ] Qt/JUCE/Unreal/Unity 等を別扱い
- [ ] unknown を推測で埋めない

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R011 -->
