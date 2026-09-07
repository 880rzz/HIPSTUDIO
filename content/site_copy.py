# coding: utf-8
from services import tr
UI={k:tr(v) for k,v in {
'home':'Kezdőlap || Home || Startseite',
'services':'Szolgáltatások || Services || Leistungen',
'work':'Munkáink || Our work || Arbeiten',
'prices':'Árak || Pricing || Preise',
'contact':'Kapcsolat || Contact || Kontakt',
'faq':'Gyakori kérdések || Frequently asked questions || Häufige Fragen',
'studio':'A stúdió || The studio || Das Studio',
'partners':'Fotós partnereink || Photography partners || Fotopartner',
'legal':'Impresszum és adatkezelés || Legal notice and privacy || Impressum und Datenschutz',
'cookies':'Cookie-k és külső tartalom || Cookies and external content || Cookies und externe Inhalte',
'cta':'Beszéljünk az elképzelésedről || Let’s talk about your idea || Sprechen wir über deine Idee',
'skip':'Ugrás a tartalomra || Skip to content || Zum Inhalt springen',
'nav':'Fő navigáció || Main navigation || Hauptnavigation',
'lang':'Nyelvválasztás || Language selection || Sprachauswahl',
'menu':'Menü || Menu || Menü',
'read':'Részletek || Explore || Entdecken',
'all':'Összes szolgáltatás || All services || Alle Leistungen',
'goal':'A cél || The aim || Das Ziel',
'brief':'A jó brief itt kezdődik || A good brief starts here || Hier beginnt ein gutes Briefing',
'process':'Így készül || The process || Der Ablauf',
'reference':'Kapcsolódó referenciák || Related references || Passende Referenzen',
'sourceLink':'Eredeti HIPStudio referencia megnyitása || Open the original HIPStudio reference || Originalreferenz von HIPStudio öffnen',
'quote':'Ajánlatot kérek || Request a quote || Angebot anfragen',
'quoteNote':'Az ajánlat a cél, a helyszín, a résztvevők, a felhasználás és a határidő egyeztetése után véglegesíthető. || A quote can be finalised after discussing purpose, location, participants, usage and deadline. || Ein Angebot wird nach Abstimmung von Ziel, Ort, Beteiligten, Nutzung und Termin finalisiert.',
'back':'Vissza a kezdőlapra || Back to home || Zur Startseite',
'notFound':'Ez az oldal nem található. || This page could not be found. || Diese Seite wurde nicht gefunden.',
'notFoundText':'Lehet, hogy a cím megváltozott. A szolgáltatások között vagy a kapcsolat oldalon folytathatod. || The address may have changed. Continue through our services or contact page. || Die Adresse wurde möglicherweise geändert. Über die Leistungen oder Kontaktseite geht es weiter.',
'net':'Nettó || Net || Netto',
'vat':'Áfa (27%) || VAT (27%) || USt. (27%)',
'gross':'Bruttó összesen || Gross total || Brutto gesamt',
'duration':'Időtartam || Duration || Dauer',
'minutes':'perc || minutes || Minuten',
'images':'retusált kép || retouched images || retuschierte Bilder',
'priceNote':'Tájékoztató HUF-árak. A csomag tartalmát, az elérhetőséget, a felhasználási jogokat és a végleges díjat írásos ajánlat rögzíti. || Indicative HUF pricing. Package scope, availability, usage rights and the final fee are recorded in a written quote. || Unverbindliche HUF-Preise. Paketumfang, Verfügbarkeit, Nutzungsrechte und endgültiger Preis werden im schriftlichen Angebot festgehalten.',
'localReview':'Előzetes változat · még nincs közzétéve || Preview · not yet published || Vorschau · noch nicht veröffentlicht',
'galleryNote':'Válogatás a HIPStudio nyilvános portfóliójából. || A selection from HIPStudio’s public portfolio. || Eine Auswahl aus dem öffentlichen Portfolio von HIPStudio.',
'related':'További lehetőségek || Related services || Weitere Möglichkeiten',
'photography':'Fotózás || Photography || Fotografie',
'film':'Film és podcast || Film and podcast || Film und Podcast',
'visualTrust':'Hiteles képek. Érthető jelenlét. || Honest images. A clear presence. || Ehrliche Bilder. Ein klarer Auftritt.',
'homeTitle':'A képen túl. || Beyond the image. || Über das Bild hinaus.',
'homeIntro':'Fotó, film és podcast. Embereknek és márkáknak, akik a saját hangjukon szeretnének megszólalni. Budapest, HIPStudio. || Photography, film and podcast. For people and brands who want to speak in their own voice. Budapest, HIPStudio. || Foto, Film und Podcast. Für Menschen und Marken, die mit eigener Stimme sprechen möchten. Budapest, HIPStudio.',
'homeEditorial':'A figyelemmel kezdődik. || It begins with attention. || Es beginnt mit Aufmerksamkeit.',
'homeBody':'Először megértjük, mit szeretnél megmutatni. Utána választunk hozzá képi nyelvet, helyszínt és formát. Egy portré személyességétől egy rendezvény történetén át egy beszélgetés hangjáig. || First we understand what you want to express. Then we choose the visual language, setting and format. From the intimacy of a portrait to the story of an event and the voice of a conversation. || Zuerst verstehen wir, was du zeigen möchtest. Dann wählen wir Bildsprache, Ort und Format. Von der Persönlichkeit eines Porträts über die Geschichte einer Veranstaltung bis zur Stimme eines Gesprächs.',
'serviceIntro':'Válassz a feladat szerint. A képi megoldást együtt alakítjuk ki. || Start with the task. We shape the visual approach together. || Beginne mit der Aufgabe. Den visuellen Ansatz entwickeln wir gemeinsam.',
'portraitGroup':'Ember és jelenlét || People and presence || Mensch und Präsenz',
'commercialGroup':'Márka és tárgy || Brands and objects || Marke und Objekt',
'artGroup':'Személyes képi világ || Personal expression || Persönlicher Ausdruck',
'spaceGroup':'Tér és építészet || Space and architecture || Raum und Architektur',
'eventGroup':'Esemény és történet || Events and stories || Ereignis und Geschichte',
'filmGroup':'Mozgókép és hang || Film and sound || Bewegtbild und Ton',
'legalReview':'Jogi felülvizsgálat szükséges. || Legal review required. || Rechtliche Prüfung erforderlich.',
'legalIntro':'A cégadatok a HIPStudio nyilvános impresszumából származnak. Az új weboldal adatkezelési működésének véglegesítéséhez az alábbi pontokat felül kell vizsgálni. || Company details come from HIPStudio’s public legal notice. The following items require review before the new website’s privacy arrangements are finalised. || Die Unternehmensdaten stammen aus dem öffentlichen Impressum von HIPStudio. Die folgenden Punkte müssen vor der Finalisierung des Datenschutzes der neuen Website geprüft werden.',
'operator':'Üzemeltető és adatkezelő || Operator and data controller || Betreiber und Verantwortlicher',
'registered':'Székhely || Registered office || Sitz',
'registration':'Cégjegyzékszám || Company registration number || Handelsregisternummer',
'tax':'Adószám || Tax number || Steuernummer',
'court':'Nyilvántartó cégbíróság || Register court || Registergericht',
'legalSource':'A jelenlegi HIPStudio impresszum || Current HIPStudio legal notice || Aktuelles HIPStudio-Impressum',
'privacyContact':'Adatvédelmi megkeresések || Privacy enquiries || Datenschutzanfragen',
'aiTrust':'Átláthatóság és AI Trust || Transparency and AI Trust || Transparenz und AI Trust',
'aiBody':'A fotók a HIPStudio portfóliójából származnak; helyettesítő AI-kép nincs. A szolgáltatási szövegek a nyilvános források szerkesztett változatai. Nem állítunk garantált üzleti eredményt, ügyfélértékelést vagy olyan partneri jogviszonyt, amely nincs igazolva. || Photographs come from the HIPStudio portfolio; there are no substitute AI images. Service texts are edited from public sources. We do not claim guaranteed business results, customer ratings or unverified legal relationships between partners. || Die Fotos stammen aus dem HIPStudio-Portfolio; es gibt keine ersetzenden KI-Bilder. Leistungstexte sind redaktionelle Fassungen öffentlicher Quellen. Wir behaupten keine garantierten Geschäftsergebnisse, Kundenbewertungen oder unbelegten rechtlichen Beziehungen zwischen Partnern.'
}.items()}
ROUTES={'home':tr(' ||  || '),'services':tr('szolgaltatasok || services || leistungen'),'work':tr('munkaink || work || arbeiten'),'prices':tr('arak || pricing || preise'),'contact':tr('kapcsolat || contact || kontakt'),'faq':tr('gyik || faq || fragen'),'studio':tr('studio || studio || studio'),'partners':tr('fotospartnerek || photography-partners || fotopartner'),'legal':tr('impresszum || legal || impressum'),'cookies':tr('cookie-k || cookies || cookies')}
FAQ=[]
def faq(q,a):FAQ.append((tr(q),tr(a)))
faq('Hogyan indul egy fotózás? || How does a photography session begin? || Wie beginnt ein Fotoshooting?', 'Egy beszélgetéssel a célodról, a képek felhasználásáról és a kívánt megjelenésről. A helyszínt, az időtartamot és az átadandó anyagot a megrendelés előtt egyeztetjük. || With a conversation about your goal, how the images will be used and your preferred look. We agree the location, duration and deliverables before the commission. || Mit einem Gespräch über dein Ziel, die Bildnutzung und den gewünschten Auftritt. Ort, Dauer und Ergebnisse stimmen wir vor dem Auftrag ab.')
faq('Headshot vagy üzleti portré kell nekem? || Do I need a headshot or a business portrait? || Brauche ich einen Headshot oder ein Businessporträt?', 'A headshot az arcra összpontosít. Az üzleti portré a környezetből és a testtartásból is többet mutathat. A felület és a bemutatkozás célja alapján érdemes választani. || A headshot focuses on the face. A business portrait can show more of the setting and posture. Choose based on the channel and the purpose of your introduction. || Ein Headshot konzentriert sich auf das Gesicht. Ein Businessporträt kann mehr Umgebung und Körperhaltung zeigen. Die Wahl richtet sich nach Kanal und Zweck des Auftritts.')
faq('Hogyan tervezünk céges vagy rendezvényfotózást? || How do we plan corporate or event photography? || Wie planen wir Unternehmens- oder Eventfotografie?', 'A résztvevők száma, a program, a párhuzamos helyszínek és a szükséges képtípusok adják a kiindulást. Jelezd a kiemelt pillanatokat és a sajtómegjelenés határidejét is. || Participant count, programme, simultaneous locations and required image types are the starting points. Include key moments and press deadlines. || Teilnehmerzahl, Programm, parallele Orte und benötigte Bildarten bilden die Grundlage. Nenne auch Schlüsselmomente und Pressetermine.')
faq('Mit tartalmazhat a videóprodukció? || What can video production include? || Was kann eine Videoproduktion umfassen?', 'Koncepció, forgatókönyv, szervezés, felvétel és utómunka is része lehet. A szereplők, helyszínek, zene, feliratok és filmváltozatok terjedelmét az ajánlatban rögzítjük. || It can include concept, script, planning, recording and post-production. People, locations, music, captions and versions are defined in the quote. || Konzept, Drehbuch, Organisation, Aufnahme und Nachbearbeitung können dazugehören. Personen, Orte, Musik, Untertitel und Versionen werden im Angebot festgelegt.')
faq('Készülhet podcast az irodánkban? || Can a podcast be recorded at our office? || Kann ein Podcast in unserem Büro aufgenommen werden?', 'A HIPStudio mobil stúdiós felvételt is ismertet. A helyszín hangját, a résztvevők számát és a felvételi körülményeket előzetesen egyeztetni kell. || HIPStudio describes mobile studio recording. Room sound, participant count and recording conditions need prior discussion. || HIPStudio beschreibt Aufnahmen mit mobilem Studio. Raumakustik, Personenzahl und Aufnahmebedingungen müssen vorher besprochen werden.')
faq('Hol található a stúdió, és bérelhető-e? || Where is the studio, and can it be rented? || Wo liegt das Studio, und kann man es mieten?', 'A nyilvános stúdiócím: 1111 Budapest, Lágymányosi utca 15. Önálló bérlésre itt nem adunk foglalható ajánlatot; a feltételekről kérj személyes tájékoztatást. || The public studio address is 1111 Budapest, Lágymányosi utca 15. We do not provide a bookable standalone rental offer here; contact us for the conditions. || Die öffentliche Studioadresse lautet 1111 Budapest, Lágymányosi utca 15. Hier gibt es kein direkt buchbares Mietangebot; bitte frage nach den Bedingungen.')
faq('Mi kell egy pontos árajánlathoz? || What do you need for an accurate quote? || Was wird für ein genaues Angebot benötigt?', 'A szolgáltatás, a cél, a helyszín, a résztvevők vagy termékek száma, az átadandó képek/filmek köre, a felhasználás és a határidő. Érzékeny adatot nem kell az első levélhez csatolni. || Service, purpose, location, participant or product count, required images or films, usage and deadline. Sensitive information is not needed in the first email. || Leistung, Ziel, Ort, Personen- oder Produktzahl, benötigte Bilder oder Filme, Nutzung und Termin. Sensible Daten sind in der ersten E-Mail nicht nötig.')
faq('Milyen pénznemben és áfával szerepelnek az árak? || What currency and VAT treatment do prices use? || Welche Währung und Umsatzsteuer gelten?', 'Minden összeg HUF-ban szerepel. Az ártáblák külön mutatják a nettó összeget, a 27%-os áfát és a bruttó végösszeget. A végleges szolgáltatást írásos ajánlat rögzíti. || All amounts are in HUF. Tables show net, 27% VAT and gross total separately. The final service is documented in a written quote. || Alle Beträge sind in HUF angegeben. Tabellen zeigen Netto, 27% Umsatzsteuer und Brutto getrennt. Die endgültige Leistung wird schriftlich angeboten.')
faq('Mikor kapom meg a képeket vagy a filmet? || When will I receive the images or film? || Wann erhalte ich die Bilder oder den Film?', 'A határidő a feladattól és az utómunkától függ. A portréoldal helyszíni képkiválasztást ismertet, de ebből nem következik minden szolgáltatásra azonnali teljes átadás. Az időpontot külön rögzítjük. || Timing depends on the task and post-production. On-site portrait selection does not mean immediate full delivery for every service. We agree the deadline separately. || Der Termin hängt von Aufgabe und Nachbearbeitung ab. Eine Bildauswahl vor Ort bedeutet nicht bei jeder Leistung eine sofortige vollständige Übergabe. Der Termin wird gesondert vereinbart.')
faq('Milyen felhasználási jogot kapok? || What usage rights do I receive? || Welche Nutzungsrechte erhalte ich?', 'A felhasználási célt, a csatornákat és az esetleges továbbadást a megrendelésben kell tisztázni. A képek átadása önmagában nem jelent korlátlan szerzői jogátruházást. || Purpose, channels and any onward sharing must be agreed in the commission. Delivery alone does not transfer unrestricted copyright. || Zweck, Kanäle und eine mögliche Weitergabe müssen im Auftrag geklärt werden. Die Übergabe allein bedeutet keine uneingeschränkte Übertragung des Urheberrechts.')
faq('Kikerülnek a képeim a portfólióba? || Will my images appear in the portfolio? || Werden meine Bilder im Portfolio veröffentlicht?', 'A fotózáson való részvétel nem automatikus marketinghozzájárulás. A referenciafelhasználáshoz megfelelő, külön tisztázott jogalap szükséges. || Taking part is not automatic marketing consent. Reference use requires an appropriate, separately established basis. || Die Teilnahme ist keine automatische Marketingeinwilligung. Referenznutzung benötigt eine geeignete, gesondert geklärte Grundlage.')
faq('Hogyan kérdezhetek az adataim kezeléséről? || How can I ask about my personal data? || Wie kann ich zur Verarbeitung meiner Daten nachfragen?', 'Adatvédelmi kérdéssel az info@hipstudio.hu címen keresheted a céget. Az impresszum tartalmazza az üzemeltető adatait és a felülvizsgálatra váró adatkezelési pontokat. || Contact the company at info@hipstudio.hu with privacy questions. The legal notice contains operator details and privacy items awaiting review. || Datenschutzfragen kannst du an info@hipstudio.hu richten. Das Impressum enthält Betreiberangaben und noch zu prüfende Datenschutzpunkte.')
PROCESS={
'portrait':[tr('Beszélgetés és képi irány || Conversation and visual direction || Gespräch und Bildrichtung'),tr('Fotózás a megbeszélt környezetben || Photography in the agreed setting || Shooting in der vereinbarten Umgebung'),tr('Közös válogatás és egyeztetett utómunka || Joint selection and agreed retouching || Gemeinsame Auswahl und vereinbarte Retusche')],
'commercial':[tr('Cél, felület és koncepció || Purpose, channel and concept || Ziel, Kanal und Konzept'),tr('Produkció és fotózás || Production and photography || Produktion und Fotografie'),tr('Képkiválasztás és színkorrekció || Image selection and colour correction || Bildauswahl und Farbkorrektur')],
'space':[tr('Helyszín és hozzáférés egyeztetése || Agree location and access || Ort und Zugang abstimmen'),tr('A terek és nézetek rögzítése || Capture spaces and viewpoints || Räume und Perspektiven aufnehmen'),tr('Az egyeztetett anyag előkészítése átadásra || Prepare the agreed material for delivery || Vereinbartes Material zur Übergabe vorbereiten')],
'art':[tr('Elképzelések és személyes határok || Ideas and personal boundaries || Vorstellungen und persönliche Grenzen'),tr('Közös alkotás || Creating together || Gemeinsam gestalten'),tr('Képkiválasztás és személyes utómunka || Image selection and individual retouching || Bildauswahl und individuelle Retusche')],
'event':[tr('Program és lefedettség tervezése || Programme and coverage planning || Programm und Abdeckung planen'),tr('Helyszíni együttműködés a szervezőkkel || Work with the organisers on site || Vor Ort mit den Organisatoren zusammenarbeiten'),tr('Válogatás, utómunka és átadás || Selection, editing and delivery || Auswahl, Bearbeitung und Übergabe')],
'film':[tr('Üzenet és szerkesztési terv || Message and editorial plan || Botschaft und redaktioneller Plan'),tr('Előkészítés és felvétel || Preparation and recording || Vorbereitung und Aufnahme'),tr('Szerkesztés és véglegesítés || Editing and finalisation || Schnitt und Fertigstellung')]
}
LEGAL_ITEMS=[tr(t) for t in [
'E-mailes megkeresések: pontos jogalap, hozzáférési kör, levelezési szolgáltató és megőrzési idő. || Email enquiries: exact legal basis, access controls, email provider and retention period. || E-Mail-Anfragen: genaue Rechtsgrundlage, Zugriffsrechte, E-Mail-Anbieter und Aufbewahrungsdauer.',
'GitHub Pages: tárhelyszolgáltatói szerepek, technikai naplók, adattovábbítás és alkalmazandó garanciák. || GitHub Pages: hosting roles, technical logs, data transfers and applicable safeguards. || GitHub Pages: Hostingrollen, technische Protokolle, Datenübermittlungen und geeignete Garantien.',
'Fotó-, videó- és hanganyagok: projektjogalap, szereplői nyilatkozatok, tárolás, átadás és törlés. || Photo, video and audio: project basis, participant releases, storage, delivery and deletion. || Foto, Video und Audio: Projektgrundlage, Freigaben, Speicherung, Übergabe und Löschung.',
'Külső szolgáltatók: tényleges adatfeldolgozói lista, szerződések, fájlátadási csatornák. || External providers: actual processor list, agreements and file delivery channels. || Externe Anbieter: tatsächliche Auftragsverarbeiter, Verträge und Dateiübertragungswege.',
'Magyar és osztrák ügyfelek: alkalmazandó fogyasztóvédelmi, adózási és e-privacy követelmények jogi vizsgálata. || Hungarian and Austrian customers: legal review of applicable consumer, tax and e-privacy requirements. || Ungarische und österreichische Kunden: rechtliche Prüfung der anwendbaren Verbraucher-, Steuer- und E-Privacy-Anforderungen.',
'Érintetti jogok és panaszkezelés: hozzáférés, helyesbítés, törlés, korlátozás, tiltakozás, adathordozhatóság és illetékes hatóság. || Data subject rights and complaints: access, correction, deletion, restriction, objection, portability and competent authority. || Betroffenenrechte und Beschwerden: Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch, Übertragbarkeit und zuständige Behörde.'
]]
