# HIPStudio production readiness audit

Audit date: 2026-09-08  
Repository: `880rzz/HIPSTUDIO`  
Pull request: `#1`  
Branch: `codex/hipstudio-static-migration`

## 1. Executive summary

The current static migration is technically ready for review and can be merged into `main` as an **unpublished production candidate**. Merge, deploy and indexing are separate decisions. The review build remains `noindex`, contains no deployment workflow or `CNAME`, and the production build still stops unless its explicit approval gates are satisfied.

No P0 or P1 code defect remains after this audit. Two validation gaps were fixed: CI now runs the locked QA dependencies, HTML validation and browser QA; tests now exercise the synthetic production robots/sitemap/index contract, redirect-chain rules, provenance hashes and consent rejection/change behavior.

Production cutover is not ready. Legal/privacy inputs, unresolved media classification, production hosting and edge behavior, security response headers, canonical domain/TLS/DNS verification, and explicit publication authorization remain unresolved. These are release dependencies rather than reasons to prevent an unpublished merge.

**Final recommendation: C. READY TO MERGE AS UNPUBLISHED PRODUCTION CANDIDATE.**

## 2. Current PR status

- Review output: 159 localized pages, 40 legacy HTML aliases and a real local 404 response.
- Languages: HU, EN and DE with reciprocal alternates and Hungarian `x-default`.
- Content: 32 service pages, 5 solution families, 2 named expert profiles and an evidence-gated empty case-study collection.
- Runtime: static HTML/CSS, local responsive images, consent module and pricing calculator. There is no server application, contact form, analytics, marketing tag or automatic external media embed.
- Release state: draft PR; no active deployment, domain configuration or DNS change.
- Real production gates: `legal=false`, `publication=false`, `domainAndDns=false`, `studioRentalTerms=false`; 27 media items remain in `audit/pending-images.json`.

## 3. Verified implementation

| Area | Result | Evidence and limit |
|---|---|---|
| Build and route generation | PASS | `tools/build.py` produced 159 localized pages and 40 aliases. Static tests enumerate every generated route. |
| HU/EN/DE variants | PASS | Every generated page has exactly one language, title and H1. Internal localized targets resolve. |
| Canonical/hreflang | PASS | Every page has its own canonical plus reciprocal HU/EN/DE and HU `x-default`; project-path generation is tested separately. |
| Review indexing | PASS | Review pages emit `noindex,nofollow`; review `robots.txt` disallows crawling and the review sitemap has no URLs. |
| Production indexing contract | PASS WITH RELEASE DEPENDENCY | A synthetic, isolated build with test-only open gates emits `index,follow`, an allow rule and all 159 sitemap URLs. Real production remains blocked. |
| Schema.org JSON-LD | PASS | One parseable graph per page; stable Organization, WebSite, ContactPoint and Person IDs; unique node IDs; visible FAQ text matches FAQPage nodes; no Offer or rating claims. |
| Wikidata references | PASS | HIPStudio `Q138482177` and Bánhalmi Norbert `Q56391118` are source-backed and mirrored in visible trust content. |
| Services and solutions | PASS | Services remain capability pages; solutions state audience, decision context, approach and related capabilities. |
| People pages | PASS | Bánhalmi Norbert is identified as founder/professional partner and Speier Vikó as professional partner. No employment or contracting status is inferred. |
| Case studies | PASS WITH RELEASE DEPENDENCY | JSON Schema and rendering template require evidence; zero case items are published because none is approved. |
| Entity/GEO/LLM records | PASS | `entity.json`, `provenance.json` and `llms.txt` are generated. Material facts also appear in visible HTML. |
| Provenance | PASS | Every declared source path exists; generated public source records include SHA-256 hashes. Historical logos are qualified and do not imply a current engagement. |
| 404 | PASS WITH RELEASE DEPENDENCY | Local server returns HTTP 404 and the page has usable localized links. Public hosting behavior requires live verification. |
| Redirect mapping | PASS WITH RELEASE DEPENDENCY | 40 unique old paths; no self-loop or chain; every entry explicitly records current HTML 200 fallback versus planned HTTP 301. Edge rules are inactive. |
| Images | PASS WITH RELEASE DEPENDENCY | Local responsive WebP variants include dimensions and assistive ALT. Exact cross-category duplicates are suppressed. Twenty-seven excluded media items remain unresolved. |
| Video | PASS | Video references are ordinary external links; no iframe or automatic Wix/CDN request occurs. |
| Pricing | PASS | Sixteen scenarios and all 22 net/VAT/gross invariants pass; approved gross totals and 27% VAT handling are unchanged. |
| Consent and privacy defaults | PASS | Necessary-only default; analytics, marketing and external media are false. Apply, reject/reset and subscription paths work. No cookie, localStorage or sessionStorage entry is created. |
| Contact data collection | PASS | There is no HTML form or newsletter flow. Contact is by explicit email/telephone link; sensitive data is discouraged in the first message. |
| Network behavior | PASS | Browser audit recorded no automatic external request. The calculator fetches only same-origin `pricing.json`. |
| CSP and DOM safety | PASS WITH RELEASE DEPENDENCY | Meta CSP restricts scripts/styles/images/connect/frame/object/form action; content and JSON-LD are escaped. Production response headers require the selected hosting/edge layer. |
| Accessibility | PASS | Semantic checks, keyboard interactions and 191 browser samples passed with zero axe WCAG 2.2 AA findings. This is not a legal certification or substitute for final manual/live review. |
| Performance | PASS WITH RELEASE DEPENDENCY | Local Lighthouse: performance 98–100, accessibility 100, best practices 100; TBT 0 and CLS 0. Cache/TLS/CDN behavior requires live hosting tests. |
| CI | PASS | Locked install, build, 14 static tests, pricing, HTML validation and full browser QA run on pull requests. Workflow has read-only contents permission and no deployment step. |

