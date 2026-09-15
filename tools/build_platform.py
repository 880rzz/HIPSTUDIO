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
COMMERCIAL = json.loads((R / 'content/commercial-content.json').read_text())
HERO_MEDIA = json.loads((R / 'content/hero-media.json').read_text())
IMAGES = {item['id']:item for item in json.loads((R / 'content/images.json').read_text())}
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
(D / 'assets/photos').mkdir(parents=True)
for image_id in ('portrait-04','commercial-05','property-16','commercial-30'):
    shutil.copyfile(R / f'assets/photos/{image_id}-1440.webp', D / f'assets/photos/{image_id}-1440.webp')

LANGS = ['hu', 'en', 'de']
LOCALES = {'hu': 'hu_HU', 'en': 'en_GB', 'de': 'de_DE'}
ROUTES = {
    'home': {'hu':'', 'en':'', 'de':''},
    'business': {'hu':'uzleti-mukodes', 'en':'business-operations', 'de':'business-operations'},
    'creative': {'hu':'kreativ-tartalom', 'en':'creative-content', 'de':'creative-content'},
    'experiences': {'hu':'vallalati-elmenyek', 'en':'corporate-experiences', 'de':'unternehmenserlebnisse'},
    'about': {'hu':'partnerek', 'en':'partners', 'de':'partner'},
    'quote': {'hu':'ajanlatkeres', 'en':'request-a-quote', 'de':'angebot-anfragen'},
    'contact': {'hu':'kapcsolat', 'en':'contact', 'de':'kontakt'},
    'trust': {'hu':'ai-trust', 'en':'ai-trust', 'de':'ai-trust'}
}

UI = {
    'review': {'hu':'Platform review build · nincs publikálva', 'en':'Platform review build · not published', 'de':'Platform-Review-Build · nicht veröffentlicht'},
    'home': {'hu':'Főoldal','en':'Home','de':'Start'},
    'about': {'hu':'Partnerek','en':'Partners','de':'Partner'},
    'quote': {'hu':'Ajánlatkérés','en':'Request a quote','de':'Angebot anfragen'},
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
    'navFooter': {'hu':'Lábléc navigáció','en':'Footer navigation','de':'Fußnavigation'},
    'skip': {'hu':'Ugrás a tartalomhoz','en':'Skip to content','de':'Zum Inhalt springen'},
    'footerNote': {
        'hu':'A HIPStudio a főmárka; a Business és a Flúgos elkülöníthető szakmai területek. Nem állítunk nem igazolt jogi, tulajdonosi vagy szervezeti kapcsolatot.',
        'en':'HIPStudio is the master brand; Business and Flúgos remain distinct areas of expertise. No unverified legal, ownership or organisational relationship is asserted.',
        'de':'HIPStudio ist die Hauptmarke; Business und Flúgos bleiben klar erkennbare Kompetenzbereiche. Nicht belegte Rechts-, Eigentums- oder Organisationsbeziehungen werden nicht behauptet.'},
    'aboutNote': {
        'hu':'A szakmai területek külön azonosíthatók. Jogi és szervezeti kapcsolatot csak ellenőrzött forrás alapján állítunk.',
        'en':'The areas of expertise remain separately identifiable. Legal and organisational relationships are stated only when supported by verified sources.',
        'de':'Die Kompetenzbereiche bleiben einzeln erkennbar. Rechtliche und organisatorische Beziehungen nennen wir nur auf Grundlage geprüfter Quellen.'},
    'contactReview': {
        'hu':'Review build: az automatikus űrlapküldés nincs bekapcsolva; az ajánlatkérő folyamat külön adatvédelmi kapu mögött marad.',
        'en':'Review build: automatic form submission is disabled; the quote-request flow remains behind its separate privacy gate.',
        'de':'Review-Build: Die automatische Formularübermittlung ist deaktiviert; die Angebotsanfrage bleibt hinter ihrer eigenen Datenschutzfreigabe.'},
    'humanControl': {'hu':'Emberi kontroll','en':'Human control','de':'Menschliche Kontrolle'},
    'humanControlBody': {
        'hu':'Az AI segítheti a kutatást, rendszerezést, szövegalkotást vagy munkafolyamat-automatizálást. A lényeges tények, ügyfélállítások, árak, jogi szövegek és publikációs döntések emberi ellenőrzést igényelnek.',
        'en':'AI may assist research, structuring, drafting or workflow automation. Material facts, client claims, pricing, legal statements and publication decisions require human verification.',
        'de':'KI kann Recherche, Strukturierung, Entwürfe oder die Automatisierung von Abläufen unterstützen. Wesentliche Fakten, Kundenaussagen, Preise, Rechtstexte und Veröffentlichungsentscheidungen werden von Menschen geprüft.'},
    'dataMinimisation': {'hu':'Adatminimalizálás','en':'Data minimisation','de':'Datenminimierung'},
    'dataMinimisationBody': {
        'hu':'A review build nem tartalmaz analitikát, marketingcímkét vagy nyilvános űrlapot. Jövőbeli AI- vagy analitikai integráció csak a jóváhagyott adatvédelmi és hozzájárulási rendszer mögött aktiválható.',
        'en':'The review build contains no analytics, marketing tags or public forms. Future AI or analytics integrations must remain behind the approved privacy and consent architecture.',
        'de':'Der Review-Build enthält keine Analyse- oder Marketing-Tags und keine öffentlichen Formulare. Künftige KI- oder Analyse-Integrationen dürfen nur hinter der freigegebenen Datenschutz- und Einwilligungsarchitektur aktiviert werden.'}
}

