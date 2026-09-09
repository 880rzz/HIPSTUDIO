# coding: utf-8
"""Inject source-governed proof blocks into selected review platform pages.

This layer publishes only evidence-registry entries marked publishable_qualified.
It never turns logo inventories into client claims or creates case studies.
"""
from pathlib import Path
from html import escape
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/evidence-registry.json').read_text())

ROUTES = {
    'about': {'hu':'hu/rolunk/index.html','en':'en/about/index.html','de':'de/ueber-uns/index.html'},
    'experiences': {'hu':'hu/vallalati-elmenyek/index.html','en':'en/corporate-experiences/index.html','de':'de/unternehmenserlebnisse/index.html'},
    'corporate-experience-design': {
        'hu':'hu/megoldasok/corporate-experience-design/index.html',
        'en':'en/solutions/corporate-experience-design/index.html',
        'de':'de/loesungen/corporate-experience-design/index.html'
    }
}

LABELS = {
    'hu': {'proof':'Forrásolt bizonyíték', 'heritage':'Igazolt márkatörténet', 'history':'Történeti Flúgos bizonyíték', 'note':'A történeti adatok nem jelentenek jelenlegi éves volument, ügyfélszámot vagy garantált üzleti eredményt.'},
    'en': {'proof':'Source-backed evidence', 'heritage':'Verified brand heritage', 'history':'Historical Flúgos evidence', 'note':'Historical figures do not represent current annual volume, current client count or guaranteed business outcomes.'},
    'de': {'proof':'Quellenbasierter Nachweis', 'heritage':'Verifizierte Markenhistorie', 'history':'Historischer Flúgos-Nachweis', 'note':'Historische Zahlen stehen nicht für aktuelles Jahresvolumen, aktuelle Kundenzahl oder garantierte Geschäftsergebnisse.'}
}


def e(v): return escape(str(v), quote=True)

def evidence(ids):
    by_id = {x['id']: x for x in DATA['evidence']}
    result = []
    for i in ids:
        item = by_id[i]
        if item['status'] != 'publishable_qualified':
            raise SystemExit(f'Evidence {i} is not publishable_qualified')
        result.append(item)
    return result

def block(lang, title, items, historical=False):
    rows = ''.join(
        f'<div class="card"><p>{e(item["claim"][lang])}</p><p class="note">Evidence ID: {e(item["id"])}</p></div>'
        for item in items
    )
    note = f'<p class="note">{e(LABELS[lang]["note"])}</p>' if historical else ''
    return f'<section class="section" data-evidence-layer="source-backed"><div class="section-head"><p class="eyebrow">{e(LABELS[lang]["proof"])}</p><h2>{e(title)}</h2></div><div class="cards">{rows}</div>{note}</section>'

def inject(path, html_block):
    file = D / path
    html = file.read_text()
    marker = '<section class="cta">'
    if marker not in html:
        raise SystemExit(f'CTA marker missing: {path}')
    html = html.replace(marker, html_block + marker, 1)
    file.write_text(html)

heritage = evidence(['hipstudio-founded-2006','hipstudio-founder'])
flugos = evidence(['flugos-history-2009','flugos-historical-programme-scale'])
count = 0
for lang in ('hu','en','de'):
    inject(ROUTES['about'][lang], block(lang, LABELS[lang]['heritage'], heritage))
    count += 1
    inject(ROUTES['experiences'][lang], block(lang, LABELS[lang]['history'], flugos, historical=True))
    count += 1
    inject(ROUTES['corporate-experience-design'][lang], block(lang, LABELS[lang]['history'], flugos, historical=True))
    count += 1

manifest = json.loads((D / 'platform-build.json').read_text())
manifest['evidenceLayer'] = {
    'version': DATA['version'],
    'publishableQualified': len([x for x in DATA['evidence'] if x['status']=='publishable_qualified']),
    'caseStudiesPublished': len(DATA['caseStudies']),
    'enrichedPages': count,
    'logoIsNotCaseStudy': DATA['policy']['logoIsNotCaseStudy']
}
(D / 'platform-build.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print(f'Evidence enrichment applied to {count} localized pages; published case studies={len(DATA["caseStudies"])}')
