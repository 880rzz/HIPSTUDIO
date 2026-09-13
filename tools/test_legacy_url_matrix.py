# coding: utf-8
from pathlib import Path
from urllib.parse import urlsplit
import json

R=Path(__file__).resolve().parents[1]
DATA=json.loads((R/'content/legacy-url-matrix.json').read_text())
OPS=json.loads((R/'ops/redirects.json').read_text())

assert DATA['version']=='legacy-url-matrix-v3'
assert DATA['status']=='review_only'
assert DATA['activeRedirects'] is False
assert DATA['masterOrigin']=='https://www.hipstudio.hu'
assert OPS['status']=='inactive-plan'
assert OPS['source']=='content/legacy-url-matrix.json'
assert OPS['requirements']['preserveQueryString'] is True
assert OPS['requirements']['avoidChains'] is True
assert OPS['requirements']['rejectBlanketHomeRedirects'] is True
assert OPS['requirements']['requireCanonicalIndexableTargetsBeforeActivation'] is True
assert set(DATA['inventoryStatus'])=={
    'https://www.hipstudio.hu',
    'https://www.hellouzlet.hu',
    'https://www.flugos.hu',
}

hip=DATA['inventoryStatus']['https://www.hipstudio.hu']
hello=DATA['inventoryStatus']['https://www.hellouzlet.hu']
flugos=DATA['inventoryStatus']['https://www.flugos.hu']
assert hip['complete'] is False
assert hip['mode']=='public_verified_partial_inventory'
assert 'sitemap' in hip['reason'].lower() and 'search console' in hip['reason'].lower()
assert hello['complete'] is True
assert hello['mode']=='retired_source_unavailable'
assert 'owner confirmed' in hello['reason'].lower()
assert flugos['complete'] is False
assert flugos['mode']=='partial_verified_inventory'

allowed=set(DATA['decisionClasses'])
assert allowed=={
    'planned_301','preserve_canonical','archive_preserve',
    'preserve_until_archive_mirrored','candidate_410_after_review','needs_inventory'
}
entries=DATA['entries']
assert len(entries)>=18
sources=[x['source'] for x in entries]
assert len(sources)==len(set(sources))

required_hipstudio={
    'https://www.hipstudio.hu/',
    'https://www.hipstudio.hu/kapcsolat',
    'https://www.hipstudio.hu/impresszum',
    'https://www.hipstudio.hu/rovidfilm-keszites',
    'https://www.hipstudio.hu/rendezvenyfotozas-budapest',
    'https://www.hipstudio.hu/reklam-fotozas-budapest',
    'https://www.hipstudio.hu/epulet-fotozas-galeria',
    'https://www.hipstudio.hu/portfolio-fotozas-budapest',
    'https://www.hipstudio.hu/portfolio-fotozas-galeria',
    'https://www.hipstudio.hu/muveszi-aktfotozas-budapest',
    'https://www.hipstudio.hu/fotozas-arak-idopontfoglalas',
}
assert required_hipstudio <= set(sources)
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
        source_path=urlsplit(item['source']).path.rstrip('/') or '/'
        target_path=urlsplit(target).path.rstrip('/') or '/'
        if item['source'].startswith('https://www.hipstudio.hu') and item['decision']=='planned_301':
            assert source_path != target_path, item
            assert target_path not in {'/','/hu'}, f'legacy route must not blanket-redirect to home: {item}'
    if item['decision']=='planned_301':
        assert target, item
    if item['decision']=='candidate_410_after_review':
        assert 'review' in item['activationGate'].lower() or 'confirm' in item['activationGate'].lower()

root=next(x for x in entries if x['source']=='https://www.hipstudio.hu/')
assert root['decision']=='preserve_canonical'
assert root['target']=='https://www.hipstudio.hu/hu/'

expected_targets={
    'https://www.hipstudio.hu/kapcsolat':'/hu/kapcsolat/',
    'https://www.hipstudio.hu/impresszum':'/hu/adatvedelem/',
    'https://www.hipstudio.hu/rovidfilm-keszites':'/hu/szolgaltatasok/hipstudio/video/commercial-brand-film/',
    'https://www.hipstudio.hu/rendezvenyfotozas-budapest':'/hu/szolgaltatasok/hipstudio/photo-event/',
    'https://www.hipstudio.hu/reklam-fotozas-budapest':'/hu/szolgaltatasok/hipstudio/photo-corporate/product-advertising-photography/',
    'https://www.hipstudio.hu/epulet-fotozas-galeria':'/hu/szolgaltatasok/hipstudio/photo-corporate/property-interior-architecture/',
    'https://www.hipstudio.hu/portfolio-fotozas-budapest':'/hu/szolgaltatasok/hipstudio/photo-portrait/portfolio-photography/',
    'https://www.hipstudio.hu/portfolio-fotozas-galeria':'/hu/szolgaltatasok/hipstudio/photo-portrait/portfolio-photography/',
    'https://www.hipstudio.hu/muveszi-aktfotozas-budapest':'/hu/szolgaltatasok/hipstudio/photo-portrait/fine-art-glamour-boudoir/',
    'https://www.hipstudio.hu/fotozas-arak-idopontfoglalas':'/hu/kreativ-tartalom/',
}
for source,path in expected_targets.items():
    item=next(x for x in entries if x['source']==source)
    assert item['decision']=='planned_301'
    assert urlsplit(item['target']).path==path

root_hello=next(x for x in entries if x['source']=='https://www.hellouzlet.hu/')
assert root_hello['decision']=='planned_301'
assert root_hello['sourceType']=='retired_html_entrypoint'
assert root_hello['observed']=='owner_confirmed_site_retired_2026-09-09'
assert root_hello['target']=='https://www.hipstudio.hu/hu/uzleti-mukodes/'
assert 'No full HelloÜzlet export is required' in root_hello['activationGate']

root_flugos=next(x for x in entries if x['source']=='https://www.flugos.hu/')
assert root_flugos['decision']=='planned_301'
assert root_flugos['target']=='https://www.hipstudio.hu/hu/vallalati-elmenyek/'
heritage=next(x for x in entries if x['source']=='https://www.flugos.hu/flugos-futam')
assert heritage['decision']=='archive_preserve'
assert heritage['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-heritage/')
pdf_2019=next(x for x in entries if '048f98564e214407aa70b03dc824a35b.pdf' in x['source'])
assert pdf_2019['decision']=='archive_preserve'
assert pdf_2019['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-2019/')

raw=(R/'content/legacy-url-matrix.json').read_text().lower()
for forbidden in ['rewrite rule','return 301','redirect 301','netlify.toml','vercel.json']:
    assert forbidden not in raw
assert 'export or crawl the full hellouzlet' not in raw
print('Legacy URL migration matrix tests passed; governed matrix is the inactive operational redirect source and current HIPStudio routes remain semantically mapped')
