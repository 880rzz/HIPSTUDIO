# coding: utf-8
"""Regression: generated Organization uses canonical legal office and separate studio Place."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
LEGAL = json.loads((ROOT / "content/legal-controller.json").read_text(encoding="utf-8"))
TARGET = LEGAL["effectiveTarget"]
REGISTERED = TARGET["registeredOfficeAddress"]
STUDIO = TARGET["publicContact"]["studioPostalAddress"]
SCRIPT_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def fail(message): raise SystemExit(message)


def main():
    checked = 0
    for directory in (ROOT / "dist", ROOT / "dist-platform"):
        for page in sorted(directory.rglob("*.html")):
            match = SCRIPT_RE.search(page.read_text(encoding="utf-8"))
            if not match: continue
            graph = json.loads(match.group(1)).get("@graph", [])
            org = next((n for n in graph if isinstance(n, dict) and str(n.get("@id", "")).endswith("/#organization")), None)
            if org is None: continue
            checked += 1
            if org.get("legalName") != TARGET["controllerName"]:
                fail(f"Legal name drift: {page}")
            if org.get("address") != {"@type":"PostalAddress", **REGISTERED}:
                fail(f"Registered office drift: {page}")
            if "foundingDate" in org:
                fail(f"Unverified Kft foundingDate in Organization: {page}")
            studio_id = org.get("location", {}).get("@id")
            if not studio_id or not studio_id.endswith("/#budapest-studio"):
                fail(f"Missing studio reference: {page}")
            studio = next((n for n in graph if isinstance(n, dict) and n.get("@id") == studio_id), None)
            if not studio or studio.get("address") != {"@type":"PostalAddress", **STUDIO}:
                fail(f"Studio Place drift: {page}")
    if not checked: fail("No Organization-bearing generated pages checked")
    print(f"Legal entity/studio schema boundary valid across {checked} generated pages")

if __name__ == "__main__": main()
