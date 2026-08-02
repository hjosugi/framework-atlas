#!/usr/bin/env python3
"""Generate readable Markdown profiles and family-tree summaries from JSON."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
PROFILES = ROOT / 'profiles'
HISTORY = ROOT / 'history'

CATEGORY_DIR = {
    'backend-web': 'web',
    'frontend-framework': 'frontend',
    'frontend-library': 'frontend',
    'meta-framework': 'frontend',
    'data-model': 'data-model',
    'mobile-desktop': 'mobile-desktop',
    'tui': 'tui',
    'ai-data': 'data-ai',
    'testing': 'testing',
    'game': 'game',
    'router': 'routing',
}

GENERATED_PROFILE_DIRS = set(CATEGORY_DIR.values()) | {'other'}


def bullets(values, empty='追加調査中'):
    values = [str(x) for x in (values or []) if x]
    return '\n'.join(f'- {x}' for x in values) if values else f'- {empty}'


def main() -> None:
    frameworks = json.loads((DATA / 'frameworks.json').read_text(encoding='utf-8'))
    concepts = json.loads((DATA / 'concepts.json').read_text(encoding='utf-8'))
    families = json.loads((DATA / 'families.json').read_text(encoding='utf-8'))
    node = {item['id']: item for item in frameworks}
    node.update({item['id']: item for item in concepts})

    # Recreate only directories owned by this generator. Curated v1 profiles
    # live at profiles/*.md and must survive catalog regeneration.
    for child in PROFILES.iterdir() if PROFILES.exists() else []:
        if child.is_dir() and child.name in GENERATED_PROFILE_DIRS:
            shutil.rmtree(child)
    PROFILES.mkdir(parents=True, exist_ok=True)

    index = ['# Deep framework profiles', '', 'JSON catalog のうち `maturity: deep` の項目を Markdown へ生成したもの。', '']
    for item in sorted((x for x in frameworks if x.get('maturity') == 'deep'), key=lambda x: (x.get('category',''), x.get('name','').casefold())):
        folder = CATEGORY_DIR.get(item.get('category',''), 'other')
        target_dir = PROFILES / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        sources = item.get('sources', [])
        content = f'''# {item['name']}

- ID: `{item['id']}`
- 分野: `{item.get('category','')}` / `{item.get('subcategory','')}`
- 言語: {', '.join(item.get('languages', []))}
- 最初の公開: {item.get('first_release','未確認')}
- status: `{item.get('status','unknown')}`
- verification: `{item.get('verification',{}).get('level','unknown')}` / `{item.get('verification',{}).get('as_of','')}`

## 一文でいうと

{item.get('summary_ja','')}

## 何を解決するか

{item.get('problem_ja','')}

## 歴史・背景

{item.get('history_ja','追加調査中')}

## 中核設計

{item.get('design_ja','追加調査中')}

## Data model

{item.get('data_model_ja','追加調査中')}

## メリット

{bullets(item.get('strengths_ja'))}

## デメリット / trade-off

{bullets(item.get('tradeoffs_ja'))}

## 向いている用途

{bullets(item.get('best_for_ja'))}

## 避ける条件

{bullets(item.get('avoid_when_ja'))}

## 実行モデル

- primary abstraction: {item.get('primary_abstraction_ja') or '追加調査中'}
- control flow: {item.get('control_flow_ja') or '追加調査中'}
- routing: {item.get('routing_ja') or '追加調査中'}
- rendering: {item.get('rendering_ja') or '追加調査中'}
- dependency injection: {item.get('dependency_injection_ja') or '追加調査中'}
- state: {item.get('state_model_ja') or '追加調査中'}
- concurrency: {item.get('concurrency_ja') or '追加調査中'}
- deployment: {item.get('deployment_ja') or '追加調査中'}
- extension: {item.get('extension_model_ja') or '追加調査中'}
- testing: {item.get('testing_ja') or '追加調査中'}
- migration cost: {item.get('migration_cost_ja') or '追加調査中'}

## Official / primary sources

{bullets([f"[{src.get('label','source')}]({src.get('url','')})" for src in sources])}

## Research gaps

{bullets(item.get('research_gaps'), 'なし')}
'''
        path = target_dir / f"{item['id']}.md"
        path.write_text(content, encoding='utf-8')
        index.append(f"- [{item['name']}]({folder}/{item['id']}.md) — {item.get('summary_ja','')}")
    (PROFILES / 'README.md').write_text('\n'.join(index) + '\n', encoding='utf-8')

    family_md = [
        '# 家系図で読む framework 史',
        '',
        '公開ページはこの data を SVG の家系図として表示する。ここでは GitHub 上で読める簡略版を掲載する。',
        '',
        '- `──▶` は一次資料で確認済みの基盤・後継・明示的影響',
        '- `╌╌▶` は設計上の応答・影響候補で、追加 evidence が必要',
        '- `┈┈▶` は直接の血縁ではなく、同じ問題領域・共通基盤・topic 分類',
        '',
    ]
    for family in families:
        family_md += [f"## {family['name_ja']}", '', family.get('summary_ja',''), '', f"**中心の問い:** {family.get('question_ja','')}", '']
        family_names: dict[str, str] = {}
        for generation in family.get('generations', []):
            names = []
            for ref in generation.get('nodes', []):
                item_id = ref.get('id') if isinstance(ref, dict) else ref
                item = node.get(item_id, ref if isinstance(ref, dict) else {})
                if isinstance(ref, dict):
                    name = item.get('name') or ref.get('name') or item_id
                    role = ref.get('role_ja', '')
                else:
                    name = item.get('name') or item_id
                    role = ''
                family_names[item_id] = name
                names.append(f"**{name}**" + (f" — {role}" if role else ''))
            family_md += [f"### {generation.get('label_ja','世代')} ({generation.get('era_ja','')})", '', *[f'- {x}' for x in names], '']
        family_md += ['### 枝', '']
        for edge in family.get('edges', []):
            verification = edge.get('verification')
            mark = '──▶' if verification == 'verified' else ('┈┈▶' if verification == 'grouping' else '╌╌▶')
            from_name = family_names.get(edge['from']) or (node.get(edge['from']) or {'name': edge['from']}).get('name', edge['from'])
            to_name = family_names.get(edge['to']) or (node.get(edge['to']) or {'name': edge['to']}).get('name', edge['to'])
            family_md.append(f"- **{from_name}** {mark} **{to_name}**: {edge.get('label_ja','')}")
        family_md += ['', '### 覚えること', '', *[f'- {x}' for x in family.get('takeaways_ja', [])], '']
    (HISTORY / 'family-trees.md').write_text('\n'.join(family_md).rstrip() + '\n', encoding='utf-8')
    print(f"generated {sum(1 for x in frameworks if x.get('maturity') == 'deep')} profiles and {len(families)} family summaries")


if __name__ == '__main__':
    main()
