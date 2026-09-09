# HIPStudio production readiness

## Current state

The repository is a production candidate, not a live release. The master brand, three-pillar architecture, multilingual routes, evidence governance, Business responsibility guardrails, quote flow, SEO structure and browser QA are implemented in review mode.

The rule is simple: green CI means the code behaved. It does not mean DNS should suddenly develop courage and move itself.

## Ready in the repository

- HIPStudio master brand and `https://www.hipstudio.hu` target master domain.
- HU / EN / DE platform and service architecture.
- Business, Creative and Flúgos by HIPStudio pillars.
- Five flagship solutions with fit, scope, process, guardrails and guided quote paths.
- No public pricing.
- Evidence-gated client/result/testimonial claims.
- Business provider/responsibility matrix covering every Business service.
- Review-safe legacy URL decision matrix; no blanket redirects.
- Guided quote-request frontend and deterministic human-reviewed routing backend.
- Canonical/hreflang/schema structure.
- HTML validation and Playwright browser QA.
- Review builds remain `noindex,nofollow`.

## External gates before production

1. **Privacy and legal approval** — confirm controller identity, privacy notice, lawful basis, retention, processors/subprocessors and the exact contracting-party model.
2. **Quote E2E verification** — test the real browser submission against the Apps Script deployment and verify Sheet write, internal mail, customer confirmation, Reply-To and `info@hipstudio.hu` Send-As behavior.
3. **Legacy URL inventory** — obtain authoritative URL exports/crawls for HelloÜzlet and Flúgos. Current evidence is not complete enough for domain-wide redirect activation.
4. **Production hosting** — choose the host and verify TLS, canonical host, cache/security headers, real 301/410 behavior and rollback procedure.
5. **Staging acceptance** — run the release candidate on the chosen host before changing DNS.
6. **DNS cutover** — connect `hipstudio.hu` only after the previous gates pass.
7. **Indexing** — only after cutover: remove review noindex, publish the production sitemap, verify canonicals/redirects and then enable search-engine discovery.

## Copy standard

Public copy should sound like a capable human specialist, not a committee, a legal robot or an AI brochure. Short sentences are preferred where they improve clarity. Jargon is used only when it helps the buyer make a decision. Small moments of wit are allowed, but never where they could weaken trust around finance, privacy, legal responsibility or measurable claims.

## Non-negotiable safeguards

- No invented client, testimonial, result, award, partnership or current-provider claim.
- No guaranteed savings, grant success, compliance, reach, lead or revenue result.
- No regulated professional responsibility without named and verified responsibility evidence.
- No public price list unless the commercial policy is explicitly changed later.
- No blind redirect of historical Flúgos material to a current sales page.
- Merge is not deploy. Deploy is not DNS. DNS is not indexing. Keeping those four separate is cheaper than learning the distinction during an outage.

The machine-readable source of truth is `content/release-gates.json`.
