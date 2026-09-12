# coding: utf-8
"""Apply the art-directed HIPStudio experience shell to generated platform HTML.

This runs after content generation/humanisation. It owns only the shared interactive
shell: privacy-gated hero film, full-screen navigation, and their static assets.
No third-party request is made during build or initial page load.
"""
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-platform"
HERO = json.loads((ROOT / "content/hero-media.json").read_text())

CSS = "platform-experience.css"
JS = "platform-experience.js"
shutil.copyfile(ROOT / "assets" / CSS, DIST / "assets" / CSS)
shutil.copyfile(ROOT / "assets" / JS, DIST / "assets" / JS)

MENU = {
    "hu": [
        ("/hu/kreativ-tartalom/", "Szolgáltatások", "Amit ténylegesen elkészítünk: fotó, film, podcast és a kapcsolódó tartalom."),
        ("/hu/megoldasok/", "Megoldások", "Ha nem szolgáltatást keresel, hanem egy konkrét kommunikációs vagy működési problémát kell megoldani."),
        ("/hu/vallalati-elmenyek/", "Élmények", "Csapat-, vezetői- és ügyfélélmények, amikor a közös programnak üzleti célja is van."),
        ("/hu/rolunk/", "Rólunk", "Kik dolgoznak a háttérben, hogyan oszlik meg a felelősség, és hogyan dolgozunk együtt."),
        ("/hu/kapcsolat/", "Kapcsolat", "Mondd el, mit kell elérni. Innen együtt rakjuk össze a szükséges stábot és formátumot."),
    ],
    "en": [
        ("/en/creative-content/", "Services", "What we actually make: photography, film, podcasts and the content around them."),
        ("/en/solutions/", "Solutions", "Start with the business problem, not a supplier category. We build the right combination around the outcome."),
        ("/en/corporate-experiences/", "Experiences", "Team, leadership and client experiences designed around a real business purpose."),
        ("/en/about/", "About", "Who works behind the scenes, how responsibility is divided and how we work together."),
        ("/en/contact/", "Contact", "Tell us what needs to happen. We will shape the right crew, scope and format from there."),
    ],
    "de": [
        ("/de/creative-content/", "Leistungen", "Was wir tatsächlich produzieren: Fotografie, Film, Podcasts und die Inhalte darum herum."),
        ("/de/solutions/", "Lösungen", "Wir starten mit dem konkreten Problem statt mit einer Lieferantenkategorie und bauen daraus den passenden Umfang."),
        ("/de/unternehmenserlebnisse/", "Erlebnisse", "Team-, Führungs- und Kundenerlebnisse mit einem klaren unternehmerischen Zweck."),
        ("/de/ueber-uns/", "Über uns", "Wer im Hintergrund arbeitet, wie Verantwortung verteilt ist und wie wir zusammenarbeiten."),
        ("/de/kontakt/", "Kontakt", "Sagen Sie uns, was erreicht werden soll. Daraus stellen wir Team, Umfang und Format zusammen."),
    ],
}

LABELS = {
    "hu": {"menu": "Menü", "close": "Menü bezárása", "nav": "Fő navigáció", "watch": "Film indítása", "source": "HIPStudio referenciafilm – saját YouTube-csatorna"},
    "en": {"menu": "Menu", "close": "Close menu", "nav": "Main navigation", "watch": "Play film", "source": "HIPStudio reference film – official YouTube channel"},
    "de": {"menu": "Menü", "close": "Menü schließen", "nav": "Hauptnavigation", "watch": "Film starten", "source": "HIPStudio Referenzfilm – offizieller YouTube-Kanal"},
}


def menu_markup(lang):
    links = "".join(
        f'<a class="menu-link" href="{href}"><span class="menu-title">{title}</span><span class="menu-copy">{copy}</span></a>'
        for href, title, copy in MENU[lang]
    )
    langs = "".join(
        f'<a href="/{code}/" lang="{code}" hreflang="{code}"' + (f' aria-current="page"' if code == lang else '') + f'>{code.upper()}</a>'
        for code in ("hu", "en", "de")
    )
    l = LABELS[lang]
    return f'''<header class="header site-header"><a class="brand" href="/{lang}/">HIPStudio</a><div class="header-tools"><nav class="langs" aria-label="Languages">{langs}</nav><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu"><span class="menu-toggle-label">{l['menu']}</span><span class="menu-icon" aria-hidden="true"><i></i><i></i></span></button></div></header><div class="menu-overlay" id="site-menu" hidden><div class="menu-shell"><div class="menu-head"><a class="menu-brand" href="/{lang}/">HIPStudio</a><button class="menu-close" type="button" aria-label="{l['close']}">×</button></div><nav class="menu-primary" aria-label="{l['nav']}">{links}</nav><div class="menu-foot"><p>Budapest · Vienna</p><a href="https://www.youtube.com/@wearehipstudio" rel="me external">YouTube / Reference films ↗</a></div></div></div>'''


def hero_markup(lang, old):
    title = re.search(r'<h1>(.*?)</h1>', old, re.S)
    lead = re.search(r'<p class="lead">(.*?)</p>', old, re.S)
    cta = re.search(r'<a class="button".*?</a>', old, re.S)
    eyebrow = re.search(r'<p class="eyebrow">(.*?)</p>', old, re.S)
    if not all((title, lead, cta, eyebrow)):
        raise SystemExit(f"Could not parse generated home hero for {lang}")
    l = LABELS[lang]
    return f'''<section class="hero hero-film" data-hero-video-id="{HERO['videoId']}"><div class="hero-film-media" aria-hidden="true"><div class="hero-film-poster"></div><div class="hero-film-frame" data-hero-frame></div></div><div class="hero-film-shade"></div><div class="hero-film-content"><p class="eyebrow">{eyebrow.group(1)}</p><h1>{title.group(1)}</h1><p class="lead">{lead.group(1)}</p><div class="hero-actions">{cta.group(0)}<button class="hero-play" type="button" data-hero-play aria-describedby="hero-film-source-{lang}"><span aria-hidden="true">▶</span>{l['watch']}</button></div><p class="hero-source" id="hero-film-source-{lang}">{l['source']}</p></div><noscript><p class="hero-noscript"><a href="{HERO['watchUrl']}">{l['watch']} ↗</a></p></noscript></section>'''


if not DIST.exists():
    raise SystemExit("dist-platform missing; run platform build first")

changed = 0
for page in DIST.rglob("*.html"):
    rel = page.relative_to(DIST).as_posix()
    lang = rel.split("/", 1)[0]
    if lang not in MENU:
        continue
    text = page.read_text()
    text = text.replace('<link rel="stylesheet" href="/assets/platform.css">', '<link rel="stylesheet" href="/assets/platform.css"><link rel="stylesheet" href="/assets/platform-experience.css">')
    text = text.replace('</head>', '<script src="/assets/platform-experience.js" defer></script></head>')
    text, n = re.subn(r'<header class="header">.*?</header>', menu_markup(lang), text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"Expected one generated header in {rel}")
    if rel == f"{lang}/index.html":
        text, n = re.subn(r'<section class="hero">.*?</section>', lambda m: hero_markup(lang, m.group(0)), text, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"Expected one home hero in {rel}")
    page.write_text(text)
    changed += 1

print(f"Enhanced platform experience shell: pages={changed}; hero={HERO['videoId']}")
