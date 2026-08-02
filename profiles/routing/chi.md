# chi

- ID: `chi`
- 分野: `router` / `idiomatic composable HTTP router`
- 言語: Go
- 最初の公開: 2015
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Go の標準 net/http Handler interface を維持しながら、軽量で composable な routing と middleware を提供する router。

## 何を解決するか

framework 固有 Context に閉じず、標準 library と互換なまま route grouping、URL parameter、middleware composition を使う。

## 歴史・背景

Go の「小さな interface と composition」を前面に出し、full framework より標準 HTTP との互換性を選ぶ流れを代表する。

## 中核設計

Router 自体が http.Handler。subrouter と middleware stack を組み合わせ、request.Context に route data を載せる。

## Data model

一切規定しない。database/sql、Ent、GORM、sqlc などを application layer で選ぶ。

## メリット

- net/http 互換で lock-in が小さい
- 小さく composable
- middleware と test が標準 API のまま

## デメリット / trade-off

- binding、validation、DI、ORM は自前選択
- 大規模 architecture の規約を提供しない
- 便利 helper は Gin 等より少ない

## 向いている用途

- 標準 Go を重視する API
- library と server を同じ Handler で組む
- 長期保守で framework 依存を抑える

## 避ける条件

- batteries-included を求める初心者チーム
- 自動 validation/serialization を core に求める
- full-stack template system が必要

## 実行モデル

- primary abstraction: http.Handler と Router
- control flow: standard middleware chain
- routing: composable tree router
- rendering: 標準 ResponseWriter
- dependency injection: なし
- state: request.Context + external state
- concurrency: net/http
- deployment: single binary/container
- extension: standard middleware
- testing: httptest
- migration cost: 低。標準 interface を維持

## Official / primary sources

- [chi repository](https://github.com/go-chi/chi)
- [chi official](https://go-chi.io/)

## Research gaps

- なし
