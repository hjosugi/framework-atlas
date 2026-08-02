# Methodology

## 1. What counts as a framework

The catalog distinguishes these kinds rather than forcing all projects into one bucket:

- `application-framework`: controls application structure and lifecycle
- `web-framework`: HTTP-oriented application framework
- `ui-framework`: component, rendering, interaction, or state framework
- `meta-framework`: integrates rendering, routing, data loading, build, and deployment
- `test-framework`: controls test discovery, execution, assertions, or fixtures
- `ml-framework`: defines model, training, inference, or pipeline abstractions
- `agent-framework`: orchestrates models, tools, state, and control flow
- `game-framework` / `game-engine`: application framework versus integrated engine
- `runtime`, `library`, `toolkit`, `platform`, `cms`, `router`, `build-system`: adjacent technologies retained for historical context

## 2. Research depth

- `deep`: purpose, origin, design ideas, tradeoffs, relationships, and primary sources are substantially reviewed.
- `standard`: comparison fields are usable, but history or lineage still has gaps.
- `seed`: identity and rough scope are known; it mainly exists to prevent omission and generate research work.

## 3. Evidence grades

- `A`: explicit official or maintainer statement
- `B`: primary design document, paper, or strong repository history
- `C`: reliable secondary source or indirect primary evidence
- `D`: architectural inference only
- `U`: unverified

Historical relationships with grades `D` or `U` are displayed as hypotheses, not facts.

## 4. Topic collection

GitHub topics are discovery signals, not taxonomy. The collector stores raw metadata first and then classifies records as framework candidates, adjacent projects, products, routers, security tools, or topic noise. It supports date-range splitting so a query can be harvested beyond a single search-result window.

## 5. Comparison discipline

Advantages and disadvantages are contextual. The atlas avoids absolute claims such as “fastest” unless a reproducible benchmark and workload are supplied. It compares control model, composition model, runtime cost, tooling, deployment, compatibility, and operational complexity.

## 6. Updating

Every generated artifact records a build date. Raw snapshots are immutable; normalized records can be corrected through pull requests. A source becoming unavailable creates a verification issue rather than silently deleting the claim.
