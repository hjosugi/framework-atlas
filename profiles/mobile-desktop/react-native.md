# React Native

- ID: `react-native`
- 分野: `mobile-desktop` / `native mobile UI framework`
- 言語: JavaScript, TypeScript
- 最初の公開: 2015
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

React component model を用い、WebView ではなく platform native view を render する Android/iOS application framework。

## 何を解決するか

Web と mobile で component skill と business logic を共有しつつ、native UI と platform API を利用する。

## 歴史・背景

React の declarative component model を mobile に拡張して 2015 年に公開。bridge architecture から JSI/Fabric/TurboModules を含む new architecture へ移行した。Expo が developer platform と distribution layer を拡張する。

## 中核設計

React reconciler が native renderer を駆動する。native module/component と JavaScript runtime の境界を codegen/JSI で接続する。

## Data model

React state と external store。persistent data は platform storage/SQLite/network library を使う。

## メリット

- React skill と ecosystem の共有
- native UI/SDK への接続
- Expo による開発・build 改善

## デメリット / trade-off

- native build/debug の知識が必要
- platform 差と third-party module compatibility
- upgrade が複数 layer に及ぶ

## 向いている用途

- iOS/Android を同一 product team で開発
- React Web と logic/component pattern を共有
- native module を必要に応じ追加

## 避ける条件

- platform 特有 UI を最大限個別最適化
- 3D/game rendering
- Web only app

## 実行モデル

- primary abstraction: React component rendered to native view
- control flow: React reconciliation + native event
- routing: React Navigation/Expo Router
- rendering: native platform renderer
- dependency injection: React context/composition
- state: React state + ecosystem
- concurrency: JS runtime + native threads
- deployment: App Store/Play Store、Expo services optional
- extension: native module/component、TurboModule
- testing: Jest、Testing Library、E2E
- migration cost: 高。React Native runtime/native modules に依存

## Official / primary sources

- [React Native official](https://reactnative.dev/)
- [React Native repository](https://github.com/facebook/react-native)

## Research gaps

- なし
