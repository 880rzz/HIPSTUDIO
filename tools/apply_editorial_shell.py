# coding: utf-8
from pathlib import Path
import json
import re
import shutil

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'
MEDIA = json.loads((R / 'content/hero-media.json').read_text())
VIDEO_ID = MEDIA['videoId']
EMBED = f"{MEDIA['embedOrigin']}/embed/{VIDEO_ID}?autoplay=1&mute=1&controls=0&loop=1&playlist={VIDEO_ID}&rel=0&playsinline=1&modestbranding=1"

shutil.copyfile(R / 'assets/editorial-shell.css', D / 'assets/editorial-shell.css')
shutil.copyfile(R / 'assets/editorial-shell.js', D / 'assets/editorial-shell.js')

MENU = {
    'hu': [
        ('business', 'Szolgáltatások', 'Amit ténylegesen megoldunk a működés, tartalom és vállalati élmény oldaláról.'),
        ('creative', 'Kreatív tartalom', 'Fotó, film, podcast és a kapcsolódó tartalom egy koordinációs pontból.'),
        ('experiences', 'Vállalati élmények', 'Amikor az eseménynek nem programnak, hanem jól megtervezett közös élménynek kell érződnie.'),
        ('about', 'Rólunk', 'Kik dolgoznak a háttérben, hogyan oszlik meg a felelősség, és hogyan épül fel a közös munka.'),
        ('contact', 'Kapcsolat', 'Mondd el, mit kell elérni. Innen együtt rakjuk össze a szükséges formátumot és stábot.')
    ],
    'en': [
        ('business', 'Services', 'What we actually solve across operations, content and corporate experience.'),
        ('creative', 'Creative content', 'Photography, film, podcast and related content through one coordination layer.'),
        ('experiences', 'Corporate experiences', 'For moments that should feel intentionally designed rather than generically programmed.'),
        ('about', 'About', 'Who works behind the scenes, how responsibility is divided and how collaboration is structured.'),
        ('contact', 'Contact', 'Tell us what needs to change. We will shape the right format and team from there.')
    ],
    'de': [
        ('business', 'Leistungen', 'Was wir konkret in Betrieb, Content und Unternehmenserlebnis lösen.'),
        ('creative', 'Creative Content', 'Fotografie, Film, Podcast und begleitender Content aus einer Koordination.'),
        ('experiences', 'Unternehmenserlebnisse', 'Wenn ein Event bewusst gestaltet wirken soll statt wie ein Standardprogramm.'),
        ('about', 'Über uns', 'Wer im Hintergrund arbeitet, wie Verantwortung verteilt ist und wie Zusammenarbeit aufgebaut wird.'),
        ('contact', 'Kontakt', 'Sag uns, was erreicht werden soll. Daraus entwickeln wir Format und Team.')
    ]
}

ROUTES = {
    'business': {'hu':'/hu/uzleti-mukodes/','en':'/en/business-operations/','de':'/de/business-operations/'},
    'creative': {'hu':'/hu/kreativ-tartalom/','en':'/en/creative-content/','de':'/de/creative-content/'},
    'experiences': {'hu':'/hu/vallalati-elmenyek/','en':'/en/corporate-experiences/','de':'/de/unternehmenserlebnisse/'},
    'about': {'hu':'/hu/rolunk/','en':'/en/about/','de':'/de/ueber-uns/'},
    'contact': {'hu':'/hu/kapcsolat/','en':'/en/contact/','de':'/de/kontakt/'}
}

HERO = {
    'hu': {
        'eyebrow':'HIPStudio · 2006 óta',
        'title':'Kevesebb koordináció. Több, ami tényleg elkészül.',
        'lead':'Fotó, film, podcast, üzleti támogatás és vállalati élmények egy olyan rendszerben, ahol mindig látszik, mi a feladat, ki felel érte és mi lesz a kézzelfogható eredmény.',
        'play':'Showreel indítása',
        'frame':'HIPStudio showreel',
        'source':'Referenciafilm a HIPStudio saját YouTube-csatornájáról'
    },
    'en': {
        'eyebrow':'HIPStudio · since 2006',
        'title':'Less coordination. More work actually delivered.',
        'lead':'Photography, film, podcast, operational support and corporate experiences in one system where the task, responsibility and concrete result remain clear.',
        'play':'Play showreel',
        'frame':'HIPStudio showreel',
        'source':'Reference film from HIPStudio’s own YouTube channel'
    },
    'de': {
        'eyebrow':'HIPStudio · seit 2006',
        'title':'Weniger Abstimmung. Mehr, das wirklich fertig wird.',
        'lead':'Fotografie, Film, Podcast, operative Unterstützung und Unternehmenserlebnisse in einem System, in dem Aufgabe, Verantwortung und Ergebnis klar bleiben.',
        'play':'Showreel starten',
        'frame':'HIPStudio Showreel',
        'source':'Referenzfilm vom eigenen HIPStudio YouTube-Kanal'
    }
}

