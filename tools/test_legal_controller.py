# coding: utf-8
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'content/legal-controller.json').read_text())
assert D['version']=='legal-controller-v1'
assert D['status']=='review'
assert D['effectiveTarget']['controllerName']=='Németh Tímea'
assert D['effectiveTarget']['publicContact']['email']=='info@hipstudio.hu'
assert D['effectiveTarget']['publicContact']['phone']=='+36 30 221 5506'
assert D['currentPublicNotice']['controllerName']=='Hipstudió Korlátolt Felelősségű Társaság'
assert D['currentPublicNotice']['companyRegistrationNumber']=='01-09-907275'
assert D['currentPublicNotice']['taxNumber']=='14513938-2-42'
assert D['publicationState']=='blocked_notice_mismatch'
assert 'must not assign Hipstudió Kft. company identifiers to Németh Tímea' in D['publicationRequirement']
print('Legal controller governance OK: target approved; public notice alignment still required')
