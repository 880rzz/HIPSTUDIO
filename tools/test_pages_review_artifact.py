# coding: utf-8
"""Validate the temporary GitHub Pages review artifact before deployment.

Production HTML intentionally uses root-relative URLs for hipstudio.hu. The review
artifact is served below /HIPSTUDIO/, so every local root-relative href/src/action
must be rewritten to that project prefix while production canonicals stay intact.
Every deployed content page must also remain noindex,nofollow.
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

attr_url_re = re.compile(r"\b(?:href|src|action)=[\"']([^\"']*)[\"']", re.I)
tag_attr_re = re.compile(r"([:\w-]+)\s*=\s*[\"']([^\"']*)[\"']", re.I)
meta_tag_re = re.compile(r"<meta\b[^>]*>", re.I)
link_tag_re = re.compile(r"<link\b[^>]*>", re.I)


def attrs(tag):
    return {k.lower(): v for k, v in tag_attr_re.findall(tag)}


errors = []
checked_attrs = 0
canonical_count = 0
content_pages = 0

for path in html_files:
    raw = path.read_text(encoding="utf-8")
    rel = path.relative_to(DIST)

    for value in attr_url_re.findall(raw):
        checked_attrs += 1
        if value.startswith("/") and not value.startswith("//") and not value.startswith(PREFIX):
            errors.append(f"{rel}: unprefixed local URL: {value}")
        if value.lower().startswith("javascript:"):
            errors.append(f"{rel}: javascript URL is not allowed: {value}")

    # index.html at artifact root is a synthetic noindex redirect, not a content page.
    if rel == Path("index.html"):
        continue

    content_pages += 1
    robots = [attrs(tag) for tag in meta_tag_re.findall(raw) if attrs(tag).get("name", "").lower() == "robots"]
    if len(robots) != 1:
        errors.append(f"{rel}: expected exactly one robots meta tag, found {len(robots)}")
    else:
        directives = {x.strip().lower() for x in re.split(r"[,\s]+", robots[0].get("content", "")) if x.strip()}
        if not {"noindex", "nofollow"}.issubset(directives):
            errors.append(f"{rel}: review page must be noindex,nofollow, got {robots[0].get('content', '')!r}")

    canonicals = []
    for tag in link_tag_re.findall(raw):
        a = attrs(tag)
        rel_tokens = {x.strip().lower() for x in a.get("rel", "").split()}
        if "canonical" in rel_tokens:
            canonicals.append(a.get("href", ""))
    canonical_count += len(canonicals)
    if len(canonicals) != 1:
        errors.append(f"{rel}: expected exactly one canonical link, found {len(canonicals)}")
    else:
        canonical = canonicals[0]
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

if canonical_count != content_pages:
    errors.append(f"canonical total mismatch: content_pages={content_pages} canonicals={canonical_count}")

if errors:
    print("GitHub Pages review artifact validation failed:")
    for error in errors[:100]:
        print(f"- {error}")
    if len(errors) > 100:
        print(f"- ... and {len(errors) - 100} more")
    raise SystemExit(1)

print(
    "GitHub Pages review artifact OK: "
    f"html_files={len(html_files)} content_pages={content_pages} attributes={checked_attrs} "
    f"canonicals={canonical_count} prefix={PREFIX}"
)
