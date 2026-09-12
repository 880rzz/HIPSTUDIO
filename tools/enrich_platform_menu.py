# coding: utf-8
"""Replace the classic platform nav with one accessible full-screen menu.

Runs after all platform page generators so services, solutions, legal and quote pages
share one navigation model without duplicating source-generator logic.
"""
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist-platform'
ASSETS=DIST/'assets'
HEADER_RE=re.compile(r'<header class="header">.*?</header>',re.DOTALL)
LANG_RE=re.compile(r'<html lang="(hu|en|de)"')
LANG_NAV_RE=re.compile(r'<nav class="langs".*?</nav>',re.DOTALL)
BRAND_RE=re.compile(r'<a class="brand" href="([^"]+)">HIPStudio</a>')

ROUTES={
 'hu':[('business','/hu/uzleti-mukodes/'),('creative','/hu/kreativ-tartalom/'),('experiences','/hu/vallalati-elmenyek/'),('about','/hu/rolunk/'),('contact','/hu/kapcsolat/')],
 'en':[('business','/en/business-operations/'),('creative','/en/creative-content/'),('experiences','/en/corporate-experiences/'),('about','/en/about/'),('contact','/en/contact/')],
 'de':[('business','/de/business-operations/'),('creative','/de/creative-content/'),('experiences','/de/unternehmenserlebnisse/'),('about','/de/ueber-uns/'),('contact','/de/kontakt/')],
}
COPY={
 'hu':{
  'open':'Menü megnyitása','close':'Menü bezárása','label':'Fő navigáció','meta':'Egy rendszer, kevesebb koordináció.',
  'note':'Mondd el, mit kell elérni. A feladathoz rakjuk össze a megfelelő formátumot, stábot és felelősségi kört — nem fordítva.',
  'business':('Üzleti működés','Ha a háttérmunka és a koordináció túl sok időt visz el a valódi döntésektől.'),
  'creative':('Kreatív tartalom','Fotó, film, podcast és kapcsolódó tartalom, amikor több beszállító helyett egy koordinált gyártás kell.'),
  'experiences':('Vállalati élmények','Ha egy eseménynek, csapatnapnak vagy aktivációnak nem sablont, hanem működő formát kell adni.'),
  'about':('Hogyan dolgozunk','Kik vannak a háttérben, hogyan oszlik meg a felelősség, és mi marad rugalmas a projektben.'),
  'contact':('Konzultáció','Pár mondat a helyzetről elég. Először a problémát tisztázzuk, utána a megoldást.'),
 },
 'en':{
  'open':'Open menu','close':'Close menu','label':'Main navigation','meta':'One system, less coordination.',
  'note':'Tell us what has to change. We assemble the right format, crew and responsibility around the job — not the other way around.',
  'business':('Business operations','When coordination and background work consume time that should stay with decisions and growth.'),
  'creative':('Creative content','Photo, film, podcast and connected content when one coordinated production is simpler than several suppliers.'),
  'experiences':('Corporate experiences','When an event, team day or activation needs a purposeful format rather than a generic package.'),
  'about':('How we work','Who is responsible for what, how the system fits together, and which parts can flex around the project.'),
  'contact':('Consultation','A few lines about the situation are enough. We clarify the problem before proposing the format.'),
 },
 'de':{
  'open':'Menü öffnen','close':'Menü schließen','label':'Hauptnavigation','meta':'Ein System, weniger Koordination.',
  'note':'Sag uns, was erreicht werden soll. Format, Team und Verantwortungsrahmen werden um die Aufgabe gebaut — nicht umgekehrt.',
  'business':('Business Operations','Wenn Koordination und Hintergrundarbeit Zeit binden, die eigentlich für Entscheidungen und Wachstum gebraucht wird.'),
  'creative':('Creative Content','Foto, Film, Podcast und verbundener Content, wenn eine koordinierte Produktion einfacher ist als mehrere Dienstleister.'),
  'experiences':('Unternehmenserlebnisse','Wenn Event, Teamtag oder Aktivierung eine passende Form statt eines Standardpakets brauchen.'),
  'about':('So arbeiten wir','Wer wofür verantwortlich ist, wie das System zusammenspielt und was im Projekt flexibel bleibt.'),
  'contact':('Beratung','Ein paar Sätze zur Situation reichen. Erst klären wir das Problem, dann das passende Format.'),
 },
}

def path_for(page:Path):
 rel=page.relative_to(DIST)
 if rel.name!='index.html': return '/'+rel.as_posix()
 parent=rel.parent.as_posix()
 return '/'+(parent+'/' if parent!='.' else '')

def menu_markup(lang:str,current:str,brand_href:str,langs:str):
 c=COPY[lang]
 items=[]
 for key,href in ROUTES[lang]:
  title,desc=c[key]
  current_attr=' aria-current="page"' if current==href or (key in ('business','creative','experiences') and current.startswith(href)) else ''
  items.append(f'<a class="menu-item" href="{href}"{current_attr}><span class="menu-item-title">{title}</span><span class="menu-item-copy">{desc}</span></a>')
 return (
  f'<header class="header"><a class="brand" href="{brand_href}">HIPStudio</a>{langs}'
  f'<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="{c["open"]}" data-menu-toggle>'
  '<span class="menu-glyph" aria-hidden="true"><span></span><span></span></span></button></header>'
  f'<div class="menu-overlay" id="site-menu" role="dialog" aria-modal="true" aria-label="{c["label"]}" data-menu-overlay hidden>'
  '<div class="menu-shell"><div class="menu-head">'
  f'<a class="menu-brand" href="{brand_href}">HIPStudio</a><button class="menu-close" type="button" aria-label="{c["close"]}" data-menu-close>×</button>'
  '</div><div class="menu-layout"><nav class="menu-primary" aria-label="'+c['label']+'">'+''.join(items)+'</nav>'
  f'<aside class="menu-meta"><p class="eyebrow">{c["meta"]}</p><p>{c["note"]}</p><div class="menu-meta-links"><a href="mailto:info@hipstudio.hu">info@hipstudio.hu</a><a href="tel:+36302215506">+36 30 221 5506</a></div></aside>'
  '</div></div></div>'
 )

def main():
 if not DIST.exists(): raise SystemExit('dist-platform is missing; run build:platform first')
 shutil.copyfile(ROOT/'assets/platform-menu.css',ASSETS/'platform-menu.css')
 shutil.copyfile(ROOT/'assets/platform-menu.mjs',ASSETS/'platform-menu.mjs')
 changed=0
 for page in sorted(DIST.rglob('*.html')):
  text=page.read_text(encoding='utf-8')
  header=HEADER_RE.search(text)
  language=LANG_RE.search(text)
  if not header or not language: continue
  lang=language.group(1)
  old=header.group(0)
  lang_nav=LANG_NAV_RE.search(old)
  brand=BRAND_RE.search(old)
  if not lang_nav or not brand:
   raise SystemExit(f'Unsupported header shape: {page}')
  replacement=menu_markup(lang,path_for(page),brand.group(1),lang_nav.group(0))
  text=text[:header.start()]+replacement+text[header.end():]
  if 'platform-menu.css' not in text:
   text=text.replace('</head>','<link rel="stylesheet" href="/assets/platform-menu.css"><script type="module" src="/assets/platform-menu.mjs"></script></head>',1)
  page.write_text(text,encoding='utf-8')
  changed+=1
 if changed<3: raise SystemExit(f'Fullscreen navigation applied to too few pages: {changed}')
 print(f'Fullscreen editorial navigation applied to {changed} platform pages')

if __name__=='__main__': main()
