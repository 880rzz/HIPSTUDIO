# coding: utf-8
"""Apply the art-directed HIPStudio navigation and privacy-gated film hero.

Runs after the platform generators/humanizer so it can preserve the final localized
copy while replacing only presentation structure. No network access is performed.
"""
from pathlib import Path
import json
import re

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
MEDIA = json.loads((R / 'content/hero-media.json').read_text())

VIDEO_ID = MEDIA['videoId']
EMBED = f"{MEDIA['embedOrigin']}/embed/{VIDEO_ID}?autoplay=1&mute=1&controls=0&loop=1&playlist={VIDEO_ID}&playsinline=1&rel=0&modestbranding=1"
CONTACT = {'hu': 'kapcsolat', 'en': 'contact', 'de': 'kontakt'}

COPY = {
    'hu': {
        'menu': 'Menü', 'close': 'Menü bezárása', 'nav': 'Fő navigáció',
        'showreel': 'Showreel indítása', 'watch': 'Film megnyitása YouTube-on',
        'intro': 'Válassz aszerint, mire van szükséged — nem aszerint, hogyan nevezzük a szolgáltatást.',
        'items': [
            ('Szolgáltatások', '/hu/kreativ-tartalom/', 'Amit ténylegesen elkészítünk: fotó, film, podcast és a kapcsolódó tartalom.'),
            ('Megoldások', '/hu/megoldasok/', 'Ha nem szolgáltatást keresel, hanem egy konkrét kommunikációs vagy működési problémát kell megoldani.'),
            ('Vállalati élmények', '/hu/vallalati-elmenyek/', 'Rugalmas formátumok, amelyek valódi helyzetekhez, csapatokhoz és helyszínekhez igazodnak.'),
            ('Hogyan dolgozunk', '/hu/rolunk/', 'Kik dolgoznak a háttérben, hogyan oszlik meg a felelősség, és mitől lesz kiszámítható a közös munka.'),
            ('Kapcsolat', '/hu/kapcsolat/', 'Mondd el, mit kell elérni. Innen együtt rakjuk össze a szükséges stábot, formátumot és tempót.'),
        ]
    },
    'en': {
        'menu': 'Menu', 'close': 'Close menu', 'nav': 'Main navigation',
        'showreel': 'Play showreel', 'watch': 'Watch film on YouTube',
        'intro': 'Start with what needs to change — not with the name of a service.',
        'items': [
            ('Services', '/en/creative-content/', 'What we actually make: photography, film, podcast and the content around them.'),
            ('Solutions', '/en/solutions/', 'For situations where the problem matters more than the service label.'),
            ('Corporate experiences', '/en/corporate-experiences/', 'Flexible formats shaped around the people, place, timing and outcome.'),
            ('How we work', '/en/about/', 'Who is responsible for what, how the work is scoped and how delivery stays predictable.'),
            ('Contact', '/en/contact/', 'Tell us what needs to happen. We will shape the right crew, format and pace around it.'),
        ]
    },
    'de': {
        'menu': 'Menü', 'close': 'Menü schließen', 'nav': 'Hauptnavigation',
        'showreel': 'Showreel starten', 'watch': 'Film auf YouTube ansehen',
        'intro': 'Beginnen Sie mit dem Problem, das gelöst werden soll — nicht mit dem Namen einer Leistung.',
        'items': [
            ('Leistungen', '/de/creative-content/', 'Was wir konkret produzieren: Fotografie, Film, Podcast und die dazugehörigen Inhalte.'),
            ('Lösungen', '/de/loesungen/', 'Für Situationen, in denen das Ergebnis wichtiger ist als die Bezeichnung einer Einzelleistung.'),
            ('Unternehmenserlebnisse', '/de/unternehmenserlebnisse/', 'Flexible Formate, abgestimmt auf Menschen, Ort, Zeit und gewünschte Wirkung.'),
            ('So arbeiten wir', '/de/ueber-uns/', 'Wer wofür verantwortlich ist, wie wir den Umfang klären und die Umsetzung planbar halten.'),
            ('Kontakt', '/de/kontakt/', 'Sagen Sie uns, was erreicht werden soll. Daraus entwickeln wir Team, Format und Tempo.'),
        ]
    }
}

