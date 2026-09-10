# HIPStudio master platform architecture

Status: implementation baseline, review-only. No deployment, DNS or indexing authorization.

## Canonical product decision

`880rzz/HIPSTUDIO` is the source of truth for the future `https://www.hipstudio.hu` website.

The current Wix site is a migration/reference source only: it remains useful for content comparison, legacy URL discovery and cutover verification, but it is not the long-term source of truth and must not drive new platform architecture after migration.

HIPStudio is the master brand and `hipstudio.hu` is the master domain. HelloÜzlet is retired and may be used only as a legacy migration/equity source. It must never reappear as the master brand, site name, canonical entity or production metadata.

## Goal

A single HIPStudio platform organizes the three commercial pillars without blurring legal or professional responsibility:

1. **HIPStudio Business / Operations** — finance/admin coordination, controlling, operational support and AI/process automation within explicitly approved responsibility boundaries.
2. **HIPStudio Creative** — video, photography, podcast, employer branding, executive communication and Content Engine, building on HIPStudio's documented heritage.
3. **Flúgos by HIPStudio / Experiences** — corporate experience design, team and leadership programmes, employer/client experience and custom game/program formats. Historical Flúgos material remains separately qualified.

The platform promise remains: **„Több idő a cégedre. Kevesebb idő a működtetésére.”**

## Brand and entity architecture

The code represents one master digital platform while keeping factual entity boundaries explicit.

- **HIPStudio** is the master brand and master website identity.
- **HIPStudio Business** and **HIPStudio Creative** are service pillars of the master platform, not automatically separate legal entities.
- **Flúgos by HIPStudio** is a specialist commercial pillar/brand with a separate infrastructure boundary for `flugos.hu`; that separate Vercel deployment must not become a duplicate SEO corpus or second master content platform.
- **HelloÜzlet** is retired. Its remaining domain/search equity is handled only through controlled migration records.
- Schema.org ownership, `parentOrganization`, `subOrganization`, contracting-party or regulated-responsibility relations are emitted only when supported by approved evidence.

## Information architecture

Language roots: `/hu/`, `/en/`, `/de/`.

Primary platform routes include:

- `/[lang]/` — HIPStudio master platform home
- localized Business / Operations pillar
- localized HIPStudio Creative pillar
- localized Flúgos / Experiences pillar
- localized About / operating-model page
- localized Contact and guided quote-request paths
- localized AI Trust page
- localized Privacy page
- solution families and governed service inventory pages

Detailed service and solution pages belong to the same HIPStudio master platform and inherit its canonical entity, language and trust architecture.

## Customer journey

`Problem → Pillar → Solution → Evidence → Consultation / brief → Quote → Project or retainer → relevant cross-pillar extension`

The homepage leads with executive/business problems rather than a raw service catalogue: leadership time, operational fragmentation, financial visibility, inconsistent communication, capacity constraints and AI/digitalization uncertainty.

## SEO / GEO / Schema / LLM architecture

Every indexable production page must have exactly one coherent search/entity contract:

- one H1;
- unique title and useful description;
- self-referencing canonical on `https://www.hipstudio.hu`;
- reciprocal HU/EN/DE hreflang plus Hungarian `x-default` where applicable;
- visible content aligned with Schema.org claims;
- stable HIPStudio Organization/WebSite identifiers;
- evidence-backed Person, service, relationship and historical claims;
- machine-readable `entity.json`, `provenance.json` and `llms.txt` as projections of the same factual source layer, never substitutes for visible HTML;
- no unsupported rating, award, customer, outcome, ownership or regulated-professional claim;
- FAQ structured data only when the same Q&A is visibly present on the page.

Review builds remain `noindex,nofollow`. Production indexing is a separate release decision after canonical-domain, redirect, live-QA and publication gates pass.

## GDPR / privacy / AI Trust architecture

Hipstudió Kft. is the approved data controller. Németh Tímea is the owner/managing director and human privacy contact, not the controller in her individual capacity.

Privacy follows data minimization and deny-by-default behavior:

- no analytics, marketing or external media request before an explicitly approved integration and consent path;
- no public pricing unless commercial policy explicitly changes;
- guided quote data is limited to information needed for triage and preparation;
- retention, processors, complaint rights and human review are stated in localized privacy content;
- no significant solely automated decision-making in the quote workflow;
- AI-assisted workflows require human control and must not create unsupported public claims.

## Technical strategy

The **future production artifact is the unified HIPStudio platform currently generated into `dist-platform/`**. This is the canonical forward path.

The older HIPStudio `dist/` build is now a **temporary migration baseline/test fixture**, retained only while it protects content coverage, legacy-route reconciliation and regression comparison. It must not become a second production website.

First-principles end state after cutover validation:

1. one canonical source-of-truth repository: `880rzz/HIPSTUDIO`;
2. one canonical HIPStudio production render path;
3. one master canonical domain: `https://www.hipstudio.hu`;
4. legacy Wix/old-build information retained only where it provides migration evidence, redirects or archived reference value;
5. CI invariants prevent brand/entity/canonical/privacy drift;
6. deployment, DNS and indexing remain separate controlled actions.

The production platform remains deliberately lean:

- static HTML/CSS/JS where possible;
- zero unnecessary runtime dependencies;
- local assets and no Wix hotlinks;
- no remote font dependency;
- no automatic third-party media request;
- review mode fail-closed for indexing and quote submission;
- production mode blocked unless release gates are satisfied.

## Cutover principle

Do not migrate by visually copying Wix. Migrate the useful information, search equity and user journeys into the cleaner source architecture, verify equivalence, then retire the redundant implementation.

Sequence:

`repository truth → green CI → review-safe GitHub Pages evidence → live quote E2E → legacy URL reconciliation → DNS/canonical cutover → live browser/SEO/security audit → indexing authorization → legacy Wix retirement`

## Not authorized by this document

- DNS/domain mutation;
- production publication;
- Wix deletion;
- blanket redirects;
- analytics/marketing activation;
- search-engine indexing;
- invented customer results, testimonials, awards or partnerships;
- unsupported legal/entity relationships.
