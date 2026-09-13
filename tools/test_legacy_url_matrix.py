# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
DATA=json.loads((R/'content/legacy-url-matrix.json').read_text())

assert DATA['version']=='legacy-url-matrix-v3'
assert DATA['status']=='review_only'
assert DATA['activeRedirects'] is False
assert DATA['masterOrigin']=='https://www.hipstudio.hu'
assert set(DATA['inventoryStatus'])=={'https://www.hipstudio.hu','https://www.hellouzlet.hu','https://www.flugos.hu'}

hip=DATA['inventoryStatus']['https://www.hipstudio.hu']
assert hip['complete'] is True
assert hip['mode']=='current_sitemap_and_gsc_verified'
assert hip['verified']=='2026-09-13'
assert hip['sitemapUrl']=='https://www.hipstudio.hu/sitemap.xml'
assert hip['sitemapUrlCount']==29
assert hip['gscSettledThrough']=='2026-09-10'

hello=DATA['inventoryStatus']['https://www.hellouzlet.hu']
flugos=DATA['inventoryStatus']['https://www.flugos.hu']
assert hello['complete'] is True
assert hello['mode']=='retired_source_unavailable'
assert 'owner confirmed' in hello['reason'].lower()
assert flugos['complete'] is False
assert flugos['mode']=='partial_verified_inventory'

allowed=set(DATA['decisionClasses'])
assert allowed=={'planned_301','archive_preserve','preserve_until_archive_mirrored','candidate_410_after_review','needs_inventory'}
entries=DATA['entries']
assert len(entries)>=36
sources=[x['source'] for x in entries]
assert len(sources)==len(set(sources))

current_hipstudio_sources={
 'https://www.hipstudio.hu/',
 'https://www.hipstudio.hu/muveszi-aktfotozas-budapest',
 'https://www.hipstudio.hu/muveszi-aktfotozas-galeria',
 'https://www.hipstudio.hu/fotozas-arak-idopontfoglalas',
 'https://www.hipstudio.hu/rendezvenyfotozas-budapest',
 'https://www.hipstudio.hu/oneletrajz-cv-fotozas-budapest',
 'https://www.hipstudio.hu/portfolio-fotozas-budapest',
 'https://www.hipstudio.hu/kapcsolat',
 'https://www.hipstudio.hu/service-page/portfólió-és-divatfotózás',
 'https://www.hipstudio.hu/service-page/cv-önéletrajz-fotózás',
 'https://www.hipstudio.hu/service-page/mini-portfólió-társkereső-fotózás-1',
 'https://www.hipstudio.hu/service-page/személyes-egyeztetés-a-stúdióban',
 'https://www.hipstudio.hu/service-page/művészi-aktfotózás',
 'https://www.hipstudio.hu/service-page/glamour-boudoir-fotózás',
 'https://www.hipstudio.hu/service-page/személyes-egyeztetés-online',
 'https://www.hipstudio.hu/service-page/üzleti-kreatív-portréfotózás',
 'https://www.hipstudio.hu/rendezvenyfotozas',
 'https://www.hipstudio.hu/referencia-videók',
 'https://www.hipstudio.hu/reklam-fotozas-budapest',
 'https://www.hipstudio.hu/ingatlanfotozas',
 'https://www.hipstudio.hu/portfolio-fotozas-galeria',
 'https://www.hipstudio.hu/impresszum',
 'https://www.hipstudio.hu/rovidfilm-keszites',
 'https://www.hipstudio.hu/reklamfoto-galeria',
 'https://www.hipstudio.hu/podcast-keszites',
 'https://www.hipstudio.hu/fotostudio-budapest',
 'https://www.hipstudio.hu/epulet-fotozas-galeria',
 'https://www.hipstudio.hu/partnereink',
 'https://www.hipstudio.hu/portrefotozas-galeria',
}
assert current_hipstudio_sources <= set(sources)
assert len(current_hipstudio_sources)==29

for item in entries:
    assert item['source'].startswith('https://')
    assert item['decision'] in allowed
    assert item['confidence'] in {'low','medium','high'}
    assert item['activationGate'].strip()
    target=item.get('target')
    if target:
        assert target.startswith('https://www.hipstudio.hu/'), target
        assert target != item['source'], item
    if item['decision']=='planned_301':
        assert target, item
    if item['decision']=='candidate_410_after_review':
        assert 'review' in item['activationGate'].lower() or 'confirm' in item['activationGate'].lower()

by_source={item['source']:item for item in entries}
assert by_source['https://www.hipstudio.hu/']['target']=='https://www.hipstudio.hu/hu/'
assert by_source['https://www.hipstudio.hu/kapcsolat']['target']=='https://www.hipstudio.hu/hu/kapcsolat/'
assert by_source['https://www.hipstudio.hu/impresszum']['target']=='https://www.hipstudio.hu/hu/adatvedelem/'
assert by_source['https://www.hipstudio.hu/rovidfilm-keszites']['target'].endswith('/hu/szolgaltatasok/hipstudio/video/commercial-brand-film/')
assert by_source['https://www.hipstudio.hu/podcast-keszites']['target'].endswith('/hu/szolgaltatasok/hipstudio/podcast-content/video-podcast/')
assert by_source['https://www.hipstudio.hu/service-page/cv-önéletrajz-fotózás']['target'].endswith('/hu/szolgaltatasok/hipstudio/photo-portrait/cv-photography/')
assert by_source['https://www.hipstudio.hu/service-page/üzleti-kreatív-portréfotózás']['target'].endswith('/hu/szolgaltatasok/hipstudio/photo-portrait/business-portrait/')

final_event_target='https://www.hipstudio.hu/hu/szolgaltatasok/hipstudio/photo-event/event-conference-photography/'
assert by_source['https://www.hipstudio.hu/rendezvenyfotozas']['target']==final_event_target
assert by_source['https://www.hipstudio.hu/rendezvenyfotozas-budapest']['target']==final_event_target

root_hello=by_source['https://www.hellouzlet.hu/']
assert root_hello['decision']=='planned_301'
assert root_hello['sourceType']=='retired_html_entrypoint'
assert root_hello['observed']=='owner_confirmed_site_retired_2026-09-09'
assert root_hello['target']=='https://www.hipstudio.hu/hu/uzleti-mukodes/'
assert 'No full HelloÜzlet export is required' in root_hello['activationGate']

root_flugos=by_source['https://www.flugos.hu/']
assert root_flugos['decision']=='planned_301'
assert root_flugos['target']=='https://www.hipstudio.hu/hu/vallalati-elmenyek/'
heritage=by_source['https://www.flugos.hu/flugos-futam']
assert heritage['decision']=='archive_preserve'
assert heritage['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-heritage/')
pdf_2019=next(x for x in entries if '048f98564e214407aa70b03dc824a35b.pdf' in x['source'])
assert pdf_2019['decision']=='archive_preserve'
assert pdf_2019['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-2019/')

raw=(R/'content/legacy-url-matrix.json').read_text().lower()
for forbidden in ['rewrite rule','return 301','redirect 301','netlify.toml','vercel.json']:
    assert forbidden not in raw
assert 'export or crawl the full hellouzlet' not in raw
print('Legacy URL migration matrix tests passed: current HIPStudio sitemap fully covered; HelloÜzlet retired; Flúgos inventory still gated')
