#!/usr/bin/env python3
from pathlib import Path
from html import escape
import re, shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist-platform'
ASSETS = DIST / 'assets'

DESCRIPTIONS = {
    'hu': {
        'business': 'Működési és üzleti háttér azokhoz a helyzetekhez, ahol kevesebb koordináció és tisztább felelősség kell.',
        'creative': 'Fotó, videó, podcast és tartalomgyártás: amit ténylegesen elkészítünk és átadunk.',
        'experiences': 'Céges események és élmények akkor, amikor a programnak karaktere és működő produkciója is kell.',
        'about': 'Kik vagyunk, hogyan dolgozunk, és hol húzzuk meg a felelősségi határokat.',
        'contact': 'Írj pár mondatot a helyzetről; innen indul a scope és a következő konkrét lépés.',
        'default': 'Nézd meg röviden, mire való ez a terület és hogyan kapcsolódik a HIPStudio rendszerhez.'
    },
    'en': {
        'business': 'Operational and business support for situations that need less coordination and clearer responsibility.',
        'creative': 'Photography, video, podcast and content production: what we actually make and deliver.',
        'experiences': 'Corporate events and experiences when the programme needs both character and dependable production.',
        'about': 'Who we are, how we work and where the responsibility boundaries are.',
        'contact': 'Tell us the situation in a few lines; scope and the next concrete step start here.',
        'default': 'See what this area is for and how it connects to the HIPStudio system.'
    },
    'de': {
        'business': 'Operative und geschäftliche Unterstützung, wenn weniger Koordination und klare Verantwortung gefragt sind.',
        'creative': 'Foto, Video, Podcast und Content-Produktion: was wir tatsächlich erstellen und liefern.',
        'experiences': 'Unternehmenserlebnisse, wenn Programm, Charakter und verlässliche Produktion zusammenkommen müssen.',
        'about': 'Wer wir sind, wie wir arbeiten und wo die Verantwortungsgrenzen liegen.',
        'contact': 'Beschreiben Sie die Situation in wenigen Zeilen; hier beginnen Scope und der nächste konkrete Schritt.',
        'default': 'Kurz erklärt, wofür dieser Bereich da ist und wie er zum HIPStudio-System gehört.'
    }
}

FALLBACK_NAV = {
    'hu': [('/hu/uzleti-mukodes/','Business'),('/hu/kreativ-tartalom/','Creative'),('/hu/vallalati-elmenyek/','Flúgos'),('/hu/rolunk/','Hogyan dolgozunk'),('/hu/kapcsolat/','Konzultáció')],
    'en': [('/en/business-operations/','Business'),('/en/creative-content/','Creative'),('/en/corporate-experiences/','Flúgos'),('/en/about/','How we work'),('/en/contact/','Consultation')],
    'de': [('/de/business-operations/','Business'),('/de/creative-content/','Creative'),('/de/unternehmenserlebnisse/','Flúgos'),('/de/ueber-uns/','So arbeiten wir'),('/de/kontakt/','Beratung')]
}


def plain(text):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', text)).strip()


def category(href, label):
    value = f'{href} {label}'.lower()
    if any(x in value for x in ('business','uzleti','mukodes')): return 'business'
    if any(x in value for x in ('creative','kreativ','hipstudio')): return 'creative'
    if any(x in value for x in ('experience','elmeny','flugos','unternehmenserlebnisse')): return 'experiences'
    if any(x in value for x in ('about','rolunk','ueber','hogyan','arbeiten')): return 'about'
    if any(x in value for x in ('contact','kapcsolat','kontakt','consult','konzult','beratung','quote','ajanlat')): return 'contact'
    return 'default'


def menu_links(nav_html, lang):
    anchors = re.findall(r'<a\b([^>]*)>(.*?)</a>', nav_html, flags=re.I|re.S)
    if not anchors:
        anchors = [(f' href="{escape(href)}"', escape(label)) for href, label in FALLBACK_NAV[lang]]
    output = []
    for attrs, body in anchors:
        href_match = re.search(r'href="([^"]+)"', attrs)
        href = href_match.group(1) if href_match else ''
        label = plain(body)
        kind = category(href, label)
        cleaned = re.sub(r'\sclass="[^"]*"', '', attrs)
        output.append(
            f'<a class="menu-link"{cleaned}><span class="menu-link-title">{escape(label)}</span>'
            f'<span class="menu-link-copy">{escape(DESCRIPTIONS[lang][kind])}</span></a>'
        )
    return ''.join(output)


