#!/usr/bin/env python3
"""Merge machine-discovered GitHub repositories as seed records.

Curated `deep` and `standard` profiles are authoritative. This script never
replaces them. It only refreshes previously generated seed records or appends
new seed records that pass the selected classification policy.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

CATEGORY_MAP = {
    "core-framework": "application-framework",
    "ecosystem-component": "router",
    "security-framework": "security-framework",
    "network-product": "network-product",
    "application": "application-framework",
    "candidate": "application-framework",
}

KIND_MAP = {
    "core-framework": "framework",
    "ecosystem-component": "component",
    "security-framework": "framework",
    "network-product": "product",
    "application": "application",
    "candidate": "candidate",
}


def slugify(value: str) -> str:
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "repository"


def homepage(repo: dict) -> str:
    value = str(repo.get("homepage") or "").strip()
    if value:
        parsed = urlparse(value)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return value
    return str(repo.get("html_url") or "")


def seed_from_repo(repo: dict, existing_ids: set[str]) -> dict:
    full_name = str(repo.get("full_name") or repo.get("name") or "repository")
    base = f"github-{slugify(full_name)}"
    item_id = base
    suffix = 2
    while item_id in existing_ids:
        item_id = f"{base}-{suffix}"
        suffix += 1
    existing_ids.add(item_id)

    classification = str(repo.get("classification") or "candidate")
    language = str(repo.get("language") or "Unknown")
    description = str(repo.get("description") or "GitHub Topic から発見された未検証候補。")
    topics = [str(value) for value in repo.get("topics", [])]
    source_topics = [str(value) for value in repo.get("source_topics", [])]
    summary = description if description.endswith(("。", ".", "!", "?")) else description + "。"
    return {
        "id": item_id,
        "name": str(repo.get("name") or full_name.split("/")[-1]),
        "aliases": [full_name],
        "languages": [language] if language and language != "Unknown" else ["Unknown"],
        "category": CATEGORY_MAP.get(classification, "application-framework"),
        "subcategory": f"topic-derived {classification}",
        "kind": KIND_MAP.get(classification, "candidate"),
        "maturity": "seed",
        "status": "archived" if repo.get("archived") else "unknown",
        "first_release": (str(repo.get("created_at") or "")[:4] or "unknown"),
        "date_precision": "year",
        "license": str(repo.get("license_spdx") or "NOASSERTION"),
        "organization": str(repo.get("owner") or ""),
        "repository": str(repo.get("html_url") or ""),
        "website": homepage(repo),
        "summary_ja": summary,
        "problem_ja": "分類、設計目的、歴史、現在の保守状況を一次資料で確認する必要がある。",
        "history_ja": "GitHub Topic collector により発見。未検証のため歴史的主張は記録していない。",
        "design_ja": "",
        "data_model_ja": "",
        "strengths_ja": [],
        "tradeoffs_ja": [],
        "best_for_ja": [],
        "avoid_when_ja": [],
        "primary_abstraction_ja": "",
        "control_flow_ja": "",
        "rendering_ja": "",
        "routing_ja": "",
        "dependency_injection_ja": "",
        "state_model_ja": "",
        "concurrency_ja": "",
        "deployment_ja": "",
        "extension_model_ja": "",
        "testing_ja": "",
        "migration_cost_ja": "",
        "tags": sorted(set(topics + source_topics + [classification, "topic-derived"])),
        "ecosystem": [],
        "sources": [{
            "label": "GitHub repository",
            "url": str(repo.get("html_url") or ""),
            "kind": "discovery",
        }],
        "verification": {
            "level": "machine-classified",
            "as_of": str(repo.get("updated_at") or "")[:10],
            "confidence": repo.get("classification_confidence"),
            "reason": repo.get("classification_reason"),
            "github_id": repo.get("github_id"),
        },
        "history_events": [],
        "research_gaps": ["manual-classification", "history-evidence"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=Path("data/discovered/github-topics.json"))
    parser.add_argument("--catalog", type=Path, default=Path("data/frameworks.json"))
    parser.add_argument("--include", default="core-framework,ecosystem-component,security-framework")
    parser.add_argument("--min-confidence", type=float, default=0.60)
    parser.add_argument("--include-network-products", action="store_true")
    parser.add_argument("--max-new", type=int, default=0, help="0 means unlimited")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    snapshot_path = args.snapshot if args.snapshot.is_absolute() else ROOT / args.snapshot
    catalog_path = args.catalog if args.catalog.is_absolute() else ROOT / args.catalog
    if not snapshot_path.exists():
        print(f"snapshot does not exist: {snapshot_path}")
        return 0

    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    frameworks = json.loads(catalog_path.read_text(encoding="utf-8"))
    include = {value.strip() for value in args.include.split(",") if value.strip()}
    if args.include_network_products:
        include.add("network-product")

    by_repo = {str(item.get("repository", "")).rstrip("/").lower(): item for item in frameworks if item.get("repository")}
    by_github_id = {
        str(item.get("verification", {}).get("github_id")): item
        for item in frameworks
        if item.get("verification", {}).get("github_id") is not None
    }
    existing_ids = {item["id"] for item in frameworks}
    added = refreshed = skipped = 0

    candidates = sorted(snapshot.get("repositories", []), key=lambda item: (-int(item.get("stars", 0)), str(item.get("full_name", ""))))
    for repo in candidates:
        classification = str(repo.get("classification") or "candidate")
        confidence = float(repo.get("classification_confidence") or 0)
        if classification not in include or confidence < args.min_confidence:
            skipped += 1
            continue
        url_key = str(repo.get("html_url") or "").rstrip("/").lower()
        github_id = str(repo.get("github_id"))
        existing = by_github_id.get(github_id) or by_repo.get(url_key)
        if existing:
            # Never overwrite curated profiles. Seed refreshes are intentionally narrow.
            if existing.get("maturity") == "seed" and existing.get("verification", {}).get("level") == "machine-classified":
                existing["status"] = "archived" if repo.get("archived") else "unknown"
                existing["license"] = str(repo.get("license_spdx") or existing.get("license") or "NOASSERTION")
                existing["tags"] = sorted(set(existing.get("tags", [])) | set(repo.get("topics", [])) | set(repo.get("source_topics", [])))
                existing["verification"].update({
                    "as_of": str(repo.get("updated_at") or "")[:10],
                    "confidence": confidence,
                    "reason": repo.get("classification_reason"),
                    "github_id": repo.get("github_id"),
                })
                refreshed += 1
            else:
                skipped += 1
            continue
        if args.max_new and added >= args.max_new:
            break
        seed = seed_from_repo(repo, existing_ids)
        frameworks.append(seed)
        by_repo[url_key] = seed
        by_github_id[github_id] = seed
        added += 1

    frameworks.sort(key=lambda item: (item.get("category", ""), item.get("name", "").casefold(), item.get("id", "")))
    print(f"merge result: added={added}, refreshed={refreshed}, skipped={skipped}, total={len(frameworks)}")
    if not args.dry_run:
        temp = catalog_path.with_suffix(catalog_path.suffix + ".tmp")
        temp.write_text(json.dumps(frameworks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(catalog_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
