# 家系図で読む framework 史

公開ページはこの data を SVG の家系図として表示する。ここでは GitHub 上で読める簡略版を掲載する。

- `──▶` は一次資料で確認済みの基盤・後継・明示的影響
- `╌╌▶` は設計上の応答・影響候補で、追加 evidence が必要
- `┈┈▶` は直接の血縁ではなく、同じ問題領域・共通基盤・topic 分類

## Java / Spring 家系

Java Web の container 標準と IoC/DI を起点に、設定の複雑さを減らす Spring、起動を簡単にする Spring Boot、build-time 最適化を重視する Micronaut / Quarkus へ進んだ流れ。

**中心の問い:** 大規模 Java application の配線、設定、起動、運用をどう簡単にするか。

### 祖先・基礎標準 (1990s–2000s)

- **Java Servlet API** — Web container と application の契約
- **Inversion of Control / Dependency Injection** — object の生成と配線を外へ出す
- **Build-time augmentation** — runtime 処理を build 時へ移す
- **Jakarta EE** — enterprise Java の標準群

### 基盤 framework (2004)

- **Spring Framework** — DI container と enterprise abstraction を統合

### 第二世代 (2011–2019)

- **Spring Data JPA** — Repository で data access を標準化
- **Spring Boot** — 良い既定値と自動設定で起動を高速化
- **Micronaut** — compile-time DI で起動と memory を改善
- **Quarkus** — cloud-native / native image 向けに build-time 化

### 拡張領域 (2024–)

- **Spring AI** — Spring の流儀で AI integration を統合

### 枝

- **Java Servlet API** ──▶ **Spring Framework**: Servlet Web stack を抽象化
- **Inversion of Control / Dependency Injection** ──▶ **Spring Framework**: IoC/DI container を中核に採用
- **Spring Framework** ──▶ **Spring Boot**: Spring を opinionated に本番化
- **Spring Framework** ──▶ **Spring Data JPA**: Repository abstraction を ecosystem 化
- **Spring Framework** ╌╌▶ **Micronaut**: Spring-like API を compile-time 化
- **Build-time augmentation** ──▶ **Micronaut**: DI/AOP metadata を build 時に生成
- **Build-time augmentation** ──▶ **Quarkus**: augmentation を build 時へ移動
- **Jakarta EE** ──▶ **Quarkus**: Jakarta EE / MicroProfile を cloud-native に実装
- **Spring Boot** ╌╌▶ **Quarkus**: 同じ生産性課題への別解
- **Spring Framework** ──▶ **Spring AI**: Spring idiom の AI integration

### 覚えること

- Spring Boot は Spring Framework の置き換えではなく、その上に良い既定値を置く層。
- Micronaut と Quarkus は単なる子孫ではなく、起動時間・memory・native image という新しい制約への設計上の応答。
- 家系図の破線は「影響の可能性や設計上の応答」で、公式に明記された直接継承とは区別する。

## Rails / Laravel と MVC 家系

MVC、Rack、Active Record、Convention over Configuration を結びつけた Rails が、Web application の開発速度を大きく変え、Laravel、Grails、Phoenix などの設計議論に影響した流れ。

**中心の問い:** database-backed Web application を、少ない設定と一貫した規約でどう速く作るか。

### 設計思想 (1979–2004)

- **Model-View-Controller** — Model / View / Controller の責務分離
- **Convention over Configuration** — 一般的な選択を規約にする
- **Rack interface** — Ruby server と app の共通 interface
- **Active Record pattern** — record object が persistence を持つ

### 第一世代 (2004–2009)

- **Ruby on Rails** — full-stack MVC + convention
- **Sinatra** — 小さな route DSL
- **ASP.NET MVC** — Microsoft の MVC framework
- **Symfony** — 再利用可能 components を持つ PHP framework

### 派生・再解釈 (2005–2014)

- **Grails** — Rails-like productivity を JVM/Groovy へ
- **Play Framework** — JVM で高速 feedback loop
- **Laravel** — PHP で expressive full-stack experience
- **Phoenix** — BEAM 上で Rails 級の productivity

### data model の枝 (2004–)

- **Rails Active Record** — Rails の ORM
- **Eloquent ORM** — Laravel の Active Record ORM

### 枝

