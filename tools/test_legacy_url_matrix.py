# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
DATA=json.loads((R/'content/legacy-url-matrix.json').read_text())

assert DATA['version']=='legacy-url-matrix-v1'
assert DATA['status']=='review_only'
assert DATA['activeRedirects'] is False
assert DATA['masterOrigin']=='https://www.hipstudio.hu'
assert set(DATA['inventoryStatus'])=={'https://www.hellouzlet.hu','https://www.flugos.hu'}
assert DATA['inventoryStatus']['https://www.hellouzlet.hu']['complete'] is False
assert DATA['inventoryStatus']['https://www.flugos.hu']['complete'] is False
allowed=set(DATA['decisionClasses'])
assert allowed=={'planned_301','archive_preserve','preserve_until_archive_mirrored','candidate_410_after_review','needs_inventory'}

entries=DATA['entries']
assert len(entries)>=7
sources=[x['source'] for x in entries]
assert len(sources)==len(set(sources))
assert 'https://www.hellouzlet.hu/' in sources
assert 'https://www.flugos.hu/' in sources
assert 'https://www.flugos.hu/flugos-futam' in sources

for item in entries:
    assert item['source'].startswith('https://')
    assert item['decision'] in allowed
    assert item['confidence'] in {'low','medium','high'}
    assert item['activationGate'].strip()
    target=item.get('target')
    if target:
        assert target.startswith('https://www.hipstudio.hu/'), target
    if item['decision']=='planned_301':
        assert target, item
    if item['decision']=='candidate_410_after_review':
        assert 'review' in item['activationGate'].lower() or 'confirm' in item['activationGate'].lower()

root_hello=next(x for x in entries if x['source']=='https://www.hellouzlet.hu/')
assert root_hello['decision']=='planned_301'
assert root_hello['target']=='https://www.hipstudio.hu/hu/uzleti-mukodes/'

root_flugos=next(x for x in entries if x['source']=='https://www.flugos.hu/')
assert root_flugos['decision']=='planned_301'
assert root_flugos['target']=='https://www.hipstudio.hu/hu/vallalati-elmenyek/'

heritage=next(x for x in entries if x['source']=='https://www.flugos.hu/flugos-futam')
assert heritage['decision']=='archive_preserve'
assert heritage['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-heritage/')

pdf_2019=next(x for x in entries if '048f98564e214407aa70b03dc824a35b.pdf' in x['source'])
assert pdf_2019['decision']=='archive_preserve'
assert pdf_2019['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-2019/')

# A review matrix may describe planned redirects but must not contain server-rule syntax or activation flags.
raw=(R/'content/legacy-url-matrix.json').read_text().lower()
for forbidden in ['rewrite rule','return 301','redirect 301','netlify.toml','vercel.json']:
    assert forbidden not in raw

print('Legacy URL migration matrix tests passed')