PILLARS = {p['key']: p for p in DATA['pillars']}
PAGES = []

def e(value): return escape(str(value), quote=True)
def emphasized(value, lang):
    text = e(value)
    phrases = {
        'hu': ('Fotó, videó és podcast', '2006 óta'),
        'en': ('Photography, video and podcasts', 'Since 2006'),
        'de': ('Fotografie, Video und Podcast', 'Seit 2006')
    }[lang]
    for phrase in phrases:
        text = text.replace(phrase, f'<strong>{phrase}</strong>')
    return text
def route(key, lang):
    slug = ROUTES[key][lang]
    return f'/{lang}/' + (slug + '/' if slug else '')
def absolute(key, lang): return BASE + route(key, lang)
def href(key, lang): return route(key, lang)

def page_title(key, lang):
    if key == 'home': return DATA['hero']['title'][lang]
    if key in PILLARS: return PILLARS[key]['title'][lang]
    if key == 'about': return UI['about'][lang]
    if key == 'quote': return UI['quote'][lang]
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
    if key == 'about': return {
        'hu':'Korábbi, dokumentált HIPStudio együttműködések és partnerlogók.',
        'en':'Documented previous HIPStudio collaborations and partner logos.',
        'de':'Dokumentierte frühere HIPStudio-Zusammenarbeiten und Partnerlogos.'
    }[lang]
    if key == 'contact': return DATA['positioning'][lang]
    return {
        'hu':'Átlátható AI-használati, emberi kontroll- és adatvédelmi elvek a HIPStudio rendszerhez.',
        'en':'Transparent AI-use, human-control and privacy principles for the HIPStudio system.',
        'de':'Transparente Prinzipien zu KI-Nutzung, menschlicher Kontrolle und Datenschutz für das HIPStudio-System.'
    }[lang]

def language_links(key, lang):
    return ''.join(f'<a lang="{l}" hreflang="{l}" href="{e(href(key,l))}"' + (' aria-current="page"' if l == lang else '') + f'>{l.upper()}</a>' for l in LANGS)