- **Model-View-Controller** ──▶ **Ruby on Rails**: MVC を中核に採用
- **Convention over Configuration** ──▶ **Ruby on Rails**: 規約で設定量を削減
- **Rack interface** ──▶ **Ruby on Rails**: Rack interface 上で動作
- **Rack interface** ──▶ **Sinatra**: Rack application
- **Active Record pattern** ──▶ **Rails Active Record**: Active Record pattern を実装
- **Ruby on Rails** ╌╌▶ **Grails**: Rails-like convention を JVM へ
- **Ruby on Rails** ╌╌▶ **Play Framework**: rapid full-stack feedback loop の系譜
- **Ruby on Rails** ──▶ **Laravel**: Laravel 公式が影響源に列挙
- **Sinatra** ──▶ **Laravel**: Laravel 公式が影響源に列挙
- **ASP.NET MVC** ──▶ **Laravel**: Laravel 公式が影響源に列挙
- **Symfony** ──▶ **Laravel**: Symfony components を利用
- **Ruby on Rails** ╌╌▶ **Phoenix**: Rails 級の productivity を BEAM で再構成
- **Rails Active Record** ╌╌▶ **Eloquent ORM**: Active Record 型 ORM の系譜

### 覚えること

- Rails の革新は個別機能より、MVC・ORM・routing・migration・testing を一つの規約にまとめた点。
- Laravel は Rails のコピーではなく、Rails / Sinatra / ASP.NET MVC の体験と Symfony components を PHP に統合した。
- Phoenix は見た目が Rails に近くても、runtime と failure model は Erlang/OTP に由来する。

## Python Web 家系

WSGI が Python Web server と application の共通契約を作り、Django と Flask が成熟した。WebSocket と async I/O の要求から ASGI、Starlette、FastAPI という新しい枝が生まれた。

**中心の問い:** Python の簡潔さを保ちながら、full-stack、microservice、async API をどう支えるか。

### server contract (2003–2016)

- **WSGI** — 同期 Web server interface
- **ASGI** — async HTTP / WebSocket interface
- **Event loop / non-blocking I/O** — non-blocking I/O

### 主要基盤 (2005–2018)

- **Django** — batteries-included full-stack
- **Flask** — 小さな WSGI microframework
- **Starlette** — 軽量 ASGI toolkit
- **Pydantic** — type-driven validation
- **Tornado** — non-blocking Web server/framework
- **SQLAlchemy** — SQLModel の ORM/query foundation

### 派生・統合 (2011–2021)

- **Django REST Framework** — Django に API layer を追加
- **Quart** — Flask-compatible async framework
- **FastAPI** — Starlette + Pydantic の API framework
- **Litestar** — ASGI application framework
- **SQLModel** — Pydantic + SQLAlchemy の model

### 枝

- **WSGI** ──▶ **Django**: WSGI deployment
- **WSGI** ──▶ **Flask**: WSGI framework
- **ASGI** ──▶ **Django**: ASGI deployment path
- **ASGI** ──▶ **Starlette**: ASGI toolkit
- **ASGI** ──▶ **FastAPI**: ASGI application
- **Event loop / non-blocking I/O** ──▶ **Tornado**: non-blocking I/O
- **Django** ┈┈▶ **Django REST Framework**: Django ecosystem の API layer
- **Flask** ──▶ **Quart**: Flask-compatible async reimplementation
- **Starlette** ──▶ **FastAPI**: Web / ASGI layer
- **Pydantic** ──▶ **FastAPI**: validation / schema layer
- **ASGI** ┈┈▶ **Litestar**: 同じ ASGI application problem を扱う
- **Pydantic** ──▶ **SQLModel**: validation/schema foundation
- **SQLAlchemy** ──▶ **SQLModel**: ORM/query foundation

### 覚えること

- Django と Flask の違いは大小だけでなく、framework が application architecture をどこまで決めるか。
- FastAPI の核は async だけではなく、Starlette の Web layer と Pydantic の data contract を統合した点。
- WSGI と ASGI は framework ではなく、server と application の契約。

## Go HTTP framework 家系

Go は標準 library の net/http が強いため、framework は薄い router と middleware の形になりやすい。Gin は httprouter と Martini-like API を統合し、Fiber は fasthttp と Express-like API を組み合わせた。

**中心の問い:** Go の標準性と単純さを壊さず、routing・middleware・validation の定型作業をどこまで提供するか。

### 共通基盤 (2009–)

- **Go net/http** — 標準 interface
- **fasthttp** — performance-oriented HTTP implementation
- **Express** — Express-like developer experience の参照点

### router / API style (2012–2015)

- **httprouter** — radix tree の高速 router
- **chi** — net/http 互換の composable router
- **Gorilla Mux** — 柔軟な URL matcher
- **Martini** — 早期の Go Web microframework
- **Echo** — 小さな API framework

### 統合 framework (2014–2020)

