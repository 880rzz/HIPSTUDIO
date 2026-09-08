# HIPStudio + unified business platform

This repository contains two deliberately separated static review builds:

1. **HIPStudio baseline** — the reviewed HU/EN/DE HIPStudio migration, merged from PR #1 and preserved as the specialist Creative/Content implementation.
2. **Unified platform** — the review-only Business + HIPStudio + Flúgos architecture that consolidates the three customer journeys without inventing legal ownership relationships.

No deployment, DNS change, Wix deletion or production indexing is automated by this repository.

## Strategic platform model

The approved three-pillar direction is documented in `PLATFORM_ARCHITECTURE.md`.

- **Business / Operations** — financial administration, payroll/HR administration support, back office, management reporting/controlling, process improvement and AI-readiness/automation preparation.
- **Creative / HIPStudio** — video, photography, podcast, employer branding, executive content and Content Engine.
- **Experiences / Flúgos** — team, leadership, employer and client experiences plus custom corporate game/program formats.

Working platform positioning:

> Több idő a cégedre. Kevesebb idő a működtetésére.

`HelloÜzlet` is currently a **working master-brand value**, not a final production brand decision. The unified production build remains blocked unless master-brand and publication approval are explicitly supplied.

## Builds

### HIPStudio baseline

```bash
npm ci
npm run build
npm test
npm run test:pricing
```

Output: `dist/`

### Unified platform

```bash
npm run build:platform
npm run test:platform
```

Output: `dist-platform/`

The current unified review build generates HU/EN/DE core platform pages and the five approved flagship solution families:

- Business Operations 360
- Finance & Control
- AI Readiness & Automation
- Content Engine
- Corporate Experience Design

Review output is `noindex,nofollow`, `robots.txt` disallows crawling and the review sitemap contains no public URLs.

## Full validation

```bash
npm run build:all
npm test
npm run test:platform
npm run test:pricing
npm run test:html
```

GitHub Actions additionally runs Playwright/axe browser QA for the existing HIPStudio build and the unified platform build.

## Source and claim governance

Important source/claim records include:

- `MIGRATION_AUDIT.md`
- `audit/PRODUCTION_READINESS.md`
- `audit/STRATEGIC_ARCHITECTURE_REVIEW.md`
- `audit/FLUGOS_SOURCE_REVIEW.md`
- `audit/BUSINESS_SOURCE_REVIEW.md`

Do not convert a strategic direction into an unsupported production claim. In particular, legal entities, ownership relationships, professional responsibility, regulated-service status, current clients/results, prices, processors, retention periods and cross-brand legal relationships require explicit evidence and approval.

## Production gates

The existing HIPStudio production approvals remain separate from the unified platform approvals.

For the unified platform, `BUILD_MODE=production` alone is insufficient. The generator also requires explicit master-brand and publication approval. This synthetic contract exists for testing; it is not authorization to deploy.

**Merge != deploy != DNS cutover != indexing.**
