# coding: utf-8
"""Regression gate for the concise one-pager problem/answer architecture."""
from pathlib import Path
from html import unescape
import json

R = Path(__file__).resolve().parents[1]
D = R / "dist-platform"
COMMERCIAL = json.loads((R / "content/commercial-content.json").read_text(encoding="utf-8"))
ROUTES = {
    "business": {"hu":"hu/uzleti-mukodes", "en":"en/business-operations", "de":"de/business-operations"},
    "creative": {"hu":"hu/kreativ-tartalom", "en":"en/creative-content", "de":"de/creative-content"},
    "experiences": {"hu":"hu/vallalati-elmenyek", "en":"en/corporate-experiences", "de":"de/unternehmenserlebnisse"},
}

for pillar, localized in ROUTES.items():
    for lang, route in localized.items():
        path = D / route / "index.html"
        assert path.exists(), path
        raw = path.read_text(encoding="utf-8")
        text = unescape(raw)
        assert raw.count('class="section editorial-problem"') == 1, path
        assert raw.count('class="section editorial-answer"') == 1, path
        assert COMMERCIAL["pillars"][pillar]["problem"][lang] in text, path
        assert COMMERCIAL["pillars"][pillar]["outcome"][lang] in text, path
        assert 'data-pain-point=' not in raw, path

print("Concise problem/answer one-pager regression gate passed for 9 localized service-area pages")
