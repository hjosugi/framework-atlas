#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from common import canonical_json

API = "https://api.github.com"
MAX_SEARCH_RESULTS = 1000


@dataclass(frozen=True)
class Window:
    since: dt.date
    until: dt.date

    def split(self) -> tuple["Window", "Window"]:
        if self.since >= self.until:
            raise ValueError("a one-day window cannot be split")
        midpoint = self.since + (self.until - self.since) // 2
        return Window(self.since, midpoint), Window(midpoint + dt.timedelta(days=1), self.until)

    def qualifier(self) -> str:
        return f"created:{self.since.isoformat()}..{self.until.isoformat()}"


class GitHubClient:
    def __init__(self, token: str | None, max_wait: int = 60, max_retries: int = 2, opener: Callable[..., Any] = urllib.request.urlopen):
        self.token = token
        self.max_wait = max_wait
        self.max_retries = max_retries
        self.opener = opener

    def get_json(self, path: str, params: dict[str, object]) -> dict[str, Any]:
        query = urllib.parse.urlencode(params)
        request = urllib.request.Request(f"{API}{path}?{query}")
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("User-Agent", "hjosugi-framework-atlas/1")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        for attempt in range(self.max_retries + 1):
            try:
                with self.opener(request, timeout=30) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code in (403, 429):
                    reset = int(exc.headers.get("X-RateLimit-Reset", "0") or 0)
                    retry_after = int(exc.headers.get("Retry-After", "0") or 0)
                    delay = retry_after or max(1, reset - int(time.time()))
                    if delay > self.max_wait or attempt == self.max_retries:
                        raise CollectionError("rate_limited", exc.code, f"rate limit requires {delay}s wait") from exc
                    time.sleep(delay)
                    continue
                if 500 <= exc.code <= 599:
                    if attempt == self.max_retries:
                        raise CollectionError("partial", exc.code, "GitHub upstream error") from exc
                    time.sleep(min(self.max_wait, 2 ** attempt))
                    continue
                raise
            except urllib.error.URLError as exc:
                if attempt == self.max_retries:
                    raise CollectionError("partial", None, "network error") from exc
                time.sleep(min(self.max_wait, 2 ** attempt))
        raise AssertionError("unreachable")


class CollectionError(RuntimeError):
    def __init__(self, state: str, status: int | None, message: str):
        super().__init__(message)
        self.state = state
        self.status = status


def search_query(topic: str, window: Window) -> str:
    return f"topic:{topic} {window.qualifier()}"


def plan_windows(topic: str, root: Window, count: Callable[[str], int]) -> list[Window]:
    pending = [root]
    planned: list[Window] = []
    while pending:
        window = pending.pop()
        total = count(search_query(topic, window))
        if total <= MAX_SEARCH_RESULTS:
            planned.append(window)
        elif window.since == window.until:
            raise RuntimeError(f"more than {MAX_SEARCH_RESULTS} results on one day: {window.since}")
        else:
            left, right = window.split()
            pending.extend((right, left))
    return sorted(planned, key=lambda item: item.since)


def checkpoint_key(topic: str, window: Window, page: int) -> str:
    return f"{topic}:{window.since}:{window.until}:{page}"


