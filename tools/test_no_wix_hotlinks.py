from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRS = [ROOT / "dist", ROOT / "dist-platform"]
PUBLIC_TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".json", ".xml", ".txt", ".svg"}
FORBIDDEN = (
    "static.wixstatic.com",
    "wixstatic.com/media/",
    "static.parastorage.com",
)


def scan_public_output():
    hits = []
    for base in PUBLIC_DIRS:
        if not base.exists():
            raise AssertionError(f"Missing generated public directory: {base.relative_to(ROOT)}")
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in PUBLIC_TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for needle in FORBIDDEN:
                if needle in text:
                    hits.append(f"{path.relative_to(ROOT)} -> {needle}")
    if hits:
        raise AssertionError("Wix/Parastorage hotlinks found in public output:\n" + "\n".join(hits[:50]))


def verify_partner_logos_are_local():
    manifest_path = ROOT / "audit" / "client-logo-manifest.json"
    logo_dir = ROOT / "assets" / "logos"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    missing = []
    for item in manifest:
        logo_id = item["id"]
        matches = list(logo_dir.glob(f"{logo_id}.*"))
        if not matches:
            missing.append(logo_id)
    if missing:
        raise AssertionError(
            "Partner/logo source records without a local GitHub asset: " + ", ".join(missing)
        )


if __name__ == "__main__":
    scan_public_output()
    verify_partner_logos_are_local()
    print("Wix hotlink gate passed: public output is self-hosted and all partner-logo source records have local assets")
