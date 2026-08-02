---
title: "Migration/upgrade cost の実例を収集する"
labels: "research,migration,maintainability,priority/p2"
---

# Migration/upgrade cost の実例を収集する

## 背景

AngularJS→Angular、Vue2→Vue3、Rails major、Spring Boot major、React Router/Remix、Prisma generation、Tauri major などの migration tooling と breaking boundary を整理する。

## 完了条件

- [ ] official migration guide を source 化
- [ ] code mod/compat mode/dual run を記録
- [ ] subjective pain score だけにしない

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R019 -->
