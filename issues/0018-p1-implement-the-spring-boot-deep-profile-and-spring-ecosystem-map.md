# #18 P1 implement the Spring Boot deep profile and Spring ecosystem map

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/18
- Updated: 2026-08-02T07:00:47Z

## Metadata
- State: complete
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
- [x] Spring FrameworkとBootを別entity。
- [x] no-code-generationという公式方針とAOT生成物を混同しない。
- [x] auto-configの利点/不可視性/条件reportを比較。
- [x] DI、routing、data、reactive、production opsを別dimension。
- [x] kofun-bootへのadapt/rejectを具体化。
- [x] 全claimがofficial sourceへjoin。

## Non-goals
Spring全projectのdeep profile、万能評価。
