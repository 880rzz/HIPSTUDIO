# coding: utf-8
from pathlib import Path
import subprocess

R = Path(__file__).resolve().parents[1]
subprocess.run(['npm','run','build:platform'], cwd=R, check=True)

routes = {
    'hu': R/'dist-platform/hu/vallalati-elmenyek/index.html',
    'en': R/'dist-platform/en/corporate-experiences/index.html',
    'de': R/'dist-platform/de/unternehmenserlebnisse/index.html',
}
for lang, path in routes.items():
    html = path.read_text()
    assert 'data-flugos-sponsors="historical"' in html, f'missing Flúgos sponsor block: {lang}'
    assert 'data-partner-references' not in html, f'HIPStudio partner block leaked into Flúgos page: {lang}'
    assert 'wixstatic.com' not in html.lower(), f'Wix hotlink in Flúgos sponsor page: {lang}'
    assert 'parastorage.com' not in html.lower(), f'Parastorage hotlink in Flúgos sponsor page: {lang}'

hu = routes['hu'].read_text()
assert 'Flúgos szponzorok és támogatók' in hu
assert 'HIPStudio partnerei' not in hu
print('Flúgos sponsor terminology and HIPStudio partner separation passed on HU/EN/DE pages')
