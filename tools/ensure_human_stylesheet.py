# coding: utf-8
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist-platform'
LINK = '<link rel="stylesheet" href="/assets/human-first-principles.css">'
HEAD_END = re.compile(r'</head\s*>', re.I)
VALID_LINK = re.compile(r'<link\b[^>]*href=["\']/assets/human-first-principles\.css["\'][^>]*>', re.I)

changed = 0
for path in DIST.rglob('*.html'):
    raw = path.read_text(encoding='utf-8')
    if VALID_LINK.search(raw):
        continue
    out, n = HEAD_END.subn(LINK + '</head>', raw, count=1)
    if n != 1:
        raise SystemExit(f'Cannot find closing head tag in {path.relative_to(DIST)}')
    path.write_text(out, encoding='utf-8')
    changed += 1

print(f'Human stylesheet guaranteed: files={changed}')
