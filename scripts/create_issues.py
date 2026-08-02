#!/usr/bin/env python3
"""Create GitHub issues from research/issues/*.md using the GitHub CLI.

The Markdown files use a deliberately small YAML-like front matter format:

---
title: "..."
labels: "label-a,label-b"
---

This script avoids a YAML dependency and supports a safe --dry-run mode.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ISSUES = ROOT / "research" / "issues"


@dataclass(frozen=True)
class IssueDraft:
    path: Path
    title: str
    labels: tuple[str, ...]
    body: str


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_issue(path: Path) -> IssueDraft:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing front matter")
    try:
        front, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: unterminated front matter") from exc

    values: dict[str, str] = {}
    for raw_line in front.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}: invalid front matter line: {raw_line!r}")
        key, value = line.split(":", 1)
        values[key.strip()] = unquote(value)

    title = values.get("title", "").strip()
    if not title:
        raise ValueError(f"{path}: title is required")
    labels = tuple(label.strip() for label in values.get("labels", "").split(",") if label.strip())
    return IssueDraft(path=path, title=title, labels=labels, body=body.strip() + "\n")


def run_json(args: list[str]) -> object:
    completed = subprocess.run(args, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout or "null")


def existing_titles(repo: str) -> set[str]:
    data = run_json([
        "gh", "issue", "list", "--repo", repo, "--state", "all", "--limit", "1000", "--json", "title"
    ])
    if not isinstance(data, list):
        return set()
    return {str(item.get("title", "")) for item in data if isinstance(item, dict)}


def ensure_labels(repo: str, labels: set[str], *, dry_run: bool) -> None:
    """Create missing labels with stable colors.

    GitHub accepts reusing the same color. Label descriptions stay generic because
    the label names themselves carry the taxonomy.
    """
    if not labels:
        return
    if dry_run:
        print(f"would ensure {len(labels)} label(s): {', '.join(sorted(labels))}")
        return
    known_raw = run_json(["gh", "label", "list", "--repo", repo, "--limit", "1000", "--json", "name"])
    known = {str(item.get("name")) for item in known_raw if isinstance(item, dict)} if isinstance(known_raw, list) else set()
    for label in sorted(labels - known):
        subprocess.run([
            "gh", "label", "create", label, "--repo", repo,
            "--color", "4F46E5", "--description", "Framework Atlas research workflow"
        ], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub repository in OWNER/REPO form")
    parser.add_argument("--issues-dir", type=Path, default=DEFAULT_ISSUES)
    parser.add_argument("--dry-run", action="store_true", help="Print planned operations without changing GitHub")
    parser.add_argument("--include", default="", help="Regex matched against file name or title")
    parser.add_argument("--limit", type=int, default=0, help="Maximum drafts to process; 0 means all")
    parser.add_argument("--no-skip-existing", action="store_true", help="Create even when an identical title already exists")
    parser.add_argument("--no-create-labels", action="store_true", help="Do not create missing labels")
    args = parser.parse_args()

    if not args.dry_run and shutil.which("gh") is None:
        print("error: gh is required. Install GitHub CLI and run `gh auth login`.", file=sys.stderr)
        return 2

    issue_dir = args.issues_dir if args.issues_dir.is_absolute() else ROOT / args.issues_dir
    paths = sorted(issue_dir.glob("*.md"))
    drafts: list[IssueDraft] = []
    pattern = re.compile(args.include, re.IGNORECASE) if args.include else None
    for path in paths:
        draft = parse_issue(path)
        if pattern and not (pattern.search(path.name) or pattern.search(draft.title)):
            continue
        drafts.append(draft)
    if args.limit:
        drafts = drafts[: args.limit]
    if not drafts:
        print("no issue drafts matched", file=sys.stderr)
        return 1

    known_titles: set[str] = set()
    if not args.no_skip_existing and not args.dry_run:
        known_titles = existing_titles(args.repo)

    labels = {label for draft in drafts for label in draft.labels}
    if not args.no_create_labels:
        ensure_labels(args.repo, labels, dry_run=args.dry_run)

    created = skipped = 0
    for draft in drafts:
        if draft.title in known_titles and not args.no_skip_existing:
            print(f"skip existing: {draft.title}")
            skipped += 1
            continue
        command = [
            "gh", "issue", "create", "--repo", args.repo,
            "--title", draft.title,
            "--body-file", str(draft.path),
        ]
        if draft.labels:
            command.extend(["--label", ",".join(draft.labels)])
        if args.dry_run:
            print("would create:")
            print(f"  title: {draft.title}")
            print(f"  labels: {', '.join(draft.labels) or '(none)'}")
            print(f"  source: {draft.path.relative_to(ROOT)}")
        else:
            # The body file contains front matter. Feed only the body over stdin.
            command = [
                "gh", "issue", "create", "--repo", args.repo,
                "--title", draft.title,
                "--body", draft.body,
            ]
            if draft.labels:
                command.extend(["--label", ",".join(draft.labels)])
            subprocess.run(command, check=True)
        created += 1

    action = "planned" if args.dry_run else "created"
    print(f"{action}: {created}; skipped: {skipped}; drafts considered: {len(drafts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
