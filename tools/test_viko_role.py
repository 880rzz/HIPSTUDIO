from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
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
print('Viko Speier role/contact contract OK: independent photography partner/contact; Hungarian HIPStudio contact isolated from BANHALMI Austria liaison data.')
