# Research Method

## Scope

この研究はframework catalog全体のうち、Spring Boot、FastAPI、Ginを詳細profileとして扱います。`kgrzybek/modular-monolith-with-ddd` はframeworkではなくapplication architectureのcase studyです。

## Evidence hierarchy

1. version固定のsource codeとrelease tag
2. official reference documentation / release notes / project blog
3. 対象repositoryのADR、test、benchmark source
4. standard specification
5. 推論。必ず`inferred`と明記

star数、人気、企業採用例は変動しやすく、設計品質の根拠にもならないため中心指標にしません。

## Version pin

| 対象 | Ref | 読んだ代表file |
|---|---|---|
| Spring Boot | `v4.1.0` | `SpringApplication.java`, `SpringBootApplication.java`, `AutoConfigurationImportSelector.java` |
| FastAPI | `0.141.1` | `applications.py`, `routing.py`, `dependencies/utils.py`, `pyproject.toml` |
| Gin | `v1.12.0` | `gin.go`, `context.go`, `tree.go`, `go.mod`, `version.go` |
| Modular Monolith with DDD | `91c8ef24...` | `README.md`, ADR 0002/0004/0009/0010/0012/0014/0015 |

## Comparison axes

- original problem and design philosophy
- abstraction level and ownership boundary
- bootstrap and lifecycle
- routing algorithm and middleware model
- DI / dependency management
- validation, serialization, OpenAPI
- data model, persistence, transaction
- concurrency, cancellation, backpressure
- error model
- security defaults and proxy behavior
- observability and production operations
- testing pyramid and architecture tests
- performance claim and benchmark validity
- extensibility, escape hatches, upgrade risk
- ecosystem coupling and supply-chain surface
- suitability for modular monolith and DDD

## Influence edge policy

`data/influence-edges.csv` のedgeは次に分類します。

- `direct-dependency`: package/sourceとして直接利用
- `official-inspiration`: project authorが明示
- `derived-code`: source headerやlicenseが由来を明示
- `ecosystem-foundation`: frameworkが下位platformに構築される
- `inferred-similarity`: 構造が似るが、影響の明示証拠なし

confidenceは`high / medium / low`。`inferred-similarity`を歴史的事実として描きません。

## Benchmark policy

公平性を保つため、次を固定しない比較結果は採用しません。

- HTTP contract、payload、status、validation rule
- TLS有無、keep-alive、compression
- logging、metrics、error handling
- worker/process/thread設定
- CPU/memory limit、runtime version、architecture
- warm-up、duration、concurrency、connection count
- DBとnetworkの有無

結果はstartup、steady-state throughput、latency distribution、CPU、RSS、allocation、artifact sizeに分解します。

## Known limitations

- 調査環境にはMavenとGo toolchainがなく、Spring BootとGin sampleのcompile/testは実行していません。
- network load testは行っていません。benchmarkは再現可能な計画とscenarioを収録しました。
- GitHub Pages siteはHTML/CSS/JavaScriptの静的検証を行いますが、browser screenshotによるvisual regressionは未実施です。
- project pagesは更新されるため、`data/sources.json`に調査日とtagを保存しました。
