# coding: utf-8
from pathlib import Path
from urllib.parse import urlsplit
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
home_paths = {'/', '/hu', '/hu/'}
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
        continue
    parsed = urlsplit(target)
    normalized_path = parsed.path.rstrip('/') or '/'
    if target == url:
        invalid.append((url, 'self-loop'))
    if normalized_path in {'/', '/hu'}:
        invalid.append((url, 'blanket-home-target'))

assert not missing, f'GSC-visible legacy URLs missing from migration map: {missing}'
assert not invalid, f'Invalid GSC legacy redirect mappings: {invalid}'

# Active SEO value must never depend on the bare or localized homepage,
# including query/fragment variants of those home routes.
for page in pages:
    if page['url'] == root:
        continue
    target = mapping_by_old[page['url']]['new']
    parsed = urlsplit(target)
    assert (parsed.path.rstrip('/') or '/') not in {'/', '/hu'}, (
        f'legacy URL must map to a semantically specific destination: {page["url"]} -> {target}'
    )

print(f'GSC legacy redirect coverage passed for {len(pages)-1} visible legacy URLs')
