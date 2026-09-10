# coding: utf-8
"""Prepare the review artifact for the GitHub Pages project URL.

Before hipstudio.hu is connected as a custom domain, GitHub Pages serves this
repository below /HIPSTUDIO/. The production source intentionally keeps root-relative
links for hipstudio.hu, so this review-only step rewrites local HTML attributes for
the temporary project path without changing canonicals or source content.
"""
from pathlib import Path
import re, shutil

R=Path(__file__).resolve().parents[1]
SRC=R/'dist-platform'
DST=R/'dist-pages-review'
PREFIX='/HIPSTUDIO'

if not SRC.exists():
    raise SystemExit('dist-platform missing; run build:platform first')
if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC,DST)

attr=re.compile(r'(?P<attr>\b(?:href|src|action)=["\'])/(?P<path>(?!/)[^"\']*)')
changed=0
for p in DST.rglob('*.html'):
    raw=p.read_text(encoding='utf-8')
    rewritten,n=attr.subn(lambda m: f"{m.group('attr')}{PREFIX}/{m.group('path')}",raw)
    if n:
        p.write_text(rewritten,encoding='utf-8')
        changed+=n

# GitHub Pages serves unknown paths through its own 404 handling; preserve our custom
# document for manual QA as well.
print(f'Prepared GitHub Pages review artifact: prefix={PREFIX}/ rewritten_attributes={changed}')
