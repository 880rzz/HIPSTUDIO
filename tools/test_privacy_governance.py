# coding: utf-8
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'content/privacy-governance.json').read_text(encoding='utf-8'))
assert P['version']=='hipstudio-privacy-v2'
assert P['status']=='approved_for_quote_flow'
assert P['controller']['shortName']=='Hipstudió Kft.'
assert P['contactPerson']['name']=='Németh Tímea'
assert P['contactPerson']['capacity']=='contact_person_not_individual_controller'
q=P['quoteForm']
assert '6. cikk (1) b)' in q['lawfulBasis']['primary']
assert '12 hónap' in q['retention']['unsuccessfulInquiry']
assert '90 nap' in q['retention']['securityLogs']
services={x['service'] for x in q['processors']}
assert {'Google Apps Script','Google Sheets','Google Workspace / Gmail'} <= services
assert any('GitHub Pages' in x for x in services)
assert P['domainArchitecture']['hipstudio']['repository']=='880rzz/HIPSTUDIO'
assert P['domainArchitecture']['hipstudio']['directDomainConnection'] is True
assert P['domainArchitecture']['flugos']['separateWebsite'] is False
assert P['domainArchitecture']['flugos']['target']=='https://www.hipstudio.hu/hu/vallalati-elmenyek/'
assert P['publication']['quoteFormMustLinkNotice'] is True
print('HIPStudio privacy governance OK: company controller, human contact, retention and processors explicit')
