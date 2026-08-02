# Cross-framework comparison

## First principle: compare the responsibility boundary

| Axis | Spring Boot 4.1 | FastAPI 0.141.1 | Gin 1.12 |
|---|---|---|---|
| Abstraction | application platform / bootstrap | API microframework | HTTP web framework |
| Runtime base | JVM + Spring Framework | Python + ASGI + Starlette + Pydantic | Go + `net/http` |
| Main metadata | annotations, bean definitions, classpath, properties | type hints, decorators, Pydantic fields, dependencies | methods, structs/tags, explicit handler chain |
| Startup work | large bean/configuration graph | route/dependency/schema construction | route tree construction |
| Request-time work | filter + dispatch + conversion + service graph | ASGI middleware + dependency solve + validation | radix lookup + handler chain + binding as called |
| DI | full application container | request-scoped provider graph | none; explicit wiring |
| OpenAPI | add Springdoc or other integration; not Boot core | built in | external/manual |
| Data | broad auto-configuration portfolio | external | external |
| Security | Spring Security ecosystem | helpers + dependencies | middleware/ecosystem |
| Observability | Actuator + Micrometer + OTel integration | compose instrumentation | compose instrumentation |
| Deploy artifact | executable JAR/image/native image | source/wheel + Python runtime/container | native binary/container |
| Escape hatch | Spring Framework/server APIs | Starlette/ASGI objects | `net/http` directly |

## Capability matrix

Legend: `core` is built into the studied project, `integrated` is officially coordinated, `compose` is intentionally external.

| Capability | Spring Boot | FastAPI | Gin |
|---|---|---|---|
| route declaration | integrated through Spring MVC/WebFlux | core | core |
| request validation | Bean Validation integration | core via Pydantic | core binding + validator dependency |
| response schema filtering | converter/DTO design | core response model | manual |
| dependency injection | Spring core, deeply integrated | core request graph | compose |
| ORM | compose but auto-configured | compose | compose |
| transaction management | integrated | compose | compose |
| health/metrics | core Boot operations integration | compose | compose |
| authn/authz | integrated Spring Security | helpers; verification logic composed | compose middleware |
| background durable jobs | compose via portfolio/products | compose queue | compose queue |
| native/low-startup path | GraalVM/AOT | process tuning/freezing options external | normal Go build |
| architecture boundaries | package/module conventions, Modulith optional | application convention | package/import convention |

## Same concern, different mechanism

### Dependency acquisition

```text
Spring Boot: application context resolves mostly long-lived beans
FastAPI: request dependency graph recursively resolves values/resources
Gin: constructor/closure wiring resolves dependencies before requests
```

Spring maximizes runtime configurability and cross-cutting integration. Gin maximizes compile-time visibility. FastAPI sits between them: providers are ordinary callables, but their request graph is runtime-inspected.

### Validation

```text
Spring: argument resolver → Jackson → Bean Validation
FastAPI: signature/type analysis → Pydantic validation
Gin: handler explicitly calls ShouldBind* → validator tags
```

All three need a separate domain invariant layer. “Field is non-empty” is transport validation; “a meeting must retain at least one host” is domain behavior.

### Middleware / cross-cutting concerns

| Need | Spring Boot | FastAPI | Gin |
|---|---|---|---|
| raw HTTP | Filter / WebFilter | ASGI middleware | HandlerFunc middleware |
| route/controller | HandlerInterceptor / dependency | dependency / custom APIRoute | group/global middleware |
| service method | AOP/proxy/decorator | Python decorator/provider | Go decorator/wrapper |
| transaction | `@Transactional` proxy | explicit unit of work | explicit unit of work |

Use the narrowest layer that owns the semantics. Database transaction middleware around every request is often too broad. Authorization checks may need both transport identity and domain object access.

## Concurrency comparison

| Dimension | Spring MVC | Spring WebFlux | FastAPI | Gin |
|---|---|---|---|---|
| Basic unit | platform/virtual thread | reactive signal pipeline | event-loop task; sync work in pool | goroutine |
| Blocking I/O | natural but consumes concurrency | harmful unless isolated | harmful in `async def` | natural, goroutine blocks but scheduler continues |
| Backpressure | server/stream API dependent | Reactor demand | ASGI streaming/cancellation; limited end-to-end semantics | application/channel/protocol design |
| Multicore | JVM threads/process replicas | event loops + workers | worker processes/replicas | Go scheduler in one process |
| Context propagation | thread-local + Micrometer context | Reactor Context | `contextvars`/request state | `context.Context` + explicit values |
| Main trap | pools larger than downstream capacity | blocking call in event loop | blocking call or per-worker memory | unbounded goroutines/shared state race |

