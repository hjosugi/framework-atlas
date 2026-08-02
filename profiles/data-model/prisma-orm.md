# Prisma ORM

- ID: `prisma-orm`
- 分野: `data-model` / `schema-first typed ORM`
- 言語: TypeScript, JavaScript
- 最初の公開: 2020
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

専用 schema から type-safe client と migration を生成し、TypeScript application と relational/document database の contract を揃える ORM。

## 何を解決するか

JavaScript ORM の runtime magic と弱い型、manual model duplication を減らし、schema と generated client を single source にする。

## 歴史・背景

Graphcool/Prisma 1 の data platform から、Prisma 2 以降は generated client、schema、migration を中心とする TypeScript ORM へ再設計された。

## 中核設計

schema.prisma を解析して query client と types を生成する。relation/query API は object graph と selection shape を型に反映する。

## Data model

schema-first。DB introspection と migration の両方向を支援し、domain object より generated data client を中心にする。

## メリット

- 優れた TypeScript 型推論
- schema/migration/client の統合
- developer tooling

## デメリット / trade-off

- 専用 schema と code generation
- 複雑 SQL/DB feature で raw query が必要
- runtime/engine/deployment compatibility を考慮

## 向いている用途

- TypeScript SaaS/API
- schema-driven team
- Next/Nest/Node ecosystem

## 避ける条件

- SQL-first heavy analytics
- code generation を置けない
- unsupported DB-specific feature が中心

## 実行モデル

- primary abstraction: Prisma schema と generated Client
- control flow: typed query object → query engine/driver → DB
- routing: 追加調査中
- rendering: 追加調査中
- dependency injection: application lifecycle managed client
- state: stateless data client; transaction scope
- concurrency: connection pool/transaction API
- deployment: Node/serverless/edge compatibility varies by adapter
- extension: generator、extension
- testing: test DB/migration
- migration cost: 高。schema/client API に結合

## Official / primary sources

- [Prisma ORM docs](https://www.prisma.io/docs/orm)
- [Prisma repository](https://github.com/prisma/prisma)

## Research gaps

- なし
