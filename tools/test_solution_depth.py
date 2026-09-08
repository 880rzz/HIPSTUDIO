# coding: utf-8
from pathlib import Path
from html import unescape
import json

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'
DATA=json.loads((R/'content/solution-depth.json').read_text())
ROOT={'hu':'megoldasok','en':'solutions','de':'loesungen'}
assert DATA['version']=='solution-depth-v1'
assert DATA['status']=='review'
assert len(DATA['solutions'])==5
manifest=json.loads((D/'platform-build.json').read_text())
meta=manifest['solutionDepth']
assert meta['version']==DATA['version']
assert meta['solutions']==5
assert meta['localizedPages']==15
assert meta['publicPricing'] is False
for key,item in DATA['solutions'].items():
  for lang in ('hu','en','de'):
    p=D/lang/ROOT[lang]/key/'index.html'
    raw=p.read_text(); text=unescape(raw)
    assert raw.count(f'data-solution-depth="{key}"')==1
    assert item['fit'][lang] in text
    assert item['guardrail'][lang] in text
    for x in item['scope'][lang]: assert x in text
    for x in item['process'][lang]: assert x in text
    assert f'pillar={item["quote"]["pillar"]}' in raw
    assert f'service={item["quote"]["service"]}' in raw
    assert '139990' not in raw and '84990' not in raw and '69990' not in raw
    assert 'guaranteed' not in raw.lower() or key=='content-engine'
business=(D/'hu/megoldasok/business-operations-360/index.html').read_text()
assert 'könyvelési, bérszámfejtési, adózási' in unescape(business)
ai=(D/'hu/megoldasok/ai-readiness/index.html').read_text()
assert 'AI nem váltja ki az emberi jóváhagyást' in unescape(ai)
flugos=(D/'hu/megoldasok/corporate-experience-design/index.html').read_text()
assert 'történeti Flúgos futamok' in unescape(flugos)
print('Flagship solution depth regression gate passed')
