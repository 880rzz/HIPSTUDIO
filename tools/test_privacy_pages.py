# coding: utf-8
from pathlib import Path
import json, subprocess
R=Path(__file__).resolve().parents[1]
subprocess.run(['npm','run','build:platform'],cwd=R,check=True)
D=R/'dist-platform'
P=json.loads((R/'content/privacy-governance.json').read_text(encoding='utf-8'))
for lang,route in P['publication']['routes'].items():
    f=D/route.strip('/')/'index.html'
    assert f.exists(), f'missing privacy page: {route}'
    h=f.read_text(encoding='utf-8')
    assert 'Hipstudió Kft.' in h
    assert 'Németh Tímea' in h
    assert 'info@hipstudio.hu' in h
    assert 'Nemzeti Adatvédelmi és Információszabadság Hatóság' in h
    assert '1055 Budapest, Falk Miksa utca 9-11.' in h
    assert 'ugyfelszolgalat@naih.hu' in h
    assert '2026-09-10' in h
quote={'hu':'/hu/ajanlatkeres/','en':'/en/request-a-quote/','de':'/de/angebot-anfragen/'}
for lang,route in quote.items():
    h=(D/route.strip('/')/'index.html').read_text(encoding='utf-8')
    assert P['publication']['routes'][lang] in h, f'quote page missing privacy link: {lang}'
en=(D/'en/privacy/index.html').read_text(encoding='utf-8')
de=(D/'de/datenschutz/index.html').read_text(encoding='utf-8')
assert 'right to lodge a complaint with the supervisory authority' in en
assert 'Recht, Beschwerde bei der Aufsichtsbehörde einzulegen' in de
assert 'owner / managing director / privacy contact' in en
assert 'Eigentümerin / Geschäftsführerin / Datenschutzkontakt' in de
assert 'preferred contact method' in en and 'project summary' in en and 'privacy-notice acknowledgement' in en
assert 'bevorzugter Kontaktweg' in de and 'Projektbeschreibung' in de and 'Bestätigung der Datenschutzhinweise' in de
for raw in ['preferred_contact','project_summary','privacy_acknowledged','pillar_specific_scope']:
    assert raw not in en, f'raw field identifier leaked in EN privacy notice: {raw}'
    assert raw not in de, f'raw field identifier leaked in DE privacy notice: {raw}'
assert 'tulajdonos / ügyvezető / adatvédelmi kapcsolattartó' not in en
assert 'tulajdonos / ügyvezető / adatvédelmi kapcsolattartó' not in de
assert 'publishing and serving the static HIPStudio website from the GitHub repository' in en
assert 'Veröffentlichung und Auslieferung der statischen HIPStudio-Website aus dem GitHub-Repository' in de
assert 'Vercel' not in en
assert 'Vercel' not in de
assert 'ajánlatkérő backend, validáció' not in en
assert 'ajánlatkérő backend, validáció' not in de
quote_js=(D/'assets/quote-form.js').read_text(encoding='utf-8')
for forbidden in ['egészségügyi','health, cultural','gesundheitliche']:
    assert forbidden not in quote_js, f'generated quote form still solicits health data: {forbidden}'
for required in ['Fizikai, akadálymentesítési, kulturális vagy időjárási korlátok','Physical, accessibility, cultural or weather constraints','Physische, Barrierefreiheits-, kulturelle oder wetterbedingte Einschränkungen']:
    assert required in quote_js
manifest=json.loads((D/'platform-build.json').read_text(encoding='utf-8'))
assert manifest['privacy']['controller']=='Hipstudió Kft.'
assert manifest['privacy']['contactPerson']=='Németh Tímea'
assert manifest['privacy']['quoteLinked'] is True
print('Generated privacy pages OK: complaint right, localized roles/fields, GitHub Pages disclosure, quote links and no health-data prompt verified')
