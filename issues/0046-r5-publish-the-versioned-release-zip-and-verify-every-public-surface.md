# #46 R5 publish the versioned release ZIP and verify every public surface

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/46
- Updated: 2026-08-02T05:43:39Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: R1-R4

## Artifacts
immutable tag、GitHub Release、ZIP、SHA256SUMS、release evidence manifest。

## Implementation
exact main SHAをtagし、同SHAから生成したZIP/checksumをReleaseへ添付する。repo/source archive/Pages/raw data/release assetsを匿名read-backする。

## Acceptance
- [ ] tag SHA = recorded main SHA。
- [ ] asset download hash = SHA256SUMS。
- [ ] ZIP issue digest = registered issues。
- [ ] Pages source digest = release manifest。
- [ ] asset size/content-type/URLを記録。
- [ ] tag/assetを再作成・forceしない。
- [ ] READMEにPages/ZIP/methodology link。

## Non-goals
mutable latest artifact、CI inclusionだけの完了判定。
