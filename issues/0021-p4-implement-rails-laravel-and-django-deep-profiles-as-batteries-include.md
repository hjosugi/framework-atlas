# #21 P4 implement Rails, Laravel, and Django deep profiles as batteries-included baselines

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/21
- Updated: 2026-08-02T05:40:27Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E3 #4](https://github.com/hjosugi/framework-atlas/issues/4)
- Blocked on: D1-D3

## Official inputs
Rails Guides、Laravel documentation、Django documentation/repositories。

## Artifacts
`profiles/rails.md`, `laravel.md`, `django.md` と比較data。

## Implementation
MVC/MTV、routing、ORM、migration、DI/service container、generator/CLI、template、job/realtime、security/opsを同じdimensionで比較する。Active Record、Eloquent、Django ORMを別entity/relationshipで扱う。

## Acceptance
- [ ] convention-over-configurationの具体的artifactを列挙。
- [ ] framework本体とapplication skeleton repositoryを区別。
- [ ] ORMのproductivityとdomain coupling/N+1/lazy IOを比較。
- [ ] release/historyはofficial evidenceにjoin。
- [ ] comparableでない欄はnot-applicable。
- [ ] Spring Boot/FastAPI/Ginとのproduction completeness差を事実として表す。

## Non-goals
言語優劣、サンプルコード量産。
