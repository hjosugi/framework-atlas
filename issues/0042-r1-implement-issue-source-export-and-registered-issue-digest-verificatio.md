# #42 R1 implement issue-source export and registered-issue digest verification

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/42
- Updated: 2026-08-02T05:43:35Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: registered issue set

## Artifacts
`issues/<number>-<slug>.md`, `issues/index.json`, export/check script。

## Implementation
実登録issueのtitle/body/state/parentをsource filesへexportし、normalized body digestを保存する。ZIP内原稿とGitHub上issueのdriftを検出する。

## Acceptance
- [ ] issue number/title/body/state/url/digest。
- [ ] comment/private metadata/tokenを含めない。
- [ ] GitHub read unavailable時はoffline index検証可能。
- [ ] body変更をdigest mismatchで検出。
- [ ] number順deterministic output。
- [ ] 本issue自身を含む全implementation issueを収録。

## Non-goals
Issue自動close、project board。
