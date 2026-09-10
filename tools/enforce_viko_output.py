from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist'
people = json.loads((R / 'content/people.json').read_text())
viko = next(p for p in people if p['key'] == 'speier-viko')
build = json.loads((R / 'audit/build.json').read_text())

legacy_roles = {
    'hu': '<h2>Speier Vikó</h2><p class="partner-role">Szakmai partner</p>',
    'en': '<h2>Speier Vikó</h2><p class="partner-role">Professional partner</p>',
    'de': '<h2>Speier Vikó</h2><p class="partner-role">Fachpartner</p>',
}

changed = 0
for page in build['pages']:
    if page['key'] != 'partners':
        continue
    path = D / page['path'].strip('/') / 'index.html'
    raw = path.read_text()
    old = legacy_roles[page['lang']]
    new = f'<h2>Speier Vikó</h2><p class="partner-role">{viko["role"][page["lang"]]}</p>'
    if old not in raw:
        raise SystemExit(f'{page["path"]}: expected legacy Viko role marker missing; update generator/source projection deliberately')
    raw = raw.replace(old, new, 1)
    path.write_text(raw)
    changed += 1

if changed != 3:
    raise SystemExit(f'Expected 3 localized partner pages, changed {changed}')
print('Projected canonical Speier Vikó role into 3 localized HIPStudio partner pages.')
