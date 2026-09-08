# HIPStudio strategic architecture review

Date: 2026-09-08. This review continues the existing static HIPStudio implementation; it does not replace the project.

## Preserved and verified

- Static HU/EN/DE generation, localized routes, reciprocal canonical and hreflang annotations.
- A single Schema.org graph on each page: Organization/ProfessionalService, WebSite, WebPage, BreadcrumbList, ContactPoint, Person, Service, ImageObject and visible FAQPage.
- HIPStudio entity `Q138482177` and founder `Q56391118` are linked from Wikidata. The current Wix legal notice and Wikidata both support the 2006-02-27 founding date and Bánhalmi Norbert’s founder role.
- No analytics, marketing cookies, remote fonts, automatic video loading, iframe, form submission, or automatic external request in the review build.
- CSP, safe DOM rendering, no Offer or review schema, HUF price invariants, content provenance manifests, production approval gates, true local 404 and redirect plan.
- Responsive images, local WebP variants, no gallery layout shift in the last measured gallery test, and WCAG-oriented semantic HTML, keyboard operation and visible focus handling.

## Targeted changes in this revision

- 2006 is visible on the home page and emitted as `foundingDate` in the entity graph.
- The brand is presented as an agency with a multi-disciplinary professional team. Services do not attribute delivery to either named professional.
- Bánhalmi Norbert appears as founder and professional partner; Speier Vikó as professional partner. The legal notice’s separation of independent entities is retained.
- The public Wix client/partner logo set is locally copied with a source and checksum manifest. It is labelled as historical/public reference only: no current engagement, endorsement or performance claim is inferred.
- The work gallery preserves image ALT text for assistive technology but uses only a discreet `© HIPStudio` visible caption. Exact duplicate source files are displayed once across categories; a regression test enforces this.
- The visual system uses a compact sticky header, white/black/grey palette with gold accent, Apple-platform system font stack and an Impact wordmark. Apple SF Pro is not embedded: Apple’s current font license limits use outside designated Apple-platform UI mock-ups.

## Open gates

- Legal review must name the production hosting provider, processor list, retention periods, transfer safeguards, contact workflow and cookie changes before an indexable release. The current privacy page deliberately marks these as review items.
- Seven approved gallery items are unavailable from their source URL and 20 creative/composite items await provenance classification. They are excluded from the build.
- Studio rental conditions, actual HTTP 301/410 infrastructure, live-domain verification and a separate publishing/DNS authorization remain open.
- A future HIPStudio / Business / Flúgos master-brand connection has no verified legal entity, URL, service boundary or consent record in this source set. The current architecture therefore keeps the namespace separate and avoids invented cross-brand claims. A future integration should add verified entity IDs, ownership/contracting relationships, consented cross-links and distinct schema IDs before any navigation or shared conversion flow is added.

## Source record

- Current Wix legal notice: `audit/raw/revision/impresszum.html`.
- Current Wix partner page and 90 public logo assets: `audit/raw/revision/partnereink.html`, `audit/client-logo-manifest.json`.
- Wikidata entity snapshot: `audit/raw/revision/wikidata-hipstudio.json`.
- Wayback returned a 2018 HIPStudio home snapshot. It identifies HIPStudio as a creative professional photography studio but did not yield safely reusable detailed service copy. Neither `banhalmi.art` nor the user-provided `banhlami.art` spelling returned an archived snapshot for the checked dates.
