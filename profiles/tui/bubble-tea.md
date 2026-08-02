# Bubble Tea

- ID: `bubble-tea`
- 分野: `tui` / `Elm Architecture TUI framework`
- 言語: Go
- 最初の公開: 2020
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

The Elm Architecture を Go terminal application に適用し、Model、Update、View と command/message で TUI を構築する framework。

## 何を解決するか

terminal input、state transition、rendering、副作用を一つの可変 loop に混ぜず、testable な state machine として記述する。

## 歴史・背景

Elm の Model-Update-View を terminal に移植し、Lip Gloss、Bubbles など Charm ecosystem とともに Go TUI の代表となった。

## 中核設計

Update は message から新しい model と command を返し、View は model の文字列表現を返す。副作用は Cmd として分離する。

## Data model

immutable に近い Model value が UI state。永続化は command と application layer に分ける。

## メリット

- 単純な unidirectional flow
- Go single binary と相性が良い
- testable な update function

## デメリット / trade-off

- 複雑 UI では message/state が増える
- widget lifecycle は GUI framework より手動
- terminal rendering 制約

## 向いている用途

- CLI dashboard、wizard、developer tool
- Go binary に UI を同梱
- state machine 的 UI

## 避ける条件

- Web DOM/native widget が必要
- 大量 form の自動 binding
- 単純な color output だけ

## 実行モデル

- primary abstraction: Model、Msg、Cmd、Update、View
- control flow: unidirectional event loop
- routing: application-defined model/screen transition
- rendering: ANSI terminal text
- dependency injection: constructor/composition
- state: Model value
- concurrency: Cmd/subscription + goroutine
- deployment: single binary
- extension: Bubbles components、Lip Gloss style
- testing: Update function unit tests
- migration cost: 低〜中。Elm-style architecture は移植可能

## Official / primary sources

- [Bubble Tea repository](https://github.com/charmbracelet/bubbletea)

## Research gaps

- なし
