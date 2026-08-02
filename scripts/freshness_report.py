#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from common import ROOT, canonical_json, load_json


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def github_repo_name(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.casefold() != "github.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    return "/".join(parts[:2]) if len(parts) >= 2 else None


def github_repo(repo: str, token: str | None) -> dict[str, Any]:
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("User-Agent", "hjosugi-framework-atlas/1")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def probe_source(url: str) -> tuple[int, str]:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "hjosugi-framework-atlas/1"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        if exc.code not in (405, 501):
            raise
    request = urllib.request.Request(url, headers={"User-Agent": "hjosugi-framework-atlas/1", "Range": "bytes=0-0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.status, response.geturl()


def build_report(previous: dict[str, Any] | None = None) -> tuple[dict[str, Any], int]:
    attempted = utc_now()
    token = os.environ.get("GITHUB_TOKEN")
    entities = load_json("data/entities.v1.json")["entities"]
    claims = load_json("data/claims.v1.json")["claims"]
    unresolved = load_json("data/unresolved.v1.json")["items"]
    claims_by_entity: dict[str, list[str]] = {}
    for claim in claims:
        claims_by_entity.setdefault(claim["entity"], []).append(claim["id"])
    repository_changes: list[dict[str, Any]] = []
    source_changes: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    state = "complete"

    for entity in entities:
        repo = github_repo_name(entity.get("repository", ""))
        if not repo:
            continue
        try:
            observed = github_repo(repo, token)
            canonical = observed.get("full_name")
            if observed.get("archived") or canonical.casefold() != repo.casefold():
                repository_changes.append({
                    "entity": entity["id"], "recorded": repo, "observed": canonical,
                    "archived": bool(observed.get("archived")), "claimIds": claims_by_entity.get(entity["id"], []),
                    "action": "human review required; historical entity is retained"
                })
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429):
                state = "rate_limited"
            else:
                state = "partial"
            failures.append({"scope": "repository", "entity": entity["id"], "httpStatus": exc.code})
        except (urllib.error.URLError, TimeoutError) as exc:
            state = "partial"
            failures.append({"scope": "repository", "entity": entity["id"], "error": type(exc).__name__})

    for claim in claims:
        try:
            status, final_url = probe_source(claim["source"])
            if final_url.rstrip("/") != claim["source"].rstrip("/"):
                source_changes.append({"claimId": claim["id"], "recorded": claim["source"], "observed": final_url, "httpStatus": status, "action": "review source pointer"})
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429) and state == "complete":
                state = "rate_limited"
            elif state == "complete":
                state = "partial"
            source_changes.append({"claimId": claim["id"], "recorded": claim["source"], "observed": None, "httpStatus": exc.code, "action": "retain claim and review source availability"})
        except (urllib.error.URLError, TimeoutError) as exc:
            state = "partial"
            failures.append({"scope": "claim-source", "claimId": claim["id"], "error": type(exc).__name__})

    today = dt.date.today()
    review_due: list[dict[str, Any]] = []
    defaults = load_json("data/claims.v1.json").get("defaults", {})
    for claim in claims:
        due = dt.date.fromisoformat(claim.get("reviewDue", defaults["reviewDue"]))
        if due <= today:
            review_due.append({"kind": "claim", "id": claim["id"], "due": due.isoformat()})
    for item in unresolved:
        reviewed = dt.date.fromisoformat(item["lastReviewed"])
        if (today - reviewed).days >= 90:
            review_due.append({"kind": "unresolved", "id": item["id"], "lastReviewed": reviewed.isoformat(), "resolutionIssue": item["resolutionIssue"]})

    last_successful = attempted if state == "complete" else (previous or {}).get("lastSuccessfulAt")
    report = {
        "version": 1, "state": state, "attemptedAt": attempted, "lastSuccessfulAt": last_successful,
        "repositoryChanges": repository_changes, "sourceChanges": source_changes, "reviewDue": review_due,
        "failures": failures,
        "policy": "review artifact only; canonical entities, claims, edges and decisions are never rewritten"
    }
    return report, 0 if state == "complete" else 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a review-only framework freshness report")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    previous = json.loads(args.previous.read_text(encoding="utf-8")) if args.previous and args.previous.exists() else None
    report, status = build_report(previous)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical_json(report), encoding="utf-8")
    print(f"freshness state={report['state']}; changes={len(report['repositoryChanges']) + len(report['sourceChanges'])}; review_due={len(report['reviewDue'])}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
