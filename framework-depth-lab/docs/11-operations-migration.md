# Operations、upgrade、migration

## production checklist

- readinessとlivenessを分ける。readinessに必要なdependencyだけを入れる。
- structured logへtrace/request/user correlationを付け、secretをredactする。
- RED metrics（Rate、Errors、Duration）とresource saturationを収集する。
- graceful shutdown、request drain、job停止、transaction完了をtestする。
- configuration provenanceを説明できるようにし、secretは外部storeへ置く。
- schema migrationはbackward-compatibleなexpand/contract手順にする。

## Spring Boot

Actuator、Micrometer、OpenTelemetry integration、externalized configurationが強みです。minor/major upgradeではSpring Boot dependency BOMに任せ、個別version overrideを減らします。4.x移行はJava、Jakarta namespace、module分割、deprecated API、test sliceを確認し、`spring-boot-properties-migrator`等の診断を一時利用します。native imageは別deployment targetとしてtestします。

## FastAPI

applicationとUvicorn/Gunicorn相当のprocess manager、reverse proxy、worker、health、metricsを一体でrunbook化します。FastAPI、Starlette、Pydantic、AnyIO、HTTPXの互換範囲をlock fileで固定し、Pydantic major migrationはmodel/serializer behaviorをcontract testします。workerを増やすとmemory内stateは共有されないため、cache/job/lockをexternalizeします。

## Gin

single binary、cross compile、小さいcontainerが運用上の利点です。`http.Server`のread/write/idle/header timeout、max header、shutdown contextを明示します。Go/Gin upgradeでは`go.mod`とrelease note、race/fuzz/benchmarkを確認します。global stateを避けるとrolling upgradeとparallel testが容易です。

## Modular Monolithの抽出可能性

moduleを将来serviceへ抽出できる条件は、別assemblyにしたことではなく、data ownership、public contract、idempotent integration、observable failure、独立migrationが成立していることです。in-memory busはsingle processでは簡単ですが、抽出時にdurable brokerへ置換するとdelivery semantics、ordering、backpressure、DLQが新たに現れます。

抽出判断はteam ownership、独立scale、release cadence、fault isolationという運用上の必要性で行います。「microserviceにできるから」は理由として弱いです。
