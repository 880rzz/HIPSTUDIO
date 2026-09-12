import {chromium} from 'playwright';

const origin='http://127.0.0.1:4175';
const prefix='/HIPSTUDIO';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage();
const errors=[];
const external=new Set();
page.on('pageerror',e=>errors.push(e.message));
page.on('request',r=>{if(!r.url().startsWith(origin)&&!r.url().startsWith('data:'))external.add(r.url())});

const routes=['/','/hu/','/en/','/de/','/hu/uzleti-mukodes/','/hu/kreativ-tartalom/','/hu/vallalati-elmenyek/','/hu/rolunk/','/hu/ajanlatkeres/'];
const failures=[];
for(const width of [390,1440]){
  await page.setViewportSize({width,height:900});
  for(const route of routes){
    const response=await page.goto(origin+prefix+route,{waitUntil:'networkidle'});
    const state=await page.evaluate(()=>({
      overflow:document.documentElement.scrollWidth>innerWidth+1,
      brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length,
      h1:document.querySelectorAll('h1').length,
      robots:document.querySelector('meta[name="robots"]')?.content||''
    }));
    const isRoot=route==='/';
    if(response.status()!==200||state.overflow||state.brokenImages||(!isRoot&&state.h1!==1)){
      failures.push({route,width,status:response.status(),...state});
    }
  }
}

// Mobile language switching is intentionally inside the fullscreen menu.
// Exercise the actual accessible interaction instead of relying on the legacy
// always-visible language links that the editorial shell replaced.
await page.setViewportSize({width:390,height:844});
await page.goto(origin+prefix+'/hu/',{waitUntil:'networkidle'});
const menuToggle=page.locator('[data-menu-toggle]');
await menuToggle.click();
const menuOverlay=page.locator('[data-menu-overlay]');
const menuOpen=await menuOverlay.isVisible();
const enLink=menuOverlay.locator('a[lang="en"][hreflang="en"]').first();
const enHref=await enLink.getAttribute('href');
await enLink.click();
await page.waitForURL(origin+prefix+'/en/');
const languageSwitch=page.url()===origin+prefix+'/en/';

await page.goto(origin+prefix+'/hu/ajanlatkeres/',{waitUntil:'networkidle'});
const formAction=await page.locator('[data-quote-form]').getAttribute('action');
const submitDisabled=await page.locator('[data-quote-form] [type=submit]').isDisabled();

console.log(JSON.stringify({failures,errors,externalRequests:[...external],menuOpen,enHref,languageSwitch,formAction,submitDisabled},null,2));
await browser.close();

if(failures.length||errors.length||external.size||!menuOpen||enHref!==prefix+'/en/'||!languageSwitch||formAction!==null||!submitDisabled){
  process.exitCode=1;
}
