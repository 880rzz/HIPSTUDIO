# coding: utf-8
"""Project the canonical HIPStudio entity model into a generated build.

This is a deterministic source-of-truth projection, not a content inference step.
It keeps the transitional builders from collapsing Brand, legal Organization and
WebSite while the two migration build paths still coexist.
"""
from pathlib import Path
import json, re, sys

R = Path(__file__).resolve().parents[1]
MODEL = json.loads((R / 'content/entity-model.json').read_text())
ORIGIN = MODEL['canonicalOrigin'].rstrip('/')
OLD_ORG = ORIGIN + '/#organization'
COMPANY_ID = MODEL['company']['@id']
BRAND_ID = MODEL['brand']['@id']
WEBSITE_ID = MODEL['website']['@id']
NORBET_ID = MODEL['people']['norbert']['@id']
VIKO_ID = MODEL['people']['viko']['@id']

if len(sys.argv) != 2:
    raise SystemExit('usage: project_entity_model.py <build-directory>')
D = R / sys.argv[1]
if not D.is_dir():
    raise SystemExit(f'build directory missing: {D}')

SCRIPT_RE = re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)', re.S | re.I)

def remap_refs(value):
    if isinstance(value, dict):
        return {k: remap_refs(v) for k, v in value.items()}
    if isinstance(value, list):
        return [remap_refs(v) for v in value]
    if value == OLD_ORG:
        return COMPANY_ID
    return value

def project_graph(payload):
    payload = remap_refs(payload)
    graph = payload.get('@graph') if isinstance(payload, dict) else None
    if not isinstance(graph, list):
        return payload

    preserved = []
    website_existing = None
    for node in graph:
        node_id = node.get('@id') if isinstance(node, dict) else None
        if node_id in {OLD_ORG, COMPANY_ID, BRAND_ID, NORBET_ID, VIKO_ID}:
            continue
        if node_id == WEBSITE_ID:
            website_existing = node
            continue
        preserved.append(node)

    website = dict(MODEL['website'])
    if isinstance(website_existing, dict):
        for key, value in website_existing.items():
            if key not in {'@id', '@type', 'name', 'url', 'publisher', 'about'}:
                website[key] = value

    canonical = [
        MODEL['company'],
        MODEL['brand'],
        MODEL['people']['norbert'],
        MODEL['people']['viko'],
        website,
    ]
    payload['@graph'] = canonical + preserved
    return payload

def project_html(path):
    text = path.read_text()
    changed = False
    def repl(match):
        nonlocal changed
        try:
            payload = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        projected = project_graph(payload)
        serialized = json.dumps(projected, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
        changed = changed or serialized != match.group(2)
        return match.group(1) + serialized + match.group(3)
    new = SCRIPT_RE.sub(repl, text)
    if changed:
        path.write_text(new)

for html in D.rglob('*.html'):
    project_html(html)

entity_file = D / 'entity.json'
if entity_file.exists():
    payload = json.loads(entity_file.read_text())
    payload = project_graph(payload)
    entity_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

print(f'Projected canonical HIPStudio company/brand/website separation into {D.name}')
