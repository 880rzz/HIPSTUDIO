# coding: utf-8
"""Prepare the root-path GitHub Pages production artifact for www.hipstudio.hu."""
from pathlib import Path
import shutil

R = Path(__file__).resolve().parents[1]
SRC = R / 'dist-platform'
DST = R / 'dist-pages-production'

if not SRC.exists():
    raise SystemExit('dist-platform missing; run the production platform build first')
if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

(DST / 'CNAME').write_text('www.hipstudio.hu\n', encoding='utf-8')
root = '''<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><link rel="canonical" href="https://www.hipstudio.hu/hu/"><meta http-equiv="refresh" content="0;url=/hu/"><title>HIPStudio</title></head><body><main><p><a href="/hu/">HIPStudio</a></p></main></body></html>'''
(DST / 'index.html').write_text(root, encoding='utf-8')
print('Prepared dist-pages-production for https://www.hipstudio.hu')
