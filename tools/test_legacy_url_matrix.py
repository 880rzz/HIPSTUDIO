# coding: utf-8
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit
import json

R = Path(__file__).resolve().parents[1]
DATA = json.loads((R / 'content/legacy-url-matrix.json').read_text(encoding='utf-8'))


def normalize_url(value):
    value = unquote(value)
    parts = urlsplit(value)
    path = parts.path or '/'
    if path != '/':
        path = path.rstrip('/')
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, '', ''))


assert DATA['version'] == 'legacy-url-matrix-v3'
assert DATA['status'] == 'review_only'
assert DATA['activeRedirects'] is False
assert DATA['masterOrigin'] == 'https://www.hipstudio.hu'
assert set(DATA['inventoryStatus']) == {
    'https://www.hipstudio.hu',
    'https://www.hellouzlet.hu',
    'https://www.flugos.hu',
}

hip = DATA['inventoryStatus']['https://www.hipstudio.hu']
assert hip['complete'] is True
assert hip['mode'] == 'current_sitemap_and_gsc_verified'
assert hip['verified'] == '2026-09-13'
assert hip['sitemapUrl'] == 'https://www.hipstudio.hu/sitemap.xml'
assert hip['sitemapUrlCount'] == 29
assert hip['gscSettledThrough'] == '2026-09-10'
assert hip['discoveryArtifact'] == 'audit/hipstudio-url-discovery-2026-09-13.json'

evidence_path = R / hip['discoveryArtifact']
assert evidence_path.exists(), evidence_path
EVIDENCE = json.loads(evidence_path.read_text(encoding='utf-8'))
assert EVIDENCE['version'] == 'hipstudio-url-discovery-v1'
assert EVIDENCE['capturedAt'] == '2026-09-13'
assert EVIDENCE['property'] == 'sc-domain:hipstudio.hu'
assert EVIDENCE['sitemap']['url'] == hip['sitemapUrl']
assert EVIDENCE['sitemap']['urlCount'] == hip['sitemapUrlCount'] == 29
assert EVIDENCE['gscLandingPages']['settledThrough'] == hip['gscSettledThrough']
assert EVIDENCE['gscLandingPages']['rowCount'] == len(EVIDENCE['gscLandingPages']['urls'])
assert len(EVIDENCE['sitemap']['urls']) == 29

hello = DATA['inventoryStatus']['https://www.hellouzlet.hu']
flugos = DATA['inventoryStatus']['https://www.flugos.hu']
assert hello['complete'] is True
assert hello['mode'] == 'retired_source_unavailable'
assert 'owner confirmed' in hello['reason'].lower()
assert flugos['complete'] is False
assert flugos['mode'] == 'partial_verified_inventory'

allowed = set(DATA['decisionClasses'])
assert allowed == {
    'planned_301',
    'archive_preserve',
    'preserve_until_archive_mirrored',
    'candidate_410_after_review',
    'needs_inventory',
}
entries = DATA['entries']
assert len(entries) >= 36
sources = [x['source'] for x in entries]
assert len(sources) == len(set(sources))
normalized_sources = {normalize_url(source) for source in sources}

# The current sitemap is the authoritative current-route snapshot. Every URL in
# the preserved discovery artifact must have an explicit migration decision.
sitemap_urls = {normalize_url(url) for url in EVIDENCE['sitemap']['urls']}
assert len(sitemap_urls) == 29
assert sitemap_urls <= normalized_sources

# Search Console can surface percent-encoded landing pages. Normalize those and
# require every settled GSC landing page to be represented by the migration map.
gsc_urls = {normalize_url(url) for url in EVIDENCE['gscLandingPages']['urls']}
assert gsc_urls <= normalized_sources

