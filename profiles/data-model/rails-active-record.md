# Rails Active Record

- ID: `rails-active-record`
- 分野: `data-model` / `Active Record ORM`
- 言語: Ruby
- 最初の公開: 2004
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

database table と Ruby class、row と object を対応させ、query、association、validation、callback、migration を統合する Rails の ORM。

## 何を解決するか

SQL と object model の往復、CRUD、relation、schema migration の反復 code を削減する。

## 歴史・背景

Martin Fowler が整理した Active Record pattern を Rails の中心に据え、Web framework と ORM の強い統合を普及させた。Eloquent など多数の後続 ORM に影響した。

## 中核設計

convention で table/primary key を推論し、model instance 自身が persistence operation を持つ。relation は lazy query object として compose される。

## Data model

rich domain model と persistence record が同一 class に置かれやすい。simple CRUD に強い一方、複雑 domain では service/value object への分離が重要。

## メリット

- 非常に速い CRUD 開発
- migration/association/validation の統合
- Rails 全体との一貫性

## デメリット / trade-off

- N+1、callback chain、fat model
- DB schema と domain の密結合
- 複雑 query/aggregate boundary で摩擦

## 向いている用途

- Rails の relational application
- CRUD と workflow
- convention に沿う schema

## 避ける条件

- event sourcing
- 複雑な domain aggregate を persistence から厳密分離
- SQL-first analytics

## 実行モデル

- primary abstraction: Model instance と Relation
- control flow: model API → query builder/adapter → DB
- routing: 追加調査中
- rendering: 追加調査中
- dependency injection: connection/configuration registry
- state: identity を持つ mutable record
- concurrency: DB transaction/connection pool
- deployment: Rails process
- extension: adapter、callback、scope
- testing: fixture/factory/database test
- migration cost: 高。model API と schema convention に結合

## Official / primary sources

- [Rails Active Record guide](https://guides.rubyonrails.org/active_record_basics.html)
- [Active Record source](https://github.com/rails/rails/tree/main/activerecord)

## Research gaps

- なし
