#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path

from common import ROOT, canonical_json, sha256

INCLUDE_ROOTS = ("data", "docs", "issues", "profiles", "release", "schema", "scripts", "tests")
INCLUDE_FILES = ("README.md", "LICENSE", "Makefile")
EXCLUDED_NAMES = {"__pycache__", ".DS_Store"}
FIXED_TIME = (2020, 1, 1, 0, 0, 0)


def source_files() -> list[Path]:
    files: list[Path] = []
    for relative in INCLUDE_FILES:
        path = ROOT / relative
        if path.is_file():
            files.append(path)
    for relative in INCLUDE_ROOTS:
        root = ROOT / relative
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_symlink():
                raise RuntimeError(f"symlinks are forbidden in release archives: {path.relative_to(ROOT)}")
            if not path.is_file() or any(part in EXCLUDED_NAMES for part in path.parts):
                continue
            if path.suffix in {".pyc", ".zip"}:
                continue
            files.append(path)
    return sorted(set(files), key=lambda item: item.relative_to(ROOT).as_posix())


def write_member(archive: zipfile.ZipFile, name: str, content: bytes, executable: bool = False) -> None:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = ((0o755 if executable else 0o644) & 0xFFFF) << 16
    archive.writestr(info, content, compresslevel=9)


def source_commit() -> str:
    explicit = os.environ.get("SOURCE_SHA")
    if explicit:
        return explicit
    try:
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
        if dirty:
            return "working-tree"
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError:
        return "uncommitted"


def build_archive(output: Path, version: str, commit: str | None = None) -> None:
    files = source_files()
    manifest = {
        "version": version,
        "sourceCommit": commit or source_commit(),
        "files": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in files
        ]
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        members = [("MANIFEST.json", canonical_json(manifest).encode("utf-8"), False)]
        members.extend(
            (
                path.relative_to(ROOT).as_posix(),
                path.read_bytes(),
                path.relative_to(ROOT).as_posix().startswith("scripts/") and path.suffix == ".py"
            )
            for path in files
        )
        for name, content, executable in sorted(members, key=lambda member: member[0]):
            write_member(archive, name, content, executable=executable)


def inspect_archive(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names != sorted(names):
            raise RuntimeError("archive members are not sorted")
        if len(names) != len(set(names)):
            raise RuntimeError("archive contains duplicate members")
        for name in names:
            if name.startswith("/") or ".." in Path(name).parts:
                raise RuntimeError(f"unsafe archive path: {name}")
        manifest = json.loads(archive.read("MANIFEST.json"))
        for entry in manifest["files"]:
            import hashlib
            payload = archive.read(entry["path"])
            if hashlib.sha256(payload).hexdigest() != entry["sha256"]:
                raise RuntimeError(f"manifest mismatch: {entry['path']}")


def reproducibility_check(version: str, commit: str | None = None) -> None:
    with tempfile.TemporaryDirectory(prefix="framework-atlas-zip-") as directory:
        first = Path(directory) / "first.zip"
        second = Path(directory) / "second.zip"
        resolved_commit = commit or source_commit()
        build_archive(first, version, resolved_commit)
        build_archive(second, version, resolved_commit)
        if first.read_bytes() != second.read_bytes():
            raise RuntimeError("two clean archive builds differ")
        inspect_archive(first)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic Framework Atlas release ZIP")
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-sha")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    reproducibility_check(args.version, args.source_sha)
    if args.check:
        print("ZIP is reproducible and safe to extract")
        return 0
    output = ROOT / "dist" / f"framework-atlas-{args.version}.zip"
    build_archive(output, args.version, args.source_sha)
    inspect_archive(output)
    checksum = sha256(output)
    sums = ROOT / "dist/SHA256SUMS"
    sums.write_text(f"{checksum}  {output.name}\n", encoding="utf-8")
    print(f"wrote {output.relative_to(ROOT)} ({checksum})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
