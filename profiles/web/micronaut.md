# Micronaut

- ID: `micronaut`
- 分野: `backend-web` / `compile-time DI cloud framework`
- 言語: Java, Kotlin, Groovy
- 最初の公開: 2018
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

compile-time DI/AOP と cloud integration により、reflection を減らし高速起動・低 memory を狙う JVM application framework。

## 何を解決するか

Spring 型 DI framework の developer experience を保ちながら、runtime classpath scan、proxy、reflection の cost を削減する。

## 歴史・背景

Grails の経験を背景に設計され、annotation processor で dependency metadata を生成する方式を採用した。Quarkus と並ぶ cloud-native JVM 世代。

## 中核設計

compile-time DI、AOP、configuration metadata、HTTP client/server code を生成する。annotation model は Spring に近いが runtime model は異なる。

## Data model

Micronaut Data が compile-time query generation を行い、JPA/JDBC/R2DBC/MongoDB 等に接続する。

## メリット

- 高速起動と少ない reflection
- DI、HTTP client、cloud integration
- Java/Kotlin/Groovy 対応

## デメリット / trade-off

- annotation processing と generated code の理解
- Spring ecosystem 全互換ではない
- compile-time 制約

## 向いている用途

- serverless/JVM microservice
- compile-time safety を重視
- Spring-like API から軽量化

## 避ける条件

- 大量の runtime dynamic proxy が必要
- Spring-only integration が必須
- annotation processing を避ける

## 実行モデル

- primary abstraction: Compile-time BeanDefinition
- control flow: generated DI/AOP + HTTP pipeline
- routing: controller annotation
- rendering: JSON/view optional
- dependency injection: compile-time DI
- state: Micronaut Data + external state
- concurrency: Netty/reactive/virtual thread options
- deployment: JVM、native、serverless/container
- extension: module/annotation processor
- testing: test integration、embedded server
- migration cost: 中。annotation API と generated metadata に依存

## Official / primary sources

- [Micronaut official](https://micronaut.io/)
- [Micronaut core repository](https://github.com/micronaut-projects/micronaut-core)

## Research gaps

- なし
