# coding: utf-8
"""Extend dist-platform with cross-pillar solution pages. No network or deploy."""
from pathlib import Path
from html import escape
import json, os

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'
DATA=json.loads((R/'content/platform.json').read_text())
SOLUTIONS=json.loads((R/'content/platform-solutions.json').read_text())
MODE=os.environ.get('BUILD_MODE','review')
BASE=os.environ.get('PLATFORM_URL','https://www.hellouzlet.hu').rstrip('/')
LANGS=['hu','en','de']
ROUTE_HUB={'hu':'megoldasok','en':'solutions','de':'loesungen'}
PILLAR_ROUTE={
 'business':{'hu':'uzleti-mukodes','en':'business-operations','de':'business-operations'},
 'creative':{'hu':'kreativ-tartalom','en':'creative-content','de':'creative-content'},
 'experiences':{'hu':'vallalati-elmenyek','en':'corporate-experiences','de':'unternehmenserlebnisse'}
}
UI={
 'hubTitle':{'hu':'Megoldások vezetői problémákra','en':'Solutions for management problems','de':'Lösungen für Führungsprobleme'},
 'hubIntro':{'hu':'Nem szolgáltatáslistából indulunk, hanem abból, hol akad el a működés, a kontroll, a láthatóság vagy az emberek kapcsolódása.','en':'We start with where operations, control, visibility or human connection break down — not with a service catalogue.','de':'Wir starten dort, wo Betrieb, Kontrolle, Sichtbarkeit oder menschliche Verbindung stocken — nicht mit einem Leistungskatalog.'},
 'decision':{'hu':'Kiinduló helyzet','en':'Starting situation','de':'Ausgangslage'},
 'outcome':{'hu':'Célállapot','en':'Target outcome','de':'Zielbild'},
 'includes':{'hu':'Mit fog össze','en':'What it brings together','de':'Was gebündelt wird'},
 'related':{'hu':'Kapcsolódó megoldások','en':'Related solutions','de':'Verwandte Lösungen'},
 'cta':{'hu':'30 perces üzleti konzultáció','en':'30-minute business consultation','de':'30-minütige Unternehmensberatung'},
 'back':{'hu':'Összes megoldás','en':'All solutions','de':'Alle Lösungen'},
 'mainNav':{'hu':'Fő navigáció','en':'Main navigation','de':'Hauptnavigation'},
 'footerNav':{'hu':'Lábléc navigáció','en':'Footer navigation','de':'Fußnavigation'}
}

def e(v):return escape(str(v),quote=True)
def hub_path(l):return f'/{l}/{ROUTE_HUB[l]}/'
def solution_path(item,l):return f'/{l}/{ROUTE_HUB[l]}/{item["key"]}/'
def home(l):return f'/{l}/'
def pillar_path(key,l):return f'/{l}/{PILLAR_ROUTE[key][l]}/'
def contact(l):return f'/{l}/'+{'hu':'kapcsolat','en':'contact','de':'kontakt'}[l]+'/'
def abs_path(path):return BASE+path

def nav(l):
 items=[(home(l),DATA['workingMasterBrand']),(hub_path(l),UI['back'][l]),(pillar_path('business',l),'Business'),(pillar_path('creative',l),'HIPStudio'),(pillar_path('experiences',l),'Flúgos'),(contact(l),UI['cta'][l])]
 return ''.join(f'<a href="{e(path)}">{e(label)}</a>' for path,label in items)

def lang_links(path_fn,l):
 return ''.join(f'<a lang="{x}" hreflang="{x}" href="{e(path_fn(x))}"'+(' aria-current="page"' if x==l else '')+f'>{x.upper()}</a>' for x in LANGS)