- **Gin** — httprouter + Martini-like API
- **Fiber** — fasthttp + Express-like API
- **GoFrame** — より統合的な Go application framework

### 枝

- **Go net/http** ┈┈▶ **httprouter**: Go HTTP ecosystem の router
- **Go net/http** ┈┈▶ **chi**: 標準 http.Handler を維持
- **Go net/http** ┈┈▶ **Gorilla Mux**: 標準 HTTP router
- **Go net/http** ┈┈▶ **Martini**: Go Web application layer
- **Go net/http** ┈┈▶ **Echo**: Go API framework
- **httprouter** ──▶ **Gin**: routing performance foundation
- **Martini** ──▶ **Gin**: Martini-like API
- **fasthttp** ──▶ **Fiber**: fasthttp runtime
- **Express** ──▶ **Fiber**: Express-inspired API
- **Go net/http** ┈┈▶ **GoFrame**: 同じ Go Web problem の統合型解

### 覚えること

- chi は標準 net/http との互換性を最優先し、Gin は便利な Context と binding を追加する。
- Fiber は net/http 互換性より fasthttp の performance model を選ぶため、移植性との tradeoff がある。
- 点線は「同じ基盤・問題領域」であり、直接影響を意味しない。

## JavaScript / Edge backend 家系

Node.js の event loop 上で Express が middleware と routing の事実上の型を作った。その後 Koa、Fastify、NestJS が構造や性能を再設計し、Hono は Fetch API を共通基盤に edge / Deno / Bun / Node を横断する。

**中心の問い:** JavaScript backend の簡潔さを保ちながら、async、型、安全な構造、multi-runtime portability をどう実現するか。

### runtime / standard (2000s–2015)

- **Event loop / non-blocking I/O** — Node の non-blocking I/O model
- **Web Standards Fetch API** — Request / Response の Web Standard

### API の原型 (2010)

- **Express** — middleware + routing の最小 core
- **Angular** — NestJS の module/decorator/DI 設計への影響源

### 再設計と分化 (2013–2022)

- **Koa** — async middleware を小さく再設計
- **Fastify** — schema と performance を重視
- **NestJS** — module / decorator / DI で大規模化
- **Hono** — Web Standards で multi-runtime 化
- **Elysia** — Bun と type inference を重視

### 枝

- **Event loop / non-blocking I/O** ──▶ **Express**: Node.js event loop 上で動作
- **Express** ──▶ **Koa**: Express authors による async/minimal 再設計
- **Express** ──▶ **NestJS**: default HTTP adapter
- **Fastify** ──▶ **NestJS**: alternate HTTP adapter
- **Angular** ──▶ **NestJS**: module/decorator/DI architecture
- **Web Standards Fetch API** ──▶ **Hono**: Web Standards Request/Response を中核化
- **Express** ──▶ **Hono**: Express に近い小さな API
- **Express** ┈┈▶ **Fastify**: 同じ Node server problem への別解
- **Web Standards Fetch API** ┈┈▶ **Elysia**: modern runtime / typed HTTP の同世代

### 覚えること

- Express は application architecture をほぼ決めない。NestJS は逆に module、DI、controller を強く規定する。
- Hono の重要点は小ささだけでなく、Node 固有 API ではなく Web Standards を共通面にしたこと。
- 同じ JavaScript でも runtime と deployment target が設計を大きく変える。

## React 家系

React は component と declarative rendering を普及させたが、routing や data layer を別選択に残した。その空白を Redux、React Router、Next.js、React Native、Expo などが埋め、巨大な ecosystem が形成された。

**中心の問い:** UI を再利用可能な component として宣言し、Web・server・native へどう拡張するか。

### 設計原理 (1990s–2020)

- **Component-based UI** — component-based UI
- **Virtual DOM** — Virtual DOM reconciliation
- **Flux architecture** — one-way data flow
- **The Elm Architecture** — Model / Update / View
- **Server Components** — server-only component execution

### 中核 (2013–2015)

- **React** — UI rendering library
- **Redux** — predictable state container

### application layer (2014–2017)

- **React Router** — routing / framework mode
- **Next.js** — full-stack meta-framework
- **Gatsby** — static/site framework
- **React Native** — native renderer
- **Ink** — terminal renderer

### さらに上の platform (2015–)

- **Expo** — React Native application platform
- **Blitz.js** — Next.js 上の full-stack toolkit
- **TanStack Router** — type-safe URL state を強化

### 枝

