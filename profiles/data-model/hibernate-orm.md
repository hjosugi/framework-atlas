# Hibernate ORM

- ID: `hibernate-orm`
- 分野: `data-model` / `Data Mapper ORM / JPA implementation`
- 言語: Java, Kotlin
- 最初の公開: 2001
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Java object graph と relational database を mapping し、unit of work、lazy loading、query language、cache、transaction integration を提供する ORM。

## 何を解決するか

enterprise Java で JDBC boilerplate と object-relational impedance mismatch を減らし、domain object graph と transaction を扱う。

## 歴史・背景

JPA より前から Java ORM を牽引し、後に Jakarta Persistence specification の主要実装となった。Spring/Jakarta/Quarkus ecosystem の data layer に大きな影響を持つ。

## 中核設計

Session/EntityManager が persistence context と identity map/unit of work を管理する。mapping metadata と dirty checking で SQL を生成する。

## Data model

entity、value type、association、inheritance を object graph として表現。transaction boundary と fetch strategy が performance/correctness の中心。

## メリット

- 複雑な relational mapping と成熟した機能
- JPA ecosystem と integration
- transaction/unit-of-work

## デメリット / trade-off

- lazy loading、N+1、cache、flush の複雑さ
- 生成 SQL が見えにくい
- domain と persistence lifecycle の結合

## 向いている用途

- Java/Kotlin の transactional business system
- 複雑 relation と long-lived schema
- JPA standard が必要

## 避ける条件

- SQL を完全管理する high-performance path
- simple key-value/data pipeline
- event sourcing only

## 実行モデル

- primary abstraction: EntityManager/Session と Entity
- control flow: unit of work → dirty checking → SQL flush
- routing: 追加調査中
- rendering: 追加調査中
- dependency injection: framework integration
- state: managed/detached entity lifecycle
- concurrency: transaction + connection pool; Session non-thread-safe
- deployment: JVM
- extension: type、dialect、event listener
- testing: integration test with DB
- migration cost: 高。mapping/lifecycle/query language に依存

## Official / primary sources

- [Hibernate ORM official](https://hibernate.org/orm/)
- [Hibernate ORM repository](https://github.com/hibernate/hibernate-orm)

## Research gaps

- なし
