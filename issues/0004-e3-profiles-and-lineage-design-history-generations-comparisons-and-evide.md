# #4 E3 profiles and lineage: design history, generations, comparisons, and evidence graph

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/4
- Updated: 2026-08-02T07:01:58Z

## Metadata
- State: complete
- Tracker role: execution lane
- Parent: [A0 #1](https://github.com/hjosugi/framework-atlas/issues/1)
- Blocked on: E1 schema

## Outcome

厳選 deep profiles と広範 catalog の二層を実装し、設計史・系譜・世代交代・長短所を evidence graph と比較表で表す。

## Mandatory deep subjects

Spring Boot、FastAPI、Gin、Rails、Laravel、Django、React、Vue。Web新世代として Elysia、Hono、axum、Fiber を standard以上で収録。router系は httprouter、chi、gorilla/mux、path-to-regexp、TanStack Router、Vue Router、Hono routers、uWebSocketsを分離して扱う。

## Artifacts

- `profiles/<id>.md` + data-backed summary
- `data/relations.v1.json`
- generation timeline
- comparison matrices: routing、DI、ORM/data model、state、middleware、runtime、DX、production
- unresolved design points

## Edge rules

各 edge は `built-on|officially-inspired-by|successor-of|component-of|competes-with|resembles` のいずれか。方向、確度、公式根拠または inference 理由を必須にする。`resembles` を公式 influence と表示しない。

## Gates

- [x] 各deep profileが history、philosophy、execution model、extension model、data model、strengths、trade-offs、unresolved、sourcesを持つ。
- [x] first-release/current-version を観測 source に結ぶ。
- [x] 世代分類は評価語でなく設計変化として説明。
- [x] graph の全 node/edge が schema validationを通る。
- [x] framework と ecosystem component を混同しない。
- [x] 比較不能な欄は `not-applicable`。

## Non-goals

総合優勝者、根拠なし系譜、marketing benchmark転載。

## Children

- [x] [#18](https://github.com/hjosugi/framework-atlas/issues/18) P1 Spring Boot
- [x] [#19](https://github.com/hjosugi/framework-atlas/issues/19) P2 FastAPI
- [x] [#20](https://github.com/hjosugi/framework-atlas/issues/20) P3 Gin
- [x] [#21](https://github.com/hjosugi/framework-atlas/issues/21) P4 Rails/Laravel/Django
- [x] [#22](https://github.com/hjosugi/framework-atlas/issues/22) P5 React/Vue
- [x] [#23](https://github.com/hjosugi/framework-atlas/issues/23) P6 modern Web cohort
- [x] [#24](https://github.com/hjosugi/framework-atlas/issues/24) P7 router lineage
- [x] [#25](https://github.com/hjosugi/framework-atlas/issues/25) P8 graph/timeline
- [x] [#26](https://github.com/hjosugi/framework-atlas/issues/26) P9 comparison matrices
