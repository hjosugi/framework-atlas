# #46 R5 publish the versioned release ZIP and verify every public surface

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/46
- Updated: 2026-08-02T07:01:38Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: R1-R4

## Artifacts
immutable tag、GitHub Release、ZIP、SHA256SUMS、release evidence manifest。

## Implementation
exact main SHAをtagし、同SHAから生成したZIP/checksumをReleaseへ添付する。repo/source archive/Pages/raw data/release assetsを匿名read-backする。

## Acceptance
- [x] tag SHA = recorded main SHA。
- [x] asset download hash = SHA256SUMS。
- [x] ZIP issue digest = registered issues。
- [x] Pages source digest = release manifest。
- [x] asset size/content-type/URLを記録。
- [x] tag/assetを再作成・forceしない。
- [x] READMEにPages/ZIP/methodology link。

## Non-goals
mutable latest artifact、CI inclusionだけの完了判定。
