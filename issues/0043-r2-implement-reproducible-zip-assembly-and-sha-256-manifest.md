# #43 R2 implement reproducible ZIP assembly and SHA-256 manifest

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/43
- Updated: 2026-08-02T07:01:33Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: source artifacts for final content; script can start

## Artifacts
`scripts/build_zip.py`, versioned ZIP、`SHA256SUMS`、content manifest。

## Implementation
sorted paths、fixed timestamp、normalized permissions、defined compressionでZIPを生成する。.git/token/cache/raw unreviewed snapshots/dist self-referenceを除外する。

## Acceptance
- [x] clean checkoutで二回buildのhash一致。
- [x] path traversal/symlink/absolute pathなし。
- [x] schema/data/profiles/site/scripts/tests/issues/licensesを含む。
- [x] extract後offline validate/build/site smoke。
- [x] ZIP内manifestのfile hashを照合。
- [x] artifact名にversion。

## Non-goals
手作業archive、外部storage。
