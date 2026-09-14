# coding: utf-8
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist-platform'
BODY_RE = re.compile(r'<body(?P<attrs>[^>]*)>', re.I)


def add_class(html):
    def repl(match):
        attrs = match.group('attrs')
        if 'human-first-principles' in attrs:
            return match.group(0)
        m = re.search(r'class=["\']([^"\']*)["\']', attrs, re.I)
        if m:
            classes = (m.group(1).strip() + ' human-first-principles').strip()
            attrs = attrs[:m.start()] + f'class="{classes}"' + attrs[m.end():]
            return f'<body{attrs}>'
        return f'<body{attrs} class="human-first-principles">'
    return BODY_RE.sub(repl, html, count=1)

changed = 0
for path in DIST.rglob('*.html'):
    raw = path.read_text(encoding='utf-8')
    out = add_class(raw)
    if out != raw:
        path.write_text(out, encoding='utf-8')
        changed += 1

print(f'Human body class fixed: files={changed}')
