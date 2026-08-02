# Actix Web

- ID: `actix-web`
- 分野: `backend-web` / `high-performance Rust web framework`
- 言語: Rust
- 最初の公開: 2017
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Rust の型、安全性、async runtime を使い、高性能 HTTP server、extractor、middleware、routing を提供する Web framework。

## 何を解決するか

低レベル network programming を直接書かず、Rust の zero-cost abstraction と type-safe handler で production Web service を作る。

## 歴史・背景

Actix actor ecosystem から生まれ、後に Web framework として独立性を高めた。Rust Web benchmark と production adoption の中心的選択肢になった。

## 中核設計

App、Service、Extractor、Responder trait を組み合わせる。compile-time type checking が request extraction と response conversion を支える。

## Data model

内蔵 ORM なし。Diesel、SQLx、SeaORM 等を application state に注入する。Serde が transport model を担う。

## メリット

- 高性能と memory safety
- 成熟した middleware/extractor
- 型で request contract を表現

## デメリット / trade-off

- trait/lifetime/error type の学習
- compile time が長くなり得る
- dynamic な変更には不向き

## 向いている用途

- 高 throughput API
- security/performance 重視 service
- Rust ecosystem の backend

## 避ける条件

- 短期 prototype で Rust 経験がない
- 動的 plugin loading が中心
- 大量の既存 JVM package が必須

## 実行モデル

- primary abstraction: App、Service、Extractor、Responder
- control flow: async service pipeline
- routing: resource/route DSL
- rendering: Serde/response types
- dependency injection: app data extraction
- state: Arc/shared state + external DB
- concurrency: async workers/runtime
- deployment: single binary/container
- extension: middleware/service trait
- testing: in-process test utilities
- migration cost: 中。Actix traits/extractors に依存

## Official / primary sources

- [Actix official](https://actix.rs/)
- [Actix Web repository](https://github.com/actix/actix-web)

## Research gaps

- なし