CTA = {'hu':'Beszéljünk róla','en':'Let’s talk','de':'Sprechen wir darüber'}
MENU_LABEL = {'hu':'Menü megnyitása','en':'Open menu','de':'Menü öffnen'}
CLOSE_LABEL = {'hu':'Menü bezárása','en':'Close menu','de':'Menü schließen'}
LANG_LABEL = {'hu':'Nyelvválasztó','en':'Languages','de':'Sprachauswahl'}


def lang_from_html(html):
    match = re.search(r'<html lang="(hu|en|de)"', html)
    if not match:
        raise RuntimeError('Missing supported html lang')
    return match.group(1)


def menu_markup(lang, current_path):
    links = []
    for key, title, copy in MENU[lang]:
        href = ROUTES[key][lang]
        current = ' aria-current="page"' if current_path == href else ''
        links.append(f'<a class="menu-link" href="{href}"{current}><span class="menu-title">{title}</span><span class="menu-copy">{copy}</span></a>')
    langs = ''.join(f'<a lang="{l}" hreflang="{l}" href="/{l}/">{l.upper()}</a>' for l in ('hu','en','de'))
    return f'''<header class="header editorial-header"><a class="brand" href="/{lang}/">HIPStudio</a><nav class="langs" aria-label="{LANG_LABEL[lang]}">{langs}</nav><button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-menu" aria-label="{MENU_LABEL[lang]}"><span class="menu-toggle-lines" aria-hidden="true"><span></span><span></span></span></button></header><div class="menu-overlay" id="site-menu" data-menu-overlay hidden><div class="menu-shell"><div class="menu-head"><a class="brand" href="/{lang}/">HIPStudio</a><button class="menu-close" type="button" data-menu-close aria-label="{CLOSE_LABEL[lang]}">×</button></div><div class="menu-grid"><nav class="menu-primary" aria-label="Main navigation">{''.join(links)}</nav><aside class="menu-meta"><p class="eyebrow">HIPStudio</p><p>{HERO[lang]['lead']}</p><nav class="langs" aria-label="{LANG_LABEL[lang]}">{langs}</nav></aside></div></div></div>'''


def hero_markup(lang):
    h = HERO[lang]
    contact = ROUTES['contact'][lang]
    return f'''<section class="hero hero-film" data-hero-film><div class="hero-video-stage" data-hero-video-stage data-embed="{EMBED}"></div><div class="hero-art" aria-hidden="true"></div><div class="hero-film-content"><p class="eyebrow">{h['eyebrow']}</p><h1>{h['title']}</h1><p class="lead">{h['lead']}</p><div class="hero-film-actions"><a class="button" href="{contact}">{CTA[lang]} →</a><button class="hero-play" type="button" data-hero-play data-frame-title="{h['frame']}">{h['play']}</button></div><p class="hero-source">{h['source']} · <a href="{MEDIA['channelUrl']}">YouTube</a></p></div></section>'''

for path in D.rglob('index.html'):
    html = path.read_text()
    lang = lang_from_html(html)
    rel = '/' + path.relative_to(D).as_posix().removesuffix('index.html')

    html = html.replace('<link rel="stylesheet" href="/assets/platform.css">', '<link rel="stylesheet" href="/assets/platform.css"><link rel="stylesheet" href="/assets/editorial-shell.css">')
    html = html.replace('</body>', '<script src="/assets/editorial-shell.js" defer></script></body>')

    header_match = re.search(r'<header class="header">.*?</header>', html, flags=re.S)
    if header_match:
        html = html[:header_match.start()] + menu_markup(lang, rel) + html[header_match.end():]

    if rel in ('/hu/','/en/','/de/'):
        hero_match = re.search(r'<section class="hero">.*?</section>', html, flags=re.S)
        if not hero_match:
            raise RuntimeError(f'Home hero not found in {path}')
        html = html[:hero_match.start()] + hero_markup(lang) + html[hero_match.end():]

    path.write_text(html)

print('Applied editorial fullscreen navigation and privacy-enhanced hero shell')
