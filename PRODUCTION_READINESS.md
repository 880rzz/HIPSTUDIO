# HIPStudio production readiness

## Current state

The repository is a production candidate, not a live release. The master brand, three-pillar architecture, multilingual routes, evidence governance, Business responsibility guardrails, quote flow, privacy layer, SEO structure and browser QA are implemented in review mode.

Green CI means the code behaved. It does not mean DNS should suddenly develop courage and move itself.

## Ready in the repository

- HIPStudio master brand and `https://www.hipstudio.hu` target master domain.
- HU / EN / DE platform and service architecture.
- Business, Creative and Flúgos by HIPStudio pillars.
- Five flagship solutions with fit, scope, process, guardrails and guided quote paths.
- No public pricing.
- Evidence-gated client/result/testimonial claims.
- Business provider/responsibility matrix covering every Business service.
- Hipstudió Kft. is the approved data controller.
- Németh Tímea is owner / managing director / human privacy contact, not the controller in her individual capacity.
- BANHALMI privacy structure adapted to HIPStudio: quote purpose, GDPR bases, 12-month unsuccessful-inquiry retention, 90-day default security-log retention, processor disclosure, rights and no significant solely automated decision-making.
- Localized privacy pages: `/hu/adatvedelem/`, `/en/privacy/`, `/de/datenschutz/`.
- Quote pages visibly link their matching privacy notice.
- Review-safe legacy URL decision matrix; no blanket redirects.
- HelloÜzlet recorded as a retired source; no artificial export blocker remains.
- Guided quote-request frontend and deterministic human-reviewed routing backend.
- Canonical/hreflang/schema structure.
- HTML validation and Playwright browser QA.
- Review builds remain `noindex,nofollow`.

## Domain and hosting architecture

- `hipstudio.hu` is the master site and will be connected directly to the static build from repository `880rzz/HIPSTUDIO` through the repository-connected production hosting path.
- `flugos.hu` is not a separate website. It is a specialist entry domain for Flúgos by HIPStudio.
- The intended Flúgos destination is `https://www.hipstudio.hu/hu/vallalati-elmenyek/`.
- The final `flugos.hu` behavior is a real permanent redirect to that HIPStudio Flúgos page after the master site is accepted.
- A separate Flúgos content stack, duplicate SEO site or duplicate quote flow must not be created.

## External gates before production

1. **Quote E2E verification** — test the real browser submission against the Apps Script deployment and verify Sheet write, internal mail, customer confirmation, Reply-To and `info@hipstudio.hu` Send-As behavior.
2. **Flúgos URL inventory** — obtain the authoritative remaining Flúgos URL export/crawl before activating redirects for historical URLs. The root-domain destination is already decided.
3. **Repository-connected hosting acceptance** — serve the release candidate from the repository-connected host and verify TLS, canonical host, cache/security headers, 404 behavior and rollback procedure.
4. **HIPStudio DNS cutover** — connect `hipstudio.hu` only after the previous gates pass.
5. **Flúgos domain cutover** — after HIPStudio is live and accepted, connect `flugos.hu` as a permanent entry redirect to the HIPStudio Flúgos page.
6. **Indexing** — only after cutover: remove review noindex, publish the production sitemap, verify canonicals/redirects and then enable search-engine discovery.

## Copy standard

Public copy should sound like a capable human specialist, not a committee, a legal robot or an AI brochure. Short sentences are preferred where they improve clarity. Jargon is used only when it helps the buyer make a decision. Small moments of wit are allowed, but never where they could weaken trust around finance, privacy, legal responsibility or measurable claims.

## Non-negotiable safeguards

- No invented client, testimonial, result, award, partnership or current-provider claim.
- No guaranteed savings, grant success, compliance, reach, lead or revenue result.
- No regulated professional responsibility without named and verified responsibility evidence.
- No public price list unless the commercial policy is explicitly changed later.
- No blind redirect of historical Flúgos material to a current sales page; only the root entry-domain destination is pre-approved.
- Hipstudió Kft. is the approved data controller; company registration and tax identifiers remain attached to the company, not to Németh Tímea personally.
- `flugos.hu` is an entry domain, not a second site.
- Merge is not deploy. Deploy is not DNS. DNS is not indexing. Keeping those four separate is cheaper than learning the distinction during an outage.

The machine-readable source of truth is `content/release-gates.json`.
