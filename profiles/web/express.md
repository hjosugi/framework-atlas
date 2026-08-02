# Express

- ID: `express`
- 分野: `backend-web` / `minimal Node.js web framework`
- 言語: JavaScript, TypeScript
- 最初の公開: 2010
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Node.js の HTTP server に routing と middleware pipeline を加える小さく非規約的な Web framework。

## 何を解決するか

Node の低レベル HTTP API を、request/response helper と再利用可能 middleware で扱いやすくする。

## 歴史・背景

Node.js 初期から普及し、Connect middleware model と Sinatra 風の簡潔な routing を標準化した。Koa、Fastify、NestJS adapters、数多くの Node framework に API と middleware culture の影響を与えた。

## 中核設計

app.use で middleware chain を組み、route handler が request/response を直接扱う。core は小さく、選択を ecosystem に委ねる。

## Data model

内蔵 model/ORM はない。Prisma、Sequelize、TypeORM、Mongoose などを選ぶ。

## メリット

- 理解しやすく ecosystem が最大級
- 低い導入コストと自由度
- middleware 再利用

## デメリット / trade-off

- architecture と error handling をチームで決める必要
- 型安全は追加設計が必要
- 古い middleware の品質差

## 向いている用途

- 小〜中規模 API
- 既存 Node middleware を使う
- framework 自由度を優先

## 避ける条件

- 強い module/DI 規約が必要
- 極限 performance と schema-first が必要
- edge multi-runtime を同一コードで求める

## 実行モデル

- primary abstraction: Application、Router、Middleware
- control flow: ordered middleware chain
- routing: method/path router
- rendering: JSON、template engine optional
- dependency injection: core なし
- state: request-local と外部 store
- concurrency: Node event loop
- deployment: Node server、container、serverless adapter
- extension: middleware package
- testing: supertest 等
- migration cost: 低〜中。標準 Node API に近いが middleware に依存

## Official / primary sources

- [Express official](https://expressjs.com/)
- [Express repository](https://github.com/expressjs/express)

## Research gaps

- なし