for item in entries:
    assert item['source'].startswith('https://')
    assert item['decision'] in allowed
    assert item['confidence'] in {'low', 'medium', 'high'}
    assert item['activationGate'].strip()
    target = item.get('target')
    if target:
        assert target.startswith('https://www.hipstudio.hu/'), target
        assert normalize_url(target) != normalize_url(item['source']), item
    if item['decision'] == 'planned_301':
        assert target, item
    if item['decision'] == 'candidate_410_after_review':
        gate = item['activationGate'].lower()
        assert 'review' in gate or 'confirm' in gate

by_source = {item['source']: item for item in entries}
assert by_source['https://www.hipstudio.hu/']['target'] == 'https://www.hipstudio.hu/hu/'
assert by_source['https://www.hipstudio.hu/kapcsolat']['target'] == 'https://www.hipstudio.hu/hu/kapcsolat/'
assert by_source['https://www.hipstudio.hu/impresszum']['target'] == 'https://www.hipstudio.hu/hu/adatvedelem/'
assert by_source['https://www.hipstudio.hu/rovidfilm-keszites']['target'].endswith(
    '/hu/szolgaltatasok/hipstudio/video/commercial-brand-film/'
)
assert by_source['https://www.hipstudio.hu/podcast-keszites']['target'].endswith(
    '/hu/szolgaltatasok/hipstudio/podcast-content/video-podcast/'
)
assert by_source['https://www.hipstudio.hu/service-page/cv-önéletrajz-fotózás']['target'].endswith(
    '/hu/szolgaltatasok/hipstudio/photo-portrait/cv-photography/'
)
assert by_source['https://www.hipstudio.hu/service-page/üzleti-kreatív-portréfotózás']['target'].endswith(
    '/hu/szolgaltatasok/hipstudio/photo-portrait/business-portrait/'
)

# Combined Wix portfolio + fashion intent must not be narrowed to portfolio only.
combined = by_source['https://www.hipstudio.hu/service-page/portfólió-és-divatfotózás']
assert combined['target'] == 'https://www.hipstudio.hu/hu/szolgaltatasok/hipstudio/photo-portrait/'
assert 'fashion' in combined['rationale'].lower()

final_event_target = (
    'https://www.hipstudio.hu/hu/szolgaltatasok/hipstudio/'
    'photo-event/event-conference-photography/'
)
assert by_source['https://www.hipstudio.hu/rendezvenyfotozas']['target'] == final_event_target
assert by_source['https://www.hipstudio.hu/rendezvenyfotozas-budapest']['target'] == final_event_target

root_hello = by_source['https://www.hellouzlet.hu/']
assert root_hello['decision'] == 'planned_301'
assert root_hello['sourceType'] == 'retired_html_entrypoint'
assert root_hello['observed'] == 'owner_confirmed_site_retired_2026-09-09'
assert root_hello['target'] == 'https://www.hipstudio.hu/hu/uzleti-mukodes/'
assert 'No full HelloÜzlet export is required' in root_hello['activationGate']

root_flugos = by_source['https://www.flugos.hu/']
assert root_flugos['decision'] == 'planned_301'
assert root_flugos['target'] == 'https://www.hipstudio.hu/hu/vallalati-elmenyek/'
heritage = by_source['https://www.flugos.hu/flugos-futam']
assert heritage['decision'] == 'archive_preserve'
assert heritage['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-heritage/')
pdf_2019 = next(x for x in entries if '048f98564e214407aa70b03dc824a35b.pdf' in x['source'])
assert pdf_2019['decision'] == 'archive_preserve'
assert pdf_2019['target'].endswith('/hu/szolgaltatasok/flugos/history-archive/flugos-futam-2019/')

raw = (R / 'content/legacy-url-matrix.json').read_text(encoding='utf-8').lower()
for forbidden in ['rewrite rule', 'return 301', 'redirect 301', 'netlify.toml', 'vercel.json']:
    assert forbidden not in raw
assert 'export or crawl the full hellouzlet' not in raw

print(
    'Legacy URL migration matrix tests passed: preserved sitemap/GSC evidence fully covered; '
    'combined service intent preserved; HelloÜzlet retired; Flúgos inventory still gated'
)