## 4. Code defects found

No functional defect was found in the generated routes, metadata, schema, pricing, consent, media loading or browser behavior. The first clean-checkout CI run did expose one provenance portability defect: three manifest entries referenced gitignored local snapshots, so their generated checksums were absent outside the audit workstation.

Two release-validation gaps were identified:

1. CI did not install the locked development dependencies and therefore did not run HTML validation or browser QA.
2. Critical production-output and privacy behaviors lacked direct regression coverage: allowed production robots/sitemap/index output, redirect chains/loops, public provenance checksums, and browser-level consent reset/storage state.
3. Three provenance entries depended on local ignored snapshots instead of a versioned extraction record.

## 5. Fixes applied

- `.github/workflows/validate.yml`: added `npm ci`, HTML validation, Chromium installation, local preview and browser QA. Deployment permissions and actions remain absent.
- `tools/test.py`: added isolated synthetic production-output assertions, redirect loop/chain assertions and provenance checksum assertions.
- `tools/browser-qa.mjs`: added consent default, preference change, rejection/reset, localStorage and sessionStorage assertions.
- `audit/entity-source-records.json` and `content/provenance.json`: preserved the relevant extracted facts, source URLs and original snapshot hashes in the repository, removing the clean-checkout dependency on ignored raw files.
- Refreshed local browser and Lighthouse evidence after the changes.

## 6. Remaining P0 blockers

| ID | Category | Severity | Affected feature/file | Exact reason | Codex autonomous? | Required evidence/input | Blocks merge | Blocks production deploy | Blocks indexing |
|---|---|---:|---|---|---|---|---|---|---|
| LEG-01 | C | P0 | Legal/privacy pages; `content/approvals.json` | Production privacy facts and legal review are incomplete; `legal=false`. | No | Approved controller/contact workflow, purposes/legal bases, recipients/processors, email/hosting details, retention, data-subject process and transfer safeguards where applicable. | No | Yes | Yes |
| MED-01 | D | P0 | `audit/pending-images.json` | 20 creative/composite items await classification and 7 approved-source files are unavailable. The production build explicitly adds `mediaReview` while this list is non-empty. | No | Item-level provenance/usage decision; replacement source files or explicit exclusion approval. | No | Yes | Yes |
| INF-01 | B | P0 | Hosting and response headers | No production hosting provider or final origin behavior is approved. Meta CSP cannot provide `frame-ancestors`, HSTS or all response protections. | Partly, after selection | Hosting decision, processor/legal record, staging URL, TLS and header readback. | No | Yes | Yes |
| INF-02 | B | P0 | `audit/url-mapping.json`, `ops/` | GitHub Pages HTML fallbacks return 200 and are not production 301/410 rules. The required edge layer is intentionally inactive. | Partly, after authorization | Approved edge platform; staging rules; status/Location crawl showing no loops or chains. | No | Yes for cutover | Yes for cutover |
| PUB-01 | F | P0 | `content/approvals.json` | Explicit publication authorization is false. | No | Separate user publication approval after reviewable production evidence. | No | Yes | Yes |
| PUB-02 | F | P0 | Canonical origin, TLS and DNS | Final www/non-www, HTTPS, certificate and DNS routing have not been changed or verified. | Partly, after authorization | Approved canonical host and DNS plan; live TLS/DNS/redirect evidence. | No | Yes for cutover | Yes |

