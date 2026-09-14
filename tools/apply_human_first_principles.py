# coding: utf-8
"""Apply the final HIPStudio /human + first-principles layer.

Runs after all platform generators. It keeps facts, legal boundaries, routes and
review protections intact while replacing promotional language with direct,
problem-first copy in HU/EN/DE and adding the three-area visual stylesheet.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist-platform'
SRC_CSS = ROOT / 'assets' / 'human-first-principles.css'
DST_CSS = DIST / 'assets' / 'human-first-principles.css'

if not DIST.exists():
    raise SystemExit('dist-platform missing; run build:platform first')
DST_CSS.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC_CSS, DST_CSS)

REPLACEMENTS = {
    # HU
    '20 év tapasztalat. Most még többet adunk egy kézből.': 'Három terület. Egy cél: működjön.',
    'Komplexebb üzleti megoldások. Egy 20 éve épülő márkától.': 'Három terület. Egy cél: működjön.',
    'A HIPStudio húsz éve segít cégeknek jól látszani. Ma már abban is segítünk, hogy jobban működjenek. Pénzügy, működés, tartalom és vállalati élmények — átláthatóan, egy helyen.': 'A HIPStudio három külön területben gondolkodik: hogyan működik a cég, hogyan látszik, és hogyan kapcsolódnak benne az emberek. Nem csomagokból indulunk ki. Először azt nézzük meg, mi a valódi probléma.',
    'A HIPStudio kreatív és kommunikációs alapjára most működési, pénzügyi, digitalizációs és vállalati élménykompetenciákat kapcsolunk. Egy partneri rendszerben segítünk a háttérműködéstől a láthatóságon át az emberek kapcsolódásáig.': 'A HIPStudio három külön területben gondolkodik: hogyan működik a cég, hogyan látszik, és hogyan kapcsolódnak benne az emberek. Nem csomagokból indulunk ki. Először azt nézzük meg, mi a valódi probléma.',
    'Egy HIPStudio. Több területen ugyanazzal a figyelemmel.': 'Három külön terület. Nem mossuk őket össze.',
    'Egy HIPStudio. Három szakmai pillér. Több lehetőség az ügyfélnek.': 'Három külön terület. Nem mossuk őket össze.',
    'Egy cég működése nem különálló feladatokból áll. A pénzügy, a napi működés, a kommunikáció és a csapat ugyanazt az üzleti célt szolgálja. Ezért hoztuk közelebb egymáshoz ezeket a területeket. Kevesebb egyeztetés, tisztább felelősség, több valódi segítség.': 'A három terület más problémát old meg. Business: rend és rálátás. Creative: érthető és hiteles jelenlét. Experiences: valódi kapcsolódás az emberek között. Ahol értelme van, együtt dolgoznak. Ahol nincs, külön maradnak.',
    'Egy partner, aki érti, hogyan működik a céged.': 'Először értsük meg, mi nem működik.',
    'Beszéljünk 30 percet': 'Beszéljük át',
    'Három terület. Egy közös szemlélet.': 'Három terület. Három külön feladat.',
    'Tisztább működés. Jobb vezetői rálátás.': 'Legyen rend a működésben.',
    'Ott segítünk, ahol a napi működés túl sok vezetői időt visz el: pénzügyi és HR-adminisztráció, back office, controlling, riporting, folyamatfejlesztés és jól megválasztott automatizálás. A szabályozott feladatokat csak tisztázott felelősségi körrel vállaljuk.': 'Ha a vezető napja adminisztrációval, riportokkal és egyeztetésekkel megy el, először azt nézzük meg, mi hagyható el, mi egyszerűsíthető és mi automatizálható. A szabályozott feladatoknál a felelősségi köröket külön tisztázzuk.',
    'Kevesebb operatív zaj. Több idő a cég vezetésére.': 'Kevesebb felesleges kör. Több rálátás.',
    'Tartalom, aminek üzleti értelme van.': 'Legyen világos, mit képvisel a cég.',
    '2006 óta készítünk fotót, videót és kommunikációs tartalmat cégeknek. Nem azért, hogy több anyag készüljön, hanem hogy jobban érthető, látható és emlékezetes legyen a márka.': 'Nem tartalmat gyártunk a tartalom kedvéért. Először azt tisztázzuk, kinek, mit és miért kell megértenie. Utána választunk formátumot: fotó, videó, podcast vagy ezek együtt.',
    'Tartalom, amit értenek — és megjegyeznek.': 'Kevesebb zaj. Egyértelműbb üzenet.',
    'Vállalati élmények, amelyek tényleg összehozzák az embereket.': 'Az emberek ne csak ott legyenek. Kapcsolódjanak.',
    'A Flúgos több mint másfél évtizedes tapasztalatából építünk olyan céges programokat, amelyeknek valódi céljuk van: jobb csapatmunka, erősebb kapcsolatok és emlékezetes közös élmények.': 'Egy program nem attól jó, hogy látványos. Attól jó, hogy történik benne valami az emberek között. A Flúgos tapasztalatára építve olyan helyzeteket tervezünk, ahol van közös feladat, valódi figyelem és emlékezetes kapcsolódás.',
    'Élmények, amelyeknek céljuk is van.': 'Ne csak program legyen. Legyen hatása.',
    'Elsősorban 10–100 fős cégekkel dolgozunk, ahol a vezető még túl sok mindent tart kézben, és nem éri meg minden területre külön belső csapatot építeni.': 'Olyan cégeknek szól, ahol már nem fér bele, hogy minden a vezető fejében és naptárában fusson. Nem a cégméret az első kérdés, hanem az, hol akad el a működés.',
    'A működés, a tartalom és az emberek nem külön világok. Ha jól kapcsolódnak egymáshoz, a cég egyszerűbben működik és gyorsabban halad.': 'Három külön probléma. Három külön szakmai terület. Csak ott kapcsoljuk össze őket, ahol annak tényleg van értelme.',

    # EN
    '20 years of experience. Now with more ways to help your business.': 'Three areas. One goal: make it work.',
    'More integrated business solutions. From a brand built over 20 years.': 'Three areas. One goal: make it work.',
    'HIPStudio has spent twenty years helping companies communicate clearly. Today we also help them run more smoothly — across operations, finance, content and corporate experiences, with one accountable partner.': 'HIPStudio looks at three different questions: how the business runs, how it is seen, and how people connect inside it. We do not start with packages. We start with the actual problem.',
    "We are extending HIPStudio's creative and communication foundation with operations, finance, digitalisation and corporate-experience capabilities. One partner model can now support the business from back-office operations to visibility and human connection.": 'HIPStudio looks at three different questions: how the business runs, how it is seen, and how people connect inside it. We do not start with packages. We start with the actual problem.',
    'One HIPStudio. More expertise, working together.': 'Three different areas. We keep them distinct.',
    'One HIPStudio. Three specialist pillars. More capability for the client.': 'Three different areas. We keep them distinct.',
    'A business does not run in separate boxes. Finance, operations, communication and people all affect the same result. We bring those areas closer together so clients spend less time coordinating suppliers and more time moving the business forward.': 'The three areas solve different problems. Business: order and visibility. Creative: a clear and credible presence. Experiences: real connection between people. They work together when that helps. Otherwise, they stay separate.',
    'One partner who understands how your business works.': 'First, understand what is not working.',
    'Talk to us for 30 minutes': 'Talk it through',
    'Three areas. One way of working.': 'Three areas. Three different jobs.',
    'Clearer operations. Better management visibility.': 'Put the operation in order.',
    'We help SMEs reduce the operational load on management: finance and HR administration, back office, controlling, reporting, process improvement and practical automation. Regulated work is only offered with clearly agreed responsibilities.': 'If management spends the day on admin, reporting and coordination, we first ask what can be removed, simplified or automated. For regulated work, responsibilities are agreed separately and explicitly.',
    'Less operational noise. More time to lead the business.': 'Fewer unnecessary loops. Better visibility.',
    'Content with a clear business purpose.': 'Make it clear what the company stands for.',
    'Since 2006, we have created photography, video and communication for companies that need to be understood, seen and remembered — not simply produce more content.': 'We do not make content for the sake of making content. First we clarify who needs to understand what, and why. Then we choose the format: photography, video, podcast, or a useful combination.',
    'Content people understand — and remember.': 'Less noise. A clearer message.',
    'Corporate experiences that genuinely bring people together.': 'People should not just attend. They should connect.',
    'We use more than fifteen years of Flúgos experience to create corporate programmes with a real purpose: stronger teams, better relationships and memorable shared experiences.': 'A programme is not good because it looks impressive. It is good when something actually happens between people. Building on Flúgos experience, we design situations with a shared task, real attention and memorable connection.',
    'Experiences with a purpose.': 'Do not just run a programme. Make it matter.',
    'We mainly work with companies of 10–100 people where management still carries too much of the day-to-day load and building a full internal team for every function would not make sense.': 'This is for companies where too much still runs through the manager’s head and calendar. Company size is not the first question. The first question is where work gets stuck.',
    'Operations, content and people are not separate worlds. When they work together, the business becomes easier to run and easier to grow.': 'Three different problems. Three different areas of expertise. We connect them only when that genuinely helps.',

    # DE
    '20 Jahre Erfahrung. Heute können wir Unternehmen noch umfassender unterstützen.': 'Drei Bereiche. Ein Ziel: Es soll funktionieren.',
    'Umfassendere Unternehmenslösungen. Von einer Marke mit 20 Jahren Erfahrung.': 'Drei Bereiche. Ein Ziel: Es soll funktionieren.',
    'Seit zwanzig Jahren hilft HIPStudio Unternehmen dabei, klar und professionell aufzutreten. Heute unterstützen wir zusätzlich bei Abläufen, Finanzen, Content und Corporate Experiences — mit einem verantwortlichen Partner.': 'HIPStudio schaut auf drei unterschiedliche Fragen: Wie funktioniert das Unternehmen? Wie wird es wahrgenommen? Und wie verbinden sich die Menschen darin? Wir beginnen nicht mit Paketen. Wir beginnen mit dem tatsächlichen Problem.',
    'Wir erweitern die kreative und kommunikative Basis von HIPStudio um Kompetenzen in Betrieb, Finanzen, Digitalisierung und Corporate Experience. Ein Partnermodell unterstützt Unternehmen vom Backoffice über Sichtbarkeit bis zur Verbindung von Menschen.': 'HIPStudio schaut auf drei unterschiedliche Fragen: Wie funktioniert das Unternehmen? Wie wird es wahrgenommen? Und wie verbinden sich die Menschen darin? Wir beginnen nicht mit Paketen. Wir beginnen mit dem tatsächlichen Problem.',
    'Ein HIPStudio. Mehr Kompetenz, die zusammenarbeitet.': 'Drei unterschiedliche Bereiche. Wir halten sie klar getrennt.',
    'Ein HIPStudio. Drei Fachsäulen. Mehr Möglichkeiten für Kunden.': 'Drei unterschiedliche Bereiche. Wir halten sie klar getrennt.',
    'Ein Unternehmen funktioniert nicht in getrennten Silos. Finanzen, Abläufe, Kommunikation und Menschen beeinflussen dasselbe Ergebnis. Wir bringen diese Bereiche zusammen, damit weniger Zeit für Koordination verloren geht und mehr Zeit für das eigentliche Geschäft bleibt.': 'Die drei Bereiche lösen unterschiedliche Probleme. Business: Ordnung und Überblick. Creative: ein klarer und glaubwürdiger Auftritt. Experiences: echte Verbindung zwischen Menschen. Sie arbeiten zusammen, wenn das sinnvoll ist. Sonst bleiben sie getrennt.',
    'Ein Partner, der versteht, wie Ihr Unternehmen arbeitet.': 'Zuerst verstehen, was nicht funktioniert.',
    '30 Minuten miteinander sprechen': 'Kurz besprechen',
    'Drei Bereiche. Eine gemeinsame Arbeitsweise.': 'Drei Bereiche. Drei unterschiedliche Aufgaben.',
    'Klarere Abläufe. Bessere Übersicht für die Geschäftsführung.': 'Ordnung in die Abläufe bringen.',
    'Wir entlasten KMU dort, wo das Tagesgeschäft zu viel Führungszeit bindet: Finanz- und HR-Administration, Backoffice, Controlling, Reporting, Prozessverbesserung und sinnvolle Automatisierung. Regulierte Aufgaben übernehmen wir nur mit klar vereinbarten Verantwortlichkeiten.': 'Wenn Führungskräfte ihren Tag mit Administration, Reporting und Abstimmung verbringen, schauen wir zuerst, was wegfallen, einfacher werden oder automatisiert werden kann. Bei regulierten Aufgaben werden Verantwortlichkeiten separat und eindeutig geklärt.',
    'Weniger operativer Lärm. Mehr Zeit für die Führung des Unternehmens.': 'Weniger unnötige Schleifen. Mehr Überblick.',
    'Content mit klarem geschäftlichem Zweck.': 'Klar machen, wofür das Unternehmen steht.',
    'Seit 2006 produzieren wir Fotografie, Video und Kommunikation für Unternehmen, die verstanden, gesehen und erinnert werden wollen — nicht einfach nur mehr Content.': 'Wir produzieren keinen Content um des Contents willen. Zuerst klären wir, wer was verstehen soll und warum. Danach wählen wir das Format: Fotografie, Video, Podcast oder eine sinnvolle Kombination.',
    'Content, den Menschen verstehen — und behalten.': 'Weniger Lärm. Eine klarere Botschaft.',
    'Unternehmenserlebnisse, die Menschen wirklich zusammenbringen.': 'Menschen sollen nicht nur teilnehmen. Sie sollen sich verbinden.',
    'Wir nutzen mehr als fünfzehn Jahre Flúgos-Erfahrung für Unternehmensprogramme mit echtem Zweck: stärkere Teams, bessere Beziehungen und gemeinsame Erlebnisse, die in Erinnerung bleiben.': 'Ein Programm ist nicht gut, weil es spektakulär aussieht. Es ist gut, wenn zwischen Menschen wirklich etwas passiert. Auf Basis der Flúgos-Erfahrung gestalten wir Situationen mit gemeinsamer Aufgabe, echter Aufmerksamkeit und erinnerbarer Verbindung.',
    'Erlebnisse mit einem Zweck.': 'Nicht nur ein Programm. Es soll etwas bewirken.',
    'Wir arbeiten vor allem mit Unternehmen mit 10–100 Mitarbeitenden, in denen die Geschäftsführung noch zu viel Tagesgeschäft selbst trägt und ein vollständiges internes Team für jede Funktion nicht sinnvoll wäre.': 'Das richtet sich an Unternehmen, in denen noch zu viel über Kopf und Kalender der Geschäftsführung läuft. Die Unternehmensgröße ist nicht die erste Frage. Die erste Frage ist, wo Arbeit hängen bleibt.',
    'Betrieb, Content und Menschen sind keine getrennten Welten. Wenn sie gut zusammenspielen, wird das Unternehmen einfacher zu führen und kann schneller vorankommen.': 'Drei unterschiedliche Probleme. Drei unterschiedliche Fachbereiche. Wir verbinden sie nur dort, wo das wirklich sinnvoll ist.'
}

changed_files = 0
changed_replacements = 0
for path in DIST.rglob('*.html'):
    raw = path.read_text(encoding='utf-8')
    out = raw
    if '<body' in out and 'human-first-principles' not in out:
        out = out.replace('<body>', '<body class="human-first-principles">', 1)
    if 'human-first-principles.css' not in out:
        out = out.replace('</head>', '<link rel="stylesheet" href="/assets/human-first-principles.css"></head>', 1)
    for old, new in REPLACEMENTS.items():
        if old in out:
            n = out.count(old)
            out = out.replace(old, new)
            changed_replacements += n
    if out != raw:
        path.write_text(out, encoding='utf-8')
        changed_files += 1

print(f'Human first-principles layer applied: files={changed_files} replacements={changed_replacements}')
