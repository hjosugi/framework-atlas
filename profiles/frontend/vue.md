# Vue

- ID: `vue`
- 分野: `frontend-framework` / `progressive UI framework`
- 言語: JavaScript, TypeScript
- 最初の公開: 2014
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

標準 HTML/CSS/JavaScript に近い template、reactivity、component を持ち、library から full framework まで段階的に採用できる UI framework。

## 何を解決するか

AngularJS の統合性と React の component 指向の間で、導入しやすく、反応性を明示しやすい UI 開発体験を提供する。

## 歴史・背景

Evan You が 2014 年に公開。Vue 2 は Virtual DOM ecosystem を確立し、Vue 3 は Proxy-based reactivity、Composition API、compiler optimization を導入した。Nuxt、Vue Router、Pinia、VitePress が公式に近い一貫した ecosystem を形成する。

## 中核設計

Single-File Component、template compiler、fine-grained dependency tracking、Composition API を組み合わせる。Options API も維持し、段階的移行を支える。

## Data model

永続化 model は持たない。ref/reactive と computed が UI state graph を作り、Pinia や server-state library に拡張する。

## メリット

- 学びやすい template と良質な文書
- 段階的導入と full-stack への拡張性
- compiler と runtime reactivity のバランス

## デメリット / trade-off

- Options/Composition の二つの流儀が混在し得る
- React より ecosystem 規模が小さい領域がある
- reactivity の unwrap 規則に学習が必要

## 向いている用途

- 中小〜大規模 Web UI
- 既存 server-rendered page への段階導入
- Nuxt を使う full-stack/SSR

## 避ける条件

- native UI を同一 core で求める
- JSX のみを組織標準にする
- 極端に小さい dependency budget

## 実行モデル

- primary abstraction: Single-File Component と reactive state
- control flow: dependency tracking → targeted update
- routing: Vue Router
- rendering: client、SSR、hydration
- dependency injection: provide/inject と plugin
- state: ref/reactive、Pinia
- concurrency: browser event loop + async component
- deployment: SPA、SSR/SSG via Nuxt、static
- extension: plugin、directive、compiler macro
- testing: Vitest、Vue Test Utils
- migration cost: 中。SFC と Vue-specific template に結合

## Official / primary sources

- [Vue official](https://vuejs.org/)
- [Vue core repository](https://github.com/vuejs/core)

## Research gaps

- なし
