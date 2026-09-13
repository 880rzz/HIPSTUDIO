# coding: utf-8
"""Regression gate for platform media provenance and publication boundaries."""
from pathlib import Path
import json
import re

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
platform = json.loads((R / 'content/platform-media.json').read_text(encoding='utf-8'))
images = {item['id']: item for item in json.loads((R / 'content/images.json').read_text(encoding='utf-8'))}
hero = json.loads((R / 'content/hero-media.json').read_text(encoding='utf-8'))
partner_manifest = json.loads((R / 'audit/client-logo-manifest.json').read_text(encoding='utf-8'))

assert platform['status'] == 'review'
policy = platform['policy']
allowed = set(policy['allowedPublicationRights'])
assert policy['runtimeSources'] == 'LOCAL_ONLY'
assert policy['clientClaimFromImage'] is False

asset_by_id = {asset['id']: asset for asset in platform['assets']}
for asset in platform['assets']:
    assert asset['id'] in images, f"Unknown platform media id: {asset['id']}"
    source = images[asset['id']]
    assert source.get('publicationRights') in allowed, f"Uncleared media: {asset['id']}"
    assert asset.get('publicationRights') == source.get('publicationRights')
    assert asset.get('sourceRegistry') == 'content/images.json'
    assert asset.get('claimBoundary'), f"Missing claim boundary: {asset['id']}"
    assert asset.get('usage'), f"Missing usage scope: {asset['id']}"
    assert asset.get('creditDecision'), f"Missing per-asset credit decision: {asset['id']}"
    assert asset.get('creditDecisionBasis'), f"Missing per-asset credit decision basis: {asset['id']}"
    variants = source.get('variants', {})
    for width in ('480', '960', '1440'):
        assert width in variants, f"Missing responsive variant metadata: {asset['id']} {width}"
        local = R / 'assets' / 'photos' / f"{asset['id']}-{width}.webp"
        assert local.exists(), f"Missing local platform asset: {local}"

# Validate every rendered repository-local platform photo against the governed allowlist.
rendered_photo_ids = set()
rendered_logo_ids = set()
for page in D.rglob('*.html'):
    html = page.read_text(encoding='utf-8')
    rendered_photo_ids.update(re.findall(r'/assets/photos/([a-z0-9-]+)-(?:480|960|1440)\.webp', html))
    rendered_logo_ids.update(re.findall(r'/assets/logos/([a-z0-9-]+)\.webp', html))

undeclared = sorted(rendered_photo_ids - set(asset_by_id))
assert not undeclared, f"Rendered platform photos missing from provenance allowlist: {undeclared}"

# Partner logos are a separately governed media class: every rendered logo must be
# present in the preserved client-logo manifest and must resolve to a local asset.
partner_ids = {item['id'] for item in partner_manifest}
unknown_logos = sorted(rendered_logo_ids - partner_ids)
assert not unknown_logos, f"Rendered partner logos missing from client-logo manifest: {unknown_logos}"
for logo_id in rendered_logo_ids:
    assert (R / 'assets' / 'logos' / f'{logo_id}.webp').exists(), f"Missing local partner logo asset: {logo_id}"

video = platform['heroVideo']
assert video['sourceRegistry'] == 'content/hero-media.json'
assert video['videoId'] == hero['videoId'] == 'gnuMDSWR_tg'
assert video['sourceStatus'] == hero['sourceStatus'] == 'USER_CONFIRMED_FIRST_PARTY'
assert video['delivery'] == hero['delivery'] == 'PRIVACY_ENHANCED_CLICK_TO_LOAD'
assert video['runtimeThirdPartyRequestBeforeUserAction'] is False

print(f'platform media provenance gate: PASS ({len(rendered_photo_ids)} photos, {len(rendered_logo_ids)} partner logos)')
