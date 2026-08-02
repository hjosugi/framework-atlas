# #43 R2 implement reproducible ZIP assembly and SHA-256 manifest

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/43
- Updated: 2026-08-02T05:43:36Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: source artifacts for final content; script can start

## Artifacts
`scripts/build_zip.py`, versioned ZIP、`SHA256SUMS`、content manifest。

## Implementation
sorted paths、fixed timestamp、normalized permissions、defined compressionでZIPを生成する。.git/token/cache/raw unreviewed snapshots/dist self-referenceを除外する。

## Acceptance
- [ ] clean checkoutで二回buildのhash一致。
- [ ] path traversal/symlink/absolute pathなし。
- [ ] schema/data/profiles/site/scripts/tests/issues/licensesを含む。
- [ ] extract後offline validate/build/site smoke。
- [ ] ZIP内manifestのfile hashを照合。
- [ ] artifact名にversion。

## Non-goals
手作業archive、外部storage。
