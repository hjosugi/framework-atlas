# ASP.NET Core

- ID: `asp-net-core`
- 分野: `backend-web` / `cross-platform web application framework`
- 言語: C#, F#
- 最初の公開: 2016
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

.NET の routing、middleware、DI、MVC、minimal API、Razor、Blazor、SignalR、auth を統合する cross-platform Web framework。

## 何を解決するか

旧 ASP.NET の Windows/IIS 結合を解き、high-performance、cross-platform、cloud/container 対応の統一 Web stack を作る。

## 歴史・背景

.NET Core とともに再設計され、OWIN/Katana の middleware 発想、MVC/Web API の統合、built-in DI を採用した。現在は minimal API から Blazor まで同一 platform に統合する。

## 中核設計

Host と middleware pipeline が基盤。endpoint routing の上に minimal API、MVC、Razor Pages、SignalR などが乗る。configuration、logging、DI が platform 共通。

## Data model

Entity Framework Core が標準的選択だが強制しない。model binding と validation が transport model を扱う。

## メリット

- 高性能で機能範囲が広い
- .NET tooling、型、安全性、長期 support
- API、SSR、real-time、auth の統合

## デメリット / trade-off

- platform 全体の API が大きい
- hosting/DI/middleware の理解が必要
- Microsoft ecosystem への結合

## 向いている用途

- 企業 .NET service
- high-throughput API
- Blazor/SignalR を含む full-stack

## 避ける条件

- 数行の非 .NET edge script
- runtime footprint を極小化
- 既存 team が別言語に統一

## 実行モデル

- primary abstraction: Host、Middleware、Endpoint
- control flow: middleware pipeline → endpoint
- routing: endpoint routing
- rendering: JSON、Razor、Blazor、SignalR
- dependency injection: built-in DI container
- state: scoped service + EF Core/cache/session
- concurrency: async/await、thread pool
- deployment: Kestrel、IIS reverse proxy、container、native AOT option
- extension: middleware、service registration、NuGet
- testing: TestServer/WebApplicationFactory
- migration cost: 中〜高。.NET hosting model に結合

## Official / primary sources

- [ASP.NET Core official docs](https://learn.microsoft.com/aspnet/core/)
- [ASP.NET Core repository](https://github.com/dotnet/aspnetcore)

## Research gaps

- なし
