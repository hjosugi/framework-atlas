# Data model、transaction、DDD

## 4つのmodelを分ける

| Model | 責任 | 典型例 |
|---|---|---|
| Transport | HTTP入力・出力、validation | Java record、Pydantic model、Go struct |
| Application command/query | use caseの意図 | `CreateItemCommand` |
| Domain | invariant、behavior、identity | Aggregate、Value Object |
| Persistence | table/document mapping | JPA entity、SQLAlchemy model、GORM model |

小規模CRUDでは一つの型を兼用できます。しかし外部contract、business rule、schema lifecycleが独立して変化するなら分離した方が安全です。

## Spring Boot

Spring Data JPA/JDBC/R2DBC/MongoDB等を自動構成できます。repository abstraction、transaction manager、connection pool、migration toolをecosystemとして統合しやすい一方、Boot自体はORMではありません。

DDDでJPAを使う場合は、lazy loading、proxy、no-arg constructor、entity equality、aggregate外のcascadeに注意します。repositoryはaggregate root単位にし、transaction内でinvariantを成立させます。read sideはprojection/raw SQLを使い、write modelを無理に再利用しない選択もできます。

## FastAPI

Pydantic modelはtransport schemaです。validationとserializationに優れますが、identity map、dirty tracking、transactionは提供しません。SQLAlchemy/SQLModel等のsessionを`yield` dependencyでrequest scopeに置き、application serviceがcommit/rollback方針を持つ構成が一般的です。

ORM objectをそのままresponseにするとlazy load、N+1、secret field漏洩が起きやすいため、明示的response modelへ投影します。async endpointを選ぶだけではDB accessはasyncになりません。async driver/sessionまで揃えるか、sync処理をthread poolへ隔離します。

## Gin

binding用structはtransport modelです。`database/sql`、sqlc、GORM等を選び、constructorでrepository/serviceをhandlerへ渡します。transaction helperは`func(ctx context.Context, fn func(Tx) error) error`のような明示APIにすると、commit/rollbackとtest seamが読みやすくなります。

JSON tagとDB tagを同じstructへ積み上げる設計は小さいサービスでは合理的ですが、APIとschemaが別々に進化する段階で分離します。

## Modular Monolithへの適用

moduleごとにschemaまたはtable ownershipを決め、他moduleが直接更新しないようにします。単一databaseでもownershipは保てます。module間の強整合が本当に必要なら同期application API、独立性を優先するならOutbox eventを選びます。すべてを非同期にするのではなく、failure semanticsを基準に決めます。

CQRSは「command classを作ること」ではなく、read/writeのmodelと最適化軸を分ける判断です。simple CRUDへ導入する価値は低く、複雑なinvariant、read projection、監査要件がある境界で選択します。
