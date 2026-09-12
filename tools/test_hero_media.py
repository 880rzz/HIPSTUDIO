# coding: utf-8
from pathlib import Path
import json
import re

R = Path(__file__).resolve().parents[1]
data = json.loads((R / 'content/hero-media.json').read_text())

assert data['videoId'] == 'gnuMDSWR_tg'
assert data['sourceStatus'] == 'USER_CONFIRMED_FIRST_PARTY'
assert data['delivery'] == 'PRIVACY_ENHANCED_CLICK_TO_LOAD'
assert data['embedOrigin'] == 'https://www.youtube-nocookie.com'
assert data['initialThirdPartyRequest'] is False
assert data['wixHotlinkAllowed'] is False
assert data['channelUrl'].startswith('https://www.youtube.com/@wearehipstudio')
assert data['watchUrl'].startswith('https://youtu.be/gnuMDSWR_tg')

# Rendered-artifact privacy guard. The visual implementation may expose the
# privacy-enhanced embed URL only as inert data before activation; an eager
# iframe src would contact YouTube before consent/click and must fail CI.
for dist_name in ('dist-platform', 'dist'):
    dist = R / dist_name
    if not dist.exists():
        continue
    for path in dist.rglob('*.html'):
        html = path.read_text(errors='ignore')
        assert not re.search(
            r'<iframe[^>]+src\s*=\s*["\']https://www\.youtube-nocookie\.com',
            html,
            flags=re.I | re.S,
        ), f'Eager youtube-nocookie iframe src in {path.relative_to(R)}'
        assert 'youtube.com/embed/gnuMDSWR_tg' not in html, (
            f'Non-privacy YouTube embed origin in {path.relative_to(R)}'
        )

print('Hero media contract and rendered privacy guard: OK')
