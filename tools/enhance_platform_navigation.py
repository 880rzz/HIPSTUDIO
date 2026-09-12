# coding: utf-8
"""Replace generated top navigation with one accessible fullscreen editorial menu."""
from pathlib import Path
from html import escape
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-platform"
HEADER_RE = re.compile(r'<header class="header">.*?</header>', re.DOTALL)
LANG_RE = re.compile(r'<html lang="(hu|en|de)">')
LANGS_RE = re.compile(r'<nav class="langs"[^>]*>.*?</nav>', re.DOTALL)
PRIVACY_ROUTES = json.loads((ROOT / "content/privacy-governance.json").read_text(encoding="utf-8"))["publication"]["routes"]

ROUTES = {
    "solutions": {"hu": "/hu/megoldasok/", "en": "/en/solutions/", "de": "/de/loesungen/"},
    "creative": {"hu": "/hu/kreativ-tartalom/", "en": "/en/creative-content/", "de": "/de/creative-content/"},
    "business": {"hu": "/hu/uzleti-mukodes/", "en": "/en/business-operations/", "de": "/de/business-operations/"},
    "experiences": {"hu": "/hu/vallalati-elmenyek/", "en": "/en/corporate-experiences/", "de": "/de/unternehmenserlebnisse/"},
    "about": {"hu": "/hu/rolunk/", "en": "/en/about/", "de": "/de/ueber-uns/"},
    "contact": {"hu": "/hu/kapcsolat/", "en": "/en/contact/", "de": "/de/kontakt/"},
}

COPY = {
    "hu": {
        "open": "Menü megnyitása", "close": "Menü bezárása", "title": "Menü", "languages": "Nyelvválasztó", "menuLanguages": "Nyelvválasztó a menüben",
        "kicker": "Merre induljunk?",
        "note": "Nem szolgáltatáslistát akarunk rád borítani. Indulj abból, mi nem működik jól — innen már megmutatjuk, milyen szakmai kombináció lehet rá ésszerű válasz.",
        "items": {
            "solutions": ("Megoldások", "Ha előbb a problémádat szeretnéd megfogalmazni, és csak utána kiválasztani az eszközöket."),
            "creative": ("Creative", "Fotó, videó és podcast akkor, amikor hiteles, használható tartalomra van szükséged — egy összefogott gyártási folyamatban."),
            "business": ("Üzleti működés", "Amikor a napi működésben kell tisztább felelősség, adminisztráció vagy kontroll. A pontos vállalási kör mindig külön scope."),
            "experiences": ("Vállalati élmények", "Események és kapcsolódó produkciós feladatok, amikor a program változhat, de a megjelenésnek és a lebonyolításnak egyben kell maradnia."),
            "about": ("Hogyan dolgozunk", "Röviden arról, hogyan választjuk szét a bizonyított tényeket, a szakmai felelősséget és azt, amit még külön kell egyeztetni."),
            "contact": ("Konzultáció", "Írd le pár mondatban a helyzetet. Először azt tisztázzuk, mi a valódi feladat — nem azt, mit lehet még eladni hozzá."),
        },
        "contactLabel": "Kapcsolat"
    },
    "en": {
        "open": "Open menu", "close": "Close menu", "title": "Menu", "languages": "Languages", "menuLanguages": "Languages in menu",
        "kicker": "Where should we start?",
        "note": "We do not want to drop a service catalogue on you. Start with what is not working well; from there we can show which combination of specialist capabilities is a sensible response.",
        "items": {
            "solutions": ("Solutions", "Start with the problem first, then choose the production or operational tools that actually fit it."),
            "creative": ("Creative", "Photography, video and podcast when you need credible, usable content through one coordinated production flow."),
            "business": ("Business operations", "For situations that need clearer responsibility, administration or control. The exact responsibility boundary is always scoped separately."),
            "experiences": ("Corporate experiences", "Events and related production work when plans may move but the delivery still has to stay coherent."),
            "about": ("How we work", "How we separate verified facts, specialist responsibility and the areas that still require explicit agreement."),
            "contact": ("Consultation", "Describe the situation in a few lines. We start by clarifying the real job, not by adding things to a package."),
        },
        "contactLabel": "Contact"
    },
    "de": {
        "open": "Menü öffnen", "close": "Menü schließen", "title": "Menü", "languages": "Sprachauswahl", "menuLanguages": "Sprachauswahl im Menü",
        "kicker": "Wo sollen wir anfangen?",
        "note": "Wir wollen keinen Leistungskatalog über Sie ausschütten. Starten Sie mit dem, was nicht gut funktioniert; daraus lässt sich ableiten, welche Fachleistungen sinnvoll zusammengehören.",
        "items": {
            "solutions": ("Lösungen", "Zuerst das Problem klären, danach die Produktions- oder Betriebsbausteine auswählen, die wirklich dazu passen."),
            "creative": ("Creative", "Foto, Video und Podcast, wenn glaubwürdiger, nutzbarer Content in einem koordinierten Produktionsablauf gebraucht wird."),
            "business": ("Business Operations", "Wenn Verantwortlichkeiten, Administration oder Kontrolle klarer werden müssen. Der genaue Verantwortungsrahmen wird immer separat vereinbart."),
            "experiences": ("Unternehmenserlebnisse", "Events und verbundene Produktionsaufgaben, wenn sich der Ablauf ändern kann, die Umsetzung aber zusammenhalten muss."),
            "about": ("So arbeiten wir", "Wie wir belegte Fakten, fachliche Verantwortung und noch ausdrücklich zu klärende Bereiche voneinander trennen."),
            "contact": ("Beratung", "Beschreiben Sie die Situation in wenigen Sätzen. Wir klären zuerst die eigentliche Aufgabe — nicht, was man zusätzlich verkaufen könnte."),
        },
        "contactLabel": "Kontakt"
    },
}


