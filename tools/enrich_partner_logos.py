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
        'title':'HIPStudio partnerek',
        'body':'Az itt látható logók a HIPStudio partneroldalának dokumentált anyagából származnak. A képeket saját GitHub assetként tároljuk; a publikus oldal nem tölt be logót a Wix rendszeréből.',
        'alt':'HIPStudio partner logó'
    },
    'en': {
        'eyebrow':'Partners',
        'title':'HIPStudio partners',
        'body':'The logos shown here come from the documented material of the HIPStudio partners page. The images are stored as repository-local GitHub assets; the public site does not load partner logos from Wix.',
        'alt':'HIPStudio partner logo'
    },
    'de': {
        'eyebrow':'Partner',
        'title':'HIPStudio Partner',
        'body':'Die hier gezeigten Logos stammen aus dem dokumentierten Material der HIPStudio-Partnerseite. Die Bilder werden als lokale GitHub-Assets gespeichert; die öffentliche Website lädt keine Partnerlogos aus Wix.',
        'alt':'HIPStudio Partnerlogo'
    }
}

ROUTES = {'hu':'rolunk','en':'about','de':'ueber-uns'}
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
