# Gin — 小さいHTTP coreと明示的composition

確認日: 2026-08-02。観測version: 1.12.0（GitHub release, 2026-02-28）。

## 核心

GinはGoのHTTP applicationにrouting、middleware chain、binding/validation、rendering、request contextを提供する。Spring Bootのようなapplication platformではないため、database transaction、configuration、observability、queue、module boundaryは利用者が組み立てる。

これは欠落ではなく境界の選択である。handlerとmiddlewareを明示的に配線し、Goのtoolchain、interface、`context.Context`と組み合わせやすい。一方、`gin.Context`はmutableなrequest scopeであり、domain/use-case層へ渡すとHTTP lifetime、key/value bag、response mutationが内部へ侵入する。request外のgoroutineで利用する場合は公式のcopy規則に従ってread-only copyを使い、より安全には必要値と標準`context.Context`だけを渡す。

middlewareはregistration orderでbefore/after処理とerror propagationが決まる。`request → recovery → trace → auth → binding → HTTP adapter → typed handler → response` をAtlasの推奨data flowとし、server shutdownはaccept停止、request cancellation、owned goroutineのbounded drainを別gateにする。公式README由来の「40 times faster」はmarketing/source claimであり、Atlas measurementには採用しない。

## 強みと代償

| 軸 | 強み | 代償 |
|---|---|---|
| routing | compactで理解しやすいhandler登録 | application contract生成は別設計 |
| concurrency | goroutine/contextと標準tooling | request終了後のcontext利用、cancel、leakを利用者が管理 |
| middleware | 順序をコードで構成 | business ruleが混ざると隠れたpipelineになる |
| operations | logging/metrics libraryを選択可能 | production baselineがprojectごとに割れる |
| deployment | 単一binaryにしやすい | migration、assets、config provenanceは別途必要 |

## kofun-bootへの抽出

Goに学ぶ点はgoroutineの表面的syntaxではなく、cancel伝播、structured lifetime、channel backpressure、race検査を標準の開発体験に含めることだ。HTTP adapterはtyped requestへdecodeした後にpure handlerを呼び、expected failureをclosed resultにし、effect capabilityを明示的に渡す。routerのstatic dispatchはadaptするがmutable ambient contextはrejectする。middleware/interceptor順序は宣言から決定し、順序の破壊試験を置く。

## Sources

- https://gin-gonic.com/en/docs/
- https://gin-gonic.com/en/docs/examples/using-middleware/
- https://gin-gonic.com/en/docs/binding/binding-and-validation/
- https://github.com/gin-gonic/gin
- https://github.com/gin-gonic/gin/releases/tag/v1.12.0
