# Biztonság és URL-kezelés

## Elkészült

- Függőségmentes publikus runtime; kizárólag a helyi kalkulátor két ES-modulja fut.
- Szöveges tartalom HTML-escape; JSON-LD `<` escape; nincs user HTML, belső tárolás, automatikus e-mail vagy fizetés.
- CSP meta: self alapértelmezés; JSON-LD tartalomhash; nincs iframe/object, külső script/style/font vagy automatikus külső kép.
- Nincs automatikus deploy workflow, nincs CNAME. Production build jóváhagyás nélkül hibával leáll.
- A régi 29 sitemap-URL és a feltárt booking-calendar/checkout szándékok: url-mapping.json.

## GitHub Pages korlátok és tervezett véglegesítés

A statikus redirect HTML HTTP200 után navigál. Ez nem HTTP301. A 40 alias konkrét tartalomra visz; a booking felület helyett a szolgáltatás/kontakt marad. A 404.html az ismeretlen URL-ekhez készült; a helyi szerver valódi 404 státusszal szolgálja ki, az éles GitHub Pages státusz csak deploy után mérhető.

A források között nem bizonyított olyan megszűnt informatív oldal, amelyet indokolt lenne 410-re tenni. A booking/checkout működés megszűnik, de releváns helyettesítő szolgáltatásoldal létezik: ide 301 a cél. Ha később valóban megszűnt és helyettesítő nélküli URL igazolódik, külön listába kerül, majd jóváhagyott edge réteg ad HTTP410-et. Sem 410-et, sem válaszfejlécet nem színlelünk meta taggel.

Élesítéskor külön jóváhagyott konfigurációs feladat: HTTPS, valódi 301/410 edge szabályok (ha szükséges), Content-Security-Policy válaszfejléc frame-ancestors 'none' értékkel, X-Content-Type-Options: nosniff, Permissions-Policy: camera=(), microphone=(), geolocation=(), HSTS csak ellenőrzött HTTPS/domainkörben. A meta CSP nem tud frame-ancestors vagy HSTS védelmet helyettesíteni. GitHub Pages egyedi header-konfigurációja nem állítható a repóban egy tetszőleges _headers fájllal.

Nincs szükség üres cookie bannerre, mert nincs nem szükséges tracker. Jövőbeli külső videó/analitika csak előzetes, visszavonható hozzájárulás és böngészős hálózati teszt után kerülhet be. A tárhely naplózása ettől független jogi felülvizsgálati tétel.
