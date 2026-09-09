# coding: utf-8
from pathlib import Path
from html import escape
from urllib.parse import urlencode
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/solution-depth.json').read_text())
LANGS = ('hu','en','de')
ROOT = {'hu':'megoldasok','en':'solutions','de':'loesungen'}
QUOTE = {'hu':'/hu/ajanlatkeres/','en':'/en/request-a-quote/','de':'/de/angebot-anfragen/'}
UI = {
  'fit': {'hu':'Mikor érdemes erről beszélni?','en':'When is this relevant?','de':'Wann ist das relevant?'},
  'scope': {'hu':'Mit foghat össze a megoldás?','en':'What can the solution bring together?','de':'Was kann die Lösung bündeln?'},
  'process': {'hu':'Hogyan indulunk el?','en':'How do we start?','de':'Wie starten wir?'},
  'guardrail': {'hu':'Felelősségi és állítási keret','en':'Responsibility and claim boundary','de':'Verantwortungs- und Aussagegrenze'},
  'quote': {'hu':'Egyedi ajánlatot kérek','en':'Request a tailored quote','de':'Individuelles Angebot anfragen'}
}

def e(v): return escape(str(v), quote=True)
def page_path(key, lang): return D / lang / ROOT[lang] / key / 'index.html'

def block(key, item, lang):
    scope = ''.join(f'<li>{e(x)}</li>' for x in item['scope'][lang])
    process = ''.join(f'<li><strong>0{i+1}</strong> {e(x)}</li>' for i, x in enumerate(item['process'][lang]))
    q = QUOTE[lang] + '?' + urlencode(item['quote'])
    return f'''<section class="section" data-solution-depth="{e(key)}"><div class="section-head"><p class="eyebrow">{e(UI['fit'][lang])}</p><h2>{e(UI['fit'][lang])}</h2><p>{e(item['fit'][lang])}</p></div><div class="trust"><div><h3>{e(UI['scope'][lang])}</h3><ul class="service-list">{scope}</ul></div><div><h3>{e(UI['process'][lang])}</h3><ol class="service-list">{process}</ol></div></div><div class="note"><strong>{e(UI['guardrail'][lang])}</strong><p>{e(item['guardrail'][lang])}</p></div><p><a class="button" href="{e(q)}">{e(UI['quote'][lang])} →</a></p></section>'''

count = 0
for key, item in DATA['solutions'].items():
    for lang in LANGS:
        p = page_path(key, lang)
        raw = p.read_text()
        marker = '<section class="cta">'
        assert marker in raw, f'missing CTA marker: {p}'
        assert f'data-solution-depth="{key}"' not in raw, f'duplicate enrichment: {p}'
        raw = raw.replace(marker, block(key, item, lang) + marker, 1)
        p.write_text(raw)
        count += 1

manifest_path = D / 'platform-build.json'
manifest = json.loads(manifest_path.read_text())
manifest['solutionDepth'] = {
    'version': DATA['version'],
    'status': DATA['status'],
    'solutions': len(DATA['solutions']),
    'localizedPages': count,
    'publicPricing': False
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print(f'Flagship solution depth applied to {count} localized pages')
