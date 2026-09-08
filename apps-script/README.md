# HIPStudio ajánlatkérő — Google Apps Script

Ez a könyvtár a hárompillérű (Business / HIPStudio / Flúgos) ajánlatkérő szerveroldali végpontját és a determinisztikus lead-routing logikát tartalmazza.

## Működés

A publikus űrlap nem számol és nem jelenít meg árat. A beküldött projekt-scope alapján:

1. a rendszer normalizálja és validálja a briefet;
2. a `QuoteRouting.gs` kizárólag operatív triage-javaslatot készít;
3. egy normalizált sor kerül a `HIPStudio - Ajánlatkérések` Google Sheetbe;
4. belső értesítés megy a `nemeth.timea@hipstudio.hu` és `banhalmi.norbert@hipstudio.hu` címekre;
5. az ügyfél automatikus visszaigazolást kap;
6. a központi kapcsolati és Reply-To cím `info@hipstudio.hu`;
7. minden rekord kap egy `response_due_at` időpontot, amely a beérkezéstől számított 24 óra.

A belső címzettek nincsenek benne a publikus JavaScriptben vagy HTML-ben.

## Triage és routing

A routing **nem ügyfélpontozás**. A projekt végrehajtási összetettségét, sürgősségét, brief-teljességét és szükséges szakmai egyeztetéseit jelzi. Nem ad árat, nem utasít el megkeresést, nem fogad el automatikusan projektet és nem nevez ki személyes felelőst.

A fő mezők:

- `queue`: `BUSINESS`, `CREATIVE`, `EXPERIENCE`, `CROSS_PILLAR` vagy `MANUAL_REVIEW`;
- `priority`: `NORMAL`, `HIGH`, `URGENT`;
- `complexity_score`: 0–10 közötti végrehajtási komplexitás;
- `completeness_score`: a brief hasznos kitöltöttségének 0–100-as mutatója;
- `next_action`: emberi következő lépés javaslat;
- `routing_flags`: például cross-border, express, streaming technikai review, drón megvalósíthatóság, felhasználási jogok;
- `owner_suggestion`: jelenleg mindig `MANUAL_ASSIGNMENT`, amíg a tényleges felelősségi körök nincsenek jóváhagyva;
- `routing_version`: a szabálykészlet auditálható verziója.

A routing minden esetben emberi felülvizsgálatot igényel.

## Első telepítés

1. Hozz létre egy Google Apps Script projektet abban a Google Workspace-fiókban, amely jogosult a HIPStudio levelezésére és a lead Sheet kezelésére.
2. Másold be **mindkét** Apps Script fájlt ugyanabba a projektbe:
   - `HIPStudioQuoteRequest.gs`
   - `QuoteRouting.gs`
3. Futtasd kézzel a `runRoutingSelfTest()` függvényt. Ennek hibamentesen `true` értékkel kell lefutnia.
4. Futtasd egyszer kézzel a `setup()` függvényt, és engedélyezd a szükséges Gmail/Sheets jogosultságokat.
5. A `setup()` létrehozza vagy megnyitja a `HIPStudio - Ajánlatkérések` Sheetet, és a Script Properties alatt eltárolja a `SHEET_ID` értéket.
6. Ellenőrizd a logban a Sheet URL-jét, a routing verzióját és azt, hogy az `info@hipstudio.hu` elérhető-e Gmail küldési aliasként.

## Feladó cím

A script mindig `info@hipstudio.hu` Reply-To címet használ. Ha ez a cím a futtató Google-fiókban igazolt Gmail **Send mail as** alias, akkor a script a levelet ebből a címről is próbálja küldeni. Ha nincs ilyen alias, a tényleges From cím a futtató fiók marad, de a válaszok az `info@hipstudio.hu` címre mennek.

Production előtt ezt tényleges levélküldéssel kell ellenőrizni.

## Web App publikálás

A jogi/adatvédelmi jóváhagyás után:

1. Deploy → New deployment → Web app.
2. A végpont a script tulajdonosaként fusson.
3. Az elérés legyen kompatibilis a publikus weboldalról érkező ajánlatkéréssel.
4. A végleges `/exec` URL-t **ne commitold** a repóba.
5. A weboldal production buildjénél környezeti változóként add meg:

```bash
QUOTE_FORM_ENDPOINT="https://script.google.com/macros/s/.../exec"
```

A platform build production módban blokkol, ha ez az endpoint nincs megadva.

## Kötelező live teszt

Élesítés előtt minimum HU / EN / DE nyelven egy-egy tesztajánlatot küldj be, és ellenőrizd:

- létrejön-e pontosan egy Sheet-sor;
- helyes-e a request ID és a 24 órás `response_due_at`;
- a `queue`, `priority`, `complexity_score`, `completeness_score`, `next_action` és `routing_flags` megfelel-e a briefnek;
- az `owner` üres marad-e, amíg ember nem osztja ki;
- mindkét belső címzett megkapja-e a strukturált briefet és a triage-blokkot;
- az ügyfél megkapja-e a visszaigazolást;
- a Reply-To valóban `info@hipstudio.hu`;
- ha konfigurálva van az alias, a From cím is `info@hipstudio.hu`;
- nincs-e böngészős CORS / redirect / Apps Script response probléma;
- ismételt beküldés nem generál-e duplikációt váratlanul;
- a honeypot és a rate limit működik-e.

Ha az Apps Script Web App közvetlen böngészős hívása az éles környezetben CORS vagy redirect problémát okoz, ne kerüljön megkerülésként gyengébb kliensoldali ellenőrzés productionbe. Ilyenkor same-origin proxy réteget kell használni.

## Adatvédelmi release gate

Production előtt külön jóváhagyandó:

- az ajánlatkérés pontos jogalapja és tájékoztató szövege;
- megőrzési idő a Sheetben és a Gmailben;
- a Sheethez és a postaládákhoz hozzáférő személyek köre;
- a Google Workspace adatfeldolgozói szerepe és releváns szerződéses feltételei;
- érintetti joggyakorlás és törlési folyamat;
- a referencia/brief linkek kezelése;
- a leadből CRM-be vagy más rendszerbe történő későbbi továbbítás szabályai;
- a routing szabályok változáskezelése és időszakos emberi felülvizsgálata.

## Biztonsági és működési alapok

- Nincs publikus árkalkuláció.
- Nincs automatikus projektelfogadás vagy elutasítás.
- Nincs automatikus személyes owner-kijelölés.
- Nincs fájlfeltöltés v1-ben; briefhez/referenciához URL adható meg.
- A belső címzettek csak a szerveroldali scriptben szerepelnek.
- A payload mérete korlátozott.
- Honeypot és e-mail alapú rövid idejű rate limit működik.
- A Sheet append ScriptLock alatt történik.
- A teljes normalizált payload és a routing eredmény a `raw_json` mezőben auditálható.
- Deployment URL és bármilyen későbbi secret nem kerülhet a repositoryba.
