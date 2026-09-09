# coding: utf-8
from pathlib import Path
from html import escape
import json, os

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'
BASE=os.environ.get('PLATFORM_URL','https://www.hipstudio.hu').rstrip('/')
MODE=os.environ.get('BUILD_MODE','review')
P=json.loads((R/'content/privacy-governance.json').read_text(encoding='utf-8'))
ROUTES=P['publication']['routes']
QUOTE={'hu':'/hu/ajanlatkeres/','en':'/en/request-a-quote/','de':'/de/angebot-anfragen/'}

COPY={
 'hu':{
  'title':'Adatkezelési tájékoztató','lead':'Így kezeljük a személyes adatokat kapcsolatfelvétel és ajánlatkérés során.','controller':'Adatkezelő','contact':'Kapcsolattartó','purpose':'Az adatkezelés célja és jogalapja','data':'Kezelt adatok','processors':'Adatfeldolgozók és szolgáltatók','retention':'Megőrzési idő','decision':'Automatizált döntéshozatal','rights':'Az Ön jogai','transfers':'Nemzetközi adattovábbítás','special':'Különleges személyes adatok','updated':'Utolsó frissítés','back':'Vissza az ajánlatkéréshez','reg':'Cégjegyzékszám','tax':'Adószám','email':'E-mail','phone':'Telefon','required':'Kötelező mezők','optional':'Opcionális mezők','contactSentence':'Németh Tímea kapcsolattartó; az adatkezelő jogi személy a Hipstudió Kft.','quotePrivacy':'Adatkezelési tájékoztató'
 },
 'en':{
  'title':'Privacy notice','lead':'How we process personal data when you contact us or request a quote.','controller':'Data controller','contact':'Contact person','purpose':'Purpose and legal basis','data':'Data processed','processors':'Processors and service providers','retention':'Retention','decision':'Automated decision-making','rights':'Your rights','transfers':'International transfers','special':'Special-category data','updated':'Last updated','back':'Back to quote request','reg':'Company registration number','tax':'Tax number','email':'Email','phone':'Phone','required':'Required fields','optional':'Optional fields','contactSentence':'Németh Tímea is the human contact person; the legal data controller is Hipstudió Kft.','quotePrivacy':'Privacy notice'
 },
 'de':{
  'title':'Datenschutzhinweise','lead':'So verarbeiten wir personenbezogene Daten bei Kontaktaufnahme und Angebotsanfragen.','controller':'Verantwortlicher','contact':'Ansprechperson','purpose':'Zweck und Rechtsgrundlage','data':'Verarbeitete Daten','processors':'Auftragsverarbeiter und Dienstleister','retention':'Speicherdauer','decision':'Automatisierte Entscheidungen','rights':'Ihre Rechte','transfers':'Internationale Übermittlungen','special':'Besondere Kategorien personenbezogener Daten','updated':'Letzte Aktualisierung','back':'Zurück zur Angebotsanfrage','reg':'Handelsregisternummer','tax':'Steuernummer','email':'E-Mail','phone':'Telefon','required':'Pflichtfelder','optional':'Optionale Felder','contactSentence':'Németh Tímea ist die persönliche Ansprechperson; rechtlich Verantwortlicher ist die Hipstudió Kft.','quotePrivacy':'Datenschutzhinweise'
 }
}

def e(v): return escape(str(v),quote=True)
def ul(items): return '<ul>'+''.join(f'<li>{e(x)}</li>' for x in items)+'</ul>'

