# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
DATA=json.loads((R/'content/domain-migration.json').read_text())

assert DATA['version']=='domain-migration-v2'
assert DATA['status']=='review_only'
assert DATA['activeRedirects'] is False
assert DATA['master']=={
    'brand':'HIPStudio',
    'origin':'https://www.hipstudio.hu',
    'cutoverScope':'master_domain_only'
}
current=DATA['currentMasterMigration']
assert current['sourceOrigin']=='https://www.hipstudio.hu'
assert current['sourcePlatform']=='wix'
assert current['inventory']=='content/legacy-url-matrix.json'
assert current['inventoryStatus']=='current_sitemap_and_gsc_verified'
assert current['inventoryCount']==29
assert current['redirectStatus']=='planned_not_active'
assert current['activation']=='explicit_domain_cutover_approval_required'

assert len(DATA['entrypoints'])==2
origins={x['sourceOrigin'] for x in DATA['entrypoints']}
assert origins=={'https://www.hellouzlet.hu','https://www.flugos.hu'}
for item in DATA['entrypoints']:
    assert item['redirectStatus']=='planned_not_active'
    assert item['blocksMasterCutover'] is False
    assert set(item['target'])=={'hu','en','de'}
    for target in item['target'].values():
        assert target.startswith('https://www.hipstudio.hu/')

hello=next(x for x in DATA['entrypoints'] if x['sourceOrigin']=='https://www.hellouzlet.hu')
assert hello['inventoryStatus']=='retired_source_unavailable_owner_confirmed'
flugos=next(x for x in DATA['entrypoints'] if x['sourceOrigin']=='https://www.flugos.hu')
assert flugos['inventoryStatus']=='partial_verified_inventory'
assert 'Historical Flúgos URLs' in flugos['archiveException']
assert 'Vercel' in flugos['separateCutoverGate']

master_gates=DATA['masterReleaseGates']
assert len(master_gates)>=7
joined=' '.join(master_gates).lower()
for required in ['sitemap url inventory','semantically equivalent','redirect chain','dns/tls/hosting','rollback','search console']:
    assert required in joined, required
assert 'flugos' not in joined

entry_gates=DATA['entryDomainGates']
assert set(entry_gates)=={'hellouzlet.hu','flugos.hu'}
assert any('full Flúgos Wix page/file URL inventory' in x for x in entry_gates['flugos.hu'])
assert any('Vercel' in x for x in entry_gates['flugos.hu'])

# The governed legacy matrix is the source of truth for master-domain URL coverage.
legacy=json.loads((R/'content/legacy-url-matrix.json').read_text())
hip=legacy['inventoryStatus']['https://www.hipstudio.hu']
assert hip['complete'] is True
assert hip['sitemapUrlCount']==current['inventoryCount']
assert hip['mode']==current['inventoryStatus']
assert legacy['activeRedirects'] is False

print('Review-only domain migration contract passed: hipstudio.hu master cutover is isolated from separate entry-domain activation')
