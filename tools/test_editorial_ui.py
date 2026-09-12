# coding: utf-8
from pathlib import Path
import re

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
assert D.exists(), 'dist-platform missing; run build:platform first'

pages = list(D.rglob('index.html'))
assert pages, 'No platform pages generated'

home_count = 0
for path in pages:
    html = path.read_text(errors='ignore')
    rel = path.relative_to(D)
    assert '/assets/platform-editorial.css' in html, f'Editorial CSS missing: {rel}'
    assert '/assets/platform-menu.js' in html, f'Editorial JS missing: {rel}'
    assert 'class="menu-toggle"' in html, f'Hamburger trigger missing: {rel}'
    assert 'id="site-menu" hidden' in html, f'Full-screen menu missing/visible by default: {rel}'
    assert 'class="menu-copy"' in html, f'Human menu descriptions missing: {rel}'
    assert 'class="nav"' not in re.sub(r'<footer.*?</footer>', '', html, flags=re.S), f'Legacy desktop nav remains: {rel}'
    if re.search(r'^((hu|en|de)/)?index\.html$', str(rel).replace('\\','/')):
        home_count += 1
        assert 'data-hero-video' in html, f'Film hero missing: {rel}'
        assert 'data-src="https://www.youtube-nocookie.com/embed/gnuMDSWR_tg?' in html, f'Privacy hero embed missing: {rel}'
        assert not re.search(r'<iframe[^>]+src="https://www\.youtube-nocookie\.com', html, re.S), f'Eager YouTube request: {rel}'

assert home_count >= 3, f'Expected three localized home pages, got {home_count}'
css = (D / 'assets/platform-editorial.css').read_text()
js = (D / 'assets/platform-menu.js').read_text()
assert '@media (prefers-reduced-motion:reduce)' in css
assert "event.key === 'Escape'" in js
assert "event.key !== 'Tab'" in js
assert "body.classList.add('menu-open')" in js
print(f'Editorial UI gate: OK ({len(pages)} pages, {home_count} localized homes)')
