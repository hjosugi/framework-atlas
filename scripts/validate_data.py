#!/usr/bin/env python3
"""Validate Framework Atlas JSON data using only the Python standard library."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

REQUIRED_FRAMEWORK_FIELDS = {
    'id', 'name', 'languages', 'category', 'subcategory', 'kind', 'maturity',
    'status', 'repository', 'website', 'summary_ja', 'problem_ja', 'sources', 'verification'
}
VALID_MATURITY = {'deep', 'standard', 'seed'}
VALID_CONFIDENCE = {'high', 'medium', 'low'}


def load(name: str):
    with (DATA / name).open(encoding='utf-8') as f:
        return json.load(f)


def is_http_url(value: str) -> bool:
    if not value:
        return True
    parsed = urlparse(value)
    return parsed.scheme in {'http', 'https'} and bool(parsed.netloc)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    frameworks = load('frameworks.json')
    concepts = load('concepts.json')
    relations = load('relations.json')
    ecosystems = load('ecosystems.json')
    timeline = load('timeline.json')
    gaps = load('research-gaps.json')

    framework_ids: set[str] = set()
    for index, item in enumerate(frameworks):
        missing = REQUIRED_FRAMEWORK_FIELDS - item.keys()
        if missing:
            errors.append(f'framework[{index}] {item.get("name", "?")}: missing {sorted(missing)}')
        item_id = item.get('id', '')
        if not item_id:
            errors.append(f'framework[{index}]: empty id')
        elif item_id in framework_ids:
            errors.append(f'duplicate framework id: {item_id}')
        framework_ids.add(item_id)
        if item.get('maturity') not in VALID_MATURITY:
            errors.append(f'{item_id}: invalid maturity {item.get("maturity")}')
        if not item.get('languages'):
            warnings.append(f'{item_id}: no language')
        for field in ('repository', 'website'):
            if not is_http_url(item.get(field, '')):
                errors.append(f'{item_id}: invalid {field} URL: {item.get(field)}')
        for src in item.get('sources', []):
            if not is_http_url(src.get('url', '')):
                errors.append(f'{item_id}: invalid source URL: {src.get("url")}')
        if item.get('maturity') == 'deep':
            for field in ('history_ja', 'design_ja', 'data_model_ja', 'strengths_ja', 'tradeoffs_ja'):
                if not item.get(field):
                    errors.append(f'{item_id}: deep profile missing {field}')
            if len(item.get('sources', [])) < 1:
                errors.append(f'{item_id}: deep profile has no source')

    concept_ids = {item['id'] for item in concepts}
    if len(concept_ids) != len(concepts):
        errors.append('duplicate concept ids')
    all_nodes = framework_ids | concept_ids

    relation_keys: set[tuple[str, str, str]] = set()
    for index, rel in enumerate(relations):
        for endpoint in ('from', 'to'):
            if rel.get(endpoint) not in all_nodes:
                errors.append(f'relation[{index}] dangling {endpoint}: {rel.get(endpoint)}')
        if rel.get('confidence') not in VALID_CONFIDENCE:
            errors.append(f'relation[{index}] invalid confidence: {rel.get("confidence")}')
        key = (rel.get('from', ''), rel.get('to', ''), rel.get('type', ''))
        if key in relation_keys:
            errors.append(f'duplicate relation: {key}')
        relation_keys.add(key)
        if rel.get('verification') == 'verified' and not rel.get('source_url'):
            warnings.append(f'verified relation without URL: {key}')
        if not is_http_url(rel.get('source_url', '')):
            errors.append(f'relation[{index}] invalid source URL')

    for ecosystem in ecosystems:
        for member in ecosystem.get('members', []):
            if member not in all_nodes:
                errors.append(f'ecosystem {ecosystem.get("id")}: unknown member {member}')

    for event in timeline:
        for node in event.get('nodes', []):
            if node not in all_nodes:
                errors.append(f'timeline {event.get("date")} {event.get("title")}: unknown node {node}')
        if not is_http_url(event.get('source_url', '')):
            errors.append(f'timeline {event.get("title")}: invalid source URL')

    gap_ids = [gap['id'] for gap in gaps]
    if len(gap_ids) != len(set(gap_ids)):
        errors.append('duplicate research gap ids')

    for warning in warnings:
        print(f'warning: {warning}', file=sys.stderr)
    if errors:
        for error in errors:
            print(f'error: {error}', file=sys.stderr)
        print(f'validation failed: {len(errors)} error(s), {len(warnings)} warning(s)', file=sys.stderr)
        return 1

    print(
        f'validation passed: {len(frameworks)} frameworks, {len(concepts)} concepts, '
        f'{len(relations)} relations, {len(timeline)} timeline events, {len(gaps)} research gaps'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
