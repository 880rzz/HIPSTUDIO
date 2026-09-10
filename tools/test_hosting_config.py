# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
V=json.loads((R/'vercel.json').read_text(encoding='utf-8'))
assert V['outputDirectory']=='dist-platform'
assert V['buildCommand']=='python3 tools/assert_vercel_build.py && npm run build:platform'
assert (R/'tools/assert_vercel_build.py').exists()
guard=(R/'tools/assert_vercel_build.py').read_text(encoding='utf-8')
assert "mode != 'production'" in guard
assert "startswith('blocked_')" in guard
headers={h['key']:h['value'] for rule in V['headers'] for h in rule['headers']}
for key in ['X-Content-Type-Options','Referrer-Policy','X-Frame-Options','Permissions-Policy']:
    assert key in headers

for rel in ['tools/build_platform_services.py','tools/build_quote_request.py','tools/remove_public_pricing.py']:
    text=(R/rel).read_text(encoding='utf-8')
    assert 'https://www.hellouzlet.hu' not in text, rel
    assert 'https://www.hipstudio.hu' in text, rel

P=json.loads((R/'content/privacy-governance.json').read_text(encoding='utf-8'))
assert P['domainArchitecture']['hipstudio']['hosting']=='vercel'
assert P['domainArchitecture']['hipstudio']['separateVercelProject'] is True
assert P['domainArchitecture']['flugos']['hosting']=='vercel'
assert P['domainArchitecture']['flugos']['separateVercelProject'] is True
assert P['domainArchitecture']['flugos']['separateContentPlatform'] is False

print('Hosting config OK: HIPStudio defaults clean; Vercel production gated; separate projects governed')