## 7. Remaining P1 blockers

| ID | Category | Severity | Affected feature/file | Exact reason | Codex autonomous? | Required evidence/input | Blocks merge | Blocks production deploy | Blocks indexing |
|---|---|---:|---|---|---|---|---|---|---|
| LEG-02 | C | P1 | Privacy configuration | The software has a place for future integrations, but no real processor, retention or AI-processing configuration can be completed before those services are selected. | No | Final production service inventory and reviewed disclosures. | No | Yes if such integrations are enabled | Yes if disclosure is incomplete |
| INF-03 | B | P1 | Monitoring and cache policy | Public cache headers, uptime/error monitoring and log access depend on the production platform. | Partly | Hosting configuration plus staging/live measurements and responsible contact. | No | Yes for cutover | No |
| BUS-01 | E | P1 | Studio page; `studioRentalTerms=false` | Standalone rental terms are not verified. The current page safely avoids a bookable rental offer. | No | Approved availability, scope, contracting party and pricing, or a decision to keep the current enquiry-only wording. | No | No | No |
| BUS-02 | E | P1 | Future master-brand architecture | HIPStudio / Business / Flúgos legal, ownership, service and consent relationships remain unverified and therefore are not represented. | No | Verified entity identifiers and approved relationships before cross-brand integration. | No | No for current standalone site | No |
| QA-01 | B/F | P1 | Public release verification | Current browser and Lighthouse evidence is local; it cannot prove public caching, edge headers, form/mail delivery, redirects or exact deployed SHA. | Partly | Live URL after authorized deploy; independent public readback. | No | No for staging; yes for final cutover | Yes |

No P2 item is required to merge or cut over. Local Lighthouse improvement opportunities such as image-byte reduction and route-specific CSS may be considered later; current measured performance is 98–100 and no regression justifies changing the stable architecture now.

## 8. Legal/privacy inputs required

This is a software-readiness list, not a legal compliance conclusion:

- Confirm the production operator/controller details and privacy contact.
- Identify the production hosting provider, email provider and any edge/CDN provider, including roles and relevant contractual records.
- Provide reviewed purposes and legal bases for contact correspondence, production logs, portfolio media and any later analytics/external-media use.
- Provide access controls and retention/deletion periods for email, technical logs and project media.
- Identify recipients, subprocessors and international transfers; provide the applicable safeguards where relevant.
- Confirm the data-subject request workflow and responsible person.
- Decide whether future AI-assisted processing occurs on visitor or client data; if it does, add the actual system, purpose, data categories, human review and provider information through the existing disclosure/configuration location.
- Keep newsletter consent separate if a newsletter is ever introduced. No newsletter or web form exists now.
- Obtain an explicit legal-content approval before setting `legal=true`.

The consent architecture supports necessary-only default, preference change and rejection. Future analytics or marketing code must register behind this layer and receive a browser-network regression test before activation.

## 9. Media/content inputs required

- Classify the 20 creative/composite images in `audit/pending-images.json` with item-level source and usage status.
- Supply recoverable source files for the 7 unavailable items or explicitly approve their permanent exclusion.
- Keep case studies empty until each claim, client identity if named, quotation, result and media right has explicit evidence.
- Do not convert historical logo display into a claim of current engagement or endorsement.
- Decide the studio-rental wording after verified business terms are available.

## 10. Infrastructure inputs required

- Select and legally review production hosting and any edge/CDN provider.
- Define the canonical host (`www` or apex), TLS coverage and HTTP-to-HTTPS behavior.
- Implement the reviewed 301/410 map at the HTTP layer; do not use the current HTML aliases as a substitute.
- Configure and read back production security headers, including header-level CSP with `frame-ancestors`, `X-Content-Type-Options`, permissions policy and HSTS only after HTTPS/domain validation.
- Define cache policy, deployment identity evidence, monitoring, logging access and rollback ownership.
- Verify Search Console ownership only after the final canonical domain is active.

