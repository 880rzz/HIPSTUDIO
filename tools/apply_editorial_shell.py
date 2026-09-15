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
        ('home', 'Főoldal', 'Röviden a HIPStudio-ról.'),
        ('creative', 'Tartalomgyártás', 'Fotó · videó · podcast.'),
        ('business', 'Üzletfejlesztés', 'Működés, információ és fejlődés.'),
        ('experiences', 'Rendezvényszervezés', 'Céges és privát események.'),
        ('about', 'Partnerek', 'Dokumentált együttműködések.'),
        ('quote', 'Ajánlatkérés', 'Mondd el röviden, mire van szükséged.'),
        ('contact', 'Kapcsolat', 'Közvetlen elérhetőségek.')
    ],
    'en': [
        ('home', 'Home', 'HIPStudio in brief.'),('creative', 'Content production', 'Photography · video · podcast.'),
        ('business', 'Business development', 'Operations, information and growth.'),('experiences', 'Event production', 'Corporate and private events.'),
        ('about', 'Partners', 'Documented collaborations.'),('quote', 'Request a quote', 'Tell us briefly what you need.'),('contact', 'Contact', 'Direct contact details.')
    ],
    'de': [
        ('home', 'Start', 'HIPStudio in Kürze.'),('creative', 'Content-Produktion', 'Fotografie · Video · Podcast.'),
        ('business', 'Geschäftsentwicklung', 'Abläufe, Information und Entwicklung.'),('experiences', 'Veranstaltungsproduktion', 'Firmen- und Privatveranstaltungen.'),
        ('about', 'Partner', 'Dokumentierte Zusammenarbeiten.'),('quote', 'Angebot anfragen', 'Beschreiben Sie kurz, was Sie brauchen.'),('contact', 'Kontakt', 'Direkte Kontaktdaten.')
    ]
}

ROUTES = {
    'home': {'hu':'/hu/','en':'/en/','de':'/de/'},
    'business': {'hu':'/hu/uzleti-mukodes/','en':'/en/business-operations/','de':'/de/business-operations/'},
    'creative': {'hu':'/hu/kreativ-tartalom/','en':'/en/creative-content/','de':'/de/creative-content/'},
    'experiences': {'hu':'/hu/vallalati-elmenyek/','en':'/en/corporate-experiences/','de':'/de/unternehmenserlebnisse/'},
    'about': {'hu':'/hu/partnerek/','en':'/en/partners/','de':'/de/partner/'},
    'quote': {'hu':'/hu/ajanlatkeres/','en':'/en/request-a-quote/','de':'/de/angebot-anfragen/'},
    'contact': {'hu':'/hu/kapcsolat/','en':'/en/contact/','de':'/de/kontakt/'}
}

HERO = {
    'hu': {
        'eyebrow':'HIPStudio · 2006 óta',
        'title':'Gondolatból látható eredmény.',
        'lead':'<strong>Fotó, film, podcast</strong>, üzleti támogatás és vállalati élmények egy olyan rendszerben, ahol mindig látszik, mi a feladat, ki felel érte és mi lesz a kézzelfogható eredmény.',
        'play':'Showreel indítása',
        'frame':'HIPStudio showreel',
        'source':'Referenciafilm a HIPStudio saját YouTube-csatornájáról'
    },
    'en': {
        'eyebrow':'HIPStudio · since 2006',
        'title':'From thought to visible result.',
        'lead':'<strong>Photography, film, podcast</strong>, operational support and corporate experiences in one system where the task, responsibility and concrete result remain clear.',
        'play':'Play showreel',
        'frame':'HIPStudio showreel',
        'source':'Reference film from HIPStudio’s own YouTube channel'
    },
    'de': {
        'eyebrow':'HIPStudio · seit 2006',
        'title':'Aus Gedanken wird sichtbares Ergebnis.',
        'lead':'<strong>Fotografie, Film, Podcast</strong>, operative Unterstützung und Unternehmenserlebnisse in einem System, in dem Aufgabe, Verantwortung und Ergebnis klar bleiben.',
        'play':'Showreel starten',
        'frame':'HIPStudio Showreel',
        'source':'Referenzfilm vom eigenen HIPStudio YouTube-Kanal'
    }
}

CTA = {'hu':'Beszéljünk róla','en':'Let’s talk','de':'Sprechen wir darüber'}
MENU_LABEL = {'hu':'Menü megnyitása','en':'Open menu','de':'Menü öffnen'}
CLOSE_LABEL = {'hu':'Menü bezárása','en':'Close menu','de':'Menü schließen'}
HEADER_LANG_LABEL = {'hu':'Oldal nyelvválasztó','en':'Page languages','de':'Seitensprachen'}
MENU_LANG_LABEL = {'hu':'Menü nyelvválasztó','en':'Menu languages','de':'Menüsprachen'}
MENU_NAV_LABEL = {'hu':'Teljes képernyős menü','en':'Fullscreen menu','de':'Vollbildmenü'}


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
    return f'''<header class="header editorial-header"><a class="brand" href="/{lang}/">HIPStudio</a><nav class="langs" aria-label="{HEADER_LANG_LABEL[lang]}">{langs}</nav><button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-menu" aria-label="{MENU_LABEL[lang]}"><span class="menu-toggle-lines" aria-hidden="true"><span></span><span></span></span></button></header><div class="menu-overlay" id="site-menu" data-menu-overlay hidden><div class="menu-shell"><div class="menu-head"><a class="brand" href="/{lang}/">HIPStudio</a><button class="menu-close" type="button" data-menu-close aria-label="{CLOSE_LABEL[lang]}">×</button></div><div class="menu-grid"><nav class="menu-primary" aria-label="{MENU_NAV_LABEL[lang]}">{''.join(links)}</nav><aside class="menu-meta"><p class="eyebrow">HIPStudio</p><p>{HERO[lang]['lead']}</p><nav class="langs" aria-label="{MENU_LANG_LABEL[lang]}">{langs}</nav></aside></div></div></div>'''


def hero_markup(lang):
    h = HERO[lang]
    quote = ROUTES['quote'][lang]
    return f'''<section class="hero hero-film" data-hero-film><div class="hero-video-stage" data-hero-video-stage data-embed="{EMBED}"></div><div class="hero-art" aria-hidden="true"></div><div class="hero-film-content"><p class="eyebrow">{h['eyebrow']}</p><h1>{h['title']}</h1><p class="lead">{h['lead']}</p><div class="hero-film-actions"><button class="hero-play" type="button" data-hero-play data-frame-title="{h['frame']}">{h['play']}</button><a class="hero-quote-link" href="{quote}">{CTA[lang]} →</a></div><p class="hero-source">{h['source']} · <a href="{MEDIA['channelUrl']}">YouTube</a></p></div></section>'''

for path in D.rglob('index.html'):
    html = path.read_text()
    lang = lang_from_html(html)
    rel = '/' + path.relative_to(D).as_posix().removesuffix('index.html')

    html = re.sub(r'<link rel="stylesheet" href="/assets/editorial-shell\.css">', '', html)
    html = html.replace('</head>', '<link rel="stylesheet" href="/assets/editorial-shell.css"></head>')
    if '/assets/editorial-shell.js' not in html:
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
