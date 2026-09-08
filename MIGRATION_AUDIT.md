# HIPStudio — migrációs audit

2026-09-07. READ → AUDIT, az implementáció előtt. Cél: 880rzz/HIPSTUDIO, a felhasználó megerősítette. Forrás: https://www.hipstudio.hu/. A 29 sitemap URL élő HTML-je, metaadatai és SHA-256 lenyomatai: audit/source-inventory.json. A teljes HTML-pillanatképek helyben: audit/raw/. A nyilvános megjelenés nem bizonyít képújraközlési engedélyt.

## Megállapítások

| Terület | Besorolás | Bizonyíték és döntés |
|---|---|---|
| Árak | bizonyított hiba | Az aktoldal törzsszövegében 119990 HUF, booking kártyáján 139990 HUF; társkereső 69990/84990; portfólió 99990/139990. Forrás: muveszi-aktfotozas-budapest, portfolio-fotozas-budapest, fotozas-arak-idopontfoglalas. Nem választunk önkényesen árat. |
| BANHALMI árazás | manuális-jogi jóváhagyást igényel | pricing-huf.json: EUR-ból 400-as tervezési árfolyam, 20% áfa, nem kötelező ajánlat. HIPStudio szolgáltatási/adózási azonosság nem bizonyított. Csak HUF jóváhagyási lista, nincs új konverzió vagy Offer. |
| Entitás | fejlesztési lehetőség | Főoldal: öt JSON-LD blokk, ismételt Organization/WebSite és azonos organization @id eltérő adatokkal. A duplikáció önmagában nem minden esetben hiba. Egy forráskövethető gráf készül. |
| SEO | fejlesztési lehetőség | A 29 sitemap URL mindegyikén van cím és canonical. A két rendezvényoldal canonicalje azonos. Célzott régi→új mapping szükséges. |
| Nyelvek | fejlesztési lehetőség | A 29 rögzített HTML-ben nincs link[hreflang]. Valós HU/EN/DE fájlok és kölcsönös alternatívák készülnek. |
| Robots/sitemap | fejlesztési lehetőség | A publikus Wix sitemapindex 21 tartalmi és 8 booking URL-t fed le. A booking funkció kiesik, a szolgáltatási szándék megőrizhető. |
| H1 | fejlesztési lehetőség | Impresszum: 16 H1; főoldal/podcast/kapcsolat/portfólió/video referencia: nincs H1 a mentett HTML-ben. Ez önmagában nem bizonyít WCAG-sértést. Rendezett címsorhierarchia készül. |
| ALT | manuális-jogi jóváhagyást igényel | Reklámgaléria: 25 üres ALT; videóreferencia: 18. Vizuális ellenőrzés szükséges az informatív/dekoratív szerep megállapításához. ALT nem készül fájlnévből. |
| LLM/GEO | fejlesztési lehetőség | A törzsszöveg a HTML-ből kiolvasható. A galériák szövege szegényes. A videó/podcast oldalak forrást nem nevező statisztikái nem kerülnek át. |
| GDPR/impresszum | manuális-jogi jóváhagyást igényel | A 2026-09-05-ös impresszum tartalmaz cégnév/székhely/adószám/cégjegyzékszám adatokat. Megőrzési idők, szolgáltatói lista, adattovábbítás és GitHub tárhelyszerepek felülvizsgálandók az új működéshez. |
| Cookie | manuális-jogi jóváhagyást igényel | HTML-ből a Wix consent tényleges hálózati működése nem bizonyított. Az új build analitika, külső font, külső kép és iframe nélkül készül; hálózati QA szükséges. |
| AI Trust | fejlesztési lehetőség | Az impresszumban már van AI Trust fejezet. A migráció megtartja az entitások különállását; nincs AI-certifikáció vagy garantált keresési helyezés. |
| Partnerek | manuális-jogi jóváhagyást igényel | A két fő fotós partner megnevezését a felhasználó kérte, a Wix JSON-LD is megerősíti. Ez nem tulajdonosi/alkalmazotti viszony. További partnernév/logó nem kerül ki engedély nélkül. |
| Létszám | manuális-jogi jóváhagyást igényel | Felhasználói adat: több mint 20 fotós. Wix törzsszöveg: 20. A 20+ felhasználói állításként követhető, a legnagyobb csapat és 3000 rendezvény állítását nem visszük tovább. |
| Fotók | manuális-jogi jóváhagyást igényel | Publikus portfólió eredet bizonyítható; szerzői/model release engedély nem következik belőle. Képjegyzék és publikációs kapu készül. AI/stock helyettesítés nincs. |
| Szolgáltatási hiányok | manuális-jogi jóváhagyást igényel | Executive portré, C-level esemény, vizuális pozicionálás, brand-fotó és önálló stúdióbérlés nem szerepel önállóan igazolt Wix ajánlatként. Tartalmi jóváhagyási listán maradnak; nem készül kitalált kínálat. |

