import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
const root=fileURLToPath(new URL('../',import.meta.url)).replace(/\/$/,'');
const build=JSON.parse(fs.readFileSync(root+'/audit/build.json'));
const browser=await chromium.launch({...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),headless:true});
const errors=[],results=[];
const context=await browser.newContext();
const page=await context.newPage();
page.on('pageerror',e=>errors.push(e.message));
const external=new Set();page.on('request',r=>{if(!r.url().startsWith('http://127.0.0.1:4173')&&!r.url().startsWith('data:'))external.add(r.url())});
for(const width of [320,390,768,1440,1920]){
 await page.setViewportSize({width,height:960});
 const paths=process.env.QA_PATHS?JSON.parse(process.env.QA_PATHS):width===390?build.pages.map(p=>p.path):['/hu/','/en/','/de/','/hu/arak/','/de/leistungen/executive-portraets/','/hu/gyik/','/hu/kapcsolat/','/hu/munkaink/'];
 for(const path of paths){
  const response=await page.goto('http://127.0.0.1:4173'+path,{waitUntil:'networkidle'});
  const geometry=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,brokenImages:[...document.images].filter(i=>i.loading!=='lazy'&&(!i.complete||i.naturalWidth===0)).length,h1:document.querySelectorAll('h1').length}));
  let violations=[];
  if(width===390||width===1440)violations=(await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze()).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}));
  results.push({path,width,status:response.status(),...geometry,violations});
  if(path==='/hu/'&&[320,390,1440].includes(width))await page.screenshot({path:root+`/audit/home-${width}.png`,fullPage:true});
 }
 console.log('Viewport complete:',width);
}
await page.setViewportSize({width:390,height:844});await page.goto('http://127.0.0.1:4173/hu/');
await page.keyboard.press('Tab');const skip=await page.locator(':focus').textContent();await page.keyboard.press('Enter');const skipTarget=await page.locator(':focus').getAttribute('id');
await page.locator('.mobile-menu summary').click();const mobileOpen=await page.locator('.mobile-menu').getAttribute('open')!==null;
await page.getByRole('link',{name:'EN',exact:true}).click();const switched=page.url().endsWith('/en/');
await page.goto('http://127.0.0.1:4173/hu/gyik/');const first=page.locator('.faq-list summary').first();await first.focus();await page.keyboard.press('Enter');const faqOpen=await page.locator('.faq-list details').first().getAttribute('open')!==null;
await page.goto('http://127.0.0.1:4173/hu/arak/');await page.locator('[name=package]').selectOption('brand120');await page.locator('[name=people]').fill('2');await page.locator('[name=images]').fill('3');const quoteText=await page.locator('output').textContent();
const unknown=await page.goto('http://127.0.0.1:4173/does-not-exist');const actual404=unknown.status();
await page.goto('http://127.0.0.1:4173/service-page/cv-%C3%B6n%C3%A9letrajz-fot%C3%B3z%C3%A1s/');await page.waitForURL('**/hu/szolgaltatasok/oneletrajz-foto/');const redirect=page.url();
const cookies=await context.cookies();
const summary={time:new Date().toISOString(),browser:await browser.version(),results,errors,externalRequests:[...external],cookies,interactions:{skip,skipTarget,mobileOpen,switched,faqOpen,quoteText,actual404,redirect}};
fs.writeFileSync(root+'/audit/'+(process.env.QA_REPORT||'browser-qa.json'),JSON.stringify(summary,null,2));
console.log(JSON.stringify({tested:results.length,overflow:results.filter(r=>r.overflow).length,axeFailures:results.filter(r=>r.violations.length).length,errors,externalRequests:[...external],interactions:summary.interactions},null,2));
await browser.close();
if(results.some(r=>r.status!==200||r.overflow||r.brokenImages||r.h1!==1||r.violations.length)||errors.length||external.size||cookies.length||skipTarget!=='main'||!mobileOpen||!switched||!faqOpen||actual404!==404||!quoteText.replace(/\s/g,'').includes('358000'))process.exitCode=1;