- **Component-based UI** ──▶ **React**: component から UI を構成
- **Virtual DOM** ──▶ **React**: reconciliation の仮想 tree
- **Server Components** ──▶ **React**: server-only component execution
- **Flux architecture** ╌╌▶ **Redux**: action/store lineage
- **The Elm Architecture** ──▶ **Redux**: reducer/update model
- **React** ──▶ **React Router**: routing ecosystem
- **React** ──▶ **Next.js**: React full-stack meta-framework
- **Server Components** ──▶ **Next.js**: App Router で RSC を統合
- **React** ──▶ **Gatsby**: React site framework
- **React** ──▶ **React Native**: component model を native に展開
- **React** ╌╌▶ **Ink**: component model を terminal に適用
- **React Native** ──▶ **Expo**: SDK / build / update platform
- **Next.js** ──▶ **Blitz.js**: Next ecosystem full-stack toolkit
- **React Router** ╌╌▶ **TanStack Router**: type-safe URL state という設計上の対比

### 覚えること

- React 自体は full framework ではないため、家族の多くが routing・data・deployment の空白を埋める。
- Next.js は React の子孫というより application framework 層。React Native は DOM 以外へ renderer を差し替えた枝。
- ecosystem の自由度は強みだが、設計判断が分散するという cost でもある。

## Vue 家系

Vue は template と reactivity の学びやすさを保ちつつ、component、Virtual DOM、compiler optimization を組み合わせた。Vue Router、Pinia、Nuxt が routing・state・full-stack の公式に近い一貫した枝を作った。

**中心の問い:** 既存 HTML に近い開発体験と、大規模 component application の構造をどう両立するか。

### 影響した設計 (2010s)

- **AngularJS** — template / directive / reactivity
- **React** — component / Virtual DOM 世代
- **Reactive programming** — dependency tracking
- **Virtual DOM** — Virtual DOM

### 中核 (2014)

- **Vue** — progressive UI framework

### 公式 ecosystem (2014–2019)

- **Vue Router** — routing
- **Pinia** — state management
- **Nuxt** — full-stack meta-framework

### 枝

- **AngularJS** ╌╌▶ **Vue**: template/directive/reactivity lineage
- **React** ╌╌▶ **Vue**: component/Virtual DOM 世代の設計統合
- **Reactive programming** ──▶ **Vue**: reactive dependency tracking
- **Virtual DOM** ──▶ **Vue**: Virtual DOM + compiler optimization
- **Vue** ──▶ **Vue Router**: official routing ecosystem
- **Vue** ──▶ **Pinia**: official state store
- **Vue** ──▶ **Nuxt**: Vue full-stack meta-framework

### 覚えること

- Vue は React と AngularJS の中間というだけではなく、runtime reactivity と compiler の協調が重要。
- Vue Router / Pinia / Nuxt が比較的一貫した推奨経路を作り、React より選択肢を絞りやすい。
- Vue 2 から Vue 3 では Proxy-based reactivity と Composition API が大きな世代交代。

## 現代 UI framework の別系統

Angular、Svelte、Solid、Qwik、Astro は同じ SPA/UI 問題に対し、DI、compiler、fine-grained signals、resumability、islands という異なる解を選んだ。直接の親子ではなく「設計競争の家系図」として読む。

**中心の問い:** 大規模 UI の開発性を保ちながら、bundle、hydration、再描画、server/client 境界の cost をどう減らすか。

### 設計原理 (2010s–2020s)

- **AngularJS** — 初期 SPA framework
- **Compiler-first UI** — compile-time UI
- **Fine-grained signals** — fine-grained dependency graph
- **Resumability** — execution を再開する model
- **Islands architecture** — 必要な island だけ hydrate

### 主要な別解 (2016–2021)

- **Angular** — 統合型 enterprise UI framework
- **Svelte** — compiler-first UI
- **SolidJS** — signals 中心の fine-grained UI
- **Qwik** — resumability
- **Astro** — islands architecture

### full-stack layer (2020–2023)

- **Analog** — Angular meta-framework
- **SvelteKit** — Svelte meta-framework
- **SolidStart** — Solid full-stack framework
- **Qwik City** — Qwik routing/meta-framework

### 枝

- **AngularJS** ──▶ **Angular**: 全面再設計された後継
- **Fine-grained signals** ──▶ **Angular**: Signals を state primitive として採用
- **Compiler-first UI** ──▶ **Svelte**: component を build 時に変換
- **Fine-grained signals** ──▶ **SolidJS**: fine-grained reactive signals
- **Resumability** ──▶ **Qwik**: serialization と lazy resume
- **Islands architecture** ──▶ **Astro**: interactive island のみ hydrate
- **Angular** ──▶ **Analog**: Angular meta-framework
- **Svelte** ──▶ **SvelteKit**: Svelte full-stack framework
- **SolidJS** ──▶ **SolidStart**: Solid full-stack framework
- **Qwik** ──▶ **Qwik City**: Qwik routing/meta-framework

