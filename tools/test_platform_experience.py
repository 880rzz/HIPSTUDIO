# coding: utf-8
"""Regression guard for the generated cinematic hero and full-screen menu."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-platform"
HERO = json.loads((ROOT / "content/hero-media.json").read_text())

if not DIST.exists():
    raise SystemExit("dist-platform missing; run build:platform first")

css = DIST / "assets/platform-experience.css"
js = DIST / "assets/platform-experience.js"
if not css.exists() or not js.exists():
    raise SystemExit("experience shell assets missing from platform build")

js_text = js.read_text()
if "www.youtube-nocookie.com/embed/" not in js_text:
    raise SystemExit("privacy-enhanced YouTube origin missing from interaction asset")
if "youtube.com/embed/" in js_text.replace("youtube-nocookie.com/embed/", ""):
    raise SystemExit("non-privacy YouTube embed origin found")

pages = list(DIST.rglob("*.html"))
localized = [p for p in pages if p.relative_to(DIST).parts[0] in {"hu", "en", "de"}]
if not localized:
    raise SystemExit("no localized platform pages found")

for page in localized:
    text = page.read_text()
    rel = page.relative_to(DIST).as_posix()
    for token in (
        'class="menu-toggle"',
        'id="site-menu"',
        'class="menu-overlay"',
        '/assets/platform-experience.css',
        '/assets/platform-experience.js',
    ):
        if token not in text:
            raise SystemExit(f"{rel}: missing experience token {token}")
    if '<iframe' in text:
        raise SystemExit(f"{rel}: iframe must not exist before user activation")
    if 'youtube-nocookie.com' in text:
        raise SystemExit(f"{rel}: third-party embed origin must not appear in initial HTML")

for lang in ("hu", "en", "de"):
    home = DIST / lang / "index.html"
    text = home.read_text()
    if f'data-hero-video-id="{HERO["videoId"]}"' not in text:
        raise SystemExit(f"{lang}: selected hero video id missing")
    if 'data-hero-play' not in text or 'data-hero-frame' not in text:
        raise SystemExit(f"{lang}: click-to-load hero controls missing")
    if HERO["watchUrl"] not in text:
        raise SystemExit(f"{lang}: noscript first-party watch fallback missing")

print(f"Platform experience shell OK: pages={len(localized)} hero={HERO['videoId']} initialThirdPartyRequests=0")
