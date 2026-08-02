# Django

- ID: `django`
- 分野: `backend-web` / `full-stack MTV`
- 言語: Python
- 最初の公開: 2005
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

ORM、URL routing、template、form、admin、auth、migration、security を統合した Python の batteries-included Web framework。

## 何を解決するか

ニュースサイト運営で必要だった、素早いコンテンツ開発、管理画面、DB model、URL 設計、セキュリティを再利用可能にする。

## 歴史・背景

Lawrence Journal-World の newsroom 開発から生まれ、2005 年に公開された。「期限のある完璧主義者」のための framework として、明示的な Python と強い標準機能を両立した。

## 中核設計

Model-Template-View と呼ぶ責務分離、declarative model、URLconf、middleware、app registry を中心にする。admin は model metadata から CRUD UI を生成する。

## Data model

Data Mapper に近い declarative ORM。model class と field から schema、query API、migration、validation の基盤を作る。

## メリット

- 標準機能とセキュリティ既定値が豊富
- admin と ORM により業務アプリが速い
- Python ecosystem と長期互換性

## デメリット / trade-off

- async と sync の境界が複雑になり得る
- 小さな API には構成が重い
- 高度な SQL では ORM 抽象を降りる必要

## 向いている用途

- CMS、業務管理、SaaS、データ中心 Web
- セキュアな標準機能を重視するチーム
- Python の monolith

## 避ける条件

- 極小 API gateway
- 完全 async-first の低レベル処理
- DB をほぼ使わない edge function

## 実行モデル

- primary abstraction: Project、App、Model、View
- control flow: middleware → URLconf → view → template/response
- routing: URL pattern と converter
- rendering: Django template または JSON
- dependency injection: app registry と設定。DI container は中心でない
- state: ORM、session、cache
- concurrency: WSGI と ASGI。sync/async view
- deployment: WSGI/ASGI server、container、PaaS
- extension: reusable app、middleware、template tags
- testing: unittest ベースの test client、DB fixture
- migration cost: 中〜高。ORM、settings、app lifecycle に結合

## Official / primary sources

- [Django official](https://www.djangoproject.com/)
- [Django repository](https://github.com/django/django)

## Research gaps

- なし
