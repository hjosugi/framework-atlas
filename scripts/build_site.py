#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from common import ROOT, canonical_json, load_json
from validate import validate

OUTPUT = ROOT / "docs/atlas-data.json"


def build() -> dict[str, object]:
    errors = validate()
    if errors:
        raise ValueError("invalid Atlas data:\n" + "\n".join(errors))
    entities = load_json("data/entities.v1.json")
    relations = load_json("data/relations.v1.json")
    claims = load_json("data/claims.v1.json")
    profiles: dict[str, str] = {}
    for entity in entities["entities"]:
        profile_doc = entity.get("profileDoc")
        if profile_doc and profile_doc not in profiles:
            profiles[profile_doc] = (ROOT / profile_doc).read_text(encoding="utf-8")
    issue_index_path = ROOT / "issues/index.json"
    issue_index = {"issues": []}
    if issue_index_path.exists():
        issue_index = json.loads(issue_index_path.read_text(encoding="utf-8"))
    source_paths = sorted([
        *ROOT.glob("data/*.json"), *ROOT.glob("data/**/*.json"), *ROOT.glob("schema/*.json"), *ROOT.glob("profiles/*.md")
    ])
    source_digests = {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in source_paths if path.is_file()
    }
    return {
        "version": 1,
        "asOf": entities["asOf"],
        "taxonomy": load_json("data/taxonomy.v1.json"),
        "entities": entities["entities"],
        "relations": relations["relations"],
        "claims": claims["claims"],
        "unresolved": load_json("data/unresolved.v1.json")["items"],
        "generations": load_json("data/generations.v1.json")["generations"],
        "caseStudy": load_json("data/case-studies/modular-monolith-ddd.v1.json"),
        "matrices": load_json("data/matrices.v1.json")["matrices"],
        "hostAdapters": load_json("data/host-adapters.v1.json")["adapters"],
        "routerMatrix": load_json("data/router-matrix.v1.json"),
        "profiles": profiles,
        "issues": issue_index.get("issues", []),
        "sourceDigests": source_digests
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the dependency-free static site data")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = canonical_json(build())
    if args.check:
        actual = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if actual != expected:
            print("docs/atlas-data.json is stale; run python3 scripts/build_site.py", file=sys.stderr)
            return 1
        print("site data is current")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
