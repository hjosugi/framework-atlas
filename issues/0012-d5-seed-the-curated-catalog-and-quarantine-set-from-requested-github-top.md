# #12 D5 seed the curated catalog and quarantine set from requested GitHub Topics

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/12
- Updated: 2026-08-02T07:00:34Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E1 #2](https://github.com/hjosugi/framework-atlas/issues/2)
- Blocked on: D1-D3

## Artifacts
初期 `entities/claims` data と quarantine fixture。

## Mandatory included seeds
Spring Boot、FastAPI、Gin、Rails、Laravel、Django、React、Vue、Elysia、Hono、axum、Fiber、chi、gorilla/mux、httprouter、uWebSockets、vue-router、TanStack Router、Mithril、single-spa、UI-Router、path-to-regexp、wouter、Symfony Routing、Drizzle、PostgREST、Tauri、Ionic、Expo、Bubble Tea、Textual、LangGraph、LlamaIndex。

## Mandatory quarantine examples
Lantern、RouterSploit、iStoreOS、ARouter。各対象はtopic hitを保持し、framework Atlas本体から分離する理由を記録する。

## Acceptance
- [x] 全seedにofficial repo、kind/cohort、profile level、observed date。
- [x] user指定対象を欠落させない。
- [x] quarantineを削除扱いにしない。
- [x] metric欄はevidenceまたはunmeasured。
- [x] validatorが全件通る。

## Non-goals
全候補のdeep profile、星順。
