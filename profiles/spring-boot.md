# Spring Boot — production opinionを配布するframework

確認日: 2026-08-02。観測version: 4.1.0（GitHub release `v4.1.0`, 2026-06-10）。

## 核心

Spring Bootの価値はHTTP routing単体ではなく、Spring ecosystemとthird-party libraryの選択・設定・運用を「starter、auto-configuration、embedded server、externalized configuration、Actuator」という一続きの体験にすることにある。公式ページはstand-alone application、Tomcat/Jetty/Undertowの組込み、starter依存、auto-configuration、metrics/health、外部設定を主要機能として挙げる。

auto-configurationは魔法ではなく条件付き構成である。classpath、既存bean、propertyなどを条件に候補を適用し、利用者のbeanで置換できる。condition evaluation reportが採否を説明する。したがって再利用すべき設計は「暗黙化」ではなく、(1) opinionの発火条件、(2) user override、(3)適用理由の診断、(4)本番観測を一つのcontractにすることだ。

公式の「通常利用でcode generation不要」という方針と、AOT/native buildが閉世界解析のために生成するartifactは別の局面であり、矛盾として混同しない。Spring FrameworkはDI/Web/data access等の基盤、Bootはその上のapplication opinionである。Spring Data/Security/Cloud/Modulith、Reactor、Micrometerも別project boundaryであり、Boot単独の機能claimへ吸収しない。

## 強みと代償

| 軸 | 強み | 代償 |
|---|---|---|
| start | Initializr/starterと既定値で縦に通る | conditionとclasspathの組合せは大規模化すると追跡が必要 |
| composition | DI containerとextension ecosystem | container lifecycleへの理解が必要 |
| operations | health、metrics、configurationを標準面に含む | endpoint exposureとsecurity policyを別途固定する必要 |
| delivery | executable artifact、embedded server、AOT/native選択 | JVM/nativeで性能・diagnosticの条件が変わる |
| evolution | version mapping、release note、upgrade support | ecosystem-wide compatibility matrixが設計制約になる |

## kofun-bootへの抽出

`starter` は依存の別名ではなく、互換性を検証したcapability bundleとしてadaptする。auto-configuration相当は「必要capabilityが存在し、利用者がoverrideしていないときだけ適用」とし、採用・不採用理由をmachine-readable reportにする。health/metrics/configは後付けpluginではなくboot contractの一部へadaptする。一方、class scanning、reflection container、class inheritanceはrejectし、Kofunの型とmodule宣言から決定的に構成する。

## Sources

- https://spring.io/projects/spring-boot
- https://docs.spring.io/spring-boot/reference/using/auto-configuration.html
- https://docs.spring.io/spring-boot/reference/actuator/index.html
- https://github.com/spring-projects/spring-boot
- https://github.com/spring-projects/spring-boot/releases/tag/v4.1.0
