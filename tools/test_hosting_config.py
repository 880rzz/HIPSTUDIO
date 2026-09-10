# coding: utf-8
from pathlib import Path
import json, subprocess

R=Path(__file__).resolve().parents[1]
assert not (R/'vercel.json').exists(), 'HIPStudio must not carry a root Vercel config'
assert not (R/'tools/assert_vercel_build.py').exists(), 'HIPStudio Vercel build guard must be removed'
workflow=R/'.github/workflows/pages-review.yml'
assert workflow.exists(), 'GitHub Pages review workflow missing'
w=workflow.read_text(encoding='utf-8')
assert 'python3 tools/prepare_pages_review.py' in w
assert 'path: dist-pages-review' in w
assert 'path: dist-platform' not in w
assert 'Refuse review deploy when a custom Pages domain is active' in w
assert 'https://api.github.com/repos/${GITHUB_REPOSITORY}/pages' in w
assert "if [ -n \"$cname\" ]" in w
assert 'Review deployment blocked: GitHub Pages custom domain is active' in w
assert 'Refusing review deployment' in w
assert 'uses: actions/configure-pages@v5' in w
assert 'enablement: true' in w

package=(R/'package.json').read_text(encoding='utf-8')
assert '${BUILD_MODE:-review}' in package
assert 'python3 tools/assert_production_activation.py' in package

for rel in ['tools/build_platform_services.py','tools/build_quote_request.py','tools/remove_public_pricing.py']:
    text=(R/rel).read_text(encoding='utf-8')
    assert 'https://www.hellouzlet.hu' not in text, rel
    assert 'https://www.hipstudio.hu' in text, rel

P=json.loads((R/'content/privacy-governance.json').read_text(encoding='utf-8'))
assert P['domainArchitecture']['hipstudio']['hosting']=='github_pages'
assert P['domainArchitecture']['hipstudio']['repository']=='880rzz/HIPSTUDIO'
assert P['domainArchitecture']['flugos']['hosting']=='vercel'
assert P['domainArchitecture']['flugos']['separateVercelProject'] is True
assert P['domainArchitecture']['flugos']['separateContentPlatform'] is False

# Review builds must remain allowed while release gates are intentionally blocked.
subprocess.run(['npm','run','build:platform'],cwd=R,check=True)

# A production build must fail closed while any release gate is blocked.
production_env={'BUILD_MODE':'production','PLATFORM_PUBLICATION_APPROVED':'1','QUOTE_FORM_ENDPOINT':'https://example.invalid/quote'}
import os
env=os.environ.copy(); env.update(production_env)
prod=subprocess.run(['npm','run','build:platform'],cwd=R,env=env,capture_output=True,text=True)
assert prod.returncode != 0, 'production build unexpectedly bypassed blocked release gates'
assert 'Production activation BLOCKED' in (prod.stdout+prod.stderr)

subprocess.run(['python3','tools/prepare_pages_review.py'],cwd=R,check=True)
D=R/'dist-pages-review'
assert D.exists()
root=(D/'index.html')
assert root.exists(), 'Pages review root index missing'
root_html=root.read_text(encoding='utf-8')
assert 'noindex,nofollow' in root_html
assert 'url=/HIPSTUDIO/hu/' in root_html
html=list(D.rglob('*.html'))
assert html
for p in html:
    s=p.read_text(encoding='utf-8')
    assert 'href="/assets/' not in s, p
    assert 'src="/assets/' not in s, p
    assert 'href="/hu/' not in s, p
    assert 'href="/en/' not in s, p
    assert 'href="/de/' not in s, p
home=(D/'hu/index.html').read_text(encoding='utf-8')
assert 'href="/HIPSTUDIO/' in home
assert 'src="/HIPSTUDIO/' in home or 'href="/HIPSTUDIO/assets/' in home

print('Hosting config OK: GitHub Pages review is isolated and production builds fail closed on blocked release gates; Flúgos remains separate Vercel infrastructure')
