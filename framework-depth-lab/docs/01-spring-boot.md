# Spring Boot 4.1.0 deep dive

## Identity

Spring Boot is not a replacement for Spring Framework. It is the bootstrap, dependency management, auto-configuration, packaging, and operations layer that turns the Spring portfolio into a runnable application.

- stable: 4.1.0, released 2026-06-10
- Java: minimum 17, compatible through 26
- Spring Framework: 7.0.8+
- build: Maven 3.6.3+ or Gradle 8.14+/9.x
- embedded Servlet: Tomcat 11.0.x or Jetty 12.1.x, Servlet 6.1
- native image: GraalVM 25+
- license: Apache-2.0

## Problem it solved

Before Boot, Spring offered powerful but separately assembled pieces: an IoC container, MVC, transactions, data access, security, integration, and more. Teams repeatedly chose versions, configured application servers, created XML/Java configuration, and rebuilt production concerns. Boot introduced a curated dependency graph, executable application model, conditional auto-configuration, externalized configuration, and operational endpoints.

Its value is not fewer lines in one controller. Its value is reducing organization-wide variance in how applications start, configure dependencies, expose health, package, and upgrade.

## Historical milestones

| Time | Change | Architectural meaning |
|---|---|---|
| 2012–2013 | project prototype and milestones | convention layer over Spring |
| 2014-04 | 1.0 GA | executable JAR, embedded server, starter/auto-config model became mainstream |
| 2018 | 2.0 | Spring Framework 5, Actuator redesign, reactive stack support |
| 2022 | 3.0 | Java 17, Jakarta namespace, AOT/GraalVM first-class direction |
| 2025 | 4.0 | codebase modularization, JSpecify null-safety work, Java 25 support, API versioning/HTTP service clients |
| 2026-06 | 4.1 | gRPC support, HTTP client SSRF guard, Jackson/observability improvements |

Spring’s official 2014 post describes Phillip Webb and Dave Syer driving Boot from concept through the 2013 prototype to 1.0 GA. This is direct project history, not an inferred Rails clone narrative.

## Bootstrap internals

`SpringApplication.run()` is an orchestrator. The 4.1.0 source describes and implements this broad sequence:

1. determine application type and application context implementation
2. create bootstrap context and application arguments
3. prepare `Environment` and ordered property sources
4. bind `spring.main.*` values back to application settings
5. create and prepare the `ApplicationContext`
6. register sources and bean definitions
7. refresh the context, creating singleton beans and starting the web server
8. invoke runners and publish lifecycle events
9. mark the application ready or perform failure handling

The important boundary is `ApplicationContext.refresh()`: definition discovery turns into an instantiated, post-processed object graph. Many startup surprises are really classpath scanning, bean definition, condition evaluation, proxy generation, or lifecycle callback problems.

## What `@SpringBootApplication` actually does

It composes three concepts:

- `@SpringBootConfiguration`: marks the primary configuration
- `@EnableAutoConfiguration`: imports matching auto-configurations
- `@ComponentScan`: discovers application components below the package

It does not scan JPA entities or Spring Data repositories merely because `scanBasePackages` was changed. Those subsystems have their own discovery rules.

## Auto-configuration algorithm

At a simplified level:

```text
META-INF/spring/...AutoConfiguration.imports
  → candidate class names
  → remove duplicates
  → apply explicit exclusions
  → evaluate class / bean / property / resource / web conditions
  → order selected configurations
  → register bean definitions
  → back off when user beans satisfy the condition
```

`AutoConfigurationImportSelector` in tag `v4.1.0` loads candidates through `ImportCandidates`, removes duplicates and exclusions, filters by conditions, publishes import events, and returns the final list. Auto-configuration is therefore conditional bean-definition generation, not runtime magic on every request.

### Strength

Adding a driver and starter can produce a coherent default configuration with metrics, health, properties, test support, and lifecycle integration.

### Cost

Behavior depends on classpath, environment, bean presence, order, and condition outcome. Debugging needs condition reports, bean graphs, and configuration metadata. A framework improvement should preserve Boot’s convenience while making every default explainable.

## Web request models

### Spring MVC / Servlet

```text
server connector
→ Servlet Filter chain
→ DispatcherServlet
→ HandlerMapping
→ HandlerAdapter
→ argument resolvers / validation
→ controller
→ service / repository
→ message converters
→ response
```

The default concurrency model is a server thread per active request. Java virtual threads can reduce the cost of blocking concurrency, but they do not make slow downstream systems faster or remove the need for connection limits and cancellation.

### Spring WebFlux

```text
Reactor Netty or reactive server
→ WebFilter chain
→ DispatcherHandler
→ reactive HandlerMapping / Adapter
→ Publisher pipeline
→ non-blocking client / driver
→ response with demand and cancellation
```

WebFlux is useful when the whole hot path is non-blocking or when streaming/backpressure matters. Wrapping blocking JPA calls in a reactive controller does not create an end-to-end reactive system.

## Dependency injection

Spring owns an application-wide object graph with scopes, lifecycle, post-processors, qualifiers, proxying, and AOP. Constructor injection should be the default because dependencies become explicit and testable. Field injection hides required dependencies and complicates plain unit tests.

