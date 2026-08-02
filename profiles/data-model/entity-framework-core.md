# Entity Framework Core

- ID: `entity-framework-core`
- 分野: `data-model` / `.NET Data Mapper ORM`
- 言語: C#, F#
- 最初の公開: 2016
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

.NET object model と relational/document providers を LINQ、change tracking、migration、unit of work で接続する ORM。

## 何を解決するか

ADO.NET boilerplate を減らし、strongly typed LINQ query と domain entity mapping を ASP.NET Core ecosystem に統合する。

## 歴史・背景

従来 Entity Framework を cross-platform .NET 向けに再設計。ASP.NET Core と同じ release train で進化し、LINQ-based data access の中心となった。

## 中核設計

DbContext が unit of work/identity map、DbSet が query root。LINQ expression tree を provider SQL に変換する。

## Data model

Data Mapper/Unit of Work。convention、annotation、Fluent API で mapping し、tracked/no-tracking query を選ぶ。

## メリット

- C# 型と LINQ の統合
- migration/change tracking/provider ecosystem
- ASP.NET Core との自然な DI

## デメリット / trade-off

- LINQ の provider translation 制約
- tracking/fetch performance の理解
- complex SQL で abstraction leak

## 向いている用途

- .NET transactional application
- LINQ-centric team
- ASP.NET Core service

## 避ける条件

- SQLを完全手書きする hot path
- non-.NET shared data layer
- event sourcing only

## 実行モデル

- primary abstraction: DbContext、DbSet、LINQ query
- control flow: expression tree → provider → DB; SaveChanges unit-of-work
- routing: 追加調査中
- rendering: 追加調査中
- dependency injection: ASP.NET Core scoped DbContext
- state: tracked entity lifecycle
- concurrency: DbContext non-thread-safe、transaction/connection pool
- deployment: .NET runtime
- extension: provider、interceptor、converter
- testing: SQLite/test DB/in-memory caveats
- migration cost: 高。LINQ/provider/DbContext に結合

## Official / primary sources

- [EF Core official docs](https://learn.microsoft.com/ef/core/)
- [EF Core repository](https://github.com/dotnet/efcore)

## Research gaps

- なし
