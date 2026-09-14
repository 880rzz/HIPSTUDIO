"""Contract tests for the editorial homepage source and generated artifacts."""
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
source = json.loads((R / 'content/homepage-redesign.json').read_text(encoding='utf-8'))
assert source['status'] == 'review'
assert len(source['painSolutions']) == 3
assert len(source['process']) == 4
assert len(source['situations']) == 2
for lang in ('hu', 'en', 'de'):
    assert source['hero']['title'][lang]
    assert all(item['pain'][lang] and item['solution'][lang] for item in source['painSolutions'])
    home = (R / 'dist' / lang / 'index.html').read_text(encoding='utf-8')
    assert home.count('data-home-pain=') == 3
    assert home.count('class="home-step"') == 4
    assert 'home-cinematic-hero' in home
    assert 'VideoObject' in home and 'ImageObject' in home
    assert 'LocalBusiness' in home and 'BreadcrumbList' in home
    assert 'review-bar' not in home or 'noindex,nofollow' in home
assert (R / 'dist' / 'llms.txt').exists()
assert (R / 'dist' / 'ai.txt').exists()
entity = json.loads((R / 'dist' / 'entity.json').read_text(encoding='utf-8'))
organization = next(node for node in entity['@graph'] if 'Organization' in node.get('@type', []))
assert organization['sameAs'][0] == 'https://www.wikidata.org/wiki/Q138482177'
assert organization['foundingDate'] == '2006-02-27'
assert 'wixstatic.com' not in (R / 'dist' / 'hu' / 'index.html').read_text(encoding='utf-8')
print('Editorial homepage source, schema and AI-content contract passed')
