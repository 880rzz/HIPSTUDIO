# coding: utf-8
"""Render HIPStudio historical/reference logos from repository-local assets.

The Wix URLs in audit/client-logo-manifest.json are provenance only. Public pages
must load logo images exclusively from the repository-built /assets/logos/ path.
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
        raise SystemExit(f"Missing local partner logo: {logo.relative_to(R)}")
    shutil.copyfile(logo, DST / logo.name)

css_src = R / 'assets/partners.css'
shutil.copyfile(css_src, D / 'assets/partners.css')

COPY = {
    'hu': {
        'eyebrow':'Referenciák',
        'title':'Márkák, amelyekkel a HIPStudio története során dolgoztunk',
        'body':'Az alábbi logók a korábbi HIPStudio partner-/referenciaoldal dokumentált anyagából származnak. Történeti referenciaként mutatjuk őket; a megjelenés önmagában nem állítás jelenlegi ügyfél- vagy partnerkapcsolatról.',
        'alt':'HIPStudio történeti referencia logó'
    },
    'en': {
        'eyebrow':'References',
        'title':'Brands HIPStudio has worked with over its history',
        'body':'These logos come from the documented material of the former HIPStudio partners/references page. They are shown as historical references; inclusion does not by itself claim a current client or partner relationship.',
        'alt':'HIPStudio historical reference logo'
    },
    'de': {
        'eyebrow':'Referenzen',
        'title':'Marken, mit denen HIPStudio im Laufe seiner Geschichte gearbeitet hat',
        'body':'Diese Logos stammen aus dem dokumentierten Material der früheren HIPStudio-Partner-/Referenzseite. Sie werden als historische Referenzen gezeigt; die Darstellung allein behauptet keine aktuelle Kunden- oder Partnerbeziehung.',
        'alt':'Historisches HIPStudio-Referenzlogo'
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
        '<section class="section partner-references" data-partner-references>'
        f'<div class="section-head"><p class="eyebrow">{copy["eyebrow"]}</p><h2>{copy["title"]}</h2>'
        f'<p class="partner-note">{copy["body"]}</p></div>'
        f'<div class="partner-logo-grid">{logos}</div></section>'
    )
    marker = '<footer class="footer">'
    if 'data-partner-references' not in html:
        html = html.replace(marker, block + marker)
    page.write_text(html)

print(f'Rendered {len(MANIFEST)} repository-local historical/reference logos on 3 About pages')
