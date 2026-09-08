"""Append API-confirmed public gallery images; descriptions require visual review."""
import json, subprocess, hashlib, concurrent.futures
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
R=Path(__file__).resolve().parents[1]
existing=json.loads((R/'content/images.json').read_text()); data=json.loads((R/'audit/api-gallery-items.json').read_text());new=[]
for cat,items in data.items():
 old=[x for x in existing if x['category']==cat];known={x['original'] for x in old};n=len(old)
 for item in items:
  info=item['image']['imageInfo']
  if info['url'] in known:continue
  n+=1;new.append({'id':f'{cat}-{n:02}','category':cat,'sourcePage':old[0]['sourcePage'],'original':info['url'],'sourceAlt':info.get('altText',''),'publicationRights':'user_confirmed_2026-09-07','alt':{},'apiItemId':item['id']})
def fetch(item):
 path=R/'audit/raw/images'/item['id']
 if not path.exists():
  result=subprocess.run(['curl','-fsSL','--max-time','60','-o',str(path),item['original']],capture_output=True)
  if result.returncode:return dict(item,error='Source CDN download failed; '+result.stderr.decode().strip())
 im=ImageOps.exif_transpose(Image.open(path)).convert('RGB');item['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();item['originalSize']=list(im.size);item['width'],item['height']=im.size
 for width in [480,960,1440]:
  if (R/'assets/photos'/f"{item['id']}-{width}.webp").exists():continue
  cp=im.copy();cp.thumbnail((width,width*2));cp.save(R/'assets/photos'/f"{item['id']}-{width}.webp",'WEBP',quality=79,method=6)
 return item
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:new=list(ex.map(fetch,new))
(R/'audit/new-image-manifest.json').write_text(json.dumps(new,ensure_ascii=False,indent=2))
for cat in data:
 subset=[i for i in new if i['category']==cat and not i.get('error')]
 for offset in range(0,len(subset),25):
  batch=subset[offset:offset+25];sheet=Image.new('RGB',(1200,((len(batch)+4)//5)*230),'#efeee9');draw=ImageDraw.Draw(sheet)
  for j,i in enumerate(batch):
   im=Image.open(R/'assets/photos'/f"{i['id']}-480.webp");im.thumbnail((230,195));xx=j%5*240;yy=j//5*230;sheet.paste(im,(xx,yy));draw.text((xx,yy+200),i['id'],fill='black')
  sheet.save(R/'audit'/f'contact-sheet-new-{cat}-{offset}.jpg')
print('New images',len(new))