### 覚えること

- この図の横並びは直接の血縁ではなく、同じ performance 問題への異なる戦略。
- Svelte は runtime diff を compiler に移し、Solid は dependency を細粒度に追跡し、Qwik は hydration 自体を避けようとする。
- meta-framework 層では routing、data loading、SSR/SSG、deployment が統合される。

## Terminal UI / Textualize 家系

Rich が terminal rendering の表現力を高め、その上に Textual が widget、reactive state、CSS-like styling、event loop を統合した。Trogon、Textual Web、snapshot testing、Frogmouth、Toolong が一つの ecosystem を形成する。

**中心の問い:** terminal を単なる文字出力ではなく、testable で配布可能な application platform にできるか。

### 複数の祖先 (1980s–2010s)

- **Terminal UI の伝統** — 共通の問題領域
- **React** — component model
- **The Elm Architecture** — Model / Update / View

### 基盤・別流派 (2004–2023)

- **Rich** — rich text / table / layout rendering
- **Urwid** — Python console UI library
- **prompt_toolkit** — interactive command line toolkit
- **Ink** — React renderer for terminal
- **Bubble Tea** — Elm Architecture for TUI
- **Ratatui** — Rust TUI library

### application framework (2021)

- **Textual** — Python TUI application framework

### 開発・配布 ecosystem (2023–)

- **Trogon** — Click/Typer CLI を TUI 化
- **Textual Web** — browser delivery
- **pytest-textual-snapshot** — snapshot testing

### 代表 application (2023–)

- **Frogmouth** — Markdown browser
- **Toolong** — log viewer / search

### 枝

- **Terminal UI の伝統** ┈┈▶ **Rich**: terminal rendering の問題領域
- **Terminal UI の伝統** ┈┈▶ **Urwid**: terminal widget/application の問題領域
- **Terminal UI の伝統** ┈┈▶ **prompt_toolkit**: interactive terminal input の問題領域
- **Terminal UI の伝統** ┈┈▶ **Ratatui**: terminal widget/rendering の問題領域
- **React** ╌╌▶ **Ink**: React component model を terminal に適用
- **The Elm Architecture** ──▶ **Bubble Tea**: Elm Architecture を TUI に適用
- **Rich** ──▶ **Textual**: terminal rendering foundation と同一 ecosystem
- **Textual** ──▶ **Trogon**: CLI を Textual UI に変換
- **Textual** ──▶ **Textual Web**: browser delivery
- **Textual** ──▶ **pytest-textual-snapshot**: snapshot testing
- **Textual** ──▶ **Frogmouth**: Textual で構築された application
- **Textual** ──▶ **Toolong**: Textual で構築された application

### 覚えること

- Rich は formatting/rendering library、Textual は application lifecycle を持つ framework。
- Textual Web は別 framework ではなく Textual application の配信先を増やす ecosystem component。
- Bubble Tea と Ink は Textual の祖先ではなく、Elm / React の考え方を terminal に持ち込んだ別系統。

## ORM / Data Model 家系

ORM は一つの家系ではない。Model 自身が保存する Active Record、mapping を分離する Data Mapper、transaction の変更をまとめる Unit of Work、schema/code generation を重視する現代型に分かれる。

**中心の問い:** object / type / domain model と relational database の差を、どの責務分担で埋めるか。

### 設計 pattern (1980s–2000s)

- **Active Record pattern** — model 自身が persistence を持つ
- **Data Mapper pattern** — mapping を独立 layer に置く
- **Unit of Work** — 変更を追跡し一括 commit
- **Typed schema / code generation** — 同じ問題への別解

### Active Record / model-centric枝 (2004–)

- **Rails Active Record** — Active Record
- **GORM** — Go の model-centric ORM
- **Django ORM** — Django model API
- **Pydantic** — SQLModel の validation/schema foundation

### Data Mapper / Unit of Work枝 (2001–)

- **Hibernate ORM** — JPA / Unit of Work
- **SQLAlchemy** — Data Mapper + Unit of Work
- **Doctrine ORM** — Data Mapper + Unit of Work
- **Entity Framework Core** — .NET DbContext / mapper

### Typed schema / codegen / SQL-first枝 (2010s–)

- **Prisma ORM** — schema-first typed client
- **Ent** — Go schema/codegen
- **sqlc** — SQL-first codegen

