# coding: utf-8
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'content/legal-controller.json').read_text())
assert D['version']=='legal-controller-v3'
assert D['status']=='approved_identity_and_quote_privacy'
assert D['effectiveTarget']['controllerName']=='Hipstudió Korlátolt Felelősségű Társaság'
assert D['effectiveTarget']['shortName']=='Hipstudió Kft.'
assert D['effectiveTarget']['companyRegistrationNumber']=='01-09-907275'
assert D['effectiveTarget']['taxNumber']=='14513938-2-42'
assert D['effectiveTarget']['registeredOffice']=='1081 Budapest, Népszínház u. 25. Fe. 2.'
assert D['effectiveTarget']['registeredOfficeAddress']=={
    'streetAddress':'Népszínház u. 25. Fe. 2.',
    'postalCode':'1081',
    'addressLocality':'Budapest',
    'addressCountry':'HU'
}
assert D['effectiveTarget']['publicContact']['email']=='info@hipstudio.hu'
assert D['effectiveTarget']['publicContact']['studioAddress']=='1111 Budapest, Lágymányosi utca 15.'
assert D['effectiveTarget']['publicContact']['studioPostalAddress']['postalCode']=='1111'
assert D['effectiveTarget']['registeredOfficeAddress'] != D['effectiveTarget']['publicContact']['studioPostalAddress']
assert D['effectiveTarget']['contactPerson']['name']=='Németh Tímea'
assert D['currentPublicNotice']['controllerName']==D['effectiveTarget']['controllerName']
assert D['currentPublicNotice']['companyRegistrationNumber']==D['effectiveTarget']['companyRegistrationNumber']
assert D['publicationState']=='controller_and_quote_privacy_aligned'
assert D['privacyGovernance']=='content/privacy-governance.json'
print('Legal controller governance OK: registered office and public studio are explicitly separated')
