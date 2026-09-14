# coding: utf-8
from pathlib import Path
import json, subprocess, os

R=Path(__file__).resolve().parents[1]
assert not (R/'vercel.json').exists(), 'HIPStudio must not carry a root Vercel config'
assert not (R/'tools/assert_vercel_build.py').exists(), 'HIPStudio Vercel build guard must be removed'
workflow=R/'.github/workflows/pages-review.yml'
assert workflow.exists(), 'GitHub Pages production workflow missing'
w=workflow.read_text(encoding='utf-8')
assert 'Publish HIPStudio production to GitHub Pages' in w
assert 'Require the approved production custom domain' in w
assert 'PRODUCTION_CUSTOM_DOMAIN: www.hipstudio.hu' in w
assert 'https://api.github.com/repos/${GITHUB_REPOSITORY}/pages' in w
assert 'expected $PRODUCTION_CUSTOM_DOMAIN' in w
assert 'BUILD_MODE: production' in w
assert 'PLATFORM_URL: https://www.hipstudio.hu' in w
assert 'QUOTE_REQUEST_BASE_URL: https://www.hipstudio.hu' in w
assert "PRODUCTION_CUTOVER_APPROVED: '1'" in w
assert 'QUOTE_FORM_ENDPOINT: ${{ secrets.QUOTE_FORM_ENDPOINT }}' in w
assert 'python3 tools/prepare_pages_production.py' in w
assert 'python3 tools/test_pages_production_artifact.py' in w
assert 'path: dist-pages-production' in w
assert 'hip.vipach.at' not in w
assert 'uses: actions/configure-pages@v5' in w
assert 'enablement: true' in w

package=(R/'package.json').read_text(encoding='utf-8')
assert '${BUILD_MODE:-review}' in package
assert 'python3 tools/assert_production_activation.py' in package
assert 'python3 tools/restore_business_scope_qualifier.py' in package
assert 'python3 tools/wire_contact.py' in package

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

# A normal production invocation still fails closed. Only the dedicated workflow
# may set the explicit owner-approved cutover flag, and it must also supply the
# real Google Apps Script endpoint.
production_env={'BUILD_MODE':'production','PLATFORM_PUBLICATION_APPROVED':'1','QUOTE_FORM_ENDPOINT':'https://example.invalid/quote'}
env=os.environ.copy(); env.update(production_env)
prod=subprocess.run(['npm','run','build:platform'],cwd=R,env=env,capture_output=True,text=True)
assert prod.returncode != 0, 'production build unexpectedly bypassed release gates'
assert 'Production activation BLOCKED' in (prod.stdout+prod.stderr)

# Review fallback remains testable and noindex even though deployment is now production.
subprocess.run(['python3','tools/prepare_pages_review.py'],cwd=R,check=True)
D=R/'dist-pages-review'
root=(D/'index.html')
assert root.exists(), 'Pages review root index missing'
root_html=root.read_text(encoding='utf-8')
assert 'noindex,nofollow' in root_html
assert 'url=/HIPSTUDIO/hu/' in root_html

assert (R/'tools/prepare_pages_production.py').exists()
assert (R/'tools/test_pages_production_artifact.py').exists()
print('Hosting config OK: www.hipstudio.hu is the sole production Pages domain; quote backend is secret-gated; review fallback remains fail-safe')
