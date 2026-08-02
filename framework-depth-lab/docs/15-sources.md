# Sources

調査基準日: 2026-08-02。version、requirement、機能は一次情報を優先し、source codeはtag/commitを固定しました。URLの機械可読版は `data/sources.json` です。

## Spring Boot

- [Spring Boot project page](https://spring.io/projects/spring-boot)
- [Spring Boot system requirements](https://docs.spring.io/spring-boot/system-requirements.html)
- [Spring Boot reference documentation](https://docs.spring.io/spring-boot/reference/)
- [Spring Boot 4.1 release notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.1-Release-Notes)
- [Spring Boot 4.0 release notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Release-Notes)
- [Spring Boot v4.1.0 tag](https://github.com/spring-projects/spring-boot/tree/v4.1.0)
- [`SpringApplication.java` at v4.1.0](https://github.com/spring-projects/spring-boot/blob/v4.1.0/core/spring-boot/src/main/java/org/springframework/boot/SpringApplication.java)
- [`AutoConfigurationImportSelector.java` at v4.1.0](https://github.com/spring-projects/spring-boot/blob/v4.1.0/core/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/AutoConfigurationImportSelector.java)
- [Spring Boot history](https://spring.io/blog/2014/04/01/spring-boot-1-0-ga-released/)

## FastAPI

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/)
- [FastAPI alternatives, inspiration and comparisons](https://fastapi.tiangolo.com/alternatives/)
- [FastAPI async guidance](https://fastapi.tiangolo.com/async/)
- [FastAPI dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
- [FastAPI deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/)
- [FastAPI 0.141.1 tag](https://github.com/fastapi/fastapi/tree/0.141.1)
- [`applications.py` at 0.141.1](https://github.com/fastapi/fastapi/blob/0.141.1/fastapi/applications.py)
- [`dependencies/utils.py` at 0.141.1](https://github.com/fastapi/fastapi/blob/0.141.1/fastapi/dependencies/utils.py)
- [`pyproject.toml` at 0.141.1](https://github.com/fastapi/fastapi/blob/0.141.1/pyproject.toml)

## Gin

- [Gin documentation](https://gin-gonic.com/en/docs/)
- [Gin 1.12.0 release announcement](https://gin-gonic.com/en/blog/releases/release1120/)
- [Gin performance documentation](https://gin-gonic.com/en/docs/benchmarks/)
- [Gin security best practices](https://gin-gonic.com/en/docs/security-best-practices/)
- [Gin v1.12.0 tag](https://github.com/gin-gonic/gin/tree/v1.12.0)
- [`gin.go` at v1.12.0](https://github.com/gin-gonic/gin/blob/v1.12.0/gin.go)
- [`context.go` at v1.12.0](https://github.com/gin-gonic/gin/blob/v1.12.0/context.go)
- [`tree.go` at v1.12.0](https://github.com/gin-gonic/gin/blob/v1.12.0/tree.go)
- [`version.go` at v1.12.0](https://github.com/gin-gonic/gin/blob/v1.12.0/version.go)

## Modular Monolith with DDD

- [Repository](https://github.com/kgrzybek/modular-monolith-with-ddd)
- [Pinned commit](https://github.com/kgrzybek/modular-monolith-with-ddd/tree/91c8ef24b4cb6ef558c95d8267fa07d68c7059f8)
- [Architecture Decision Log](https://github.com/kgrzybek/modular-monolith-with-ddd/tree/91c8ef24b4cb6ef558c95d8267fa07d68c7059f8/docs/architecture-decision-log)
- [ADR 0002: Modular Monolith](https://github.com/kgrzybek/modular-monolith-with-ddd/blob/91c8ef24b4cb6ef558c95d8267fa07d68c7059f8/docs/architecture-decision-log/0002-modular-monolith.md)
- [ADR 0009: CQRS read model](https://github.com/kgrzybek/modular-monolith-with-ddd/blob/91c8ef24b4cb6ef558c95d8267fa07d68c7059f8/docs/architecture-decision-log/0009-use-cqrs.md)
- [ADR 0014: Modules communicate asynchronously](https://github.com/kgrzybek/modular-monolith-with-ddd/blob/91c8ef24b4cb6ef558c95d8267fa07d68c7059f8/docs/architecture-decision-log/0014-modules-communicate-asynchronously.md)
- [ADR 0015: In-memory event bus](https://github.com/kgrzybek/modular-monolith-with-ddd/blob/91c8ef24b4cb6ef558c95d8267fa07d68c7059f8/docs/architecture-decision-log/0015-in-memory-event-bus.md)

## Runtime and security lifecycle

- [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)
- [IdentityServer4 archived repository](https://github.com/DuendeArchive/IdentityServer4)
- [OAuth 2.1 draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)

## Interpretation policy

release dateやversionは上記の公式release/tagを根拠にしています。性能値は条件付きの測定結果であり、一般化しません。影響関係は公式説明またはsource headerがあるものだけを強いedgeとし、類似だけの場合は`inferred-similarity`として明示します。
