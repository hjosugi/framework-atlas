#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import ROOT, canonical_json, load_json


def classify(repository: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    full_name = str(repository.get("fullName") or repository.get("full_name") or "")
    for override in rules.get("exactOverrides", []):
        if full_name.casefold() == override["fullName"].casefold():
            return {
                "classifierVersion": rules["version"], "fullName": full_name,
                "disposition": override["disposition"], "reasonCode": override["reasonCode"],
                "rule": "exact-override", "source": override["source"]
            }
    text = " ".join([
        str(repository.get("description") or ""),
        " ".join(repository.get("topics") or []),
        str(repository.get("name") or "")
    ]).casefold()
    framework_terms = ("web framework", "http framework", "application framework", "ui framework", "router for react", "router for vue")
    ambiguous_terms = ("vpn", "openwrt", "exploit", "nas system", "embedded devices")
    if any(term in text for term in ambiguous_terms):
        return {"classifierVersion": rules["version"], "fullName": full_name, "disposition": "review_required", "reasonCode": "ambiguous-topic", "rule": "ambiguous-keyword"}
    if any(term in text for term in framework_terms):
        return {"classifierVersion": rules["version"], "fullName": full_name, "disposition": "review_required", "reasonCode": "application-framework-api", "rule": "candidate-only-needs-human-review"}
    return {"classifierVersion": rules["version"], "fullName": full_name, "disposition": "review_required", "reasonCode": "ambiguous-topic", "rule": "default-review"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Propose, but never approve, GitHub topic classifications")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = json.loads(args.input.read_text(encoding="utf-8"))
    rules = load_json("data/rules/classification.v1.json")
    repositories = document.get("repositories", document.get("items", []))
    output = {"version": 1, "classifierVersion": rules["version"], "results": [classify(item, rules) for item in repositories]}
    args.output.write_text(canonical_json(output), encoding="utf-8")
    print(f"classified {len(output['results'])} candidates; human review is required for promotion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
