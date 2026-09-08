# coding: utf-8
"""Capture public portfolio assets for local review; no publication rights inferred."""
import json, subprocess, hashlib, concurrent.futures
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
R=Path(__file__).resolve().parents[1]
x=json.loads((R/'audit/source-inventory.json').read_text())
items=[]
for category,slug in [('portrait','portrefotozas-galeria'),('portfolio','portfolio-fotozas-galeria'),('property','epulet-fotozas-galeria'),('commercial','reklamfoto-galeria'),('art','muveszi-aktfotozas-galeria')]:
 p=next(p for p in x['pages'] if p['url'].endswith('/'+slug))
 for i,img in enumerate(p['images']):
  src=(img.get('src') or '').split('/v1/')[0]
  if not src.startswith('https://static.wixstatic.com/media/'):continue
  items.append({'id':f'{category}-{i+1:02}','category':category,'sourcePage':p['url'],'original':src,'sourceAlt':img['alt'],'publicationRights':'pending','alt':{}})
(R/'assets/photos').mkdir(parents=True,exist_ok=True)
(R/'audit/raw/images').mkdir(parents=True,exist_ok=True)
def fetch(item):
 path=R/'audit/raw/images'/item['id']
 res=subprocess.run(['curl','-sSL','--fail','--max-time','45','-o',str(path),item['original']],capture_output=True)
 if res.returncode:return dict(item,error='download failed')
 try:
  im=ImageOps.exif_transpose(Image.open(path)).convert('RGB'); item['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
  item['originalSize']=list(im.size)
  for width in [480,960,1440]:
   cp=im.copy();cp.thumbnail((width,width*2));cp.save(R/'assets/photos'/f"{item['id']}-{width}.webp",'WEBP',quality=79,method=6)
  item['width'],item['height']=im.size
 except Exception as e:return dict(item,error=str(e))
 return item
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:items=list(ex.map(fetch,items))
(R/'audit/image-manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
for category in ['portrait','portfolio','property','commercial','art']:
 subset=[i for i in items if i['category']==category and not i.get('error')]
 sheet=Image.new('RGB',(1000,((len(subset)+4)//5)*190),'#efeee9'); draw=ImageDraw.Draw(sheet)
 for j,i in enumerate(subset):
  im=Image.open(R/'assets/photos'/f"{i['id']}-480.webp");im.thumbnail((190,155));xx=(j%5)*200;yy=(j//5)*190
  sheet.paste(im,(xx,yy));draw.text((xx,yy+158),i['id'],fill='black')
 sheet.save(R/'audit'/f'contact-sheet-{category}.jpg')
print('Images captured:',len(items),'errors:',sum(bool(i.get('error')) for i in items))
