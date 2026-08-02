# Spring Boot

- ID: `spring-boot`
- 分野: `backend-web` / `opinionated application framework`
- 言語: Java, Kotlin
- 最初の公開: 2014
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Spring アプリケーションを自動設定、Starter、組み込みサーバー、運用機能で素早く本番化するための意見を持った層。

## 何を解決するか

Spring の柔軟性が生む初期設定、依存関係選定、サーバー構築、監視・設定管理の反復作業を削減する。

## 歴史・背景

Spring Framework の上に「良い既定値」を置き、単体実行可能 JAR と自動設定を標準化した。マイクロサービス普及期に Java の新規サービス作成速度を大きく改善した。

## 中核設計

classpath と設定プロパティを条件に AutoConfiguration を適用し、Starter が互換性のある依存セットを提供する。Actuator が health、metrics、環境情報などを統合する。

## Data model

Spring Data JPA、JDBC、R2DBC、MongoDB などを Starter で接続する。データモデル自体は選択式だが、Repository と設定規約が統合点になる。

## メリット

- 起動可能な本番向けサービスを短時間で作れる
- 監視・外部設定・組み込みサーバーが標準化
- Spring 全体との互換性

## デメリット / trade-off

- 自動設定の条件を理解しないとデバッグが難しい
- 依存グラフと起動時処理が大きくなりやすい
- 既定値から外れると Spring 本体の知識が必要

## 向いている用途

- Java/Kotlin API と業務サービス
- 企業標準のマイクロサービス
- 監視・セキュリティ・DB を統合するアプリ

## 避ける条件

- 数 MB 以下やミリ秒起動を絶対条件とする処理
- 非常に単純な単一 HTTP ハンドラー
- Spring の抽象を避けたいチーム

## 実行モデル

- primary abstraction: Application と AutoConfiguration
- control flow: Spring コンテナ + 条件付き自動設定
- routing: Controller または RouterFunction
- rendering: Spring MVC / WebFlux
- dependency injection: Spring DI
- state: ステートレスサービス + 外部永続化
- concurrency: Servlet/virtual thread 選択肢、Reactor
- deployment: java -jar、OCI image、クラウド、native image
- extension: Starter と AutoConfiguration module
- testing: @SpringBootTest と slice tests
- migration cost: 中〜高。Spring ecosystem への結合が強い

## Official / primary sources

- [Spring Boot README](https://github.com/spring-projects/spring-boot/blob/main/README.adoc)
- [Spring Boot official project](https://spring.io/projects/spring-boot)

## Research gaps

- なし
