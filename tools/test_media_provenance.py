# coding: utf-8
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
manifest = json.loads((R / "content/media-provenance.json").read_text(encoding="utf-8"))
hero = json.loads((R / "content/hero-media.json").read_text(encoding="utf-8"))

assert manifest.get("status") == "review", "media provenance must remain review-scoped"
assert manifest.get("rules", {}).get("publicationSourceIsNotRehostingPermission") is True
assert manifest.get("rules", {}).get("noWixHotlinks") is True

assets = {item["id"]: item for item in manifest.get("assets", [])}
assert "home-hero-youtube-gnuMDSWR_tg" in assets
assert "hipstudio-youtube-channel" in assets

entry = assets["home-hero-youtube-gnuMDSWR_tg"]
assert entry["sourceClassification"] == "USER_CONFIRMED_FIRST_PARTY_PUBLICATION"
assert entry["sourceUrl"].endswith("gnuMDSWR_tg")
assert entry["channelUrl"] == hero["channelUrl"]
assert hero["videoId"] in entry["sourceUrl"]
assert entry["delivery"]["embedOrigin"] == "https://www.youtube-nocookie.com"
assert entry["delivery"]["initialThirdPartyRequest"] is False
assert entry["rights"]["downloadOrSelfHostDerivative"] == "NOT_ESTABLISHED"
assert entry["productionStatus"] == "CLEARED_FOR_PRIVACY_ENHANCED_OFFICIAL_EMBED_ONLY"

channel = assets["hipstudio-youtube-channel"]
assert channel["sourceUrl"] == hero["channelUrl"]
assert channel["rights"]["downloadOrSelfHostDerivative"] == "NOT_ESTABLISHED"
assert channel["productionStatus"] == "SOURCE_ONLY"

for item in manifest.get("assets", []):
    text = json.dumps(item, ensure_ascii=False).lower()
    assert "wixstatic.com" not in text
    assert "static.wixstatic.com" not in text

print("media provenance contract OK")
