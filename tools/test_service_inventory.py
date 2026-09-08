#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = json.loads((ROOT / 'content/service-inventory.json').read_text(encoding='utf-8'))
QUOTE = json.loads((ROOT / 'content/quote-request.json').read_text(encoding='utf-8'))

assert INV['version'] == 'unified-service-inventory-v1'
assert INV['status'] == 'review'
assert set(INV['pillars']) == {'business', 'creative', 'experiences'}

quote_keys = {
    service['key']
    for pillar in QUOTE['pillars']
    for service in pillar['services']
}

seen = set()
counts = {}
statuses = {}
for pillar_key, pillar in INV['pillars'].items():
    count = 0
    for family_key, family in pillar['families'].items():
        assert family['label_hu'].strip(), (pillar_key, family_key)
        assert family['services'], (pillar_key, family_key)
        for service in family['services']:
            key = service['key']
            assert key not in seen, f'duplicate service key: {key}'
            seen.add(key)
            count += 1
            assert service['label_hu'].strip(), key
            status = service['status']
            assert status in {'verified_current', 'approved_extension', 'strategic_gated', 'archive_only'}, (key, status)
            statuses[status] = statuses.get(status, 0) + 1
            if service.get('archive_only'):
                assert status == 'archive_only', key
                assert 'quote_request_key' not in service, key
            else:
                qkey = service.get('quote_request_key')
                assert qkey, f'missing quote_request_key: {key}'
                assert qkey in quote_keys, f'unknown quote_request_key {qkey} for {key}'
    counts[pillar_key] = count

# Coverage floors prevent silent loss while detailed migration is being built.
assert counts['business'] >= 16, counts
assert counts['creative'] >= 30, counts
assert counts['experiences'] >= 8, counts
assert statuses.get('verified_current', 0) >= 25, statuses
assert statuses.get('strategic_gated', 0) >= 10, statuses
assert statuses.get('archive_only', 0) >= 2, statuses

# Public quote routing must continue to expose at least one route for all non-archive services.
missing = []
for pillar in INV['pillars'].values():
    for family in pillar['families'].values():
        for service in family['services']:
            if not service.get('archive_only') and service['quote_request_key'] not in quote_keys:
                missing.append(service['key'])
assert not missing, missing

print(json.dumps({'services': len(seen), 'byPillar': counts, 'byStatus': statuses}, ensure_ascii=False))
