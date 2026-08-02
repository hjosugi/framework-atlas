#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import canonical_json


def normalize(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        identity = str(item.get("node_id") or item.get("id") or item.get("full_name", "").casefold())
        if not identity:
            continue
        grouped.setdefault(identity, []).append(item)
    normalized: list[dict[str, Any]] = []
    for identity, rows in grouped.items():
        ordered = sorted(rows, key=lambda row: (str(row.get("updated_at") or ""), str(row.get("full_name") or "").casefold()))
        item = ordered[-1]
        aliases = sorted({str(row.get("full_name")) for row in rows if row.get("full_name") and row.get("full_name") != item.get("full_name")})
        topics = sorted({topic for row in rows for topic in (row.get("topics") or [])})
        topic_sources = sorted({str(row.get("snapshotTopic")) for row in rows if row.get("snapshotTopic")})
        reasons = ["deduplicated-by-node-id"] if len(rows) > 1 else ["canonical-node-id"]
        if aliases:
            reasons.append("rename-alias-preserved")
        record = {
            "identity": identity,
            "name": item.get("name"),
            "fullName": item.get("full_name"),
            "url": item.get("html_url"),
            "description": item.get("description"),
            "createdAt": item.get("created_at"),
            "updatedAt": item.get("updated_at"),
            "language": item.get("language"),
            "topics": topics,
            "topicSources": topic_sources,
            "isFork": any(bool(row.get("fork")) for row in rows),
            "archived": bool(item.get("archived")),
            "ownerType": (item.get("owner") or {}).get("type"),
            "normalizationReasons": reasons
        }
        if aliases:
            record["aliases"] = aliases
        normalized.append(record)
    return sorted(normalized, key=lambda item: (str(item.get("fullName") or "").casefold(), item["identity"]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize a raw GitHub collector snapshot")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = json.loads(args.input.read_text(encoding="utf-8"))
    output = args.output or args.input.with_name(args.input.stem + ".normalized.json")
    document = {
        "version": 1,
        "topic": source.get("topic"),
        "query": source.get("query"),
        "repositories": normalize(source.get("items", [])),
        "limitations": source.get("limitations", [])
    }
    output.write_text(canonical_json(document), encoding="utf-8")
    print(f"normalized {len(document['repositories'])} repositories into {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
