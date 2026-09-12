# coding: utf-8
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
DATA = json.loads((R / 'content/platform.json').read_text(encoding='utf-8'))
PAIN = json.loads((R / 'content/pain-points.json').read_text(encoding='utf-8'))
MANIFEST = json.loads((D / 'platform-build.json').read_text(encoding='utf-8'))

# Stable master-brand and heritage invariants.
assert DATA['workingMasterBrand'] == 'HIPStudio'
assert DATA['masterDomain'] == 'https://www.hipstudio.hu'
assert DATA['masterBrandApprovalRequired'] is False
assert DATA['heritage']['founded'] == '2006-02-27'
assert DATA['heritage']['yearsIn2026'] == 20
assert '20 év' in DATA['heritage']['headline']['hu']
assert DATA['pillars'][0]['brand'] == 'HIPStudio Business'
assert DATA['pillars'][1]['brand'] == 'HIPStudio Creative'
assert DATA['pillars'][2]['brand'] == 'Flúgos by HIPStudio'

# The approved public IA is buyer-first. Business / Operations remains qualified
# until provider-responsibility and evidence gates are production-ready.
assert PAIN['status'] == 'review'
verified = {item['key'] for item in PAIN['painPoints'] if item['status'] == 'VERIFIED'}
qualified = {item['key'] for item in PAIN['painPoints'] if item['status'] == 'QUALIFIED'}
assert {'integrated-content', 'adaptive-event-coverage'} <= verified
assert 'management-operations-overload' in qualified

assert MANIFEST['masterBrand'] == 'HIPStudio'
assert MANIFEST['base'] == 'https://www.hipstudio.hu'
assert MANIFEST['masterDomain'] == 'https://www.hipstudio.hu'
for page in MANIFEST['pages']:
    assert page['canonical'].startswith('https://www.hipstudio.hu/'), page['canonical']
    html = (D / page['path'].strip('/') / 'index.html').read_text(encoding='utf-8')
    assert '<meta property="og:site_name" content="HelloÜzlet">' not in html
    assert '<title>HelloÜzlet |' not in html

hu = (D / 'hu/index.html').read_text(encoding='utf-8')
assert '20 év tapasztalat' in hu
assert '2006-02-27' in hu
assert 'class="buyer-needs"' in hu
assert 'data-pain-point="integrated-content"' in hu
assert 'data-pain-point="adaptive-event-coverage"' in hu
assert 'data-pain-point="management-operations-overload"' not in hu
assert 'Nem szolgáltatással kezdünk. A problémával.' in hu

print('HIPStudio master-brand + buyer-first regression gate passed')
