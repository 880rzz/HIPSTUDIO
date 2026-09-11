# coding: utf-8
"""Humanize generated HIPStudio platform copy without changing routes or data structure.

This layer intentionally runs after all platform/service/solution generators. It replaces
stiff internal-language phrasing with clearer executive-level language in HU/EN/DE.
It does not alter legal notices, facts, canonical URLs, structured data or service names.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-platform"

REPLACEMENTS = {
    # Hungarian — concise, natural, executive-level
    "Komplexebb üzleti megoldások. Egy 20 éve épülő márkától.": "20 év tapasztalat. Most még többet adunk egy kézből.",
    "A HIPStudio kreatív és kommunikációs alapjára most működési, pénzügyi, digitalizációs és vállalati élménykompetenciákat kapcsolunk. Egy partneri rendszerben segítünk a háttérműködéstől a láthatóságon át az emberek kapcsolódásáig.": "A HIPStudio húsz éve segít cégeknek jól látszani. Ma már abban is segítünk, hogy jobban működjenek. Pénzügy, működés, tartalom és vállalati élmények — átláthatóan, egy helyen.",
    "Egy HIPStudio. Három szakmai pillér. Több lehetőség az ügyfélnek.": "Egy HIPStudio. Több területen ugyanazzal a figyelemmel.",
    "Az ügyfelek üzleti problémái nem különülnek el szolgáltatói dobozokra. A működés, a pénzügyi kontroll, a kommunikáció és az emberek kapcsolódása gyakran ugyanannak a növekedési célnak a része. Ezért a HIPStudio 20 éves kreatív és kommunikációs alapjára egy közös rendszerben építjük rá a Business és a Flúgos kompetenciákat. Így az ügyfél kevesebb beszállítóval, kevesebb koordinációval és több összekapcsolható szakértelemmel dolgozhat.": "Egy cég működése nem különálló feladatokból áll. A pénzügy, a napi működés, a kommunikáció és a csapat ugyanazt az üzleti célt szolgálja. Ezért hoztuk közelebb egymáshoz ezeket a területeket. Kevesebb egyeztetés, tisztább felelősség, több valódi segítség.",
    "Egy partner a céged működéséhez, növekedéséhez és láthatóságához.": "Egy partner, aki érti, hogyan működik a céged.",
    "Három szakmai pillér": "Három terület. Egy közös szemlélet.",
    "Egy HIPStudio rendszer": "Ami összetartja az egészet",
    "Miért egy rendszerben?": "Miért működik jobban együtt?",
    "Fókuszterületek": "Amiben segítünk",
    "Szakmai pillér": "Szakterület",
    "Bizonyíték és felelősség": "Amit állítunk, azért vállaljuk a felelősséget",
    "Nézzük meg, hol tudunk több terhet levenni a cégedről.": "Nézzük meg, miben tudjuk egyszerűbbé tenni a céged működését.",
    "30 perces üzleti konzultáció": "Beszéljünk 30 percet",
    "Működés, pénzügy és vezetői kontroll": "Tisztább működés. Jobb vezetői rálátás.",
    "Külső működési partneri irány KKV-knak: pénzügyi adminisztráció, bér- és HR-adminisztrációs támogatás, back office, controlling, vezetői riporting, folyamatfejlesztés és AI-automatizálási előkészítés. A szabályozott és felelősségi körök élesítés előtt külön jóváhagyást igényelnek.": "Ott segítünk, ahol a napi működés túl sok vezetői időt visz el: pénzügyi és HR-adminisztráció, back office, controlling, riporting, folyamatfejlesztés és jól megválasztott automatizálás. A szabályozott feladatokat csak tisztázott felelősségi körrel vállaljuk.",
    "A háttérműködést mi fogjuk össze. Te a céget vezeted.": "Kevesebb operatív zaj. Több idő a cég vezetésére.",
    "Tartalom üzleti céllal": "Tartalom, aminek üzleti értelme van.",
    "A HIPStudio 2006 óta épített kreatív kompetenciája: videó, fotó, podcast, employer branding és vezetői kommunikáció olyan cégeknek, amelyeknél a tartalom üzleti eszköz.": "2006 óta készítünk fotót, videót és kommunikációs tartalmat cégeknek. Nem azért, hogy több anyag készüljön, hanem hogy jobban érthető, látható és emlékezetes legyen a márka.",
    "Tartalom, amit nem csak megnéznek. Hanem megjegyeznek.": "Tartalom, amit értenek — és megjegyeznek.",
    "Vállalati élmények, amelyek összehozzák az embereket": "Vállalati élmények, amelyek tényleg összehozzák az embereket.",
    "A Flúgos tapasztalati és játéktervezési örökségére épülő B2B irány: csapat-, vezetői-, employer- és ügyfélélmények, egyedi programok és márkázott játékformátumok.": "A Flúgos több mint másfél évtizedes tapasztalatából építünk olyan céges programokat, amelyeknek valódi céljuk van: jobb csapatmunka, erősebb kapcsolatok és emlékezetes közös élmények.",
    "Élménytervezés céges célokra.": "Élmények, amelyeknek céljuk is van.",
    "Elsődleges fókusz: 10–100 fős magyar KKV-k, ahol a tulajdonos vagy ügyvezető még jelentős operatív terhet visz, és nincs minden funkcióra belső szakértői kapacitás.": "Elsősorban 10–100 fős cégekkel dolgozunk, ahol a vezető még túl sok mindent tart kézben, és nem éri meg minden területre külön belső csapatot építeni.",
    "A három pillér nem három külön világ: ugyanannak az üzleti rendszernek más részeit kapcsolja össze — működés, növekedés, láthatóság és kapcsolódás.": "A működés, a tartalom és az emberek nem külön világok. Ha jól kapcsolódnak egymáshoz, a cég egyszerűbben működik és gyorsabban halad.",

    # English — less consulting jargon
    "More integrated business solutions. From a brand built over 20 years.": "20 years of experience. Now with more ways to help your business.",
    "We are extending HIPStudio's creative and communication foundation with operations, finance, digitalisation and corporate-experience capabilities. One partner model can now support the business from back-office operations to visibility and human connection.": "HIPStudio has spent twenty years helping companies communicate clearly. Today we also help them run more smoothly — across operations, finance, content and corporate experiences, with one accountable partner.",
    "One HIPStudio. Three specialist pillars. More capability for the client.": "One HIPStudio. More expertise, working together.",
    "Business problems do not fit into separate supplier boxes. Operations, financial control, communication and human connection are often parts of the same growth objective. We therefore build Business and Flúgos capabilities into one system on top of HIPStudio's 20-year creative and communication foundation. Clients can work with fewer suppliers, less coordination and more connected expertise.": "A business does not run in separate boxes. Finance, operations, communication and people all affect the same result. We bring those areas closer together so clients spend less time coordinating suppliers and more time moving the business forward.",
    "One partner for the operation, growth and visibility of your business.": "One partner who understands how your business works.",
    "Three specialist pillars": "Three areas. One way of working.",
    "One HIPStudio system": "What brings it together",
    "Why one system?": "Why it works better together",
    "Focus areas": "How we can help",
    "Specialist pillar": "Expertise",
    "Let us identify where one connected partner can remove more operational load.": "Let’s see what we can make simpler for your business.",
    "30-minute business consultation": "Talk to us for 30 minutes",
    "Operations, finance and management control": "Clearer operations. Better management visibility.",
    "An external operating-partner direction for SMEs: financial administration, payroll and HR administration support, back office, controlling, management reporting, process improvement and AI automation preparation. Regulated and responsibility-sensitive scopes require separate approval before production.": "We help SMEs reduce the operational load on management: finance and HR administration, back office, controlling, reporting, process improvement and practical automation. Regulated work is only offered with clearly agreed responsibilities.",
    "We coordinate the background operations. You lead the business.": "Less operational noise. More time to lead the business.",
    "Content built for business outcomes": "Content with a clear business purpose.",
    "HIPStudio's creative capability built since 2006: video, photography, podcast, employer branding and executive communication for companies that use content as a business tool.": "Since 2006, we have created photography, video and communication for companies that need to be understood, seen and remembered — not simply produce more content.",
    "Content people do not just watch. They remember it.": "Content people understand — and remember.",
    "Corporate experiences that bring people together": "Corporate experiences that genuinely bring people together.",
    "A B2B direction built on Flúgos experience and game-design heritage: team, leadership, employer and client experiences, custom programmes and branded game formats.": "We use more than fifteen years of Flúgos experience to create corporate programmes with a real purpose: stronger teams, better relationships and memorable shared experiences.",
    "Experience design for business goals.": "Experiences with a purpose.",
    "Primary focus: Hungarian SMEs with 10–100 employees where the owner or managing director still carries significant operational load and not every function has internal expert capacity.": "We mainly work with companies of 10–100 people where management still carries too much of the day-to-day load and building a full internal team for every function would not make sense.",
    "The three pillars are not separate worlds: they connect different parts of the same business system — operations, growth, visibility and connection.": "Operations, content and people are not separate worlds. When they work together, the business becomes easier to run and easier to grow.",

    # German — direct and natural
    "Umfassendere Unternehmenslösungen. Von einer Marke mit 20 Jahren Erfahrung.": "20 Jahre Erfahrung. Heute können wir Unternehmen noch umfassender unterstützen.",
    "Wir erweitern die kreative und kommunikative Basis von HIPStudio um Kompetenzen in Betrieb, Finanzen, Digitalisierung und Corporate Experience. Ein Partnermodell unterstützt Unternehmen vom Backoffice über Sichtbarkeit bis zur Verbindung von Menschen.": "Seit zwanzig Jahren hilft HIPStudio Unternehmen dabei, klar und professionell aufzutreten. Heute unterstützen wir zusätzlich bei Abläufen, Finanzen, Content und Corporate Experiences — mit einem verantwortlichen Partner.",
    "Ein HIPStudio. Drei Fachsäulen. Mehr Möglichkeiten für Kunden.": "Ein HIPStudio. Mehr Kompetenz, die zusammenarbeitet.",
    "Unternehmerische Probleme passen nicht in getrennte Lieferanten-Silos. Betrieb, Finanzkontrolle, Kommunikation und menschliche Verbindung sind oft Teile desselben Wachstumsziels. Deshalb verbinden wir Business- und Flúgos-Kompetenzen mit der 20-jährigen Kreativ- und Kommunikationsbasis von HIPStudio in einem gemeinsamen System. Kunden arbeiten mit weniger Anbietern, weniger Koordination und stärker vernetzter Expertise.": "Ein Unternehmen funktioniert nicht in getrennten Silos. Finanzen, Abläufe, Kommunikation und Menschen beeinflussen dasselbe Ergebnis. Wir bringen diese Bereiche zusammen, damit weniger Zeit für Koordination verloren geht und mehr Zeit für das eigentliche Geschäft bleibt.",
    "Ein Partner für Betrieb, Wachstum und Sichtbarkeit Ihres Unternehmens.": "Ein Partner, der versteht, wie Ihr Unternehmen arbeitet.",
    "Drei Fachsäulen": "Drei Bereiche. Eine gemeinsame Arbeitsweise.",
    "Ein HIPStudio-System": "Was alles verbindet",
    "Warum in einem System?": "Warum es gemeinsam besser funktioniert",
    "Schwerpunkte": "Wobei wir helfen",
    "Fachsäule": "Kompetenzbereich",
    "Finden wir heraus, wo ein vernetzter Partner mehr operative Last übernehmen kann.": "Schauen wir, was wir für Ihr Unternehmen einfacher machen können.",
    "30-minütige Unternehmensberatung": "30 Minuten miteinander sprechen",
    "Betrieb, Finanzen und Managementsteuerung": "Klarere Abläufe. Bessere Übersicht für die Geschäftsführung.",
    "Eine externe Betriebspartner-Richtung für KMU: Finanzadministration, Lohn- und HR-Administrationssupport, Backoffice, Controlling, Management-Reporting, Prozessverbesserung und Vorbereitung von KI-Automatisierung. Regulierte und verantwortungssensitive Leistungsumfänge benötigen vor Veröffentlichung eine gesonderte Freigabe.": "Wir entlasten KMU dort, wo das Tagesgeschäft zu viel Führungszeit bindet: Finanz- und HR-Administration, Backoffice, Controlling, Reporting, Prozessverbesserung und sinnvolle Automatisierung. Regulierte Aufgaben übernehmen wir nur mit klar vereinbarten Verantwortlichkeiten.",
    "Wir bündeln die Hintergrundprozesse. Sie führen das Unternehmen.": "Weniger operativer Lärm. Mehr Zeit für die Führung des Unternehmens.",
    "Content mit geschäftlichem Ziel": "Content mit klarem geschäftlichem Zweck.",
    "Die seit 2006 aufgebaute Kreativkompetenz von HIPStudio: Video, Fotografie, Podcast, Employer Branding und Führungskräftekommunikation für Unternehmen, die Content als Geschäftsinstrument nutzen.": "Seit 2006 produzieren wir Fotografie, Video und Kommunikation für Unternehmen, die verstanden, gesehen und erinnert werden wollen — nicht einfach nur mehr Content brauchen.",
    "Content, den man nicht nur ansieht, sondern behält.": "Content, den Menschen verstehen — und behalten.",
    "Unternehmenserlebnisse, die Menschen zusammenbringen": "Unternehmenserlebnisse, die Menschen wirklich zusammenbringen.",
    "Eine B2B-Richtung auf Basis der Flúgos-Erlebnis- und Spieldesign-Tradition: Team-, Leadership-, Employer- und Kundenerlebnisse, individuelle Programme und gebrandete Spielformate.": "Aus mehr als fünfzehn Jahren Flúgos-Erfahrung entwickeln wir Unternehmensprogramme mit einem klaren Ziel: stärkere Teams, bessere Beziehungen und gemeinsame Erlebnisse, die bleiben.",
    "Experience Design für Unternehmensziele.": "Erlebnisse mit einem klaren Zweck.",
    "Primärer Fokus: ungarische KMU mit 10–100 Mitarbeitenden, bei denen Eigentümer oder Geschäftsführung noch erhebliche operative Last tragen und nicht jede Funktion intern fachlich besetzt ist.": "Wir arbeiten vor allem mit Unternehmen mit 10–100 Mitarbeitenden, bei denen die Geschäftsführung noch zu viel Tagesgeschäft selbst trägt und nicht für jede Aufgabe ein eigenes internes Team sinnvoll ist.",
    "Die drei Säulen sind keine getrennten Welten: Sie verbinden unterschiedliche Teile desselben Unternehmenssystems — Betrieb, Wachstum, Sichtbarkeit und Verbindung.": "Abläufe, Content und Menschen sind keine getrennten Welten. Wenn sie zusammenspielen, lässt sich ein Unternehmen einfacher führen und weiterentwickeln.",
}


def humanize(text: str) -> tuple[str, int]:
    count = 0
    for old, new in REPLACEMENTS.items():
        if old in text:
            occurrences = text.count(old)
            text = text.replace(old, new)
            count += occurrences
    return text, count


def main() -> None:
    if not DIST.exists():
        raise SystemExit("dist-platform does not exist; run platform generators first")
    changed_files = 0
    replacements = 0
    for path in DIST.rglob("*.html"):
        original = path.read_text(encoding="utf-8")
        updated, count = humanize(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1
            replacements += count
    print(f"Human copy layer applied: files={changed_files} replacements={replacements}")


if __name__ == "__main__":
    main()
