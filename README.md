# HIPStudio unified business platform

This repository contains two deliberately separated static review builds:

1. **HIPStudio baseline** — the reviewed HU/EN/DE migration of the existing HIPStudio site and its verified service/history layer.
2. **HIPStudio unified platform** — the review-only master platform that connects Business / Operations, HIPStudio Creative and Flúgos Experiences in one customer journey without inventing legal ownership or regulated-service responsibility relationships.

No deployment, DNS change, Wix deletion or production indexing is automated by this repository.

## Master-brand decision

**HIPStudio is the approved master brand. `https://www.hipstudio.hu` is the approved master domain for the unified architecture.**

The repository provenance records support the HIPStudio founding date **2006-02-27**, so the 2026 platform may use a verified 20-year heritage claim.

Core consolidation narrative:

> **20 év tapasztalat. Most egy komplexebb üzleti partnerként.**
>
> **Egy HIPStudio. Három szakmai pillér. Több lehetőség az ügyfélnek.**

The reason for consolidation is customer value, not organisational theatre: fewer suppliers, less coordination and more connected expertise across operations, finance/control, creative communication and corporate experiences.

## Three specialist pillars

- **HIPStudio Business / Operations** — financial administration, payroll/HR administration support, back office, management reporting/controlling, process improvement and AI-readiness/automation preparation. Responsibility-sensitive and regulated scopes remain gated until verified.
- **HIPStudio Creative** — video, photography, podcast, employer branding, executive content and Content Engine, building on HIPStudio's verified 2006 heritage.
- **Flúgos by HIPStudio / Experiences** — team, leadership, employer and client experiences plus custom corporate game/program formats. Historical Flúgos material remains time-qualified and separate from the current B2B offer.

HelloÜzlet is no longer a master-brand candidate. Its domain and any residual recognition are migration assets to be handled later through a controlled redirect/content plan.

## Builds

### HIPStudio baseline

```bash
npm ci
npm run build
npm test
npm run test:pricing
```

Output: `dist/`

### HIPStudio unified platform

```bash
npm run build:platform
npm run test:platform
npm run test:master-brand
npm run test:service-inventory
```

Output: `dist-platform/`

The unified review build currently contains 258 localized HU/EN/DE pages: core platform pages, five flagship solution families, governed service hubs/families, 55 concrete service entries and the guided quote-request layer.

Review output is `noindex,nofollow`, `robots.txt` disallows crawling and the review sitemap contains no public URLs.

## Full validation

```bash
npm run build:all
npm test
npm run test:platform
npm run test:master-brand
npm run test:service-inventory
npm run test:public-quote
npm run test:quote-routing
npm run test:pricing
npm run test:html
```

GitHub Actions additionally runs Playwright/axe browser QA for the HIPStudio baseline and unified platform.

## Source and claim governance

Important records include:

- `content/provenance.json`
- `MIGRATION_AUDIT.md`
- `audit/PRODUCTION_READINESS.md`
- `audit/STRATEGIC_ARCHITECTURE_REVIEW.md`
- `audit/FLUGOS_SOURCE_REVIEW.md`
- `audit/BUSINESS_SOURCE_REVIEW.md`
- `BRAND_CONSOLIDATION.md`

Do not convert a strategic direction into an unsupported production claim. Legal entities, ownership relationships, professional responsibility, regulated-service status, current clients/results, prices, processors, retention periods and cross-brand legal relationships require explicit evidence and approval.

## Production gates

The master-brand decision is complete, but publication approval remains separate. `BUILD_MODE=production` still requires `PLATFORM_PUBLICATION_APPROVED=1`, and quote submission additionally requires a valid HTTPS `QUOTE_FORM_ENDPOINT` plus legal/privacy approval.

DNS cutover, redirects from `hellouzlet.hu` / `flugos.hu`, Wix retirement and search indexing are separate release steps.

**Merge != deploy != DNS cutover != indexing.**
