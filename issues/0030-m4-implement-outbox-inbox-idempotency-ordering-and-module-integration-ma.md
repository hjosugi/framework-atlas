# #30 M4 implement Outbox/Inbox, idempotency, ordering, and module-integration mappings

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/30
- Updated: 2026-08-02T05:42:11Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M1

## Artifacts
integration-event sequence、delivery semantics matrix、failure injection cases。

## Implementation
module間非同期integration、transactional outbox、inbox、background dispatch、at-least-once delivery/processingを抽出し、duplicate/order/poison/retry/recoveryの未解決点を実装仕様にする。

## Acceptance
- [ ] exactly-onceと表現しない。
- [ ] producer transactionとconsumer transactionを分離。
- [ ] idempotency key/processed marker/ordering scopeを必須項目化。
- [ ] crash pointsを列挙し再実行結果を定義。
- [ ] module direct call禁止のbenefit/costを比較。
- [ ] L4 replayとL6 concurrencyへのkofun linkを持つ。

## Non-goals
message broker製品比較、無限retry。
