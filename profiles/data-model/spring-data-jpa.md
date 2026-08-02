# Spring Data JPA

- ID: `spring-data-jpa`
- 分野: `data-model` / `repository abstraction for JPA`
- 言語: Java, Kotlin
- 最初の公開: 2011
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

JPA EntityManager の上に Repository interface、query derivation、pagination、auditing、specification を追加する Spring data access framework。

## 何を解決するか

aggregate ごとに繰り返す DAO CRUD と query implementation を減らし、Spring application の data access 規約を揃える。

## 歴史・背景

Spring Data umbrella の一部として repository abstraction を普及させ、method name から query を導出する開発体験を Java enterprise の標準にした。

## 中核設計

Repository interface を runtime proxy で実装し、method signature/name、annotation、Specification から query を構築する。

## Data model

JPA entity model を前提とする。aggregate root ごとに Repository を置きやすいが、entity-centric CRUD に偏る可能性がある。

## メリット

- boilerplate が非常に少ない
- pagination/auditing/specification 統合
- Spring Boot との強い統合

## デメリット / trade-off

- query derivation が複雑化すると読みにくい
- JPA lifecycle の問題は隠せない
- Repository の過剰な汎用化

## 向いている用途

- Spring + JPA business service
- 標準 CRUD/query
- Repository pattern を組織標準化

## 避ける条件

- SQL-first complex reporting
- JPA を使わない
- event sourcing

## 実行モデル

- primary abstraction: Repository interface
- control flow: proxy → query derivation/JPA
- routing: 追加調査中
- rendering: 追加調査中
- dependency injection: Spring container
- state: JPA persistence context
- concurrency: transaction-bound EntityManager
- deployment: Spring application
- extension: custom repository fragment/specification
- testing: DataJpaTest
- migration cost: 高。Spring Data/JPA に結合

## Official / primary sources

- [Spring Data JPA official](https://spring.io/projects/spring-data-jpa)
- [Spring Data JPA repository](https://github.com/spring-projects/spring-data-jpa)

## Research gaps

- なし
