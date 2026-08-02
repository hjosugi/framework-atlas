# Svelte

- ID: `svelte`
- 分野: `frontend-framework` / `compiler-first UI framework`
- 言語: JavaScript, TypeScript
- 最初の公開: 2016
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

component を build 時に命令的 DOM 更新コードへ変換し、runtime abstraction を小さくする compiler-first UI framework。

## 何を解決するか

Virtual DOM runtime と framework ceremony を減らし、HTML/CSS/JavaScript に近い記述から効率的な更新コードを生成する。

## 歴史・背景

Rich Harris が 2016 年に公開。Svelte 3 の reactive syntax で普及し、SvelteKit が full-stack layer を担う。Svelte 5 では runes により reactivity model を明示化した。

## 中核設計

compiler が component dependency を解析する。runtime reconciliation より compile-time transformation を重視し、scoped CSS と transition も component に統合する。

## Data model

UI state は component-level reactivity と stores/runes。永続化 model は SvelteKit の server/load/API に分離する。

## メリット

- 少ない boilerplate と直感的な component
- 小さな runtime と compiler 最適化
- animation と style の統合

## デメリット / trade-off

- compiler semantics を理解する必要
- React ecosystem ほど library 選択肢が多くない
- 大規模 architecture は SvelteKit/規約の設計が必要

## 向いている用途

- 高速な UI、content site、application
- 少人数で簡潔な component を好む
- SvelteKit full-stack

## 避ける条件

- React-specific ecosystem が必須
- runtime-only 配布が必要
- compiler toolchain を置けない

## 実行モデル

- primary abstraction: Compiled component
- control flow: compile-time dependency analysis → direct updates
- routing: SvelteKit が担当
- rendering: client、SSR、hydration
- dependency injection: context と module composition
- state: runes/store/local state
- concurrency: event loop + async rendering
- deployment: static、server、edge via SvelteKit adapters
- extension: preprocessor、compiler integration
- testing: Vitest、Testing Library、Playwright
- migration cost: 中。Svelte syntax/compiler に依存

## Official / primary sources

- [Svelte official](https://svelte.dev/)
- [Svelte repository](https://github.com/sveltejs/svelte)

## Research gaps

- なし
