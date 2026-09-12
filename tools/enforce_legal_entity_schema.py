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
    org.pop("foundingDate", None)

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
            raise SystemExit(f"Missing generated directory: {directory.name}")
        for path in sorted(directory.rglob("*.html")):
            has_org, was_changed = normalize(path)
            eligible += int(has_org); changed += int(was_changed)
    if not eligible:
        raise SystemExit("No Organization-bearing generated HTML found")
    print(f"Canonical legal entity schema projected into {changed}/{eligible} generated pages")

if __name__ == "__main__":
    main()