### framework integration (ecosystem)

- **Eloquent ORM** — Laravel Active Record
- **Spring Data JPA** — Repository abstraction over JPA
- **SQLModel** — Pydantic + SQLAlchemy

### 枝

- **Active Record pattern** ──▶ **Rails Active Record**: Active Record pattern を実装
- **Active Record pattern** ╌╌▶ **GORM**: model-centric ORM API
- **Active Record pattern** ╌╌▶ **Django ORM**: model-centric persistence API
- **Rails Active Record** ╌╌▶ **Eloquent ORM**: Active Record 型 ORM の系譜
- **Data Mapper pattern** ┈┈▶ **Hibernate ORM**: mapping layer の系譜
- **Unit of Work** ──▶ **Hibernate ORM**: Persistence Context / Unit of Work
- **Data Mapper pattern** ──▶ **SQLAlchemy**: Data Mapper
- **Unit of Work** ──▶ **SQLAlchemy**: Session が Unit of Work を管理
- **Data Mapper pattern** ──▶ **Doctrine ORM**: Data Mapper / Unit of Work
- **Data Mapper pattern** ──▶ **Entity Framework Core**: DbContext / mapper model
- **Unit of Work** ──▶ **Entity Framework Core**: DbContext SaveChanges
- **Hibernate ORM** ──▶ **Spring Data JPA**: JPA provider の一般的選択
- **SQLAlchemy** ──▶ **SQLModel**: ORM/query foundation
- **Pydantic** ──▶ **SQLModel**: validation/schema foundation
- **Typed schema / code generation** ┈┈▶ **Prisma ORM**: typed schema/code generation の流れ
- **Typed schema / code generation** ┈┈▶ **Ent**: typed schema/code generation の流れ
- **Typed schema / code generation** ┈┈▶ **sqlc**: SQL-first code generation の流れ

### 覚えること

- Active Record は速く作りやすいが、domain logic と persistence の責務が一つの model に集まりやすい。
- Data Mapper は境界を分けやすいが、mapping と session lifecycle の複雑さが増える。
- Prisma / Ent / sqlc は ORM の単純な後継ではなく、型・schema・code generation を重視する別の答え。

## HTML over the wire 家系

HTMX、Hotwire、Phoenix LiveView は、すべてを巨大な client application にする代わりに、server で生成した HTML または server-managed UI state を活用する。

**中心の問い:** SPA-like な操作感を保ちながら、client-side JavaScript と二重 state 管理をどこまで減らせるか。

### 設計原理 (2000s–)

- **HTML over the wire** — HTML fragment を主要 transfer format にする

### 構成要素・主要 framework (2018–2020)

- **Stimulus** — HTML-first behavior controller
- **Turbo** — navigation / frames / streams
- **HTMX** — HTML response を DOM に swap
- **Phoenix** — BEAM full-stack framework
- **Ruby on Rails** — Hotwire を統合する application framework

### 統合体 (2019–2020)

- **Hotwire** — Turbo + Stimulus の approach
- **Phoenix LiveView** — server-driven realtime UI

### 枝

- **HTML over the wire** ──▶ **HTMX**: HTML response を DOM に swap
- **HTML over the wire** ──▶ **Hotwire**: HTML を transfer format として利用
- **Stimulus** ──▶ **Hotwire**: HTML behavior controller
- **Turbo** ──▶ **Hotwire**: navigation / frames / streams
- **Phoenix** ──▶ **Phoenix LiveView**: server-driven UI extension
- **HTML over the wire** ┈┈▶ **Phoenix LiveView**: 同じ client-state 削減問題への別解
- **Ruby on Rails** ──▶ **Hotwire**: modern Rails interaction stack

### 覚えること

- HTMX は HTML attribute と server response を中心にする小さな layer。Hotwire は Turbo と Stimulus を組み合わせた ecosystem。
- LiveView は HTML fragment だけでなく、server process が UI state と event loop を管理する点が異なる。
- offline-first や非常に rich な local interaction では client-heavy architecture が有利な場合もある。

## Erlang/OTP・Elixir・Phoenix 家系

Actor model を実用化した Erlang/OTP、その VM 上で生産性を高めた Elixir、Plug / Ecto を統合する Phoenix、server-driven UI の LiveView へ続く流れ。

**中心の問い:** 大量 concurrency、failure isolation、realtime communication を、application developer が扱いやすい形にできるか。

### 理論と runtime (1973–1986)

- **Actor model** — message passing と isolation
- **Erlang/OTP** — process / supervision / distribution

### language と components (2012–2014)

