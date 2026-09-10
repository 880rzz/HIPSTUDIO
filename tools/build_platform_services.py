# coding: utf-8
"""Generate three-pillar service hubs, family pages and service pages from governed inventory.
Review-safe: no prices, no invented results, no deploy. Archive items are clearly separated.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlencode
import json, os

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'
INV=json.loads((R/'content/service-inventory.json').read_text())
DATA=json.loads((R/'content/platform.json').read_text())
MODE=os.environ.get('BUILD_MODE','review')
BASE=os.environ.get('PLATFORM_URL','https://www.hipstudio.hu').rstrip('/')
LANGS=['hu','en','de']
ROOT={'hu':'szolgaltatasok','en':'services','de':'leistungen'}
PSEG={'business':'business','creative':'hipstudio','experiences':'flugos'}
QUOTE={'hu':'ajanlatkeres','en':'request-a-quote','de':'angebot-anfragen'}
PILLAR_TITLE={
 'business':{'hu':'Business / Operations szolgáltatások','en':'Business / Operations services','de':'Business / Operations Leistungen'},
 'creative':{'hu':'HIPStudio kreatív szolgáltatások','en':'HIPStudio creative services','de':'HIPStudio Kreativleistungen'},
 'experiences':{'hu':'Flúgos vállalati élmények','en':'Flúgos corporate experiences','de':'Flúgos Unternehmenserlebnisse'}
}
PILLAR_INTRO={
 'business':{'hu':'Pénzügyi, adminisztrációs, működési, controlling és automatizálási szolgáltatási irányok. A felelősségi és szabályozott szolgáltatási körök élesítés előtt külön jóváhagyást igényelnek.','en':'Finance, administration, operations, controlling and automation service directions. Responsibility and regulated-service scope require separate approval before production.','de':'Leistungsrichtungen für Finanzen, Administration, Betrieb, Controlling und Automatisierung. Verantwortlichkeiten und regulierte Leistungsumfänge benötigen vor Veröffentlichung eine gesonderte Freigabe.'},
 'creative':{'hu':'Fotó, videó, streaming, podcast és tartalomrendszerek egy specialist kreatív pillérben.','en':'Photography, video, streaming, podcast and content systems in one specialist creative pillar.','de':'Fotografie, Video, Streaming, Podcast und Contentsysteme in einer spezialisierten Kreativsäule.'},
 'experiences':{'hu':'Vállalati élménytervezés, csapat- és vezetői programok, employer- és ügyfélélmények, valamint egyedi játékformátumok.','en':'Corporate experience design, team and leadership programmes, employer and client experiences, and custom game formats.','de':'Corporate Experience Design, Team- und Leadership-Programme, Employer- und Kundenerlebnisse sowie individuelle Spielformate.'}
}
FAMILY={
 'finance-admin':{'en':'Financial operations','de':'Finanzbetrieb'},'people-admin':{'en':'Payroll and HR administration','de':'Lohn- und HR-Administration'},'operations':{'en':'Back office and executive operations','de':'Backoffice und Executive Operations'},'control':{'en':'Controlling and management control','de':'Controlling und Managementsteuerung'},'grants':{'en':'Grant support','de':'Fördermittel-Support'},'ai-automation':{'en':'AI and automation','de':'KI und Automatisierung'},
 'photo-portrait':{'en':'Portrait and personal presence','de':'Porträt und persönlicher Auftritt'},'photo-corporate':{'en':'Corporate and advertising photography','de':'Unternehmens- und Werbefotografie'},'photo-event':{'en':'Event photography and activation','de':'Eventfotografie und Aktivierung'},'video':{'en':'Video and film','de':'Video und Film'},'podcast-content':{'en':'Podcast and content systems','de':'Podcast und Contentsysteme'},
 'corporate-experience':{'en':'Corporate Experience Design','de':'Corporate Experience Design'},'history-archive':{'en':'Flúgos history and archive','de':'Flúgos Geschichte und Archiv'}
}
NAMES={
 'financial-administration':('Financial administration','Finanzadministration'),'accounting-coordination':('Accounting coordination and administration support','Buchhaltungskoordination und Administrationssupport'),'cashflow-forecast-structure':('Cash-flow and forecast structure','Cashflow- und Forecast-Struktur'),'payroll-support':('Payroll support','Payroll-Support'),'hr-administration':('HR administration support','HR-Administrationssupport'),'back-office-support':('Back-office support','Backoffice-Support'),'executive-operations-support':('Executive operations support','Executive-Operations-Support'),'process-improvement':('Process improvement','Prozessverbesserung'),'operating-system-design':('Operating-system design','Gestaltung des Betriebssystems'),'management-reporting':('Management reporting','Management Reporting'),'controlling':('Controlling','Controlling'),'fractional-cfo-readiness':('Fractional CFO / finance-control direction','Fractional-CFO-/Finance-Control-Richtung'),'grant-support':('Grant support and coordination','Fördermittel-Support und Koordination'),'ai-readiness-audit':('AI readiness audit','KI-Readiness-Audit'),'automation-sprint':('Process-automation sprint','Prozessautomatisierungs-Sprint'),'managed-ai-operations':('Managed AI operations direction','Managed-AI-Operations-Richtung'),
 'business-portrait':('Business portrait','Businessporträt'),'executive-headshot':('Executive portrait / headshot','Executive-Porträt / Headshot'),'cv-photography':('CV photography','Bewerbungsfotografie'),'portfolio-photography':('Portfolio photography','Portfoliofotografie'),'fashion-photography':('Fashion photography','Modefotografie'),'personal-portrait':('Personal portrait / dating photography','Persönliches Porträt / Dating-Fotografie'),'fine-art-glamour-boudoir':('Fine-art / glamour / boudoir photography','Fine-Art-/Glamour-/Boudoir-Fotografie'),'team-group-portrait':('Team and group portraits','Team- und Gruppenporträts'),'brand-corporate-photography':('Brand and corporate photography','Brand- und Corporate-Fotografie'),'product-advertising-photography':('Product, advertising and campaign photography','Produkt-, Werbe- und Kampagnenfotografie'),'property-interior-architecture':('Property, interior and architecture photography','Immobilien-, Interior- und Architekturfotografie'),'aerial-photography':('Aerial photography','Luftaufnahmen'),'3d-virtual-tour':('3D virtual tour','Virtueller 3D-Rundgang'),'event-conference-photography':('Event and conference photography','Event- und Konferenzfotografie'),'souvenir-photography':('Souvenir photography and photo wall','Erinnerungsfotografie und Fotowand'),'onsite-printing':('On-site photo printing','Fotodruck vor Ort'),'greenbox-photography':('Green-screen photography','Greenscreen-Fotografie'),'commercial-brand-film':('Commercial / image / brand film','Werbe-/Image-/Brandfilm'),'executive-interview-video':('Interview and executive video','Interview- und Executive-Video'),'employer-branding-video':('Employer branding / recruitment video','Employer-Branding-/Recruiting-Video'),'event-conference-video':('Event and conference video','Event- und Konferenzvideo'),'sports-video':('Sports video','Sportvideo'),'concert-stage-video':('Concert and stage video','Konzert- und Bühnenvideo'),'music-video':('Music video','Musikvideo'),'conference-streaming':('Conference streaming','Konferenz-Streaming'),'live-projection':('Live venue projection','Liveprojektion vor Ort'),'video-podcast':('Video podcast','Video-Podcast'),'audio-podcast':('Audio podcast','Audio-Podcast'),'content-engine':('Content Engine / repurposing','Content Engine / Repurposing'),'ceo-content-system':('CEO Content System','CEO Content System'),'employer-branding-content':('Employer branding content system','Employer-Branding-Contentsystem'),
 'team-experience':('Team Experience / team building','Team Experience / Teambuilding'),'leadership-experience':('Leadership Experience','Leadership Experience'),'employer-experience':('Employer Experience','Employer Experience'),'client-experience':('Client Experience','Client Experience'),'custom-corporate-program':('Custom corporate programme','Individuelles Unternehmensprogramm'),'custom-branded-game':('Custom Branded Game','Custom Branded Game'),'flugos-futam-heritage':('Flúgos Futam history from 2009','Flúgos-Futam-Geschichte seit 2009'),'flugos-futam-2019':('Flúgos Futam 2019 archive','Flúgos Futam 2019 Archiv')
}
UI={
 'all':{'hu':'Összes szolgáltatás','en':'All services','de':'Alle Leistungen'},'families':{'hu':'Szolgáltatáscsaládok','en':'Service families','de':'Leistungsfamilien'},'services':{'hu':'Konkrét szolgáltatások','en':'Specific services','de':'Konkrete Leistungen'},'quote':{'hu':'Egyedi ajánlatot kérek','en':'Request a tailored quote','de':'Individuelles Angebot anfragen'},'archive':{'hu':'Történeti archívum','en':'Historical archive','de':'Historisches Archiv'},'back':{'hu':'Vissza a szolgáltatásokhoz','en':'Back to services','de':'Zurück zu den Leistungen'},'status':{'hu':'Publikációs státusz','en':'Publication status','de':'Publikationsstatus'},'mainNav':{'hu':'Fő navigáció','en':'Main navigation','de':'Hauptnavigation'},'footerNav':{'hu':'Lábléc navigáció','en':'Footer navigation','de':'Fußnavigation'}
}
STATUS={
 'verified_current':{'hu':'Jelenlegi, forrással igazolt szolgáltatás. A konkrét scope minden esetben egyedi ajánlatban rögzül.','en':'Current, source-verified service. The exact scope is confirmed in a tailored quote.','de':'Aktuelle, quellengeprüfte Leistung. Der genaue Umfang wird im individuellen Angebot festgelegt.'},
 'approved_extension':{'hu':'Jóváhagyott kínálati irány a közös platformban; a konkrét deliverable és scope egyedi egyeztetés tárgya.','en':'Approved offer direction in the unified platform; exact deliverables and scope are agreed individually.','de':'Freigegebene Angebotsrichtung der gemeinsamen Plattform; konkrete Deliverables und Umfang werden individuell abgestimmt.'},
 'strategic_gated':{'hu':'Stratégiai szolgáltatási irány. Éles szerződéses kommunikáció előtt a szolgáltatói felelősség és az esetleges szabályozott szakmai kör külön jóváhagyandó.','en':'Strategic service direction. Provider responsibility and any regulated professional scope must be approved before production contracting language is used.','de':'Strategische Leistungsrichtung. Anbieter-Verantwortung und gegebenenfalls regulierte Fachumfänge müssen vor produktiver Vertragskommunikation freigegeben werden.'},
 'archive_only':{'hu':'Történeti anyag. Nem aktuális kereskedelmi feltétel vagy jelenlegi szolgáltatásígéret.','en':'Historical material. This is not a current commercial condition or current service promise.','de':'Historisches Material. Dies ist keine aktuelle Geschäftsbedingung oder gegenwärtige Leistungszusage.'}
}

def e(v): return escape(str(v),quote=True)
def absu(p): return BASE+p
def home(l): return f'/{l}/'
def root_path(l): return f'/{l}/{ROOT[l]}/'
def pillar_path(pk,l): return f'{root_path(l)}{PSEG[pk]}/'
def family_path(pk,fk,l): return f'{pillar_path(pk,l)}{fk}/'
def service_path(pk,fk,sk,l): return f'{family_path(pk,fk,l)}{sk}/'
def quote_path(l,pillar=None,service=None):
 p=f'/{l}/{QUOTE[l]}/'
 q={}
 if pillar:q['pillar']=pillar
 if service:q['service']=service
 return p+('?' + urlencode(q) if q else '')
def label(service,l):
 if l=='hu': return service['label_hu']
 pair=NAMES.get(service['key'])
 return pair[0] if l=='en' and pair else pair[1] if pair else service['label_hu']
def family_label(fk,fam,l):
 if l=='hu':return fam['label_hu']
 return FAMILY.get(fk,{}).get(l,fam['label_hu'])
def langlinks(fn,l):return ''.join(f'<a lang="{x}" hreflang="{x}" href="{e(fn(x))}"'+(' aria-current="page"' if x==l else '')+f'>{x.upper()}</a>' for x in LANGS)
def nav(l):
 items=[(home(l),DATA['workingMasterBrand']),(root_path(l),UI['all'][l]),(pillar_path('business',l),'Business'),(pillar_path('creative',l),'HIPStudio'),(pillar_path('experiences',l),'Flúgos'),(quote_path(l),UI['quote'][l])]
 return ''.join(f'<a href="{e(p)}">{e(t)}</a>' for p,t in items)
def shell(path_fn,l,title,desc,body,crumbs,service_node=None):
 path=path_fn(l);url=absu(path)
 alts=''.join(f'<link rel="alternate" hreflang="{x}" href="{e(absu(path_fn(x)))}">' for x in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{e(absu(path_fn("hu")))}">'
 bc=[]
 for pos,(name,p) in enumerate(crumbs,1):bc.append({'@type':'ListItem','position':pos,'name':name,'item':absu(p)})
 graph=[{'@type':'WebSite','@id':BASE+'/#website','name':DATA['workingMasterBrand'],'url':BASE+'/'},{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':l,'isPartOf':{'@id':BASE+'/#website'}},{'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':bc}]
 if service_node:graph.append(service_node)
 ld=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 review='<div class="review">Platform review build · no production publication</div>' if MODE=='review' else ''
 meta=f'{title} | {DATA["workingMasterBrand"]}'
 html=f'''<!DOCTYPE html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(meta[:72])}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="{'noindex,nofollow' if MODE=='review' else 'index,follow'}"><link rel="canonical" href="{e(url)}">{alts}<link rel="stylesheet" href="/assets/platform.css"><script type="application/ld+json">{ld}</script></head><body><a class="skip" href="#main">Skip</a>{review}<header class="header"><a class="brand" href="{e(home(l))}">{e(DATA['workingMasterBrand'])}</a><nav class="nav" aria-label="{e(UI['mainNav'][l])}">{nav(l)}</nav><nav class="langs" aria-label="Languages">{langlinks(path_fn,l)}</nav></header><main id="main">{body}</main><footer class="footer"><strong>{e(DATA['workingMasterBrand'])}</strong><nav aria-label="{e(UI['footerNav'][l])}">{nav(l)}</nav><p class="legal-note">Service inventory is evidence-gated. No public prices, invented client results, legal ownership or unsupported regulated-service responsibility are asserted.</p></footer></body></html>'''
 out=D/path.strip('/')/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html)
 return {'key':'service-content','lang':l,'path':path,'canonical':url}

if not D.exists():raise SystemExit('dist-platform missing')
manifest=json.loads((D/'platform-build.json').read_text())
existing={(p['path'],p['lang']) for p in manifest['pages']}
new=[]
# Global service hub
for l in LANGS:
 cards=''.join(f'<a class="card" href="{e(pillar_path(pk,l))}"><p class="eyebrow">{e(pdata["brand"])}</p><h2>{e(PILLAR_TITLE[pk][l])}</h2><p>{e(PILLAR_INTRO[pk][l])}</p><span aria-hidden="true">↗</span></a>' for pk,pdata in INV['pillars'].items())
 title=UI['all'][l];desc={'hu':'A Business, HIPStudio és Flúgos teljes, státusz szerint kezelt szolgáltatási térképe.','en':'The complete status-governed service map for Business, HIPStudio and Flúgos.','de':'Die vollständige, statusgesteuerte Leistungsübersicht für Business, HIPStudio und Flúgos.'}[l]
 body=f'<section class="page-hero"><p class="eyebrow">{e(DATA["positioning"][l])}</p><h1>{e(title)}</h1><p class="lead">{e(desc)}</p></section><section class="section"><div class="cards">{cards}</div></section>'
 new.append(shell(root_path,l,title,desc,body,[(DATA['workingMasterBrand'],home(l)),(title,root_path(l))]))
# Pillars, families, services
for pk,pdata in INV['pillars'].items():
 for l in LANGS:
  famcards=''.join(f'<a class="card" href="{e(family_path(pk,fk,l))}"><h2>{e(family_label(fk,fam,l))}</h2><p>{len(fam["services"])} {e(UI["services"][l].lower())}</p><span aria-hidden="true">↗</span></a>' for fk,fam in pdata['families'].items())
  title=PILLAR_TITLE[pk][l];desc=PILLAR_INTRO[pk][l]
  body=f'<section class="page-hero"><a class="back" href="{e(root_path(l))}">← {e(UI["back"][l])}</a><p class="eyebrow">{e(pdata["brand"])}</p><h1>{e(title)}</h1><p class="lead">{e(desc)}</p></section><section class="section"><h2>{e(UI["families"][l])}</h2><div class="cards">{famcards}</div></section>'
  new.append(shell(lambda x,pk=pk:pillar_path(pk,x),l,title,desc,body,[(DATA['workingMasterBrand'],home(l)),(UI['all'][l],root_path(l)),(title,pillar_path(pk,l))]))
 for fk,fam in pdata['families'].items():
  for l in LANGS:
   fl=family_label(fk,fam,l); archive_family=all(s.get('archive_only') for s in fam['services'])
   cards=''.join(f'<a class="card" href="{e(service_path(pk,fk,s["key"],l))}"><p class="eyebrow">{e(UI["archive"][l] if s.get("archive_only") else pdata["brand"])}</p><h3>{e(label(s,l))}</h3><span aria-hidden="true">↗</span></a>' for s in fam['services'])
   desc=(STATUS['archive_only'][l] if archive_family else {'hu':'A szolgáltatáscsalád elemei külön oldalon, egységes ajánlatkérési útvonallal.','en':'Each service in this family has its own page and a consistent quote-request path.','de':'Jede Leistung dieser Familie hat eine eigene Seite und einen einheitlichen Angebotsweg.'}[l])
   body=f'<section class="page-hero"><a class="back" href="{e(pillar_path(pk,l))}">← {e(PILLAR_TITLE[pk][l])}</a><p class="eyebrow">{e(pdata["brand"])}</p><h1>{e(fl)}</h1><p class="lead">{e(desc)}</p></section><section class="section"><div class="cards">{cards}</div></section>'
   new.append(shell(lambda x,pk=pk,fk=fk:family_path(pk,fk,x),l,fl,desc,body,[(DATA['workingMasterBrand'],home(l)),(UI['all'][l],root_path(l)),(PILLAR_TITLE[pk][l],pillar_path(pk,l)),(fl,family_path(pk,fk,l))]))
  for s in fam['services']:
   for l in LANGS:
    title=label(s,l);fl=family_label(fk,fam,l);status=s['status'];archive=s.get('archive_only',False)
    desc=STATUS[status][l]
    if archive:
     cta=f'<section class="cta"><h2>{e(UI["archive"][l])}</h2><p>{e(STATUS["archive_only"][l])}</p></section>'
     service_node=None
    else:
     qp=quote_path(l,pk,s['quote_request_key'])
     cta=f'<section class="cta"><h2>{e(UI["quote"][l])}</h2><p>{e(STATUS[status][l])}</p><a class="button" href="{e(qp)}">{e(UI["quote"][l])} →</a></section>'
     service_node={'@type':'Service','@id':absu(service_path(pk,fk,s['key'],l))+'#service','name':title,'serviceType':title,'description':desc,'url':absu(service_path(pk,fk,s['key'],l))}
    body=f'<section class="page-hero"><a class="back" href="{e(family_path(pk,fk,l))}">← {e(fl)}</a><p class="eyebrow">{e(pdata["brand"])} · {e(UI["status"][l])}</p><h1>{e(title)}</h1><p class="lead">{e(desc)}</p></section><section class="section"><div class="section-head"><h2>{e(fl)}</h2><p>{e(PILLAR_INTRO[pk][l])}</p></div><p class="note">{e(STATUS[status][l])}</p></section>{cta}'
    new.append(shell(lambda x,pk=pk,fk=fk,s=s:service_path(pk,fk,s['key'],x),l,title,desc,body,[(DATA['workingMasterBrand'],home(l)),(UI['all'][l],root_path(l)),(PILLAR_TITLE[pk][l],pillar_path(pk,l)),(fl,family_path(pk,fk,l)),(title,service_path(pk,fk,s['key'],l))],service_node))
for p in new:
 if (p['path'],p['lang']) not in existing:manifest['pages'].append(p)
manifest['serviceInventory']={'version':INV['version'],'localizedPages':len(new),'services':sum(len(f['services']) for p in INV['pillars'].values() for f in p['families'].values()),'families':sum(len(p['families']) for p in INV['pillars'].values())}
(D/'platform-build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
if MODE=='production':
 sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(p["canonical"])}</loc></url>' for p in manifest['pages'])+'</urlset>'
 (D/'sitemap.xml').write_text(sitemap)
print(f'Generated service inventory pages: {len(new)} localized pages; total={len(manifest["pages"])}')
