# Electron

- ID: `electron`
- 分野: `mobile-desktop` / `desktop web runtime framework`
- 言語: JavaScript, TypeScript, C++
- 最初の公開: 2013
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

ChromiumとNode.jsを同梱し、Web技術でWindows/macOS/Linuxのdesktop applicationを構築するframework。

## 何を解決するか

Web teamのskillsとecosystemを再利用し、platform別native UI実装の重複を減らす。

## 歴史・背景

Atom editorのshellとして始まり、VS Code、Slack等のdesktop application modelを普及させた。multi-process browser architectureとsecurity boundaryが中心課題。

## 中核設計

main processがwindowとOS integrationを管理し、renderer processがChromiumでUIを実行する。preloadとcontext isolationで権限境界を作る。

## Data model

application固有。renderer state、main process state、persistent storageをIPC境界で分離する。

## メリット

- Web codeと人材を再利用できる
- cross-platform desktop ecosystemが成熟
- 複雑なWeb UIをdesktopへ持ち込みやすい

## デメリット / trade-off

- memory・disk footprintが大きい
- main/renderer/preloadのsecurity設計が必要
- native UXとの差を調整する必要

## 向いている用途

- cross-platform desktop SaaS client
- Web-first teamのdesktop product

## 避ける条件

- 極小binary・低memory・native control fidelityが最優先

## 実行モデル

- primary abstraction: BrowserWindow、main/renderer process
- control flow: main processがlifecycleを管理しrendererとIPC
- routing: Web routerまたはwindow navigation
- rendering: Chromium DOM
- dependency injection: framework内蔵DIなし
- state: renderer/main processに分離
- concurrency: Chromium multi-process + Node event loop
- deployment: platform別installer/package
- extension: Node modules、native modules、preload APIs
- testing: Playwright/Spectron後継tooling等
- migration cost: 中〜高。Electron APIとsecurity modelに結合

## Official / primary sources

- [Electron official](https://www.electronjs.org/)
- [Electron repository](https://github.com/electron/electron)

## Research gaps

- なし
