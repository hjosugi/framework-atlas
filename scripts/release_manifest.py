#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from pathlib import Path

from common import ROOT, canonical_json, sha256


def main() -> int:
    parser = argparse.ArgumentParser(description="Record immutable release and Pages source evidence")
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--zip", type=Path, required=True)
    parser.add_argument("--checksum", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.source_sha) != 40:
        parser.error("--source-sha must be an exact 40-character commit")
    pages = {}
    for relative in ("docs/index.html", "docs/app.js", "docs/style.css", "docs/atlas-data.json"):
        path = ROOT / relative
        pages[relative] = {"sha256": sha256(path), "bytes": path.stat().st_size, "contentType": mimetypes.guess_type(path.name)[0] or "application/octet-stream"}
    issue_index = ROOT / "issues/index.json"
    document = {
        "version": args.version,
        "sourceCommit": args.source_sha,
        "tagCommit": args.source_sha,
        "zip": {"name": args.zip.name, "sha256": sha256(args.zip), "bytes": args.zip.stat().st_size, "contentType": "application/zip"},
        "checksum": {"name": args.checksum.name, "sha256": sha256(args.checksum), "bytes": args.checksum.stat().st_size, "contentType": "text/plain"},
        "issueIndex": {"path": "issues/index.json", "sha256": sha256(issue_index), "count": len(json.loads(issue_index.read_text(encoding="utf-8"))["issues"])},
        "pagesSource": pages,
        "publicVerification": {"state": "pending-read-back", "policy": "release publication does not become verified until anonymous HTTP responses are recorded"}
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical_json(document), encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
