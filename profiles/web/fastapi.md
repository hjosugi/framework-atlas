# FastAPI

- ID: `fastapi`
- 分野: `backend-web` / `typed async API framework`
- 言語: Python
- 最初の公開: 2018
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Python type hints から validation、serialization、dependency、OpenAPI schema を導出する ASGI API framework。

## 何を解決するか

API の request validation、型、document、async handling の重複を減らし、editor support と実行時 contract を一致させる。

## 歴史・背景

Starlette の ASGI/Web 基盤と Pydantic の data validation を統合し、Python type hints を API design の中心に置いた。typed API framework の普及を加速した。

## 中核設計

path operation function の signature と annotation を読み、dependency graph、validation、OpenAPI を構築する。async/sync handler を共存させる。

## Data model

Pydantic model が transport schema。DB model は SQLAlchemy、SQLModel、Django ORM 等と分離できる。

## メリット

- 型から API docs と validation を生成
- 高い開発速度と editor support
- ASGI/async ecosystem

## デメリット / trade-off

- dependency injection と Pydantic の magic を理解する必要
- CPU-bound 処理は別 worker が必要
- 大規模 domain architecture は自分で定義

## 向いている用途

- typed REST API、ML service、BFF
- OpenAPI-first に近い開発
- Python async service

## 避ける条件

- server-rendered full-stack が中心
- Python type hints を使わない codebase
- 非常に低レベルな protocol server

## 実行モデル

- primary abstraction: Path operation と Pydantic model
- control flow: ASGI → routing → dependency resolution → validation → handler
- routing: Starlette routing
- rendering: JSON/Response
- dependency injection: function parameter based runtime DI
- state: request dependency + external DB/cache
- concurrency: asyncio/ASGI
- deployment: ASGI server、container、serverless adapter
- extension: dependency、middleware、Starlette ecosystem
- testing: TestClient/httpx
- migration cost: 中。Pydantic/FastAPI signature に結合

## Official / primary sources

- [FastAPI official](https://fastapi.tiangolo.com/)
- [FastAPI repository](https://github.com/fastapi/fastapi)

## Research gaps

- なし
