#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from common import ROOT, load_json


def is_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_fixture_document(document: dict[str, object]) -> list[str]:
    """Validate destructive contract fixtures without reading canonical data."""
    errors: list[str] = []
    if document.get("version") != 1:
        errors.append(f"/version: expected 1, got {document.get('version')!r}")
    kind = document.get("kind")
    record = document.get("record")
    if not isinstance(record, dict):
        return errors + ["/record: expected object"]
    if kind == "entity":
        for field in ("id", "source", "observedAt", "kind"):
            if not record.get(field):
                errors.append(f"/record/{field}: required field is missing")
        if record.get("kind") not in {"framework", "router", "library", "platform", "case-study"}:
            errors.append(f"/record/kind: unknown enum {record.get('kind')}")
        if record.get("source") and not is_url(record.get("source")):
            errors.append("/record/source: must be https URL")
    elif kind == "relation":
        known = set(document.get("knownIds", []))
        for field in ("from", "to"):
            if record.get(field) not in known:
                errors.append(f"/record/{field}: dangling entity {record.get(field)}")
    elif kind == "measurement":
        for field in ("rawEvidence", "method", "environment", "source", "observedAt"):
            if not record.get(field):
                errors.append(f"/record/{field}: required for numeric Atlas measurement")
    else:
        errors.append(f"/kind: unknown fixture kind {kind}")
    return errors


