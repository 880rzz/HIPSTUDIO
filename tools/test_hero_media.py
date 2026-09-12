# coding: utf-8
from pathlib import Path
import json

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

print('Hero media contract: OK')
