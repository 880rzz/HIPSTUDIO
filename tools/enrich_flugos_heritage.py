# coding: utf-8
from pathlib import Path
from html import escape
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/platform.json').read_text())
EXP = next(p for p in DATA['pillars'] if p['key'] == 'experiences')
HER = EXP.get('heritage', {})

ROUTES = {'hu':'hu/vallalati-elmenyek/index.html','en':'en/corporate-experiences/index.html','de':'de/unternehmenserlebnisse/index.html'}
LABELS = {
 'hu': {'eyebrow':'Flúgos története és csapata','title':'2009 óta nem csak programokat, hanem közös történeteket építünk.','founders':'Alapítók','milestones':'Történeti mérföldkövek'},
 'en': {'eyebrow':'Flúgos history and team','title':'Since 2009, we have built more than programmes — we have built shared stories.','founders':'Founders','milestones':'Historical milestones'},
 'de': {'eyebrow':'Flúgos Geschichte und Team','title':'Seit 2009 entstehen nicht nur Programme, sondern gemeinsame Geschichten.','founders':'Gründer','milestones':'Historische Meilensteine'}
}

def e(v): return escape(str(v), quote=True)

for lang, rel in ROUTES.items():
    path = D / rel
    if not path.exists():
        raise SystemExit(f'missing generated experience page: {path}')
    html = path.read_text()
    founders = ' · '.join(HER.get('founders', []))
    milestones = ''.join(f'<li>{e(x)}</li>' for x in HER.get('historicalMilestones', {}).get(lang, []))
    copy = HER.get('teamPrinciple', {}).get(lang, '')
    labels = LABELS[lang]
    block = (
      '<section class="section flugos-heritage" data-flugos-heritage="true">'
      f'<div class="section-head"><p class="eyebrow">{e(labels["eyebrow"])}</p><h2>{e(labels["title"])}</h2><p>{e(copy)}</p></div>'
      '<div class="pillar-grid">'
      f'<article class="pillar"><p class="eyebrow">{e(labels["founders"])}</p><h3>{e(founders)}</h3></article>'
      f'<article class="pillar"><p class="eyebrow">{e(labels["milestones"])}</p><ul class="service-list">{milestones}</ul></article>'
      '</div></section>'
    )
    marker = '<section class="cta">'
    if 'data-flugos-heritage="true"' not in html:
        if marker not in html:
            raise SystemExit(f'CTA marker missing in {path}')
        html = html.replace(marker, block + marker, 1)
        path.write_text(html)

print('Flúgos founder, team and heritage block rendered on HU/EN/DE experience pages')
