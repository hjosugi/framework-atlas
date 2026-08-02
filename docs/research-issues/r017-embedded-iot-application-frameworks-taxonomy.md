---
title: "Embedded/IoT application frameworks を独立 taxonomy 化する"
labels: "research,embedded,iot,priority/p2"
---

# Embedded/IoT application frameworks を独立 taxonomy 化する

## 背景

Nerves、Zephyr、ESP-IDF、Arduino、Mbed OS、F Prime、Matter SDK 等を OS/SDK/framework/runtime に分ける。

## 完了条件

- [ ] hardware abstraction と application framework を区別
- [ ] real-time/fault tolerance/update model を記録
- [ ] network router firmware との誤分類を防ぐ

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R017 -->
