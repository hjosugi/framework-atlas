# #16 C4 implement topic classifier and reason-coded quarantine

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/16
- Updated: 2026-08-02T07:00:42Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E2 #3](https://github.com/hjosugi/framework-atlas/issues/3)
- Blocked on: C3, D2

## Artifacts
classification rules、quarantine dataset、false-positive fixtures。

## Implementation
repo topics/description/language/known overridesからcandidate cohortを提案する。VPN、network router OS、exploit framework、Android navigation等をreason codeでquarantineし、人手reviewなしにincludedへ昇格しない。

## Acceptance
- [x] rulesはdata fileでreview可能。
- [x] exact overrideは理由/source付き。
- [x] ambiguousはincludedでなくreview_required。
- [x] Lantern/RouterSploit/iStoreOS/ARouter fixtureが期待分類。
- [x] false positive/negative fixtureを保持。
- [x] classifier versionをoutputへ記録。

## Non-goals
LLM分類、候補削除、自動architecture判断。
