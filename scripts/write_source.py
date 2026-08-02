#!/usr/bin/env python3
"""Write the exact commit/version marker included only in the Pages artifact."""
from __future__ import annotations

import argparse

from common import ROOT, canonical_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    if len(args.commit) != 40 or any(character not in "0123456789abcdef" for character in args.commit.lower()):
        parser.error("--commit must be an exact 40-character hexadecimal SHA")
    output = ROOT / "docs/source.json"
    output.write_text(
        canonical_json({"commit": args.commit, "version": args.version}), encoding="utf-8"
    )
    print(f"wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
