# coding: utf-8
from pathlib import Path
from html import unescape
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/commercial-content.json').read_text())

ROUTES = {
    'home': {'hu':'hu/index.html','en':'en/index.html','de':'de/index.html'},
    'about': {'hu':'hu/rolunk/index.html','en':'en/about/index.html','de':'de/ueber-uns/index.html'},
    'business': {'hu':'hu/uzleti-mukodes/index.html','en':'en/business-operations/index.html','de':'de/business-operations/index.html'},
    'creative': {'hu':'hu/kreativ-tartalom/index.html','en':'en/creative-content/index.html','de':'de/creative-content/index.html'},
    'experiences': {'hu':'hu/vallalati-elmenyek/index.html','en':'en/corporate-experiences/index.html','de':'de/unternehmenserlebnisse/index.html'}
}

assert DATA['version'] == 'commercial-content-v1'
assert DATA['status'] == 'review'
assert len(DATA['home']['problemCards']) == 3
assert set(DATA['pillars']) == {'business','creative','experiences'}

manifest = json.loads((D / 'platform-build.json').read_text())
commercial = manifest['commercialContent']
assert commercial['version'] == DATA['version']
assert commercial['enrichedPages'] == 15
assert commercial['problemCards'] == 3

for lang in ('hu','en','de'):
    home_raw = (D / ROUTES['home'][lang]).read_text()
    home = unescape(home_raw)
    assert home_raw.count('data-commercial-layer="problem-led-home"') == 1
    assert home_raw.count('data-commercial-layer="partner-benefits"') == 1
    for item in DATA['home']['problemCards']:
        assert item['title'][lang] in home
        assert item['body'][lang] in home
    assert 'hellouzlet.hu' not in home.lower()
    assert '139990' not in home and '84990' not in home and '69990' not in home

    about_raw = (D / ROUTES['about'][lang]).read_text()
    about = unescape(about_raw)
    assert about_raw.count('data-commercial-layer="integration-story"') == 1
    assert DATA['about']['title'][lang] in about
    for section in DATA['about']['sections']:
        assert section['title'][lang] in about

    for pillar in ('business','creative','experiences'):
        page_raw = (D / ROUTES[pillar][lang]).read_text()
        page = unescape(page_raw)
        assert page_raw.count('data-commercial-layer="pillar-value"') == 1
        assert DATA['pillars'][pillar]['problem'][lang] in page
        assert DATA['pillars'][pillar]['outcome'][lang] in page

business_hu = unescape((D / ROUTES['business']['hu']).read_text())
assert 'előre jóváhagyott felelősségi körökön belül' in business_hu
about_hu = unescape((D / ROUTES['about']['hu']).read_text())
assert '2006' in about_hu
assert 'Nem márkát cserélünk' in about_hu

print('Commercial content regression gate passed')
