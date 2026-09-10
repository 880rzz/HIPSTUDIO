# coding: utf-8
"""Render the Flúgos sponsor/supporter history separately from HIPStudio partners."""
from pathlib import Path
from html import escape
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/flugos-sponsors.json').read_text())

ROUTES = {
    'hu': 'hu/vallalati-elmenyek/index.html',
    'en': 'en/corporate-experiences/index.html',
    'de': 'de/unternehmenserlebnisse/index.html',
}
COPY = {
    'hu': {
        'eyebrow': 'Flúgos szponzorok és támogatók',
        'title': 'A Flúgos Futam történetét szponzorok és támogatók is segítették.',
        'facts': 'Dokumentált szponzori múlt',
    },
    'en': {
        'eyebrow': 'Flúgos sponsors and supporters',
        'title': 'Sponsors and supporters have also contributed to the history of Flúgos Futam.',
        'facts': 'Documented sponsorship history',
    },
    'de': {
        'eyebrow': 'Flúgos Sponsoren und Unterstützer',
        'title': 'Auch Sponsoren und Unterstützer haben zur Geschichte des Flúgos Futam beigetragen.',
        'facts': 'Dokumentierte Sponsoring-Historie',
    },
}

def e(value):
    return escape(str(value), quote=True)

for lang, rel in ROUTES.items():
    page = D / rel
    if not page.exists():
        raise SystemExit(f'missing generated experience page: {page}')
    html = page.read_text()
    c = COPY[lang]
    facts = ''.join(f'<li>{e(item[lang])}</li>' for item in DATA.get('verifiedFacts', []))
    block = (
        '<section class="section flugos-sponsors" data-flugos-sponsors="historical">'
        f'<div class="section-head"><p class="eyebrow">{e(c["eyebrow"])}</p>'
        f'<h2>{e(c["title"])}</h2><p>{e(DATA["notes"][lang])}</p></div>'
        f'<div class="pillar"><p class="eyebrow">{e(c["facts"])}</p><ul class="service-list">{facts}</ul></div>'
        '</section>'
    )
    marker = '<section class="cta">'
    if 'data-flugos-sponsors=' not in html:
        if marker not in html:
            raise SystemExit(f'CTA marker missing in {page}')
        html = html.replace(marker, block + marker, 1)
        page.write_text(html)

print('Flúgos sponsor/supporter history rendered separately on HU/EN/DE experience pages')
