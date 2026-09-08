import {chromium} from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';

const root=fileURLToPath(new URL('../',import.meta.url)).replace(/\/$/,'');
const build=JSON.parse(fs.readFileSync(root+'/dist-platform/platform-build.json'));
const origin='http://127.0.0.1:4174';
const browser=await chromium.launch({...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),headless:true});
const context=await browser.newContext();
const page=await context.newPage();
const errors=[];const external=new Set();const results=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('request',r=>{if(!r.url().startsWith(origin)&&!r.url().startsWith('data:'))external.add(r.url())});

const representative=['/hu/','/en/','/de/','/hu/uzleti-mukodes/','/hu/kreativ-tartalom/','/hu/vallalati-elmenyek/','/hu/megoldasok/','/hu/megoldasok/business-operations-360/','/hu/megoldasok/content-engine/','/hu/ai-trust/','/hu/kapcsolat/','/hu/ajanlatkeres/'];
for(const width of [320,390,768,1440,1920]){
  await page.setViewportSize({width,height:960});
  const paths=width===390?build.pages.map(p=>p.path):representative;
  for(const path of paths){
    const response=await page.goto(origin+path,{waitUntil:'networkidle'});
    const geometry=await page.evaluate(()=>({
      overflow:document.documentElement.scrollWidth>innerWidth+1,
      scrollWidth:document.documentElement.scrollWidth,
      viewport:innerWidth,
      h1:document.querySelectorAll('h1').length,
      review:document.querySelectorAll('.review').length,
      brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length
    }));
    let violations=[];
    if(width===390||width===1440){
      violations=(await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze()).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length}));
    }
    results.push({path,width,status:response.status(),...geometry,violations});
  }
}

await page.setViewportSize({width:390,height:844});
await page.goto(origin+'/hu/');
const skip=page.locator('.skip');
const skipHref=await skip.getAttribute('href');
await skip.focus();
const skipFocused=await skip.evaluate(el=>document.activeElement===el);
await page.keyboard.press('Enter');
const skipTarget=await page.evaluate(()=>location.hash==='#main'&&!!document.querySelector('#main'));
await page.getByRole('link',{name:'EN',exact:true}).click();
const languageSwitch=page.url().endsWith('/en/');

await page.goto(origin+'/hu/ajanlatkeres/');
await page.locator('[name=pillars][value=creative]').check();
const creativeServiceVisible=await page.locator('[data-services=creative]').isVisible();
await page.locator('[name=services][value=photo-business-portrait]').check();
const creativeScopeVisible=await page.locator('[data-creative-scope]').isVisible();
const photoScopeVisible=await page.getByText('Fotó-specifikus adatok',{exact:true}).isVisible();
const quoteSubmitDisabled=await page.locator('[data-quote-form] [type=submit]').isDisabled();
const internalEmailsExposed=await page.locator('body').evaluate(el=>/nemeth\.timea@hipstudio\.hu|banhalmi\.norbert@hipstudio\.hu/.test(el.innerText+el.innerHTML));

const cookies=await context.cookies();
const storage=await page.evaluate(()=>({localStorage:localStorage.length,sessionStorage:sessionStorage.length}));

const summary={time:new Date().toISOString(),browser:await browser.version(),tested:results.length,results,errors,externalRequests:[...external],cookies,storage,interactions:{skipHref,skipFocused,skipTarget,languageSwitch,creativeServiceVisible,creativeScopeVisible,photoScopeVisible,quoteSubmitDisabled,internalEmailsExposed}};
fs.writeFileSync(root+'/audit/browser-platform-qa.json',JSON.stringify(summary,null,2));
console.log(JSON.stringify({tested:results.length,overflow:results.filter(r=>r.overflow).length,axeFailures:results.filter(r=>r.violations.length).length,errors,externalRequests:[...external],cookies:cookies.length,storage,interactions:summary.interactions},null,2));
await browser.close();
if(results.some(r=>r.status!==200||r.overflow||r.brokenImages||r.h1!==1||r.review!==1||r.violations.length)||errors.length||external.size||cookies.length||storage.localStorage||storage.sessionStorage||skipHref!=='#main'||!skipFocused||!skipTarget||!languageSwitch||!creativeServiceVisible||!creativeScopeVisible||!photoScopeVisible||!quoteSubmitDisabled||internalEmailsExposed)process.exitCode=1;