def collect(topic: str, root: Window, client: GitHubClient, checkpoint_path: Path) -> dict[str, Any]:
    attempted_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    checkpoint: dict[str, Any] = {"completed": [], "completedWindows": [], "items": [], "lastSuccessfulAt": None}
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    completed = set(checkpoint.get("completed", []))
    completed_windows = set(checkpoint.get("completedWindows", []))
    items_by_node = {item["node_id"]: item for item in checkpoint.get("items", []) if item.get("node_id")}

    def count(query: str) -> int:
        payload = client.get_json("/search/repositories", {"q": query, "per_page": 1, "page": 1})
        return int(payload["total_count"])

    failure: dict[str, object] | None = None
    state = "complete"
    try:
        windows = plan_windows(topic, root, count)
    except CollectionError as exc:
        windows = []
        state = exc.state
        failure = {"kind": exc.state, "httpStatus": exc.status, "message": str(exc)}
    except RuntimeError as exc:
        windows = []
        state = "truncated"
        failure = {"kind": "single-day-overflow", "httpStatus": None, "message": str(exc)}
    for window in windows:
        window_key = f"{topic}:{window.since}:{window.until}"
        if window_key in completed_windows:
            continue
        query = search_query(topic, window)
        page = 1
        while page <= 10:
            key = checkpoint_key(topic, window, page)
            if key in completed:
                page += 1
                continue
            try:
                payload = client.get_json("/search/repositories", {"q": query, "sort": "created", "order": "asc", "per_page": 100, "page": page})
            except CollectionError as exc:
                state = exc.state
                failure = {"kind": exc.state, "httpStatus": exc.status, "message": str(exc), "window": window_key, "page": page}
                checkpoint.update({"state": state, "failure": failure, "attemptedAt": attempted_at})
                checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
                checkpoint_path.write_text(canonical_json(checkpoint), encoding="utf-8")
                break
            batch = payload.get("items", [])
            if not isinstance(batch, list):
                raise CollectionError("partial", None, "malformed GitHub response: items is not a list")
            for item in batch:
                node_id = item.get("node_id")
                if node_id:
                    items_by_node[node_id] = item
            completed.add(key)
            checkpoint = {
                "version": 1, "topic": topic, "state": "partial", "completed": sorted(completed),
                "completedWindows": sorted(completed_windows), "items": list(items_by_node.values()),
                "attemptedAt": attempted_at, "lastSuccessfulAt": checkpoint.get("lastSuccessfulAt")
            }
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            checkpoint_path.write_text(canonical_json(checkpoint), encoding="utf-8")
            if len(batch) < 100:
                completed_windows.add(window_key)
                checkpoint["completedWindows"] = sorted(completed_windows)
                checkpoint_path.write_text(canonical_json(checkpoint), encoding="utf-8")
                break
            page += 1
        if state != "complete":
            break
    items = sorted(items_by_node.values(), key=lambda item: item.get("full_name", "").casefold())
    records_digest = hashlib.sha256(canonical_json(items).encode("utf-8")).hexdigest()
    last_successful = attempted_at if state == "complete" else checkpoint.get("lastSuccessfulAt")
    result = {
        "version": 1,
        "state": state,
        "topic": topic,
        "query": {"since": root.since.isoformat(), "until": root.until.isoformat()},
        "apiRevision": "2022-11-28",
        "attemptedAt": attempted_at,
        "lastSuccessfulAt": last_successful,
        "windows": [{"since": item.since.isoformat(), "until": item.until.isoformat()} for item in windows],
        "completedPages": sorted(completed),
        "recordsSha256": records_digest,
        "items": items,
        "limitations": ["GitHub topics are self-assigned and incomplete", "single-day windows with more than 1000 matches require another partition key"]
    }
    if failure:
        result["failure"] = failure
    checkpoint.update({"state": state, "attemptedAt": attempted_at, "lastSuccessfulAt": last_successful, "recordsSha256": records_digest})
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_path.write_text(canonical_json(checkpoint), encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect a GitHub topic with recursive date partitioning")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--since", "--from", dest="since", default="2008-01-01")
    parser.add_argument("--until", "--to", dest="until", default=dt.date.today().isoformat())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--max-wait", type=int, default=60)
    parser.add_argument("--max-retries", type=int, default=2)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    root = Window(dt.date.fromisoformat(args.since), dt.date.fromisoformat(args.until))
    checkpoint = args.checkpoint or args.output.with_suffix(".checkpoint.json")
    result = collect(args.topic, root, GitHubClient(token, args.max_wait, args.max_retries), checkpoint)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical_json(result), encoding="utf-8")
    print(f"collector state={result['state']}: {len(result['items'])} unique repositories in {len(result['windows'])} windows")
    if not token:
        print("note: unauthenticated GitHub API rate limits apply", file=sys.stderr)
    return 0 if result["state"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
