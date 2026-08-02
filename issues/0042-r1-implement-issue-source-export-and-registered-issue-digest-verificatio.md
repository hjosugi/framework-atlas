# #42 R1 implement issue-source export and registered-issue digest verification

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/42
- Updated: 2026-08-02T07:01:31Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: registered issue set

## Artifacts
`issues/<number>-<slug>.md`, `issues/index.json`, export/check script。

## Implementation
実登録issueのtitle/body/state/parentをsource filesへexportし、normalized body digestを保存する。ZIP内原稿とGitHub上issueのdriftを検出する。

## Acceptance
- [x] issue number/title/body/state/url/digest。
- [x] comment/private metadata/tokenを含めない。
- [x] GitHub read unavailable時はoffline index検証可能。
- [x] body変更をdigest mismatchで検出。
- [x] number順deterministic output。
- [x] 本issue自身を含む全implementation issueを収録。

## Non-goals
Issue自動close、project board。
