# Data schema

Canonical editorial files live under `data/`.

## `frameworks.json`

Each record represents a framework or an adjacent project retained for context.

| Field | Meaning |
|---|---|
| `id` | Stable lowercase identifier |
| `name`, `aliases` | Display name and known aliases |
| `languages` | Main implementation or authoring languages |
| `category`, `subcategory` | Atlas taxonomy |
| `kind` | framework, library, framework-adjacent, data-framework, etc. |
| `maturity` | `deep`, `standard`, or `seed` research depth |
| `status` | active, maintenance, archived, discontinued, etc. |
| `first_release`, `date_precision` | Origin date and precision |
| `license` | SPDX-like license name when known |
| `repository`, `website` | Canonical public locations |
| `summary_ja`, `problem_ja` | Positioning and problem statement |
| `history_ja`, `design_ja` | Historical background and core design |
| `data_model_ja` | Persistence/state/data model |
| `strengths_ja`, `tradeoffs_ja` | Context-dependent benefits and costs |
| `best_for_ja`, `avoid_when_ja` | Fit guidance |
| architecture fields | routing, DI, state, concurrency, deployment, extension, testing, etc. |
| `sources` | Official or primary source records |
| `verification` | Review level and `as_of` date |
| `research_gaps` | Unresolved questions |

## `concepts.json`

Architecture ideas and standards such as MVC, IoC/DI, Active Record, WSGI, ASGI, Virtual DOM, islands, and actor model. Concepts may be endpoints in relationship graphs.

## `relations.json`

A directed global edge uses `from --type--> to`.

| Field | Meaning |
|---|---|
| `from`, `to` | Framework or concept IDs |
| `type` | built-on, direct-influence, platform-foundation, ecosystem, etc. |
| `label_ja` | Human-readable reason for the edge |
| `confidence` | high, medium, or low |
| `verification` | verified or needs-evidence |
| `evidence_ja` | Optional explanation |
| `source_url` | Primary evidence URL when available |

## `families.json`

Editorial layer for readable family trees. It does not replace the global graph.

- `generations`: top-to-bottom rows
- `nodes`: canonical IDs or local `virtual` classification nodes
- `edges`: verified, hypothesis, or grouping connections
- `takeaways_ja`: what the reader should remember

`verification: grouping` and relation types such as `same-problem` / `classification` explicitly mean that no historical parent-child claim is being made.

## Other files

- `timeline.json`: dated historical events
- `ecosystems.json`: organization/ecosystem groupings
- `classification-examples.json`: GitHub topic classification examples
- `research-gaps.json`: structured Issue backlog
- `stats.json`: generated coverage counts
