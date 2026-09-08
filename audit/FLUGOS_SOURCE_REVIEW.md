# Flúgos source review and migration direction

Audit date: 2026-09-08

Status: source review for the unified platform. This document does not authorize publication, legal-entity linkage or transfer of historical claims as current claims.

## Verified public sources

1. Current public Flúgos page: `https://www.flugos.hu/flugos-futam`
2. Public 10-year anniversary PDF: `https://www.flugos.hu/_files/ugd/279667_282489bc8248449db8288b358ac8342e.pdf`
3. Historical 2019 rules PDF: `https://www.flugos.hu/_files/ugd/279667_048f98564e214407aa70b03dc824a35b.pdf`
4. Wix account context: site `50216226-28c4-44ce-bdef-734cdfaef0b0`, published Wix site `https://flugos.wixsite.com/flugos-futam`.

## Source-backed historical facts suitable for qualified use

The current public Flúgos page and anniversary PDF support the following as historical statements:

- the concept began in 2009;
- 10 charity car rallies were organised;
- 2 Night Race 4U events were organised;
- a KÖKI Terminál mall race was organised;
- the brand reports numerous corporate team-building programmes;
- the source reports more than 1000 participants and hundreds of donations/offerings;
- the project historically supported organisations working with children;
- the game model uses location discovery, clues and tasks that may test strength, speed, creativity or problem solving;
- the anniversary PDF describes a later game series combining conventional team-building elements with extreme, creative and problem-solving tasks and states potential application in sales, promotion, retention and customer acquisition contexts.

These facts must be presented with historical/time-qualified language. They must not be transformed into current annual volume, current client count, current CSR commitments or guaranteed business outcomes.

## Historical/archive-only material

The 2019 public event content includes dated event details, fees, capacity, accommodation and rules. These are historical and must not be reused as current commercial conditions.

The 2019 rules PDF identifies the organiser for that historical event. It does not by itself establish the current contracting party for new corporate services. Current legal/contracting entity must therefore remain an approval-gated field.

## Recommended migration architecture

### Current specialist positioning

**Flúgos — Corporate Experience Design**

Business use cases:

- Team Experience
- Leadership Experience
- Employer Experience
- Client Experience
- Custom corporate programme
- Custom Branded Game

This positioning is an extension of the source-backed team-building/game methodology into the approved business strategy. Specific deliverables, prices, guarantees and outcomes require separate evidence.

### Archive strategy

The 2009–2019 Flúgos Futam history should be retained as heritage/proof, not as the primary current sales proposition.

Suggested new structure:

- `/experiences/` — current B2B proposition
- `/experiences/team-experience/`
- `/experiences/leadership-experience/`
- `/experiences/employer-experience/`
- `/experiences/client-experience/`
- `/experiences/custom-game/`
- `/experiences/history/` — 2009 onward brand/game history
- `/archive/flugos-futam-2019/` — dated event content if retained for historical value

Production URL structure will be decided only after the master-domain and canonical-domain strategy is approved.

## Claims that require approval/evidence before production

- current trademark status and exact protected classes/territories;
- current legal owner/operator/contracting party;
- current team size;
- current event capacity;
- current prices;
- current named customers;
- current participant totals beyond source-qualified historical statements;
- performance or business-outcome claims;
- current charity programme commitments;
- cross-brand ownership or legal relationship with HIPStudio or HelloÜzlet.

## Integration rule

Flúgos may be presented visually and commercially as the Experience pillar of the unified customer journey, but Schema.org ownership, `parentOrganization`, `subOrganization`, legal contracting statements and shared privacy/controller claims remain prohibited until independently verified and approved.
