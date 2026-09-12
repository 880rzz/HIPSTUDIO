# coding: utf-8
"""Regression checks for the generated fullscreen platform navigation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-platform"

REQUIRED = (
    'data-menu-toggle',
    'aria-controls="site-menu"',
    'aria-expanded="false"',
    'id="site-menu"',
    'role="dialog"',
    'aria-modal="true"',
    'data-menu-close',
    'class="site-menu-nav"',
    '/assets/platform-menu.css',
    '/assets/platform-menu.js',
)


def fail(message):
    raise SystemExit(message)


def main():
    if not DIST.exists():
        fail("dist-platform missing")
    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        fail("No platform HTML pages found")
    for asset in (DIST / "assets/platform-menu.css", DIST / "assets/platform-menu.js"):
        if not asset.exists() or asset.stat().st_size < 100:
            fail(f"Navigation asset missing or empty: {asset}")
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if '<header class="header">' not in text:
            continue
        checked += 1
        for token in REQUIRED:
            if token not in text:
                fail(f"Missing navigation contract {token!r}: {page}")
        header = re.search(r'<header class="header">(.*?)</header>', text, re.DOTALL)
        if not header:
            fail(f"Header parse failed: {page}")
        if 'class="nav"' in header.group(1):
            fail(f"Legacy desktop nav remains in header: {page}")
        if text.count('id="site-menu"') != 1:
            fail(f"Expected one site-menu id: {page}")
        if text.count('id="site-menu-title"') != 1:
            fail(f"Expected one menu title id: {page}")
        if 'href="/hu/megoldasok/"' not in text and '<html lang="hu">' in text:
            fail(f"HU solutions entry missing: {page}")
        if 'href="/en/solutions/"' not in text and '<html lang="en">' in text:
            fail(f"EN solutions entry missing: {page}")
        if 'href="/de/loesungen/"' not in text and '<html lang="de">' in text:
            fail(f"DE solutions entry missing: {page}")
    if not checked:
        fail("No platform headers checked")
    print(f"Fullscreen navigation contract valid across {checked} generated pages")


if __name__ == "__main__":
    main()
