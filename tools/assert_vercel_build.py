# coding: utf-8
"""Guard the Vercel build path.

Review/preview builds remain available while production is blocked. If BUILD_MODE is
explicitly set to production, all machine-readable release gates must be clear before
the static build can emit indexable/submission-enabled output.
"""
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parents[1]
mode = os.environ.get('BUILD_MODE', 'review').strip().lower()

if mode != 'production':
    print(f'Vercel build gate: {mode or "review"} build allowed; production gates not consumed.')
    raise SystemExit(0)

gates = json.loads((ROOT / 'content/release-gates.json').read_text(encoding='utf-8'))
blocked = [g for g in gates['gates'] if str(g['state']).startswith('blocked_')]
if blocked:
    print('Vercel production build BLOCKED:')
    for gate in blocked:
        print(f"- {gate['id']}: {gate['state']} — {gate['requirement']}")
    raise SystemExit(1)

print('Vercel production build gates clear.')
