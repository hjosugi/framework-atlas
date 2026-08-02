# NestJS

- ID: `nestjs`
- 分野: `backend-web` / `opinionated Node.js application framework`
- 言語: TypeScript
- 最初の公開: 2017
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Angular に似た module、decorator、DI を Node.js server development に適用する TypeScript framework。Express/Fastify を transport layer として利用できる。

## 何を解決するか

大規模 Node backend で controller、service、module、validation、testing、microservice transport の構造を統一する。

## 歴史・背景

Angular の architecture と TypeScript decorator culture を server side に持ち込み、Node ecosystem の自由度と enterprise-style structure を橋渡しした。

## 中核設計

Module graph と DI container が中心。decorator metadata から controller、guard、pipe、interceptor を構成し、platform adapter が Express/Fastify を抽象化する。

## Data model

ORM は TypeORM、Prisma、Mongoose など選択式。DTO、class-validator、pipe が API data contract を構成する。

## メリット

- 大規模 TypeScript team の構造統一
- DI、OpenAPI、GraphQL、microservices 統合
- testability と module boundary

## デメリット / trade-off

- decorator と reflection による magic
- 小規模 API には boilerplate
- platform abstraction の下層理解も必要

## 向いている用途

- 大規模 Node backend
- Angular 経験チーム
- REST/GraphQL/message transport 混在

## 避ける条件

- 極小 function
- decorator/reflection を避ける
- Web Standards のみで multi-runtime を狙う

## 実行モデル

- primary abstraction: Module、Controller、Provider
- control flow: DI graph + decorator pipeline
- routing: decorator controller
- rendering: API response、template optional
- dependency injection: runtime hierarchical DI
- state: provider scope + external DB/cache
- concurrency: Node event loop / worker integration
- deployment: Node、container、serverless
- extension: dynamic module、adapter、custom decorator
- testing: official testing module、Jest ecosystem
- migration cost: 高め。Nest module/decorator model に結合

## Official / primary sources

- [NestJS official](https://nestjs.com/)
- [NestJS repository](https://github.com/nestjs/nest)

## Research gaps

- なし