def current_path(path: Path) -> str:
    rel = path.relative_to(DIST)
    parent = rel.parent.as_posix()
    return "/" + (parent + "/" if parent != "." else "")


def active(current: str, key: str, lang: str) -> bool:
    target = ROUTES[key][lang]
    if key == "solutions":
        return current.startswith(target)
    return current == target


def synthetic_language_nav(lang: str, current: str) -> str:
    c = COPY[lang]
    if current in PRIVACY_ROUTES.values():
        targets = PRIVACY_ROUTES
    else:
        targets = {code: f"/{code}/" for code in ("hu", "en", "de")}
    links = []
    for code in ("hu", "en", "de"):
        aria = ' aria-current="page"' if code == lang else ""
        links.append(f'<a lang="{code}" hreflang="{code}" href="{escape(targets[code], quote=True)}"{aria}>{code.upper()}</a>')
    return f'<nav class="langs" aria-label="{escape(c["languages"], quote=True)}">{"".join(links)}</nav>'


def menu_markup(lang: str, current: str, langs_nav: str) -> str:
    c = COPY[lang]
    links = []
    for key in ("solutions", "creative", "business", "experiences", "about", "contact"):
        title, desc = c["items"][key]
        aria = ' aria-current="page"' if active(current, key, lang) else ""
        links.append(
            f'<a class="site-menu-link" href="{escape(ROUTES[key][lang], quote=True)}"{aria}>'
            f'<span class="site-menu-title">{escape(title)}</span>'
            f'<span class="site-menu-copy">{escape(desc)}</span></a>'
        )
    overlay_langs = langs_nav.replace('class="langs"', 'class="site-menu-langs"')
    overlay_langs = re.sub(r'aria-label="[^"]*"', f'aria-label="{escape(c["menuLanguages"], quote=True)}"', overlay_langs, count=1)
    return (
        '<header class="header">'
        f'<a class="brand" href="/{lang}/">HIPStudio</a>'
        '<div class="header-tools">'
        f'{langs_nav}'
        f'<button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-menu" aria-label="{escape(c["open"], quote=True)}">'
        '<span class="menu-toggle-lines" aria-hidden="true"><span></span><span></span></span></button>'
        '</div></header>'
        f'<div class="site-menu" id="site-menu" role="dialog" aria-modal="true" aria-labelledby="site-menu-title" hidden>'
        '<div class="site-menu-shell">'
        '<div class="site-menu-head">'
        '<span class="site-menu-brand">HIPStudio</span>'
        f'<button class="menu-close" type="button" data-menu-close aria-label="{escape(c["close"], quote=True)}">×</button>'
        '</div>'
        '<div class="site-menu-grid">'
        f'<nav class="site-menu-nav" aria-labelledby="site-menu-title"><h2 id="site-menu-title" class="sr-only">{escape(c["title"])}</h2>{"".join(links)}</nav>'
        '<aside class="site-menu-aside">'
        f'<p class="site-menu-kicker">{escape(c["kicker"])}</p>'
        f'<p class="site-menu-note">{escape(c["note"])}</p>'
        f'<ul class="site-menu-quick"><li><a href="mailto:info@hipstudio.hu">info@hipstudio.hu</a></li><li><a href="{escape(ROUTES["contact"][lang], quote=True)}">{escape(c["contactLabel"])} →</a></li></ul>'
        f'{overlay_langs}'
        '</aside></div></div></div>'
    )


def main():
    if not DIST.exists():
        raise SystemExit("dist-platform missing; run platform build first")
    shutil.copyfile(ROOT / "assets/platform-menu.css", DIST / "assets/platform-menu.css")
    shutil.copyfile(ROOT / "assets/platform-menu.js", DIST / "assets/platform-menu.js")
    changed = 0
    for page in sorted(DIST.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        lang_match = LANG_RE.search(text)
        header_match = HEADER_RE.search(text)
        if not lang_match or not header_match:
            continue
        lang = lang_match.group(1)
        current = current_path(page)
        langs_match = LANGS_RE.search(header_match.group(0))
        langs_nav = langs_match.group(0) if langs_match else synthetic_language_nav(lang, current)
        replacement = menu_markup(lang, current, langs_nav)
        text = text[:header_match.start()] + replacement + text[header_match.end():]
        if '/assets/platform-menu.css' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="/assets/platform-menu.css"><script src="/assets/platform-menu.js" defer></script></head>')
        page.write_text(text, encoding="utf-8")
        changed += 1
    if not changed:
        raise SystemExit("No platform headers enhanced")
    print(f"Fullscreen navigation applied to {changed} platform pages")


if __name__ == "__main__":
    main()
