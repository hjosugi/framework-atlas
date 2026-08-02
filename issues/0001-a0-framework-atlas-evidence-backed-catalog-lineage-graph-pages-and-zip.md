# #1 A0 framework atlas: evidence-backed catalog, lineage graph, Pages, and ZIP

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/1
- Updated: 2026-08-02T07:04:16Z

## Metadata
- State: complete
- Tracker role: program
- Repository outcome: public GitHub Pages + reproducible ZIP
- Consumer: https://github.com/hjosugi/kofun-boot/issues/15
- Blocked on: nothing

## Outcome

GitHub Topics と公式資料を、検索可能な framework atlas に変換する。単なるリンク集ではなく、分類・歴史・設計思想・系譜・長所/短所・未解決点・実装対応を、機械検証可能な evidence とともに公開する。

完成時に必ず存在するもの:

1. versioned catalog/schema と source/evidence model
2. `framework` / `web-framework` / `router` と周辺 topic の再収集器
3. topic 誤分類を理由付きで隔離する classifier
4. Spring Boot、FastAPI、Gin、Rails、Laravel、Django、React、Vue の deep profile
5. router、DI、ORM、state management、middleware、runtime の比較
6. official と inference を区別する有向 lineage graph
7. 世代交代 timeline と未解決点 tracker
8. `kgrzybek/modular-monolith-with-ddd` case study と Spring Boot/FastAPI/Gin/kofun-boot 対応表
9. 追加サービス不要の静的 GitHub Pages
10. 生成スクリプト、Issue 原稿、主要データを含む deterministic ZIP + SHA-256
11. CI、Pages、Release、公開 read-back

## Execution lanes

- [x] [E1 #2](https://github.com/hjosugi/framework-atlas/issues/2) data model and evidence
- [x] [E2 #3](https://github.com/hjosugi/framework-atlas/issues/3) topic collection and classification
- [x] [E3 #4](https://github.com/hjosugi/framework-atlas/issues/4) deep profiles, history, and lineage
- [x] [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5) production architecture case study and framework mappings
- [x] [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6) static site and graph UX
- [x] [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7) packaging, CI, publication, and freshness

## Global gates

- [x] すべての fact/edge/metric に source URL、観測日、evidence kind がある。
- [x] official influence と research inference が UI と data の両方で区別される。
- [x] 数値は raw evidence に join するか `unmeasured`。
- [x] topic 誤分類候補は消さず、判定理由付き quarantine に入る。
- [x] generator は同じ入力から byte-identical output を生成する。
- [x] site は JavaScript/CSS/JSON の静的ファイルだけで動作する。
- [x] ZIP は同じ commit から同じ SHA-256 になる。
- [x] Pages、Release asset、ZIP checksum を匿名 read-back する。

## Non-goals

- 星数による総合ランキング
- 根拠のない性能順位
- framework と router/UI/ORM/agent を同じ尺度で順位付け
- framework の再実装
- 広告、認証、外部DB、外部検索サービス
- kofun-boot に着地しない一般技術ニュース