## ARCHITECT

- Standard-library Python generátor, statikus HTML, egy kanonikus CSS, nincs Wix SDK/Bookings vagy alkalmazásszerver.
- Valós /hu/, /en/, /de/ útvonalak. Review: noindex. Production: explicit jóváhagyási kapu. A review nem indexelhető éles kiadás.
- Régi URL-ek: célhivatkozásos statikus átirányító HTML. Valódi HTTP 301/410 és egyedi válaszfejlécek külön infrastruktúrát igényelnek; HTML nem színleli ezeket.
- Email/telefon és árajánlatkérési útmutató, automatikus üzenetküldés nélkül.
- Egyedi szolgáltatási tartalom; a még nem bizonyított kínálat az auditban marad.

## Források

- https://www.hipstudio.hu/sitemap.xml és https://www.hipstudio.hu/robots.txt
- https://www.hipstudio.hu/impresszum
- https://github.com/880rzz/BANHALMI/blob/c3bc1143254a467cb8d47091e84acc2aac361ebc/pricing-huf.json
- https://github.com/880rzz/BANHALMI/blob/c3bc1143254a467cb8d47091e84acc2aac361ebc/pricing-guide.json
- https://www.wikidata.org/wiki/Q138482177
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://eur-lex.europa.eu/eli/reg/2016/679/oj — jogi keret, nem megfelelőségi tanúsítás.

## Közzétételi korlát

Publikálás, DNS-módosítás és Wix-törlés külön jóváhagyás nélkül tilos. A teszt/build/browser/performance/review eredmények a dokumentum végén következnek.

## Implementáció és lezárt döntések — 2026-09-07

A fenti táblázat az implementáció előtti állapotot őrzi. Az alábbi döntések felülírják a korábbi „jóváhagyást igényel” ár- és képjogi állapotot:

- A célrepo a felhasználó által megerősített `880rzz/HIPSTUDIO`. A BANHALMI forrás külön, olvasási célú checkoutja `c3bc1143254a467cb8d47091e84acc2aac361ebc` commiton készült.
- A felhasználó megerősítette a fotósi és szereplői engedélyek rendelkezésre állását a nyilvános referenciaanyag átvételéhez. Az engedélyt `content/approvals.json` és a képjegyzék rögzíti; nem a nyilvános URL-ből következtettünk rá.
- A magasabb Wix-összegek nettók: akt 139 990, társkereső 84 990, portfólió 139 990 HUF. Ezekhez 27% áfa adódik. A BANHALMI-kalkulátor átvett HUF-végösszege változatlan, belső bontása 27%-os: `nettó = round(bruttó / 1,27)`, `áfa = bruttó − nettó`. Egész forintos, half-up kerekítés; nincs új EUR-konverzió.
- 32 szolgáltatás, mindhárom nyelven. A felhasználó által kért executive/brand/C-level irányokat a BANHALMI-forrás és a brief támasztja alá. A Wix-oldalon közvetlenül hivatkozott 24 oldalas bemutatkozó PDF igazolja a további rendezvény-, greenbox-, helyszíni nyomtatási, sport-, koncert- és streaming szolgáltatási irányokat. A PDF történeti létszám-, évszám- és ügyfélállításai nem kerültek át aktuális tényként.
- Az önálló stúdióbérlés díja, mérete, felszerelése és minimum időtartama még nem igazolt. Az oldal az igazolt címet és egyeztetési lehetőséget közli; nem tartalmaz kitalált bérleti ajánlatot. Célzott kérdés kiküldve a felhasználónak.
- Az induló HTML-pillanatkép 116 képet tartalmazott. A Wix galériametadata 221-et jelzett. A böngészős görgetés nem töltötte be mindet; a felhasználó csatlakoztatott Wix-fiókjának dokumentált, csak olvasó Pro Gallery API-ja feloldotta a lapozást. A galériaazonosítók a publikus oldalból származnak. Teljes darabszám: portré 30, portfólió 51, ingatlan 46, reklám 78, művészi akt 16.
- 18 referenciafilm és 1 showreel közvetlen, HTTP 200-zal ellenőrzött médiacíme bekerült. Külső automatikus letöltés nincs; kattintással nyílnak meg. A videóhoszting továbbra is Wix CDN-függőség, ezért a Wix törlése/médiaeltávolítása nem része ennek az átadásnak.

