# 歴史と影響関係

## 読み方

「影響」は曖昧な語です。本章と `data/influence-edges.csv` では、次のedgeを混ぜません。

| 種別 | 意味 | 証拠の例 |
|---|---|---|
| `direct-dependency` | 実行時またはbuild時に直接依存する | manifest、source import |
| `official-inspiration` | 作者・公式文書が着想元と明記する | official docs |
| `derived-code` | codeまたはalgorithmの派生をlicense headerが示す | source header |
| `ecosystem-foundation` | 標準・runtime・hostとして下支えする | specification、official docs |
| `inferred-similarity` | 構造が似るが、直接影響は確認できない | 比較分析のみ |

## Spring Boot

Spring Bootは2013年にprototypeが公開され、1.0 GAは2014年4月でした。Spring Framework、Servlet container、build tool、Actuatorなどを「意見のあるdefault」で束ね、XML中心だったSpring設定からannotation・classpath・configuration property中心へ重心を移しました。

重要なのはSpring Frameworkの代替ではないことです。Bootは`ApplicationContext`、dependency injection、MVC/WebFlux、transaction abstractionをSpringから受け取り、起動・条件付き自動構成・dependency management・production diagnosticsを足します。4.0でmodule分割、JSpecify、API versioning、Java 25対応が進み、4.1はgRPCやobservability/securityの統合を広げました。

Spring Bootに「影響されたframework」を単純列挙するのは危険です。NestJSなどにannotation/DI/moduleの類似はありますが、公式な影響表明がないものは本資料では`inferred-similarity`に留めます。一方、Spring Initializr、Spring Cloud、Spring ModulithはBoot ecosystem上に直接成立します。

## FastAPI

FastAPIは複数の先行projectから、作者が良いと考えた性質を意識的に統合しています。

- Starlette: ASGI routing、middleware、request/response、WebSocket。FastAPIは`Starlette`を継承する。
- Pydantic: Python type hintからvalidation、serialization、JSON Schemaを生成する。
- Uvicorn: ASGI server。FastAPIそのものとserverを分離する。
- Django REST Framework: API schema、authentication、serializationを一体として扱うdeveloper experience。
- Flask: 小さいroute decoratorと直感的なrequest handling。
- Requests: 人が読みやすいAPI設計思想。
- Swagger/OpenAPI: interactive docsとcontract。
- Marshmallow、webargs、APISpec、flask-apispec: schema/validation/docs連携。
- NestJS/Angular: dependency injectionの宣言的構造。
- Sanic、Falcon、Molten、Hug、APIStar: performance、type annotation、schema generationに関する先行試行。

FastAPIの大きな貢献は個々の機能の発明というより、Pythonの標準type hintを中心に、これらの機能を重複宣言なしで繋いだことです。SQLModel、Typerなどは同じ作者・設計思想を共有しますが、FastAPI coreの一部ではありません。

## Gin

Ginのofficial taglineはMartini-like APIと高いperformanceの両立です。API ergonomicsはMartiniを参照しつつ、reflection中心のhandler injectionを避け、`net/http`互換の`Engine`、radix tree、`Context`、明示的middleware chainに絞りました。

routerの`tree.go`は`julienschmidt/httprouter`から派生したことをsource headerが明示しています。これは単なる「似ている」ではなく`derived-code`です。Go標準library、`httprouter`、validator/JSON codecなどを薄く統合する一方、DI containerやORMはcoreへ持ち込みません。

Echo、Fiber、Chiなど同時代/後発Go web frameworkとの機能比較はできますが、Ginからの直接影響を公式資料なしに断定しません。

## 3者が共有する大きな潮流

1. conventionで反復設定を減らす。ただしBootは広いplatform、FastAPIはtype/schema、GinはHTTP hot pathに適用する。
2. middleware/filter/decoratorで横断関心をhandler本体から分離する。
3. open standardへ接続する。Servlet/Reactive Streams、ASGI/OpenAPI/JSON Schema、`net/http`/HTTP。
4. escape hatchを残す。Spring Beanの明示定義、Starlette primitive、Go標準`http.Handler`へ降りられる。

## 誤読しやすい点

- 同じdecorator/annotation syntaxでもlifecycleとruntime costは違う。
- 「zero allocation router」はHTTP application全体がzero allocationという意味ではない。
- FastAPIのPydantic modelとDDD Value Objectは目的が違う。
- Springのmodule/Bean構成とbounded contextは同義ではない。
