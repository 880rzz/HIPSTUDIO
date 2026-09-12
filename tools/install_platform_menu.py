#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist-platform'
ASSET=ROOT/'assets'/'platform-menu.js'
TARGET=DIST/'assets'/'platform-menu.js'
SCRIPT='<script src="/assets/platform-menu.js" defer></script>'

if not DIST.exists():
    raise SystemExit('dist-platform missing; build platform before installing menu')
if not ASSET.exists():
    raise SystemExit('assets/platform-menu.js missing')
TARGET.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(ASSET,TARGET)

count=0
for html in DIST.rglob('*.html'):
    text=html.read_text()
    if SCRIPT in text:
        continue
    if '</head>' not in text:
        raise SystemExit(f'No </head> in {html}')
    text=text.replace('</head>',SCRIPT+'</head>',1)
    html.write_text(text)
    count+=1
print(f'Installed full-screen navigation on {count} platform HTML files')