def text_for(lang):
 q=P['quoteForm']; c=P['controller']; cp=P['contactPerson']; t=COPY[lang]
 purpose={
  'hu':f"{q['purpose']} Elsődleges jogalap: {q['lawfulBasis']['primary']}. Biztonsági és visszaélés-megelőzési célból {q['lawfulBasis']['security']}. Szerződés létrejötte után szükség szerint {q['lawfulBasis']['accountingAfterContract']}.",
  'en':"We process quote-request data to respond, prepare a quote and take pre-contractual steps at your request under GDPR Article 6(1)(b). Proportionate security and abuse-prevention processing may rely on legitimate interests under Article 6(1)(f). After a contract is formed, accounting and tax data may be processed where required by law under Article 6(1)(c).",
  'de':"Wir verarbeiten Angebotsanfragen zur Beantwortung, Angebotserstellung und für vorvertragliche Maßnahmen auf Ihre Anfrage gemäß Art. 6 Abs. 1 lit. b DSGVO. Angemessene Sicherheits- und Missbrauchsprävention kann auf berechtigten Interessen gemäß Art. 6 Abs. 1 lit. f DSGVO beruhen. Nach Vertragsschluss können buchhalterische und steuerliche Daten aufgrund gesetzlicher Pflichten gemäß Art. 6 Abs. 1 lit. c DSGVO verarbeitet werden."
 }[lang]
 retention={
  'hu':f"Szerződéssé nem váló megkeresés: {q['retention']['unsuccessfulInquiry']} Létrejött projekt: {q['retention']['successfulProject']} Biztonsági naplók: {q['retention']['securityLogs']}",
  'en':"Inquiries that do not become a contract are deleted or anonymised 12 months after the last meaningful contact. Contract/project data is kept for the relationship and then for the period required by applicable Hungarian accounting, tax, limitation and legal rules. Security logs are generally kept for no more than 90 days unless needed for incident investigation or legal claims.",
  'de':"Anfragen ohne Vertragsabschluss werden grundsätzlich 12 Monate nach dem letzten wesentlichen Kontakt gelöscht oder anonymisiert. Vertrags- und Projektdaten werden während der Geschäftsbeziehung und anschließend entsprechend den anwendbaren ungarischen Buchhaltungs-, Steuer-, Verjährungs- und Rechtspflichten aufbewahrt. Sicherheitsprotokolle werden grundsätzlich höchstens 90 Tage gespeichert, sofern sie nicht für Vorfalluntersuchungen oder Rechtsansprüche benötigt werden."
 }[lang]
 special={
  'hu':q['specialCategoryPolicy'],
  'en':'The public quote form does not request special-category personal data. Please do not include health data, intimate information, identity-document numbers or similar sensitive information in free-text fields.',
  'de':'Das öffentliche Anfrageformular verlangt keine besonderen Kategorien personenbezogener Daten. Bitte übermitteln Sie in Freitextfeldern keine Gesundheitsdaten, intimen Informationen, Ausweisnummern oder vergleichbar sensible Angaben.'
 }[lang]
 decision={
  'hu':q['automatedDecisionMaking'],
  'en':'We do not use solely automated decision-making or profiling that produces legal or similarly significant effects. Routing is only an operational pre-classification and remains subject to human review.',
  'de':'Wir verwenden keine ausschließlich automatisierte Entscheidungsfindung oder Profilbildung mit rechtlicher oder ähnlich erheblicher Wirkung. Das Routing ist lediglich eine operative Vorzuordnung und wird menschlich geprüft.'
 }[lang]
 rights={
  'hu':'A jogszabályi feltételek szerint kérhet hozzáférést, helyesbítést, törlést, korlátozást és adathordozhatóságot, továbbá tiltakozhat a jogos érdeken alapuló adatkezelés ellen. Joggyakorlás: info@hipstudio.hu.',
  'en':'Subject to the legal conditions, you may request access, rectification, erasure, restriction and data portability, and object to processing based on legitimate interests. Contact: info@hipstudio.hu.',
  'de':'Unter den gesetzlichen Voraussetzungen können Sie Auskunft, Berichtigung, Löschung, Einschränkung und Datenübertragbarkeit verlangen sowie der Verarbeitung auf Grundlage berechtigter Interessen widersprechen. Kontakt: info@hipstudio.hu.'
 }[lang]
 transfer={
  'hu':q['internationalTransfers'],
  'en':'Where a service provider operates globally, the lawful transfer mechanism applicable to the active contract and account configuration is used. The public notice does not claim more than the actual service agreement and configuration support.',
  'de':'Wenn ein Dienstleister global tätig ist, wird der für den aktiven Vertrag und die Kontoeinstellungen geltende rechtmäßige Übermittlungsmechanismus verwendet. Die öffentliche Information behauptet nicht mehr, als der tatsächliche Dienstleistungsvertrag und die Konfiguration belegen.'
 }[lang]
 processors=[f"{x['service']} — {x['purpose']}" for x in q['processors']]
 required=', '.join(q['requiredFields']); optional=', '.join(q['optionalFieldGroups'])
 return f'''<section class="quote-shell"><div class="quote-intro"><p class="eyebrow">HIPStudio</p><h1>{e(t['title'])}</h1><p class="lead">{e(t['lead'])}</p></div><div class="legal prose"><h2>{e(t['controller'])}</h2><p><strong>{e(c['legalName'])}</strong> ({e(c['shortName'])})<br>{e(c['registeredOffice'])}<br>{e(t['reg'])}: {e(c['companyRegistrationNumber'])}<br>{e(t['tax'])}: {e(c['taxNumber'])}<br>{e(t['email'])}: <a href="mailto:{e(c['email'])}">{e(c['email'])}</a><br>{e(t['phone'])}: {e(c['phone'])}</p><h2>{e(t['contact'])}</h2><p><strong>{e(cp['name'])}</strong> — {e(cp['role'])}. {e(t['contactSentence'])}</p><h2>{e(t['purpose'])}</h2><p>{e(purpose)}</p><h2>{e(t['data'])}</h2><p><strong>{e(t['required'])}:</strong> {e(required)}<br><strong>{e(t['optional'])}:</strong> {e(optional)}</p><h2>{e(t['processors'])}</h2>{ul(processors)}<h2>{e(t['retention'])}</h2><p>{e(retention)}</p><h2>{e(t['decision'])}</h2><p>{e(decision)}</p><h2>{e(t['transfers'])}</h2><p>{e(transfer)}</p><h2>{e(t['rights'])}</h2><p>{e(rights)}</p><h2>{e(t['special'])}</h2><p>{e(special)}</p><h2>{e(t['updated'])}</h2><p>2026-09-09</p><p><a class="button" href="{e(QUOTE[lang])}">{e(t['back'])}</a></p></div></section>'''

