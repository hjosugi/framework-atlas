# #29 M3 implement CQRS, command/query, decorator, and cross-cutting-concern mappings

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/29
- Updated: 2026-08-02T07:01:07Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M1

## Artifacts
command/query flow、decorator pipeline、logging/validation/unit-of-work mapping data。

## Implementation
API→module→command/query handler、write domain model、raw-SQL read model、logging/validation/unit-of-work decoratorsをsequence dataへ落とし、direct call/mediator/function pipelineの選択肢を比較する。

## Acceptance
- [x] CQRSを別database必須と誤記しない。
- [x] commandがresultを返すtrade-offを保持。
- [x] mediatorの疎結合とindirection costを対で記録。
- [x] cross-cutting orderとfailure propagationを明示。
- [x] unit-of-workのtransaction/cancellation境界を記録。
- [x] exception型とclosed result型mappingを区別。

## Non-goals
MediatR/Decoratorの一律採用。
