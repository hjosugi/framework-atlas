# #18 P1 implement the Spring Boot deep profile and Spring ecosystem map

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/18
- Updated: 2026-08-02T05:40:24Z

## Metadata
- State: ready
- Tracker role: bounded implementation
- Parent: [E3 #4](https://github.com/hjosugi/framework-atlas/issues/4)
- Blocked on: D1-D3

## Official inputs
https://spring.io/projects/spring-boot/ and current Spring Boot reference documentation.

## Artifacts
`profiles/spring-boot.md`, entity/claims/relations/unresolved records.

## Implementation
歴史、opinionated starters、auto-configuration conditions、embedded server、externalized config、Actuator/metrics/health、Initializr、AOT/native、Spring Data/Security/Cloud/Modulithとの境界をdeep profile化する。4.1.0観測値は日付/source付き。

## Acceptance
- [ ] Spring FrameworkとBootを別entity。
- [ ] no-code-generationという公式方針とAOT生成物を混同しない。
- [ ] auto-configの利点/不可視性/条件reportを比較。
- [ ] DI、routing、data、reactive、production opsを別dimension。
- [ ] kofun-bootへのadapt/rejectを具体化。
- [ ] 全claimがofficial sourceへjoin。

## Non-goals
Spring全projectのdeep profile、万能評価。
