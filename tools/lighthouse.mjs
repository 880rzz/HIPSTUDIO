import {fileURLToPath} from 'node:url';
import lighthouse from 'lighthouse';import * as chromeLauncher from 'chrome-launcher';import fs from 'node:fs';
const root=fileURLToPath(new URL('../audit',import.meta.url));const results=[];
for(const [name,path] of (process.env.LH_TARGETS?JSON.parse(process.env.LH_TARGETS):[['home','/hu/'],['service','/hu/szolgaltatasok/uzleti-portre/'],['pricing','/hu/arak/'],['gallery','/hu/munkaink/']])){
 for(const mode of ['mobile','desktop']){
  const chrome=await chromeLauncher.launch({...(process.env.CHROME_PATH?{chromePath:process.env.CHROME_PATH}:{}),chromeFlags:['--headless','--disable-gpu']});
  const options={port:chrome.port,output:'json',logLevel:'error',onlyCategories:['performance','accessibility','best-practices','seo'],...mode==='desktop'?{formFactor:'desktop',screenEmulation:{mobile:false,width:1350,height:940,deviceScaleFactor:1,disabled:false},throttling:{rttMs:40,throughputKbps:10240,cpuSlowdownMultiplier:1,requestLatencyMs:0,downloadThroughputKbps:0,uploadThroughputKbps:0}}:{}};
  const result=await lighthouse('http://127.0.0.1:4173'+path,options);fs.writeFileSync(`${root}/lighthouse-${name}-${mode}.json`,result.report);
  const row={name,path,mode,version:result.lhr.lighthouseVersion,scores:Object.fromEntries(Object.entries(result.lhr.categories).map(([k,v])=>[k,Math.round(v.score*100)])),metrics:Object.fromEntries(['first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index'].map(k=>[k,result.lhr.audits[k].numericValue])),failed:Object.entries(result.lhr.audits).filter(([k,v])=>v.score!==null&&v.score<1).map(([k,v])=>({id:k,title:v.title,score:v.score,details:v.displayValue}))};results.push(row);console.log(JSON.stringify(row));await chrome.kill();
 }
}
fs.writeFileSync(root+'/'+(process.env.QA_REPORT||'lighthouse-summary.json'),JSON.stringify({time:new Date().toISOString(),context:'Local HTTP review build with noindex, not live PageSpeed or field data',results},null,2));
