---
title: "Data model/ORM 比較 matrix を拡張する"
labels: "research,orm,data-model,priority/p1"
---

# Data model/ORM 比較 matrix を拡張する

## 背景

Active Record、Data Mapper、Unit of Work、schema-first、SQL-first、codegen の軸で Hibernate、Rails Active Record、Eloquent、Django ORM、SQLAlchemy、EF Core、Prisma、Ent、sqlc、Diesel を比較する。

## 完了条件

- [ ] identity map/dirty checking/lazy loading を記録
- [ ] migration と transaction boundary を比較
- [ ] N+1 と generated SQL observability を比較

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R008 -->
