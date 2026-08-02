# #7 E6 release: deterministic ZIP, CI, Pages, issues export, and public verification

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/7
- Updated: 2026-08-02T05:45:15Z

## Metadata
- State: ready
- Tracker role: execution lane
- Parent: [A0 #1](https://github.com/hjosugi/framework-atlas/issues/1)
- Blocked on: E1-E5 artifacts for final release; tooling can start

## Outcome

repository、Pages、Issue原稿、ZIP、Releaseが同じcommitとevidenceに結ばれ、第三者が再生成・検証できる公開経路を実装する。

## Artifacts

- deterministic `scripts/build_zip.py`
- `dist/framework-atlas-v<version>.zip`
- `dist/SHA256SUMS`
- issue export under `issues/`
- CI workflow: validate → test → generate → drift check → zip reproducibility
- GitHub Pages configuration
- release evidence manifest

## ZIP contents

schema、主要data、profiles、case study、site source/generated site、collection/generation scripts、offline fixtures、Issue原稿、README、licenses。token、raw auth、cache、unreviewed dumpsは除外。

## Gates

- [ ] path順、timestamp、permissionsを固定し二回buildのSHA-256一致。
- [ ] ZIP展開後にoffline validate/build/site smokeが通る。
- [ ] Issue原稿と実登録issueのtitle/body digestを照合。
- [ ] tag/release/main SHAをmanifestへ固定。
- [ ] Pages endpoint、raw data、source ZIP、release ZIP、checksumを匿名HTTP read-back。
- [ ] asset size/content-type/hashを記録。
- [ ] scheduled freshnessはreview artifactのみを生成し、判断/dataを自動上書きしない。

## Non-goals

外部artifact storage、private release、mutable tag、手作業ZIP、CI greenだけで公開完了とみなすこと。

## Children

- [ ] [#42](https://github.com/hjosugi/framework-atlas/issues/42) R1 issue export/digests
- [ ] [#43](https://github.com/hjosugi/framework-atlas/issues/43) R2 reproducible ZIP
- [ ] [#44](https://github.com/hjosugi/framework-atlas/issues/44) R3 CI gates
- [ ] [#45](https://github.com/hjosugi/framework-atlas/issues/45) R4 GitHub Pages
- [ ] [#46](https://github.com/hjosugi/framework-atlas/issues/46) R5 release/public verification
- [ ] [#47](https://github.com/hjosugi/framework-atlas/issues/47) R6 scheduled freshness
