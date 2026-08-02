# Flask

- ID: `flask`
- 分野: `backend-web` / `micro web framework`
- 言語: Python
- 最初の公開: 2010
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Werkzeug と Jinja を基盤に、routing、request context、template を小さく提供する Python microframework。

## 何を解決するか

Django の full-stack 規約を必要としない小さな Web app/API を、Pythonic な最小 core と extension で構築する。

## 歴史・背景

Pocoo ecosystem の April Fools project から実用 framework へ発展。Sinatra 型 microframework の Python 代表として、多数の extension と教育事例を生んだ。

## 中核設計

application/request context、decorator routing、WSGI を中心にする。DB、auth、form は extension または application が選ぶ。

## Data model

内蔵 model なし。SQLAlchemy、MongoEngine 等を選択。

## メリット

- 小さく理解しやすい
- 自由な architecture
- 成熟した WSGI ecosystem

## デメリット / trade-off

- extension 選定と統合責任が利用者側
- async-first ではない
- 大規模化すると独自規約が必要

## 向いている用途

- 小規模 Web/API、教育、internal tool
- custom architecture を組む
- WSGI 資産を活用

## 避ける条件

- 自動 OpenAPI/validation が必須
- full admin/ORM/auth を標準で求める
- 完全 async service

## 実行モデル

- primary abstraction: Flask application、request context
- control flow: WSGI → route → view function
- routing: Werkzeug routing
- rendering: Jinja/JSON
- dependency injection: なし
- state: context locals + external state
- concurrency: WSGI server model
- deployment: WSGI server/container/serverless adapter
- extension: Flask extensions
- testing: built-in test client
- migration cost: 低〜中。Werkzeug/Flask context に依存

## Official / primary sources

- [Flask official](https://flask.palletsprojects.com/)
- [Flask repository](https://github.com/pallets/flask)

## Research gaps

- なし
