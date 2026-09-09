# coding: utf-8
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'content/release-gates.json').read_text())
assert D['version']=='production-release-gates-v2'
assert D['status']=='review'
assert D['masterDomain']=='https://www.hipstudio.hu'
g={x['id']:x for x in D['gates']}
required={'code-ci','master-brand','public-pricing','evidence-governance','business-provider','privacy-legal','quote-e2e','legacy-url-inventory','hosting-headers','dns-cutover','indexing'}
assert set(g)==required
for key in ['code-ci','master-brand','public-pricing','evidence-governance']:
    assert g[key]['state']=='ready'
assert g['business-provider']['state']=='ready_with_restrictions'
assert g['privacy-legal']['state']=='blocked_notice_alignment'
assert 'Németh Tímea' in g['privacy-legal']['requirement']
assert g['legacy-url-inventory']['state']=='blocked_flugos_inventory_only'
assert 'HelloÜzlet is confirmed retired' in g['legacy-url-inventory']['requirement']
for key in ['quote-e2e','hosting-headers','dns-cutover','indexing']:
    assert g[key]['state'].startswith('blocked_')
assert 'every blocked_* gate is resolved' in D['activationRule']
print('Production release gates OK:', len(g), 'gates; HelloÜzlet retired, remaining blockers explicit')
