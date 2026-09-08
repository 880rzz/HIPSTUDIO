# coding: utf-8
from pathlib import Path
import json, re, subprocess, os, shutil

R=Path(__file__).resolve().parents[1]
D=R/'dist-platform'

def build(env=None):
    e=os.environ.copy(); e.update(env or {})
    subprocess.run(['python3','tools/build_platform.py'],cwd=R,env=e,check=True,capture_output=True,text=True)

def assert_review():
    build()
    manifest=json.loads((D/'platform-build.json').read_text())
    assert manifest['mode']=='review'
    assert len(manifest['pages'])==21
    assert set(manifest['pillars'])=={'business','creative','experiences'}
    assert manifest['masterBrandApprovalRequired'] is True
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
    assert (D/'robots.txt').read_text()=='User-agent: *\nDisallow: /\n'
    assert '<url><loc>' not in (D/'sitemap.xml').read_text()

def assert_production_gate():
    e=os.environ.copy();e.update({'BUILD_MODE':'production','PLATFORM_URL':'https://example.com'})
    p=subprocess.run(['python3','tools/build_platform.py'],cwd=R,env=e,capture_output=True,text=True)
    assert p.returncode != 0
    assert 'masterBrandApproval' in (p.stdout+p.stderr)
    assert 'publicationApproval' in (p.stdout+p.stderr)

def assert_isolated_production_contract():
    build({'BUILD_MODE':'production','PLATFORM_URL':'https://example.com','PLATFORM_MASTER_BRAND_APPROVED':'1','PLATFORM_PUBLICATION_APPROVED':'1'})
    manifest=json.loads((D/'platform-build.json').read_text())
    assert manifest['mode']=='production'
    assert (D/'robots.txt').read_text()=='User-agent: *\nAllow: /\n'
    sitemap=(D/'sitemap.xml').read_text()
    assert sitemap.count('<url><loc>')==21
    for page in manifest['pages']:
        html=(D/page['path'].strip('/')/'index.html').read_text()
        assert 'index,follow' in html
        assert page['canonical'].startswith('https://example.com/')

if __name__=='__main__':
    assert_review()
    assert_production_gate()
    assert_isolated_production_contract()
    build()
    print('Unified platform tests passed')