Spring DI is broader than FastAPI `Depends`: it creates long-lived application components and infrastructure. Request/session scopes exist, but most services are singleton beans. Circular references are a design smell; Boot’s current defaults no longer encourage relying on them.

## Data and transactions

Boot auto-configures data technologies but does not define the domain model.

- JPA/Hibernate: unit of work, identity map, dirty checking, lazy relationships
- Spring Data JDBC: simpler aggregate persistence without full ORM behavior
- R2DBC: reactive SQL access; transaction context follows Reactor context rather than a thread-local assumption
- jOOQ: SQL-first, type-safe query generation; Boot 4.1’s supported line requires Java 21+
- MongoDB/Redis/Elasticsearch/etc.: separate consistency and modeling rules

`@Transactional` is usually implemented by a proxy. Self-invocation, wrong visibility, async boundaries, and caught exceptions can invalidate assumptions. Transaction boundary should align with a business consistency boundary, not a controller method by habit.

For modular monoliths, prefer package/module ownership and schema ownership. Spring Modulith can verify module dependencies and support event publication, but it does not discover bounded contexts for the team.

## Production features

- Actuator health, readiness/liveness, metrics, info, environment-safe diagnostics
- Micrometer metrics and tracing façade
- OpenTelemetry integration
- externalized and profile-aware configuration
- structured logging ecosystem
- buildpacks and layered container images
- graceful shutdown and lifecycle events
- SSL bundles, service connections, Docker Compose/Testcontainers development support

Boot 4.1 specifically adds automatic context propagation for `@Async`, more observation conventions, and controls for the OpenTelemetry SDK. Cardinality and sensitive endpoint exposure remain application responsibilities.

## Security

Spring Security is powerful because authentication, authorization, CSRF, session, OAuth2 client/resource server, method security, and filter ordering share one model. It is also easy to misconfigure because multiple filter chains and matcher order change semantics.

Boot 4.1 adds outgoing HTTP client address filtering for SSRF hardening. This is valuable, but application policy must also cover redirects, DNS rebinding assumptions, metadata endpoints, proxy behavior, and egress controls.

Critical review points:

- first matching `SecurityFilterChain`
- public endpoint matcher scope
- CSRF decision for browser-cookie requests
- CORS versus authentication failure behavior
- JWT issuer/audience/algorithm and authority mapping
- Actuator exposure on a separate port or protected network
- trusted proxy and forwarded header strategy

## Testing

Boot’s test advantage is controlled context slicing:

- plain JUnit for domain logic
- `@WebMvcTest` / `@WebFluxTest` for transport adapters
- data slices for mapping/query behavior
- `@SpringBootTest` for full context
- Testcontainers/service connections for real infrastructure
- contract and end-to-end tests outside the JVM boundary
- architecture tests via ArchUnit or Spring Modulith verification

The context cache makes suites fast only when tests reuse the same configuration. Excessive mocks and unique profiles fragment the cache. A test passing with H2 does not prove MySQL/PostgreSQL behavior.

## Spring Boot 4.1 changes that matter

- Spring gRPC server/client and test support, including standalone Netty or Servlet HTTP/2 integration
- common Jackson read/write properties and factory customization
- configurable HTTP client cookie handling
- `InetAddressFilter` for blocking selected outbound addresses
- async observation context propagation and OpenTelemetry controls
- RabbitMQ Streams service connections and SSL
- OAuth2 resource server authority extraction using SpEL expressions
- MongoDB support for Spring Batch, Redis listener auto-configuration
- Log4j size/time/combined/cron rotation strategies
- Spock support restored
- APIs deprecated in 4.0 removed; layertools jar mode removed

## Advantages

- broad, coherent production ecosystem
- strong dependency version management
- diagnostics and operations are first-class
- mature testing and security integrations
- multiple web/data programming models under one application model
- organizational standardization and long-term maintainability

## Costs and failure modes

- startup and memory overhead versus thin frameworks
- implicit behavior from auto-configuration and proxies
- dependency graph and upgrade surface are large
- mixing MVC/WebFlux or blocking/reactive code can create hidden bottlenecks
- `@Transactional`, `@Async`, caching, security method annotations depend on proxy boundaries
- defaults make demos easy but do not replace capacity planning or threat modeling

## Best fit

Choose Boot when integration breadth, governance, observability, security, data, and maintainable conventions matter more than the smallest runtime. Avoid treating it as mandatory for a tiny stateless edge handler whose main value is low footprint and immediate startup.

## Primary sources

- <https://docs.spring.io/spring-boot/4.1/index.html>
- <https://docs.spring.io/spring-boot/4.1/system-requirements.html>
- <https://github.com/spring-projects/spring-boot/releases/tag/v4.1.0>
- <https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.1-Release-Notes>
- <https://github.com/spring-projects/spring-boot/blob/v4.1.0/core/spring-boot/src/main/java/org/springframework/boot/SpringApplication.java>
- <https://github.com/spring-projects/spring-boot/blob/v4.1.0/core/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/AutoConfigurationImportSelector.java>
