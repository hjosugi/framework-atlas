# Tauri

- ID: `tauri`
- 分野: `mobile-desktop` / `webview desktop/mobile application framework`
- 言語: Rust, JavaScript, TypeScript
- 最初の公開: 2022
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

system WebView と Rust backend を組み合わせ、Web frontend skill で小型・権限制御可能な desktop/mobile application を作る framework。

## 何を解決するか

Electron の bundled browser と Node runtime による size/memory cost を抑えつつ、cross-platform desktop app と native capability を提供する。

## 歴史・背景

WebView + Rust security boundary を中核に成長し、1.0 以降 desktop、2.x 世代で mobile/capability model を拡張した。

## 中核設計

frontend は任意 Web framework、backend command/plugin は Rust。capability/permission configuration が native API access を制限する。

## Data model

frontend state と Rust application state を command/event で接続。DB は plugin/Rust crate/Web API を選ぶ。

## メリット

- 小さい配布物と system WebView 利用
- Rust backend と明示的 capability
- frontend framework を選べる

## デメリット / trade-off

- OS WebView 差
- Rust/JavaScript 境界の設計
- 高度 native UI は別実装

## 向いている用途

- developer tool、business desktop app
- Web UI と native filesystem/process access
- Electron footprint を減らす

## 避ける条件

- 完全 native widget UI
- 同一 browser engine 表示が絶対条件
- 既存 Node native module を大量利用

## 実行モデル

- primary abstraction: WebView window、Rust command、capability
- control flow: frontend IPC → Rust command/event
- routing: frontend framework に委譲
- rendering: system WebView
- dependency injection: Rust state management/composition
- state: frontend state + managed Rust state
- concurrency: async Rust + WebView event loop
- deployment: signed desktop/mobile bundle
- extension: Rust/JS plugin
- testing: unit + Web/E2E/platform tests
- migration cost: 中。Web frontend は移植しやすいが Tauri IPC に依存

## Official / primary sources

- [Tauri official](https://tauri.app/)
- [Tauri repository](https://github.com/tauri-apps/tauri)

## Research gaps

- なし
