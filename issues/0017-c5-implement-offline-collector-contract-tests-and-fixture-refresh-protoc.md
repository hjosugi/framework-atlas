# #17 C5 implement offline collector contract tests and fixture refresh protocol

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/17
- Updated: 2026-08-02T05:39:05Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E2 #3](https://github.com/hjosugi/framework-atlas/issues/3)
- Blocked on: C1-C4

## Artifacts
GitHub API response fixtures、unittest suite、fixture provenance manifest。

## Implementation
pagination、split、rate limit、rename、fork、partial、quarantineをnetworkなしで再現する。fixture refreshは明示commandでのみ行い、source date/digestを更新する。

## Acceptance
- [ ] CIはGitHub APIを呼ばない。
- [ ] 各failure modeに一fixture。
- [ ] fixtureにtoken/user private dataなし。
- [ ] refresh前後diffがreview可能。
- [ ] malformed API responseをtyped errorとして拒否。
- [ ] test順に依存しない。

## Non-goals
live API integrationをCI必須にすること。
