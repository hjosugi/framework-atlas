# Next.js

- ID: `next-js`
- 分野: `meta-framework` / `React full-stack framework`
- 言語: JavaScript, TypeScript
- 最初の公開: 2016
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

React に file-based routing、server rendering、static generation、server functions、bundling、deployment conventions を加える full-stack meta-framework。

## 何を解決するか

React 単体で未決定の routing、data fetching、SSR、code splitting、build、cache、deployment を一つの production path に統合する。

## 歴史・背景

2016 年に Zeit（現 Vercel）が公開。pages router から app router、React Server Components、streaming、nested layout へ進み、React の server-first application architecture を先導した。

## 中核設計

route segment が UI と server boundary を構成する。server/client component、cache、revalidation、middleware、route handler を build system と統合する。

## Data model

ORM を内蔵せず、server component/action から DB や API を呼ぶ。cache と request lifecycle が data access architecture に強く影響する。

## メリット

- React の production 機能を一式統合
- SSR/SSG/streaming と hosting ecosystem
- 大きな community と tooling

## デメリット / trade-off

- rendering/cache model の変更が速く複雑
- Vercel 最適化と他 platform 差を意識
- framework upgrade の影響範囲が広い

## 向いている用途

- React の full-stack Web
- SEO/content と対話 UI の混在
- server component を活用する SaaS

## 避ける条件

- client-only SPA で十分
- framework-specific server runtime を避けたい
- 長期固定 API を最優先

## 実行モデル

- primary abstraction: Route segment と React component
- control flow: request → route tree → server/client rendering
- routing: file-system App/Pages Router
- rendering: SSR、RSC、streaming、SSG、CSR
- dependency injection: module composition と React context
- state: server data/cache + client state
- concurrency: React concurrent/server rendering
- deployment: Node、container、serverless、edge、static export
- extension: plugin は限定的。compiler/bundler/config integration
- testing: React test stack + E2E
- migration cost: 高め。router と rendering convention に強く依存

## Official / primary sources

- [Next.js official](https://nextjs.org/)
- [Next.js repository](https://github.com/vercel/next.js)

## Research gaps

- なし
