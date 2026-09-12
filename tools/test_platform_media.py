# coding: utf-8
"""Regression gate for platform media provenance and publication boundaries."""
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
platform = json.loads((R / 'content/platform-media.json').read_text(encoding='utf-8'))
images = {item['id']: item for item in json.loads((R / 'content/images.json').read_text(encoding='utf-8'))}
hero = json.loads((R / 'content/hero-media.json').read_text(encoding='utf-8'))

assert platform['status'] == 'review'
policy = platform['policy']
allowed = set(policy['allowedPublicationRights'])
assert policy['runtimeSources'] == 'LOCAL_ONLY'
assert policy['clientClaimFromImage'] is False

for asset in platform['assets']:
    assert asset['id'] in images, f"Unknown platform media id: {asset['id']}"
    source = images[asset['id']]
    assert source.get('publicationRights') in allowed, f"Uncleared media: {asset['id']}"
    assert asset.get('publicationRights') == source.get('publicationRights')
    assert asset.get('sourceRegistry') == 'content/images.json'
    assert asset.get('claimBoundary'), f"Missing claim boundary: {asset['id']}"
    assert asset.get('usage'), f"Missing usage scope: {asset['id']}"
    variants = source.get('variants', {})
    for width in ('480', '960', '1440'):
        assert width in variants, f"Missing responsive variant metadata: {asset['id']} {width}"
        local = R / 'assets' / 'photos' / f"{asset['id']}-{width}.webp"
        assert local.exists(), f"Missing local platform asset: {local}"

video = platform['heroVideo']
assert video['sourceRegistry'] == 'content/hero-media.json'
assert video['videoId'] == hero['videoId'] == 'gnuMDSWR_tg'
assert video['sourceStatus'] == hero['sourceStatus'] == 'USER_CONFIRMED_FIRST_PARTY'
assert video['delivery'] == hero['delivery'] == 'PRIVACY_ENHANCED_CLICK_TO_LOAD'
assert video['runtimeThirdPartyRequestBeforeUserAction'] is False

print('platform media provenance gate: PASS')
