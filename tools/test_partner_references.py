# coding: utf-8
from pathlib import Path
import json, subprocess

R = Path(__file__).resolve().parents[1]
subprocess.run(['npm','run','build:platform'], cwd=R, check=True)
manifest = json.loads((R/'audit/client-logo-manifest.json').read_text())
expected = len(manifest)
assert expected > 0

for lang, slug in {'hu':'rolunk','en':'about','de':'ueber-uns'}.items():
    html = (R/'dist-platform'/lang/slug/'index.html').read_text()
    assert 'data-partner-references' in html, f'missing partner block: {lang}'
    assert html.count('class="partner-logo"') == expected, f'partner logo count mismatch: {lang}'
    assert 'wixstatic.com' not in html.lower(), f'wix hotlink in partner page: {lang}'
    assert 'parastorage.com' not in html.lower(), f'parastorage hotlink in partner page: {lang}'
    assert '/assets/partners.css' in html

for item in manifest:
    built = R/'dist-platform'/'assets'/'logos'/f"{item['id']}.webp"
    assert built.exists(), f'missing built partner logo: {built}'

print(f'Partner references OK: {expected} local logos rendered on HU/EN/DE About pages')
