#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from common import ROOT, canonical_json


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return normalized[:72] or "issue"


def render_issue(issue: dict[str, Any]) -> str:
    labels = ", ".join(label["name"] for label in issue.get("labels", [])) or "none"
    body = (issue.get("body") or "").rstrip()
    return (
        f"# #{issue['number']} {issue['title']}\n\n"
        f"- State: {issue['state']}\n"
        f"- Labels: {labels}\n"
        f"- URL: {issue['html_url']}\n"
        f"- Updated: {issue['updated_at']}\n\n"
        f"{body}\n"
    )


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def fetch_issues(repo: str, token: str | None) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    page = 1
    while True:
        params = urllib.parse.urlencode({"state": "all", "per_page": 100, "page": page, "sort": "created", "direction": "asc"})
        request = urllib.request.Request(f"https://api.github.com/repos/{repo}/issues?{params}")
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("User-Agent", "hjosugi-framework-atlas/1")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.loads(response.read().decode("utf-8"))
        issues.extend(item for item in batch if "pull_request" not in item)
        if len(batch) < 100:
            break
        page += 1
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Export GitHub implementation issues as release evidence")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "issues")
    parser.add_argument("--check", action="store_true", help="compare registered title/body digests without writing")
    args = parser.parse_args()
    issues = fetch_issues(args.repo, os.environ.get("GITHUB_TOKEN"))
    issues = sorted(issues, key=lambda issue: issue["number"])
    if args.check:
        index_path = args.output / "index.json"
        recorded = {item["number"]: item for item in json.loads(index_path.read_text(encoding="utf-8"))["issues"]}
        errors: list[str] = []
        for issue in issues:
            item = recorded.get(issue["number"])
            if not item:
                errors.append(f"registered issue #{issue['number']} is absent from export")
                continue
            if item.get("titleDigest") != digest(issue["title"]):
                errors.append(f"issue #{issue['number']} title digest differs")
            if item.get("bodyDigest") != digest(issue.get("body") or ""):
                errors.append(f"issue #{issue['number']} body digest differs")
        missing = sorted(set(recorded) - {issue["number"] for issue in issues})
        errors.extend(f"exported issue #{number} is absent from GitHub" for number in missing)
        if errors:
            print("\n".join(errors))
            return 1
        print(f"registered title/body digests match {len(issues)} exported issues")
        return 0
    args.output.mkdir(parents=True, exist_ok=True)
    expected_names: set[str] = set()
    index: list[dict[str, Any]] = []
    for issue in issues:
        filename = f"{issue['number']:04d}-{slug(issue['title'])}.md"
        expected_names.add(filename)
        rendered = render_issue(issue)
        (args.output / filename).write_text(rendered, encoding="utf-8")
        index.append({
            "number": issue["number"], "title": issue["title"], "state": issue["state"],
            "url": issue["html_url"], "updatedAt": issue["updated_at"], "file": f"issues/{filename}",
            "parent": next((line.removeprefix("- Parent: ") for line in (issue.get("body") or "").splitlines() if line.startswith("- Parent: ")), None),
            "titleDigest": digest(issue["title"]), "bodyDigest": digest(issue.get("body") or ""), "fileDigest": digest(rendered)
        })
    for path in args.output.glob("[0-9][0-9][0-9][0-9]-*.md"):
        if path.name not in expected_names:
            path.unlink()
    (args.output / "index.json").write_text(canonical_json({"version": 1, "repo": args.repo, "issues": index}), encoding="utf-8")
    print(f"exported {len(index)} issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
