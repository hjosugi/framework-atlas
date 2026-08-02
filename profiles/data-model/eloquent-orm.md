# Eloquent ORM

- ID: `eloquent-orm`
- 分野: `data-model` / `Active Record ORM`
- 言語: PHP
- 最初の公開: 2011
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Laravel の Active Record ORM。relation、query scope、cast、event、factory、resource serialization を表現力の高い PHP API に統合する。

## 何を解決するか

PHP application の SQL/CRUD/relation boilerplate を減らし、Laravel conventions と一体化した data model を提供する。

## 歴史・背景

Rails Active Record の影響を受けた Laravel の中心機能として発展。Laravel ecosystem の auth、queue、notification、API resource と model を結び付ける。

## 中核設計

Model instance が persistence behavior を持ち、Builder が fluent query を compose。magic property と relation method で object graph を表す。

## Data model

database record と domain behavior が近い Active Record。cast、accessor、observer に責務が集まりやすい。

## メリット

- 読みやすい CRUD/relation API
- Laravel integration
- factory、resource、pagination が豊富

## デメリット / trade-off

- magic property と hidden query
- N+1/callback/model obesity
- domain separation が弱くなりやすい

## 向いている用途

- Laravel CRUD/SaaS
- relational business app
- rapid development

## 避ける条件

- 複雑 DDD aggregate
- SQL-first analytics
- Laravel 外で軽量 data mapper が必要

## 実行モデル

- primary abstraction: Model と Builder
- control flow: fluent query/model event → DB
- routing: 追加調査中
- rendering: 追加調査中
- dependency injection: Laravel connection manager
- state: mutable record
- concurrency: request/transaction model
- deployment: Laravel/PHP runtime
- extension: scope、cast、observer、macro
- testing: factory/database assertions
- migration cost: 高。Eloquent API に結合

## Official / primary sources

- [Eloquent official docs](https://laravel.com/docs/eloquent)
- [Eloquent source](https://github.com/laravel/framework/tree/13.x/src/Illuminate/Database/Eloquent)

## Research gaps

- なし
