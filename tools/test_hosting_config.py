# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
assert not (R/'vercel.json').exists(), 'HIPStudio must not carry a root Vercel config'
assert not (R/'tools/assert_vercel_build.py').exists(), 'HIPStudio Vercel build guard must be removed'
assert (R/'.github/workflows/pages-review.yml').exists(), 'GitHub Pages review workflow missing'

for rel in ['tools/build_platform_services.py','tools/build_quote_request.py','tools/remove_public_pricing.py']:
    text=(R/rel).read_text(encoding='utf-8')
    assert 'https://www.hellouzlet.hu' not in text, rel
    assert 'https://www.hipstudio.hu' in text, rel

P=json.loads((R/'content/privacy-governance.json').read_text(encoding='utf-8'))
assert P['domainArchitecture']['hipstudio']['hosting']=='github_pages'
assert P['domainArchitecture']['hipstudio']['repository']=='880rzz/HIPSTUDIO'
assert P['domainArchitecture']['flugos']['hosting']=='vercel'
assert P['domainArchitecture']['flugos']['separateVercelProject'] is True
assert P['domainArchitecture']['flugos']['separateContentPlatform'] is False

print('Hosting config OK: HIPStudio uses GitHub Pages; Flúgos remains separate Vercel infrastructure')
