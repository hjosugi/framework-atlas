#!/usr/bin/env python3
"""Generate registerable GitHub Issue drafts from data/research-gaps.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'research-gaps.json'
OUTPUT = ROOT / 'research' / 'issues'


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-') or 'research'


def main() -> None:
    gaps = json.loads(DATA.read_text(encoding='utf-8'))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for old in OUTPUT.glob('*.md'):
        old.unlink()
    for gap in gaps:
        labels = ','.join(gap.get('labels', []))
        title = gap['title']
        body = [
            '---',
            f'title: "{title.replace(chr(34), chr(39))}"',
            f'labels: "{labels}"',
            '---',
            '',
            f'# {title}',
            '',
            '## 背景',
            '',
            gap.get('body_ja', ''),
            '',
            '## 完了条件',
            '',
        ]
        body.extend(f'- [ ] {item}' for item in gap.get('acceptance_ja', []))
        body.extend([
            '',
            '## Evidence rule',
            '',
            '- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。',
            '- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。',
            '- 変更した relation には confidence、verification、source URL を付ける。',
            '',
            '## 主な変更対象',
            '',
            '- `data/frameworks.json`',
            '- `data/relations.json` または `data/families.json`',
            '- `profiles/`、`history/`、`research/`',
            '',
            f'<!-- framework-atlas-gap:{gap["id"]} -->',
            '',
        ])
        filename = f'{gap["id"].lower()}-{slug(title)[:70]}.md'
        (OUTPUT / filename).write_text('\n'.join(body), encoding='utf-8')
    print(f'generated {len(gaps)} issue drafts in {OUTPUT}')


if __name__ == '__main__':
    main()