def nav(key, lang):
    items = ['home','creative','business','experiences','about','quote','contact']
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
    html = f'''<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(meta_title(key,lang))}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="{'noindex,nofollow' if MODE=='review' else 'index,follow'}"><link rel="canonical" href="{e(url)}">{alternates}<meta property="og:type" content="website"><meta property="og:locale" content="{LOCALES[lang]}"><meta property="og:site_name" content="HIPStudio"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><link rel="stylesheet" href="/assets/platform.css"><script type="application/ld+json">{ld}</script></head><body><a class="skip" href="#main">{e(UI['skip'][lang])}</a>{review}<header class="header"><a class="brand" href="{e(href('home',lang))}">HIPStudio</a><nav class="nav" aria-label="{e(UI['navMain'][lang])}">{nav(key,lang)}</nav><nav class="langs" aria-label="{e(UI['navLang'][lang])}">{language_links(key,lang)}</nav></header><main id="main">{body}</main><footer class="footer"><strong>HIPStudio</strong><nav aria-label="{e(UI['navFooter'][lang])}">{nav(key,lang)}</nav><p class="legal-note">{e(UI['footerNote'][lang])}</p></footer></body></html>'''
    out = D / route(key,lang).strip('/') / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    PAGES.append({'key':key,'lang':lang,'path':route(key,lang),'canonical':url})

def cta(lang):
    return f'<section class="cta"><p class="eyebrow">HIPStudio</p><h2>{e(UI["ctaTitle"][lang])}</h2><a class="button" href="{e(href("quote",lang))}">{e(UI["quote"][lang])} →</a></section>'

def pillar_card(p, lang, index):
    return f'''<a class="pillar" href="{e(href(p['key'],lang))}"><span class="number">0{index} · {e(p['brand'])}</span><p class="eyebrow">{e(p['label'][lang])}</p><h3>{e(p['title'][lang])}</h3><p>{e(p['intro'][lang])}</p><span class="arrow" aria-hidden="true">↗</span></a>'''

