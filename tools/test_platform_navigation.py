#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist-platform'
errors = []
pages = list(DIST.rglob('*.html'))
if not pages:
    errors.append('dist-platform contains no HTML pages')

for page in pages:
    text = page.read_text(encoding='utf-8')
    rel = page.relative_to(DIST)
    if '<header class="header">' not in text:
        continue
    required = [
        'data-menu-toggle',
        'aria-controls="site-menu"',
        'aria-expanded="false"',
        'data-menu-overlay',
        'data-menu-close',
        'class="menu-primary"',
        'class="menu-link-title"',
        'class="menu-link-copy"',
        '/assets/platform-menu.css',
        '/assets/platform-menu.js',
    ]
    for token in required:
        if token not in text:
            errors.append(f'{rel}: missing {token}')
    header = re.search(r'<header class="header">(.*?)</header>', text, flags=re.S)
    if header and 'class="nav"' in header.group(1):
        errors.append(f'{rel}: legacy desktop nav remains in header')
    if 'class="mobile-nav"' in text:
        errors.append(f'{rel}: legacy mobile details navigation remains')

for asset in ('platform-menu.css','platform-menu.js'):
    if not (DIST / 'assets' / asset).exists():
        errors.append(f'missing built asset: assets/{asset}')

js = (ROOT / 'assets/platform-menu.js').read_text(encoding='utf-8')
for behavior in ("event.key === 'Escape'", "event.key !== 'Tab'", "aria-expanded", "menu-open"):
    if behavior not in js:
        errors.append(f'platform-menu.js missing accessibility behavior: {behavior}')

css = (ROOT / 'assets/platform-menu.css').read_text(encoding='utf-8')
for selector in ('.menu-overlay', '.menu-link:focus-visible', '@media(max-width:900px)', '@media(prefers-reduced-motion:reduce)'):
    if selector not in css:
        errors.append(f'platform-menu.css missing responsive/accessibility rule: {selector}')

if errors:
    print('Platform navigation QA failed:', file=sys.stderr)
    for error in errors:
        print(f'- {error}', file=sys.stderr)
    raise SystemExit(1)
print(f'Platform navigation QA passed for {len(pages)} HTML pages')
