# coding: utf-8
"""Regression gate for the evidence-backed buyer-first IA.

The public/review render may expose only VERIFIED pain points. QUALIFIED/REMOVE
items remain planning data and must never leak into generated routes.
"""
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
DATA = json.loads((R / "content/pain-points.json").read_text(encoding="utf-8"))
DIST = R / "dist-platform"
LANGS = ("hu", "en", "de")
ROUTE_DIRS = {
    "home": {"hu": "hu", "en": "en", "de": "de"},
    "creative": {
        "hu": "hu/kreativ-tartalom",
        "en": "en/creative-content",
        "de": "de/creative-content",
    },
    "business": {
        "hu": "hu/uzleti-mukodes",
        "en": "en/business-operations",
        "de": "de/business-operations",
    },
}


def fail(message):
    raise SystemExit(message)


if DATA.get("status") != "review":
    fail("pain-point IA must remain review-scoped")

items = DATA.get("painPoints")
if not isinstance(items, list) or not items:
    fail("painPoints must be a non-empty list")

keys = [item.get("key") for item in items]
if len(keys) != len(set(keys)) or any(not key for key in keys):
    fail("pain-point keys must be present and unique")

priorities = [item.get("priority") for item in items]
if len(priorities) != len(set(priorities)) or any(not isinstance(p, int) for p in priorities):
    fail("pain-point priorities must be unique integers")

allowed_statuses = {"VERIFIED", "QUALIFIED", "REMOVE"}
for item in items:
    status = item.get("status")
    if status not in allowed_statuses:
        fail(f"invalid pain-point status for {item.get('key')}: {status}")
    for field in ("pain", "solution", "cta"):
        localized = item.get(field, {})
        for lang in LANGS:
            if not isinstance(localized.get(lang), str) or not localized[lang].strip():
                fail(f"missing {field}.{lang} for {item['key']}")
    evidence = item.get("evidence")
    if status == "VERIFIED" and (not isinstance(evidence, list) or not evidence or any(not str(e).strip() for e in evidence)):
        fail(f"VERIFIED pain point requires evidence: {item['key']}")
    routes = item.get("routes")
    if not isinstance(routes, list) or not routes:
        fail(f"pain point requires routes: {item['key']}")
    unknown = set(routes) - set(ROUTE_DIRS)
    if unknown:
        fail(f"unknown pain-point route(s) for {item['key']}: {sorted(unknown)}")

if not DIST.exists():
    fail("dist-platform missing; run build:platform before test:pain-points")

html_by_route = {}
for route, localized_dirs in ROUTE_DIRS.items():
    for lang, relative in localized_dirs.items():
        path = DIST / relative / "index.html"
        if not path.exists():
            fail(f"generated route missing: {path.relative_to(R)}")
        html_by_route[(route, lang)] = path.read_text(encoding="utf-8")

for item in items:
    marker = f'data-pain-point="{item["key"]}"'
    status = item["status"]
    if status == "VERIFIED":
        for route in item["routes"]:
            for lang in LANGS:
                if marker not in html_by_route[(route, lang)]:
                    fail(f"VERIFIED pain point not rendered: {item['key']} on {route}/{lang}")
        for route in ROUTE_DIRS:
            if route not in item["routes"]:
                for lang in LANGS:
                    if marker in html_by_route[(route, lang)]:
                        fail(f"pain point rendered outside declared route: {item['key']} on {route}/{lang}")
    else:
        for (route, lang), html in html_by_route.items():
            if marker in html:
                fail(f"non-VERIFIED pain point leaked into generated output: {item['key']} on {route}/{lang}")

print("pain-point IA regression gate passed")
