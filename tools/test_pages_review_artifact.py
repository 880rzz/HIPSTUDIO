# coding: utf-8
"""Validate the temporary GitHub Pages review artifact before deployment.

Production HTML intentionally uses root-relative URLs for hipstudio.hu. The review
artifact is served below /HIPSTUDIO/, so every local root-relative href/src/action
must be rewritten to that project prefix while production canonicals stay intact.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-pages-review"
PREFIX = "/HIPSTUDIO/"

if not DIST.exists():
    raise SystemExit("dist-pages-review missing; run tools/prepare_pages_review.py first")

html_files = sorted(DIST.rglob("*.html"))
if not html_files:
    raise SystemExit("dist-pages-review contains no HTML files")

attr_re = re.compile(r"\b(?:href|src|action)=[\"']([^\"']*)[\"']", re.I)
canonical_re = re.compile(r"<link\b[^>]*rel=[\"']canonical[\"'][^>]*href=[\"']([^\"']+)[\"']", re.I)

errors = []
checked_attrs = 0
canonical_count = 0

for path in html_files:
    raw = path.read_text(encoding="utf-8")
    rel = path.relative_to(DIST)

    for value in attr_re.findall(raw):
        checked_attrs += 1
        if value.startswith("/") and not value.startswith("//") and not value.startswith(PREFIX):
            errors.append(f"{rel}: unprefixed local URL: {value}")
        if value.lower().startswith("javascript:"):
            errors.append(f"{rel}: javascript URL is not allowed: {value}")

    for canonical in canonical_re.findall(raw):
        canonical_count += 1
        if "/HIPSTUDIO/" in canonical:
            errors.append(f"{rel}: review prefix leaked into canonical: {canonical}")
        if not canonical.startswith("https://www.hipstudio.hu/"):
            errors.append(f"{rel}: unexpected canonical host: {canonical}")

root = DIST / "index.html"
if not root.exists():
    errors.append("review root index.html is missing")
else:
    root_raw = root.read_text(encoding="utf-8")
    required_root = [
        'name="robots" content="noindex,nofollow"',
        "url=/HIPSTUDIO/hu/",
        'href="/HIPSTUDIO/hu/"',
    ]
    for token in required_root:
        if token not in root_raw:
            errors.append(f"review root index.html missing: {token}")

if (DIST / "CNAME").exists():
    errors.append("review artifact must not contain CNAME")

if canonical_count == 0:
    errors.append("no canonical links found in review artifact")

if errors:
    print("GitHub Pages review artifact validation failed:")
    for error in errors[:100]:
        print(f"- {error}")
    if len(errors) > 100:
        print(f"- ... and {len(errors) - 100} more")
    raise SystemExit(1)

print(
    "GitHub Pages review artifact OK: "
    f"html_files={len(html_files)} attributes={checked_attrs} canonicals={canonical_count} prefix={PREFIX}"
)
