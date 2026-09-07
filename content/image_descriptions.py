# coding: utf-8
# Visually reviewed against contact sheets on 2026-09-07. No identities inferred.
from services import tr
DESCRIPTIONS={}
def add(category,rows):
 for i,row in enumerate(rows.strip().split('\n'),1): DESCRIPTIONS[f'{category}-{i:02}']=tr(row)
add('portrait','''Női arckép rózsaszín virággal az előtérben || Woman’s face with a pink flower in the foreground || Frauengesicht mit rosa Blume im Vordergrund
Szemüveges férfi kültéri portréja || Outdoor portrait of a man wearing glasses || Außenporträt eines Mannes mit Brille
Kék pólós férfi karba tett kézzel || Man in a blue polo shirt with folded arms || Mann im blauen Poloshirt mit verschränkten Armen
Nő kültéri portréja mintás felsőben || Outdoor portrait of a woman in a patterned top || Außenporträt einer Frau in gemustertem Oberteil
Nő sárga kabátban, oldalra nézve || Woman in a yellow coat looking to the side || Frau im gelben Mantel mit seitlichem Blick
Közelkép egy nő arcáról, kezére támaszkodva || Close portrait of a woman resting on her hand || Nahporträt einer Frau auf ihre Hand gestützt
Szemüveges nő stúdióportréja karba tett kézzel || Studio portrait of a woman with glasses and folded arms || Studioporträt einer Frau mit Brille und verschränkten Armen
Teljes alakos női portré sötét kosztümben || Full-length portrait of a woman in a dark suit || Ganzkörperporträt einer Frau im dunklen Kostüm
Férfi kávézóasztalnál szürke pólóban || Man at a café table wearing a grey shirt || Mann am Cafétisch im grauen Shirt
Férfi arcképe sötét háttér előtt || Close portrait of a man against a dark background || Nahporträt eines Mannes vor dunklem Hintergrund
Mosolygó férfi pohárral és kalappal || Smiling man holding a glass and hat || Lächelnder Mann mit Glas und Hut
Férfi szürke zakóban sötét háttér előtt || Man in a grey jacket against a dark background || Mann im grauen Sakko vor dunklem Hintergrund
Fény és árnyékminta egy nő arcán || Patterned light and shadow across a woman’s face || Licht- und Schattenmuster auf einem Frauengesicht
Szakállas férfi portréja kék ingben || Portrait of a bearded man in a blue shirt || Porträt eines bärtigen Mannes im blauen Hemd
Fekete-fehér női portré archoz emelt kezekkel || Black-and-white portrait of a woman with hands raised to her face || Schwarz-Weiß-Porträt einer Frau mit Händen am Gesicht
Férfi világosszürke zakóban || Man wearing a light grey jacket || Mann im hellgrauen Sakko
Férfi stúdióportréja fehér ingben || Studio portrait of a man in a white shirt || Studioporträt eines Mannes im weißen Hemd
Nő oldalra fordulva, haján meleg fénnyel || Woman turned to the side with warm light on her hair || Seitlich gedrehte Frau mit warmem Licht im Haar
Férfi gyújtóval, füsttel körülvéve || Man holding a lighter, surrounded by smoke || Mann mit Feuerzeug, von Rauch umgeben
Szemüveges férfi csészével a kanapén || Man wearing glasses and holding a cup on a sofa || Mann mit Brille und Tasse auf einem Sofa
Mosolygó férfi őszi lombok előtt || Smiling man in front of autumn foliage || Lächelnder Mann vor Herbstlaub
Nő portréja zöld lombok között || Portrait of a woman among green leaves || Frauenporträt zwischen grünen Blättern
Férfi fekete pólóban sötét stúdióban || Man in a black shirt in a dark studio || Mann im schwarzen Shirt im dunklen Studio
Férfi világos zakóban téglafal mellett || Man in a light jacket beside a brick wall || Mann im hellen Sakko neben einer Backsteinwand
Nő piros ruhában, válla fölött visszanézve || Woman in a red dress looking over her shoulder || Frau im roten Kleid mit Blick über die Schulter''')
add('portfolio','''Négy férfi összehangolt öltözékben, kalapokkal || Four men in coordinated outfits holding hats || Vier Männer in abgestimmter Kleidung mit Hüten
Szakállas férfi farmerdzsekiben || Bearded man wearing a denim jacket || Bärtiger Mann in einer Jeansjacke
Női sziluett meleg ellenfényben || Woman’s silhouette in warm backlight || Weibliche Silhouette im warmen Gegenlicht
Férfi kabátban korlátnál || Man in a coat beside a railing || Mann im Mantel an einem Geländer
Férfi kék megvilágításban a kanapén || Man on a sofa in blue lighting || Mann auf einem Sofa in blauem Licht
Fekete-fehér portré egy ülő nőről || Black-and-white portrait of a seated woman || Schwarz-Weiß-Porträt einer sitzenden Frau
Mosolygó nő portréja vörös háttér előtt || Portrait of a smiling woman against a red background || Porträt einer lächelnden Frau vor rotem Hintergrund
Szakállas férfi világos zakóban egy asztalnál || Bearded man in a light jacket at a table || Bärtiger Mann im hellen Sakko an einem Tisch
Sötét tónusú férfiportré oldalirányú fényben || Dark-toned male portrait with side lighting || Dunkles Männerporträt mit Seitenlicht
Férfi világosszürke zakóban stúdióháttér előtt || Man in a light grey jacket against a studio background || Mann im hellgrauen Sakko vor Studiohintergrund
Gitáros sötét színpadon kék fénnyel || Guitarist on a dark stage with blue light || Gitarrist auf dunkler Bühne mit blauem Licht
Férfi kalapban és kockás mellényben || Man wearing a hat and checked waistcoat || Mann mit Hut und karierter Weste
Napszemüveges férfi mintás ingben || Man in sunglasses and a patterned shirt || Mann mit Sonnenbrille und gemustertem Hemd
Szakállas férfi sötét kabátban kültéren || Bearded man in a dark coat outdoors || Bärtiger Mann im dunklen Mantel im Freien
Fekete-fehér női portré emelt tekintettel || Black-and-white portrait of a woman looking upward || Schwarz-Weiß-Porträt einer Frau mit Blick nach oben
Nő napszemüvegben zöld ruhában || Woman wearing sunglasses and a green dress || Frau mit Sonnenbrille im grünen Kleid
Szemüveges férfi csészével kanapén || Man wearing glasses with a cup on a sofa || Mann mit Brille und Tasse auf einem Sofa
Nő piros ruhában visszanézve || Woman in a red dress looking back || Frau im roten Kleid mit Blick zurück
Fiatal férfi piros sportmezben itallal || Young man in a red sports vest holding a drink || Junger Mann im roten Sporttrikot mit Getränk
Fekete-fehér portré ülő, hosszú hajú nőről || Black-and-white portrait of a seated woman with long hair || Schwarz-Weiß-Porträt einer sitzenden Frau mit langen Haaren
Nő lovas sisakban, oldalról fényképezve || Woman wearing a riding helmet, seen from the side || Frau mit Reithelm von der Seite
Nő napszemüvegben, fehér mintás felsőben || Woman in sunglasses and a patterned white top || Frau mit Sonnenbrille und weißem gemustertem Oberteil
Fekete-fehér férfiportré összefogott kézzel || Black-and-white male portrait with hands together || Schwarz-Weiß-Männerporträt mit zusammengelegten Händen
Nő piros ruhában kerti padon || Woman in a red dress on a garden bench || Frau im roten Kleid auf einer Gartenbank
Nő fekete felsőben és piros szoknyában || Woman in a black top and red skirt || Frau im schwarzen Oberteil und roten Rock''')
add('commercial','''Városi utca magas házakkal és piros busszal || City street with tall buildings and a red bus || Stadtstraße mit hohen Gebäuden und rotem Bus
Világos, bordázott épületbelső emberekkel || Bright ribbed architectural interior with people || Heller gerippter Innenraum mit Menschen
Városi jelenetekből összeállított fotókollázs || Photo collage of city scenes || Fotocollage aus Stadtszenen
Régi autó zöld növények között || Vintage car among green plants || Altes Auto zwischen grünen Pflanzen
Idősebb férfi könyvekkel teli szobában || Older man in a room filled with books || Älterer Mann in einem Raum voller Bücher
Két ember séta közben egy városi utcán || Two people walking along a city street || Zwei Menschen beim Gehen auf einer Stadtstraße
Sötét autó egy városi zebránál || Dark car at a city pedestrian crossing || Dunkles Auto an einem städtischen Zebrastreifen
Nő vörös felsőben drótkerítés előtt || Woman in a red top in front of a wire fence || Frau im roten Oberteil vor einem Drahtzaun
Ember a vízparton, háttérben városi látképpel || Person at the waterfront with a city skyline behind || Person am Wasser vor einer Stadtsilhouette
Makrókép egy növényi részletről || Macro photograph of a plant detail || Makroaufnahme eines Pflanzendetails
Nő virágos fejdísszel kültéri rendezvényen || Woman wearing a floral headpiece at an outdoor event || Frau mit Blumenkopfschmuck bei einer Außenveranstaltung
Lovas naplementében || Horse rider at sunset || Reiter im Sonnenuntergang
Fekete-fehér közeli kép férfiról és kisbabáról || Black-and-white close-up of a man and a baby || Schwarz-Weiß-Nahaufnahme eines Mannes mit Baby
Sportautó hátulról egy városi utcában || Rear view of a sports car on a city street || Sportwagen von hinten in einer Stadtstraße
Nő korlátnál a vízparton || Woman beside a waterfront railing || Frau an einem Geländer am Wasser
Fekete-fehér női divatkép városi fal előtt || Black-and-white fashion photograph of a woman by an urban wall || Schwarz-Weiß-Modefoto einer Frau vor einer Stadtmauer
Sportcipő közeli képe, háttérben szökőkúttal || Close-up of a trainer with a fountain behind || Nahaufnahme eines Sportschuhs vor einem Brunnen
Művészi testtanulmány fény és árnyék határán || Artistic body study between light and shadow || Künstlerische Körperstudie zwischen Licht und Schatten
Hosszú városi utca magas épületek között || Long city street between tall buildings || Lange Stadtstraße zwischen hohen Gebäuden
Rózsaszín ruhás alak egy városi utcában || Figure in pink clothing on a city street || Person in rosa Kleidung auf einer Stadtstraße
Divatkép éjszakai városi fényekben || Fashion photograph in city lights at night || Modeaufnahme im nächtlichen Stadtlicht
Sötét tónusú városi férfiportré || Dark-toned urban male portrait || Dunkles urbanes Männerporträt
Nő és gyermek ülve egy kirakat előtt || Woman and child seated in front of a shop window || Frau und Kind sitzend vor einem Schaufenster
Nő hegedűvel, erős fény-árnyék hatással || Woman holding a violin in contrasting light || Frau mit Geige in kontrastreichem Licht
Városi látkép vízparti cölöpökkel naplementében || Skyline with waterfront posts at sunset || Stadtsilhouette mit Pfählen am Wasser im Sonnenuntergang''')
add('property','''Kivilágított magasépületek éjszaka || Illuminated high-rise buildings at night || Beleuchtete Hochhäuser bei Nacht
Fekete-fehér épületfotó széles előtérrel || Black-and-white building photograph with a wide foreground || Schwarz-Weiß-Gebäudefoto mit weitem Vordergrund
Jacht a vízen városi látkép előtt || Yacht on the water in front of a city skyline || Jacht auf dem Wasser vor einer Stadtsilhouette
Világos épületbelső vörös szőnyeges lépcsővel || Bright interior with a red-carpeted staircase || Heller Innenraum mit rot ausgelegter Treppe
Díszes kupola belső nézete || Interior view of an ornate dome || Innenansicht einer verzierten Kuppel
Íves üvegfalú folyosó napfényben || Curved glass corridor in sunlight || Gebogener Glaskorridor im Sonnenlicht
Téglaépületek közötti zöld udvar || Green courtyard between brick buildings || Grüner Innenhof zwischen Backsteingebäuden
Megvilágított irodaablakok éjszaka || Illuminated office windows at night || Beleuchtete Bürofenster bei Nacht
Díszes belső lépcsőház || Ornate interior staircase || Verziertes inneres Treppenhaus
Épületegyüttes felülnézetből || Building complex viewed from above || Gebäudekomplex von oben
Fehér templom és íves épület napsütésben || White church and curved building in sunlight || Weiße Kirche und gebogenes Gebäude im Sonnenlicht
Üveghomlokzatok felfelé nézve || Glass façades viewed upward || Glasfassaden mit Blick nach oben
Tetőterasz és városi épület esti fényben || Rooftop terrace and city building in evening light || Dachterrasse und Stadtgebäude im Abendlicht
Színes történelmi homlokzatok és türkiz autó || Colourful historic façades and a turquoise car || Bunte historische Fassaden und türkisfarbenes Auto
Fehér, bordázott csarnok emberekkel || White ribbed hall with people || Weiße gerippte Halle mit Menschen
Nagy ablakos nappali városi kilátással || Living room with large windows and a city view || Wohnzimmer mit großen Fenstern und Stadtblick
Emberek sziluettje üvegkorlát mögött || Silhouettes of people behind a glass railing || Menschliche Silhouetten hinter einem Glasgeländer
Modern üvegépület nagy nyitott előtérrel || Modern glass building with a large open foreground || Modernes Glasgebäude mit großem offenem Vorplatz
Világos, üres szoba nagy ablakokkal || Bright empty room with large windows || Heller leerer Raum mit großen Fenstern
Boltozatos épületbelső hosszú padsorokkal || Vaulted interior with long rows of benches || Gewölbter Innenraum mit langen Bankreihen
Modern épület ismétlődő erkélyekkel || Modern building with repeating balconies || Modernes Gebäude mit wiederkehrenden Balkonen
Lépcsőház végében magas ablak || Tall window at the end of a staircase || Hohes Fenster am Ende eines Treppenhauses
Kivilágított üvegépületek alkonyatkor || Illuminated glass buildings at dusk || Beleuchtete Glasgebäude in der Dämmerung
Csatorna színes házak között || Canal between colourful houses || Kanal zwischen bunten Häusern
Ovális lépcsőház felfelé nézve || Oval staircase viewed upward || Ovales Treppenhaus mit Blick nach oben''')
add('art','''Művészi női portré sötét, meleg oldalfényben || Artistic portrait of a woman in dark warm side light || Künstlerisches Frauenporträt in dunklem warmem Seitenlicht
Művészi akt részlete háttal álló alakról || Fine-art nude detail of a figure seen from behind || Künstlerisches Aktdetail einer Figur von hinten
Nő ülve kék és vörös stúdiófényben || Seated woman in blue and red studio light || Sitzende Frau in blauem und rotem Studiolicht
Női profil meleg árnyékban || Woman’s profile in warm shadow || Weibliches Profil im warmen Schatten
Művészi akt részlete fehér anyaggal || Fine-art nude detail with white fabric || Künstlerisches Aktdetail mit weißem Stoff
Nő arca és válla finom oldalfényben || Woman’s face and shoulder in soft side light || Gesicht und Schulter einer Frau in sanftem Seitenlicht
Csíkos fény egy álló női alakon || Striped light across a standing female figure || Gestreiftes Licht auf einer stehenden weiblichen Figur
Művészi testtanulmány ékszerrel sötét háttéren || Artistic body study with jewellery on a dark background || Künstlerische Körperstudie mit Schmuck vor dunklem Hintergrund
Boudoir részlet vörös fehérneműben || Boudoir detail in red lingerie || Boudoirdetail in roten Dessous
Női sziluett karra tett kézzel || Woman’s silhouette with one hand on her hip || Weibliche Silhouette mit einer Hand an der Hüfte
Nő vörös anyagba burkolva meleg fényben || Woman wrapped in red fabric in warm light || Frau in rotem Stoff in warmem Licht
Női váll és hát részlete aranyszínű fényben || Detail of a woman’s shoulder and back in golden light || Detail von Schulter und Rücken einer Frau in goldenem Licht
Fekvő nő sziluettje meleg háttér előtt || Silhouette of a reclining woman against a warm background || Silhouette einer liegenden Frau vor warmem Hintergrund
Boudoir részlet kék és lila fényben || Boudoir detail in blue and violet light || Boudoirdetail in blauem und violettem Licht
Nő ülve oldalirányú vörös fényben || Seated woman in red side light || Sitzende Frau in rotem Seitenlicht
Fekvő nő sötét ruhában lágy háttér előtt || Reclining woman in dark clothing against a soft background || Liegende Frau in dunkler Kleidung vor weichem Hintergrund''')
