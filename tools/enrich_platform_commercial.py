# coding: utf-8
"""Add review-safe commercial content to core HIPStudio platform pages.

This is a deterministic post-build enrichment layer. It does not change routes,
canonical URLs, schema, publication mode or deployment behavior.
"""
from pathlib import Path
from html import escape
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/commercial-content.json').read_text())

LANGS = ['hu', 'en', 'de']
ROUTES = {
    'home': {'hu':'/hu/','en':'/en/','de':'/de/'},
    'about': {'hu':'/hu/rolunk/','en':'/en/about/','de':'/de/ueber-uns/'},
    'business': {'hu':'/hu/uzleti-mukodes/','en':'/en/business-operations/','de':'/de/business-operations/'},
    'creative': {'hu':'/hu/kreativ-tartalom/','en':'/en/creative-content/','de':'/de/creative-content/'},
    'experiences': {'hu':'/hu/vallalati-elmenyek/','en':'/en/corporate-experiences/','de':'/de/unternehmenserlebnisse/'}
}

LABELS = {
    'problem': {'hu':'Miből indulunk ki?','en':'Where we start','de':'Womit wir starten'},
    'benefits': {'hu':'Egy partneri rendszer előnye','en':'The value of one connected partner','de':'Der Wert eines vernetzten Partners'},
    'problemLabel': {'hu':'Tipikus helyzet','en':'Typical situation','de':'Typische Situation'},
    'outcomeLabel': {'hu':'Célállapot','en':'Target outcome','de':'Zielbild'},
    'readMore': {'hu':'Megnézem ezt a területet','en':'Explore this area','de':'Diesen Bereich ansehen'},
    'integration': {'hu':'A HIPStudio integráció logikája','en':'How the HIPStudio integration works','de':'Wie die HIPStudio-Integration funktioniert'}
}

def e(value):
    return escape(str(value), quote=True)

def file_for(route):
    return D / route.strip('/') / 'index.html'

def insert_before_final_cta(raw, block):
    marker = '<section class="cta">'
    if marker in raw:
        head, tail = raw.rsplit(marker, 1)
        return head + block + marker + tail
    return raw.replace('</main>', block + '</main>', 1)

def cards(items, lang):
    out = []
    for item in items:
        href = ROUTES[item['pillar']][lang]
        out.append(
            f'''<a class="card" href="{e(href)}"><p class="eyebrow">{e(LABELS['problem'][lang])}</p>'''
            f'''<h3>{e(item['title'][lang])}</h3><p>{e(item['body'][lang])}</p>'''
            f'''<span>{e(item['cta'][lang])} →</span></a>'''
        )
    return ''.join(out)

def enrich_home(lang):
    path = file_for(ROUTES['home'][lang])
    raw = path.read_text()
    home = DATA['home']
    problem = f'''<section class="section" data-commercial-layer="problem-led-home"><div class="section-head"><p class="eyebrow">{e(LABELS['problem'][lang])}</p><h2>{e(home['problemIntro']['title'][lang])}</h2><p>{e(home['problemIntro']['intro'][lang])}</p></div><div class="cards">{cards(home['problemCards'],lang)}</div></section>'''
    benefits = ''.join(
        f'''<div><h3>{e(item['title'][lang])}</h3><p>{e(item['body'][lang])}</p></div>'''
        for item in home['partnerBenefits']['items']
    )
    benefit_block = f'''<section class="section" data-commercial-layer="partner-benefits"><div class="section-head"><p class="eyebrow">{e(LABELS['benefits'][lang])}</p><h2>{e(home['partnerBenefits']['title'][lang])}</h2></div><div class="trust">{benefits}</div></section>'''
    raw = insert_before_final_cta(raw, problem + benefit_block)
    path.write_text(raw)

def enrich_about(lang):
    path = file_for(ROUTES['about'][lang])
    raw = path.read_text()
    about = DATA['about']
    sections = ''.join(
        f'''<div class="card"><h3>{e(item['title'][lang])}</h3><p>{e(item['body'][lang])}</p></div>'''
        for item in about['sections']
    )
    block = f'''<section class="section" data-commercial-layer="integration-story"><div class="section-head"><p class="eyebrow">{e(LABELS['integration'][lang])}</p><h2>{e(about['title'][lang])}</h2><p>{e(about['lead'][lang])}</p></div><div class="cards">{sections}</div></section>'''
    raw = insert_before_final_cta(raw, block)
    path.write_text(raw)

def enrich_pillar(key, lang):
    path = file_for(ROUTES[key][lang])
    raw = path.read_text()
    p = DATA['pillars'][key]
    block = f'''<section class="section" data-commercial-layer="pillar-value"><div class="trust"><div><p class="eyebrow">{e(LABELS['problemLabel'][lang])}</p><h2>{e(p['problem'][lang])}</h2></div><div><p class="eyebrow">{e(LABELS['outcomeLabel'][lang])}</p><h2>{e(p['outcome'][lang])}</h2></div></div></section>'''
    raw = insert_before_final_cta(raw, block)
    path.write_text(raw)

if not (D / 'platform-build.json').exists():
    raise SystemExit('dist-platform missing; run build_platform.py first')

for lang in LANGS:
    enrich_home(lang)
    enrich_about(lang)
    for pillar in ('business','creative','experiences'):
        enrich_pillar(pillar,lang)

manifest_path = D / 'platform-build.json'
manifest = json.loads(manifest_path.read_text())
manifest['commercialContent'] = {
    'version': DATA['version'],
    'status': DATA['status'],
    'enrichedPages': 15,
    'problemCards': len(DATA['home']['problemCards'])
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print('Commercial content enrichment applied to 15 localized core pages')
