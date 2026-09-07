# coding: utf-8
from html import escape as e
from services import tr

def calculator(data,l):
 def label(text):return tr(text)[l]
 def number(name,title,value,minimum=1):return f'<label>{e(label(title))}<input name="{name}" type="number" min="{minimum}" max="100000" step="1" value="{value}" inputmode="numeric"></label>'
 select=''.join(f'<option value="{e(p["code"])}">{e(p["name"][l])} · {p["durationMinutes"]} min</option>' for p in data['packages']+data['wixPackages'])
 select+=f'<option value="group">{e(label("Csoportos portré || Group portraits || Gruppenporträts"))}</option>'
 h=f'<section class="section calculator" data-calculator hidden><h2>{e(label("Tervezd meg a keretet || Plan your budget || Plane dein Budget"))}</h2><p>{e(label("HUF alapú tájékoztató kalkuláció, 27% áfával. Az eredményt nem küldjük el, és nem foglal időpontot. || An indicative HUF estimate with 27% VAT. Results are not sent and no appointment is booked. || Unverbindliche HUF-Kalkulation mit 27% Umsatzsteuer. Es werden keine Ergebnisse versendet und keine Termine gebucht."))}</p><div class="calculator-grid"><label>{e(label("Csomag || Package || Paket"))}<select name="package">{select}</select></label>'
 h+='<div data-groups="group brand-visual-positioning">'+number('people','Résztvevők || Participants || Personen',1)+'</div>'
 h+='<div data-groups="group">'+number('hours','Fotózási órák || Photography hours || Fotostunden',1)+'</div>'
 h+='<div data-groups="group portrait brand-visual-positioning fine-art">'+number('images','Kiválasztott képek (csoport/brand: fejenként) || Selected images (group/brand: per person) || Ausgewählte Bilder (Gruppe/Brand: pro Person)',1)+'</div>'
 h+='<div data-groups="event">'+number('guests','Vendégek || Guests || Gäste',100)+number('tracks','Párhuzamos programok || Parallel sessions || Parallele Programmpunkte',1)+number('extra','További fotósok minimuma || Minimum additional photographers || Mindestzahl zusätzlicher Fotografen',0,0)+'</div></div><div data-extras><fieldset><legend>'+e(label('Opcionális kiegészítők || Optional extras || Optionale Extras'))+'</legend>'
 names={'stylist':'Stylist || Stylist || Styling','hair':'Fodrász || Hair styling || Haarstyling','makeup':'Smink || Makeup || Make-up','expressDelivery':'Expressz átadás || Express delivery || Expressübergabe','mobileStudio':'Mobil stúdió || Mobile studio || Mobiles Studio','artDirection':'Művészeti vezetés || Art direction || Künstlerische Leitung'}
 for key,title in names.items():h+=f'<label class="check"><input type="checkbox" name="addon" value="{key}">{e(label(title))}</label>'
 h+=f'<label class="check"><input type="checkbox" name="travel">{e(label("Utazás szükséges || Travel required || Reise erforderlich"))}</label></fieldset><div class="calculator-grid" data-travel><label>{e(label("Ország || Country || Land"))}<select name="country"><option value="HU">Magyarország / Hungary / Ungarn</option><option value="AT">Ausztria / Austria / Österreich</option><option value="other">'+e(label('Más ország || Other country || Anderes Land'))+'</option></select></label>'+number('crew','Utazó stábtagok || Travelling crew members || Reisende Teammitglieder',1)+'</div></div><output aria-live="polite"></output></section>'
 return h
