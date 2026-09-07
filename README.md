# HIPStudio — statikus HU / EN / DE oldal

Ellenőrizhető migrációs munkapéldány a `880rzz/HIPSTUDIO` repóhoz. **Nincs publikálva.** A Wix-oldal, a domain és a DNS változatlan. A build alapértelmezetten `noindex`; az éles buildet a hiányzó jogi és publikálási jóváhagyás megállítja.

## Helyi indítás

Python 3.9+ és Node.js 22+ szükséges. A HTML-generálásnak nincs külső Python- vagy npm-függősége.

```sh
npm run build
npm test
npm run test:pricing
npm run preview
```

Előnézet: http://127.0.0.1:4173/hu/ — a szerver kizárólag a helyi gépen figyel.

További QA:

```sh
npm ci
npx playwright install chromium
npm run test:html
npm run test:browser
npm run test:lighthouse
```

A böngészős és Lighthouse-vizsgálathoz fusson az előnézeti szerver. Meglévő Chrome használatához állítsd be a `CHROME_PATH` környezeti változót. Az első mérés Google Chrome-mal macOS-en készült; az automatikus eredmény nem teljes kézi WCAG-tanúsítás vagy éles Core Web Vitals-adat.

## Tartalomszerkesztés

- `content/services.json`: 32 szolgáltatás három nyelven; név, slug, bevezető, eredmény, folyamat, forrás.
- `content/site_copy.py`: közös felületi szövegek, útvonalak, GYIK, jogi felülvizsgálati tételek.
- `content/images.json`: helyi képek, eredet, ellenőrzött HU/EN/DE képleírás és engedélyállapot.
- `content/videos.json`: 18 referenciafilm és a showreel, ellenőrzött közvetlen médiacímek. Csak kattintáskor nyílnak meg; a filmek tárhelye továbbra is a Wix CDN.
- `content/pricing.json`: HUF-csomagok és árelemek. BANHALMI bruttó = HIPStudio bruttó; HIPStudio nettó = kerekített bruttó / 1,27. A Wix magasabb, jóváhagyott nettó csomagáraihoz 27% áfa adódik. Nincs devizaváltás.
- `content/approvals.json`: felhasználói jóváhagyások. A jogi és közzétételi mező nem állítható igazra pusztán a tesztek sikere alapján.
- `assets/site.css`: egyetlen közös stílusforrás; a build tartalomhash alapján verziózza.
- `assets/pricing-engine.mjs`: külön tesztelhető árazás; a táblázatok JavaScript nélkül is olvashatók.

A teljes leltár 221 képes: 7 forrásfájl nem tölthető le, 20 kreatív kép besorolása felhasználói válaszra vár. Ezek tételesen az `audit/pending-images.json` fájlban szerepelnek, és kimaradnak a buildből.

A `tools/prepare.py` történeti importáló le van tiltva: felülírná a felülvizsgált JSON-tartalmat. A `services.py`, `extra_services.py`, `image_descriptions.py` a szerkesztési eredetet őrzi; a szolgáltatás- és képlistánál a JSON az aktív forrás.

## Felépítés és korlátok

126 nyelvi oldal, 194 aktív referenciafotó, 19 közvetlen videóhivatkozás, 40 régi útvonalhoz célzott statikus alias és valódi helyi 404. A régi Bookings-oldalak a megfelelő szolgáltatási tájékoztatóhoz vezetnek. Nincs foglalási, fizetési, ügyféladatbázis- vagy automatikus emailküldési funkció. Kapcsolat: email, telefon, árajánlatkérési útmutató.

Minden nyelvi oldal saját URL-t, címet, leírást, canonicalt, kölcsönös hreflangot és forráskövethető Schema.org-gráfot kap. Nincs kitalált értékelés, árfolyam, Offer vagy partner. A képek helyben vannak, a betűk rendszerbetűk; nincs automatikus külső média, analitika vagy marketingcookie.

A GitHub Pages statikus HTML-aliasai HTTP 200 + meta refresh megoldások. **Nem HTTP 301-ek.** A tényleges 301/410 és egyedi biztonsági válaszfejlécek külön infrastruktúrát igényelnek. Lásd `audit/url-mapping.json` és `audit/SECURITY_AND_REDIRECTS.md`.

## Ellenőrzés és későbbi kiadás

Az `audit/` könyvtár tartalmazza a forrásleltárt, URL-mappinget, képeredetet, árjóváhagyást, konkurenciaelemzést és helyi QA-eredményeket. Részletes állapot: [MIGRATION_AUDIT.md](MIGRATION_AUDIT.md).

A `.github/workflows/validate.yml` kizárólag buildet és teszteket futtat; nincs telepítési joga. Az `ops/github-pages.yml.example` inaktív, kézzel indítható későbbi telepítési minta. Aktiválás előtt szükséges a jogi tartalom véglegesítése, a médiahiányok lezárása és a felhasználó külön publikálási döntése. A stúdióbérlés feltételei külön tartalmi hiányként szerepelnek.

Későbbi, jóváhagyott projekt-URL-es build:

```sh
BUILD_MODE=production SITE_URL=https://880rzz.github.io/HIPSTUDIO npm run build
```

Ez jelenleg szándékosan meghiúsul a jóváhagyási kapun. Saját domainhez külön domain/DNS-jóváhagyás kell. Élesítés után külön CI-, böngészős-, indexelési-, átirányítási- és élő commitazonosság-ellenőrzés szükséges; a helyi eredmény ezt nem helyettesíti.