def pillar_page(p, lang):
    services = ''.join(f'<li>{e(s)}</li>' for s in p['services'][lang])
    problem = COMMERCIAL['pillars'][p['key']]['problem'][lang]
    outcome = COMMERCIAL['pillars'][p['key']]['outcome'][lang]
    labels = {
      'hu':('A helyzet','A válasz','Amiben segítünk','Referenciák','Korábbi együttműködések és igazolt munkák.'),
      'en':('The situation','Our answer','What we do','References','Previous collaborations and verified work.'),
      'de':('Die Situation','Unsere Antwort','Wobei wir helfen','Referenzen','Frühere Zusammenarbeiten und belegte Arbeiten.')
    }[lang]
    gallery = ''
    if p['key'] == 'creative':
        protected_label = {'hu':'Védett tartalom','en':'Protected content','de':'Geschützter Inhalt'}[lang]
        groups = {
            'hu':[('Fotó — portré és személyes jelenlét','/hu/szolgaltatasok/hipstudio/photo-portrait/',['portrait-04','commercial-05','property-16']),('Fotó — céges és reklám','/hu/szolgaltatasok/hipstudio/photo-corporate/',['commercial-05','property-16','portrait-04']),('Fotó — esemény és konferencia','/hu/szolgaltatasok/hipstudio/photo-event/',['commercial-30','commercial-05','property-16'])],
            'en':[('Photography — portrait and personal presence','/en/services/hipstudio/photo-portrait/',['portrait-04','commercial-05','property-16']),('Photography — corporate and advertising','/en/services/hipstudio/photo-corporate/',['commercial-05','property-16','portrait-04']),('Photography — events and conferences','/en/services/hipstudio/photo-event/',['commercial-30','commercial-05','property-16'])],
            'de':[('Fotografie — Porträt und persönlicher Auftritt','/de/leistungen/hipstudio/photo-portrait/',['portrait-04','commercial-05','property-16']),('Fotografie — Unternehmen und Werbung','/de/leistungen/hipstudio/photo-corporate/',['commercial-05','property-16','portrait-04']),('Fotografie — Events und Konferenzen','/de/leistungen/hipstudio/photo-event/',['commercial-30','commercial-05','property-16'])]
        }[lang]
        blocks=[]
        for title,service_href,images in groups:
            photos=''.join(f'<figure><img src="/assets/photos/{image_id}-1440.webp" alt="{e(protected_label)}" loading="lazy" decoding="async"><figcaption>{e(protected_label)}</figcaption></figure>' for image_id in images)
            blocks.append(f'<details class="service-reference"><summary>{e(title)}</summary><div class="editorial-photo-grid">{photos}</div><p><a class="text-link" href="{service_href}">{e(labels[2])} →</a></p></details>')
        video_copy={'hu':'Videó — márka-, vezetői és eseményfilmek a HIPStudio referencia-videóiból.','en':'Video — brand, executive and event films from HIPStudio reference videos.','de':'Video — Marken-, Executive- und Eventfilme aus den HIPStudio-Referenzvideos.'}[lang]
        podcast_copy={'hu':'Podcast — videós és audio podcastok, valamint a hozzájuk tartozó tartalomrendszer.','en':'Podcast — video and audio podcasts with the surrounding content system.','de':'Podcast — Video- und Audio-Podcasts mit dem dazugehörigen Contentsystem.'}[lang]
        channel=HERO_MEDIA['channelUrl']
        blocks.append(f'<details class="service-reference"><summary>Videó</summary><p>{e(video_copy)}</p><p><a class="text-link" href="{channel}">Referencia-videók megnyitása →</a></p></details>')
        blocks.append(f'<details class="service-reference"><summary>Podcast</summary><p>{e(podcast_copy)}</p><p><a class="text-link" href="{channel}">Referencia-videók megnyitása →</a></p></details>')
        gallery=''.join(blocks)
    history=f'''<section class="section editorial-history"><p class="eyebrow">2006 → 2026</p><h2>{e(DATA['heritage']['headline'][lang])}</h2><p>{e(DATA['heritage']['claim'][lang])}</p></section>'''
    return f'''<section class="page-hero editorial-onepager-hero"><a class="back" href="{e(href('home',lang))}">← HIPStudio</a><p class="eyebrow">{e(p['brand'])}</p><h1>{e(p['title'][lang])}</h1><p class="lead">{emphasized(p['intro'][lang],lang)}</p></section>{history}<section class="section editorial-problem"><p class="eyebrow">{e(labels[0])}</p><h2>{e(problem)}</h2></section><section class="section editorial-answer"><p class="eyebrow">{e(labels[1])}</p><h2>{e(outcome)}</h2><h3>{e(labels[2])}</h3><ul class="service-list">{services}</ul></section>{gallery}<section class="section editorial-references"><p class="eyebrow">{e(labels[3])}</p><h2>{e(labels[4])}</h2><a class="text-link" href="{e(href('about',lang))}">{e(UI['about'][lang])} →</a></section>{cta(lang)}'''

