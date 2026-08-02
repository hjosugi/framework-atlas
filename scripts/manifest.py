#!/usr/bin/env python3
"""Write or verify deterministic SHA-256 manifests for both research artifacts."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPTH_LAB = ROOT / "framework-depth-lab"
EXCLUDED_PARTS = {".git", "__pycache__", ".cache", ".venv", "dist"}
EXCLUDED_NAMES = {".DS_Store", ".env", "MANIFEST.json", "source.json"}


def included_files(base: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in base.rglob("*")
            if path.is_file()
            and path.name not in EXCLUDED_NAMES
            and path != base / "MANIFEST.sha256"
            and not any(part in EXCLUDED_PARTS for part in path.relative_to(base).parts)
            and path.suffix not in {".pyc", ".zip"}
        ),
        key=lambda path: path.relative_to(base).as_posix(),
    )


def render(base: Path) -> str:
    lines = []
    for path in included_files(base):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  ./{path.relative_to(base).as_posix()}")
    return "\n".join(lines) + "\n"


def process(base: Path, check: bool) -> bool:
    target = base / "MANIFEST.sha256"
    expected = render(base)
    if check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            print(f"stale checksum manifest: {target.relative_to(ROOT)}", file=sys.stderr)
            return False
        print(f"verified {target.relative_to(ROOT)}")
        return True
    target.write_text(expected, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    # The root manifest includes the completed nested manifest, so order matters.
    valid = process(DEPTH_LAB, args.check)
    valid = process(ROOT, args.check) and valid
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