## 11. Merge readiness

**READY**, as an unpublished production candidate.

Reasons:

- No P0/P1 code blocker remains.
- CI is read-only and has no deploy job.
- Review output is noindex and the real production build remains gated.
- Legal, media, publication and DNS dependencies are explicit and preserved.

Merging does not authorize deployment, indexing, DNS changes or Wix removal. PR #1 remains draft until a human chooses to mark it Ready for Review.

## 12. Deploy readiness

**NOT READY.** LEG-01, MED-01, INF-01, INF-02 and PUB-01 remain P0 for a production cutover. A private/staging deployment would still require an approved host and access/indexing controls.

## 13. Indexing readiness

**NOT READY.** Production legal/media approvals, canonical domain, TLS/DNS behavior, real redirects and live structured-data/robots/sitemap verification are unresolved. The current review build correctly prevents indexing.

## 14. Cutover checklist

### Before staging

- [ ] Approve hosting/edge providers and record privacy roles.
- [ ] Close legal/privacy inputs and set `legal=true` only after documented review.
- [ ] Resolve or explicitly exclude every pending media item.
- [ ] Approve the final canonical host and URL base.
- [ ] Freeze and re-crawl the Wix URL inventory.
- [ ] Reconcile all old paths and approve any true 410 entries.
- [ ] Prepare edge security headers, cache rules and exact 301/410 rules.

### Staging validation

- [ ] Build the exact candidate SHA in production mode without bypassing repository gates.
- [ ] Verify TLS, host normalization and HTTP-to-HTTPS behavior.
- [ ] Crawl every sitemap URL, canonical and reciprocal hreflang.
- [ ] Validate the visible content against the JSON-LD graph and test structured data with current public tools.
- [ ] Verify 301 status and `Location` for every old URL; verify 410 only for approved removals.
- [ ] Prove no redirect loops, chains, blanket home redirects or cross-brand destinations.
- [ ] Read back CSP and all security response headers.
- [ ] Run full browser QA, accessibility checks and Lighthouse/PageSpeed against staging.
- [ ] Verify no external analytics/marketing request before consent; test accept, reject, change and withdrawal if an integration is added.
- [ ] Verify actual contact email delivery and handling workflow; no web form currently exists.
- [ ] Confirm robots and access controls keep staging out of public indexing.
- [ ] Record the deployed commit SHA and artifact checksum.

### Authorized production cutover

- [ ] Obtain separate publication and DNS authorization.
- [ ] Capture the current Wix/DNS configuration and rollback values.
- [ ] Keep Wix available during the agreed rollback window.
- [ ] Deploy the already-tested immutable artifact.
- [ ] Apply TLS/DNS and edge rules without changing unapproved services.
- [ ] Confirm canonical host, HTTP-to-HTTPS and www/apex redirects.
- [ ] Confirm production `robots.txt`, `sitemap.xml`, canonical tags and indexability.
- [ ] Submit the final sitemap and verify Search Console ownership.
- [ ] Run public structured-data validation and live Lighthouse/PageSpeed.
- [ ] Re-crawl the old inventory and new sitemap from outside the hosting network.
- [ ] Verify contact delivery, consent-sensitive network behavior and monitoring alerts.
- [ ] Record exact live SHA, DNS answers, headers and timestamps.

## 15. Rollback requirements

- Preserve the pre-cutover Wix site, DNS records, TTL values and screenshots/exports of relevant settings.
- Define one owner and one decision threshold for rollback.
- Keep the previous DNS/edge routing ready for restoration during the rollback window.
- Roll back on TLS failure, widespread 5xx/404, canonical-host loop, broken contact delivery, unsafe consent behavior, missing critical media or material accessibility regression.
- After rollback, verify Wix availability, DNS propagation, TLS, robots/canonical behavior and old critical URLs from the public internet.
- Do not delete Wix or irreversible source material as part of cutover or rollback.

## 16. Final recommendation

**C. READY TO MERGE AS UNPUBLISHED PRODUCTION CANDIDATE.**

PR #1 may be marked Ready for Review and, after human review, merged into `main` without publishing. Production deploy and indexing must remain blocked until the P0 release dependencies have documentary and live technical evidence. This audit does not authorize publication, merge, DNS changes or removal of Wix.