for lang in LANGS:
    cards = ''.join(pillar_card(p,lang,i+1) for i,p in enumerate(DATA['pillars']))
    flow_labels = {'hu':['Működés','Növekedés','Láthatóság','Kapcsolódás'],'en':['Operate','Grow','Be seen','Connect'],'de':['Betreiben','Wachsen','Sichtbar sein','Verbinden']}[lang]
    flow = ''.join(f'<div><strong>0{i+1}</strong><span>{e(label)}</span></div>' for i,label in enumerate(flow_labels))
    heritage = f'''<section class="section"><div class="section-head"><p class="eyebrow">2006 → 2026</p><h2>{e(DATA['heritage']['headline'][lang])}</h2><p>{e(DATA['heritage']['claim'][lang])}</p></div></section>'''
    integration = f'''<section class="dark"><div class="section"><div class="section-head"><h2>{e(DATA['integrationStory']['title'][lang])}</h2><p>{e(DATA['integrationStory']['reason'][lang])}</p></div><div class="flow">{flow}</div></div></section>'''
    intro = {'hu':'2006 óta készítünk tartalmat, fejlesztünk működést és szervezünk olyan eseményeket, amelyeknek világos céljuk van.','en':'Since 2006, we have produced content, improved operations and created events with a clear purpose.','de':'Seit 2006 produzieren wir Content, verbessern Abläufe und gestalten Veranstaltungen mit einem klaren Ziel.'}[lang]
    home = f'''<section class="hero"><div><p class="eyebrow">HIPStudio · 2006</p><h1>{e(DATA['hero']['title'][lang])}</h1><p class="lead">{emphasized(intro,lang)}</p></div></section><section class="section home-introduction"><p class="eyebrow">HIPStudio</p><h2>{e(intro)}</h2></section><section class="section home-three-doors"><div class="section-head"><h2>{e(UI['pillars'][lang])}</h2></div><div class="pillars">{cards}</div></section>{cta(lang)}'''
    shell('home',lang,home)
    for p in DATA['pillars']:
        shell(p['key'],lang,pillar_page(p,lang))
    partner_intro = {'hu':'Dokumentált együttműködések. A logók nem jelentenek jelenlegi megbízást vagy ajánlást.','en':'Documented collaborations. Logos do not imply a current engagement or endorsement.','de':'Dokumentierte Zusammenarbeiten. Logos bedeuten keinen aktuellen Auftrag und keine Empfehlung.'}[lang]
    about = f'''<section class="page-hero"><p class="eyebrow">HIPStudio</p><h1>{e(UI['about'][lang])}</h1><p class="lead">{e(partner_intro)}</p></section>'''
    shell('about',lang,about)
    contact_review = f'<p class="note">{e(UI["contactReview"][lang])}</p>' if MODE == 'review' else ''
    contact = f'''<section class="page-hero"><p class="eyebrow">{e(DATA['positioning'][lang])}</p><h1>{e(DATA['primaryCta'][lang])}</h1><p class="lead">{e(UI['ctaTitle'][lang])}</p></section><section class="section"><div class="cards"><div class="card"><h2>HIPStudio Business</h2><p>{e(PILLARS['business']['intro'][lang])}</p></div><div class="card"><h2>HIPStudio Creative</h2><p>{e(PILLARS['creative']['intro'][lang])}</p></div><div class="card"><h2>Flúgos by HIPStudio</h2><p>{e(PILLARS['experiences']['intro'][lang])}</p></div></div>{contact_review}</section>'''
    shell('contact',lang,contact)
    trust = f'''<section class="page-hero"><p class="eyebrow">AI Trust</p><h1>{e(UI['trust'][lang])}</h1><p class="lead">{e(page_desc('trust',lang))}</p></section><section class="section"><div class="trust"><div><h2>{e(UI['humanControl'][lang])}</h2><p>{e(UI['humanControlBody'][lang])}</p></div><div><h2>{e(UI['dataMinimisation'][lang])}</h2><p>{e(UI['dataMinimisationBody'][lang])}</p></div></div></section>'''
    shell('trust',lang,trust)

(D / 'robots.txt').write_text('User-agent: *\nDisallow: /\n' if MODE == 'review' else 'User-agent: *\nAllow: /\n')
(D / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ('' if MODE == 'review' else ''.join(f'<url><loc>{e(p["canonical"])}</loc></url>' for p in PAGES)) + '</urlset>')
(D / 'platform-build.json').write_text(json.dumps({'mode':MODE,'base':BASE,'pages':PAGES,'pillars':[p['key'] for p in DATA['pillars']],'masterBrand':DATA['workingMasterBrand'],'masterDomain':DATA.get('masterDomain'),'masterBrandApprovalRequired':DATA['masterBrandApprovalRequired']},ensure_ascii=False,indent=2))
print(f'Built unified platform: {len(PAGES)} localized pages; mode={MODE}; base={BASE}')
