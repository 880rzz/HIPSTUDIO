"""Read-only public source capture. Raw snapshots stay out of the build."""
from pathlib import Path
import json, hashlib, subprocess, concurrent.futures, xml.etree.ElementTree as ET
from urllib.parse import urlsplit, quote
from datetime import datetime, timezone
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
urls=[]
for name in ['hipstudio-pages.xml','hipstudio-bookings.xml']:
    tree=ET.parse(ROOT/'audit/raw'/name)
    urls += [u.find('{*}loc').text for u in tree.getroot()]

def capture(url):
    slug=urlsplit(url).path.strip('/') or 'home'
    key=slug.replace('/','__')
    dest=ROOT/'audit/raw'/f'{key}.html'
    safe=quote(url,safe=':/?=&%')
    result=subprocess.run(['curl','-sSL','--fail','--max-time','60','-D',str(dest.with_suffix('.headers')),'-o',str(dest),safe],capture_output=True,text=True)
    if result.returncode: return {'url':url,'error':result.stderr}
    raw=dest.read_text(); soup=BeautifulSoup(raw,'html.parser')
    main=soup.find('main') or soup
    for tag in main.select('script,style,svg'): tag.decompose()
    texts=[x.get_text(' ',strip=True) for x in main.select('h1,h2,h3,h4,p,li')]
    texts=list(dict.fromkeys(t for t in texts if t))
    all_soup=BeautifulSoup(raw,'html.parser')
    row={'url':url,'file':str(dest.relative_to(ROOT)), 'sha256':hashlib.sha256(raw.encode()).hexdigest(), 'title':all_soup.title.get_text() if all_soup.title else '', 'text':texts, 'h1':[x.get_text(' ',strip=True) for x in all_soup.select('h1')], 'meta':{m.get('name',m.get('property')):m.get('content') for m in all_soup.select('meta[name],meta[property]')},'canonical':[x.get('href') for x in all_soup.select('link[rel=canonical]')], 'hreflang':[{k:x.get(k) for k in ['hreflang','href']} for x in all_soup.select('link[hreflang]')], 'jsonld':[s.get_text() for s in all_soup.select('script[type="application/ld+json"]')], 'images':[{'src':x.get('src'),'alt':x.get('alt'),'width':x.get('width'),'height':x.get('height')} for x in main.select('img')], 'links':list(dict.fromkeys(x.get('href') for x in all_soup.select('a[href]')))}
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    rows=list(ex.map(capture,urls))
(ROOT/'audit/source-inventory.json').write_text(json.dumps({'capturedAt':datetime.now(timezone.utc).isoformat(),'pages':rows},ensure_ascii=False,indent=2))
for r in rows: print(r['url'],r.get('error') or f"{len(r['text'])} blocks; {len(r['images'])} images")