def shell(path_fn,l,title,desc,body,graph_nodes):
 path=path_fn(l);url=abs_path(path)
 alts=''.join(f'<link rel="alternate" hreflang="{x}" href="{e(abs_path(path_fn(x)))}">' for x in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{e(abs_path(path_fn("hu")))}">'
 graph={'@context':'https://schema.org','@graph':[
   {'@type':'WebSite','@id':BASE+'/#website','name':DATA['workingMasterBrand'],'url':BASE+'/'},
   {'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':l,'isPartOf':{'@id':BASE+'/#website'}},
   {'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':DATA['workingMasterBrand'],'item':abs_path(home(l))},{'@type':'ListItem','position':2,'name':title,'item':url}]}
 ]+graph_nodes}
 ld=json.dumps(graph,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 meta_title=f'{title} | {DATA["workingMasterBrand"]}'
 if len(meta_title)>70:meta_title=f'{title} | HelloÜzlet'
 review='<div class="review">Platform review build · no production publication</div>' if MODE=='review' else ''
 html=f'''<!DOCTYPE html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(meta_title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="{'noindex,nofollow' if MODE=='review' else 'index,follow'}"><link rel="canonical" href="{e(url)}">{alts}<link rel="stylesheet" href="/assets/platform.css"><script type="application/ld+json">{ld}</script></head><body><a class="skip" href="#main">Skip</a>{review}<header class="header"><a class="brand" href="{e(home(l))}">{e(DATA['workingMasterBrand'])}</a><nav class="nav" aria-label="{e(UI['mainNav'][l])}">{nav(l)}</nav><nav class="langs" aria-label="Languages">{lang_links(path_fn,l)}</nav></header><main id="main">{body}</main><footer class="footer"><strong>{e(DATA['workingMasterBrand'])}</strong><nav aria-label="{e(UI['footerNav'][l])}">{nav(l)}</nav><p class="legal-note">Review-only cross-pillar solution architecture. No unverified client result, legal-entity ownership or endorsement claim is asserted.</p></footer></body></html>'''
 out=D/path.strip('/')/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html)
 return {'key':'solutions' if path==hub_path(l) else 'solution','lang':l,'path':path,'canonical':url}

def card(item,l):
 return f'''<a class="card" href="{e(solution_path(item,l))}"><p class="eyebrow">{e(item['audience'][l])}</p><h2>{e(item['name'][l])}</h2><p>{e(item['problem'][l])}</p><span aria-hidden="true">↗</span></a>'''

manifest=json.loads((D/'platform-build.json').read_text())
existing={(p['path'],p['lang']) for p in manifest['pages']}
new=[]
for l in LANGS:
 hub_body=f'''<section class="page-hero"><p class="eyebrow">{e(DATA['positioning'][l])}</p><h1>{e(UI['hubTitle'][l])}</h1><p class="lead">{e(UI['hubIntro'][l])}</p></section><section class="section"><div class="cards">{''.join(card(x,l) for x in SOLUTIONS)}</div></section>'''
 new.append(shell(hub_path,l,UI['hubTitle'][l],UI['hubIntro'][l],hub_body,[]))
 for item in SOLUTIONS:
  includes=''.join(f'<li>{e(x)}</li>' for x in item['includes'][l])
  related=''.join(f'<a class="card" href="{e(solution_path(next(s for s in SOLUTIONS if s["key"]==k),l))}"><h3>{e(next(s for s in SOLUTIONS if s["key"]==k)["name"][l])}</h3><span aria-hidden="true">↗</span></a>' for k in item.get('related',[]))
  body=f'''<section class="page-hero"><a class="back" href="{e(hub_path(l))}">← {e(UI['back'][l])}</a><p class="eyebrow">{e(item['audience'][l])}</p><h1>{e(item['name'][l])}</h1><p class="lead">{e(item['problem'][l])}</p></section><section class="section"><div class="section-head"><h2>{e(UI['outcome'][l])}</h2><p>{e(item['outcome'][l])}</p></div><h3>{e(UI['includes'][l])}</h3><ul class="service-list">{includes}</ul><p class="note">Specialist pillar: <a href="{e(pillar_path(item['pillar'],l))}">{e(item['pillar'])} ↗</a></p></section>{('<section class="section"><h2>'+e(UI['related'][l])+'</h2><div class="cards">'+related+'</div></section>') if related else ''}<section class="cta"><h2>{e(UI['cta'][l])}</h2><a class="button" href="{e(contact(l))}">{e(UI['cta'][l])} →</a></section>'''
  service={'@type':'Service','@id':abs_path(solution_path(item,l))+'#service','name':item['name'][l],'description':item['problem'][l],'serviceType':item['name'][l],'url':abs_path(solution_path(item,l))}
  new.append(shell(lambda x,it=item:solution_path(it,x),l,item['name'][l],item['problem'][l],body,[service]))
for p in new:
 if (p['path'],p['lang']) not in existing:manifest['pages'].append(p)
manifest['solutions']=len(SOLUTIONS)
(D/'platform-build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
if MODE=='production':
 sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(p["canonical"])}</loc></url>' for p in manifest['pages'])+'</urlset>'
 (D/'sitemap.xml').write_text(sitemap)
print(f'Extended unified platform with {len(new)} localized solution pages; total={len(manifest["pages"])}')
