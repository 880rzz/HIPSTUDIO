# HIPStudio domain readiness — evidence pass 03

Status: public-source verification for the unpublished master-site rebuild. This file is not a production approval.

## VERIFIED current service evidence

### Campaign / commercial photography

Source: https://www.hipstudio.hu/reklam-fotozas-budapest

Current public page explicitly offers:
- creative and conservative product photography;
- catalogue photography;
- advertising photography;
- studio and external-location production.

Evidence classification: **VERIFIED service capability** for advertising / product / catalogue photography.

Safe production use:
- may support the `campaign-commerce` buyer solution at the service-capability level;
- may support flexibility claims around studio vs external location.

Do not infer from this page alone:
- integrated multi-channel campaign strategy;
- guaranteed cross-format visual consistency;
- global delivery capability merely from the phrase “the world any point” without a concrete scoped project;
- specific client relationships.

### Property / interior production

Sources:
- https://www.hipstudio.hu/epulet-fotozas-galeria
- https://www.hipstudio.hu/_files/ugd/b0aee1_6a982328d7fb44948c05188d2cd35bec.pdf

Current public evidence supports:
- property and interior photography;
- aerial capture;
- 3D virtual tour production;
- a company presentation stating activity in property photography since 2011.

Evidence classification: **VERIFIED capability**, with the date claim retained only as a source-qualified historical statement until canonical company/brand chronology is fully reconciled.

Safe production use:
- supports the `spaces-experiences` buyer solution for still / aerial / virtual presentation of spaces;
- supports explaining that the technique can vary by the decision problem.

Do not infer:
- architecture/design consultancy;
- venue operations;
- event-experience design;
- ownership of third-party buildings shown in legacy galleries.

### Event production flexibility

Source: https://www.hipstudio.hu/rendezvenyfotozas-budapest

Current public page explicitly describes:
- event photography and video;
- adaptation when the programme changes;
- urgent image selection/retouching for fast publication;
- mobile studio / press-wall portraits;
- short reference-film delivery.

Evidence classification: **VERIFIED service capability**.

Important qualification: the same page also contains historic scale claims such as event counts, team size and “largest team” language. Those claims remain **QUALIFIED / DO NOT REPEAT UNLESS SEPARATELY VERIFIED**.

## Legal / structured-data blocker reproduced

Canonical legal source: `content/legal-controller.json`

Approved registered office:
- 1081 Budapest, Népszínház u. 25. Fe. 2.

Public studio/contact address:
- 1111 Budapest, Lágymányosi utca 15.

Current generator source: `tools/build.py`

The generated `Organization` / `ProfessionalService` JSON-LD currently uses the **studio address** as the organization postal address. This conflicts with the approved legal-controller source of truth and must be fixed before production cutover.

The same generator also currently projects `foundingDate: 2006-02-27` directly onto the combined Organization node. Current public HIPStudio pages are inconsistent about the visible historical date, and the repository already documents the need to keep brand history separate from legal-company identity. Therefore the production schema must not use an unqualified founding date on the legal company until the entity split / chronology is resolved.

Required implementation direction:
1. derive legal-company name, registered office, company identifiers and contact details from `content/legal-controller.json` rather than hardcoding them in `tools/build.py`;
2. keep the public studio location separately identified as a place/contact location rather than replacing the registered office;
3. separate legal Organization, HIPStudio Brand and WebSite identities in structured data;
4. attach historical founding chronology to the correct brand/history entity only when the canonical date is approved;
5. add regression tests that fail if the legal Organization address equals the studio address or if a disputed founding date is projected onto the legal company.

## Current cutover stance

**NO-GO** remains appropriate until at least:
- legal Organization schema uses the registered office source of truth;
- brand/legal/WebSite entity roles are no longer collapsed in generated JSON-LD;
- founding-date conflict is resolved or omitted/qualified;
- hero video is self-hosted with explicit rights/credit basis and poster fallback;
- full-screen accessible hamburger navigation is implemented;
- selected real media has per-asset provenance;
- final responsive/browser/WCAG/release gates are green.
