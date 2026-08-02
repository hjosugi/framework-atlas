# Rails・Laravel・Django — cohesive full-stack conventions

確認日: 2026-08-02。観測version: Rails 8.1.3.1、Laravel Framework 13.23.0、Django 6.0.7。Rails/Laravelではframework本体repositoryとapplication skeleton repositoryを別artifactとして扱う。

## 共通する設計

三者は言語もcontainer modelも異なるが、routing、data access、templates、validation、security、CLI、migrationなどを一つのapplication workflowとして提供する。個々の部品の最小性ではなく、チームが同じ場所に同じ責務を置けることが速度を生む。

| 軸 | Rails | Laravel | Django |
|---|---|---|---|
| primary opinion | Convention over Configuration | expressive API + service container | batteries included + explicit app/project |
| data | Active Record | Eloquent | Django ORM |
| CLI | `bin/rails` generators/tasks | Artisan | `manage.py` commands |
| composition | initializer/framework conventions | container/providers/facades | settings/apps/middleware |
| notable standard surface | Hotwire/Active Job/Action Cable等 | queue/events/scheduler等 | admin/forms/auth/security等 |

## 長所と限界

規約はonboarding、生成、upgrade、横断機能を揃える。ただしdomainが複雑になるとORM model、request model、domain modelを同一視しない工夫が必要である。ORMはquery/migration/relationshipのproductivityを高める一方、lazy I/O、N+1、persistence lifecycle、Active Record methodがdomainへ結合する。generatorはstartを速めるが、生成後の所有権とupgrade pathが無ければ複製されたboilerplateになる。frameworkの規約にdomain boundaryを合わせるのではなく、bounded contextの内部でframework adapterを使う。

Spring Bootはfull-stack UI/ORMを一つに固定せずstarter/auto-config/operationsを統合する。FastAPIはtyped API surfaceを強くするがORM/admin/queueを内包しない。Ginはさらに小さいHTTP coreである。このproduction completeness差は優劣ではなく、frameworkが所有する範囲の差として記録する。frontend routingなど非適用の軸は `not-applicable`、未調査は `unknown` にする。

## kofun-bootへの抽出

directory、naming、test、configuration、migrationのgolden pathをCLIで生成し、生成物を一回限りの雛形にせずupgrade可能な宣言へ寄せる。defaultはproduction-readyで、外す方法と外した影響を診断する。Active Record型の便利さをdomain ruleへ直結せず、data mappingを選べるportにする。

## Sources

- https://rubyonrails.org/doctrine
- https://guides.rubyonrails.org/command_line.html
- https://laravel.com/docs
- https://docs.djangoproject.com/en/6.0/intro/overview/
- https://github.com/rails/rails/releases/tag/v8.1.3.1
- https://github.com/laravel/framework/releases/tag/v13.23.0
- https://www.djangoproject.com/weblog/2026/jul/07/security-releases/
