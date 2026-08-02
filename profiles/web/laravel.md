# Laravel

- ID: `laravel`
- 分野: `backend-web` / `full-stack MVC`
- 言語: PHP
- 最初の公開: 2011
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

表現力の高い API と統合された routing、container、Eloquent ORM、queue、cache、auth、CLI を提供する PHP のフルスタック framework。

## 何を解決するか

PHP Web 開発で繰り返される認証、ルーティング、セッション、キャッシュ、DB 操作を、楽しく一貫した開発体験で解決する。

## 歴史・背景

Taylor Otwell が 2011 年に開始した。初期公式文書は Ruby on Rails、ASP.NET MVC、Sinatra などから良い点を組み合わせたと明記している。Symfony components を活用しつつ独自の Eloquent、Blade、Artisan、service container を発展させた。

## 中核設計

service container と provider が起動・拡張の中心。Facade は container 解決を簡潔に表し、Artisan と convention が日常作業を統合する。

## Data model

Eloquent Active Record。relation、scope、cast、event、factory を model に集約し、Query Builder と raw SQL も併用できる。

## メリット

- PHP で非常に高い開発速度
- 公式 ecosystem が広く整合している
- 文書・学習資源・採用市場が大きい

## デメリット / trade-off

- Facade と magic により依存が見えにくくなることがある
- Active Record model の責務過多
- 大規模化では境界設計を意識しないと密結合

## 向いている用途

- SaaS、EC、管理系、API
- PHP チームの標準 platform
- queue、mail、notification を含む製品

## 避ける条件

- 極小ランタイムや常時低メモリが必要
- 完全に明示的な dependency graph を要求
- 単一関数だけの edge workload

## 実行モデル

- primary abstraction: Application、Service Container、Eloquent Model
- control flow: middleware → route/controller → service/model → response
- routing: 宣言的 route と middleware group
- rendering: Blade、JSON、Inertia/Livewire ecosystem
- dependency injection: runtime service container
- state: Eloquent、session、cache、queue
- concurrency: PHP request model + queue / Octane option
- deployment: PHP-FPM、container、serverless/Octane
- extension: Service Provider、package、macro
- testing: PHPUnit/Pest 統合、HTTP/database helpers
- migration cost: 中〜高。Laravel conventions への依存

## Official / primary sources

- [Laravel current docs](https://laravel.com/docs)
- [Laravel 4.2 philosophy and influences](https://github.com/laravel/docs/blob/4.2/introduction.md)
- [Laravel framework repository](https://github.com/laravel/framework)

## Research gaps

- なし
