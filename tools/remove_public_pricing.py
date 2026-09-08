# coding: utf-8
"""Remove public pricing artefacts from the generated HIPStudio specialist site.

Internal pricing source files remain in the repository for audit/internal planning.
Generated public HTML must not expose package prices or pricing.json.
"""
from pathlib import Path
from html import escape
import json, os, re

R=Path(__file__).resolve().parents[1]
D=R/'dist'
QUOTE_BASE=os.environ.get('QUOTE_REQUEST_BASE_URL','https://www.hellouzlet.hu').rstrip('/')
LANG={
 'hu':{'slug':'arak','quote':'ajanlatkeres','title':'Egyedi ajánlat','h1':'Minden projekt egyedi. Az ajánlat is az.','lead':'Nem teszünk közzé sablonárakat. A projekt célja, terjedelme, helyszíne, résztvevői, felhasználása, határideje és szükséges szakmai kapacitása alapján 24 órán belül egyedi ajánlatot készítünk.','button':'Részletes ajánlatkérés','label':'Egyedi ajánlat','note':'A végleges díjat minden esetben a jóváhagyott projekt-scope és az írásos ajánlat rögzíti.','faqq':'Miért nincs publikus árlista?','faqa':'Minden projekt scope-ja egyedi. A szolgáltatás, cél, helyszín, résztvevők, felhasználás és határidő alapján 24 órán belül egyedi ajánlatot készítünk.'},
 'en':{'slug':'pricing','quote':'request-a-quote','title':'Tailored quote','h1':'Every project is different. So is the quote.','lead':'We do not publish template prices. We prepare a tailored quote within 24 hours based on objective, scope, location, participants, usage, deadline and required specialist capacity.','button':'Detailed quote request','label':'Tailored quote','note':'The final fee is always defined by the approved project scope and written quote.','faqq':'Why is there no public price list?','faqa':'Every project has a different scope. We prepare a tailored quote within 24 hours based on service, objective, location, participants, usage and deadline.'},
 'de':{'slug':'preise','quote':'angebot-anfragen','title':'Individuelles Angebot','h1':'Jedes Projekt ist anders. Das Angebot auch.','lead':'Wir veröffentlichen keine Standardpreise. Auf Basis von Ziel, Umfang, Ort, Beteiligten, Nutzung, Termin und benötigter Fachkapazität erstellen wir innerhalb von 24 Stunden ein individuelles Angebot.','button':'Detaillierte Angebotsanfrage','label':'Individuelles Angebot','note':'Der endgültige Preis wird immer durch den freigegebenen Projektumfang und das schriftliche Angebot festgelegt.','faqq':'Warum gibt es keine öffentliche Preisliste?','faqa':'Jedes Projekt hat einen individuellen Umfang. Auf Basis von Leistung, Ziel, Ort, Beteiligten, Nutzung und Termin erstellen wir innerhalb von 24 Stunden ein individuelles Angebot.'}
}
OLD={
 'hu':{
  'label':'Árak','note':'Tájékoztató HUF-árak. A csomag tartalmát, az elérhetőséget, a felhasználási jogokat és a végleges díjat írásos ajánlat rögzíti.',
  'faqq':'Milyen pénznemben és áfával szerepelnek az árak?','faqa':'Minden összeg HUF-ban szerepel. Az ártáblák külön mutatják a nettó összeget, a 27%-os áfát és a bruttó végösszeget. A végleges szolgáltatást írásos ajánlat rögzíti.'},
 'en':{
  'label':'Pricing','note':'Indicative HUF pricing. Package scope, availability, usage rights and the final fee are recorded in a written quote.',
  'faqq':'What currency and VAT treatment do prices use?','faqa':'All amounts are in HUF. Tables show net, 27% VAT and gross total separately. The final service is documented in a written quote.'},
 'de':{
  'label':'Preise','note':'Unverbindliche HUF-Preise. Paketumfang, Verfügbarkeit, Nutzungsrechte und endgültiger Preis werden im schriftlichen Angebot festgehalten.',
  'faqq':'Welche Währung und Umsatzsteuer gelten?','faqa':'Alle Beträge sind in HUF angegeben. Tabellen zeigen Netto, 27% Umsatzsteuer und Brutto getrennt. Die endgültige Leistung wird schriftlich angeboten.'}
}

