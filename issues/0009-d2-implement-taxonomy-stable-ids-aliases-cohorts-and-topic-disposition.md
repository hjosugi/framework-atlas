# #9 D2 implement taxonomy, stable IDs, aliases, cohorts, and topic disposition

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/9
- Updated: 2026-08-02T07:00:29Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E1 #2](https://github.com/hjosugi/framework-atlas/issues/2)
- Blocked on: D1 schema

## Artifacts
`data/taxonomy.v1.json`, alias rules, taxonomy validation fixtures.

## Implementation
kind (`framework|router|library|platform|case-study`)、cohort、profile level、language/runtime、design trait、topic disposition (`included|adjacent|quarantined`) を定義する。repo renameや通称をstable idへ解決する。

## Acceptance
- [x] ReactはUI library、Vueはprogressive frameworkとして同一kindに強制しない。
- [x] Gin/httprouter、Vue/vue-router、Hono/router implementationを別entityで結べる。
- [x] duplicate alias/cyclic aliasを拒否。
- [x] quarantine reason codeが必須。
- [x] category追加はschema versionを壊さずreview可能。

## Non-goals
品質ranking、自動昇格。
