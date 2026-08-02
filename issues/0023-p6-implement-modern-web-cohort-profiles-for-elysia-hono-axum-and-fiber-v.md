# #23 P6 implement modern Web cohort profiles for Elysia, Hono, axum, and Fiber v3

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/23
- Updated: 2026-08-02T07:00:56Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E3 #4](https://github.com/hjosugi/framework-atlas/issues/4)
- Blocked on: D1-D3

## Official inputs
https://elysiajs.com/、https://hono.dev/docs、https://docs.rs/axum/latest/axum/、https://docs.gofiber.io/next/。

## Artifacts
standard/deep profiles、relations、same-fixture comparison schema。

## Implementation
Elysiaのschema/type/DX、HonoのWeb Standards/multi-runtime/router selection、axumのextractor/Tower/Tokio、Fiber v3のfasthttp/zero-allocation/batteriesを同じHTTP conformance dimensionsで収録する。

## Acceptance
- [x] observed version/beta statusをsource/date付きで記録。
- [x] runtimeとframeworkの寄与を分離。
- [x] request value lifetime、ambient context、middleware stateを比較。
- [x] performanceはunmeasuredまたはraw evidenceのみ。
- [x] portability claimをhost adapter matrixへ落とす。
- [x] kofun-boot R1/R6 issueへのimplementation mapping。

## Non-goals
本repo内で各runtimeをinstall/benchmark。
