# coding: utf-8
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
assert D.exists(), 'dist-platform missing; run build:platform first'

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

for rel, needles in checks.items():
    p = D / rel
    assert p.exists(), rel
    s = p.read_text(encoding='utf-8')
    assert 'class="human-first-principles"' in s, rel
    assert 'href="/assets/human-first-principles.css"' in s, rel
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

css = (D / 'assets/human-first-principles.css')
assert css.exists(), 'human-first-principles.css not copied to dist-platform'
style = css.read_text(encoding='utf-8')
assert 'grid-template-columns:repeat(3,minmax(0,1fr))' in style
assert '.pillar:nth-child(3)' in style

print('Human first-principles regression gate passed for HU/EN/DE and three-area separation')
