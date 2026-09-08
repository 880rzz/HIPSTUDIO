# Unified business platform architecture

Status: implementation baseline, review-only. No deployment, DNS or index authorization.

## Goal

Egy közös digitális platformba szervezzük a jelenlegi három üzleti irányt úgy, hogy a szakmai márkaérték ne vesszen el:

1. **Business / Operations** — pénzügy, adminisztráció, bérszámfejtés, controlling, működési támogatás és AI/folyamat-automatizálás.
2. **Creative / HIPStudio** — videó, fotó, podcast, employer branding, vezetői kommunikáció és Content Engine.
3. **Experiences / Flúgos** — vállalati élménytervezés, csapat- és vezetői programok, employer/client experience és egyedi játékformátumok.

A platform fő ígérete: **„Több idő a cégedre. Kevesebb idő a működtetésére.”**

## Márkaarchitektúra

A kód egyetlen platformot épít, de a jogi és tulajdonosi kapcsolatokat nem találja ki.

- A master-brand munkanév jelenleg `HelloÜzlet`; productionben csak külön jóváhagyással használható végleges master brandként.
- HIPStudio külön specialist brand/entity marad.
- Flúgos külön specialist brand marad.
- A három pillér közös navigációban és ügyfélútban jelenhet meg, de Schema.org ownership/subOrganization kapcsolat csak ellenőrzött jogi és szerződéses adatok után kerülhet be.

## Információs architektúra

Nyelvi gyökér: `/hu/`, `/en/`, `/de/`.

Elsődleges platform útvonalak:

- `/[lang]/` — master platform home
- `/[lang]/business/` — Business / Operations pillar
- `/[lang]/creative/` — HIPStudio / Creative pillar
- `/[lang]/experiences/` — Flúgos / Experiences pillar
- `/[lang]/about/` — működési modell és hárompillérű struktúra
- `/[lang]/contact/` — 30 perces konzultáció CTA
- `/[lang]/ai-trust/` — AI használati és emberi kontroll elvek

A részletes HIPStudio szolgáltatási és referenciaoldalak továbbra is a meglévő HIPStudio buildben maradnak, amíg a végleges domain/canonical migráció nincs jóváhagyva.

## Ügyfélút

`Probléma → Pillér → Megoldási csomag → Bizonyíték / referencia → Konzultáció → Ajánlat → Retainer / projekt → cross-sell`

A homepage nem szolgáltatáslistával indul. A vezetői problémára épít:

- kevés vezetői idő;
- szétszórt operáció;
- pénzügyi átláthatatlanság;
- rendszertelen kommunikáció;
- kapacitáshiány;
- digitalizáció/AI implementációs bizonytalanság.

## Kereső- és LLM-architektúra

- Minden indexelhető oldalnak egyértelmű H1, title, description, canonical és hreflang kell.
- A platform build review módban mindig `noindex,nofollow`.
- A master site Schema.org gráf nem állít be nem igazolt legalName, ownership vagy subOrganization kapcsolatot.
- HIPStudio entitáskapcsolat csak a már bizonyított Wikidata és publikus forrásokra támaszkodik.
- Flúgos/Business kapcsolatot a visible HTML üzleti kínálatként mutathatjuk be, de jogi entitáskapcsolatként nem.
- FAQ csak akkor kerül strukturált adatba, ha a kérdés-válasz látható is.
- `llms.txt`/gépileg olvasható összefoglalók nem helyettesítik a látható HTML-t.

## Konverziós modell

Elsődleges CTA: **30 perces üzleti konzultáció**.

Másodlagos CTA-k:

- működési audit;
- kreatív brief;
- csapat/élmény brief.

A production kontakt/adatgyűjtés csak jóváhagyott adatvédelmi workflow után aktiválható.

## Technikai stratégia

A meglévő HIPStudio statikus generátor stabil baseline marad. Az új `tools/build_platform.py` külön `dist-platform/` review buildet készít. Ez szándékosan csökkenti a regressziós kockázatot és lehetővé teszi, hogy a master domain, hosting és redirect döntés később konfigurációként kerüljön rá.

A platform build:

- statikus HTML/CSS;
- HU/EN/DE;
- zero runtime dependency;
- zero tracker;
- zero remote font;
- zero automatic external media request;
- review módban noindex;
- production mód külön approval gate nélkül nem használható.

## Nem része ennek a fázisnak

- DNS vagy domainmódosítás;
- Wix törlés;
- közös jogi entitás kitalálása;
- automatikus CRM/form integráció;
- analytics aktiválás;
- production indexelés;
- ügyféleredmények vagy testimonialok kitalálása.
