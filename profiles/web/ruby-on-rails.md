# Ruby on Rails

- ID: `ruby-on-rails`
- 分野: `backend-web` / `full-stack MVC`
- 言語: Ruby
- 最初の公開: 2004
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

データベース駆動 Web アプリを Convention over Configuration、MVC、Active Record、統合ツール群で一体的に構築するフルスタック framework。

## 何を解決するか

Web アプリごとに繰り返していたルーティング、ORM、テンプレート、migration、mail、job、asset、test の組み立てを一つの生産的な規約にまとめる。

## 歴史・背景

Basecamp から抽出され、2004 年に公開された。設定より規約、DRY、Active Record、scaffolding を広め、Laravel、Grails、Play、Phoenix など多くの後続に「生産性の高い統合 framework」という基準を与えた。

## 中核設計

MVC を中心に Active Record、Action Pack、Action View、Active Job、Action Cable、Active Storage などを統合する。強い規約と generator により、一般的なアプリ構造を揃える。

## Data model

Active Record パターン。DB row と振る舞いを持つ Ruby object を近づけ、migration、validation、association、callback を model に集約しやすい。

## メリット

- CRUD と業務 Web の開発速度
- 一貫した規約と成熟した gem ecosystem
- フルスタック機能が統合されている

## デメリット / trade-off

- 規約に沿わないドメインでは摩擦が増える
- Active Record model が肥大化しやすい
- 高負荷・並列処理は設計と運用の注意が必要

## 向いている用途

- SaaS、管理画面、マーケットプレイス
- 少人数で素早く価値検証する製品
- DB 中心の長寿命 Web アプリ

## 避ける条件

- 極端な低遅延・CPU 集約処理
- 厳密なヘキサゴナル境界を最初から強制したい
- 規約から大幅に外れる組込みサービス

## 実行モデル

- primary abstraction: Resource を表す Model/Controller/View
- control flow: router → controller → model → view
- routing: RESTful routes と resource
- rendering: server-rendered HTML、JSON、Hotwire
- dependency injection: 明示的 DI は中心でなく Ruby の object composition と framework hooks
- state: Active Record + session/cache/job
- concurrency: process/thread + background jobs
- deployment: Rack server、container、PaaS
- extension: Railtie、Engine、gem
- testing: Minitest 標準、RSpec ecosystem
- migration cost: 高め。Rails 規約と Active Record に深く結合

## Official / primary sources

- [Rails README](https://github.com/rails/rails/blob/main/README.md)
- [Rails official](https://rubyonrails.org/)

## Research gaps

- なし