def validate_alias_records(records: list[dict[str, object]], entity_ids: set[str]) -> list[str]:
    errors: list[str] = []
    aliases: set[str] = set()
    targets: dict[str, str] = {}
    for index, record in enumerate(records):
        alias = str(record.get("alias") or "")
        target = str(record.get("target") or "")
        if alias in aliases:
            errors.append(f"/aliases/{index}/alias: duplicate alias {alias}")
        aliases.add(alias)
        if record.get("status") != "unresolved":
            if target not in entity_ids and target not in {str(item.get('alias')) for item in records}:
                errors.append(f"/aliases/{index}/target: dangling entity {target}")
            targets[alias] = target
    for alias in targets:
        seen: set[str] = set()
        current = alias
        while current in targets:
            if current in seen:
                errors.append(f"/aliases: cyclic alias at {current}")
                break
            seen.add(current)
            current = targets[current]
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    taxonomy = load_json("data/taxonomy.v1.json")
    entities_doc = load_json("data/entities.v1.json")
    relations_doc = load_json("data/relations.v1.json")
    claims_doc = load_json("data/claims.v1.json")
    unresolved_doc = load_json("data/unresolved.v1.json")
    generations_doc = load_json("data/generations.v1.json")
    case_doc = load_json("data/case-studies/modular-monolith-ddd.v1.json")
    aliases_doc = load_json("data/aliases.v1.json")
    matrices_doc = load_json("data/matrices.v1.json")
    host_adapters_doc = load_json("data/host-adapters.v1.json")
    router_matrix_doc = load_json("data/router-matrix.v1.json")

    versioned = {
        "data/taxonomy.v1.json": taxonomy,
        "data/entities.v1.json": entities_doc,
        "data/relations.v1.json": relations_doc,
        "data/claims.v1.json": claims_doc,
        "data/unresolved.v1.json": unresolved_doc,
        "data/generations.v1.json": generations_doc,
        "data/aliases.v1.json": aliases_doc,
        "data/matrices.v1.json": matrices_doc,
        "data/host-adapters.v1.json": host_adapters_doc,
        "data/router-matrix.v1.json": router_matrix_doc,
        "data/case-studies/modular-monolith-ddd.v1.json": case_doc
    }
    for path, document in versioned.items():
        if document.get("version") != 1:
            errors.append(f"/{path}/version: expected 1, got {document.get('version')!r}")

    entities = entities_doc.get("entities", [])
    entity_ids: set[str] = set()
    names: set[str] = set()
    allowed_kinds = set(taxonomy["kinds"])
    allowed_profiles = set(taxonomy["profiles"])
    allowed_evidence = set(taxonomy["evidenceKinds"])

    entity_allowed = {
        "id", "name", "kind", "cohort", "language", "launchYear", "profile", "disposition",
        "repository", "homepage", "profileDoc", "summary", "traits", "sources", "observedAt",
        "metrics", "observedVersion", "releaseSource", "quarantineReason", "quarantineReasonCode", "topicHits"
    }
    entity_defaults = entities_doc.get("defaults", {})
    for index, entity in enumerate(entities):
        where = f"/entities/{index}"
        for field in sorted(set(entity) - entity_allowed):
            errors.append(f"{where}/{field}: unknown field")
        required = ("id", "name", "kind", "cohort", "profile", "disposition", "summary", "sources")
        for field in required:
            if not entity.get(field):
                errors.append(f"{where}/{field}: required field is missing")
        entity_id = entity.get("id")
        if entity_id in entity_ids:
            errors.append(f"{where}/id: duplicate id {entity_id}")
        entity_ids.add(entity_id)
        folded_name = str(entity.get("name", "")).casefold()
        if folded_name in names:
            errors.append(f"{where}/name: duplicate name {entity.get('name')}")
        names.add(folded_name)
        if entity.get("kind") not in allowed_kinds:
            errors.append(f"{where}/kind: unknown enum {entity.get('kind')}")
        if entity.get("profile") not in allowed_profiles:
            errors.append(f"{where}/profile: unknown enum {entity.get('profile')}")
        if entity.get("disposition") not in {"included", "adjacent", "quarantined"}:
            errors.append(f"{where}/disposition: unknown enum {entity.get('disposition')}")
        if entity.get("disposition") == "quarantined":
            if not entity.get("quarantineReason"):
                errors.append(f"{where}/quarantineReason: required for quarantined item")
            if not entity.get("quarantineReasonCode"):
                errors.append(f"{where}/quarantineReasonCode: required for quarantined item")
        sources = entity.get("sources", [])
        if not sources or any(not is_url(source) for source in sources):
            errors.append(f"{where}/sources: must be non-empty https URLs")
        if not entity.get("observedAt", entity_defaults.get("observedAt")):
            errors.append(f"{where}/observedAt: required directly or through document defaults")
        if entity.get("evidenceKind", entity_defaults.get("evidenceKind")) not in allowed_evidence:
            errors.append(f"{where}/evidenceKind: required official/primary-code/inference value")
        metrics = entity.get("metrics", entity_defaults.get("metrics", {}))
        if metrics.get("performance") not in {"unmeasured", "measured"}:
            errors.append(f"{where}/metrics/performance: expected measured or unmeasured")
        if entity.get("profile") == "deep" and not entity.get("profileDoc"):
            errors.append(f"{where}/profileDoc: required for deep profile")
        if entity.get("profile") in {"deep", "standard", "seed"} and not is_url(entity.get("repository")):
            errors.append(f"{where}/repository: official https repository is required")
        profile_doc = entity.get("profileDoc")
        if profile_doc and not (ROOT / profile_doc).is_file():
            errors.append(f"{where}/profileDoc: does not exist: {profile_doc}")

    errors.extend(validate_alias_records(aliases_doc.get("aliases", []), entity_ids))

    relation_ids: set[str] = set()
    allowed_relations = set(taxonomy["relations"])
    allowed_confidence = set(taxonomy["confidence"])
    relation_defaults = relations_doc.get("defaults", {})
    for index, relation in enumerate(relations_doc.get("relations", [])):
        where = f"/relations/{index}"
        relation_id = relation.get("id")
        if relation_id in relation_ids:
            errors.append(f"{where}/id: duplicate id {relation_id}")
        relation_ids.add(relation_id)
        if relation.get("from") not in entity_ids:
            errors.append(f"{where}/from: dangling entity {relation.get('from')}")
        targets = int("to" in relation) + int("toExternal" in relation)
        if targets != 1:
            errors.append(f"{where}: exactly one of to/toExternal is required")
        if relation.get("to") and relation["to"] not in entity_ids:
            errors.append(f"{where}/to: dangling entity {relation['to']}")
        if relation.get("type") not in allowed_relations:
            errors.append(f"{where}/type: unknown enum {relation.get('type')}")
        if relation.get("evidenceKind") not in allowed_evidence:
            errors.append(f"{where}/evidenceKind: unknown enum")
        if relation.get("confidence") not in allowed_confidence:
            errors.append(f"{where}/confidence: unknown enum")
        if not is_url(relation.get("source")):
            errors.append(f"{where}/source: must be https URL")
        if not relation.get("observedAt", relation_defaults.get("observedAt")):
            errors.append(f"{where}/observedAt: required directly or through document defaults")

    for relation_type in taxonomy.get("relationCyclePolicy", {}).get("acyclic", []):
        graph: dict[str, list[str]] = {}
        for relation in relations_doc.get("relations", []):
            if relation.get("type") == relation_type and relation.get("to"):
                graph.setdefault(relation["from"], []).append(relation["to"])
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> bool:
            if node in visiting:
                return True
            if node in visited:
                return False
            visiting.add(node)
            if any(visit(target) for target in graph.get(node, [])):
                return True
            visiting.remove(node)
            visited.add(node)
            return False

        if any(visit(node) for node in list(graph)):
            errors.append(f"/relations: cycle is forbidden for {relation_type}")

    claim_ids: set[str] = set()
    claim_defaults = claims_doc.get("defaults", {})
    for index, claim in enumerate(claims_doc.get("claims", [])):
        where = f"/claims/{index}"
        if claim.get("id") in claim_ids:
            errors.append(f"{where}/id: duplicate id {claim.get('id')}")
        claim_ids.add(claim.get("id"))
        if claim.get("entity") not in entity_ids:
            errors.append(f"{where}/entity: dangling entity {claim.get('entity')}")
        if claim.get("evidenceKind") not in allowed_evidence:
            errors.append(f"{where}/evidenceKind: unknown enum")
        if not is_url(claim.get("source")):
            errors.append(f"{where}/source: must be https URL")
        if not claim.get("verified"):
            errors.append(f"{where}/verified: required field is missing")
        for field in ("sourceKind", "claimKind", "revision", "confidence", "reviewDue"):
            if not claim.get(field, claim_defaults.get(field)):
                errors.append(f"{where}/{field}: required directly or through document defaults")
        claim_kind = claim.get("claimKind", claim_defaults.get("claimKind"))
        if claim_kind == "atlas-measurement" and claim.get("metricStatus") != "measured":
            errors.append(f"{where}/metricStatus: Atlas measurement must be measured and joined to raw evidence")
        if claim_kind == "marketing" and claim.get("metricStatus") != "unmeasured":
            errors.append(f"{where}/metricStatus: marketing numeric claim cannot become an Atlas measurement")

    for index, measurement in enumerate(claims_doc.get("measurements", [])):
        where = f"/measurements/{index}"
        for field in ("rawEvidence", "method", "environment", "source", "observedAt"):
            if not measurement.get(field):
                errors.append(f"{where}/{field}: required for Atlas measurement")

    unresolved_ids: set[str] = set()
    for index, item in enumerate(unresolved_doc.get("items", [])):
        where = f"/unresolved/{index}"
        if item.get("id") in unresolved_ids:
            errors.append(f"{where}/id: duplicate id {item.get('id')}")
        unresolved_ids.add(item.get("id"))
        for field in ("ownerEntity", "cohort", "dimension", "question", "options", "tradeoff", "status", "reason", "nextEvidence", "lastReviewed", "resolutionIssue", "profileDoc"):
            if not item.get(field):
                errors.append(f"{where}/{field}: required field is missing")
        if item.get("ownerEntity") not in entity_ids:
            errors.append(f"{where}/ownerEntity: dangling entity {item.get('ownerEntity')}")
        if not is_url(item.get("resolutionIssue")):
            errors.append(f"{where}/resolutionIssue: must be https URL")
        if item.get("profileDoc") and not (ROOT / item["profileDoc"]).is_file():
            errors.append(f"{where}/profileDoc: does not exist")
        if item.get("status") == "resolved" and not item.get("decisionEvidence"):
            errors.append(f"{where}/decisionEvidence: required when resolved")

    generation_ids: set[str] = set()
    for index, generation in enumerate(generations_doc.get("generations", [])):
        where = f"generations[{index}]"
        if generation.get("id") in generation_ids:
            errors.append(f"{where}: duplicate id")
        generation_ids.add(generation.get("id"))
        for entity_id in generation.get("entities", []):
            if entity_id not in entity_ids:
                errors.append(f"{where}: dangling entity {entity_id}")
        if generation.get("from", 0) > generation.get("to", 0):
            errors.append(f"{where}: invalid year range")
        if not is_url(generation.get("source")):
            errors.append(f"{where}/source: generation membership requires an https source")

    pattern_ids: set[str] = set()
    for index, pattern in enumerate(case_doc.get("patterns", [])):
        where = f"case.patterns[{index}]"
        if pattern.get("id") in pattern_ids:
            errors.append(f"{where}: duplicate id")
        pattern_ids.add(pattern.get("id"))
        for field in ("name", "problem", "mechanism", "invariant", "failureMode"):
            if not pattern.get(field):
                errors.append(f"{where}: missing {field}")
    mapping_targets = {mapping.get("target") for mapping in case_doc.get("mappings", [])}
    expected_targets = {"spring-boot", "fastapi", "gin", "kofun-boot"}
    if mapping_targets != expected_targets:
        errors.append(f"case.mappings: expected {sorted(expected_targets)}, got {sorted(mapping_targets)}")
    for index, mapping in enumerate(case_doc.get("mappings", [])):
        for field in ("moduleBoundary", "commandQuery", "effects", "outboxInbox", "eventSourcing", "testing", "warning", "lifecycle", "architectureGate", "implementationIssues", "patternDecisions"):
            if not mapping.get(field):
                errors.append(f"case.mappings[{index}]: missing {field}")
        decisions = {decision.get("pattern"): decision for decision in mapping.get("patternDecisions", [])}
        if set(decisions) != pattern_ids:
            errors.append(f"/case/mappings/{index}/patternDecisions: every pattern requires a decision")
        for decision in decisions.values():
            if decision.get("decision") not in {"adopt", "adapt", "reject"} or not decision.get("reason"):
                errors.append(f"/case/mappings/{index}/patternDecisions: invalid decision or missing reason")

    event_pattern = next((pattern for pattern in case_doc.get("patterns", []) if pattern.get("id") == "event-sourcing"), {})
    if "監査ログ" not in event_pattern.get("invariant", ""):
        errors.append("/case/patterns/event-sourcing/invariant: must distinguish Event Sourcing from audit log")
    source_manifest = case_doc.get("sourceManifest", {})
    if len(source_manifest.get("revision", "")) != 40:
        errors.append("/case/sourceManifest/revision: exact 40-character commit SHA is required")
    for index, pointer in enumerate(source_manifest.get("pointers", [])):
        if pointer.get("pattern") not in pattern_ids or not is_url(pointer.get("url")):
            errors.append(f"/case/sourceManifest/pointers/{index}: pattern and pinned https URL are required")

    matrix_states = set(matrices_doc.get("cellStates", []))
    unresolved_ids = {item["id"] for item in unresolved_doc.get("items", [])}
    for matrix_index, matrix in enumerate(matrices_doc.get("matrices", [])):
        for target in matrix.get("targets", []):
            if target not in entity_ids:
                errors.append(f"/matrices/{matrix_index}/targets: dangling entity {target}")
        for row_index, row in enumerate(matrix.get("rows", [])):
            cells = row.get("cells", {})
            if set(cells) != set(matrix.get("targets", [])):
                errors.append(f"/matrices/{matrix_index}/rows/{row_index}/cells: must cover every target exactly once")
            for target, cell in cells.items():
                if cell.get("state") not in matrix_states:
                    errors.append(f"/matrices/{matrix_index}/rows/{row_index}/cells/{target}/state: unknown enum")
                if not cell.get("strength") or not cell.get("cost"):
                    errors.append(f"/matrices/{matrix_index}/rows/{row_index}/cells/{target}: strength and cost are required")
                for claim_id in cell.get("claimIds", []):
                    if claim_id not in claim_ids:
                        errors.append(f"/matrices/{matrix_index}/rows/{row_index}/cells/{target}/claimIds: dangling claim {claim_id}")
                if cell.get("state") == "claim" and not cell.get("claimIds"):
                    errors.append(f"/matrices/{matrix_index}/rows/{row_index}/cells/{target}: claim state requires claimIds")
                if cell.get("unresolvedId") and cell["unresolvedId"] not in unresolved_ids:
                    errors.append(f"/matrices/{matrix_index}/rows/{row_index}/cells/{target}/unresolvedId: dangling unresolved id")

    for index, adapter in enumerate(host_adapters_doc.get("adapters", [])):
        if adapter.get("entity") not in entity_ids:
            errors.append(f"/host-adapters/{index}/entity: dangling entity")
        if not is_url(adapter.get("source")):
            errors.append(f"/host-adapters/{index}/source: must be https URL")
    for index, router in enumerate(router_matrix_doc.get("routers", [])):
        if router.get("entity") not in entity_ids:
            errors.append(f"/router-matrix/{index}/entity: dangling entity")
        if not is_url(router.get("source")):
            errors.append(f"/router-matrix/{index}/source: must be https URL")

    for schema_path in sorted((ROOT / "schema").glob("*.json")):
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"/schema/{schema_path.name}: unreadable: {exc}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    entities = load_json("data/entities.v1.json")["entities"]
    relations = load_json("data/relations.v1.json")["relations"]
    claims = load_json("data/claims.v1.json")["claims"]
    print(f"validated {len(entities)} entities, {len(relations)} relations, {len(claims)} claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
