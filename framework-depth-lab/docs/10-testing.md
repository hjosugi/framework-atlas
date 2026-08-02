# Testing strategy

## test portfolio

| Layer | 目的 | 避けること |
|---|---|---|
| Domain unit | invariantとevent | framework/DB起動 |
| Handler/service | use case、transaction decision | HTTP詳細 |
| HTTP slice | routing、validation、auth、error contract | 全外部system |
| Integration | real DB/broker adapter | owned dependencyの過剰mock |
| Contract | OpenAPIとconsumer互換 | implementation detail |
| System | module間eventual consistency | 固定sleepのみ |
| Architecture | dependency/visibility rule | 人のreviewだけに依存 |

## Spring Boot

plain JUnitでdomainをtestし、`@WebMvcTest`/`WebTestClient`でHTTP slice、`@DataJpaTest`やTestcontainersでdata integration、`@SpringBootTest`は統合が必要な範囲に限定します。ApplicationContext cacheを壊すannotation乱用はsuiteを遅くします。architecture ruleはArchUnit、migrationは実databaseで検証します。

## FastAPI

dependency overrideでauth/repository seamを差し替え、Starlette/FastAPIのTestClientまたはHTTPX ASGI transportでHTTP contractをtestします。async testではevent loop/backendを揃えます。Pydantic validationの422構造、response filtering、dependency cleanup、exception handlerもcontractとして固定します。

## Gin

`httptest.NewRecorder`と`http.NewRequest`でrouter/handlerを標準libraryだけでtestできます。service interfaceを小さくしfakeをconstructor injectionします。race detector、fuzz test、benchmarkを標準toolchainに組み込み、middleware orderingとabort behaviorを明示的にtestします。

## ケーススタディから学ぶ点

公開domain APIだけでaggregateを準備する方針、SUT factory、architecture tests、実DB integration、polling probeによるeventual consistency test、mutation testingは価値があります。ただしpoller実装は`Thread.Sleep`と未await taskを避け、async delay・cancellation・deadline・観測可能なlast stateを使うべきです。

system testは「eventがいつ届くか」ではなく、最終observable stateとtimeoutを検証します。Outbox/Inboxならduplicate、順序逆転、consumer restart、poison messageもtest matrixへ含めます。
