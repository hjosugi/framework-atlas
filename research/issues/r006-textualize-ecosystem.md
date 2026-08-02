---
title: "Textualize ecosystem の組織内系譜を完成する"
labels: "research,tui,textual,priority/p1"
---

# Textualize ecosystem の組織内系譜を完成する

## 背景

Rich、Textual、Trogon、Textual Web、textual-serve、pytest-textual-snapshot、Frogmouth、Toolong の役割、dependency、release history を整理する。

## 完了条件

- [ ] framework/library/application/test tooling を区別
- [ ] Rich→Textual の technical dependency を source で確認
- [ ] browser delivery architecture を図示

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R006 -->
