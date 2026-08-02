# #36 M10 implement the modular-monolith mapping for kofun-boot

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/36
- Updated: 2026-08-02T05:42:18Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Consumer: https://github.com/hjosugi/kofun-boot/issues/15
- Blocked on: M2-M6 and relevant kofun language lanes

## Artifacts
kofun-boot mapping table、target issue links、contract/gate pseudostructure。

## Implementation
bounded context→module ADT/contract、composition root→capability record、command/query→pure function + closed result、decorators→shell composition、outbox/inbox→typed trace、event sourcing→versioned event ADT、architecture tests→FCIS/import gatesへ変換する。

## Acceptance
- [ ] reflection/container/class inheritanceを持ち込まない。
- [ ] expected failureをexceptionでなくclosed ADTへ。
- [ ] clock/net/db/logをcapability argumentへ。
- [ ] module/event schema driftをproducer gateで拒否。
- [ ] outbox/replay/concurrencyをL4/L6 blockersへ正確にlink。
- [ ] 実装可能部分とlanguage blocked部分を分離。

## Non-goals
kofun-boot側のcode変更、このAtlasでlanguage featureを仮実装。
