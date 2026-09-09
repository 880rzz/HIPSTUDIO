# coding: utf-8
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'content/release-gates.json').read_text(encoding='utf-8'))
blocked=[g for g in D['gates'] if str(g['state']).startswith('blocked_')]
if blocked:
    print('Production activation BLOCKED:')
    for g in blocked:
        print(f"- {g['id']}: {g['state']} — {g['requirement']}")
    raise SystemExit(1)
print('Production activation gates clear.')
