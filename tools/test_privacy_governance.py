# coding: utf-8
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'content/privacy-governance.json').read_text(encoding='utf-8'))
assert P['version']=='hipstudio-privacy-v7'
assert P['status']=='approved_for_quote_flow'
assert P['controller']['shortName']=='Hipstudió Kft.'
assert P['contactPerson']['name']=='Németh Tímea'
assert P['contactPerson']['capacity']=='contact_person_not_individual_controller'
a=P['supervisoryAuthority']
assert a['shortName']=='NAIH'
assert a['website']=='https://www.naih.hu/'
assert a['verified']=='2026-09-10'
q=P['quoteForm']
assert '6. cikk (1) b)' in q['lawfulBasis']['primary']
assert 'preferred_contact' in q['requiredFields']
assert 'preferred_contact' not in q['optionalFieldGroups']
assert 'egészségügyi állapotra vagy diagnózisra nem' in q['specialCategoryPolicy']
assert '12 hónap' in q['retention']['unsuccessfulInquiry']
assert '90 nap' in q['retention']['securityLogs']
assert set(q['submissionMetadata']['fields'])=={'page_url','form_started_at','submitted_at'}
assert '90 nap' in q['submissionMetadata']['retention']
assert 'panasz benyújtása a felügyeleti hatósághoz' in q['rights']
services={x['service'] for x in q['processors']}
assert {'Google Apps Script','Google Sheets','Google Workspace / Gmail','GitHub Pages / GitHub'} <= services
assert 'Vercel' not in services
assert P['domainArchitecture']['hipstudio']['repository']=='880rzz/HIPSTUDIO'
assert P['domainArchitecture']['hipstudio']['hosting']=='github_pages'
assert P['domainArchitecture']['flugos']['hosting']=='vercel'
assert P['domainArchitecture']['flugos']['separateVercelProject'] is True
assert P['domainArchitecture']['flugos']['separateContentPlatform'] is False
assert P['domainArchitecture']['flugos']['target']=='https://www.hipstudio.hu/hu/vallalati-elmenyek/'
assert P['publication']['quoteFormMustLinkNotice'] is True
print('HIPStudio privacy governance OK: controller, submission metadata, complaint right, GitHub Pages master hosting and Flúgos Vercel boundary explicit')
