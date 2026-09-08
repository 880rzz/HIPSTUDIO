# coding: utf-8
"""Build the review-only unified HIPStudio master platform.

No network or deployment is performed. HIPStudio is the approved master brand;
Business and Flúgos remain separately identifiable specialist pillars until any
legal/entity relationships are independently verified.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json, os, shutil

R = Path(__file__).resolve().parents[1]
DATA = json.loads((R / 'content/platform.json').read_text())
MODE = os.environ.get('BUILD_MODE', 'review')
BASE = os.environ.get('PLATFORM_URL', DATA.get('masterDomain', 'https://www.hipstudio.hu')).rstrip('/')

if MODE not in ('review', 'production'):
    raise SystemExit('BUILD_MODE must be review or production')
if not BASE.startswith('https://') or urlsplit(BASE).query or urlsplit(BASE).fragment:
    raise SystemExit('PLATFORM_URL must be an HTTPS origin')
if MODE == 'production':
    missing = []
    if DATA.get('masterBrandApprovalRequired') and os.environ.get('PLATFORM_MASTER_BRAND_APPROVED') != '1':
        missing.append('masterBrandApproval')
    if os.environ.get('PLATFORM_PUBLICATION_APPROVED') != '1':
        missing.append('publicationApproval')
    if missing:
        raise SystemExit('Platform production blocked: ' + ', '.join(missing))

D = R / 'dist-platform'
if D.exists():
    shutil.rmtree(D)
(D / 'assets').mkdir(parents=True)
shutil.copyfile(R / 'assets/platform.css', D / 'assets/platform.css')

LANGS = ['hu', 'en', 'de']
LOCALES = {'hu': 'hu_HU', 'en': 'en_GB', 'de': 'de_DE'}
ROUTES = {
    'home': {'hu':'', 'en':'', 'de':''},
    'business': {'hu':'uzleti-mukodes', 'en':'business-operations', 'de':'business-operations'},
    'creative': {'hu':'kreativ-tartalom', 'en':'creative-content', 'de':'creative-content'},
    'experiences': {'hu':'vallalati-elmenyek', 'en':'corporate-experiences', 'de':'unternehmenserlebnisse'},
    'about': {'hu':'rolunk', 'en':'about', 'de':'ueber-uns'},
    'contact': {'hu':'kapcsolat', 'en':'contact', 'de':'kontakt'},
    'trust': {'hu':'ai-trust', 'en':'ai-trust', 'de':'ai-trust'}
}

UI = {
    'review': {'hu':'Platform review build · nincs publikálva', 'en':'Platform review build · not published', 'de':'Platform-Review-Build · nicht veröffentlicht'},
    'home': {'hu':'Főoldal','en':'Home','de':'Start'},
    'about': {'hu':'Hogyan dolgozunk','en':'How we work','de':'So arbeiten wir'},
    'contact': {'hu':'Konzultáció','en':'Consultation','de':'Beratung'},
    'trust': {'hu':'AI Trust','en':'AI Trust','de':'AI Trust'},
    'audience': {'hu':'Kinek szól','en':'Who it is for','de':'Für wen'},
    'pillars': {'hu':'Három szakmai pillér','en':'Three specialist pillars','de':'Drei Fachsäulen'},
    'model': {'hu':'Egy HIPStudio rendszer','en':'One HIPStudio system','de':'Ein HIPStudio-System'},
    'services': {'hu':'Fókuszterületek','en':'Focus areas','de':'Schwerpunkte'},
    'why': {'hu':'Miért egy rendszerben?','en':'Why one system?','de':'Warum in einem System?'},
    'ctaTitle': {'hu':'Nézzük meg, hol tudunk több terhet levenni a cégedről.','en':'Let us identify where one connected partner can remove more operational load.','de':'Finden wir heraus, wo ein vernetzter Partner mehr operative Last übernehmen kann.'},
    'back': {'hu':'Vissza a HIPStudio rendszerhez','en':'Back to the HIPStudio system','de':'Zurück zum HIPStudio-System'},
    'specialist': {'hu':'Szakmai pillér','en':'Specialist pillar','de':'Fachsäule'},
    'evidence': {'hu':'Bizonyíték és felelősség','en':'Evidence and responsibility','de':'Nachweis und Verantwortung'},
    'navMain': {'hu':'Fő navigáció','en':'Main navigation','de':'Hauptnavigation'},
    'navLang': {'hu':'Nyelvválasztó','en':'Languages','de':'Sprachauswahl'},
    'navFooter': {'hu':'Lábléc navigáció','en':'Footer navigation','de':'Fußnavigation'}
}

PILLARS = {p['key']: p for p in DATA['pillars']}
PAGES = []

def e(value): return escape(str(value), quote=True)
def route(key, lang):
    slug = ROUTES[key][lang]
    return f'/{lang}/' + (slug + '/' if slug else '')
def absolute(key, lang): return BASE + route(key, lang)
def href(key, lang): return route(key, lang)

def page_title(key, lang):
    if key == 'home': return DATA['hero']['title'][lang]
    if key in PILLARS: return PILLARS[key]['title'][lang]
    if key == 'about': return UI['about'][lang]
    if key == 'contact': return DATA['primaryCta'][lang]
    return UI['trust'][lang]

def meta_title(key, lang):
    if key == 'home':
        return {
            'hu':'HIPStudio | Business, Creative és vállalati élmények',
            'en':'HIPStudio | Business, Creative and corporate experiences',
            'de':'HIPStudio | Business, Creative und Unternehmenserlebnisse'
        }[lang]
    return f'{page_title(key, lang)} | {DATA["workingMasterBrand"]}'

def page_desc(key, lang):
    if key == 'home': return DATA['hero']['intro'][lang]
    if key in PILLARS: return PILLARS[key]['intro'][lang]
    if key == 'about': return DATA['integrationStory']['reason'][lang]
    if key == 'contact': return DATA['positioning'][lang]
    return {
        'hu':'Átlátható AI-használati, emberi kontroll- és adatvédelmi elvek a HIPStudio rendszerhez.',
        'en':'Transparent AI-use, human-control and privacy principles for the HIPStudio system.',
        'de':'Transparente Prinzipien zu KI-Nutzung, menschlicher Kontrolle und Datenschutz für das HIPStudio-System.'
    }[lang]

def language_links(key, lang):
    return ''.join(f'<a lang="{l}" hreflang="{l}" href="{e(href(key,l))}"' + (' aria-current="page"' if l == lang else '') + f'>{l.upper()}</a>' for l in LANGS)

def nav(key, lang):
    items = ['business','creative','experiences','about','contact']
    return ''.join(f'<a href="{e(href(k,lang))}"' + (' aria-current="page"' if k == key else '') + f'>{e(page_title(k,lang) if k in PILLARS else UI[k][lang])}</a>' for k in items)

def graph(key, lang, title, desc):
    url = absolute(key, lang)
    website_id = BASE + '/#website'
    organization_id = 'https://www.hipstudio.hu/#organization'
    nodes = [
        {'@type':'WebSite','@id':website_id,'name':'HIPStudio','url':BASE+'/' ,'inLanguage':LANGS,'publisher':{'@id':organization_id}},
        {'@type':['Organization','ProfessionalService'],'@id':organization_id,'name':'HIPStudio','url':'https://www.hipstudio.hu/','foundingDate':'2006-02-27','sameAs':['https://www.wikidata.org/wiki/Q138482177']},
        {'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':lang,'isPartOf':{'@id':website_id}},
        {'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':UI['home'][lang],'item':absolute('home',lang)}]}
    ]
    if key != 'home':
        nodes[3]['itemListElement'].append({'@type':'ListItem','position':2,'name':title,'item':url})
    if key in PILLARS:
        p = PILLARS[key]
        brand_id = BASE + f'/#brand-{key}'
        brand = {'@type':'Brand','@id':brand_id,'name':p['brand']}
        if key == 'creative':
            brand = {'@type':'Brand','@id':brand_id,'name':'HIPStudio Creative','url':BASE + route('creative',lang)}
        elif key == 'experiences':
            brand['url'] = 'https://www.flugos.hu/'
        elif key == 'business':
            brand['url'] = BASE + route('business',lang)
        nodes.append(brand)
        nodes.append({'@type':'Service','@id':url+'#service','name':p['title'][lang],'description':p['intro'][lang],'url':url,'serviceType':p['label'][lang]})
        nodes[2]['mainEntity'] = {'@id':url+'#service'}
    return {'@context':'https://schema.org','@graph':nodes}

def shell(key, lang, body):
    title = page_title(key, lang); desc = page_desc(key, lang); url = absolute(key, lang)
    alternates = ''.join(f'<link rel="alternate" hreflang="{l}" href="{e(absolute(key,l))}">' for l in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{e(absolute(key,"hu"))}">'
    ld = json.dumps(graph(key,lang,title,desc), ensure_ascii=False, separators=(',',':')).replace('<','\\u003c')
    review = f'<div class="review">{e(UI["review"][lang])}</div>' if MODE == 'review' else ''
    html = f'''<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(meta_title(key,lang))}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="{'noindex,nofollow' if MODE=='review' else 'index,follow'}"><link rel="canonical" href="{e(url)}">{alternates}<meta property="og:type" content="website"><meta property="og:locale" content="{LOCALES[lang]}"><meta property="og:site_name" content="HIPStudio"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><link rel="stylesheet" href="/assets/platform.css"><script type="application/ld+json">{ld}</script></head><body><a class="skip" href="#main">Skip</a>{review}<header class="header"><a class="brand" href="{e(href('home',lang))}">HIPStudio</a><nav class="nav" aria-label="{e(UI['navMain'][lang])}">{nav(key,lang)}</nav><nav class="langs" aria-label="{e(UI['navLang'][lang])}">{language_links(key,lang)}</nav></header><main id="main">{body}</main><footer class="footer"><strong>HIPStudio</strong><nav aria-label="{e(UI['navFooter'][lang])}">{nav(key,lang)}</nav><p class="legal-note">Review architecture: HIPStudio is the master brand. Business and Flúgos are presented as specialist pillars; no unverified legal-entity or ownership relationship is asserted.</p></footer></body></html>'''
    out = D / route(key,lang).strip('/') / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    PAGES.append({'key':key,'lang':lang,'path':route(key,lang),'canonical':url})

def cta(lang):
    return f'<section class="cta"><p class="eyebrow">{e(DATA["positioning"][lang])}</p><h2>{e(UI["ctaTitle"][lang])}</h2><a class="button" href="{e(href("contact",lang))}">{e(DATA["primaryCta"][lang])} →</a></section>'

def pillar_card(p, lang, index):
    return f'''<a class="pillar" href="{e(href(p['key'],lang))}"><span class="number">0{index} · {e(p['brand'])}</span><p class="eyebrow">{e(p['label'][lang])}</p><h3>{e(p['title'][lang])}</h3><p>{e(p['intro'][lang])}</p><span class="arrow" aria-hidden="true">↗</span></a>'''

def pillar_page(p, lang):
    services = ''.join(f'<li>{e(s)}</li>' for s in p['services'][lang])
    heritage = ''
    if p['key'] == 'creative':
        heritage = f'<p class="note"><strong>{e(DATA["heritage"]["headline"][lang])}</strong> {e(DATA["heritage"]["claim"][lang])}</p>'
    elif p['key'] == 'experiences':
        heritage = '<p class="note">Flúgos historical material is preserved separately from the current B2B offer and remains time-qualified.</p>'
    return f'''<section class="page-hero"><a class="back" href="{e(href('home',lang))}">← {e(UI['back'][lang])}</a><p class="eyebrow">{e(p['brand'])} · {e(p['label'][lang])}</p><h1>{e(p['title'][lang])}</h1><p class="lead">{e(p['intro'][lang])}</p></section><section class="section"><div class="section-head"><h2>{e(p['promise'][lang])}</h2><p>{e(DATA['crossSell'][lang])}</p></div><h3>{e(UI['services'][lang])}</h3><ul class="service-list">{services}</ul>{heritage}</section>{cta(lang)}'''

for lang in LANGS:
    cards = ''.join(pillar_card(p,lang,i+1) for i,p in enumerate(DATA['pillars']))
    flow_labels = {'hu':['Működés','Növekedés','Láthatóság','Kapcsolódás'],'en':['Operate','Grow','Be seen','Connect'],'de':['Betreiben','Wachsen','Sichtbar sein','Verbinden']}[lang]
    flow = ''.join(f'<div><strong>0{i+1}</strong><span>{e(label)}</span></div>' for i,label in enumerate(flow_labels))
    heritage = f'''<section class="section"><div class="section-head"><p class="eyebrow">2006 → 2026</p><h2>{e(DATA['heritage']['headline'][lang])}</h2><p>{e(DATA['heritage']['claim'][lang])}</p></div></section>'''
    integration = f'''<section class="dark"><div class="section"><div class="section-head"><h2>{e(DATA['integrationStory']['title'][lang])}</h2><p>{e(DATA['integrationStory']['reason'][lang])}</p></div><div class="flow">{flow}</div></div></section>'''
    home = f'''<section class="hero"><div><p class="eyebrow">{e(DATA['positioning'][lang])}</p><h1>{e(DATA['hero']['title'][lang])}</h1><p class="lead">{e(DATA['hero']['intro'][lang])}</p><a class="button" href="{e(href('contact',lang))}">{e(DATA['primaryCta'][lang])} →</a></div><aside class="hero-side"><p class="eyebrow">{e(UI['audience'][lang])}</p><p>{e(DATA['audience'][lang])}</p></aside></section>{heritage}<section class="section"><div class="section-head"><h2>{e(UI['pillars'][lang])}</h2><p>{e(DATA['crossSell'][lang])}</p></div><div class="pillars">{cards}</div></section>{integration}{cta(lang)}'''
    shell('home',lang,home)
    for p in DATA['pillars']:
        shell(p['key'],lang,pillar_page(p,lang))
    about = f'''<section class="page-hero"><p class="eyebrow">2006 → 2026</p><h1>{e(DATA['integrationStory']['title'][lang])}</h1><p class="lead">{e(DATA['integrationStory']['reason'][lang])}</p></section><section class="section"><div class="trust"><div><h2>{e(DATA['heritage']['headline'][lang])}</h2><p>{e(DATA['heritage']['claim'][lang])}</p></div><div><h2>{e(UI['why'][lang])}</h2><p>{e(DATA['crossSell'][lang])}</p><p class="note">The specialist pillars remain separately identifiable. Legal/entity relationships are asserted only after verification.</p></div></div></section>{cta(lang)}'''
    shell('about',lang,about)
    contact = f'''<section class="page-hero"><p class="eyebrow">{e(DATA['positioning'][lang])}</p><h1>{e(DATA['primaryCta'][lang])}</h1><p class="lead">{e(UI['ctaTitle'][lang])}</p></section><section class="section"><div class="cards"><div class="card"><h2>HIPStudio Business</h2><p>{e(PILLARS['business']['intro'][lang])}</p></div><div class="card"><h2>HIPStudio Creative</h2><p>{e(PILLARS['creative']['intro'][lang])}</p></div><div class="card"><h2>Flúgos by HIPStudio</h2><p>{e(PILLARS['experiences']['intro'][lang])}</p></div></div><p class="note">Review build: no web form or automatic data submission is active here. The dedicated quote flow remains separately privacy-gated.</p></section>'''
    shell('contact',lang,contact)
    trust = f'''<section class="page-hero"><p class="eyebrow">AI Trust</p><h1>{e(UI['trust'][lang])}</h1><p class="lead">{e(page_desc('trust',lang))}</p></section><section class="section"><div class="trust"><div><h2>Human control</h2><p>AI may assist research, structuring, drafting or workflow automation. Material facts, client claims, pricing, legal statements and publication decisions require human verification.</p></div><div><h2>Data minimisation</h2><p>The review build contains no analytics, marketing tags or public forms. Future AI or analytics integrations must remain behind the approved privacy and consent architecture.</p></div></div></section>'''
    shell('trust',lang,trust)

(D / 'robots.txt').write_text('User-agent: *\nDisallow: /\n' if MODE == 'review' else 'User-agent: *\nAllow: /\n')
(D / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ('' if MODE == 'review' else ''.join(f'<url><loc>{e(p["canonical"])}</loc></url>' for p in PAGES)) + '</urlset>')
(D / 'platform-build.json').write_text(json.dumps({'mode':MODE,'base':BASE,'pages':PAGES,'pillars':[p['key'] for p in DATA['pillars']],'masterBrand':DATA['workingMasterBrand'],'masterDomain':DATA.get('masterDomain'),'masterBrandApprovalRequired':DATA['masterBrandApprovalRequired']},ensure_ascii=False,indent=2))
print(f'Built unified platform: {len(PAGES)} localized pages; mode={MODE}; base={BASE}')
