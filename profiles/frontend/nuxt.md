# Nuxt

- ID: `nuxt`
- 分野: `meta-framework` / `Vue full-stack framework`
- 言語: JavaScript, TypeScript
- 最初の公開: 2016
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Vue に routing、SSR/SSG、server endpoints、auto-import、modules、deployment adapters を統合する full-stack meta-framework。

## 何を解決するか

Vue application の routing、server rendering、build、data fetching、SEO、deployment の定型構成を標準化する。

## 歴史・背景

Vue ecosystem の universal application framework として 2016 年に登場。Nuxt 3 は Vue 3、Vite、Nitro を基盤に server/edge multi-runtime を強化した。

## 中核設計

file-based routing と convention、auto-import、composable、Nitro server を組み合わせる。module system が ecosystem integration の中心。

## Data model

ORM は選択式。useFetch/useAsyncData、server routes、Nitro storage/cache が server/client data flow を統合する。

## メリット

- Vue full-stack の一貫した標準
- module と deployment adapter が豊富
- SSR/SSG/hybrid rendering

## デメリット / trade-off

- auto-import と magic が依存を見えにくくする
- Nuxt lifecycle の学習が必要
- module quality に差がある

## 向いている用途

- Vue の SaaS、content、commerce
- SSR/SSG と API を一 repo に統合
- multi-runtime deployment

## 避ける条件

- 小さな埋め込み widget
- manual bundler/control を優先
- Vue 以外の UI が主

## 実行モデル

- primary abstraction: Page/layout/composable/module
- control flow: route → Nitro/server data → Vue render
- routing: file-system routing
- rendering: SSR、SSG、hybrid、CSR
- dependency injection: Nuxt plugin/provide と Vue inject
- state: useState、Pinia、server data
- concurrency: async data と server runtime
- deployment: Node、serverless、edge、static via Nitro presets
- extension: Nuxt Module
- testing: Nuxt test utils、Vitest、Playwright
- migration cost: 中〜高。Nuxt convention と Nitro に依存

## Official / primary sources

- [Nuxt official](https://nuxt.com/)
- [Nuxt repository](https://github.com/nuxt/nuxt)

## Research gaps

- なし
