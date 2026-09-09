# coding: utf-8
from pathlib import Path
from html import unescape
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/evidence-registry.json').read_text())

assert DATA['version'] == 'evidence-registry-v1'
assert DATA['status'] == 'review'
assert DATA['policy']['publishOnlyWithItemEvidence'] is True
assert DATA['policy']['logoIsNotCaseStudy'] is True
assert DATA['caseStudies'] == []
assert all(x['status'] == 'publishable_qualified' for x in DATA['evidence'])
assert any(x['id'] == 'historical-client-logos' and x['status'] == 'not_case_study' for x in DATA['pendingEvidence'])

manifest = json.loads((D / 'platform-build.json').read_text())
layer = manifest['evidenceLayer']
assert layer['version'] == DATA['version']
assert layer['publishableQualified'] == 4
assert layer['caseStudiesPublished'] == 0
assert layer['enrichedPages'] == 9
assert layer['logoIsNotCaseStudy'] is True

paths = [
    'hu/rolunk/index.html', 'en/about/index.html', 'de/ueber-uns/index.html',
    'hu/vallalati-elmenyek/index.html', 'en/corporate-experiences/index.html', 'de/unternehmenserlebnisse/index.html',
    'hu/megoldasok/corporate-experience-design/index.html', 'en/solutions/corporate-experience-design/index.html', 'de/loesungen/corporate-experience-design/index.html'
]
for p in paths:
    html = unescape((D / p).read_text())
    assert html.count('data-evidence-layer="source-backed"') == 1
    assert 'Evidence ID:' in html
    assert 'client-01' not in html
    assert 'testimonial' not in html.lower()

about_hu = unescape((D / 'hu/rolunk/index.html').read_text())
assert '2006. február 27.' in about_hu
assert 'Bánhalmi Norbert' in about_hu

exp_hu = unescape((D / 'hu/vallalati-elmenyek/index.html').read_text())
assert '2009-ben indult' in exp_hu
assert '10 jótékonysági autós futamot' in exp_hu
assert 'több mint 1000 történeti résztvevőt' in exp_hu
assert 'nem jelentenek jelenlegi éves volument' in exp_hu

print('Evidence and case-study publication gate passed')
