# #24 P7 implement router-topic lineage and HTTP-vs-client-vs-system-router classification

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/24
- Updated: 2026-08-02T05:40:30Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E3 #4](https://github.com/hjosugi/framework-atlas/issues/4)
- Blocked on: D2, D5, C4

## Mandatory subjects
httprouter、Gin router、chi、gorilla/mux、Hono routers、uWebSockets(.js)、path-to-regexp、Vue Router、TanStack Router、Mithril router、single-spa、UI-Router、wouter、Symfony Routing。

## Artifacts
router profiles、router taxonomy、evidence edges、quarantine boundary。

## Implementation
server HTTP matcher、client navigation/state router、microfrontend orchestrator、path compiler、network/system routerを別cohortへ分類。radix tree、regex compilation、linear matcher、typed search params、nested state等のdesign traitsを記録する。

## Acceptance
- [ ] router topic hitを一律Web router扱いしない。
- [ ] built-on/inspired-byはofficial source必須。
- [ ] deprecated/maintenance状態を観測日付きで保持。
- [ ] matching ambiguity、registration cost、dispatch cost、type safetyを別軸。
- [ ] VPN/OS/exploit候補はquarantine reason付き。
- [ ] kofun static dispatchへの採否をedgeでなくdecision claimにする。

## Non-goals
ルータ性能ranking、network routing product atlas。
