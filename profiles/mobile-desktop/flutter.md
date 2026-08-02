# Flutter

- ID: `flutter`
- 分野: `mobile-desktop` / `cross-platform UI application framework`
- 言語: Dart
- 最初の公開: 2018
- status: `active`
- verification: `official-reviewed` / `2026-08-02`

## 一文でいうと

Dart と独自 rendering engine/widget tree で Android、iOS、Web、desktop、embedded UI を共有する cross-platform application framework。

## 何を解決するか

platform ごとに UI codebase と behavior を分けず、高い描画一貫性と hot reload を持つ製品開発を行う。

## 歴史・背景

Google が mobile-first で開発し、2018 年に 1.0。後に Web/desktop を正式対応し、declarative widget framework と独自 renderer の代表になった。

## 中核設計

すべてを Widget として composition し、Element/RenderObject tree が lifecycle と layout/paint を扱う。platform channel で native API に接続する。

## Data model

domain model は Dart object。UI state は StatefulWidget、ChangeNotifier、Riverpod、BLoC 等を選び、永続化は plugin を使う。

## メリット

- 単一 codebase と一貫した UI
- hot reload と豊富な widget
- mobile/desktop/Web の広い target

## デメリット / trade-off

- binary size と engine cost
- platform-native behavior 差の調整
- Dart/Flutter ecosystem への結合

## 向いている用途

- cross-platform consumer/business app
- custom branded UI
- 同一 team で mobile/desktop/Web

## 避ける条件

- platform native control を最大限利用
- 非常に小さい Web widget
- 既存 native codebase の小変更

## 実行モデル

- primary abstraction: Widget tree
- control flow: state change → build → layout/paint
- routing: Navigator/Router packages
- rendering: Skia/Impeller based engine and platform integration
- dependency injection: provider ecosystem
- state: local state、Riverpod/BLoC 等
- concurrency: event loop、isolate
- deployment: mobile binary、Web bundle、desktop app
- extension: plugin、package、platform channel
- testing: widget/golden/integration tests
- migration cost: 高。Dart/widget/rendering model に依存

## Official / primary sources

- [Flutter official](https://flutter.dev/)
- [Flutter repository](https://github.com/flutter/flutter)

## Research gaps

- なし
