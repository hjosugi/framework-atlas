#!/usr/bin/env python3
"""Collect GitHub repositories for framework-related topics.

The GitHub Search API returns at most 1,000 results per query. This collector
recursively partitions each topic by repository creation date. If a single day
still exceeds the limit, it partitions by stars and then repository size.

Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

API = 'https://api.github.com'
SEARCH_LIMIT = 1000
PER_PAGE = 100
EARLIEST = dt.date(2007, 10, 1)

CORE_TOPICS = {
    'framework', 'web-framework', 'frontend-framework', 'backend-framework',
    'meta-framework', 'router', 'routing', 'orm', 'data-modeling',
    'tui', 'terminal-ui', 'testing-framework', 'machine-learning-framework',
    'llm-framework', 'ai-agents', 'css-framework', 'game-engine',
}

NETWORK_TERMS = {
    'openwrt', 'router firmware', 'wireless router', 'vpn', 'censorship',
    'asuswrt', 'nat router', 'wifi repeater', 'access point', 'nas system',
}
SECURITY_TERMS = {
    'exploit', 'exploitation', 'penetration testing', 'scanner', 'bruteforce',
    'offensive security', 'payload', 'vulnerability framework',
}
APP_TERMS = {'viewer', 'browser', 'client app', 'dashboard app', 'operating system'}
FRAMEWORK_TERMS = {
    'framework', 'application framework', 'web framework', 'ui framework',
    'game engine', 'testing framework', 'machine learning framework',
}
COMPONENT_TERMS = {
    'router', 'routing library', 'middleware', 'orm', 'query builder',
    'runtime', 'toolkit', 'component library', 'server interface',
}


@dataclass(frozen=True)
class Range:
    created_from: dt.date
    created_to: dt.date
    stars_from: int | None = None
    stars_to: int | None = None
    size_from: int | None = None
    size_to: int | None = None

    def query(self, topic: str) -> str:
        parts = [f'topic:{topic}', f'created:{self.created_from.isoformat()}..{self.created_to.isoformat()}']
        if self.stars_from is not None and self.stars_to is not None:
            parts.append(f'stars:{self.stars_from}..{self.stars_to}')
        if self.size_from is not None and self.size_to is not None:
            parts.append(f'size:{self.size_from}..{self.size_to}')
        return ' '.join(parts)


class GitHubClient:
    def __init__(self, token: str | None, verbose: bool = True):
        self.token = token
        self.verbose = verbose
        self.requests = 0

    def get_json(self, path: str, params: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
        query = urllib.parse.urlencode(params)
        url = f'{API}{path}?{query}'
        headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'framework-atlas-topic-collector',
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        for attempt in range(8):
            request = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    self.requests += 1
                    data = json.load(response)
                    response_headers = {k.lower(): v for k, v in response.headers.items()}
                    self._respect_rate_limit(response_headers)
                    return data, response_headers
            except urllib.error.HTTPError as error:
                body = error.read().decode('utf-8', errors='replace')
                headers_lower = {k.lower(): v for k, v in error.headers.items()}
                if error.code in {403, 429}:
                    wait = self._wait_seconds(headers_lower, attempt)
                    print(f'rate limited ({error.code}); sleeping {wait}s', file=sys.stderr)
                    time.sleep(wait)
                    continue
                if 500 <= error.code < 600:
                    wait = min(60, 2 ** attempt + random.random())
                    print(f'GitHub server error {error.code}; retrying in {wait:.1f}s', file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise RuntimeError(f'GitHub API {error.code}: {body[:500]}') from error
            except urllib.error.URLError as error:
                wait = min(60, 2 ** attempt + random.random())
                print(f'network error {error}; retrying in {wait:.1f}s', file=sys.stderr)
                time.sleep(wait)
        raise RuntimeError(f'GitHub API request failed after retries: {url}')

    def _wait_seconds(self, headers: dict[str, str], attempt: int) -> int:
        retry_after = headers.get('retry-after')
        if retry_after and retry_after.isdigit():
            return max(1, int(retry_after))
        reset = headers.get('x-ratelimit-reset')
        if reset and reset.isdigit():
            return max(1, int(reset) - int(time.time()) + 2)
        return min(120, 5 * (attempt + 1))

    def _respect_rate_limit(self, headers: dict[str, str]) -> None:
        remaining = headers.get('x-ratelimit-remaining')
        reset = headers.get('x-ratelimit-reset')
        if remaining == '0' and reset and reset.isdigit():
            wait = max(1, int(reset) - int(time.time()) + 2)
            print(f'GitHub search quota exhausted; sleeping {wait}s', file=sys.stderr)
            time.sleep(wait)


def midpoint(start: dt.date, end: dt.date) -> dt.date:
    return start + (end - start) // 2


def split_numeric(low: int, high: int) -> tuple[tuple[int, int], tuple[int, int]]:
    mid = (low + high) // 2
    return (low, mid), (mid + 1, high)


def classify_repo(repo: dict[str, Any], source_topic: str) -> tuple[str, float, str]:
    text = ' '.join([
        repo.get('name') or '', repo.get('description') or '',
        ' '.join(repo.get('topics') or []), source_topic,
    ]).lower()

    if any(term in text for term in SECURITY_TERMS):
        return 'security-framework', 0.92, 'security/offensive terminology detected'
    if source_topic in {'router', 'routing'} and any(term in text for term in NETWORK_TERMS):
        return 'network-product', 0.95, 'network-router/VPN/firmware terminology detected'
    if any(term in text for term in FRAMEWORK_TERMS):
        return 'core-framework', 0.86, 'description or topics explicitly identify a framework'
    if any(term in text for term in COMPONENT_TERMS):
        return 'ecosystem-component', 0.72, 'focused router/ORM/middleware/runtime component'
    if any(term in text for term in APP_TERMS):
        return 'application', 0.64, 'description appears to identify an end-user application'
    return 'candidate', 0.35, 'insufficient evidence; manual review required'


def compact_repo(repo: dict[str, Any], topic: str) -> dict[str, Any]:
    classification, confidence, reason = classify_repo(repo, topic)
    owner = repo.get('owner') or {}
    license_data = repo.get('license') or {}
    return {
        'github_id': repo.get('id'),
        'full_name': repo.get('full_name'),
        'name': repo.get('name'),
        'owner': owner.get('login'),
        'html_url': repo.get('html_url'),
        'description': repo.get('description') or '',
        'homepage': repo.get('homepage') or '',
        'language': repo.get('language') or '',
        'topics': sorted(repo.get('topics') or []),
        'stars': repo.get('stargazers_count', 0),
        'forks': repo.get('forks_count', 0),
        'open_issues': repo.get('open_issues_count', 0),
        'archived': bool(repo.get('archived')),
        'disabled': bool(repo.get('disabled')),
        'is_template': bool(repo.get('is_template')),
        'license_spdx': license_data.get('spdx_id') or 'NOASSERTION',
        'created_at': repo.get('created_at'),
        'updated_at': repo.get('updated_at'),
        'pushed_at': repo.get('pushed_at'),
        'default_branch': repo.get('default_branch'),
        'source_topics': [topic],
        'classification': classification,
        'classification_confidence': confidence,
        'classification_reason': reason,
        'verification': 'machine-classified',
    }


def load_topics(path: Path, scope: str) -> list[str]:
    data = json.loads(path.read_text(encoding='utf-8'))
    values = [item['topic'] if isinstance(item, dict) else str(item) for item in data]
    if scope == 'core':
        values = [value for value in values if value in CORE_TOPICS]
    return sorted(set(values))


def search_count(client: GitHubClient, topic: str, query_range: Range) -> int:
    data, _ = client.get_json('/search/repositories', {
        'q': query_range.query(topic), 'per_page': 1, 'page': 1,
    })
    return int(data.get('total_count', 0))


def ranges_for_topic(client: GitHubClient, topic: str, query_range: Range, depth: int = 0) -> Iterable[tuple[Range, int]]:
    count = search_count(client, topic, query_range)
    indent = '  ' * depth
    print(f'{indent}{topic}: {query_range.query(topic)} => {count}', file=sys.stderr)
    if count <= SEARCH_LIMIT:
        yield query_range, count
        return

    if query_range.created_from < query_range.created_to:
        mid = midpoint(query_range.created_from, query_range.created_to)
        left = Range(query_range.created_from, mid, query_range.stars_from, query_range.stars_to, query_range.size_from, query_range.size_to)
        right = Range(mid + dt.timedelta(days=1), query_range.created_to, query_range.stars_from, query_range.stars_to, query_range.size_from, query_range.size_to)
        yield from ranges_for_topic(client, topic, left, depth + 1)
        yield from ranges_for_topic(client, topic, right, depth + 1)
        return

    if query_range.stars_from is None:
        low, high = 0, 2_000_000
    else:
        low, high = query_range.stars_from, query_range.stars_to or 2_000_000
    if low < high:
        (l1, h1), (l2, h2) = split_numeric(low, high)
        left = Range(query_range.created_from, query_range.created_to, l1, h1, query_range.size_from, query_range.size_to)
        right = Range(query_range.created_from, query_range.created_to, l2, h2, query_range.size_from, query_range.size_to)
        yield from ranges_for_topic(client, topic, left, depth + 1)
        yield from ranges_for_topic(client, topic, right, depth + 1)
        return

    # Extremely unlikely fallback: partition repositories with the same creation day
    # and star count by repository size.
    size_low = query_range.size_from if query_range.size_from is not None else 0
    size_high = query_range.size_to if query_range.size_to is not None else 100_000_000
    if size_low >= size_high:
        raise RuntimeError(f'cannot partition query below 1,000 results: {query_range.query(topic)}')
    (l1, h1), (l2, h2) = split_numeric(size_low, size_high)
    left = Range(query_range.created_from, query_range.created_to, low, high, l1, h1)
    right = Range(query_range.created_from, query_range.created_to, low, high, l2, h2)
    yield from ranges_for_topic(client, topic, left, depth + 1)
    yield from ranges_for_topic(client, topic, right, depth + 1)


def fetch_range(client: GitHubClient, topic: str, query_range: Range, count: int) -> Iterable[dict[str, Any]]:
    pages = math.ceil(count / PER_PAGE)
    for page in range(1, pages + 1):
        data, _ = client.get_json('/search/repositories', {
            'q': query_range.query(topic),
            'sort': 'stars',
            'order': 'desc',
            'per_page': PER_PAGE,
            'page': page,
        })
        for repo in data.get('items', []):
            yield compact_repo(repo, topic)


def merge_repo(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    topics = set(existing.get('source_topics', [])) | set(incoming.get('source_topics', []))
    result = existing if existing.get('updated_at', '') >= incoming.get('updated_at', '') else incoming
    result = dict(result)
    result['source_topics'] = sorted(topics)
    # Prefer manual-looking higher confidence machine classification across topics.
    if incoming.get('classification_confidence', 0) > existing.get('classification_confidence', 0):
        result['classification'] = incoming['classification']
        result['classification_confidence'] = incoming['classification_confidence']
        result['classification_reason'] = incoming['classification_reason']
    return result


def write_snapshot(path: Path, repositories: dict[int, dict[str, Any]], meta: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'meta': meta,
        'repositories': sorted(repositories.values(), key=lambda x: (-x.get('stars', 0), x.get('full_name') or '')),
    }
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics-file', type=Path, default=Path('data/topics.json'))
    parser.add_argument('--output', type=Path, default=Path('data/discovered/github-topics.json'))
    parser.add_argument('--scope', choices=['core', 'all'], default='core')
    parser.add_argument('--topic', action='append', default=[], help='Collect only this topic; may be repeated.')
    parser.add_argument('--max-repositories', type=int, default=0, help='Stop after this many unique repositories; 0 means unlimited.')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--dry-run', action='store_true', help='Only count and partition queries; do not fetch pages.')
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    topics_path = args.topics_file if args.topics_file.is_absolute() else root / args.topics_file
    output_path = args.output if args.output.is_absolute() else root / args.output
    topics = sorted(set(args.topic)) if args.topic else load_topics(topics_path, args.scope)
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print('warning: GITHUB_TOKEN is not set; GitHub Search rate limits will be very low', file=sys.stderr)
    client = GitHubClient(token)

    repositories: dict[int, dict[str, Any]] = {}
    completed_topics: list[str] = []
    if args.resume and output_path.exists():
        old = json.loads(output_path.read_text(encoding='utf-8'))
        for repo in old.get('repositories', []):
            if repo.get('github_id') is not None:
                repositories[int(repo['github_id'])] = repo
        completed_topics = list(old.get('meta', {}).get('completed_topics', []))

    today = dt.date.today()
    meta = {
        'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope': args.scope,
        'topics': topics,
        'completed_topics': completed_topics,
        'api_version': '2022-11-28',
        'collector': 'scripts/collect_github_topics.py',
        'search_limit_strategy': 'recursive created-date partition; stars and size fallback',
        'requests': 0,
    }

    for topic in topics:
        if topic in completed_topics:
            print(f'skip completed topic: {topic}', file=sys.stderr)
            continue
        root_range = Range(EARLIEST, today)
        for query_range, count in ranges_for_topic(client, topic, root_range):
            if args.dry_run:
                continue
            for repo in fetch_range(client, topic, query_range, count):
                repo_id = int(repo['github_id'])
                if repo_id in repositories:
                    repositories[repo_id] = merge_repo(repositories[repo_id], repo)
                else:
                    repositories[repo_id] = repo
                if args.max_repositories and len(repositories) >= args.max_repositories:
                    meta['requests'] = client.requests
                    meta['stopped_early'] = True
                    write_snapshot(output_path, repositories, meta)
                    print(f'stopped at {len(repositories)} repositories')
                    return 0
            meta['requests'] = client.requests
            meta['unique_repositories'] = len(repositories)
            write_snapshot(output_path, repositories, meta)
        completed_topics.append(topic)
        meta['completed_topics'] = completed_topics
        meta['requests'] = client.requests
        meta['unique_repositories'] = len(repositories)
        write_snapshot(output_path, repositories, meta)

    meta['completed'] = True
    meta['requests'] = client.requests
    meta['unique_repositories'] = len(repositories)
    write_snapshot(output_path, repositories, meta)
    print(f'wrote {len(repositories)} unique repositories to {output_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