- **Elixir language/platform** — BEAM 上の language/tooling
- **Plug** — HTTP connection pipeline
- **Ecto** — data layer

### Web framework (2014)

- **Phoenix** — full-stack Web framework

### realtime UI (2019)

- **Phoenix LiveView** — server-driven UI

### 枝

- **Actor model** ──▶ **Erlang/OTP**: process/message/supervision model
- **Erlang/OTP** ──▶ **Phoenix**: BEAM supervision/distribution
- **Elixir language/platform** ──▶ **Phoenix**: Elixir macro/process ecosystem
- **Plug** ──▶ **Phoenix**: HTTP connection pipeline
- **Ecto** ──▶ **Phoenix**: 標準的 data layer
- **Phoenix** ──▶ **Phoenix LiveView**: server-driven UI extension

### 覚えること

- Phoenix の強みは Ruby-like syntax だけでなく、BEAM の process と supervision にある。
- Ecto は Rails Active Record と異なり、changeset と query を明示的に扱う。
- LiveView は server process と WebSocket を使い、UI state の中心を server に置く。

## Mobile / Desktop UI 家系

React Native は React component model を native renderer に展開し、Expo が application platform を追加した。Tauri は system WebView を利用する。Flutter、SwiftUI、Jetpack Compose は declarative UI という同世代の別解で、直接の親子とは限らない。

**中心の問い:** 一つの開発 model で複数 platform を狙いながら、native UX、binary size、performance をどう両立するか。

### 基礎モデル (2000s–2010s)

- **React** — component model
- **System WebView** — OS の embedded Web renderer
- **Declarative native UI** — 同じ問題への別解

### 主要 framework (2015–2022)

- **React Native** — React renderer for native
- **Tauri** — system WebView + Rust host
- **Flutter** — cross-platform rendering framework
- **SwiftUI** — Apple declarative UI
- **Jetpack Compose** — Android declarative UI
- **Qt** — mature cross-platform native toolkit

### application platform / expansion (2015–2021)

- **Expo** — React Native SDK/build/update layer
- **Compose Multiplatform** — Compose を desktop 等へ拡張

### 枝

- **React** ──▶ **React Native**: component model を native に展開
- **React Native** ──▶ **Expo**: SDK / router / build / update layer
- **System WebView** ╌╌▶ **Tauri**: system WebView を UI renderer に利用
- **Declarative native UI** ┈┈▶ **Flutter**: declarative cross-platform UI
- **Declarative native UI** ┈┈▶ **SwiftUI**: declarative native UI
- **Declarative native UI** ┈┈▶ **Jetpack Compose**: declarative native UI
- **Jetpack Compose** ┈┈▶ **Compose Multiplatform**: Compose programming model の platform expansion
- **Declarative native UI** ┈┈▶ **Qt**: cross-platform UI toolkit の先行世代

### 覚えること

- React Native は WebView ではなく native renderer の枝。Tauri は system WebView を使う枝。
- Flutter は独自 rendering stack を持ち、platform widget の wrapper とは異なる。
- 一つの codebase という利点と、platform-specific UX/SDK に降りる cost を比較する。

## AI / Agent framework 家系

TensorFlow / PyTorch の model execution 系、Keras / Lightning の高水準 training 系、LangChain / LangGraph の LLM orchestration 系、AutoGen / Agents SDK の agent runtime 系は、同じ AI topic でも解く問題が異なる。

**中心の問い:** model の構築、training、tool orchestration、stateful agent execution のどこを framework が管理するか。

### 基盤・設計原理 (1973–2022)

- **TensorFlow** — model/training runtime
- **PyTorch** — eager tensor/autograd framework
- **LangChain** — LLM chain/tool orchestration
- **Actor model** — message-driven isolated actors
- **Spring Framework** — enterprise application integration

### 上位 abstraction (2015–2025)

- **Keras** — high-level neural network API
- **Lightning** — PyTorch training structure
- **LangGraph** — stateful graph/agent orchestration
- **AutoGen** — multi-agent runtime
- **Spring AI** — Spring AI integration
- **OpenAI Agents SDK** — agent/tool/handoff runtime

### 同世代の ecosystem (2022–2024)

- **LlamaIndex** — data/RAG framework
- **CrewAI** — role-based multi-agent framework
- **Semantic Kernel** — enterprise AI orchestration

### 枝

