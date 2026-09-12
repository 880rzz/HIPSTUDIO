# coding: utf-8
"""Validate unique accessible names for every generated navigation landmark."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-platform"


def landmark_names(text):
    rows = []
    for match in re.finditer(r'<nav\b([^>]*)>', text, re.IGNORECASE):
        attrs = match.group(1)
        label = re.search(r'aria-label="([^"]*)"', attrs)
        labelledby = re.search(r'aria-labelledby="([^"]*)"', attrs)
        if label:
            name = label.group(1).strip()
            source = 'aria-label'
        elif labelledby:
            target = labelledby.group(1).strip()
            node = re.search(rf'<[^>]+id="{re.escape(target)}"[^>]*>(.*?)</[^>]+>', text, re.IGNORECASE | re.DOTALL)
            name = re.sub(r'<[^>]+>', '', node.group(1)).strip() if node else ''
            source = f'aria-labelledby:{target}'
        else:
            name = ''
            source = 'unnamed'
        rows.append((match.start(), source, name))
    return rows


def main():
    failures = []
    checked = 0
    for page in sorted(DIST.rglob('*.html')):
        text = page.read_text(encoding='utf-8')
        rows = landmark_names(text)
        if not rows:
            continue
        checked += 1
        seen = {}
        for pos, source, name in rows:
            key = name.casefold()
            if not name:
                failures.append(f'{page}: empty navigation name at {pos}; navs={rows}')
            elif key in seen:
                failures.append(f'{page}: duplicate navigation name {name!r} at {seen[key]} and {pos}; navs={rows}')
            else:
                seen[key] = pos
    if failures:
        raise SystemExit('\n'.join(failures[:30]))
    print(f'Navigation landmark names unique across {checked} generated pages')


if __name__ == '__main__':
    main()
