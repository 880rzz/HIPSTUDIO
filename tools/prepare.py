# coding: utf-8
"""Prepare audited editorial data; does not publish or change remote services."""
raise SystemExit("Historical import disabled: edit content/*.json directly; this script would overwrite reviewed content and approvals.")
from pathlib import Path
import json,sys
from decimal import Decimal, ROUND_HALF_UP
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'content'))
from services import SERVICES,PENDING,tr
from image_descriptions import DESCRIPTIONS
images=json.loads((R/'audit/image-manifest.json').read_text())
for i in images:
 i['alt']=DESCRIPTIONS[i['id']]
 i['publicationRights']='user_confirmed_2026-09-07'
 i['visualReview']='contact_sheet_2026-09-07'
(R/'content/images.json').write_text(json.dumps(images,ensure_ascii=False,indent=2))
(R/'content/services.json').write_text(json.dumps(SERVICES,ensure_ascii=False,indent=2))
(R/'audit/pending-services.json').write_text(json.dumps(PENDING,ensure_ascii=False,indent=2))
source=json.load(open('/private/tmp/hipstudio-banhalmi-source/pricing-huf.json'))
def split(gross):
 net=int((Decimal(gross)/Decimal('1.27')).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
 return {'grossHUF':gross,'netHUF':net,'vatHUF':gross-net}
packages=[]
for s in source['services']:
 for p in s['packages']:
  name={k:s['name'][('de-AT' if k=='de' else k)] for k in ['hu','en','de']}
  packages.append({'code':p['code'],'group':s['id'],'name':name,'durationMinutes':p.get('durationMinutes',p.get('durationHours',0)*60),'includedImages':p.get('includedRetouchedImages',s.get('includedRetouchedImages',1 if s['id']=='portrait' else None)),**split(p['grossHUF']),'source':'BANHALMI gross preserved; user approved 27% VAT split'})
wix=[]
for code,label,net,minutes,count in [('wix-cv','CV / Önéletrajz || CV photography || Bewerbungsfotos',34990,30,1),('wix-business','Üzleti / kreatív portré || Business / creative portrait || Business- / Kreativporträt',64990,60,3),('wix-dating','Mini portfólió / társkereső || Mini portfolio / dating || Miniportfolio / Dating',84990,90,6),('wix-portfolio','Portfólió és divat || Portfolio and fashion || Portfolio und Mode',139990,180,20),('wix-nude','Művészi akt || Fine-art nude || Künstlerischer Akt',139990,180,20),('wix-boudoir','Glamour / boudoir || Glamour / boudoir || Glamour / Boudoir',94990,120,10)]:
 vat=int((Decimal(net)*Decimal('.27')).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
 wix.append({'code':code,'group':'wix','name':tr(label),'durationMinutes':minutes,'includedImages':count,'netHUF':net,'vatHUF':vat,'grossHUF':net+vat,'source':'Wix higher NET amount confirmed by user; VAT27 added; whole-HUF half-up rounding'})
pricing={'currency':'HUF','vatRate':27,'dateModified':'2026-09-07','status':'indicative_user_approved','sourceCommit':'c3bc1143254a467cb8d47091e84acc2aac361ebc','packages':packages,'wixPackages':wix,'components':source['priceComponentsGrossHUF'],'rounding':'Whole HUF, half up. BANHALMI net=round(gross/1.27), VAT=gross-net. Wix approved net retained, VAT=round(net*0.27). No currency conversion.','offerSchema':False}
(R/'content/pricing.json').write_text(json.dumps(pricing,ensure_ascii=False,indent=2))
(R/'content/approvals.json').write_text(json.dumps({'imageRights':True,'pricing':True,'legal':False,'publication':False,'domainAndDns':False,'studioRentalTerms':False,'notes':'Image rights and pricing approved by user on 2026-09-07. Publication explicitly requires separate approval.'},indent=2))
print(len(SERVICES),'services;',len(images),'reviewed images;',len(packages)+len(wix),'price packages')