if not D.exists(): raise SystemExit('dist-platform missing; run build_platform.py first')
manifest=json.loads((D/'platform-build.json').read_text(encoding='utf-8'))
existing={(x['path'],x['lang']) for x in manifest['pages']}
for lang in ['hu','en','de']:
 p=ROUTES[lang]; url=BASE+p; title=COPY[lang]['title']
 alts=''.join(f'<link rel="alternate" hreflang="{x}" href="{e(BASE+ROUTES[x])}">' for x in ['hu','en','de'])+f'<link rel="alternate" hreflang="x-default" href="{e(BASE+ROUTES["hu"])}">'
 html=f'''<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | HIPStudio</title><meta name="description" content="{e(COPY[lang]['lead'])}"><meta name="robots" content="{'noindex,nofollow' if MODE=='review' else 'index,follow'}"><link rel="canonical" href="{e(url)}">{alts}<link rel="stylesheet" href="/assets/platform.css"><link rel="stylesheet" href="/assets/quote-form.css"></head><body><a class="skip" href="#main">Skip</a><header class="header"><a class="brand" href="/{lang}/">HIPStudio</a></header><main id="main">{text_for(lang)}</main><footer class="footer"><strong>HIPStudio</strong><p><a href="mailto:info@hipstudio.hu">info@hipstudio.hu</a></p></footer></body></html>'''
 out=D/p.strip('/')/'index.html'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(html,encoding='utf-8')
 row={'key':'privacy','lang':lang,'path':p,'canonical':url}
 if (p,lang) not in existing: manifest['pages'].append(row)

 # Make the generated quote page visibly link the matching privacy notice.
 quote_file=D/QUOTE[lang].strip('/')/'index.html'
 if quote_file.exists():
  qhtml=quote_file.read_text(encoding='utf-8')
  marker='</section>'
  privacy_link=f'<p class="legal-note"><a href="{e(p)}">{e(COPY[lang]["quotePrivacy"])}</a> · Hipstudió Kft. · Németh Tímea</p>'
  if privacy_link not in qhtml:
   idx=qhtml.find(marker)
   if idx!=-1: qhtml=qhtml[:idx]+privacy_link+qhtml[idx:]
   quote_file.write_text(qhtml,encoding='utf-8')

manifest['privacy']={'version':P['version'],'controller':P['controller']['shortName'],'contactPerson':P['contactPerson']['name'],'routes':ROUTES,'quoteLinked':True}
(D/'platform-build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
if MODE=='production':
 sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(x["canonical"])}</loc></url>' for x in manifest['pages'])+'</urlset>'
 (D/'sitemap.xml').write_text(sitemap,encoding='utf-8')
print('Built localized HIPStudio privacy pages:', len(ROUTES), 'and linked quote pages')
