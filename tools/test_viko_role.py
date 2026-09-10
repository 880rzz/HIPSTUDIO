from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
D = R / 'dist'
people = json.loads((R / 'content/people.json').read_text())
viko = next((p for p in people if p.get('key') == 'speier-viko'), None)
assert viko, 'Speier Viko person record missing'
assert viko['role']['hu'] == 'Független szakmai fotós partner · fotós szolgáltatások kapcsolattartója'
assert viko['role']['en'] == 'Independent professional photography partner · photography-services contact'
assert viko['role']['de'] == 'Unabhängige professionelle Fotografiepartnerin · Ansprechpartnerin für Fotoleistungen'
summary = ' '.join(viko['summary'].values()).lower()
for boundary in ['owner', 'tulajdonos', 'eigentümerin', 'employee', 'munkavállaló', 'arbeitnehmerin', 'corporate officer', 'vezető tisztségviselő', 'organ', 'general representative', 'általános képviselő', 'allgemeine vertreterin']:
    assert boundary in summary, f'Role boundary missing: {boundary}'
contact = viko['contact']['hipstudioHungary']
assert contact == {
    'email': 'hello@vikospeier.com',
    'telephone': '+36304788850',
    'website': 'https://www.vikospeier.com/',
    'areaServed': 'HU'
}
serialized = json.dumps(viko, ensure_ascii=False).lower()
assert 'banhalmi.at' not in serialized, 'BANHALMI Austria contact leaked into HIPStudio Hungary Viko record'
assert '+4367764733262' not in serialized, 'Austrian BANHALMI liaison phone leaked into HIPStudio Hungary Viko record'

# Generated-output contract: source truth must survive the build, not merely exist in JSON.
build = json.loads((R / 'audit/build.json').read_text())
for lang, expected in viko['role'].items():
    person_page = next(p for p in build['pages'] if p['key'] == 'person:speier-viko' and p['lang'] == lang)
    partner_page = next(p for p in build['pages'] if p['key'] == 'partners' and p['lang'] == lang)
    for page in [person_page, partner_page]:
        html = (D / page['path'].strip('/') / 'index.html').read_text()
        assert expected in html, f"{page['path']}: canonical Viko role missing from generated HTML"
        assert 'viko@banhalmi.at' not in html.lower(), f"{page['path']}: BANHALMI Austria email leaked into HIPStudio output"
        assert '+4367764733262' not in html, f"{page['path']}: BANHALMI Austria phone leaked into HIPStudio output"

print('Viko Speier role/contact contract OK: source and generated pages preserve independent photography partner/contact semantics and isolate HIPStudio Hungary from BANHALMI Austria liaison data.')
