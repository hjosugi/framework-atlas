# SQLAlchemy

- ID: `sqlalchemy`
- 分野: `data-model` / `SQL toolkit and ORM`
- 言語: Python
- 最初の公開: 2006
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

SQL expression language と Data Mapper ORM を分離しつつ統合し、Python から relational database を明示的かつ柔軟に扱う toolkit。

## 何を解決するか

単純 Active Record では表しにくい SQL と domain mapping を、SQL の能力を失わず object model と unit of work に接続する。

## 歴史・背景

2006 年から Python data access の中核となり、Core と ORM の二層設計、explicit session、unit of work を普及させた。FastAPI/Flask ecosystem でも標準的選択。

## 中核設計

Core の SQL AST/engine/connection の上に ORM mapper/session を置く。declarative mapping と explicit query の両方を提供する。

## Data model

Data Mapper。domain class と table mapping を分けられ、Session が identity map と unit of work を管理する。

## メリット

- SQL の表現力と ORM の両立
- 複雑 schema/query に強い
- sync/async と広い DB 対応

## デメリット / trade-off

- 概念と API が大きい
- session/transaction/fetch strategy の理解が必要
- 簡単 CRUD には冗長

## 向いている用途

- Python の本格 relational system
- 複雑 query/schema
- framework-independent data layer

## 避ける条件

- 非常に単純な script
- document DB only
- ORM lifecycle を避けたい SQL-only app

## 実行モデル

- primary abstraction: Engine、Connection、Session、Mapper
- control flow: SQL expression/unit of work → dialect → DB
- routing: 追加調査中
- rendering: 追加調査中
- dependency injection: application-managed session
- state: transient/persistent/detached object lifecycle
- concurrency: session per unit-of-work; async session option
- deployment: Python runtime
- extension: dialect、type、event
- testing: transactional integration tests
- migration cost: 中〜高。Core は比較的 portable、ORM lifecycle は結合

## Official / primary sources

- [SQLAlchemy official](https://www.sqlalchemy.org/)
- [SQLAlchemy repository](https://github.com/sqlalchemy/sqlalchemy)

## Research gaps

- なし
