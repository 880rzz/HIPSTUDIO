#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "apps-script" / "HIPStudioQuoteRequest.gs"
text = SOURCE.read_text(encoding="utf-8")

fields_match = re.search(r"const CUSTOMER_FIELDS\s*=\s*\[(.*?)\];", text, re.S)
assert fields_match, "CUSTOMER_FIELDS not found"
fields = re.findall(r"'([a-z0-9_]+)'", fields_match.group(1))
assert fields, "CUSTOMER_FIELDS is empty"
assert len(fields) == len(set(fields)), "CUSTOMER_FIELDS contains duplicates"

labels_match = re.search(r"function customerLabels_\(lang\)\s*\{(.*?)\n\}", text, re.S)
assert labels_match, "customerLabels_ not found"
labels_fn = labels_match.group(1)

for lang, next_lang in (("hu", "en"), ("en", "de")):
    block_match = re.search(rf"\b{lang}:\s*\{{(.*?)\n\s*\}},\s*\n\s*{next_lang}:", labels_fn, re.S)
    assert block_match, f"{lang} label block not found"
    block = block_match.group(1)
    missing = [key for key in fields if not re.search(rf"\b{re.escape(key)}\s*:", block)]
    assert not missing, f"{lang} labels missing: {', '.join(missing)}"

de_match = re.search(r"\bde:\s*\{(.*?)\n\s*\}\s*\n\s*\}\[lang\]", labels_fn, re.S)
assert de_match, "de label block not found"
missing_de = [key for key in fields if not re.search(rf"\b{re.escape(key)}\s*:", de_match.group(1))]
assert not missing_de, f"de labels missing: {', '.join(missing_de)}"

assert "common[k] || k.replace" not in text, "technical fallback still used by quote email labels"
assert "customer_label_missing:" in labels_fn, "runtime fail-closed label coverage guard missing"

required_copy = [
    "Köszönjük, megérkezett az ajánlatkérésed.",
    "Hamarosan felvesszük veled a kapcsolatot.",
    "Thank you, we received your quote request.",
    "We will contact you shortly.",
    "Vielen Dank, Ihre Angebotsanfrage ist bei uns eingegangen.",
    "Wir melden uns in Kürze bei Ihnen.",
]
for phrase in required_copy:
    assert phrase in text, f"confirmation copy missing: {phrase}"

assert text.count("customerSubmittedRows_(r, r.language)") >= 2, "submitted fields must be included in internal and customer emails"
assert "replyTo:replyTo" in text and "HIPSTUDIO.CENTRAL_EMAIL" in text, "central Reply-To contract missing"

internal_only = {
    "request_id", "received_at", "response_due_at", "status", "owner", "owner_suggestion",
    "route", "queue", "priority", "complexity_score", "completeness_score", "next_action",
    "routing_flags", "routing_version", "raw_json"
}
leaked = sorted(internal_only.intersection(fields))
assert not leaked, f"internal-only fields exposed to customer email: {', '.join(leaked)}"

print(f"Quote email localization OK: {len(fields)} customer fields x 3 languages; no technical label fallback.")
