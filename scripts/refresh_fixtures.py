#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from common import ROOT, canonical_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh fixture digests only after explicit review")
    parser.add_argument("--explicit", action="store_true", help="acknowledge that fixture changes were reviewed")
    args = parser.parse_args()
    if not args.explicit:
        parser.error("--explicit is required; fixtures never refresh implicitly")
    path = ROOT / "tests/fixtures/manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for record in manifest["files"]:
        fixture = ROOT / record["path"]
        record["sha256"] = hashlib.sha256(fixture.read_bytes()).hexdigest()
    path.write_text(canonical_json(manifest), encoding="utf-8")
    print("fixture digests refreshed; review the manifest diff before commit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
