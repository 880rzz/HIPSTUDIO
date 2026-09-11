# coding: utf-8
from pathlib import Path
import json
import re
import subprocess

R = Path(__file__).resolve().parents[1]
model = json.loads((R/'content/flugos-sponsors.json').read_text(encoding='utf-8'))
assert model['relationship']['hu'] == 'szponzor / támogató'
assert model['logoPublicationGate']['runtimeHotlinking'] == 'forbidden'
assert model['logoPublicationGate']['allowedAssetOrigin'] == 'repository-local'

named = model.get('namedSponsors', [])
if not named:
    assert model['logoPublicationGate']['status'] == 'blocked_until_source_identification'

subprocess.run(['npm','run','build:platform'], cwd=R, check=True)

routes = {
    'hu': R/'dist-platform/hu/vallalati-elmenyek/index.html',
    'en': R/'dist-platform/en/corporate-experiences/index.html',
    'de': R/'dist-platform/de/unternehmenserlebnisse/index.html',
}
for lang, path in routes.items():
    html = path.read_text(encoding='utf-8')
    assert 'data-flugos-sponsors="historical"' in html, f'missing Flúgos sponsor block: {lang}'
    assert 'data-partner-references' not in html, f'HIPStudio partner block leaked into Flúgos page: {lang}'
    assert 'wixstatic.com' not in html.lower(), f'Wix hotlink in Flúgos sponsor page: {lang}'
    assert 'parastorage.com' not in html.lower(), f'Parastorage hotlink in Flúgos sponsor page: {lang}'
    sponsor_section = re.search(r'<section[^>]+data-flugos-sponsors="historical".*?</section>', html, re.S)
    assert sponsor_section, f'cannot isolate Flúgos sponsor block: {lang}'
    if not named:
        assert '<img ' not in sponsor_section.group(0), f'unidentified sponsor logo published: {lang}'

hu = routes['hu'].read_text(encoding='utf-8')
assert 'Flúgos szponzorok és támogatók' in hu
assert 'HIPStudio partnerei' not in hu
print('Flúgos sponsor terminology, evidence gate and HIPStudio partner separation passed on HU/EN/DE pages')