for asset in ('platform-editorial.css', 'platform-menu.js'):
    (D / 'assets').mkdir(parents=True, exist_ok=True)
    (D / 'assets' / asset).write_text((R / 'assets' / asset).read_text())

for path in D.rglob('index.html'):
    html = path.read_text()
    mlang = re.search(r'<html lang="(hu|en|de)"', html)
    if not mlang:
        continue
    lang = mlang.group(1)
    c = COPY[lang]

    if '/assets/platform-editorial.css' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="/assets/platform.css">',
            '<link rel="stylesheet" href="/assets/platform.css"><link rel="stylesheet" href="/assets/platform-editorial.css">',
            1,
        )

    old_header = re.search(r'<header class="header">.*?</header>', html, flags=re.S)
    if old_header:
        old = old_header.group(0)
        langs = re.search(r'<nav class="langs".*?</nav>', old, flags=re.S)
        langs_html = langs.group(0) if langs else ''
        menu_links = ''.join(
            f'<a class="menu-link" href="{href}"><span class="menu-title">{title}</span><span class="menu-copy">{desc}</span></a>'
            for title, href, desc in c['items']
        )
        new_header = (
            '<header class="header header--editorial">'
            f'<a class="brand" href="/{lang}/">HIPStudio</a>'
            '<div class="header-controls">' + langs_html +
            f'<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="{c["menu"]}">'
            '<span></span><span></span></button></div></header>'
            '<div class="menu-overlay" id="site-menu" hidden>'
            '<div class="menu-shell"><div class="menu-head"><strong>HIPStudio</strong>'
            f'<button class="menu-close" type="button" aria-label="{c["close"]}"><span aria-hidden="true">×</span></button></div>'
            '<div class="menu-grid">'
            f'<nav class="menu-primary" aria-label="{c["nav"]}">{menu_links}</nav>'
            '<aside class="menu-meta"><p class="menu-kicker">HIPStudio</p>'
            f'<p class="menu-intro">{c["intro"]}</p>'
            f'<a class="menu-contact" href="/{lang}/{CONTACT[lang]}/">hipstudio.hu</a></aside>'
            '</div></div></div>'
        )
        html = html[:old_header.start()] + new_header + html[old_header.end():]

    hero = re.search(r'<section class="hero"><div>(.*?)</div><aside class="hero-side">(.*?)</aside></section>', html, flags=re.S)
    if hero:
        copy_html, meta_html = hero.group(1), hero.group(2)
        film = (
            '<section class="hero hero--film" data-hero-video>'
            '<div class="hero-film" aria-hidden="true">'
            '<div class="hero-film-placeholder"></div>'
            f'<iframe class="hero-film-frame" title="HIPStudio showreel" data-src="{EMBED}" loading="lazy" allow="autoplay; encrypted-media; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" tabindex="-1"></iframe>'
            '<div class="hero-film-shade"></div></div>'
            f'<div class="hero-film-copy">{copy_html}</div>'
            f'<aside class="hero-film-meta">{meta_html}</aside>'
            f'<button class="hero-film-activate" type="button"><span class="play-mark" aria-hidden="true">▶</span><span>{c["showreel"]}</span></button>'
            f'<noscript><p class="hero-noscript"><a href="{MEDIA["watchUrl"]}">{c["watch"]}</a></p></noscript>'
            '</section>'
        )
        html = html[:hero.start()] + film + html[hero.end():]

    if '/assets/platform-menu.js' not in html:
        html = html.replace('</body>', '<script src="/assets/platform-menu.js" defer></script></body>', 1)

    path.write_text(html)

print('Applied editorial navigation and privacy-gated film hero')
