# coding: utf-8
"""Append the review-safe three-pillar quote request to dist-platform.

No price is calculated or displayed. The Google Apps Script endpoint is injected only
from QUOTE_FORM_ENDPOINT and is required for a production build.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json, os, shutil

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'
MODE=os.environ.get('BUILD_MODE','review')
BASE=os.environ.get('PLATFORM_URL','https://www.hipstudio.hu').rstrip('/')
ENDPOINT=os.environ.get('QUOTE_FORM_ENDPOINT','').strip()
DATA=json.loads((R/'content/platform.json').read_text())
QUOTE=json.loads((R/'content/quote-request.json').read_text())
LANGS=['hu','en','de']
ROUTES={'hu':'ajanlatkeres','en':'request-a-quote','de':'angebot-anfragen'}
CONTACT={'hu':'kapcsolat','en':'contact','de':'kontakt'}
PILLARS={
 'business':{'hu':'uzleti-mukodes','en':'business-operations','de':'business-operations'},
 'creative':{'hu':'kreativ-tartalom','en':'creative-content','de':'creative-content'},
 'experiences':{'hu':'vallalati-elmenyek','en':'corporate-experiences','de':'unternehmenserlebnisse'}
}
COPY={
 'hu':{
  'title':'Egyedi árajánlatkérés','desc':'Mondd el, mire van szükséged. A HIPStudio és specialist partnerei 24 órán belül egyedi ajánlatot készítenek a projekt scope-ja alapján.','eyebrow':'Nincs automatikus árkalkuláció','lead':'Minden projekt más. Nem sablonárat mutatunk, hanem a tényleges scope-ot kérdezzük végig: cél, terjedelem, résztvevők, helyszín, időzítés, felhasználás és szükséges szakmai kapacitás.','nav':'Fő navigáció','langs':'Nyelvválasztó','footer':'Lábléc navigáció','privacy':'Az éles beküldés csak jóváhagyott adatkezelési tájékoztatóval és backenddel aktiválható.','contact':'Központi kapcsolat'
 },
 'en':{
  'title':'Request a tailored quote','desc':'Tell us what you need. HIPStudio and its specialist partners prepare a tailored quote within 24 hours based on the actual project scope.','eyebrow':'No automatic price calculation','lead':'Every project is different. Instead of showing a template price, we capture the variables that actually change scope: objective, volume, participants, location, timing, usage and required specialist capacity.','nav':'Main navigation','langs':'Language selector','footer':'Footer navigation','privacy':'Live submission is activated only with an approved privacy notice and backend.','contact':'Central contact'
 },
 'de':{
  'title':'Individuelles Angebot anfragen','desc':'Beschreiben Sie Ihren Bedarf. HIPStudio und seine Fachpartner erstellen innerhalb von 24 Stunden ein individuelles Angebot auf Basis des tatsächlichen Projektumfangs.','eyebrow':'Keine automatische Preisberechnung','lead':'Jedes Projekt ist anders. Statt eines Standardpreises erfassen wir die Faktoren, die den Umfang tatsächlich verändern: Ziel, Volumen, Teilnehmende, Ort, Timing, Nutzung und benötigte Fachkapazität.','nav':'Hauptnavigation','langs':'Sprachauswahl','footer':'Fußnavigation','privacy':'Der Live-Versand wird erst mit freigegebenen Datenschutzhinweisen und Backend aktiviert.','contact':'Zentraler Kontakt'
 }
}

def e(v): return escape(str(v),quote=True)
def path(l): return f'/{l}/{ROUTES[l]}/'
def abs_path(p): return BASE+p
def home(l): return f'/{l}/'
def pillar(k,l): return f'/{l}/{PILLARS[k][l]}/'
def contact(l): return f'/{l}/{CONTACT[l]}/'
def nav(l):
 items=[(home(l),DATA['workingMasterBrand']),(pillar('business',l),'Business'),(pillar('creative',l),'HIPStudio'),(pillar('experiences',l),'Flúgos'),(path(l),COPY[l]['title'])]
 return ''.join(f'<a href="{e(p)}">{e(label)}</a>' for p,label in items)
def langs(l):
 return ''.join(f'<a lang="{x}" hreflang="{x}" href="{e(path(x))}"'+(' aria-current="page"' if x==l else '')+f'>{x.upper()}</a>' for x in LANGS)

if not D.exists(): raise SystemExit('dist-platform missing; run build_platform.py first')
if MODE=='production':
 if not ENDPOINT: raise SystemExit('Quote production blocked: QUOTE_FORM_ENDPOINT is required')
 u=urlsplit(ENDPOINT)
 if u.scheme!='https' or not u.netloc: raise SystemExit('QUOTE_FORM_ENDPOINT must be HTTPS')

shutil.copyfile(R/'assets/quote-form.js',D/'assets/quote-form.js')
# The first-contact form must not solicit special-category health data. Keep only
# general accessibility/physical/cultural/weather constraints needed for scoping.
quote_js=D/'assets/quote-form.js'
quote_source=quote_js.read_text(encoding='utf-8')
health_prompt_replacements={
 'Fizikai, akadálymentesítési, egészségügyi, kulturális vagy időjárási korlátok':'Fizikai, akadálymentesítési, kulturális vagy időjárási korlátok',
 'Physische, Barrierefreiheits-, gesundheitliche, kulturelle oder wetterbedingte Einschränkungen':'Physische, Barrierefreiheits-, kulturelle oder wetterbedingte Einschränkungen',
 'Physical, accessibility, health, cultural or weather constraints':'Physical, accessibility, cultural or weather constraints'
}
for old,new_label in health_prompt_replacements.items():
 if old not in quote_source:
  raise SystemExit(f'Expected quote health prompt missing: {old}')
 quote_source=quote_source.replace(old,new_label)
quote_js.write_text(quote_source,encoding='utf-8')
shutil.copyfile(R/'assets/quote-prefill.js',D/'assets/quote-prefill.js')
shutil.copyfile(R/'assets/quote-form.css',D/'assets/quote-form.css')
manifest=json.loads((D/'platform-build.json').read_text())
existing={(x['path'],x['lang']) for x in manifest['pages']}
new=[]
config_json=json.dumps(QUOTE,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
for l in LANGS:
 p=path(l);url=abs_path(p);c=COPY[l]
 alts=''.join(f'<link rel="alternate" hreflang="{x}" href="{e(abs_path(path(x)))}">' for x in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{e(abs_path(path("hu")))}">'
 graph={'@context':'https://schema.org','@graph':[
  {'@type':'WebSite','@id':BASE+'/#website','name':DATA['workingMasterBrand'],'url':BASE+'/'},
  {'@type':'WebPage','@id':url+'#webpage','url':url,'name':c['title'],'description':c['desc'],'inLanguage':l,'isPartOf':{'@id':BASE+'/#website'}},
  {'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':DATA['workingMasterBrand'],'item':abs_path(home(l))},{'@type':'ListItem','position':2,'name':c['title'],'item':url}]}
 ]}
 ld=json.dumps(graph,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 review='<div class="review">Platform review build · quote submission disabled</div>' if MODE=='review' else ''
 body=f'''<section class="quote-shell"><div class="quote-intro"><p class="eyebrow">{e(c['eyebrow'])}</p><h1>{e(c['title'])}</h1><p class="lead">{e(c['lead'])}</p><div class="q-meta"><span><strong>24h</strong> · {e(QUOTE['responsePromise'][l])}</span><span>{e(c['contact'])}: <a href="mailto:{e(QUOTE['centralEmail'])}">{e(QUOTE['centralEmail'])}</a></span></div></div><div data-quote-root data-endpoint="{e(ENDPOINT if MODE=='production' else '')}"></div><noscript><p class="note">JavaScript is required for the guided quote form. Contact: <a href="mailto:{e(QUOTE['centralEmail'])}">{e(QUOTE['centralEmail'])}</a></p></noscript><p class="legal-note">{e(c['privacy'])}</p></section>'''
 html=f'''<!DOCTYPE html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(c['title'])} | HIPStudio</title><meta name="description" content="{e(c['desc'])}"><meta name="robots" content="{'noindex,nofollow' if MODE=='review' else 'index,follow'}"><link rel="canonical" href="{e(url)}">{alts}<link rel="stylesheet" href="/assets/platform.css"><link rel="stylesheet" href="/assets/quote-form.css"><script type="application/ld+json">{ld}</script><script type="application/json" id="quote-config">{config_json}</script><script defer src="/assets/quote-form.js"></script><script defer src="/assets/quote-prefill.js"></script></head><body><a class="skip" href="#main">Skip</a>{review}<header class="header"><a class="brand" href="{e(home(l))}">{e(DATA['workingMasterBrand'])}</a><nav class="nav" aria-label="{e(c['nav'])}">{nav(l)}</nav><nav class="langs" aria-label="{e(c['langs'])}">{langs(l)}</nav></header><main id="main">{body}</main><footer class="footer"><strong>{e(DATA['workingMasterBrand'])}</strong><nav aria-label="{e(c['footer'])}">{nav(l)}</nav><p>{e(c['contact'])}: <a href="mailto:{e(QUOTE['centralEmail'])}">{e(QUOTE['centralEmail'])}</a></p></footer></body></html>'''
 out=D/p.strip('/')/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html)
 row={'key':'quote-request','lang':l,'path':p,'canonical':url}
 if (p,l) not in existing: manifest['pages'].append(row)
 new.append(row)
manifest['quoteRequest']={'version':QUOTE['version'],'pages':len(new),'pricing':'none','responseHours':24,'endpointConfigured':bool(ENDPOINT and MODE=='production')}
(D/'platform-build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
if MODE=='production':
 sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(x["canonical"])}</loc></url>' for x in manifest['pages'])+'</urlset>'
 (D/'sitemap.xml').write_text(sitemap)
print(f'Added quote request: {len(new)} localized pages; total={len(manifest["pages"])}; endpoint={"configured" if ENDPOINT else "review-disabled"}')
