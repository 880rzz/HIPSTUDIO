# coding: utf-8
"""Regression checks for legal entity vs public studio structured-data boundaries."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SCRIPT_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', flags=re.DOTALL)

EXPECTED_REGISTERED = {
    "streetAddress": "Népszínház u. 25. Fe. 2.",
    "postalCode": "1081",
    "addressLocality": "Budapest",
    "addressCountry": "HU",
}
EXPECTED_STUDIO = {
    "streetAddress": "Lágymányosi utca 15.",
    "postalCode": "1111",
    "addressLocality": "Budapest",
    "addressCountry": "HU",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        fail("No generated dist HTML found; build must run before legal entity schema test")

    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        match = SCRIPT_RE.search(text)
        if not match:
            continue
        payload = json.loads(match.group(1))
        graph = payload.get("@graph", [])
        org = next((n for n in graph if isinstance(n, dict) and str(n.get("@id", "")).endswith("/#organization")), None)
        if org is None:
            continue
        checked += 1

        address = org.get("address", {})
        for key, value in EXPECTED_REGISTERED.items():
            if address.get(key) != value:
                fail(f"Legal Organization address drift in {page}: {key}={address.get(key)!r}")

        if "foundingDate" in org:
            fail(f"Unverified legal incorporation date leaked into Organization schema: {page}")

        studio_ref = org.get("location", {}).get("@id")
        if not studio_ref or not studio_ref.endswith("/#budapest-studio"):
            fail(f"Organization must reference the public studio as a separate Place: {page}")

        studio = next((n for n in graph if isinstance(n, dict) and n.get("@id") == studio_ref), None)
        if studio is None or studio.get("@type") != "Place":
            fail(f"Missing public studio Place node: {page}")
        studio_address = studio.get("address", {})
        for key, value in EXPECTED_STUDIO.items():
            if studio_address.get(key) != value:
                fail(f"Studio address drift in {page}: {key}={studio_address.get(key)!r}")

    if not checked:
        fail("No generated pages with legal Organization JSON-LD were checked")
    print(f"Legal entity schema boundary valid across {checked} Organization-bearing pages")


if __name__ == "__main__":
    main()
