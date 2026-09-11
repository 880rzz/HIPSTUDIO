# HIPStudio autonomous build brief

This repository is the source of truth for the new HIPStudio master site. Work from first principles: remove ambiguity, reduce friction, preserve evidence, and make every design and content decision earn its place.

## Mission

Take the current review build to a domain-ready `hipstudio.hu` release. Do not stop at visual polish. Audit the complete information architecture, service inventory, messaging, evidence, responsive behavior, accessibility, performance, privacy, and release gates. The final site must explain, in plain human language, which customer pain point each offer solves, what the proven solution is, why HIPStudio is credible, how flexible delivery can be, and what the next action is.

## Non-negotiable release rule

Do not recommend attaching `hipstudio.hu` until ALL of these are true:
- every CI/release gate is green;
- responsive QA passes at 320, 390, 768, 1440 and 1920 widths;
- WCAG AA automated checks are green on representative and full-route review sets;
- no horizontal overflow, broken images, missing H1s, external Wix hotlinks, exposed internal emails, accidental cookies/storage, or production-only actions in review mode;
- the Pages review artifact is noindex and uses the `/HIPSTUDIO/` project prefix correctly;
- navigation, language switching, quote-request flows and focus/keyboard behavior work;
- all factual claims, dates, client/reference claims, partner relationships, image credits and historical claims have evidence or are explicitly qualified;
- domain cutover instructions are documented and reversible.

Never change DNS, the production domain, live Wix, or activate quote sending without explicit user approval.

## Design doctrine: deliberately avoid the generic AI look

Research current design discussions before major visual work. Treat these as banned defaults unless there is a specific reason and a human-designed variation:
- centered hero + generic headline + one CTA;
- three equal rounded cards in a row;
- purple/blue SaaS gradients;
- glassmorphism on every surface;
- excessive glow blobs;
- identical border radii everywhere;
- default Inter-like typography with no typographic hierarchy;
- repetitive section rhythm;
- gratuitous fade-up animations;
- decorative whitespace with no narrative purpose;
- generic stock imagery;
- empty marketing adjectives such as innovative, complex, cutting-edge, premium or tailored without proof.

Use concrete design decisions instead of adjective prompts. Define and enforce typography scale, spacing rhythm, image aspect ratios, corner language, surface hierarchy, grid behavior, motion rules, and color roles. The visual system should feel editorial, cinematic and crafted rather than like a SaaS template.

Brand direction: white / warm ivory, navy, restrained gold. Gradients are allowed, but must be art-directed and quiet. Prefer asymmetry, editorial image crops, large real photography/video, confident negative space, varied composition, and a small number of memorable visual gestures. Keep motion restrained and respect `prefers-reduced-motion`.

The requested navigation direction is a full-screen hamburger menu on desktop and mobile, with categories plus short human descriptions of what each area contains. It must be keyboard accessible, focus trapped, ESC-closeable, and screen-reader coherent.

The requested hero direction is full-bleed HIPStudio video with local/self-hosted assets, poster fallback, `autoplay muted loop playsinline`, dark art-directed overlay, and reduced-motion fallback. Never hotlink Wix assets in production output.

## Content doctrine: /human

Write for an intelligent buyer who has no patience for agency jargon. Prefer short, concrete statements that answer:
1. What problem is this for?
2. What do you actually do?
3. What changes for the client?
4. Why should they believe it?
5. What can be adapted?
6. What is the next step?

Use first-principles simplification as the audit lens. If a service exists only because it historically existed, challenge it. If two services solve the same pain point, consolidate or clearly differentiate them. If a service has no proof, owner, process, delivery boundary or buyer use case, do not overclaim it.

Organize offers around buyer problems and outcomes first; service mechanics second. Examples of pain-point framing:
- "We need credible content but cannot coordinate five suppliers." → integrated photo/video/podcast/content production with one coordination layer.
- "Our leadership lacks a clear operational picture." → business-operations / finance-admin / reporting support within explicitly approved responsibility boundaries.
- "Our internal event needs to feel intentional, not generic." → designed corporate experience with scoped logistics/content/production.

Do not imply legal identity between HIPStudio Kft., BANHALMI/Bánhalmi Norbert, Speier Vikó or other independent entities. The contracting party must remain clear.

## Evidence and provenance

Before publishing a claim, classify it as one of:
- VERIFIED: supported by an authoritative company page, contractual/internal source already in repo, reputable third-party source, or reproducible repository evidence;
- QUALIFIED: plausible but not independently confirmed; phrase cautiously;
- REMOVE: unsupported marketing claim.

Maintain or extend an evidence/reference layer in the repo for factual claims.

Known authoritative starting points to verify against current web evidence include:
- current `hipstudio.hu` pages and legal/impressum data;
- repository migration/audit documents;
- historical HIPStudio pages and archived/current service pages;
- public third-party mentions where provenance is clear.

Search for HIPStudio mentions, historical references, event/client mentions, press, partner pages, image bylines and credits. Do not use a client logo, testimonial, event photo, portrait, or project image unless usage/provenance is defensible. Record image source URL, original author/photographer if known, license/permission status if known, subject/project context, and whether a visible credit is required.

Do not treat search-engine image captions as proof of rights. Prefer original publisher/source pages. If copyright status is unclear, flag the asset rather than publishing it.

## Media strategy

The site currently needs more visual density. Build a real media inventory before filling gaps with generated or stock visuals.

Priority order:
1. authentic HIPStudio-owned historical/current photography and video;
2. client/project imagery with verified permission/credit;
3. partner imagery with verified permission/credit;
4. commissioned/generative decorative visuals only when they do not falsely imply real clients, people, events or facilities.

Use real imagery to break long text sections. Avoid a wall of cards. Alternate full-bleed media, editorial split layouts, compact proof blocks, process strips, selected case evidence, and strong CTA moments.

## Information architecture audit

Audit every current route and service. Produce a pain-point → solution → evidence → CTA map. Remove duplicate or confusing routes. Preserve SEO-relevant legacy intent with redirects/migration mappings where justified.

The master brand is HIPStudio. The rationale for consolidation should be explained simply: the combined capabilities allow clients to solve broader problems with fewer suppliers and less coordination overhead, while specialist expertise remains explicit.

Flúgos remains a specialist entry-domain/infrastructure boundary unless explicitly changed by the user.

## Implementation discipline

Do not hand-edit generated HTML if a source generator/content file exists. Modify source-of-truth files and rebuild.

Prefer semantic selectors/data attributes in tests rather than assertions tied to marketing copy. Do not weaken real functional, accessibility, privacy or release gates to make CI green.

After each meaningful batch:
1. build;
2. run static tests;
3. run HTML/privacy/hosting/release gates;
4. run browser QA;
5. run platform browser/WCAG QA;
6. inspect the review artifact;
7. only then commit.

Keep review quote submission disabled until explicit approval.

## Definition of done

The site is ready for domain review only when:
- visual design no longer resembles a default AI/SaaS template;
- real media is integrated with documented provenance/credits;
- buyer pain points and proven solutions are understandable without industry jargon;
- service flexibility is concrete (scope, modularity, locations, formats, team model, integration options) rather than vague;
- every substantive credibility claim is evidence-backed or qualified;
- full-screen navigation and video hero are complete and accessible;
- all three languages are coherent where supported;
- full responsive/browser/WCAG QA is green;
- Pages review is manually inspected on desktop and mobile;
- production readiness and rollback/cutover steps are current.

When these conditions are met, report exactly what was verified, what remains a business/legal approval, and whether `hipstudio.hu` can safely be pointed to the new build. Do not declare domain-ready while any critical gate or provenance issue remains open.
