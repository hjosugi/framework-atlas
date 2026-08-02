# #32 M6 implement architecture tests, integration/system tests, mutation tests, C4, and ADR mappings

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/32
- Updated: 2026-08-02T05:42:13Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E4 #5](https://github.com/hjosugi/framework-atlas/issues/5)
- Blocked on: M1

## Artifacts
architecture invariant catalog、test-level matrix、diagram/ADR mapping、CI evidence。

## Implementation
NetArchTest/ArchUnit型のdependency gate、domain unit tests、real DB integration、async system sampling、mutation testing、SUT preparation、C4/ADR/CIをframework-neutral gatesへ変換する。

## Acceptance
- [ ] unit/integration/system/architecture/mutation testを混同しない。
- [ ] polling testにtimeout/observable effect必須。
- [ ] real dependencyとuncontrolled dependencyのtest-double方針を比較。
- [ ] architecture conventionをcompile/gate/reviewのどこで保つか記録。
- [ ] code coverageをtest adequacyと同一視しない。
- [ ] local/CI同一build logicの利点とtooling costを記録。

## Non-goals
特定test frameworkの採用強制。
