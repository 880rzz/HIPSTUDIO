# coding: utf-8
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
SNAP = json.loads((R / 'audit/gsc-legacy-inventory-2026-09-13.json').read_text(encoding='utf-8'))
MAPPING = json.loads((R / 'audit/url-mapping.json').read_text(encoding='utf-8'))

assert SNAP['property'] == 'sc-domain:hipstudio.hu'
assert SNAP['searchType'] == 'web'
assert SNAP['settledThrough'] == '2026-09-10'

pages = SNAP['pages']
assert pages and len({p['url'] for p in pages}) == len(pages)
assert all(p['url'].startswith('https://www.hipstudio.hu/') for p in pages)

mapping_by_old = {item['old']: item for item in MAPPING}
assert len(mapping_by_old) == len(MAPPING), 'duplicate old URL in audit/url-mapping.json'

root = 'https://www.hipstudio.hu/'
missing = []
invalid = []
for page in pages:
    url = page['url']
    if url == root:
        continue
    item = mapping_by_old.get(url)
    if not item:
        missing.append(url)
        continue
    if item.get('plannedHttpStatus') not in {301, 308}:
        invalid.append((url, 'plannedHttpStatus'))
    target = item.get('new', '')
    if not target.startswith('https://www.hipstudio.hu/'):
        invalid.append((url, 'target'))
    if target == url:
        invalid.append((url, 'self-loop'))

assert not missing, f'GSC-visible legacy URLs missing from migration map: {missing}'
assert not invalid, f'Invalid GSC legacy redirect mappings: {invalid}'

# Active SEO value must never depend on a generic blanket-home redirect.
non_root_targets = [mapping_by_old[p['url']]['new'] for p in pages if p['url'] != root]
assert all(t != root for t in non_root_targets), 'legacy URLs must map to semantically specific destinations'

print(f'GSC legacy redirect coverage passed for {len(pages)-1} visible legacy URLs')
