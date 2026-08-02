# Textual

- ID: `textual`
- 分野: `tui` / `rapid application development TUI framework`
- 言語: Python
- 最初の公開: 2021
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Python API、reactive state、CSS-like styling、widgets、async event loop で sophisticated な terminal UI を作り、browser delivery にも展開できる RAD framework。

## 何を解決するか

curses の座標・再描画・input 処理を直接管理せず、GUI/Web framework に近い component、layout、event、style model で TUI を構築する。

## 歴史・背景

Rich の terminal rendering ecosystem から発展し、terminal を application platform として扱う。Textual Web、Trogon、snapshot testing など、開発・配布・test を含む組織 ecosystem を形成した。

## 中核設計

App、Screen、Widget、Message、reactive attribute、CSS selector/layout を中心にする。async worker と message pump が UI update を調停する。

## Data model

UI state は reactive descriptor と widget tree。永続化は application が選び、data binding は watch/compose/event で明示する。

## メリット

- Python だけで高機能 TUI
- style/layout/test/devtools が統合
- SSH、terminal、browser delivery の選択

## デメリット / trade-off

- terminal capability 差と remote latency
- Web/native GUI の全機能代替ではない
- event/reactive lifecycle の学習

## 向いている用途

- developer tool、operations console、log/data browser
- SSH で配布する internal app
- Python CLI を UI 化

## 避ける条件

- pixel-perfect native GUI
- screen reader/browser semantics が最優先の public Web
- 単純な一問一答 CLI

## 実行モデル

- primary abstraction: App、Screen、Widget、Message
- control flow: async message pump + reactive updates
- routing: screen stack / command navigation
- rendering: terminal cells または browser bridge
- dependency injection: composition と app services
- state: reactive attributes + widget tree
- concurrency: asyncio workers/messages
- deployment: Python package、SSH、Textual Web/browser
- extension: custom Widget、driver、worker、CSS
- testing: headless pilot と snapshot ecosystem
- migration cost: 中。Textual widget/message model に依存

## Official / primary sources

- [Textual official docs](https://textual.textualize.io/)
- [Textual repository](https://github.com/Textualize/textual)
- [Textualize organization](https://github.com/Textualize)

## Research gaps

- なし
