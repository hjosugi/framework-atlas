# #15 C3 implement deterministic repository normalization, aliases, forks, and deduplication

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/15
- Updated: 2026-08-02T05:39:03Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E2 #3](https://github.com/hjosugi/framework-atlas/issues/3)
- Blocked on: C2, D2

## Artifacts
`scripts/normalize_snapshot.py`、normalization fixtures、candidate output。

## Implementation
owner/name case、renames、fork/source、archived、mirror、複数topic hitをstable candidateへ集約する。raw snapshotは不変、normalized outputは決定的にsort。

## Acceptance
- [ ] 同repoの複数topic hitをsource list付きで一件化。
- [ ] forkをupstreamと混同しない。
- [ ] rename aliasをstable idへ保持。
- [ ] orderの違うraw inputから同一bytes。
- [ ] archivedを削除しない。
- [ ] normalization reasonを追跡可能。

## Non-goals
quality score、deep profile採否。
