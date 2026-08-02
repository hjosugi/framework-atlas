# Interview / design review field guide

## 60秒で比較する

「Spring Bootはapplication platform、FastAPIはtyped API framework、GinはHTTP toolkit寄りです。Spring Bootは広いintegrationと運用標準を買う代わりにcontainer/annotationの暗黙性を受け入れます。FastAPIはtype hintをvalidation・DI・OpenAPIへ再利用しますが、ORMやworker topologyは別途必要です。Ginは`net/http`互換と小さいhot pathが強みで、architectureやDIは利用者が明示します。選定は生のrouter速度ではなく、必要機能を揃えたときの総complexity、SLO、team skill、運用costで行います。」

## 深掘り質問への軸

- request lifecycleをserverからcleanupまで説明できるか。
- sync/async、thread/event loop/goroutineとblocking pointを特定できるか。
- transport/domain/persistence modelを分ける基準は何か。
- transaction boundaryとmodule間consistencyをどう決めるか。
- auto-configuration/DIの失敗をどうdiagnoseするか。
- p99悪化時にframeworkより先に何を測るか。
- authn/authz、proxy trust、input limitをどこへ置くか。
- upgradeとrollback、schema compatibilityをどう運用するか。

## Modular Monolith説明

「単一deployableだからmonolithなのではなく、moduleがdataとpublic contractを所有し、compile/testでdependency directionを守る構造です。transaction内で完結するuse caseは同期、独立性や遅延を許容する連携はOutbox eventを選びます。将来のservice抽出は目標ではなく、ownershipと運用要求が生じたときのoptionです。」

## red flags

- 「FastAPIだから全部async」「Ginだから必ず最速」「Spring Bootだからenterprise-ready」
- router microbenchmarkだけでframeworkを選ぶ
- `request DTO = ORM entity = domain aggregate`を無条件に採用
- message brokerを使えばexactly-onceになると説明
- module間を非同期にすればdecoupledだと断定
- test coverageだけでtest品質を判断
