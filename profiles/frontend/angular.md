# Angular

- ID: `angular`
- 分野: `frontend-framework` / `full client application framework`
- 言語: TypeScript
- 最初の公開: 2016
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

component、template、routing、forms、HTTP、DI、build tooling を統合した TypeScript の full client application framework。

## 何を解決するか

大規模フロントエンドで architecture、dependency management、routing、forms、test/build の組織標準を一式提供する。

## 歴史・背景

AngularJS の後継として全面再設計され、TypeScript、component、RxJS、DI を中心に 2016 年に安定版が登場した。近年は standalone component、signals、より軽い build/runtime へ進化した。

## 中核設計

compiler が template と metadata を解析し、DI container、router、forms、change detection を統合する。選択肢を減らし大規模チームの一貫性を優先する。

## Data model

domain model は TypeScript class/interface。UI state は signals/RxJS、form model、service に分散し、永続化は API 側に置く。

## メリット

- 公式機能が広く統一される
- 型、DI、tooling が企業開発に向く
- 長期的な移行 tooling と規約

## デメリット / trade-off

- 概念と API の学習量が多い
- 小規模ページには過剰
- framework lifecycle と compiler への結合が強い

## 向いている用途

- 大規模業務 SPA
- 多数チームで規約を統一
- TypeScript/DI/RxJS を活用する製品

## 避ける条件

- 小さな widget
- 自由な library 組み合わせを優先
- 最小 bundle を最優先

## 実行モデル

- primary abstraction: Component、Directive、Service
- control flow: DI + change detection/signals
- routing: official Angular Router
- rendering: compiled template、SSR/hydration
- dependency injection: hierarchical DI container
- state: signals、RxJS、service/store
- concurrency: Zone/event loop、signals、RxJS
- deployment: SPA、SSR、static
- extension: library、schematics、builders
- testing: TestBed と browser/unit tooling
- migration cost: 高。Angular-specific architecture に深く結合

## Official / primary sources

- [Angular official](https://angular.dev/)
- [Angular repository](https://github.com/angular/angular)

## Research gaps

- なし
