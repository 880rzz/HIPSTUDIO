# coding: utf-8
from pathlib import Path
import re
import subprocess

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'

# test_platform.py intentionally rebuilds the lower-level platform during its
# isolated contract checks. Recreate the canonical final platform before testing
# the post-processing layer that users actually see.
subprocess.run(['npm', 'run', 'build:platform'], cwd=R, check=True)
assert D.exists(), 'dist-platform missing after build:platform'

checks = {
    'hu/index.html': [
        'Három terület. Egy cél: működjön.',
        'Legyen rend a működésben.',
        'Legyen világos, mit képvisel a cég.',
        'Az emberek ne csak ott legyenek. Kapcsolódjanak.'
    ],
    'en/index.html': [
        'Three areas. One goal: make it work.',
        'Put the operation in order.',
        'Make it clear what the company stands for.',
        'People should not just attend. They should connect.'
    ],
    'de/index.html': [
        'Drei Bereiche. Ein Ziel: Es soll funktionieren.',
        'Ordnung in die Abläufe bringen.',
        'Klar machen, wofür das Unternehmen steht.',
        'Menschen sollen nicht nur teilnehmen. Sie sollen sich verbinden.'
    ]
}

human_css_link = re.compile(r'<link\b[^>]*href=["\']/assets/human-first-principles\.css["\'][^>]*>', re.I)

for rel, needles in checks.items():
    p = D / rel
    assert p.exists(), rel
    s = p.read_text(encoding='utf-8')
    assert human_css_link.search(s), f'{rel}: human stylesheet link missing'
    for needle in needles:
        assert needle in s, f'{rel}: missing {needle!r}'

banned = [
    'Komplexebb üzleti megoldások',
    'More integrated business solutions',
    'Umfassendere Unternehmenslösungen',
    'Egy HIPStudio. Több területen ugyanazzal a figyelemmel.',
    'One HIPStudio. More expertise, working together.',
    'Ein HIPStudio. Mehr Kompetenz, die zusammenarbeitet.'
]
for rel in checks:
    s = (D / rel).read_text(encoding='utf-8')
    for phrase in banned:
        assert phrase not in s, f'{rel}: promotional phrase leaked: {phrase}'

css = D / 'assets/human-first-principles.css'
assert css.exists(), 'human-first-principles.css not copied to dist-platform'
style = css.read_text(encoding='utf-8')
assert 'body{background:#f7f6f2' in style
assert 'grid-template-columns:repeat(3,minmax(0,1fr))' in style
assert '.pillar:nth-child(1){background:#eeeae1' in style
assert '.pillar:nth-child(2){background:#fff' in style
assert '.pillar:nth-child(3){background:#0b1736' in style

print('Human first-principles regression gate passed for HU/EN/DE and three-area separation')
