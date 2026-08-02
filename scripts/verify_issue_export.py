#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys

from common import ROOT


def main() -> int:
    index_path = ROOT / "issues/index.json"
    if not index_path.exists():
        print("issues/index.json is missing", file=sys.stderr)
        return 1
    document = json.loads(index_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    numbers: set[int] = set()
    for record in document.get("issues", []):
        number = record.get("number")
        if number in numbers:
            errors.append(f"duplicate issue #{number}")
        numbers.add(number)
        path = ROOT / record.get("file", "")
        if not path.is_file():
            errors.append(f"issue #{number}: missing {path.relative_to(ROOT)}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != record.get("fileDigest"):
            errors.append(f"issue #{number}: exported file digest differs")
        title = record.get("title", "")
        if hashlib.sha256(title.encode("utf-8")).hexdigest() != record.get("titleDigest"):
            errors.append(f"issue #{number}: title digest differs")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"verified {len(numbers)} exported issue records and digests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
