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
    assert '2026-09-09' in h
quote={'hu':'/hu/ajanlatkeres/','en':'/en/request-a-quote/','de':'/de/angebot-anfragen/'}
for lang,route in quote.items():
    h=(D/route.strip('/')/'index.html').read_text(encoding='utf-8')
    assert P['publication']['routes'][lang] in h, f'quote page missing privacy link: {lang}'
manifest=json.loads((D/'platform-build.json').read_text(encoding='utf-8'))
assert manifest['privacy']['controller']=='Hipstudió Kft.'
assert manifest['privacy']['contactPerson']=='Németh Tímea'
assert manifest['privacy']['quoteLinked'] is True
print('Generated privacy pages OK: localized notices and quote links verified')