def apply(path):
    html = path.read_text(encoding='utf-8')
    lang_match = re.search(r'<html\s+lang="(hu|en|de)"', html, re.I)
    if not lang_match or '<header class="header">' not in html:
        return False
    lang = lang_match.group(1).lower()
    header_match = re.search(r'<header class="header">(.*?)</header>', html, flags=re.S)
    if not header_match:
        return False
    header = header_match.group(1)
    brand_match = re.search(r'<a class="brand".*?</a>', header, flags=re.S)
    brand = brand_match.group(0) if brand_match else f'<a class="brand" href="/{lang}/">HIPStudio</a>'
    nav_match = re.search(r'<nav class="nav"[^>]*>(.*?)</nav>', header, flags=re.S)
    nav_html = nav_match.group(1) if nav_match else ''
    langs_match = re.search(r'<nav class="langs"[^>]*>(.*?)</nav>', header, flags=re.S)
    langs_inner = langs_match.group(1) if langs_match else ''
    links = menu_links(nav_html, lang)
    language_nav = f'<nav class="langs" aria-label="Languages">{langs_inner}</nav>' if langs_inner else ''
    menu_label = {'hu':'Menü','en':'Menu','de':'Menü'}[lang]
    close_label = {'hu':'Menü bezárása','en':'Close menu','de':'Menü schließen'}[lang]
    kicker = {'hu':'Navigáció','en':'Navigation','de':'Navigation'}[lang]
    aside_title = {'hu':'Kevesebb keresgélés.','en':'Less searching around.','de':'Weniger Suchen.'}[lang]
    aside_copy = {
        'hu':'A menü azt mutatja, milyen problémákra melyik szakmai terület ad választ. A részletek mögött a scope, a bizonyíték és a következő lépés is látható.',
        'en':'The menu shows which specialist area answers which kind of problem. Each route makes scope, evidence and the next step visible.',
        'de':'Das Menü zeigt, welcher Fachbereich welches Problem löst. Jede Route macht Scope, Nachweis und den nächsten Schritt sichtbar.'
    }[lang]
    replacement = (
        f'<header class="header">{brand}<div class="header-menu-tools">'
        f'<button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-menu" aria-label="{escape(menu_label)}">'
        '<span class="menu-toggle-lines" aria-hidden="true"><span></span><span></span></span></button></div></header>'
        f'<div class="menu-overlay" id="site-menu" data-menu-overlay hidden aria-hidden="true"><div class="menu-shell">'
        f'<div class="menu-head"><p class="menu-kicker">{escape(kicker)}</p><button class="menu-close" type="button" data-menu-close aria-label="{escape(close_label)}">×</button></div>'
        f'<div class="menu-grid"><nav class="menu-primary" aria-label="{escape(kicker)}">{links}</nav><aside class="menu-aside">'
        f'<strong>{escape(aside_title)}</strong><p>{escape(aside_copy)}</p>{language_nav}</aside></div></div></div>'
    )
    html = html[:header_match.start()] + replacement + html[header_match.end():]
    if '/assets/platform-menu.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/assets/platform-menu.css"><script src="/assets/platform-menu.js" defer></script></head>', 1)
    path.write_text(html, encoding='utf-8')
    return True


def main():
    if not DIST.exists():
        raise SystemExit('dist-platform missing; run platform build first')
    ASSETS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / 'assets/platform-menu.css', ASSETS / 'platform-menu.css')
    shutil.copy2(ROOT / 'assets/platform-menu.js', ASSETS / 'platform-menu.js')
    changed = 0
    for page in DIST.rglob('*.html'):
        changed += int(apply(page))
    if changed == 0:
        raise SystemExit('No platform pages received full-screen navigation')
    print(f'Applied full-screen navigation to {changed} platform pages')

if __name__ == '__main__':
    main()
