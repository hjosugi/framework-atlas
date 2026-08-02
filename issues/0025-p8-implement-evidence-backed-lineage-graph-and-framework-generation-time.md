# #25 P8 implement evidence-backed lineage graph and framework generation timeline

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/25
- Updated: 2026-08-02T05:40:31Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E3 #4](https://github.com/hjosugi/framework-atlas/issues/4)
- Blocked on: P1-P7 partial data

## Artifacts
`data/relations.v1.json`、`data/generations.v1.json`、graph/timeline validation fixtures。

## Implementation
公式 influence/build dependency/successor と research inference/competitive similarityを区別した有向graphを作る。世代はCGI/MVC、batteries-included、microframework、type-driven API、edge/multi-runtime、compiled/static contract等のdesign shiftとして表現する。

## Acceptance
- [ ] edgeにfrom/to/type/direction/evidence/confidence。
- [ ] cycleが許可されるrelationと禁止relationを定義。
- [ ] sourceなし official edgeを拒否。
- [ ] generation membershipに根拠/理由。
- [ ] same-year順序を断定しない。
- [ ] graph nodeがcatalogから孤立しない。

## Non-goals
単一の進化直線、古い=悪いという評価。
