from pathlib import Path
import json, re

R = Path(__file__).resolve().parents[1]
model = json.loads((R / 'content/entity-model.json').read_text())
origin = model['canonicalOrigin'].rstrip('/')
company_id = model['company']['@id']
brand_id = model['brand']['@id']
website_id = model['website']['@id']
old_org = origin + '/#organization'
qid = 'https://www.wikidata.org/wiki/Q138482177'

assert model['company']['@type'] == 'Organization'
assert model['brand']['@type'] == 'Brand'
assert model['website']['@type'] == 'WebSite'
assert model['brand']['foundingDate'] == '2006-02-27'
assert 'foundingDate' not in model['company'], 'brand founding date must not be legal-company founding date'
assert qid in model['brand']['sameAs'], 'Q138482177 must identify HIPStudio brand/history node'
assert 'sameAs' not in model['company'] or qid not in model['company'].get('sameAs', []), 'Q138482177 must not identify legal company node'
assert model['website']['publisher']['@id'] == company_id
assert model['website']['about']['@id'] == brand_id

script_re = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.S | re.I)

def walk(value):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from walk(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk(v)

def validate_graph(payload, label):
    nodes = payload.get('@graph', []) if isinstance(payload, dict) else []
    ids = {n.get('@id') for n in nodes if isinstance(n, dict)}
    assert company_id in ids, f'{label}: legal company node missing'
    assert brand_id in ids, f'{label}: HIPStudio brand node missing'
    assert website_id in ids, f'{label}: website node missing'
    assert old_org not in ids, f'{label}: legacy collapsed organization node returned'
    company = next(n for n in nodes if isinstance(n, dict) and n.get('@id') == company_id)
    brand = next(n for n in nodes if isinstance(n, dict) and n.get('@id') == brand_id)
    website = next(n for n in nodes if isinstance(n, dict) and n.get('@id') == website_id)
    assert company.get('@type') == 'Organization', f'{label}: legal company type drift'
    assert company.get('legalName') == 'Hipstudió Korlátolt Felelősségű Társaság', f'{label}: legalName drift'
    assert 'foundingDate' not in company, f'{label}: brand founding date leaked to legal company'
    assert qid not in company.get('sameAs', []), f'{label}: HIPStudio QID leaked to legal company identity'
    assert brand.get('@type') == 'Brand' and brand.get('foundingDate') == '2006-02-27', f'{label}: brand history drift'
    assert qid in brand.get('sameAs', []), f'{label}: brand QID missing'
    assert website.get('publisher', {}).get('@id') == company_id, f'{label}: website publisher must be legal company'
    assert website.get('about', {}).get('@id') == brand_id, f'{label}: website about must be HIPStudio brand'
    for node in walk(payload):
        assert node.get('@id') != old_org, f'{label}: legacy #organization reference returned'

for build_name in ['dist', 'dist-platform']:
    build = R / build_name
    assert build.is_dir(), f'{build_name} missing; run build:all before tests'
    htmls = list(build.rglob('*.html'))
    assert htmls, f'{build_name}: no HTML files'
    inspected = 0
    for html in htmls:
        text = html.read_text()
        for raw in script_re.findall(text):
            payload = json.loads(raw)
            if isinstance(payload, dict) and isinstance(payload.get('@graph'), list):
                validate_graph(payload, f'{build_name}/{html.relative_to(build)}')
                inspected += 1
    assert inspected, f'{build_name}: no graph-bearing HTML inspected'

entity_path = R / 'dist/entity.json'
assert entity_path.exists(), 'dist/entity.json missing'
validate_graph(json.loads(entity_path.read_text()), 'dist/entity.json')

print('HIPStudio entity contract OK: Brand, Hipstudió Kft. and WebSite are distinct; Q138482177/2006 history stays on Brand; publisher stays legal company.')
