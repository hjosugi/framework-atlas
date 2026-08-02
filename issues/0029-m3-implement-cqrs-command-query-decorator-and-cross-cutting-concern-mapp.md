# #29 M3 implement CQRS, command/query, decorator, and cross-cutting-concern mappings

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/29
- Updated: 2026-08-02T05:42:10Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M1

## Artifacts
command/query flow、decorator pipeline、logging/validation/unit-of-work mapping data。

## Implementation
API→module→command/query handler、write domain model、raw-SQL read model、logging/validation/unit-of-work decoratorsをsequence dataへ落とし、direct call/mediator/function pipelineの選択肢を比較する。

## Acceptance
- [ ] CQRSを別database必須と誤記しない。
- [ ] commandがresultを返すtrade-offを保持。
- [ ] mediatorの疎結合とindirection costを対で記録。
- [ ] cross-cutting orderとfailure propagationを明示。
- [ ] unit-of-workのtransaction/cancellation境界を記録。
- [ ] exception型とclosed result型mappingを区別。

## Non-goals
MediatR/Decoratorの一律採用。
