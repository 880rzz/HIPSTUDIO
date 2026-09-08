# coding: utf-8
"""Static HTML build. No network, no deployment. Production requires approvals."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit,quote,unquote
import sys,json,os,hashlib,base64,shutil
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'content'))
from site_copy import UI,ROUTES,FAQ,PROCESS,LEGAL_ITEMS
from services import tr
from calculator import calculator
DATA=json.loads((R/'content/services.json').read_text())
SOLUTIONS=json.loads((R/'content/solutions.json').read_text())
PEOPLE=json.loads((R/'content/people.json').read_text())
CASE_STUDIES=json.loads((R/'content/case_studies.json').read_text())
PROVENANCE=json.loads((R/'content/provenance.json').read_text())
PRIVACY_CONFIG=json.loads((R/'content/privacy-config.json').read_text())
IMAGES=json.loads((R/'content/images.json').read_text()); IMAGE={i['id']:i for i in IMAGES}
CLIENT_LOGOS=json.loads((R/'audit/client-logo-manifest.json').read_text()) if (R/'audit/client-logo-manifest.json').exists() else []
VIDEOS=json.loads((R/'content/videos.json').read_text())
PRICING=json.loads((R/'content/pricing.json').read_text())
APPROVALS=json.loads((R/'content/approvals.json').read_text())
MODE=os.environ.get('BUILD_MODE','review');BASE=os.environ.get('SITE_URL','https://www.hipstudio.hu').rstrip('/')
if MODE not in ['review','production']:raise SystemExit('BUILD_MODE must be review or production')
if MODE=='production':
 missing=[k for k in ['imageRights','pricing','legal','publication'] if not APPROVALS.get(k)]
 if (R/'audit/pending-images.json').exists() and json.loads((R/'audit/pending-images.json').read_text()):missing.append('mediaReview')
 if missing:raise SystemExit('Production blocked: approvals missing: '+', '.join(missing))
if not BASE.startswith('https://') or urlsplit(BASE).query or urlsplit(BASE).fragment:raise SystemExit('SITE_URL must be an HTTPS origin with optional project path')
PREFIX=urlsplit(BASE).path.rstrip('/')
D=R/'dist'
if D.exists():shutil.rmtree(D)
D.mkdir();shutil.copytree(R/'assets',D/'assets',ignore=shutil.ignore_patterns('photos'))
(D/'assets/photos').mkdir()
for picture in IMAGES:
 for width in [480,960,1440]:
  filename=f"{picture['id']}-{width}.webp"
  shutil.copyfile(R/'assets/photos'/filename,D/'assets/photos'/filename)
CSS='site.'+hashlib.sha256((R/'assets/site.css').read_bytes()).hexdigest()[:12]+'.css'
(D/'assets/site.css').rename(D/'assets'/CSS)
LANGS=['hu','en','de'];LOCALES={'hu':'hu_HU','en':'en_GB','de':'de_DE'}
SERVICE={s['key']:s for s in DATA}
SOLUTION={s['key']:s for s in SOLUTIONS}
PERSON={p['key']:p for p in PEOPLE}
PAGES=[]
def e(v):return escape(str(v),quote=True)
def ui(k,l):return UI[k][l]
def route(key,l):
 if key in ROUTES:return '/'+l+'/'+(ROUTES[key][l]+'/' if ROUTES[key][l] else '')
 if key.startswith('solution:'):
  item=SOLUTION[key.split(':',1)[1]]
  return '/'+l+'/'+ROUTES['solutions'][l]+'/'+item['slug'][l]+'/'
 if key.startswith('person:'):
  item=PERSON[key.split(':',1)[1]]
  return '/'+l+'/'+ROUTES['people'][l]+'/'+item['slug'][l]+'/'
 if key.startswith('case:'):
  item=next(item for item in CASE_STUDIES['items'] if item['key']==key.split(':',1)[1])
  return '/'+l+'/'+ROUTES['cases'][l]+'/'+item['slug'][l]+'/'
 return '/'+l+'/'+ROUTES['services'][l]+'/'+SERVICE[key]['slug'][l]+'/'
def href(key,l):return PREFIX+route(key,l)
def absolute(key,l):return BASE+route(key,l)
def asset(path):return PREFIX+'/assets/'+path

def img(i,l,hero=False,gallery=False):
 m=IMAGE[i];sizes='(max-width: 700px) 100vw, 60vw' if hero else '(max-width: 700px) 100vw, 45vw'
 if gallery:sizes='(max-width: 420px) calc(100vw - 40px), (max-width: 1000px) 45vw, 30vw'
 variants={m.get('variants',{}).get(str(w),{}).get('width',min(w,m['width'])):w for w in [480,960,1440]}
 sources=', '.join(asset('photos/'+i+'-'+str(w)+'.webp')+' '+str(actual)+'w' for actual,w in variants.items())
 return f'<img src="{asset("photos/"+i+"-960.webp")}" srcset="{sources}" sizes="{sizes}" width="{m["width"]}" height="{m["height"]}" alt="{e(m["alt"][l])}" loading="{"eager" if hero else "lazy"}" decoding="async"'+(' fetchpriority="high"' if hero else '')+'>'

def fqs(items,l):
 return '<div class="faq-list">'+''.join(f'<details><summary>{e(q[l])}</summary><p>{e(a[l])}</p></details>' for q,a in items)+'</div>'

def cta(l):return f'<section class="cta"><p class="eyebrow">HIPStudio · Budapest</p><h2>{e(ui("cta",l))}</h2><p>{e(ui("quoteNote",l))}</p><a class="button light" href="{href("contact",l)}">{e(ui("quote",l))} <span aria-hidden="true">↗</span></a></section>'

def render(key,l,title,desc,body,faq=None,image_id=None,page_type='WebPage',script=False):
 url=absolute(key,l);org=BASE+'/#organization';website=BASE+'/#website'
 graph=[{'@type':['Organization','ProfessionalService'],'@id':org,'name':'HIPStudio','legalName':'Hipstudió Korlátolt Felelősségű Társaság','url':BASE+'/','sameAs':['https://www.wikidata.org/wiki/Q138482177'],'foundingDate':'2006-02-27','telephone':'+36302215506','email':'info@hipstudio.hu','address':{'@type':'PostalAddress','streetAddress':'Lágymányosi utca 15.','postalCode':'1111','addressLocality':'Budapest','addressCountry':'HU'},'contactPoint':{'@id':BASE+'/#contact'},'founder':{'@id':BASE+'/#norbert-banhalmi'}},
 {'@type':'ContactPoint','@id':BASE+'/#contact','contactType':'customer enquiries','email':'info@hipstudio.hu','telephone':'+36302215506'},
 {'@type':'Person','@id':BASE+'/#norbert-banhalmi','name':'Bánhalmi Norbert','url':'https://www.norbertbanhalmi.com/','sameAs':['https://www.wikidata.org/wiki/Q56391118']},
 {'@type':'Person','@id':BASE+'/#viko-speier','name':'Speier Vikó','alternateName':'Speier Viktória','url':'https://www.vikospeier.com/'},
 {'@type':'WebSite','@id':website,'name':'HIPStudio','url':BASE+'/','inLanguage':LANGS,'publisher':{'@id':org}},
 {'@type':page_type,'@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':l,'isPartOf':{'@id':website},'about':{'@id':org}},
 {'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':ui('home',l),'item':absolute('home',l)}]+([] if key=='home' else [{'@type':'ListItem','position':2,'name':title,'item':url}])}]
 if key in SERVICE:
  graph.append({'@type':'Service','@id':url+'#service','name':SERVICE[key]['name'][l],'serviceType':SERVICE[key]['name'][l],'description':desc,'url':url,'provider':{'@id':org},'areaServed':{'@type':'City','name':'Budapest'}})
 if key.startswith('solution:'):
  solution=SOLUTION[key.split(':',1)[1]]
  graph.append({'@type':'Service','@id':url+'#solution','name':solution['name'][l],'description':desc,'url':url,'provider':{'@id':org},'areaServed':{'@type':'City','name':'Budapest'},'hasPart':[{'@id':absolute(service,l)+'#service'} for service in solution['services']]})
  graph[5]['mainEntity']={'@id':url+'#solution'}
 if key.startswith('person:'):
  person=PERSON[key.split(':',1)[1]]
  person_id=BASE+('/#norbert-banhalmi' if person['key']=='banhalmi-norbert' else '/#viko-speier')
  graph[5]['mainEntity']={'@id':person_id}
 if key.startswith('case:'):
  graph.append({'@type':'CreativeWork','@id':url+'#case-study','name':title,'description':desc,'url':url,'publisher':{'@id':org},'inLanguage':l})
  graph[5]['mainEntity']={'@id':url+'#case-study'}
 if image_id:
  graph.append({'@type':'ImageObject','@id':url+'#image','contentUrl':BASE+'/assets/photos/'+image_id+'-1440.webp','caption':IMAGE[image_id]['alt'][l],'width':min(1440,IMAGE[image_id]['width'])})
  graph[5]['primaryImageOfPage']={'@id':url+'#image'}
 if faq:
  graph.append({'@type':'FAQPage','@id':url+'#faq','inLanguage':l,'mainEntity':[{'@type':'Question','name':q[l],'acceptedAnswer':{'@type':'Answer','text':a[l]}} for q,a in faq]})
 ld=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 ld_hash=base64.b64encode(hashlib.sha256(ld.encode()).digest()).decode()
 csp=f"default-src 'self'; script-src 'self' 'sha256-{ld_hash}'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
 links=''.join(f'<link rel="alternate" hreflang="{a}" href="{e(absolute(key,a))}">' for a in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{e(absolute(key,"hu"))}">'
 nav=''.join(f'<a href="{href(k,l)}"'+(' aria-current="page"' if k==key or (k=='solutions' and key.startswith('solution:')) else '')+f'>{e(ui(k,l))}</a>' for k in ['solutions','work','cases','contact'])
 languages=''.join(f'<a lang="{a}" hreflang="{a}" href="{href(key,a)}"'+(' aria-current="page"' if a==l else '')+f'>{a.upper()}</a>' for a in LANGS)
 footer=''.join(f'<a href="{href(k,l)}">{e(ui(k,l))}</a>' for k in ['services','people','prices','studio','partners','faq','trust','legal','cookies'])
 ogimage=BASE+'/assets/photos/'+(image_id or 'portrait-20')+'-1440.webp'
 html=f'''<!DOCTYPE html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="{e(csp)}"><meta name="referrer" content="strict-origin-when-cross-origin"><title>{e(title)} | HIPStudio</title><meta name="description" content="{e(desc)}"><meta name="robots" content="{'noindex,nofollow' if MODE=='review' else 'index,follow'}"><link rel="canonical" href="{e(url)}">{links}<meta property="og:type" content="website"><meta property="og:locale" content="{LOCALES[l]}"><meta property="og:site_name" content="HIPStudio"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{ogimage}"><meta property="og:image:alt" content="{e(IMAGE[image_id or 'portrait-20']['alt'][l])}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="{asset('favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{asset(CSS)}"><script type="application/ld+json">{ld}</script><script type="module" src="{asset("consent.mjs")}"></script>{f'<script type="module" src="{asset("calculator.mjs")}"></script>' if script else ''}</head><body><a class="skip" href="#main">{e(ui('skip',l))}</a>{f'<div class="review-bar">{e(ui("localReview",l))}</div>' if MODE=='review' else ''}<header class="header"><a class="wordmark" href="{href('home',l)}" aria-label="HIPStudio — {e(ui('home',l))}">HIP<span>Studio</span></a><nav class="desktop-nav" aria-label="{e(ui('nav',l))}">{nav}</nav><nav class="languages" aria-label="{e(ui('lang',l))}">{languages}</nav><details class="mobile-menu"><summary>{e(ui('menu',l))}</summary><nav aria-label="{e(ui('menu',l))}">{nav}{footer}</nav></details></header><main id="main" tabindex="-1">{body}</main><footer class="footer"><div><a class="wordmark" href="{href('home',l)}">HIP<span>Studio</span></a><p>1111 Budapest, Lágymányosi utca 15.</p><a href="mailto:info@hipstudio.hu">info@hipstudio.hu</a><a href="tel:+36302215506">+36 30 221 5506</a></div><nav aria-label="{e(ui('related',l))}">{footer}</nav><p class="copyright">© HIPStudio Kft.</p></footer></body></html>'''
 out=D/route(key,l).strip('/')/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html)
 PAGES.append({'path':route(key,l),'url':url,'key':key,'lang':l,'title':title})

def heading(title,intro,l,kicker='HIPStudio · Budapest'):
 return f'<section class="page-heading"><p class="eyebrow">{e(kicker)}</p><h1>{e(title)}</h1><p class="lead">{e(intro)}</p></section>'

def cards(keys,l):
 return '<div class="service-list">'+''.join(f'<a class="service-card" href="{href(k,l)}"><h3>{e(SERVICE[k]["name"][l])}</h3><p>{e(SERVICE[k]["intro"][l])}</p><span aria-hidden="true">↗</span></a>' for k in keys)+'</div>'

def solution_cards(items,l):
 return '<div class="solution-grid">'+''.join(f'<a class="solution-card" href="{href("solution:"+item["key"],l)}"><p class="eyebrow">{e(item["audience"][l])}</p><h2>{e(item["name"][l])}</h2><p>{e(item["problem"][l])}</p><span aria-hidden="true">↗</span></a>' for item in items)+'</div>'

def case_study_body(item,l):
 sections=[('decision','challenge'),('process','method'),('goal','outcome')]
 body=heading(item['title'][l],item['scope'][l],l)
 body+='<section class="reading">'
 for label,field in sections:
  if item.get(field,{}).get(l):body+=f'<h2>{e(ui(label,l))}</h2><p>{e(item[field][l])}</p>'
 body+='</section>'
 if item.get('services'):body+=f'<section class="section"><h2>{e(ui("capabilities",l))}</h2>{cards(item["services"],l)}</section>'
 return body+cta(l)

def client_grid():
 return '<div class="client-grid">'+''.join(f'<figure><img src="{asset("logos/"+logo["id"]+".webp")}" width="{logo["width"]}" height="{logo["height"]}" alt="{e(tr("Ügyfél- vagy partnerreferencia logó || Client or partner reference logo || Logo einer Kunden- oder Partnerreferenz")[l])}" loading="lazy" decoding="async"><figcaption>© HIPStudio</figcaption></figure>' for logo in CLIENT_LOGOS)+'</div>'

CLUSTER_IMAGES={'portrait':'portrait-20','commercial':'commercial-17','space':'property-04','art':'portfolio-15','event':'commercial-11','film':'portfolio-11'}
HERO={'cv':'portrait-17','business':'portrait-20','headshot':'portrait-10','dating':'portrait-04','portfolio':'portfolio-13','fashion':'portfolio-01','advertising':'commercial-17','product':'commercial-17','catalogue':'commercial-14','property':'property-04','aerial':'property-10','virtual':'property-19','nude':'art-04','boudoir':'art-03','event':'commercial-11','video':'portfolio-11','shoot':'portfolio-11','werk':'portfolio-11','social':'commercial-20','podcast':'portrait-02','executive':'portrait-12','brand':'portfolio-17','positioning':'portfolio-12','fineart':'portfolio-15','clevel':'portrait-24'}
# Film/podcast/event pages do not label unrelated photographs as their project references.
for l in LANGS:
 home=f'<section class="home-hero"><div class="hero-copy"><p class="eyebrow">Budapest · {e(ui("photography",l))} / Film / Podcast</p><h1>{e(ui("homeTitle",l))}</h1><p class="lead">{e(ui("homeIntro",l))}</p><a class="button" href="{href("solutions",l)}">{e(ui("solutions",l))} <span aria-hidden="true">↗</span></a></div><figure class="hero-image">{img("portrait-20",l,True)}<figcaption>HIPStudio · {e(ui("photography",l))}</figcaption></figure><div class="hero-index" aria-hidden="true">01 — HIPStudio</div></section>'
 home+=f'<section class="heritage"><p class="heritage-year">2006</p><div><p class="eyebrow">{e(ui("visualTrust",l))}</p><h2>{e(ui("homeEditorial",l))}</h2><p>{e(ui("homeBody",l))}</p><a href="{href("people",l)}">{e(ui("people",l))} ↗</a></div></section><section class="section"><div class="section-heading"><h2>{e(ui("solutions",l))}</h2><a href="{href("solutions",l)}">{e(ui("allSolutions",l))} ↗</a></div>{solution_cards(SOLUTIONS,l)}</section>'
 home+=f'<section class="diptych"><figure>{img("portfolio-07",l)}<figcaption>{e(ui("portraitGroup",l))}</figcaption></figure><figure>{img("property-06",l)}<figcaption>{e(ui("spaceGroup",l))}</figcaption></figure></section>'+cta(l)
 render('home',l,ui('homeTitle',l),ui('homeIntro',l),home,image_id='portrait-20')
 content=heading(ui('solutions',l),ui('solutionIntro',l),l)+f'<section class="section">{solution_cards(SOLUTIONS,l)}</section>'+cta(l)
 render('solutions',l,ui('solutions',l),ui('solutionIntro',l),content,page_type='CollectionPage')
 for solution in SOLUTIONS:
  k='solution:'+solution['key']
  content=heading(solution['name'][l],solution['audience'][l],l)
  content+=f'<section class="reading"><h2>{e(ui("decision",l))}</h2><p>{e(solution["problem"][l])}</p><h2>{e(ui("approach",l))}</h2><p>{e(solution["approach"][l])}</p></section><section class="section"><h2>{e(ui("capabilities",l))}</h2>{cards(solution["services"],l)}</section>'
  render(k,l,solution['name'][l],solution['problem'][l],content+cta(l),page_type='WebPage')
 content=heading(ui('cases',l),ui('caseIntro',l),l)+f'<section class="reading"><p class="evidence-note">{e(ui("casePending",l))}</p><p><a href="{href("work",l)}">{e(ui("work",l))} ↗</a></p></section>'+cta(l)
 render('cases',l,ui('cases',l),ui('caseIntro',l),content,page_type='CollectionPage')
 for item in CASE_STUDIES['items']:
  if item.get('status')=='approved':render('case:'+item['key'],l,item['title'][l],item['scope'][l],case_study_body(item,l),page_type='ProfilePage')
 content=heading(ui('people',l),ui('peopleIntro',l),l)+f'<section class="people-grid">'
 for person in PEOPLE:
  content+=f'<a class="person-card" href="{href("person:"+person["key"],l)}"><p class="partner-role">{e(person["role"][l])}</p><h2>{e(person["name"])}</h2><p>{e(person["summary"][l])}</p><span aria-hidden="true">↗</span></a>'
 content+='</section>'+cta(l)
 render('people',l,ui('people',l),ui('peopleIntro',l),content,page_type='CollectionPage')
 for person in PEOPLE:
  k='person:'+person['key'];content=heading(person['name'],person['role'][l],l)
  content+=f'<section class="reading"><h2>{e(ui("verifiedFacts",l))}</h2><p>{e(person["summary"][l])}</p><p><a href="{e(person["url"])}" rel="external">{e(person["name"])} ↗</a></p>'
  content+=''.join(f'<p><a href="{e(source)}" rel="external">Wikidata ↗</a></p>' for source in person['sameAs'])+'</section>'+cta(l)
  render(k,l,person['name'],person['summary'][l],content,page_type='ProfilePage')
 content=heading(ui('trust',l),ui('trustIntro',l),l)+f'<section class="reading"><h2>{e(ui("verifiedFacts",l))}</h2><dl><dt>HIPStudio</dt><dd>2006-02-27 · <a href="https://www.wikidata.org/wiki/Q138482177">Wikidata Q138482177</a></dd><dt>Bánhalmi Norbert</dt><dd>{e(PERSON["banhalmi-norbert"]["role"][l])} · <a href="https://www.wikidata.org/wiki/Q56391118">Wikidata Q56391118</a></dd></dl><h2>{e(ui("sourceRegister",l))}</h2><p><a href="{PREFIX}/provenance.json">provenance.json</a> · <a href="{PREFIX}/entity.json">entity.json</a> · <a href="{PREFIX}/llms.txt">llms.txt</a></p><h2>{e(ui("aiTrust",l))}</h2><p>{e(ui("aiBody",l))}</p></section>'
 render('trust',l,ui('trust',l),ui('trustIntro',l),content,page_type='AboutPage')
 content=heading(ui('services',l),ui('serviceIntro',l),l)
 for cluster in CLUSTER_IMAGES:
  content+=f'<section class="section" id="{cluster}"><h2>{e(ui(cluster+"Group",l))}</h2>'+cards([s['key'] for s in DATA if s['cluster']==cluster],l)+'</section>'
 render('services',l,ui('services',l),ui('serviceIntro',l),content+cta(l))
 for s in DATA:
  k=s['key'];hero=HERO.get(k,CLUSTER_IMAGES[s['cluster']]);q=[(s['question'],s['answer']),FAQ[6],FAQ[8],FAQ[9]]
  content=heading(s['name'][l],s['intro'][l],l)
  # Only show relevant gallery images on photography pages; film is text-led.
  if s['cluster'] not in ['film','event']:content+=f'<figure class="service-hero">{img(hero,l,True)}<figcaption>{e(IMAGE[hero]["alt"][l])}</figcaption></figure>'
  content+=f'<section class="reading"><h2>{e(ui("goal",l))}</h2><p>{e(s["result"][l])}</p><h2>{e(ui("brief",l))}</h2><p>{e(s["brief"][l])}</p><h2>{e(ui("process",l))}</h2><ol class="process">'+''.join(f'<li>{e(t[l])}</li>' for t in PROCESS[s['cluster']])+f'</ol><h2>{e(ui("reference",l))}</h2>'
  reference_key={'portrait':'portrait','commercial':'commercial','space':'property','art':'art'}.get(s['cluster'])
  if reference_key:content+=f'<a class="text-link" href="{href("work",l)}#{reference_key}">{e(ui("work",l))} ↗</a>'
  else:content+=f'<p><a class="text-link" href="{e(s["reference"])}" rel="external">{e(ui("sourceLink",l))} ↗</a></p>'
  if k=='virtual':content+='<p><a href="https://my.matterport.com/show/?m=uHq2PVEUSQX" rel="external">Matterport · HIPStudio ↗</a></p>'
  content+=f'<h2>{e(ui("prices",l))}</h2><p>{e(ui("priceNote",l))}</p><a href="{href("prices",l)}">{e(ui("prices",l))} ↗</a><h2>{e(ui("faq",l))}</h2>{fqs(q,l)}</section>'
  related=[x['key'] for x in DATA if x['cluster']==s['cluster'] and x['key']!=k][:3]
  if related:content+=f'<section class="section"><h2>{e(ui("related",l))}</h2>{cards(related,l)}</section>'
  render(k,l,s['name'][l],s['intro'][l],content+cta(l),q,hero if s['cluster'] not in ['film','event'] else None)
 content=heading(ui('work',l),ui('galleryNote',l),l)
 seen_gallery_sha=set()
 for cat,cluster in [('portrait','portrait'),('portfolio','portrait'),('commercial','commercial'),('property','space'),('art','art')]:
  content+=f'<section class="section gallery-section" id="{cat}"><h2>{e(ui(cluster+"Group",l))}'+(' · Portfolio' if cat=='portfolio' else '')+'</h2><div class="gallery">'
  for m in IMAGES:
   if m['category']==cat and m['sha256'] not in seen_gallery_sha:
    seen_gallery_sha.add(m['sha256'])
    content+=f'<figure><a href="{asset("photos/"+m["id"]+"-1440.webp")}">{img(m["id"],l,hero=m["id"]=="portrait-01",gallery=True)}</a><figcaption>© HIPStudio</figcaption></figure>'
  content+='</div></section>'
 content+=f'<section class="reading" id="films"><h2>{e(ui("film",l))}</h2><ul>'
 for n,v in enumerate(VIDEOS):
  label='HIPStudio Showreel' if n==0 else tr('Referenciafilm || Reference film || Referenzfilm')[l]+f' {n:02d}'
  content+=f'<li><a href="{e(v["url"])}" rel="external">{e(label)} ↗</a></li>'
 content+='</ul></section>'
 render('work',l,ui('work',l),ui('galleryNote',l),content+cta(l),page_type='CollectionPage')
 render('faq',l,ui('faq',l),ui('quoteNote',l),heading(ui('faq',l),ui('quoteNote',l),l)+f'<section class="reading">{fqs(FAQ,l)}</section>'+cta(l),FAQ)
 content=heading(ui('contact',l),ui('cta',l),l)+f'<section class="contact-grid"><div><h2>{e(ui("quote",l))}</h2><a class="contact-big" href="mailto:info@hipstudio.hu">info@hipstudio.hu ↗</a><a class="contact-big" href="tel:+36302215506">+36 30 221 5506</a><p>1111 Budapest<br>Lágymányosi utca 15.</p></div><div><h2>{e(ui("brief",l))}</h2><p>{e(FAQ[6][1][l])}</p><p>{e(ui("quoteNote",l))}</p><a href="{href("legal",l)}">{e(ui("legal",l))} ↗</a></div></section>'
 render('contact',l,ui('contact',l),ui('quoteNote',l),content,page_type='ContactPage')
 studio_intro=tr('Találkozási pont a közös munkához, Budapest XI. kerületében. || A place to meet and create in Budapest’s 11th district. || Ein Ort zum Kennenlernen und Gestalten im 11. Bezirk von Budapest.')[l]
 content=heading(ui('studio',l),studio_intro,l)+f'<section class="reading"><h2>1111 Budapest, Lágymányosi utca 15.</h2><p>{e(FAQ[5][1][l])}</p><p>{e(tr("Személyes egyeztetéshez kérjen időpontot emailben vagy telefonon. A helyszín pontos felszereltségét és az akadálymentes bejutás lehetőségét érkezés előtt egyeztetjük. || Arrange a visit by email or telephone. Please discuss equipment and step-free access before arriving. || Vereinbaren Sie einen Besuch per E-Mail oder Telefon. Bitte klären Sie Ausstattung und barrierefreien Zugang vor Ihrer Ankunft.")[l])}</p><a class="button" href="{href("contact",l)}">{e(ui("contact",l))} ↗</a></section>'
 render('studio',l,ui('studio',l),studio_intro,content)
 partner_intro=tr('Alapítói irány, független szakmai partnerségek és egy nagy szakembergárda. || Founder-led direction, independent professional partnerships and a broad expert team. || Gründungsgeleitete Richtung, unabhängige Fachpartnerschaften und ein großes Expertenteam.')[l]
 partner_note=tr('A HIPStudio kommunikációs és kreatív márkát Bánhalmi Norbert alapította 2006. február 27-én. A HIPStudio nem egyszemélyes fotóstúdió: minden feladathoz több szakterületet lefedő csapat áll össze. Bánhalmi Norbert és Speier Vikó független szakmai partnerek; projektben betöltött szerepüket és a szerződő felet minden esetben az ajánlat és a szerződés rögzíti. || Bánhalmi Norbert founded the HIPStudio communications and creative brand on 27 February 2006. HIPStudio is not a one-person photography studio: each assignment is planned with specialists from the relevant disciplines. Bánhalmi Norbert and Speier Vikó are independent professional partners; their project roles and the contracting party are always set out in the quote and agreement. || Bánhalmi Norbert gründete die Kommunikations- und Kreativmarke HIPStudio am 27. Februar 2006. HIPStudio ist kein Ein-Personen-Fotostudio: Für jede Aufgabe wird ein Team aus den passenden Fachbereichen zusammengestellt. Bánhalmi Norbert und Speier Vikó sind unabhängige Fachpartner; Rollen im Projekt und Vertrag werden stets im Angebot und Vertrag festgehalten.')[l]
 content=heading(ui('partners',l),partner_intro,l)+f'<section class="reading"><p class="history-note">{e(partner_note)}</p><h2>Bánhalmi Norbert</h2><p class="partner-role">{e(tr("Alapító · szakmai partner || Founder · professional partner || Gründer · Fachpartner")[l])}</p><a href="https://www.norbertbanhalmi.com/">BANHALMI ↗</a><h2>Speier Vikó</h2><p class="partner-role">{e(tr("Szakmai partner || Professional partner || Fachpartner")[l])}</p><a href="https://www.vikospeier.com/">Viko Speier ↗</a></section><section class="section"><h2>{e(tr("Ügyfelek és együttműködő partnerek || Clients and collaborating partners || Kunden und Kooperationspartner")[l])}</h2><p class="lead">{e(tr("A következő logók a jelenlegi HIPStudio partneroldalán nyilvánosan szereplő ügyfél- és partnerreferenciák. A megjelenítés nem jelent aktuális megbízást, ajánlást vagy eredményígéretet. || The following marks are client and partner references publicly shown on HIPStudio’s current partner page. Their presence does not imply a current engagement, endorsement or promised outcome. || Die folgenden Logos sind Kunden- und Partnerreferenzen, die auf der aktuellen HIPStudio-Partnerseite öffentlich gezeigt werden. Ihre Darstellung bedeutet weder einen aktuellen Auftrag noch eine Empfehlung oder Ergebniszusage.")[l])}</p>{client_grid()}</section>'
 render('partners',l,ui('partners',l),partner_intro,content+cta(l),page_type='AboutPage')
 content=heading(ui('legal',l),ui('legalIntro',l),l)+f'<section class="reading"><h2>{e(ui("operator",l))}</h2><p>Hipstudió Korlátolt Felelősségű Társaság · Hipstudió Kft.</p><dl><dt>{e(ui("registered",l))}</dt><dd>1081 Budapest, Népszínház u. 25. Fe. 2.</dd><dt>{e(ui("registration",l))}</dt><dd>01-09-907275</dd><dt>{e(ui("tax",l))}</dt><dd>14513938-2-42</dd><dt>{e(ui("court",l))}</dt><dd>Fővárosi Törvényszék Cégbírósága</dd></dl><p><a href="https://www.hipstudio.hu/impresszum">{e(ui("legalSource",l))} ↗</a></p><h2>{e(ui("legalReview",l))}</h2><ul>'+''.join(f'<li>{e(t[l])}</li>' for t in LEGAL_ITEMS)+f'</ul><h2>{e(ui("privacyContact",l))}</h2><a href="mailto:info@hipstudio.hu">info@hipstudio.hu</a><p><a href="https://www.naih.hu/">NAIH</a> · <a href="https://www.dsb.gv.at/">Datenschutzbehörde</a> · <a href="https://eur-lex.europa.eu/eli/reg/2016/679/oj">GDPR</a></p><h2>{e(ui("aiTrust",l))}</h2><p>{e(ui("aiBody",l))}</p></section>'
 render('legal',l,ui('legal',l),ui('legalIntro',l),content)
 cookie=tr('Ez a változat nem használ analitikát, marketingcookie-t vagy automatikusan betöltődő külső videót. A képek és a betűkészlet nem kérnek le külső szolgáltatást. A külső referenciaoldalak és a levelezőprogram csak a megfelelő hivatkozás használatakor nyílnak meg. A tárhely technikai adatkezelését az impresszum jogi felülvizsgálata rendezi. || This version uses no analytics, marketing cookies or automatically loaded external videos. Images and fonts do not contact external providers. External references and your email application open only when you use their links. Hosting-related technical data processing requires the legal review described in the notice. || Diese Version verwendet keine Analyse- oder Marketingcookies und lädt keine externen Videos automatisch. Bilder und Schriften kontaktieren keine externen Anbieter. Externe Referenzen und Ihr E-Mail-Programm öffnen sich erst beim Aufruf der Links. Die technische Datenverarbeitung des Hostings wird im Rahmen der rechtlichen Prüfung geklärt.')[l]
 render('cookies',l,ui('cookies',l),ui('cookies',l),heading(ui('cookies',l),ui('cookies',l),l)+f'<section class="reading"><p>{e(cookie)}</p><a href="{href("legal",l)}">{e(ui("legal",l))}</a></section>')
 # Static price tables remain usable without JavaScript.
 content=heading(ui('prices',l),ui('priceNote',l),l)
 for group,label,pkgs in [('banhalmi',tr('Vezetői, brand-, művészi és rendezvénycsomagok || Executive, brand, fine-art and event packages || Executive-, Brand-, Kunst- und Eventpakete')[l],PRICING['packages']),('wix',tr('Stúdiós portré és személyes fotózás || Studio portraits and personal photography || Studioporträts und persönliche Fotografie')[l],PRICING['wixPackages'])]:
  content+=f'<section class="section" id="{group}"><h2>{e(label)}</h2><section class="table-wrap" tabindex="0" aria-label="{e(label)}"><table><caption>{e(label)} · HUF</caption><thead><tr><th scope="col">{e(ui("services",l))}</th><th scope="col">{e(ui("duration",l))}</th><th scope="col">{e(ui("net",l))}</th><th scope="col">{e(ui("vat",l))}</th><th scope="col">{e(ui("gross",l))}</th></tr></thead><tbody>'
  for p in pkgs:
   label=e(p['name'][l])+(' · '+str(p['includedImages'])+' '+e(ui('images',l)) if p.get('includedImages') is not None else '')
   content+=f'<tr><th scope="row">{label}</th><td>{p["durationMinutes"]} {e(ui("minutes",l))}</td>'+''.join(f'<td>{p[f]:,} HUF</td>'.replace(',',' ') for f in ['netHUF','vatHUF','grossHUF'])+'</tr>'
  content+='</tbody></table></section></section>'
 # Gross preservation is disclosed without bringing implementation details into the buyer flow.
 content+=f'<section class="reading"><h2>{e(tr("Egyedi tervezés || Custom planning || Individuelle Planung")[l])}</h2><p>{e(ui("quoteNote",l))}</p><p>{e(tr("Több résztvevő, további retusált képek, utazás és speciális produkció esetén kérjen tételes ajánlatot. || For additional participants, retouched images, travel or specialist production, request an itemised quote. || Für weitere Personen, retuschierte Bilder, Reisen oder besondere Produktion fragen Sie nach einem aufgeschlüsselten Angebot.")[l])}</p></section>'+cta(l)
 render('prices',l,ui('prices',l),ui('priceNote',l),content+calculator(PRICING,l),script=True)

# URL intent mapping. The resulting HTML is a client redirect, never a claimed HTTP301.
old={'reklam-fotozas-budapest':'advertising','fotostudio-budapest':'services','impresszum':'legal','rovidfilm-keszites':'video','muveszi-aktfotozas-budapest':'nude','epulet-fotozas-galeria':'work','partnereink':'partners','referencia-videók':'work','reklamfoto-galeria':'work','muveszi-aktfotozas-galeria':'work','portfolio-fotozas-galeria':'work','portfolio-fotozas-budapest':'portfolio','oneletrajz-cv-fotozas-budapest':'cv','podcast-keszites':'podcast','rendezvenyfotozas':'event','ingatlanfotozas':'property','portrefotozas-galeria':'work','fotozas-arak-idopontfoglalas':'prices','rendezvenyfotozas-budapest':'event','kapcsolat':'contact'}
booking={'művészi-aktfotózás':'nude','portfólió-és-divatfotózás':'portfolio','glamour-boudoir-fotózás':'boudoir','cv-önéletrajz-fotózás':'cv','személyes-egyeztetés-a-stúdióban':'contact','személyes-egyeztetés-online':'contact','üzleti-kreatív-portréfotózás':'business','mini-portfólió-társkereső-fotózás-1':'dating'}
for slug,key in booking.items():
 for prefix in ['service-page/','booking-calendar/']:old[prefix+slug]=key
for slug,key in {'mini-portfólió-társkereső-fotózás-1':'dating','portfólió-fotózás-művészi-aktfotózás-1':'portfolio','személyes-egyeztetés-1':'contact'}.items():old['bookings-checkout/'+slug]=key
old['']='home';mapping=[]
anchors={'epulet-fotozas-galeria':'property','reklamfoto-galeria':'commercial','muveszi-aktfotozas-galeria':'art','portfolio-fotozas-galeria':'portfolio','portrefotozas-galeria':'portrait','referencia-videók':'films'}
for old_path,key in old.items():
 target=href(key,'hu')+('#'+anchors[old_path] if old_path in anchors else '')
 out=D/old_path/'index.html';out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(f'<!DOCTYPE html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={e(target)}"><link rel="canonical" href="{e(absolute(key,"hu"))}"><title>HIPStudio · Az oldal új címe</title></head><body><main><h1>Az oldal új címre költözött</h1><a href="{e(target)}">{e(ui(key,"hu") if key in UI else SERVICE[key]["name"]["hu"])}</a></main></body></html>')
 mapping.append({'old':'https://www.hipstudio.hu/'+quote(old_path,safe='/'),'new':absolute(key,'hu')+('#'+anchors[old_path] if old_path in anchors else ''),'implementation':'static HTML refresh and fallback link','plannedHttpStatus':301,'actualPagesStatus':200,'reason':'Preserve service intent; booking function removed' if 'booking' in old_path or 'service-page' in old_path else 'Preserve content intent'})
(R/'audit/url-mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2))
# GitHub Pages serves this actual file for missing URLs. Language links lead to real homes.
(D/'404.html').write_text('<!DOCTYPE html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>404 · HIPStudio</title><link rel="stylesheet" href="'+asset(CSS)+'"></head><body><main class="page-heading"><p class="eyebrow">HIPStudio · 404</p><h1>'+e(ui('notFound','hu'))+'</h1>'+''.join(f'<section lang="{l}"><p>{e(ui("notFoundText",l))}</p><a class="button" href="{href("home",l)}">{e(ui("back",l))}</a></section>' for l in LANGS)+'</main></body></html>')
(D/'.nojekyll').write_text('')
(D/'robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+BASE+'/sitemap.xml\n' if MODE=='production' else 'Disallow: /\n'))
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(p['url'])+'</loc></url>' for p in PAGES if MODE=='production')+'</urlset>\n'
(D/'sitemap.xml').write_text(xml)
(D/'pricing.json').write_text(json.dumps(PRICING,ensure_ascii=False,indent=2))
public_provenance=json.loads(json.dumps(PROVENANCE))
for source in public_provenance['sources'].values():
 source_path=R/source['path']
 if source_path.is_file():source['sha256']=hashlib.sha256(source_path.read_bytes()).hexdigest()
(D/'provenance.json').write_text(json.dumps(public_provenance,ensure_ascii=False,indent=2))
(D/'privacy-config.json').write_text(json.dumps(PRIVACY_CONFIG,ensure_ascii=False,indent=2))
entity={'@context':'https://schema.org','@graph':[
 {'@type':['Organization','ProfessionalService'],'@id':BASE+'/#organization','name':'HIPStudio','legalName':'Hipstudió Korlátolt Felelősségű Társaság','url':BASE+'/','foundingDate':'2006-02-27','founder':{'@id':BASE+'/#norbert-banhalmi'},'sameAs':['https://www.wikidata.org/wiki/Q138482177']},
 {'@type':'Person','@id':BASE+'/#norbert-banhalmi','name':'Bánhalmi Norbert','sameAs':['https://www.wikidata.org/wiki/Q56391118']},
 {'@type':'Person','@id':BASE+'/#viko-speier','name':'Speier Vikó','alternateName':'Speier Viktória'}]}
(D/'entity.json').write_text(json.dumps(entity,ensure_ascii=False,indent=2))
llms=['# HIPStudio','','Verified entity summary:','- Creative communications agency in Budapest, founded on 2006-02-27.','- Founder: Bánhalmi Norbert (Wikidata Q56391118).','- Photography, film and podcast capabilities are organised around business solutions.','- Named professional partners: Bánhalmi Norbert and Speier Vikó. Specific project roles and contracting relationships are defined per agreement.','','Primary machine-readable records:','- Entity graph: '+BASE+'/entity.json','- Claim provenance: '+BASE+'/provenance.json','- Pricing data: '+BASE+'/pricing.json','- Privacy integration state: '+BASE+'/privacy-config.json','','Solution pages:']
llms+=['- '+solution['name']['en']+': '+absolute('solution:'+solution['key'],'en') for solution in SOLUTIONS]
llms+=['','People pages:']+['- '+person['name']+': '+absolute('person:'+person['key'],'en') for person in PEOPLE]
llms+=['','Editorial limits:','- No client outcome, testimonial, certification, performance claim or current relationship is inferred.','- Historical logo display is not evidence of a current engagement or endorsement.','- No substitute AI-generated portfolio imagery is used.','- Case studies remain unpublished until their claims and usage rights are approved item by item.','']
(D/'llms.txt').write_text('\n'.join(llms))
(R/'audit/build.json').write_text(json.dumps({'mode':MODE,'base':BASE,'pages':PAGES,'redirects':len(mapping),'images':len(IMAGES),'solutions':len(SOLUTIONS),'people':len(PEOPLE),'approvedCaseStudies':sum(item.get('status')=='approved' for item in CASE_STUDIES['items']),'css':CSS},ensure_ascii=False,indent=2))
print(f'Built {len(PAGES)} localized pages, {len(mapping)} legacy aliases, 404; mode={MODE}; base={BASE}')
