# Gin

- ID: `gin`
- 分野: `backend-web` / `high-performance HTTP framework`
- 言語: Go
- 最初の公開: 2014
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Go の net/http ecosystem 上で高速 router、middleware、binding/validation、rendering を提供する小さな Web framework。

## 何を解決するか

Go 標準 HTTP の明示性を保ちつつ、REST API で繰り返す routing、parameter binding、JSON、recovery、logging を簡潔にする。

## 歴史・背景

公式 README が Martini-like API と httprouter による高速化を明記する。Go の軽量 API framework の代表となり、microservice と REST API の標準候補として広く使われた。

## 中核設計

radix-tree 系 router を利用し、gin.Context が request、parameter、middleware state、response helper を集約する。middleware chain は明示的で比較的小さい。

## Data model

内蔵 ORM はない。GORM、Ent、sqlc、database/sql 等を選ぶ。binding/validator は transport DTO に集中する。

## メリット

- 学習しやすく高速
- Go ecosystem で事例と middleware が多い
- REST API の定型処理が簡潔

## デメリット / trade-off

- gin.Context への結合が強くなりやすい
- application architecture は自分で設計
- 標準 net/http handler との adapter が必要な場面

## 向いている用途

- REST API、microservice
- Go で迅速な prototype と production
- 高 throughput の JSON service

## 避ける条件

- net/http のみで十分な極小 service
- compile-time DI/full-stack 規約を求める
- Web Standards multi-runtime が必要

## 実行モデル

- primary abstraction: Engine、RouterGroup、Context
- control flow: router → middleware chain → handler
- routing: httprouter 系 tree router
- rendering: JSON/XML/HTML 等
- dependency injection: core なし。constructor/wire 等を選択
- state: request context + external state
- concurrency: goroutine per request (net/http model)
- deployment: single binary、container、serverless adapter
- extension: middleware と handler wrapper
- testing: httptest
- migration cost: 中。gin.Context API に依存

## Official / primary sources

- [Gin README](https://github.com/gin-gonic/gin/blob/master/README.md)
- [Gin official](https://gin-gonic.com/)

## Research gaps

- なし
