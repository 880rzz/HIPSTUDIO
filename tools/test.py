"""Semantic release checks across every generated route; standard library only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,sys,re,subprocess,os,unittest,tempfile,shutil
R=Path(__file__).resolve().parents[1];D=R/'dist'
class Doc(HTMLParser):
 def __init__(self,raw):
  super().__init__();self.tags=[];self.ids=set();self.text=[];self.ld=[];self.in_ld=False;self.json='';self.feed(raw)
 def handle_starttag(self,t,a):
  a=dict(a);self.tags.append((t,a));
  if a.get('id'):self.ids.add(a['id'])
  if t=='script' and a.get('type')=='application/ld+json':self.in_ld=True;self.json=''
 def handle_endtag(self,t):
  if t=='script' and self.in_ld:self.ld.append(json.loads(self.json));self.in_ld=False
 def handle_data(self,t):
  if self.in_ld:self.json+=t
  else:self.text.append(t)
 def select(self,t,**a):return [v for tag,v in self.tags if tag==t and all(v.get(k)==val for k,val in a.items())]
class ReleaseTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.build=json.loads((R/'audit/build.json').read_text());cls.docs={p['path']:Doc((D/p['path'].strip('/')/'index.html').read_text()) for p in cls.build['pages']}
 def test_all_languages_and_metadata(self):
  pages=self.build['pages'];self.assertEqual(len(pages),159)
  for p in pages:
   with self.subTest(path=p['path']):
    d=self.docs[p['path']];self.assertEqual(len(d.select('h1')),1);self.assertEqual(d.select('html')[0]['lang'],p['lang'])
    self.assertEqual(d.select('link',rel='canonical')[0]['href'],p['url'])
    self.assertEqual({x['hreflang'] for x in d.select('link',rel='alternate')},{'hu','en','de','x-default'})
    self.assertTrue(d.select('meta',name='description')[0]['content']);self.assertTrue(d.select('meta',property='og:image'))
    self.assertEqual(d.select('meta',name='robots')[0]['content'],'noindex,nofollow')
    for alt in d.select('link',rel='alternate'):
     target=unquote(urlsplit(alt['href']).path);self.assertIn(target,self.docs)
     self.assertTrue(any(x['href']==p['url'] for x in self.docs[target].select('link',rel='alternate')))
 def test_links_fragments_and_local_assets(self):
  for path,d in self.docs.items():
   for t,a in d.tags:
    attr='href' if t in ['a','link'] else 'src' if t in ['img','script'] else None
    u=a.get(attr) if attr else None
    if not u:continue
    parsed=urlsplit(u)
    if parsed.scheme or parsed.netloc:continue
    target=unquote(parsed.path) or path;dest=D/target.lstrip('/')
    if target.endswith('/'):dest=dest/'index.html'
    self.assertTrue(dest.is_file(),f'{path}: missing {u}')
    if parsed.fragment:
     td=self.docs.get(target) or Doc(dest.read_text());self.assertIn(unquote(parsed.fragment),td.ids,f'{path}: missing fragment {u}')
 def test_schema_and_visible_faq(self):
  for path,d in self.docs.items():
   self.assertEqual(len(d.ld),1);g=d.ld[0]['@graph'];ids=[n['@id'] for n in g];self.assertEqual(len(ids),len(set(ids)))
   types=[n['@type'] for n in g];self.assertIn('WebSite',types);self.assertIn('ContactPoint',types);self.assertIn('BreadcrumbList',types)
   text=' '.join(d.text)
   for n in g:
    if n['@type']=='FAQPage':
     for q in n['mainEntity']:
      self.assertIn(q['name'],text);self.assertIn(q['acceptedAnswer']['text'],text)
    self.assertNotIn('Offer',n['@type']);self.assertNotIn('AggregateRating',n['@type'])
 def test_images_and_no_tracking(self):
  for path,d in self.docs.items():
   self.assertFalse(d.select('iframe'));self.assertFalse(d.select('form'))
   for m in d.select('img'):
    self.assertTrue(m['alt'].strip());self.assertGreater(int(m['width']),0);self.assertGreater(int(m['height']),0);self.assertTrue(m['src'].startswith('/assets/'))
   for t,a in d.tags:
    if t in ['script','link','img'] and (a.get('src','').startswith('http') or a.get('rel')=='stylesheet' and a.get('href','').startswith('http')):self.fail(f'external automatic resource: {path}')
 def test_gallery_has_no_cross_category_duplicates(self):
  for lang,path in [('hu','munkaink'),('en','work'),('de','arbeiten')]:
   raw=(D/lang/path/'index.html').read_text()
   gallery_sources=re.findall(r'<div class="gallery">(.*?)</div>',raw,re.S)
   sources=[]
   for gallery in gallery_sources:sources+=re.findall(r'<img src="/assets/photos/([^"/]+)-960\.webp',gallery)
   self.assertEqual(len(sources),len(set(sources)),lang)
   self.assertTrue(all('© HIPStudio' in gallery for gallery in gallery_sources))
 def test_pricing_tax_invariants(self):
  p=json.loads((R/'content/pricing.json').read_text());self.assertEqual(p['currency'],'HUF');self.assertEqual(p['vatRate'],27)
  expected={'headshotcv':48000,'quick30':88000,'guided60':168000,'guided120':276000,'brand60':199600,'brand120':316000,'brand180':436000,'brand240':556000,'art60':276000,'art120':396000,'art180':516000,'event60':236000,'event120':356000,'event180':476000,'event240':596000,'eventFullDay':996000}
  for row in p['packages']+p['wixPackages']:
   self.assertEqual(row['netHUF']+row['vatHUF'],row['grossHUF'])
   self.assertLessEqual(abs(row['netHUF']*.27-row['vatHUF']),.7)
  self.assertEqual({r['code']:r['grossHUF'] for r in p['packages']},expected)
  self.assertEqual(next(r for r in p['wixPackages'] if r['code']=='wix-nude')['netHUF'],139990)
 def test_production_is_blocked(self):
  env=dict(os.environ,BUILD_MODE='production')
  result=subprocess.run([sys.executable,str(R/'tools/build.py')],env=env,capture_output=True,text=True)
  self.assertNotEqual(result.returncode,0);self.assertIn('legal, publication',result.stderr)
 def test_production_output_contract_with_synthetic_gates(self):
  with tempfile.TemporaryDirectory() as temp:
   target=Path(temp)
   shutil.copytree(R/'content',target/'content');shutil.copytree(R/'tools',target/'tools');(target/'audit').mkdir();(target/'assets').symlink_to(R/'assets',target_is_directory=True)
   approvals=json.loads((target/'content/approvals.json').read_text())
   for key in ['imageRights','pricing','legal','publication']:approvals[key]=True
   (target/'content/approvals.json').write_text(json.dumps(approvals))
   result=subprocess.run([sys.executable,str(target/'tools/build.py')],env=dict(os.environ,BUILD_MODE='production',SITE_URL='https://www.hipstudio.hu'),capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   self.assertEqual((target/'dist/robots.txt').read_text(),'User-agent: *\nAllow: /\nSitemap: https://www.hipstudio.hu/sitemap.xml\n')
   sitemap=(target/'dist/sitemap.xml').read_text();self.assertEqual(sitemap.count('<url>'),159)
   home=Doc((target/'dist/hu/index.html').read_text());self.assertEqual(home.select('meta',name='robots')[0]['content'],'index,follow')
 def test_old_url_coverage(self):
  inventory=json.loads((R/'audit/source-inventory.json').read_text());mapping=json.loads((R/'audit/url-mapping.json').read_text())
  mapped={unquote(urlsplit(p['old']).path).rstrip('/') for p in mapping}
  for p in inventory['pages']:self.assertIn(unquote(urlsplit(p['url']).path).rstrip('/'),mapped)
  for m in mapping:
   self.assertTrue((D/unquote(urlsplit(m['old']).path).strip('/')/'index.html').exists())
  old_paths={urlsplit(item['old']).path for item in mapping}
  self.assertEqual(len(old_paths),len(mapping))
  for item in mapping:
   self.assertNotEqual(urlsplit(item['old']).path,urlsplit(item['new']).path)
   self.assertNotIn(urlsplit(item['new']).path,old_paths)
   self.assertEqual(item['plannedHttpStatus'],301);self.assertEqual(item['actualPagesStatus'],200)
 def test_github_project_base_path(self):
  with tempfile.TemporaryDirectory() as temp:
   target=Path(temp)
   shutil.copytree(R/'content',target/'content');shutil.copytree(R/'tools',target/'tools');(target/'audit').mkdir();(target/'assets').symlink_to(R/'assets',target_is_directory=True)
   env=dict(os.environ,SITE_URL='https://880rzz.github.io/HIPSTUDIO',BUILD_MODE='review')
   result=subprocess.run([sys.executable,str(target/'tools/build.py')],env=env,capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   d=Doc((target/'dist/en/index.html').read_text())
   self.assertEqual(d.select('link',rel='canonical')[0]['href'],'https://880rzz.github.io/HIPSTUDIO/en/')
   for tag,a in d.tags:
    for attr in ['href','src']:
     u=a.get(attr,'')
     if u.startswith('/'):self.assertTrue(u.startswith('/HIPSTUDIO/'),u)
 def test_no_automatic_deployment(self):
  self.assertFalse((R/'.github/workflows/deploy.yml').exists());self.assertFalse((D/'CNAME').exists())
 def test_solution_people_case_and_trust_architecture(self):
  solutions=json.loads((R/'content/solutions.json').read_text());services={item['key'] for item in json.loads((R/'content/services.json').read_text())}
  self.assertEqual(len(solutions),5)
  for solution in solutions:
   self.assertEqual(set(solution['slug']),{'hu','en','de'});self.assertTrue(set(solution['services'])<=services)
   for lang in ['hu','en','de']:
    self.assertTrue((D/lang/({'hu':'megoldasok','en':'solutions','de':'loesungen'}[lang])/solution['slug'][lang]/'index.html').exists())
  people=json.loads((R/'content/people.json').read_text());self.assertEqual({p['name'] for p in people},{'Bánhalmi Norbert','Speier Vikó'})
  cases=json.loads((R/'content/case_studies.json').read_text());self.assertEqual(cases['items'],[])
  self.assertTrue((R/'content/case-study.schema.json').exists())
  for path in ['provenance.json','entity.json','privacy-config.json','llms.txt']:self.assertTrue((D/path).exists(),path)
  provenance=json.loads((D/'provenance.json').read_text())
  self.assertTrue(all(len(source.get('sha256',''))==64 for source in provenance['sources'].values()))
  self.assertIn('Case studies remain unpublished', (D/'llms.txt').read_text())
 def test_privacy_hooks_are_inert(self):
  config=json.loads((R/'content/privacy-config.json').read_text());self.assertFalse(config['storageEnabled']);self.assertFalse(config['networkActivationEnabled']);self.assertEqual(config['optionalIntegrations'],[])
  consent=(R/'assets/consent.mjs').read_text()
  for token in ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'document.cookie']:self.assertNotIn(token,consent)
  redirects=json.loads((R/'ops/redirects.json').read_text());self.assertEqual(redirects['status'],'inactive-plan')
  self.assertFalse(any((R/name).exists() for name in ['wrangler.toml','_redirects']))
 def test_gallery_accounting_and_pending_exclusion(self):
  active=json.loads((R/'content/images.json').read_text())
  pending=json.loads((R/'audit/pending-images.json').read_text())
  all_images=active+pending
  self.assertEqual(len({i['id'] for i in all_images}),221)
  for category,count in {'portrait':30,'portfolio':51,'property':46,'commercial':78,'art':16}.items():
   self.assertEqual(sum(i['category']==category for i in all_images),count)
  for item in pending:
   self.assertFalse((D/'assets/photos'/f"{item['id']}-960.webp").exists())
  for item in active:
   self.assertEqual(set(item['alt']),{'hu','en','de'})
   self.assertTrue(all(item['alt'].values()))
if __name__=='__main__':unittest.main(verbosity=2)
