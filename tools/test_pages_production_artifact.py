# coding: utf-8
from pathlib import Path
import re

R = Path(__file__).resolve().parents[1]
D = R / 'dist-pages-production'
assert D.exists(), 'dist-pages-production missing'
assert (D / 'CNAME').read_text(encoding='utf-8').strip() == 'www.hipstudio.hu'

root = (D / 'index.html').read_text(encoding='utf-8')
assert 'url=/hu/' in root
assert 'noindex' not in root.lower()
assert 'https://www.hipstudio.hu/hu/' in root

for rel in ['hu/index.html', 'en/index.html', 'de/index.html']:
    s = (D / rel).read_text(encoding='utf-8')
    assert 'https://www.hipstudio.hu/' in s, rel
    assert 'noindex,nofollow' not in s.lower(), rel
    assert 'hip.vipach.at' not in s, rel
    assert '/HIPSTUDIO/' not in s, rel

for rel, quote_path in [
    ('hu/kapcsolat/index.html', '/hu/ajanlatkeres/'),
    ('en/contact/index.html', '/en/request-a-quote/'),
    ('de/kontakt/index.html', '/de/angebot-anfragen/'),
]:
    s = (D / rel).read_text(encoding='utf-8')
    assert 'data-contact-live' in s, rel
    assert quote_path in s, rel
    assert 'mailto:info@hipstudio.hu' in s, rel
    assert 'tel:+36302215506' in s, rel

for rel in ['hu/ajanlatkeres/index.html', 'en/request-a-quote/index.html', 'de/angebot-anfragen/index.html']:
    s = (D / rel).read_text(encoding='utf-8')
    m = re.search(r'data-endpoint="([^"]+)"', s)
    assert m and m.group(1).startswith('https://script.google.com/macros/s/') and m.group(1).endswith('/exec'), rel
    assert '<script defer src="/assets/quote-form.js"></script>' in s, rel

# The guided form, including its submit button, is rendered by quote-form.js.
# Validate the runtime contract instead of expecting dynamic markup in HTML.
quote_js = (D / 'assets/quote-form.js').read_text(encoding='utf-8')
assert 'type="submit"' in quote_js
assert "(!endpoint?'disabled':'')" in quote_js
assert "if(!endpoint){error.textContent=t.review" in quote_js
assert "fetch(endpoint,{method:'POST'" in quote_js

all_html = '\n'.join(p.read_text(encoding='utf-8') for p in D.rglob('*.html'))
assert 'hip.vipach.at' not in all_html
assert 'nemeth.timea@hipstudio.hu' not in all_html
assert 'banhalmi.norbert@hipstudio.hu' not in all_html

print('Production Pages artifact OK: www canonical, root paths, live quote endpoint and contact routing verified')
