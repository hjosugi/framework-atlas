---
title: "Accessibility と internationalization の比較軸を追加する"
labels: "research,accessibility,i18n,priority/p2"
---

# Accessibility と internationalization の比較軸を追加する

## 背景

Web/mobile/desktop/TUI framework で semantic output、focus、screen reader、RTL、locale、IME、keyboard navigation の support model を比較する。

## 完了条件

- [ ] platform limitation と framework support を分離
- [ ] official accessibility guide を source 化
- [ ] TUI/browser/native の比較を行う

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R015 -->
