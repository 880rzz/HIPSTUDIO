# coding: utf-8
from pathlib import Path
import json, subprocess, os

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'
EXPECTED_PAGES=258
EXPECTED_SERVICE_PAGES=216
EXPECTED_SERVICES=55
EXPECTED_FAMILIES=13


def build(env=None):
    e=os.environ.copy(); e.update(env or {})
    subprocess.run(['python3','tools/build_platform.py'],cwd=R,env=e,check=True,capture_output=True,text=True)
    subprocess.run(['python3','tools/build_platform_solutions.py'],cwd=R,env=e,check=True,capture_output=True,text=True)
    subprocess.run(['python3','tools/build_platform_services.py'],cwd=R,env=e,check=True,capture_output=True,text=True)
    subprocess.run(['python3','tools/build_quote_request.py'],cwd=R,env=e,check=True,capture_output=True,text=True)


def assert_review():
    build()
    manifest=json.loads((D/'platform-build.json').read_text())
    assert manifest['mode']=='review'
    assert len(manifest['pages'])==EXPECTED_PAGES
    assert manifest['solutions']==5
    assert manifest['serviceInventory']['version']=='unified-service-inventory-v1'
    assert manifest['serviceInventory']['localizedPages']==EXPECTED_SERVICE_PAGES
    assert manifest['serviceInventory']['services']==EXPECTED_SERVICES
    assert manifest['serviceInventory']['families']==EXPECTED_FAMILIES
    assert manifest['quoteRequest']['version']=='hipstudio-quote-v1'
    assert manifest['quoteRequest']['pages']==3
    assert manifest['quoteRequest']['pricing']=='none'
    assert manifest['quoteRequest']['responseHours']==24
    assert manifest['quoteRequest']['endpointConfigured'] is False
    assert set(manifest['pillars'])=={'business','creative','experiences'}
    assert manifest['masterBrandApprovalRequired'] is True
    expected_solution_keys={'business-operations-360','finance-control','ai-readiness','content-engine','corporate-experience-design'}
    for page in manifest['pages']:
        html=(D/page['path'].strip('/')/'index.html').read_text()
        assert 'noindex,nofollow' in html
        assert f'<link rel="canonical" href="{page["canonical"]}">' in html
        assert html.count('rel="alternate" hreflang=')==4
        assert '<h1>' in html
        assert 'application/ld+json' in html
        assert 'subOrganization' not in html
        assert 'parentOrganization' not in html
        assert 'localStorage' not in html
        assert 'sessionStorage' not in html
    for key in expected_solution_keys:
        assert any('/'+key+'/' in p['path'] for p in manifest['pages'])
    expected_service_paths=[
      '/hu/szolgaltatasok/business/finance-admin/financial-administration/',
      '/hu/szolgaltatasok/hipstudio/photo-portrait/business-portrait/',
      '/hu/szolgaltatasok/hipstudio/video/conference-streaming/',
      '/hu/szolgaltatasok/flugos/corporate-experience/team-experience/',
      '/hu/szolgaltatasok/flugos/history-archive/flugos-futam-2019/'
    ]
    for path in expected_service_paths:
        assert any(p['path']==path for p in manifest['pages']),path
        html=(D/path.strip('/')/'index.html').read_text()
        if 'history-archive' in path:
            assert 'Történeti anyag' in html
            assert '<section class="cta">' not in html
            assert '"@type":"Service"' not in html
        else:
            assert '"@type":"Service"' in html
            assert '<section class="cta">' in html
            assert 'Egyedi ajánlatot kérek' in html
            assert '?pillar=' in html and '&amp;service=' in html
    for quote_path in ['/hu/ajanlatkeres/','/en/request-a-quote/','/de/angebot-anfragen/']:
        html=(D/quote_path.strip('/')/'index.html').read_text()
        assert 'info@hipstudio.hu' in html
        assert 'nemeth.timea@hipstudio.hu' not in html
        assert 'banhalmi.norbert@hipstudio.hu' not in html
        assert '24' in html
        assert '139990' not in html and '84990' not in html and '69990' not in html
        assert 'data-endpoint=""' in html
        assert '/assets/quote-form.js' in html
        assert '/assets/quote-prefill.js' in html
    app=(R/'apps-script/HIPStudioQuoteRequest.gs').read_text()
    assert 'nemeth.timea@hipstudio.hu' in app
    assert 'banhalmi.norbert@hipstudio.hu' in app
    assert "CENTRAL_EMAIL: 'info@hipstudio.hu'" in app
    assert "RESPONSE_HOURS: 24" in app
    assert (D/'robots.txt').read_text()=='User-agent: *\nDisallow: /\n'
    assert '<url><loc>' not in (D/'sitemap.xml').read_text()


def assert_production_gate():
    e=os.environ.copy();e.update({'BUILD_MODE':'production','PLATFORM_URL':'https://example.com'})
    p=subprocess.run(['python3','tools/build_platform.py'],cwd=R,env=e,capture_output=True,text=True)
    assert p.returncode != 0
    assert 'masterBrandApproval' in (p.stdout+p.stderr)
    assert 'publicationApproval' in (p.stdout+p.stderr)


def assert_quote_endpoint_gate():
    e={'BUILD_MODE':'production','PLATFORM_URL':'https://example.com','PLATFORM_MASTER_BRAND_APPROVED':'1','PLATFORM_PUBLICATION_APPROVED':'1'}
    env=os.environ.copy();env.update(e)
    subprocess.run(['python3','tools/build_platform.py'],cwd=R,env=env,check=True,capture_output=True,text=True)
    subprocess.run(['python3','tools/build_platform_solutions.py'],cwd=R,env=env,check=True,capture_output=True,text=True)
    subprocess.run(['python3','tools/build_platform_services.py'],cwd=R,env=env,check=True,capture_output=True,text=True)
    p=subprocess.run(['python3','tools/build_quote_request.py'],cwd=R,env=env,capture_output=True,text=True)
    assert p.returncode != 0
    assert 'QUOTE_FORM_ENDPOINT' in (p.stdout+p.stderr)


def assert_isolated_production_contract():
    build({'BUILD_MODE':'production','PLATFORM_URL':'https://example.com','PLATFORM_MASTER_BRAND_APPROVED':'1','PLATFORM_PUBLICATION_APPROVED':'1','QUOTE_FORM_ENDPOINT':'https://script.google.com/macros/s/test-review-endpoint/exec'})
    manifest=json.loads((D/'platform-build.json').read_text())
    assert manifest['mode']=='production'
    assert len(manifest['pages'])==EXPECTED_PAGES
    assert manifest['quoteRequest']['endpointConfigured'] is True
    assert (D/'robots.txt').read_text()=='User-agent: *\nAllow: /\n'
    sitemap=(D/'sitemap.xml').read_text()
    assert sitemap.count('<url><loc>')==EXPECTED_PAGES
    for page in manifest['pages']:
        html=(D/page['path'].strip('/')/'index.html').read_text()
        assert 'index,follow' in html
        assert page['canonical'].startswith('https://example.com/')
    quote=(D/'hu/ajanlatkeres/index.html').read_text()
    assert 'https://script.google.com/macros/s/test-review-endpoint/exec' in quote


if __name__=='__main__':
    assert_review()
    assert_production_gate()
    assert_quote_endpoint_gate()
    assert_isolated_production_contract()
    build()
    print('Unified platform tests passed')