## Data model comparison

| Question | Spring Boot | FastAPI | Gin |
|---|---|---|---|
| Transport DTO | Java record/class + Jackson/validation | Pydantic model | Go struct + tags |
| Domain model | Java/Kotlin object model; independent of Boot | plain Python classes/value types | plain Go packages/types |
| Persistence model | JPA entity/JDBC aggregate/etc. | SQLAlchemy/SQLModel/etc. | sqlc/GORM/Ent/etc. |
| Unit of work | JPA/transaction manager can provide | explicit session/UoW | explicit transaction/UoW |
| Lazy loading risk | high with JPA | depends on ORM | depends on ORM |
| Framework pressure to merge models | annotation convenience | Pydantic/ORM integration convenience | struct tag reuse convenience |

The safe default for complex domains is boundary-specific models with explicit mapping. For simple CRUD, one model may be pragmatic, but document the coupling.

## Operational comparison

Spring Boot spends more framework complexity to give every service a consistent operations surface. FastAPI and Gin spend less runtime/framework complexity but require an internal platform template if many teams must produce consistent health, logs, traces, metrics, auth, and deployment.

This creates an organizational tradeoff:

```text
framework complexity paid once and reused
vs.
application/platform composition repeated or centralized internally
```

Gin’s smaller binary is not automatically cheaper if every team independently rebuilds a production platform. Boot’s broad ecosystem is not automatically better if a service uses only three endpoints and one client.

## Performance comparison without misleading claims

Never place Gin’s router ns/op beside Spring Boot or FastAPI full-request numbers. Use two benchmark layers:

1. mechanism benchmark: route match, validation, serialization separately
2. equal-feature application benchmark: same contract, validation, auth stub, logging, response, runtime limits

Report:

- cold start to readiness
- warm p50/p95/p99
- max sustainable throughput under an error-rate SLO
- CPU/request and RSS at fixed throughput
- allocation/GC behavior
- artifact/container size
- cancellation and overload behavior

## Security responsibility

| Area | Spring Boot | FastAPI | Gin |
|---|---|---|---|
| secure framework | Spring Security exists but must be configured | security scheme helpers, application verifies | application middleware/libraries |
| CSRF/session | first-class | external/Starlette middleware decisions | external/custom |
| JWT resource server | integrated | compose verifier/provider | compose verifier/middleware |
| proxy trust | forwarded-header/server config | ASGI server/proxy config | explicit trusted proxies critical |
| SSRF | Boot 4.1 HTTP client filter support | client/egress policy | client/egress policy |

More built-in security reduces omitted plumbing but increases configuration semantics. Less built-in security gives clarity only when the application actually implements the missing controls.

## Maintainability and upgrades

- Spring Boot: managed BOM reduces version combinatorics; major upgrades can include Jakarta/package, modularization, removed deprecations, and portfolio compatibility work.
- FastAPI: 0.x versioning and fast release cadence require lockfiles, OpenAPI/error contract tests, and dependency compatibility tests.
- Gin: 1.x API is comparatively narrow; Go/compiler baseline and transitive codec/network dependency upgrades still matter.

## Decision questions

1. Is the main complexity HTTP, API schema, or the whole application platform?
2. Which ecosystem must the business logic access?
3. Does the organization already have a paved road for auth/metrics/config/deploy?
4. Is workload I/O-bound, CPU-bound, streaming, or ordinary CRUD?
5. How much runtime reflection/dynamic wiring is acceptable?
6. How will module boundaries be enforced?
7. What is the upgrade and support horizon?
8. Which failure should be easy to diagnose at 03:00?

## Recommendation by architecture

- Enterprise modular monolith: Spring Boot + Modulith/ArchUnit is the shortest standardized path, but FastAPI/Gin can implement it with explicit package rules.
- ML inference API: FastAPI is usually the integration-efficient choice unless model runtime is Go/JVM-native.
- latency-sensitive gateway: Gin or raw `net/http` offers a small hot path; confirm required auth/observability features.
- event-heavy business system: framework choice is secondary to transaction, Outbox, idempotency, broker, and domain boundaries.
