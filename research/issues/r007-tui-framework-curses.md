---
title: "TUI framework の歴史を curses 以前から整理する"
labels: "research,tui,history,priority/p1"
---

# TUI framework の歴史を curses 以前から整理する

## 背景

curses、Turbo Vision、Urwid、prompt_toolkit、Rich/Textual、Elm Architecture 系 Bubble Tea/Iced/Ratatui、Terminal.Gui、Ink を timeline と設計比較に追加する。

## 完了条件

- [ ] retained/immediate/reactive/MVU を比較
- [ ] input/layout/render diff model を記録
- [ ] terminal と browser delivery の差を整理

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R007 -->
