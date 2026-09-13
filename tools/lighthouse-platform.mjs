import {fileURLToPath} from 'node:url';
import fs from 'node:fs';
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

const auditDir=fileURLToPath(new URL('../audit',import.meta.url));
const baseUrl=process.env.LH_BASE_URL||'http://127.0.0.1:4174';
const context=process.env.LH_CONTEXT||'review';
const targets=process.env.LH_TARGETS?JSON.parse(process.env.LH_TARGETS):[
  ['home','/hu/'],
  ['creative','/hu/kreativ-tartalom/'],
  ['contact','/hu/kapcsolat/'],
  ['ai-trust','/hu/ai-trust/']
];
const seoMinimum=context==='production'
  ? Number(process.env.LH_MIN_SEO||90)
  : Number(process.env.LH_REVIEW_MIN_SEO||65);
const thresholds={
  performance:Number(process.env.LH_MIN_PERFORMANCE||80),
  accessibility:Number(process.env.LH_MIN_ACCESSIBILITY||95),
  'best-practices':Number(process.env.LH_MIN_BEST_PRACTICES||95),
  seo:seoMinimum
};
const metricLimits={
  'largest-contentful-paint':Number(process.env.LH_MAX_LCP_MS||3500),
  'total-blocking-time':Number(process.env.LH_MAX_TBT_MS||300),
  'cumulative-layout-shift':Number(process.env.LH_MAX_CLS||0.1)
};
const results=[];
const failures=[];

for(const [name,path] of targets){
  for(const mode of ['mobile','desktop']){
    const chrome=await chromeLauncher.launch({
      ...(process.env.CHROME_PATH?{chromePath:process.env.CHROME_PATH}:{}),
      chromeFlags:['--headless','--disable-gpu','--no-sandbox']
    });
    try{
      const options={
        port:chrome.port,
        output:'json',
        logLevel:'error',
        onlyCategories:['performance','accessibility','best-practices','seo'],
        ...(mode==='desktop'?{
          formFactor:'desktop',
          screenEmulation:{mobile:false,width:1440,height:960,deviceScaleFactor:1,disabled:false},
          throttling:{rttMs:40,throughputKbps:10240,cpuSlowdownMultiplier:1,requestLatencyMs:0,downloadThroughputKbps:0,uploadThroughputKbps:0}
        }:{})
      };
      const result=await lighthouse(baseUrl+path,options);
      if(!result?.lhr) throw new Error(`Lighthouse returned no result for ${path} (${mode})`);
      fs.writeFileSync(`${auditDir}/lighthouse-platform-${name}-${mode}.json`,result.report);
      const scores=Object.fromEntries(Object.entries(result.lhr.categories).map(([key,value])=>[key,Math.round(value.score*100)]));
      const metrics=Object.fromEntries(Object.keys(metricLimits).map(key=>[key,result.lhr.audits[key].numericValue]));
      const row={name,path,mode,version:result.lhr.lighthouseVersion,scores,metrics};
      results.push(row);
      for(const [category,min] of Object.entries(thresholds)){
        if((scores[category]??0)<min) failures.push(`${name}/${mode}: ${category} ${scores[category]??0} < ${min}`);
      }
      for(const [metric,max] of Object.entries(metricLimits)){
        if((metrics[metric]??Infinity)>max) failures.push(`${name}/${mode}: ${metric} ${metrics[metric]} > ${max}`);
      }
      console.log(JSON.stringify(row));
    } finally {
      await chrome.kill();
    }
  }
}

const summary={
  time:new Date().toISOString(),
  context,
  note:context==='review'
    ? 'Review builds are intentionally noindex. The review SEO floor only guards unexpected Lighthouse regressions; production SEO remains gated at >=90 plus the canonical metadata/indexability regression suite.'
    : 'Production Lighthouse SEO threshold is enforced at >=90.',
  baseUrl,
  thresholds,
  metricLimits,
  results,
  failures
};
fs.writeFileSync(`${auditDir}/lighthouse-platform-summary.json`,JSON.stringify(summary,null,2));
if(failures.length){
  console.error('Platform Lighthouse release gate failed:\n'+failures.map(item=>`- ${item}`).join('\n'));
  process.exit(1);
}
console.log(`Platform Lighthouse ${context} gate passed for ${results.length} audits.`);
