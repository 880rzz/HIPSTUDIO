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
for forbidden in ['owner', 'tulajdonos', 'eigentümerin', 'employee', 'munkavállaló', 'arbeitnehmerin', 'corporate officer', 'vezető tisztségviselő', 'organ', 'general representative', 'általános képviselő', 'allgemeine vertreterin']:
    assert forbidden in summary, f'Role boundary missing: {forbidden}'
print('Viko Speier role contract OK: independent photography partner/contact; ownership, employment and officer/general-representative boundaries explicit.')
