# coding: utf-8
from pathlib import Path
import re

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'

assert (D / 'assets/editorial-shell.css').exists(), 'Missing editorial shell CSS'
assert (D / 'assets/editorial-shell.js').exists(), 'Missing editorial shell JS'

for lang in ('hu', 'en', 'de'):
    path = D / lang / 'index.html'
    html = path.read_text()
    assert 'class="header editorial-header"' in html, f'Missing editorial header: {lang}'
    assert 'data-menu-toggle' in html and 'data-menu-overlay' in html and 'data-menu-close' in html, f'Missing fullscreen menu controls: {lang}'
    assert 'data-hero-film' in html and 'data-hero-video-stage' in html and 'data-hero-play' in html, f'Missing hero film shell: {lang}'
    assert 'https://www.youtube-nocookie.com/embed/gnuMDSWR_tg' in html, f'Missing privacy-enhanced hero source: {lang}'
    assert not re.search(r'<iframe[^>]+src=', html, flags=re.I | re.S), f'Eager third-party iframe request: {lang}'
    assert '/assets/editorial-shell.css' in html and '/assets/editorial-shell.js' in html, f'Missing editorial assets: {lang}'
    assert '<nav class="nav"' not in html, f'Legacy desktop navigation still rendered: {lang}'

js = (D / 'assets/editorial-shell.js').read_text()
for contract in ('Escape', 'aria-expanded', 'youtube-nocookie.com/embed/', 'prefers-reduced-motion'):
    assert contract in js, f'Missing interaction/privacy contract: {contract}'

css = (D / 'assets/editorial-shell.css').read_text()
for selector in ('.menu-overlay', '.menu-grid', '.hero.hero-film', '@media(prefers-reduced-motion:reduce)'):
    assert selector in css, f'Missing responsive/design contract: {selector}'

print('Editorial hero and fullscreen navigation regression: OK')
