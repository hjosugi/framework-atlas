#!/usr/bin/env python3
"""Static validation for the research artifact; uses only Python stdlib."""

from __future__ import annotations

import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def validate_json() -> None:
    for path in sorted((ROOT / "data").glob("*.json")):
        try:
            with path.open(encoding="utf-8") as handle:
                json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def validate_csv() -> None:
    required = {
        "comparison.csv": {"dimension", "spring_boot", "fastapi", "gin"},
        "influence-edges.csv": {"source", "target", "type", "confidence", "evidence"},
    }
    for name, expected in required.items():
        path = ROOT / "data" / name
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            actual = set(reader.fieldnames or [])
            rows = list(reader)
        if expected != actual:
            fail(f"unexpected CSV columns in {name}: {actual}")
        if not rows:
            fail(f"CSV has no data: {name}")


def validate_markdown_links() -> None:
    link_pattern = re.compile(r"\[[^]]*]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"link escapes repository: {path.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                fail(f"broken link: {path.relative_to(ROOT)} -> {target}")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        return {}
    result: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def validate_issues() -> None:
    issues = sorted((ROOT / "issues").glob("*.md"))
    if len(issues) < 15:
        fail(f"expected at least 15 research issues, found {len(issues)}")
    for path in issues:
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        for key in ("title", "labels", "priority"):
            if not metadata.get(key):
                fail(f"missing {key} in {path.relative_to(ROOT)}")
        for heading in ("## Context", "## Acceptance criteria", "## Evidence"):
            if heading not in text:
                fail(f"missing {heading} in {path.relative_to(ROOT)}")


def validate_examples() -> None:
    endpoint_markers = {
        "spring-boot/src/main/java/lab/frameworkdepth/items/ItemController.java": [
            '"/healthz"', '"/items/{item_id}"', '"/items"'
        ],
        "fastapi/app/main.py": ['"/healthz"', '"/items/{item_id}"', '"/items"'],
        "gin/main.go": ['"/healthz"', '"/items/:item_id"', '"/items"'],
    }
    for relative, markers in endpoint_markers.items():
        path = ROOT / "examples" / relative
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                fail(f"missing endpoint marker {marker} in {path.relative_to(ROOT)}")

    pom = ROOT / "examples" / "spring-boot" / "pom.xml"
    try:
        ET.parse(pom)
    except ET.ParseError as exc:
        fail(f"invalid Maven XML: {exc}")

    for path in sorted((ROOT / "examples" / "fastapi").rglob("*.py")):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            fail(f"invalid Python {path.relative_to(ROOT)}: {exc}")


def validate_site() -> None:
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    for asset in ("styles.css", "app.js"):
        if asset not in html or not (ROOT / "site" / asset).exists():
            fail(f"site asset missing or unreferenced: {asset}")
    for section_id in ("compare", "flow", "influence", "case-study"):
        if f'id="{section_id}"' not in html:
            fail(f"site section missing: {section_id}")


def validate_versions() -> None:
    expected = {
        "Spring Boot": "4.1.0",
        "FastAPI": "0.141.1",
        "Gin": "1.12.0",
        "case study commit": "91c8ef24b4cb6ef558c95d8267fa07d68c7059f8",
    }
    corpus = "\n".join(
        [
            (ROOT / "data" / "frameworks.json").read_text(encoding="utf-8"),
            (ROOT / "EXECUTIVE_SUMMARY.md").read_text(encoding="utf-8"),
        ]
    )
    for name, version in expected.items():
        if version not in corpus:
            fail(f"missing pinned {name}: {version}")


def main() -> int:
    validate_json()
    validate_csv()
    validate_markdown_links()
    validate_issues()
    validate_examples()
    validate_site()
    validate_versions()
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} error(s)")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    files = sum(1 for path in ROOT.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    print(f"OK: validated {files} files")
    print("Checks: JSON, CSV, Markdown links, issue metadata, examples, site, pinned versions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
