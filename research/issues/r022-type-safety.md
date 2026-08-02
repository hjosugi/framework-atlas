---
title: "Type safety の意味を層別に比較する"
labels: "research,types,comparison,priority/p2"
---

# Type safety の意味を層別に比較する

## 背景

route params、request validation、DB query、server-client RPC、template、state、DI、codegen のどこが compile-time/runtime で検査されるかを分ける。

## 完了条件

- [ ] 単一の type-safe ラベルを廃止
- [ ] FastAPI/Nest/Hono/TanStack/Servant/Goa/Prisma を比較
- [ ] generated client と shared types を区別

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R022 -->
