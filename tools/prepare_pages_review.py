# coding: utf-8
"""Prepare the noindex GitHub Pages review artifact.

The same review build must work in two hosting modes:
- GitHub project Pages: /HIPSTUDIO/
- approved temporary custom domain: /

PAGES_PREFIX selects the public path. It defaults to /HIPSTUDIO so ordinary
project-path validation remains unchanged. Production canonicals are never rewritten.
"""
from pathlib import Path
import os, re, shutil

R=Path(__file__).resolve().parents[1]
SRC=R/'dist-platform'
DST=R/'dist-pages-review'
raw_prefix=os.environ.get('PAGES_PREFIX','/HIPSTUDIO').strip() or '/'
PREFIX='/' if raw_prefix=='/' else '/' + raw_prefix.strip('/')

if not SRC.exists():
    raise SystemExit('dist-platform missing; run build:platform first')
if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC,DST)

attr=re.compile(r'(?P<attr>\b(?:href|src|action)=["\'])/(?P<path>(?!/)[^"\']*)')
changed=0
if PREFIX != '/':
    for p in DST.rglob('*.html'):
        raw=p.read_text(encoding='utf-8')
        rewritten,n=attr.subn(lambda m: f"{m.group('attr')}{PREFIX}/{m.group('path')}",raw)
        if n:
            p.write_text(rewritten,encoding='utf-8')
            changed+=n

root_target='/hu/' if PREFIX=='/' else f'{PREFIX}/hu/'
root_index=DST/'index.html'
root_index.write_text(
    '<!doctype html><html lang="hu"><head><meta charset="utf-8">'
    '<meta name="robots" content="noindex,nofollow">'
    f'<meta http-equiv="refresh" content="0; url={root_target}">'
    '<title>HIPStudio review</title></head><body>'
    f'<p><a href="{root_target}">HIPStudio review megnyitása</a></p>'
    '</body></html>',
    encoding='utf-8'
)

print(f'Prepared GitHub Pages review artifact: prefix={PREFIX} rewritten_attributes={changed}; root entry created')
