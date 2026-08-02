# Hono

- ID: `hono`
- 分野: `backend-web` / `Web Standards multi-runtime framework`
- 言語: TypeScript, JavaScript
- 最初の公開: 2021
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Fetch API など Web Standards の Request/Response を中核に、edge、Deno、Bun、Node、WASI へ同一 API を展開する軽量 Web framework。

## 何を解決するか

runtime ごとに異なる server API と adapter を減らし、edge から Node まで portable な TypeScript HTTP application を作る。

## 歴史・背景

Cloudflare Workers 周辺から成長し、Express に近い小さな API と Web Standards portability を組み合わせた。edge runtime の多様化に対する「標準 API を共通基盤にする」世代を代表する。

## 中核設計

Request/Response/Headers など Web Standard object を直接使い、router と middleware を小さく保つ。型付き RPC/client、validator、JSX renderer などを追加可能。

## Data model

内蔵 ORM はない。runtime 対応 DB client、Drizzle、Prisma 等を選ぶ。schema validator と typed routes が API data contract を担う。

## メリット

- multi-runtime portability
- 小型・高速で Web API に近い
- TypeScript type inference と edge 対応

## デメリット / trade-off

- runtime 間で利用可能 API/DB driver が異なる
- full-stack 規約は別選択
- Node 固有 middleware をそのまま使えない場合

## 向いている用途

- edge API、BFF、proxy
- Cloudflare/Deno/Bun/Node をまたぐ library
- 小さな typed service

## 避ける条件

- 巨大な batteries-included backend
- Express middleware 互換が絶対条件
- 重い ORM/DI を core に求める

## 実行モデル

- primary abstraction: Hono app、Context、Web Request/Response
- control flow: router → middleware chain → handler
- routing: RegExpRouter/SmartRouter 等
- rendering: JSON/text/HTML/JSX optional
- dependency injection: context variables と middleware composition
- state: request context + external store
- concurrency: runtime event loop
- deployment: edge、Deno、Bun、Node、WASI
- extension: middleware、helper、adapter
- testing: app.request による in-process test
- migration cost: 低〜中。Web Standards に近い

## Official / primary sources

- [Hono official](https://hono.dev/)
- [Hono Web Standards concept](https://hono.dev/docs/concepts/web-standard)
- [Hono repository](https://github.com/honojs/hono)

## Research gaps

- なし