- **TensorFlow** ──▶ **Keras**: TensorFlow high-level API として統合
- **PyTorch** ╌╌▶ **Lightning**: training framework layer
- **LangChain** ──▶ **LangGraph**: stateful graph/agent orchestration
- **Actor model** ╌╌▶ **AutoGen**: message-driven multi-agent runtime の設計比較
- **Spring Framework** ──▶ **Spring AI**: Spring idiom の AI integration
- **LangChain** ┈┈▶ **LlamaIndex**: LLM application data/orchestration の同世代
- **Actor model** ┈┈▶ **CrewAI**: multi-agent coordination の同じ問題領域
- **Actor model** ┈┈▶ **OpenAI Agents SDK**: agent handoff/tool execution の同じ問題領域
- **Spring Framework** ┈┈▶ **Semantic Kernel**: enterprise integration の同じ問題領域

### 覚えること

- AI framework という一語で model training と agent orchestration を混ぜない。
- LangGraph は LangChain の stateful workflow/agent branch。Keras は model API、Lightning は training lifecycle の layer。
- agent framework の影響関係は新しく、公式 evidence が不足するため破線が多い。

## GitHub router topic の「単語の家系」

GitHub の router topic は同じ単語を使う異なる分野が混ざる。これは歴史的な血縁図ではなく、誤分類を防ぐための分類家系図。

**中心の問い:** router という名前だけで、Web framework と network product を混同しないようにする。

### 曖昧な検索語 (GitHub Topic)

- **router topic** — 入口

### 意味の分岐 (分類)

- **HTTP request routing**
- **UI / application navigation**
- **Page transition / microfrontend**
- **Network router / firmware**
- **Router security tool**

### HTTP request routing (server)

- **httprouter** — Go HTTP router
- **chi** — Go HTTP router
- **Gorilla Mux** — Go HTTP router
- **Symfony Routing** — PHP routing component
- **path-to-regexp** — path parser
- **uWebSockets** — HTTP/WebSocket runtime

### UI / application navigation (client/mobile)

- **React Router** — React routing/framework
- **Vue Router** — Vue router
- **TanStack Router** — type-safe router
- **UI-Router** — AngularJS state router
- **wouter** — minimal React router
- **ARouter** — Android component routing
- **Voyager** — Compose navigation

### Transition / microfrontend (frontend composition)

- **Barba.js** — page transition
- **swup** — page transition
- **single-spa** — microfrontend

### Network product / security (別カテゴリ)

- **Lantern** — VPN/circumvention application
- **iStoreOS** — router/NAS OS
- **RouterSploit** — embedded router exploitation framework

### 枝

- **router topic** ┈┈▶ **HTTP request routing**: 語の意味を分類
- **router topic** ┈┈▶ **UI / application navigation**: 語の意味を分類
- **router topic** ┈┈▶ **Page transition / microfrontend**: 語の意味を分類
- **router topic** ┈┈▶ **Network router / firmware**: 語の意味を分類
- **router topic** ┈┈▶ **Router security tool**: 語の意味を分類
- **HTTP request routing** ┈┈▶ **httprouter**: HTTP server routing
- **HTTP request routing** ┈┈▶ **chi**: HTTP server routing
- **HTTP request routing** ┈┈▶ **Gorilla Mux**: HTTP server routing
- **HTTP request routing** ┈┈▶ **Symfony Routing**: HTTP server routing
- **HTTP request routing** ┈┈▶ **path-to-regexp**: HTTP server routing
- **HTTP request routing** ┈┈▶ **uWebSockets**: HTTP server routing
- **UI / application navigation** ┈┈▶ **React Router**: application navigation
- **UI / application navigation** ┈┈▶ **Vue Router**: application navigation
- **UI / application navigation** ┈┈▶ **TanStack Router**: application navigation
- **UI / application navigation** ┈┈▶ **UI-Router**: application navigation
- **UI / application navigation** ┈┈▶ **wouter**: application navigation
- **UI / application navigation** ┈┈▶ **ARouter**: application navigation
- **UI / application navigation** ┈┈▶ **Voyager**: application navigation
- **Page transition / microfrontend** ┈┈▶ **Barba.js**: transition / composition
- **Page transition / microfrontend** ┈┈▶ **swup**: transition / composition
- **Page transition / microfrontend** ┈┈▶ **single-spa**: transition / composition
- **Network router / firmware** ┈┈▶ **Lantern**: network product
- **Network router / firmware** ┈┈▶ **iStoreOS**: network product
- **Router security tool** ┈┈▶ **RouterSploit**: security/exploitation tool

### 覚えること

- GitHub Topic は discovery signal であり、分類体系ではない。
- Lantern や iStoreOS は router topic に存在しても Web framework catalog の core には入れない。
- RouterSploit の framework は security exploitation framework で、HTTP routing framework ではない。
