# Reproducible benchmark protocol

このdirectoryは結果を捏造せず、同等機能を測るためのprotocolを提供します。3例はmemory storeなので、主scenarioは`GET /healthz`です。DB、auth、loggingを含むapplication benchmarkは別suiteとして追加してください。

## Environment record

実行前に次を `results-template.csv` とPR本文へ記録します。

- commit SHA、framework/runtime/server version
- CPU model/core limit、memory limit、OS/kernel、container runtime
- server command、worker/thread/event-loop設定
- access log、TLS、compression、metricsのon/off
- clientとserverの配置、network latency
- warm-up/measurement duration、virtual users、payload

## Example commands

各serverを同じCPU/memory制限で起動し、base URLを切り替えて実行します。

```bash
k6 run -e BASE_URL=http://127.0.0.1:8080 scenario.js
```

Spring BootはJVM warm-up後のsteady stateに加えてcold startupを別計測します。FastAPIはworker数を記録します。Ginは`GOMAXPROCS`を記録します。

## Pass criteria

- error rate < 0.1%
- response contract一致
- CPU throttle/OOMなし
- 少なくとも5 run、中央値とrangeを報告
- p50/p95/p99、requests/s、CPU、RSSを一緒に評価

## What this does not prove

`/healthz`はrouting/middleware/serializationの比較であり、business applicationの性能を証明しません。framework選定にはDB、remote I/O、validation、auth、telemetryを含む代表workloadが必要です。
