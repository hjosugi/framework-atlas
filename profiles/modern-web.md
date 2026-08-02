# Elysia・Hono・axum・Fiber — 現代Web frameworkの異なる最適化

確認日: 2026-08-02。観測release: Elysia 1.4.29、Hono 4.12.33、axum 0.8.9、Fiber 3.4.0。いずれもstable release tagとして観測し、beta扱いを推定しない。

| 対象 | 主たる設計単位 | 得意な境界 | 注意点 |
|---|---|---|---|
| Elysia | schema + lifecycle + TypeScript inference | Bunで短い型付きAPIとend-to-end contract | runtime portabilityとcompile/runtime schema差を測る |
| Hono | Web Standards Request/Response + adapter | edgeを含むmulti-runtime portability | runtimeごとのcapability差はadapter外へ漏らさない |
| axum | handler + extractor + Tower service | Rust type system、async ecosystem、middleware reuse | compile-time複雑性とerror型の設計がDXを左右 |
| Fiber | Express風routing/middleware on fasthttp | Goで親しみやすいHTTP API | net/http互換性とfasthttp前提を選択として扱う |

四者を「速い新世代」と一括りにしない。Elysiaは推論、Honoはstandards portability、axumはtyped extraction/service composition、FiberはAPI ergonomicsという異なる軸を強くする。Bun、Cloudflare/Deno/Node、Tokio/Hyper、fasthttpのruntime寄与をframework自身の寄与から分ける。request value lifetimeは、Elysia lifecycle context、Hono Context、axum extractor ownership、Fiber Contextの再利用/ambient stateという別条件で比較する。middleware stateをrequest外へ保持しない。性能主張は機能同等の公開測定なしにAtlasの順位へ変換しない。

host adapter matrixではHonoをWeb Standards中心の複数runtime、ElysiaをBun中心、axumをTokio/Hyper、Fiberをfasthttpとして記録する。portableという語は全capability同等を意味しない。`kofun-boot` R1（typed Web contract）へschema/extractor設計を、R6（runtime portability）へprotocol core + explicit adapterをmappingする。

`kofun-boot` はtyped route declaration、portable runtime adapter、extractor errorのclosed type、middleware/service compositionを組み合わせられる。ただし一つの巨大generic型や暗黙contextへ集約せず、compile diagnosticsとincremental buildを受入条件に含める。

## Sources

- https://elysiajs.com/
- https://hono.dev/docs/
- https://docs.rs/axum/latest/axum/
- https://docs.gofiber.io/
- https://github.com/elysiajs/elysia/releases/tag/1.4.29
- https://github.com/honojs/hono/releases/tag/v4.12.33
- https://github.com/tokio-rs/axum/releases/tag/axum-v0.8.9
- https://github.com/gofiber/fiber/releases/tag/v3.4.0
