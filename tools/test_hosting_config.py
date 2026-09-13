# coding: utf-8
from pathlib import Path
import json, subprocess, os

R=Path(__file__).resolve().parents[1]
assert not (R/'vercel.json').exists(), 'HIPStudio must not carry a root Vercel config'
assert not (R/'tools/assert_vercel_build.py').exists(), 'HIPStudio Vercel build guard must be removed'
workflow=R/'.github/workflows/pages-review.yml'
assert workflow.exists(), 'GitHub Pages review workflow missing'
w=workflow.read_text(encoding='utf-8')
assert 'python3 tools/prepare_pages_review.py' in w
assert 'path: dist-pages-review' in w
assert 'path: dist-platform' not in w
assert 'Allow only the approved temporary review custom domain' in w
assert 'REVIEW_CUSTOM_DOMAIN: hip.vipach.at' in w
assert 'https://api.github.com/repos/${GITHUB_REPOSITORY}/pages' in w
assert 'if [ -n "$cname" ] && [ "$cname" != "$REVIEW_CUSTOM_DOMAIN" ]; then' in w
assert 'Review deployment blocked: unexpected GitHub Pages custom domain is active' in w
assert 'Approved temporary review custom domain is active' in w
assert 'pages_prefix=/' in w
assert 'pages_prefix=/HIPSTUDIO' in w
assert 'PAGES_PREFIX: ${{ steps.pages_domain.outputs.pages_prefix }}' in w
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

subprocess.run(['npm','run','build:platform'],cwd=R,check=True)

production_env={'BUILD_MODE':'production','PLATFORM_PUBLICATION_APPROVED':'1','QUOTE_FORM_ENDPOINT':'https://example.invalid/quote'}
env=os.environ.copy(); env.update(production_env)
prod=subprocess.run(['npm','run','build:platform'],cwd=R,env=env,capture_output=True,text=True)
assert prod.returncode != 0, 'production build unexpectedly bypassed blocked release gates'
assert 'Production activation BLOCKED' in (prod.stdout+prod.stderr)

# Project-path fallback remains valid.
subprocess.run(['python3','tools/prepare_pages_review.py'],cwd=R,check=True)
D=R/'dist-pages-review'
root=(D/'index.html')
assert root.exists(), 'Pages review root index missing'
root_html=root.read_text(encoding='utf-8')
assert 'noindex,nofollow' in root_html
assert 'url=/HIPSTUDIO/hu/' in root_html
home=(D/'hu/index.html').read_text(encoding='utf-8')
assert 'href="/HIPSTUDIO/' in home

# Approved custom-domain mode must serve from /, never from /HIPSTUDIO/.
custom_env=os.environ.copy(); custom_env['PAGES_PREFIX']='/'
subprocess.run(['python3','tools/prepare_pages_review.py'],cwd=R,env=custom_env,check=True)
subprocess.run(['python3','tools/test_pages_review_artifact.py'],cwd=R,env=custom_env,check=True)
root_html=(D/'index.html').read_text(encoding='utf-8')
assert 'url=/hu/' in root_html
assert '/HIPSTUDIO/' not in root_html
home=(D/'hu/index.html').read_text(encoding='utf-8')
assert 'href="/hu/' in home or 'href="/en/' in home or 'href="/de/' in home
assert 'href="/HIPSTUDIO/' not in home
assert 'src="/HIPSTUDIO/' not in home

print('Hosting config OK: hip.vipach.at uses root-path review artifacts, project-path fallback remains available, review stays noindex, and production remains fail-closed')
