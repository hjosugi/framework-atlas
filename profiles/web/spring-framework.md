# Spring Framework

- ID: `spring-framework`
- 分野: `backend-web` / `enterprise application framework`
- 言語: Java, Kotlin
- 最初の公開: 2004
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Java/Kotlin アプリケーションの構成、依存性注入、Web、データアクセス、トランザクション、テストを統合する基盤フレームワーク。

## 何を解決するか

初期 J2EE/EJB の重いコンテナ依存、テスト困難、設定量、インフラ API と業務コードの密結合を減らす。

## 歴史・背景

Rod Johnson の書籍と実装から始まり、軽量 IoC コンテナと POJO 中心設計を広めた。Servlet MVC だけでなく、データ、セキュリティ、統合、リアクティブ処理へ広がり、Java エンタープライズ開発の事実上の共通基盤になった。

## 中核設計

IoC/DI コンテナ、AOP、宣言的トランザクション、テンプレート/抽象化、アノテーションと Java 設定を組み合わせる。フレームワーク側がオブジェクトの生成とライフサイクルを管理する。

## Data model

特定 ORM を強制せず JDBC、JPA、Hibernate、R2DBC などを抽象化する。ドメインモデルと永続化境界を分けられるが、Spring Data を使うと Repository 抽象が中心になる。

## メリット

- 巨大で成熟したエコシステム
- DI・トランザクション・テスト支援が一貫
- 長期運用と企業統合に強い

## デメリット / trade-off

- 抽象化層が多く、実行時挙動が見えにくい
- 学習範囲と設定選択肢が大きい
- 小規模サービスには過剰になりやすい

## 向いている用途

- 長寿命の業務システム
- 複数データソースや認証基盤を統合するサービス
- 組織標準を揃えたい大規模チーム

## 避ける条件

- 極小バイナリや極短起動が最優先
- 依存性注入を使わない明示的構成を望む
- 一時的な単機能ツール

## 実行モデル

- primary abstraction: Bean と ApplicationContext
- control flow: コンテナが生成・配線・横断的処理を管理
- routing: アノテーションまたは関数型ルーター
- rendering: Spring MVC / WebFlux を選択
- dependency injection: 実行時 DI コンテナ
- state: 通常はステートレス Bean。状態は DB、キャッシュ、セッションへ分離
- concurrency: Servlet スレッドモデルと Reactor の両方
- deployment: WAR、実行可能 JAR、コンテナ、ネイティブイメージ連携
- extension: 多数の Spring Projects と Starter
- testing: TestContext、MockMvc、WebTestClient、スライステスト
- migration cost: 中〜高。大規模 API と慣習に依存しやすい

## Official / primary sources

- [Spring Framework official project](https://spring.io/projects/spring-framework)
- [Spring Framework repository](https://github.com/spring-projects/spring-framework)

## Research gaps

- なし
