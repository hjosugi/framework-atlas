# Axum

- ID: `axum`
- 分野: `backend-web` / `Tokio ecosystem web framework`
- 言語: Rust
- 最初の公開: 2021
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Tokio、Tower、Hyper の型と middleware ecosystem を直接活用する ergonomic な Rust Web framework。

## 何を解決するか

Rust async network stack の強力な component を、macro や独自 service abstraction を増やしすぎず、handler/extractor として使いやすくする。

## 歴史・背景

Tokio project 内で Hyper/Tower ecosystem の application-facing layer として登場。Rust Web の composable service model を広く普及させた。

## 中核設計

Router、Handler、Extractor と Tower Service/Layer を組み合わせる。既存 Tower middleware がそのまま利用できることを重視する。

## Data model

内蔵 ORM なし。Serde、SQLx、SeaORM、Diesel 等を state/extractor で統合する。

## メリット

- Tokio/Tower との自然な統合
- 型安全で比較的明快
- middleware composition

## デメリット / trade-off

- Rust async/trait の基礎が必要
- full-stack 機能は別 package
- version compatibility を ecosystem 全体で見る必要

## 向いている用途

- modern Rust API
- Tower middleware を使う service
- gRPC/HTTP stack を共有

## 避ける条件

- batteries-included admin/ORM が必要
- Rust 学習コストを取れない
- runtime dynamic framework が必要

## 実行モデル

- primary abstraction: Router、Handler、Extractor
- control flow: Tower Service/Layer
- routing: typed route tree
- rendering: typed response + Serde
- dependency injection: State extractor
- state: shared state + external DB
- concurrency: Tokio async runtime
- deployment: single binary/container
- extension: Tower Layer
- testing: tower ServiceExt/in-process
- migration cost: 低〜中。Tower/HTTP standard types に近い

## Official / primary sources

- [Axum repository](https://github.com/tokio-rs/axum)
- [Axum API docs](https://docs.rs/axum/)

## Research gaps

- なし
