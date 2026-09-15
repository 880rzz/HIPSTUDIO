# coding: utf-8
"""Project canonical legal-controller data into generated JSON-LD outputs."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
LEGAL = json.loads((ROOT / "content/legal-controller.json").read_text(encoding="utf-8"))
TARGET = LEGAL["effectiveTarget"]
REGISTERED = TARGET["registeredOfficeAddress"]
STUDIO = TARGET["publicContact"]["studioPostalAddress"]
WIKIDATA = "https://www.wikidata.org/wiki/Q138482177"
FOUNDED = "2006-02-27"
SCRIPT_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.DOTALL)


def organization_node(graph):
    for node in graph if isinstance(graph, list) else []:
        if not isinstance(node, dict):
            continue
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if "Organization" in types and str(node.get("@id", "")).endswith("/#organization"):
            return node
    return None


def normalize(path: Path):
    text = path.read_text(encoding="utf-8")
    match = SCRIPT_RE.search(text)
    if not match:
        return False, False
    payload = json.loads(match.group(2))
    graph = payload.get("@graph", [])
    org = organization_node(graph)
    if org is None:
        return False, False

    org["legalName"] = TARGET["controllerName"]
    org["address"] = {"@type": "PostalAddress", **REGISTERED}
    org["foundingDate"] = FOUNDED
    same_as = org.get("sameAs", [])
    if isinstance(same_as, str):
        same_as = [same_as]
    org["sameAs"] = [WIKIDATA] + [value for value in same_as if value != WIKIDATA]

    studio_id = org["@id"].replace("/#organization", "/#budapest-studio")
    org["location"] = {"@id": studio_id}
    expected = {
        "@type": "Place",
        "@id": studio_id,
        "name": "HIPStudio Budapest studio",
        "address": {"@type": "PostalAddress", **STUDIO},
    }
    studio = next((n for n in graph if isinstance(n, dict) and n.get("@id") == studio_id), None)
    if studio is None:
        graph.append(expected)
    else:
        studio.clear(); studio.update(expected)

    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    path.write_text(text[:match.start(2)] + encoded + text[match.end(2):], encoding="utf-8")
    return True, True


def main():
    eligible = changed = 0
    for directory in (ROOT / "dist", ROOT / "dist-platform"):
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.html")):
            has_org, was_changed = normalize(path)
            eligible += int(has_org); changed += int(was_changed)
    if not eligible:
        raise SystemExit("No Organization-bearing generated HTML found")
    print(f"Canonical legal entity schema projected into {changed}/{eligible} generated pages")

if __name__ == "__main__":
    main()
