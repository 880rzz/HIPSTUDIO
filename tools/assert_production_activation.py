# coding: utf-8
from pathlib import Path
from urllib.parse import urlparse
import json
import os

R = Path(__file__).resolve().parents[1]
D = json.loads((R / 'content/release-gates.json').read_text(encoding='utf-8'))
blocked = [g for g in D['gates'] if str(g['state']).startswith('blocked_')]

if not blocked:
    print('Production activation gates clear.')
    raise SystemExit(0)

# Production cutover can only be opened by an explicit owner-approved deploy.
# The override does not mark external gates as resolved; it permits the live
# deployment needed to verify them, while constraining domain and form backend.
if os.environ.get('PRODUCTION_CUTOVER_APPROVED') != '1':
    print('Production activation BLOCKED:')
    for gate in blocked:
        print(f"- {gate['id']}: {gate['state']} — {gate['requirement']}")
    raise SystemExit(1)

platform_url = os.environ.get('PLATFORM_URL', '').strip().rstrip('/')
if platform_url != 'https://www.hipstudio.hu':
    raise SystemExit('Production activation BLOCKED: PLATFORM_URL must be exactly https://www.hipstudio.hu')

endpoint = os.environ.get('QUOTE_FORM_ENDPOINT', '').strip()
parsed = urlparse(endpoint)
if parsed.scheme != 'https' or parsed.hostname != 'script.google.com' or not parsed.path.startswith('/macros/s/') or not parsed.path.endswith('/exec'):
    raise SystemExit('Production activation BLOCKED: QUOTE_FORM_ENDPOINT must be a deployed HTTPS Google Apps Script /macros/s/.../exec endpoint')

if os.environ.get('PLATFORM_PUBLICATION_APPROVED') != '1':
    raise SystemExit('Production activation BLOCKED: PLATFORM_PUBLICATION_APPROVED=1 is required')

print('Owner-approved production verification deploy allowed for https://www.hipstudio.hu.')
print('External gates remain verification obligations after deploy:')
for gate in blocked:
    print(f"- {gate['id']}: {gate['state']}")
