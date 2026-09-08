# coding:utf-8
from pathlib import Path
import json,subprocess,concurrent.futures
R=Path(__file__).resolve().parents[1]
x=json.loads((R/'audit/raw/video-complete.json').read_text())['appsWarmupData'];rows=[]
for gs in x.values():
 for group,g in gs.items():
  if not isinstance(g,dict) or not isinstance(g.get('items'),list):continue
  for item in g['items']:
   m=item['metaData'];qualities=m['qualities'];quality=next((q for q in qualities if q['height']==720),min(qualities,key=lambda q:abs(q['height']-720)))['quality']
   rows.append({'id':item['itemId'],'sourceTitle':m['title'].strip(),'group':group,'durationMs':m['duration'],'url':'https://video.wixstatic.com/video/'+item['mediaUrl']+'/'+quality+'/mp4/file.mp4','sourcePage':'https://www.hipstudio.hu/referencia-vide%C3%B3k','hosting':'Wix public media CDN; opens only on explicit link activation'})
rows.insert(0,{'id':'showreel','sourceTitle':'HIPStudio ShowReel','group':'showreel','url':'https://video.wixstatic.com/video/b0aee1_bdce417615614253a25aaedeb7af65e3/1080p/mp4/file.mp4','sourcePage':'https://www.hipstudio.hu/referencia-vide%C3%B3k','hosting':'Wix public media CDN; opens only on explicit link activation'})
def check(row):
 res=subprocess.run(['curl','-sSL','-I','--max-time','25','-o','/dev/null','-w','%{http_code}',row['url']],capture_output=True,text=True);row['verifiedHttpStatus']=int(res.stdout) if res.stdout.isdigit() else None;return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(check,rows))
(R/'content/videos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print([(r['id'],r['verifiedHttpStatus']) for r in rows])
