# coding: utf-8
"""Normalize legacy JSON-LD so legal entity and public studio are not conflated.

This is a deterministic build-stage normalization. It does not touch source content,
DNS, Wix, or production configuration.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

REGISTERED_OFFICE = {
    "@type": "PostalAddress",
    "streetAddress": "Népszínház u. 25. Fe. 2.",
    "postalCode": "1081",
    "addressLocality": "Budapest",
    "addressCountry": "HU",
}

STUDIO_ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "Lágymányosi utca 15.",
    "postalCode": "1111",
    "addressLocality": "Budapest",
    "addressCountry": "HU",
}

SCRIPT_RE = re.compile(
    r'(<script type="application/ld\+json">)(.*?)(</script>)',
    flags=re.DOTALL,
)


def find_organization(payload: dict):
    graph = payload.get("@graph")
    if not isinstance(graph, list):
        return None, graph
    for node in graph:
        if not isinstance(node, dict):
            continue
        node_id = node.get("@id", "")
        node_types = node.get("@type", [])
        if isinstance(node_types, str):
            node_types = [node_types]
        if node_id.endswith("/#organization") and "Organization" in node_types:
            return node, graph
    return None, graph


def normalize_graph(payload: dict) -> bool:
    organization, graph = find_organization(payload)
    if organization is None:
        return False

    changed = False

    if organization.get("address") != REGISTERED_OFFICE:
        organization["address"] = REGISTERED_OFFICE
        changed = True

    # 2006-02-27 is supported as HIPStudio brand/domain history, not as the
    # legal incorporation date of Hipstudió Kft. Keep it off the Organization
    # node until a primary legal source verifies the company's incorporation.
    if "foundingDate" in organization:
        organization.pop("foundingDate", None)
        changed = True

    studio_id = organization.get("@id", "").replace("/#organization", "/#budapest-studio")
    if organization.get("location") != {"@id": studio_id}:
        organization["location"] = {"@id": studio_id}
        changed = True

    studio = next((n for n in graph if isinstance(n, dict) and n.get("@id") == studio_id), None)
    expected_studio = {
        "@type": "Place",
        "@id": studio_id,
        "name": "HIPStudio Budapest studio",
        "address": STUDIO_ADDRESS,
    }
    if studio is None:
        graph.append(expected_studio)
        changed = True
    elif any(studio.get(k) != v for k, v in expected_studio.items()):
        studio.clear()
        studio.update(expected_studio)
        changed = True

    return changed


def normalize_html(path: Path) -> tuple[bool, bool]:
    text = path.read_text(encoding="utf-8")
    match = SCRIPT_RE.search(text)
    if not match:
        return False, False

    payload = json.loads(match.group(2))
    organization, _ = find_organization(payload)
    if organization is None:
        return False, False

    changed = normalize_graph(payload)
    if changed:
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        updated = text[: match.start(2)] + encoded + text[match.end(2) :]
        path.write_text(updated, encoding="utf-8")
    return True, changed


def main() -> None:
    if not DIST.exists():
        raise SystemExit("dist does not exist; run tools/build.py first")

    html_files = sorted(DIST.rglob("*.html"))
    if not html_files:
        raise SystemExit("No generated HTML files found in dist")

    eligible = 0
    changed = 0
    for path in html_files:
        has_org, was_changed = normalize_html(path)
        eligible += int(has_org)
        changed += int(was_changed)

    if not eligible:
        raise SystemExit("No generated HTML pages with legal Organization JSON-LD found")
    if changed != eligible:
        raise SystemExit(f"Legal schema normalization incomplete: {changed}/{eligible} Organization pages changed")

    print(f"Legal entity schema normalized in {changed} Organization-bearing HTML files")


if __name__ == "__main__":
    main()