## Ellenőrzési bizonyítékok

- `npm run build`: 126 nyelvi oldal, 40 régi útvonal-alias és 404; review üzemmód.
- `npm test`: 10 ellenőrzés sikeres, köztük minden belső link és fragment, nyelvi metaadatok, látható GYIK/JSON-LD egyezés, képek, HUF-áfabontás, élesítési kapu és GitHub projekt-útvonal.
- `npm run test:pricing`: 16 kalkulátorszcenárió és 22 csomag adóinvariánsa sikeres. Példa: kétfős, kétórás brandfotózás 6 képpel bruttó 358 000 HUF = nettó 281 890 + 76 110 HUF áfa.
- HTML Validate 11.14.0: nulla hibás dokumentum az ellenőrzött buildben.
- Playwright + axe-core: 158 oldalméret-minta (320/390/768/1440/1920 px), minden 126 oldal mobilon; nulla talált axe-sértés, túlcsordulás, JavaScript-hiba, hibás kép, automatikus külső kérés vagy cookie. Billentyűzetes skip-link, mobilmenü, nyelvváltás, GYIK, kalkulátor, régi CV-útvonal és tényleges 404 ellenőrizve. Ez automatizált eredmény; kézi képernyőolvasós, Safari/Firefox és teljes jogi megfelelőségi vizsgálatot nem állítunk.
- Lighthouse 13.4.1: főoldal, üzleti portré és árlista mobilon/asztalon, hat helyi futás. Performance 100, accessibility 100, best practices 100 a mintán. SEO 66–69, mert az átadási változat szándékosan tiltja az indexelést. A noindexet nem távolítottuk el jobb pontszám kedvéért. TBT és CLS a mért mintán 0. Részletes mérés: `audit/lighthouse-summary.json`; nem éles PageSpeed vagy terepi CWV.
- A fejlesztői lockfile feloldásakor npm audit: 0 ismert sérülékenység. Ez nem független mély biztonsági audit.

## Nyitott élesítési tételek

Jogi tartalom (tárhely, megőrzés, adatfeldolgozók, adattovábbítás), stúdióbérlési feltételek, videóhoszting későbbi sorsa, HTTP 301/410 infrastruktúra, külön publikálási és szükség esetén domain/DNS-döntés. A produkciós jóváhagyási kapu aktív. A draft PR, a helyi ellenőrzés és a CI sikere nem jelenti a weboldal publikálását vagy az éles commit visszaellenőrzését.

### Teljes képanyag ellenőrzése

A 221 bejegyzés közül 214 képfájl letölthető. Hét reklámkép eredeti CDN-címe 403-as választ ad (`commercial-52`–`commercial-58`). Az első hiányzó kép tulajdonosi Media Manager letöltési API-ja is `RESOURCE_NOT_FOUND` választ adott; nincs hozzá kitalált vagy helyettesítő kép. Tételes jegyzék: `audit/pending-images.json`.

A 214 letöltött képből 20 (`commercial-59`–`commercial-78`) szürreális/montázsjellegű kreatív anyag. Előállítási módjuk és megnevezésük felhasználói tisztázására kérdés készült. Jelenleg 194 vizuálisan ellenőrzött fotó van az aktív képlistában, mindegyik saját HU/EN/DE képleírással. A függőben lévő képek nem kerülnek a `dist` könyvtárba. A teljes fotóátvétel ezért **részleges**, nem késznek nyilvánított tétel; az API-leltár teljessége külön eredmény.

A bővített galéria első mobilos Lighthouse-mérése 87 performance pontot és 0,248 CLS-t mutatott. Az ok egy mobilos `aspect-ratio:auto` felülírás volt, amely elvette a betöltés előtti képméret-foglalást. A felülírást eltávolítottuk az egyetlen CSS-forrásból, a forrásválasztó szélességeket a valódi WebP-méretekhez igazítottuk, az első látható galériaképet prioritással töltjük. A javítás utáni mérés külön kerül rögzítésre.

### Galériajavítás visszamérése

`audit/gallery-lighthouse-final.json`: mobil performance 99, desktop 100; accessibility és best practices mindkettőn 100; CLS 0 mindkét nézetben. Mobil LCP 2,03 s, desktop 0,39 s. A három nyelvi galéria 5 képernyőméreten ismét ellenőrizve: 15 minta, nulla túlcsordulás vagy axe-sértés (`audit/browser-gallery-final.json`). A teljes leltár és a függő képek buildből kizárása külön regressziós tesztet kapott.
