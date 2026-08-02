# Quarkus

- ID: `quarkus`
- 分野: `backend-web` / `Kubernetes-native Java framework`
- 言語: Java, Kotlin
- 最初の公開: 2019
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

build-time processing と GraalVM native image 対応により、Java の起動時間・memory footprint を cloud/container 向けに最適化する framework。

## 何を解決するか

従来 JVM framework の起動時間と memory 使用量が、serverless、dense container、autoscaling で不利になる問題を減らす。

## 歴史・背景

Jakarta EE/MicroProfile と Vert.x ecosystem を再構成し、build-time augmentation を中核にした。Spring Boot 後の cloud-native Java framework 世代を代表する。

## 中核設計

extension が build step で metadata と wiring を生成し、runtime reflection を減らす。imperative と reactive API を併存させる。

## Data model

Hibernate ORM with Panache、Hibernate Reactive、JDBC clients 等。Active Record 風と Repository 風の両方を選べる。

## メリット

- 高速起動・低 memory
- Jakarta/MicroProfile と Kubernetes 統合
- developer mode と native build

## デメリット / trade-off

- build-time 制約と native image compatibility
- extension 外の library は追加設定が必要
- build complexity

## 向いている用途

- Kubernetes microservice
- serverless Java
- 既存 Jakarta skill の cloud migration

## 避ける条件

- 動的 reflection/plugin が中心
- native build toolchain を持てない
- 単純 monolith で起動性能が問題でない

## 実行モデル

- primary abstraction: Extension と CDI Bean
- control flow: build-time augmentation + CDI runtime
- routing: JAX-RS/reactive routes
- rendering: RESTEasy Reactive/Qute/JSON
- dependency injection: Arc CDI
- state: Panache/ORM + external state
- concurrency: imperative、virtual threads、reactive Vert.x
- deployment: JVM、native binary、container/Kubernetes
- extension: Quarkus Extension
- testing: QuarkusTest、Dev Services
- migration cost: 中〜高。extension/build-time model に依存

## Official / primary sources

- [Quarkus official](https://quarkus.io/)
- [Quarkus repository](https://github.com/quarkusio/quarkus)

## Research gaps

- なし
