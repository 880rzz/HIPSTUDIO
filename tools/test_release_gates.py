# coding: utf-8
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'content/release-gates.json').read_text())
assert D['version']=='production-release-gates-v5'
assert D['status']=='review'
assert D['masterDomain']=='https://www.hipstudio.hu'
g={x['id']:x for x in D['gates']}
required={'code-ci','master-brand','public-pricing','evidence-governance','business-provider','privacy-legal','quote-e2e','legacy-url-inventory','hosting-headers','flugos-domain','dns-cutover','indexing'}
assert set(g)==required
for key in ['code-ci','master-brand','public-pricing','evidence-governance','privacy-legal']:
    assert g[key]['state']=='ready'
assert g['business-provider']['state']=='ready_with_restrictions'
assert 'Hipstudió Kft.' in g['privacy-legal']['requirement']
assert 'Németh Tímea' in g['privacy-legal']['requirement']
assert '12-month' in g['privacy-legal']['requirement']
assert g['legacy-url-inventory']['state']=='blocked_flugos_inventory_only'
assert 'HelloÜzlet is confirmed retired' in g['legacy-url-inventory']['requirement']
assert 'vallalati-elmenyek' in g['legacy-url-inventory']['requirement']
assert g['hosting-headers']['state']=='blocked_repo_domain_connection'
assert '880rzz/HIPSTUDIO' in g['hosting-headers']['requirement']
assert g['flugos-domain']['state']=='blocked_until_master_live'
assert 'do not create a separate Flúgos website' in g['flugos-domain']['requirement']
for key in ['quote-e2e','legacy-url-inventory','hosting-headers','flugos-domain','dns-cutover','indexing']:
    assert g[key]['state'].startswith('blocked_')
assert 'every blocked_* gate is resolved' in D['activationRule']
print('Production release gates OK:', len(g), 'gates; privacy ready, repo-host and Flúgos entry-domain blockers explicit')
