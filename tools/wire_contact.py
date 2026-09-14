# coding: utf-8
"""Wire the public HIPStudio contact pages to verified contact data and quote routes."""
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R / 'dist-platform'

CONTACTS = {
    'hu/kapcsolat/index.html': {
        'title': 'Írd meg, mire van szükséged.',
        'text': 'Ha már körvonalazódik a feladat, indíts ajánlatkérést. Ha még csak kérdésed van, írj vagy hívj.',
        'quote': '/hu/ajanlatkeres/', 'quote_label': 'Ajánlatkérés', 'email_label': 'E-mail', 'phone_label': 'Telefon'
    },
    'en/contact/index.html': {
        'title': 'Tell us what you need.',
        'text': 'If the scope is already clear, start a quote request. If you still have a question, email or call us.',
        'quote': '/en/request-a-quote/', 'quote_label': 'Request a quote', 'email_label': 'Email', 'phone_label': 'Phone'
    },
    'de/kontakt/index.html': {
        'title': 'Sag uns, was du brauchst.',
        'text': 'Wenn die Aufgabe schon klar ist, starte eine Angebotsanfrage. Wenn noch Fragen offen sind, schreib uns oder ruf an.',
        'quote': '/de/angebot-anfragen/', 'quote_label': 'Angebot anfragen', 'email_label': 'E-Mail', 'phone_label': 'Telefon'
    },
}

for rel, c in CONTACTS.items():
    path = D / rel
    if not path.exists():
        raise SystemExit(f'missing contact page: {rel}')
    html = path.read_text(encoding='utf-8')
    if 'data-contact-live' in html:
        continue
    block = f'''<section class="contact-live" data-contact-live aria-label="{c['title']}">
<h2>{c['title']}</h2>
<p>{c['text']}</p>
<div class="contact-live__actions"><a class="button" href="{c['quote']}">{c['quote_label']}</a></div>
<div class="contact-live__details"><a href="mailto:info@hipstudio.hu">{c['email_label']}: info@hipstudio.hu</a><a href="tel:+36302215506">{c['phone_label']}: +36&nbsp;30&nbsp;221&nbsp;5506</a></div>
</section>'''
    if '</main>' not in html:
        raise SystemExit(f'missing </main> in {rel}')
    html = html.replace('</main>', block + '</main>', 1)
    path.write_text(html, encoding='utf-8')

print('Live contact routing wired for HU/EN/DE')
