# coding: utf-8
"""Render the evidence-backed buyer-first IA into generated platform pages.

This is a build-time enrichment layer. It reads content/pain-points.json and only
renders VERIFIED items. QUALIFIED/REMOVE items remain non-public planning data.
No network access or production action is performed here.
"""
from pathlib import Path
from html import escape
import json

R = Path(__file__).resolve().parents[1]
D = R / "dist-platform"
DATA = json.loads((R / "content/pain-points.json").read_text(encoding="utf-8"))

LANGS = ("hu", "en", "de")
ROUTE_DIRS = {
    "home": {"hu": "hu", "en": "en", "de": "de"},
    "creative": {
        "hu": "hu/kreativ-tartalom",
        "en": "en/creative-content",
        "de": "de/creative-content",
    },
}
CONTACT = {
    "hu": "/hu/kapcsolat/",
    "en": "/en/contact/",
    "de": "/de/kontakt/",
}
COPY = {
    "hu": {
        "eyebrow": "Miből indulunk ki",
        "title": "Nem szolgáltatással kezdünk. A problémával.",
        "intro": "A brief akkor jó, ha előbb tisztázza, mit kell megoldani. Ezek azok a helyzetek, amelyekre jelenleg ellenőrzött HIPStudio-megoldást tudunk kapcsolni.",
        "problem": "Helyzet",
        "solution": "Mit csinálunk",
        "evidence": "Ellenőrzött jelenlegi HIPStudio szolgáltatásoldalak alapján.",
        "next": "Következő lépés",
    },
    "en": {
        "eyebrow": "Where we start",
        "title": "We do not start with a service. We start with the problem.",
        "intro": "A useful brief first defines what needs to change. These are the situations where HIPStudio currently has an evidence-backed response.",
        "problem": "Situation",
        "solution": "What we do",
        "evidence": "Backed by current verified HIPStudio service pages.",
        "next": "Next step",
    },
    "de": {
        "eyebrow": "Womit wir beginnen",
        "title": "Wir beginnen nicht mit einer Leistung. Wir beginnen mit dem Problem.",
        "intro": "Ein gutes Briefing klärt zuerst, was sich ändern soll. Für diese Situationen gibt es derzeit belegte HIPStudio-Lösungen.",
        "problem": "Situation",
        "solution": "Was wir tun",
        "evidence": "Durch aktuelle verifizierte HIPStudio-Leistungsseiten belegt.",
        "next": "Nächster Schritt",
    },
}


def e(value):
    return escape(str(value), quote=True)


def verified_for(route):
    return sorted(
        (
            item for item in DATA.get("painPoints", [])
            if item.get("status") == "VERIFIED" and route in item.get("routes", [])
        ),
        key=lambda item: item.get("priority", 999),
    )


def render(route, lang):
    items = verified_for(route)
    if not items:
        return ""
    c = COPY[lang]
    rows = []
    for index, item in enumerate(items, start=1):
        rows.append(
            f'''<li class="buyer-need" data-pain-point="{e(item['key'])}" data-evidence-status="VERIFIED">
  <div class="buyer-need__index" aria-hidden="true">{index:02d}</div>
  <div class="buyer-need__problem"><span>{e(c['problem'])}</span><h3>{e(item['pain'][lang])}</h3></div>
  <div class="buyer-need__answer"><span>{e(c['solution'])}</span><p>{e(item['solution'][lang])}</p><small>{e(c['evidence'])}</small></div>
  <div class="buyer-need__next"><span>{e(c['next'])}</span><a href="{e(CONTACT[lang])}">{e(item['cta'][lang])} <span aria-hidden="true">↗</span></a></div>
</li>'''
        )
    return f'''<section class="buyer-needs" aria-labelledby="buyer-needs-{lang}-{route}">
  <div class="buyer-needs__intro">
    <p class="eyebrow">{e(c['eyebrow'])}</p>
    <h2 id="buyer-needs-{lang}-{route}">{e(c['title'])}</h2>
    <p>{e(c['intro'])}</p>
  </div>
  <ol class="buyer-needs__list">{''.join(rows)}</ol>
</section>'''


def inject_stylesheet(html):
    href = "/assets/pain-points.css"
    if href in html:
        return html
    marker = '<link rel="stylesheet" href="/assets/platform.css">'
    if marker not in html:
        raise SystemExit("platform stylesheet marker missing")
    return html.replace(marker, marker + f'<link rel="stylesheet" href="{href}">', 1)


def inject_section(html, section):
    marker = '<section class="cta">'
    if marker not in html:
        raise SystemExit("CTA marker missing while inserting buyer-first IA")
    return html.replace(marker, section + marker, 1)


if DATA.get("status") != "review":
    raise SystemExit("pain-point architecture must remain review-scoped")

source_css = R / "assets/pain-points.css"
if not source_css.exists():
    raise SystemExit("assets/pain-points.css missing")
(D / "assets").mkdir(parents=True, exist_ok=True)
(D / "assets/pain-points.css").write_text(source_css.read_text(encoding="utf-8"), encoding="utf-8")

changed = 0
for route, lang_dirs in ROUTE_DIRS.items():
    for lang in LANGS:
        path = D / lang_dirs[lang] / "index.html"
        if not path.exists():
            raise SystemExit(f"platform route missing: {path.relative_to(R)}")
        html = path.read_text(encoding="utf-8")
        section = render(route, lang)
        html = inject_stylesheet(html)
        html = inject_section(html, section)
        path.write_text(html, encoding="utf-8")
        changed += 1

print(f"buyer-first IA rendered on {changed} localized routes")
