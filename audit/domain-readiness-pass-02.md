# HIPStudio domain readiness — pass 02

Status: evidence/provenance research for the unpublished master-site rebuild. This file is not a production approval.

## Public-source findings

### Founding-date conflict

Current public HIPStudio sources are inconsistent about the brand founding date:

- the current Impresszum states 2006-02-27;
- the current contact page states 2006-03-15.

Production rule: do not emit an unqualified founding date in visible copy or structured data until one canonical date is approved and the public-source inconsistency is resolved. Do not conflate the HIPStudio brand founding date with the later incorporation date of Hipstudió Kft.

Sources:
- https://www.hipstudio.hu/impresszum
- https://www.hipstudio.hu/kapcsolat

### Registered office vs studio

The current Impresszum distinguishes the company registered office from the Budapest studio address. The generator currently uses the studio as the Organization postal address in JSON-LD. This must be corrected from the existing legal-controller source of truth before production.

Source:
- https://www.hipstudio.hu/impresszum
- repository source of truth: `content/legal-controller.json`

## Third-party credit evidence

### Piac&Profit — Ford Mustang article

Source:
- https://piacesprofit.hu/cikkek/teszt/ford-mustang-5-0-v8-convertible-magasrol-tesz-az-eloirasokra.html

Observed credit:
- `Fotó: Tóth László Rudolf HIPStudio.hu`

Classification:
- VERIFIED third-party editorial photo credit;
- useful as historical production evidence;
- does not by itself prove a direct client contract, ownership of the published image, or permission to reuse the article image on the new HIPStudio site.

Recommended relationship type: `third_party_editorial_photo_credit`.

### Vimeo — VI. VW Beach Találkozó (2011)

Source:
- https://vimeo.com/26386522

Observed credit:
- `Foto és video: Flórián Péter | Photographer - HIPStudio.hu`

Classification:
- VERIFIED third-party event photo/video credit;
- supports historical event-production capability;
- does not establish reuse rights for the video or frames.

Recommended relationship type: `third_party_event_photo_video_credit`.

### Vimeo — Black Food Festival 2020

Source:
- https://vimeo.com/480130855

Observed public credit chain:
- HIPStudio is displayed on the item;
- the source explicitly states `Video by: gamosvideo.com`.

Classification:
- VERIFIED third-party credit chain;
- do not represent HIPStudio as sole video producer from this source;
- media reuse remains uncleared.

Recommended relationship type: `third_party_credit_chain`.

### Babafotókiállítás

Source:
- https://polgarnoemi-oldala.hupont.hu/85/babafotokiallitas

Observed statements:
- HIPStudio photographers are named as Elek Anett, Pál Anita, Perényi Dorottya and Bánhalmi Norbert;
- the page states that more than 500 images were made;
- it also states that a making-of film and live stream were produced.

Classification:
- VERIFIED historical third-party project mention for the textual facts above;
- displayed images are not cleared for migration/reuse by this evidence alone.

Recommended relationship type: `historical_project_mention`.

## Relationship-inflation guard

The new site may use these findings only at their supported level:

- credit != client;
- mention != commission;
- event participation != partnership;
- public display != copyright ownership;
- public source != media reuse permission.

## Production impact

Current cutover stance remains **NO-GO** until at minimum:

1. PR #21 review findings are fixed and regression-tested;
2. Organization structured data derives the legal address from the approved legal-controller source of truth;
3. founding-date conflict is resolved or visible/schema copy is qualified;
4. hero video has an approved self-hosted source, poster and rights/credit basis;
5. selected imagery retains per-asset provenance;
6. required CI, responsive, browser and WCAG gates are green.
