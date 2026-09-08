# coding: utf-8
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
DATA=json.loads((R/'content/domain-migration.json').read_text())

assert DATA['version']=='domain-migration-v1'
assert DATA['status']=='review_only'
assert DATA['activeRedirects'] is False
assert DATA['master']=={'brand':'HIPStudio','origin':'https://www.hipstudio.hu'}
assert len(DATA['entrypoints'])==2
origins={x['sourceOrigin'] for x in DATA['entrypoints']}
assert origins=={'https://www.hellouzlet.hu','https://www.flugos.hu'}
for item in DATA['entrypoints']:
    assert item['redirectStatus']=='planned_not_active'
    assert set(item['target'])=={'hu','en','de'}
    for target in item['target'].values():
        assert target.startswith('https://www.hipstudio.hu/')
flugos=next(x for x in DATA['entrypoints'] if x['sourceOrigin']=='https://www.flugos.hu')
assert 'Historical Flúgos URLs' in flugos['archiveException']
assert len(DATA['releaseGates'])>=5
print('Review-only domain migration map passed')
