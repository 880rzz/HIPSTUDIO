# coding: utf-8
"""Render HIPStudio partner logos from repository-local assets.

The Wix URLs in audit/client-logo-manifest.json are provenance only. Public pages
must load logo images exclusively from the repository-built /assets/logos/ path.
Flúgos sponsor relationships are a separate content category and are not rendered
by this HIPStudio partner block.
"""
from pathlib import Path
import json, shutil

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
MANIFEST = json.loads((R / 'audit/client-logo-manifest.json').read_text())
SRC = R / 'assets/logos'
DST = D / 'assets/logos'
DST.mkdir(parents=True, exist_ok=True)

for item in MANIFEST:
    logo = SRC / f"{item['id']}.webp"
    if not logo.exists():
        raise SystemExit(f"Missing local HIPStudio partner logo: {logo.relative_to(R)}")
    shutil.copyfile(logo, DST / logo.name)

css_src = R / 'assets/partners.css'
shutil.copyfile(css_src, D / 'assets/partners.css')

COPY = {
    'hu': {
        'eyebrow':'Partnereink',
        'title':'Akikkel már együtt dolgoztunk',
        'body':'Dokumentált korábbi együttműködések. A logók nem jelentenek jelenlegi megbízást vagy ajánlást.',
        'alt':'HIPStudio partner logó'
    },
    'en': {
        'eyebrow':'Partners',
        'title':'Selected collaborations',
        'body':'Documented previous collaborations. Logos do not imply a current engagement or endorsement.',
        'alt':'HIPStudio partner logo'
    },
    'de': {
        'eyebrow':'Partner',
        'title':'Ausgewählte Zusammenarbeiten',
        'body':'Dokumentierte frühere Zusammenarbeiten. Logos bedeuten keinen aktuellen Auftrag und keine Empfehlung.',
        'alt':'HIPStudio Partnerlogo'
    }
}

ROUTES = {'hu':'partnerek','en':'partners','de':'partner'}
for lang, slug in ROUTES.items():
    page = D / lang / slug / 'index.html'
    html = page.read_text()
    if '/assets/partners.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/assets/partners.css"></head>')
    copy = COPY[lang]
    logos = ''.join(
        f'<div class="partner-logo"><img src="/assets/logos/{item["id"]}.webp" alt="{copy["alt"]} {i:02d}" loading="lazy" decoding="async"></div>'
        for i, item in enumerate(MANIFEST, 1)
    )
    block = (
        '<section class="section hipstudio-partners" data-hipstudio-partners>'
        f'<div class="section-head"><p class="eyebrow">{copy["eyebrow"]}</p><h2>{copy["title"]}</h2>'
        f'<p class="partner-note">{copy["body"]}</p></div>'
        f'<div class="partner-logo-grid">{logos}</div></section>'
    )
    marker = '<footer class="footer">'
    if 'data-hipstudio-partners' not in html:
        html = html.replace(marker, block + marker)
    page.write_text(html)

print(f'Rendered {len(MANIFEST)} repository-local HIPStudio partner logos on 3 About pages; Flúgos sponsors remain a separate category')
