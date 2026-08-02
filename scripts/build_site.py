#!/usr/bin/env python3
"""Build both Framework Atlas datasets into one zero-dependency site."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from common import canonical_json, load_json
from validate import validate as validate_v1

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
DOCS_DATA = DOCS / "data"
DOCS_ISSUES = DOCS / "research-issues"
LEGACY_OUTPUT = DOCS / "atlas-data.json"


def load(name: str, default: Any = None) -> Any:
    path = DATA / name
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build() -> dict[str, object]:
    """Build the v1 evidence bundle retained for API compatibility."""
    errors = validate_v1()
    if errors:
        raise ValueError("invalid v1 Atlas data:\n" + "\n".join(errors))
    entities = load_json("data/entities.v1.json")
    profiles: dict[str, str] = {}
    for entity in entities["entities"]:
        profile_doc = entity.get("profileDoc")
        if profile_doc and profile_doc not in profiles:
            profiles[profile_doc] = (ROOT / profile_doc).read_text(encoding="utf-8")
    issue_index_path = ROOT / "issues/index.json"
    issue_index = {"issues": []}
    if issue_index_path.exists():
        issue_index = json.loads(issue_index_path.read_text(encoding="utf-8"))
    source_paths = sorted(
        {
            *ROOT.glob("data/*.json"),
            *ROOT.glob("data/**/*.json"),
            *ROOT.glob("schema/*.json"),
            *ROOT.glob("profiles/*.md"),
        }
    )
    source_digests = {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in source_paths
        if path.is_file()
    }
    return {
        "version": 1,
        "asOf": entities["asOf"],
        "taxonomy": load_json("data/taxonomy.v1.json"),
        "entities": entities["entities"],
        "relations": load_json("data/relations.v1.json")["relations"],
        "claims": load_json("data/claims.v1.json")["claims"],
        "unresolved": load_json("data/unresolved.v1.json")["items"],
        "generations": load_json("data/generations.v1.json")["generations"],
        "caseStudy": load_json("data/case-studies/modular-monolith-ddd.v1.json"),
        "matrices": load_json("data/matrices.v1.json")["matrices"],
        "hostAdapters": load_json("data/host-adapters.v1.json")["adapters"],
        "routerMatrix": load_json("data/router-matrix.v1.json"),
        "profiles": profiles,
        "issues": issue_index.get("issues", []),
        "sourceDigests": source_digests,
    }


def counter(items: list[dict[str, Any]], field: str) -> dict[str, int]:
    values: Counter[str] = Counter()
    for item in items:
        raw = item.get(field, [])
        if not isinstance(raw, list):
            raw = [raw]
        values.update(str(value) for value in raw if value)
    return dict(sorted(values.items(), key=lambda pair: (-pair[1], pair[0].casefold())))


def latest_as_of(frameworks: list[dict[str, Any]]) -> str:
    dates = [
        item.get("verification", {}).get("as_of", "")
        for item in frameworks
        if isinstance(item.get("verification"), dict)
    ]
    return max((value for value in dates if value), default="")


def issue_records() -> list[dict[str, str]]:
    source = ROOT / "research" / "issues"
    if not source.exists():
        return []
    return [
        {"id": path.name.split("-", 1)[0].upper(), "file": path.name}
        for path in sorted(source.glob("*.md"))
    ]


def build_catalog() -> tuple[dict[str, Any], dict[str, Any]]:
    frameworks = load("frameworks.json", [])
    concepts = load("concepts.json", [])
    relations = load("relations.json", [])
    timeline = load("timeline.json", [])
    ecosystems = load("ecosystems.json", [])
    families = load("families.json", [])
    research_gaps = load("research-gaps.json", [])
    stats = {
        "as_of": latest_as_of(frameworks),
        "frameworks": len(frameworks),
        "deep_profiles": sum(1 for item in frameworks if item.get("maturity") == "deep"),
        "standard_profiles": sum(1 for item in frameworks if item.get("maturity") == "standard"),
        "seed_profiles": sum(1 for item in frameworks if item.get("maturity") == "seed"),
        "concepts": len(concepts),
        "relations": len(relations),
        "verified_relations": sum(1 for edge in relations if edge.get("verification") == "verified"),
        "hypothesis_relations": sum(1 for edge in relations if edge.get("verification") != "verified"),
        "families": len(families),
        "timeline_events": len(timeline),
        "ecosystems": len(ecosystems),
        "research_gaps": len(research_gaps),
        "categories": counter(frameworks, "category"),
        "languages": counter(frameworks, "languages"),
        "maturity": counter(frameworks, "maturity"),
        "status": counter(frameworks, "status"),
    }
    atlas = {
        "meta": {
            "title": "Framework Atlas",
            "subtitle_ja": "framework の歴史・設計思想・影響関係を家系図で理解する",
            "as_of": stats["as_of"],
            "coverage_note_ja": (
                "curated profile と topic-derived seed を分離し、未検証候補が確認済み解説を"
                "上書きしない。GitHub Topic は発見用 signal として扱い、taxonomy とは分ける。"
            ),
            "stats": stats,
        },
        "frameworks": frameworks,
        "concepts": concepts,
        "relations": relations,
        "timeline": timeline,
        "ecosystems": ecosystems,
        "families": families,
        "classification_examples": load("classification-examples.json", []),
        "research_gaps": research_gaps,
        "taxonomy": load("taxonomy.json", {}),
        "topics": load("topics.json", []),
        "issue_files": issue_records(),
    }
    return atlas, stats


def write_csv(frameworks: list[dict[str, Any]]) -> None:
    fields = [
        "id", "name", "aliases", "languages", "category", "subcategory", "kind",
        "maturity", "status", "first_release", "license", "organization", "repository",
        "website", "summary_ja", "problem_ja", "tags", "verification_level",
    ]
    for path in (DATA / "frameworks.csv", DOCS_DATA / "frameworks.csv"):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            for item in frameworks:
                row = {field: item.get(field, "") for field in fields}
                row["aliases"] = "|".join(item.get("aliases", []))
                row["languages"] = "|".join(item.get("languages", []))
                row["tags"] = "|".join(item.get("tags", []))
                row["verification_level"] = item.get("verification", {}).get("level", "")
                writer.writerow(row)


def write_outputs() -> tuple[int, int, int]:
    atlas, stats = build_catalog()
    if DOCS_DATA.exists():
        shutil.rmtree(DOCS_DATA)
    DOCS_DATA.mkdir(parents=True)
    compact = json.dumps(atlas, ensure_ascii=False, separators=(",", ":"))
    (DOCS_DATA / "atlas.json").write_text(compact, encoding="utf-8")
    (DOCS_DATA / "atlas.pretty.json").write_text(
        json.dumps(atlas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (DOCS_DATA / "atlas.js").write_text("window.FRAMEWORK_ATLAS=" + compact + ";\n", encoding="utf-8")
    (DOCS_DATA / "families.json").write_text(
        json.dumps(atlas["families"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(atlas["frameworks"])
    (DATA / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if DOCS_ISSUES.exists():
        shutil.rmtree(DOCS_ISSUES)
    DOCS_ISSUES.mkdir(parents=True)
    for record in atlas["issue_files"]:
        shutil.copy2(ROOT / "research" / "issues" / record["file"], DOCS_ISSUES / record["file"])
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    for name in ("METHODOLOGY.md", "README.md"):
        shutil.copy2(ROOT / name, DOCS / name)

    LEGACY_OUTPUT.write_text(canonical_json(build()), encoding="utf-8")
    return len(atlas["frameworks"]), len(atlas["families"]), len(atlas["relations"])


def generated_snapshot() -> dict[str, bytes]:
    paths = [
        DATA / "frameworks.csv", DATA / "stats.json", DOCS / ".nojekyll",
        DOCS / "METHODOLOGY.md", DOCS / "README.md", LEGACY_OUTPUT,
    ]
    for directory in (DOCS_DATA, DOCS_ISSUES):
        if directory.exists():
            paths.extend(path for path in directory.rglob("*") if path.is_file())
    return {
        path.relative_to(ROOT).as_posix(): path.read_bytes()
        for path in sorted(set(paths))
        if path.is_file()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build both Framework Atlas static datasets")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    before = generated_snapshot() if args.check else {}
    frameworks, families, relations = write_outputs()
    if args.check and before != generated_snapshot():
        print("generated site files were stale; run make build", file=sys.stderr)
        return 1
    print(f"built site data: {frameworks} frameworks, {families} families, {relations} relations -> {DOCS_DATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
