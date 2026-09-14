# coding: utf-8
"""Restore an explicit, stable responsibility boundary on Business pillar pages."""
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'

PAGES = {
    'hu/uzleti-mukodes/index.html': 'A szabályozott feladatokat csak tisztázott felelősségi körrel vállaljuk.',
    'en/business-operations/index.html': 'Regulated work is only offered with clearly agreed responsibilities.',
    'de/business-operations/index.html': 'Regulierte Aufgaben übernehmen wir nur mit klar vereinbarten Verantwortlichkeiten.',
}

for rel, text in PAGES.items():
    path = D / rel
    if not path.exists():
        raise SystemExit(f'missing business pillar page: {rel}')
    html = path.read_text(encoding='utf-8')
    if 'data-business-scope-qualifier' not in html:
        block = f'<p class="scope-qualifier" data-business-scope-qualifier>{text}</p>'
        if '</main>' not in html:
            raise SystemExit(f'missing </main> in {rel}')
        html = html.replace('</main>', block + '</main>', 1)
        path.write_text(html, encoding='utf-8')

print('Business responsibility qualifier restored in HU/EN/DE')
