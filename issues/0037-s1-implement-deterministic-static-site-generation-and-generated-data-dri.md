# #37 S1 implement deterministic static-site generation and generated-data drift checks

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/37
- Updated: 2026-08-02T05:43:30Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E5 #6](https://github.com/hjosugi/framework-atlas/issues/6)
- Blocked on: D1 data contract; fixtures can start

## Artifacts
`scripts/build_site.py`, `docs/atlas-data.json`, generated manifests、drift tests。

## Implementation
canonical dataをvalidateし、sorted/minified public JSON、summary counts、profile/source indexesへ生成する。`--check` は生成物を書かずdiffを報告する。

## Acceptance
- [ ] Python標準ライブラリのみ。
- [ ] 同一入力からbyte-identical。
- [ ] invalid/dangling dataで生成前に停止。
- [ ] generated fileにsource schema/data digests。
- [ ] hand editしたdocs dataをCIが拒否。
- [ ] secret/raw snapshotをpublic outputへ含めない。

## Non-goals
UI実装、network fetch。
