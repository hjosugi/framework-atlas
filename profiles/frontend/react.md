# React

- ID: `react`
- 分野: `frontend-library` / `component UI library`
- 言語: JavaScript, TypeScript
- 最初の公開: 2013
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

component と declarative rendering で Web と native UI を構築するライブラリ。routing や data layer は別選択に残す。

## 何を解決するか

大規模 UI で DOM 更新手順を直接管理せず、状態から画面を再計算し、独立した component を組み合わせられるようにする。

## 歴史・背景

Facebook 内部で開発され 2013 年に公開。Virtual DOM、one-way data flow、component model を普及させ、Next.js、React Native、Expo、Remix など多数の framework の表示基盤になった。2026 年には Linux Foundation がホストする React Foundation への移行が発表された。

## 中核設計

component は props と state から UI を宣言する。reconciliation が更新差分を扱い、Hooks が stateful logic の再利用単位になる。React 自体は application architecture 全体を固定しない。

## Data model

永続化 model は持たない。server state、form、client state は framework や library に委ねる。React Server Components では server/client 境界が data flow の一部になる。

## メリット

- 巨大な ecosystem と採用市場
- UI を component として合成しやすい
- Web/native/meta-framework に広く接続

## デメリット / trade-off

- アプリ全体の選択肢が多く設計が分散
- 再レンダーと effect の理解が必要
- meta-framework ごとの差が大きい

## 向いている用途

- 複雑な対話型 UI
- 複数 platform で component skill を共有
- Next.js/React Router/Expo を使う製品

## 避ける条件

- JavaScript をほぼ送らない静的ページ
- 最小依存の Web Components だけで十分
- 統合規約を一つの core package に求める

## 実行モデル

- primary abstraction: Component と Hook
- control flow: state/props 変更 → reconciliation → commit
- routing: core には含めず framework/router が担当
- rendering: client、server、native renderer
- dependency injection: Context と composition
- state: local state、context、external store、server state
- concurrency: concurrent rendering と transitions
- deployment: 静的、SSR、streaming、native
- extension: renderer、hooks、framework ecosystem
- testing: Testing Library、framework test stack
- migration cost: 中。JSX/component model は移植可能だが ecosystem API に依存

## Official / primary sources

- [React official](https://react.dev/)
- [React repository](https://github.com/facebook/react)
- [React Foundation announcement](https://react.dev/blog/2026/02/24/the-react-foundation)

## Research gaps

- なし
