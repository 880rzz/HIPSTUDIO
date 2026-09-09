# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
M=json.loads((R/'content/business-provider-matrix.json').read_text())
INV=json.loads((R/'content/service-inventory.json').read_text())

assert M['version']=='business-provider-matrix-v1'
assert M['status']=='review_only'
assert M['productionDirectProviderClaimsAllowed'] is False
assert M['productionGate']['currentVerifiedDirectCount']==0

services=M['services']
assert len(services)==16
keys=[x['serviceKey'] for x in services]
assert len(keys)==len(set(keys))

# Inventory and provider matrix must cover the exact same Business service keys.
business=INV['pillars']['business']
inv_keys=[]
for family in business['families'].values():
    inv_keys.extend(x['key'] for x in family['services'])
assert set(keys)==set(inv_keys),(set(keys)-set(inv_keys),set(inv_keys)-set(keys))

allowed_delivery=set(M['deliveryModes'])
allowed_wording=set(M['publicWordingClasses'])
for item in services:
    assert item['deliveryMode'] in allowed_delivery
    assert item['publicWordingClass'] in allowed_wording
    assert item['contractingParty']
    assert item['professionalPerformer']
    assert item['requiredEvidence']
    if not item['productionDirectProviderAllowed']:
        assert item['publicWordingClass']!='verified_direct'
    if item['publicWordingClass']=='verified_direct':
        assert item['productionDirectProviderAllowed'] is True
        assert item['deliveryMode']=='verified_direct'

sensitive={'accounting-coordination','payroll-support','fractional-cfo-readiness','grant-support'}
for key in sensitive:
    item=next(x for x in services if x['serviceKey']==key)
    assert item['productionDirectProviderAllowed'] is False
    assert item['publicWordingClass'] in {'support_coordination','strategic_direction'}

acct=next(x for x in services if x['serviceKey']=='accounting-coordination')
assert acct['regulatedScope'] is True
assert acct['deliveryMode']=='coordinated_support'
payroll=next(x for x in services if x['serviceKey']=='payroll-support')
assert payroll['regulatedScope'] is True

# Protect against accidental direct-provider marketing claims in governed content.
for path in ['content/platform.json','content/platform-solutions.json','content/commercial-content.json','content/solution-depth.json']:
    raw=(R/path).read_text().lower()
    for forbidden in ['mi könyveljük','we do your accounting','wir übernehmen ihre buchhaltung','garantált pályázati','guaranteed grant funding']:
        assert forbidden not in raw,(path,forbidden)

print('Business provider responsibility matrix tests passed')