def qurl(l): return f'{QUOTE_BASE}/{l}/{LANG[l]["quote"]}/'
def update_graph(raw,l):
 def repl(m):
  try:
   graph=json.loads(m.group(1))
   for n in graph.get('@graph',[]):
    typ=n.get('@type')
    if typ=='WebPage': n['name']=LANG[l]['title'];n['description']=LANG[l]['lead']
    if typ=='BreadcrumbList':
     items=n.get('itemListElement',[])
     if items: items[-1]['name']=LANG[l]['title']
   return '<script type="application/ld+json">'+json.dumps(graph,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'
  except Exception:return m.group(0)
 return re.sub(r'<script type="application/ld\+json">(.*?)</script>',repl,raw,flags=re.S)

def quote_main(l):
 c=LANG[l];url=qurl(l)
 return f'''<main id="main"><section class="page-hero"><p class="eyebrow">24h · {escape(c['label'])}</p><h1>{escape(c['h1'])}</h1><p class="lead">{escape(c['lead'])}</p><div class="hero-actions"><a class="button" href="{escape(url)}">{escape(c['button'])} →</a><a class="button button-secondary" href="mailto:info@hipstudio.hu">info@hipstudio.hu</a></div></section><section class="reading"><h2>{escape(c['label'])}</h2><p>{escape(c['note'])}</p></section></main>'''

for html_path in D.rglob('*.html'):
 raw=html_path.read_text()
 l=html_path.parts[len(D.parts)] if len(html_path.parts)>len(D.parts) else ''
 if l not in LANG: continue
 old=OLD[l];new=LANG[l]
 raw=raw.replace(old['note'],new['note']).replace(old['faqq'],new['faqq']).replace(old['faqa'],new['faqa'])
 route=f'/{l}/{new["slug"]}/'
 raw=re.sub(r'(<a\b[^>]*href="'+re.escape(route)+r'"[^>]*>)(.*?)(</a>)',lambda m:m.group(1)+escape(new['label'])+m.group(3),raw,flags=re.S)
 raw=raw.replace('<h2>'+old['label']+'</h2>','<h2>'+new['label']+'</h2>')
 if html_path == D/l/new['slug']/'index.html':
  raw=re.sub(r'<title>.*?</title>','<title>'+escape(new['title'])+' | HIPStudio</title>',raw,count=1,flags=re.S)
  raw=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+escape(new['lead'],quote=True)+'">',raw,count=1)
  # Generated pages use additional attributes on <main>; match by id rather than exact opening tag.
  raw=re.sub(r'<main\b[^>]*\bid="main"[^>]*>.*?</main>',quote_main(l),raw,count=1,flags=re.S)
  # Defence in depth: remove any stale calculator fragment/script left outside the main replacement.
  raw=re.sub(r'<section\b[^>]*\bdata-calculator\b[^>]*>.*?</section>','',raw,flags=re.S)
  raw=re.sub(r'<script\b[^>]*calculator\.mjs[^>]*></script>','',raw,flags=re.S)
  raw=update_graph(raw,l)
 raw=raw.replace(old['label'],new['label']) if html_path == D/l/new['slug']/'index.html' else raw
 html_path.write_text(raw)

for rel in ['pricing.json','assets/calculator.mjs','assets/pricing-engine.mjs']:
 p=D/rel
 if p.exists(): p.unlink()

print('Public pricing removed; internal pricing sources retained; tailored quote flow active in generated HIPStudio site.')
