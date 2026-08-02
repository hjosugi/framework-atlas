# Concurrencyとperformance

## execution model

| 対象 | 代表model | 強み | 主な事故 |
|---|---|---|---|
| Spring MVC | request thread / virtual thread | blocking ecosystemと親和 | pool枯渇、ThreadLocal誤用 |
| Spring WebFlux | event loop + reactive pipeline | 高concurrency I/O、backpressure | blocking call混入、debug難度 |
| FastAPI | ASGI event loop + thread pool + workers | async Python ecosystem | event loop blocking、CPU-bound/GIL |
| Gin | goroutine per request (`net/http`) | 軽量・明示的 | shared state race、無制限fan-out |

## framework別の判断

SpringではMVC + virtual threadsがblocking codeを保ちながらconcurrencyを上げる選択肢です。WebFluxはstream/backpressureやnon-blocking end-to-endが必要な場合に選び、速そうという理由だけで混ぜません。JVMはwarm-up後throughputとstartup/RSSを分けて測ります。AOT/native imageはstartupとmemoryを改善し得ますが、reflection/configurationとpeak throughputのtrade-offを再計測します。

FastAPIでは`async def`は待機可能なI/Oに有効です。CPU-bound workはprocess/queueへ逃がします。sync libraryなら普通の`def` endpoint/dependencyとしてthread poolへ任せる方が、async endpoint内で直接呼ぶより安全です。production throughputはworker数、event loop、keep-alive、Pydantic payload、JSON libraryに左右されます。

Gin/Goではgoroutineが安価でもfreeではありません。downstream timeout、`context.Context` cancellation、connection pool、semaphoreでfan-outを制御します。shared map/cacheにはlockまたはownershipを置き、`go test -race`をCIに入れます。

## 公平なbenchmark

比較対象は同じ機能に揃えます。

- 同じOpenAPI、payload size、validation、JSON field
- 同じDBまたはDBなしの2系統
- TLS、access log、metrics、compressionの条件を明記
- 固定CPU/memory、同じhost、同じnetwork
- warm-up、steady-state、cooldownを分離
- p50/p95/p99、throughput、error、CPU、RSS、startup、artifact size
- 5回以上実行し中央値とばらつきを保存

Gin公式router benchmarkの0 allocationはrouterの性質を示す良いmicrobenchmarkですが、application選定の結論にはできません。本ZIPの`benchmarks/`は測定手順を再現可能にし、架空の勝者を作らないため結果欄を空にしています。

## optimization順序

1. trace/profileでbottleneckを特定する。
2. N+1、index、payload、remote call、connection poolを直す。
3. serialization/validation、logging allocationを調整する。
4. runtime/framework tuningを行う。
5. framework交換は移行costと得られるSLO差を比較する。
