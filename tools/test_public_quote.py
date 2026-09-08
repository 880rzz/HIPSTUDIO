# coding: utf-8
from pathlib import Path
import re

R=Path(__file__).resolve().parents[1]
D=R/'dist'

PRICE_PAGES={
 'hu':D/'hu/arak/index.html',
 'en':D/'en/pricing/index.html',
 'de':D/'de/preise/index.html'
}
KNOWN_PRICE_TOKENS=['48 000 HUF','88 000 HUF','168 000 HUF','276 000 HUF','139 990 HUF','84 990 HUF','358 000 HUF']


def main():
    for rel in ['pricing.json','assets/calculator.mjs','assets/pricing-engine.mjs']:
        assert not (D/rel).exists(), f'public pricing artifact leaked: {rel}'
    for lang,path in PRICE_PAGES.items():
        raw=path.read_text()
        assert 'data-calculator' not in raw
        assert '<table' not in raw.lower()
        assert 'info@hipstudio.hu' in raw
        assert '24' in raw
        assert 'hellouzlet.hu/' + lang + '/' in raw
        assert not re.search(r'\b(?:netHUF|grossHUF|vatHUF)\b',raw)
        for token in KNOWN_PRICE_TOKENS:
            assert token not in raw, f'{lang}: leaked known public price {token}'
    all_html='\n'.join(p.read_text() for p in D.rglob('*.html'))
    assert 'Tájékoztató HUF-árak' not in all_html
    assert 'Indicative HUF pricing' not in all_html
    assert 'Unverbindliche HUF-Preise' not in all_html
    assert 'Milyen pénznemben és áfával szerepelnek az árak?' not in all_html
    assert 'What currency and VAT treatment do prices use?' not in all_html
    assert 'Welche Währung und Umsatzsteuer gelten?' not in all_html
    print('Public pricing suppression and tailored quote routing passed')

if __name__=='__main__': main()
