# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'
DATA=json.loads((R/'content/platform.json').read_text())
MANIFEST=json.loads((D/'platform-build.json').read_text())

assert DATA['workingMasterBrand']=='HIPStudio'
assert DATA['masterDomain']=='https://www.hipstudio.hu'
assert DATA['masterBrandApprovalRequired'] is False
assert DATA['heritage']['founded']=='2006-02-27'
assert DATA['heritage']['yearsIn2026']==20
assert '20 év' in DATA['heritage']['headline']['hu']
assert 'Egy HIPStudio. Három szakmai pillér.' in DATA['integrationStory']['title']['hu']
assert DATA['pillars'][0]['brand']=='HIPStudio Business'
assert DATA['pillars'][1]['brand']=='HIPStudio Creative'
assert DATA['pillars'][2]['brand']=='Flúgos by HIPStudio'

assert MANIFEST['masterBrand']=='HIPStudio'
assert MANIFEST['base']=='https://www.hipstudio.hu'
assert MANIFEST['masterDomain']=='https://www.hipstudio.hu'
for page in MANIFEST['pages']:
    assert page['canonical'].startswith('https://www.hipstudio.hu/'), page['canonical']
    html=(D/page['path'].strip('/')/'index.html').read_text()
    assert '<meta property="og:site_name" content="HelloÜzlet">' not in html
    assert '<title>HelloÜzlet |' not in html

hu=(D/'hu/index.html').read_text()
assert '20 év tapasztalat' in hu
assert 'Egy HIPStudio. Három szakmai pillér.' in hu
assert 'HIPStudio Business' in hu
assert 'HIPStudio Creative' in hu
assert 'Flúgos by HIPStudio' in hu
assert '2006-02-27' in hu

print('HIPStudio master-brand regression gate passed')
