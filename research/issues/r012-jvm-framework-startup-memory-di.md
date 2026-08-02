---
title: "JVM framework 世代交代を startup/memory/DI で比較する"
labels: "research,jvm,history,priority/p1"
---

# JVM framework 世代交代を startup/memory/DI で比較する

## 背景

Servlet/J2EE/EJB、Spring、Spring Boot、Dropwizard、Micronaut、Quarkus、Helidon を runtime scan、build-time processing、native image、virtual threads、reactive の軸で整理する。

## 完了条件

- [ ] 直接 influence と design response を分離
- [ ] version-neutral architecture を記録
- [ ] benchmark は reproducible source のみ採用

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R012 -->
