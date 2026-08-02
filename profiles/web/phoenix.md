# Phoenix

- ID: `phoenix`
- 分野: `backend-web` / `real-time full-stack web framework`
- 言語: Elixir
- 最初の公開: 2014
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Elixir/Erlang VM の supervision、lightweight process、message passing を Web、channel、LiveView に結び付ける full-stack framework。

## 何を解決するか

Rails 級の生産性を保ちながら、高並行、障害分離、real-time connection、長時間 session を扱う。

## 歴史・背景

Rails 経験を持つ Chris McCord が Elixir/OTP 上に構築。Plug と Ecto を組み合わせ、Channels、Presence、LiveView により server-driven interactive UI を発展させた。

## 中核設計

Plug pipeline、router、controller、socket/channel、supervision tree が中心。各 connection/process を BEAM process として隔離する。

## Data model

Ecto は schema と changeset、query DSL、migration を提供するが Active Record と異なり data と変更検証を明示的に分ける。

## メリット

- 高並行と fault tolerance
- real-time/LiveView の統合
- 明示的 data transformation と pattern matching

## デメリット / trade-off

- BEAM/functional programming の学習
- CPU-heavy 処理は別設計が必要
- ecosystem 規模は JVM/Node より小さい

## 向いている用途

- chat、dashboard、collaboration、IoT control plane
- 高接続数の Web service
- server-driven interactive UI

## 避ける条件

- CPU-bound numerical processing
- Elixir 導入が組織的に困難
- 巨大既存 Java/.NET ecosystem が必須

## 実行モデル

- primary abstraction: Plug、Controller、Socket、LiveView
- control flow: supervision + message passing + request pipeline
- routing: Phoenix Router
- rendering: HTML/JSON/LiveView diff
- dependency injection: module/function composition と application supervision
- state: immutable data、process state、Ecto
- concurrency: BEAM processes
- deployment: BEAM release、container、cluster
- extension: Plug、Hex package、behaviour
- testing: ExUnit、ConnCase、LiveViewTest
- migration cost: 中〜高。BEAM/Elixir model に依存

## Official / primary sources

- [Phoenix official](https://www.phoenixframework.org/)
- [Phoenix repository](https://github.com/phoenixframework/phoenix)

## Research gaps

- なし
