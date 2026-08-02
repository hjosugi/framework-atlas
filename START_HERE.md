# Start Here

## この project の目的

新しい framework を設計したり、既存 framework を改善したりするときに、過去の失敗と設計上の選択を見落とさないための background map です。

## まず行うこと

```bash
make build validate test
make serve
```

ブラウザで `http://localhost:8000` を開きます。

## 読み方

1. 家系図から問題領域を選ぶ
2. 上から下へ世代交代を追う
3. node をクリックして「何を解決したか」を読む
4. 線の理由と evidence state を確認する
5. 比較画面で data model、DI、state、deployment、tradeoff を横に並べる
6. 不明点は `research/issues/` の Issue として調べる

## 新しい framework を考えるときの質問

- framework が制御を反転する範囲はどこか
- library と framework の境界はどこか
- application lifecycle を誰が管理するか
- data model と transaction boundary を誰が所有するか
- runtime reflection と build-time generation のどちらを選ぶか
- server/client、sync/async、local/distributed の境界はどこか
- escape hatch はあるか
- observability、security、migration を後付けにしていないか
- 既存の成功例を継承するのか、制約の変化に対する別解なのか
- 類似性を歴史的 influence と誤認していないか
