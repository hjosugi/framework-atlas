# Modular Monolith with DDD — framework上の本番architecture

確認日: 2026-08-02

このリポジトリはframework製品ではない。ASP.NET/.NET上に、module ownership、tactical DDD、CQRS、cross-cutting decorators、非同期integration、Outbox/Inbox、Event Sourcing、architecture tests、real dependency integration testsをどう積むかを説明する実装事例である。

## load-bearing decisions

1. APIは薄く、command/queryをmoduleへ委譲する。
2. moduleは別schemaとcomposition rootを持ち、他moduleの内部dataへ直接依存しない。
3. command handlerをlogging、validation、unit-of-workでdecorateする。
4. module間はintegration eventで非同期連携し、Outbox/Inboxでat-least-onceを成立させる。
5. Event Sourcingはeventから状態を復元する箇所だけに用い、audit logと区別する。
6. compilerで守れないarchitecture ruleをarchitecture testで固定する。
7. unit、integration、system integration、mutation testが異なる主張を証明する。

## 採用時の注意

この形を全applicationへ機械的に複製しない。module数、eventual consistency、CQRS、Event Sourcingはdomain complexityとquality attributeに対する費用である。最初にmodule ownershipとtransaction boundaryを決め、同期呼出しで十分な箇所までevent busにしない。Outbox/Inboxはexactly-onceを提供しないので、idempotencyと再処理運用が必須である。

具体的なSpring Boot、FastAPI、Gin、Kofun対応は `data/case-studies/modular-monolith-ddd.v1.json` にmachine-readableに収録する。

## Sources

- https://github.com/kgrzybek/modular-monolith-with-ddd
- https://github.com/kgrzybek/modular-monolith-with-ddd/tree/master/docs
