# #8 D1 implement atlas-v1 JSON schemas and offline validator

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/8
- Updated: 2026-08-02T05:38:53Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E1 #2](https://github.com/hjosugi/framework-atlas/issues/2)
- Blocked on: nothing

## Artifacts
`schema/*.json`, `scripts/validate.py`, valid/invalid fixtures.

## Implementation
entity、relation、claim、unresolved、taxonomy、snapshot manifest の v1 schema と、Python標準ライブラリだけのvalidatorを実装する。JSON Schema draft名を宣言しつつ、CIで必要なcross-file整合性もvalidatorで検査する。

## Acceptance
- [ ] 欠落id/source/observed_at、unknown enum、dangling idを個別fixtureで拒否。
- [ ] errorはJSON pointerとreasonを出す。
- [ ] schema version mismatchを拒否。
- [ ] valid fixtureを二回normalizeしてbyte-identical。
- [ ] network不要。

## Non-goals
catalog内容、UI、GitHub API。
