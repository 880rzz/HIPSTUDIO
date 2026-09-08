import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const root=fileURLToPath(new URL('../',import.meta.url)).replace(/\/$/,'');
const code=fs.readFileSync(root+'/apps-script/QuoteRouting.gs','utf8');
const sandbox={console};
vm.createContext(sandbox);
vm.runInContext(code,sandbox,{filename:'QuoteRouting.gs'});
assert.equal(vm.runInContext('runRoutingSelfTest()',sandbox),true);

const now=new Date('2026-09-08T10:00:00Z');
sandbox.now=now;
function triage(payload){sandbox.payload=payload;return vm.runInContext('triage_(payload,now)',sandbox);}

const business=triage({pillars:'business',services:'accounting-finance-admin, controlling-reporting',name:'N',company:'C',email:'n@c.hu',project_summary:'Back office',business_entities:'2',business_payroll_headcount:'75',business_monthly_invoices:'350',business_countries:'HU, AT',business_engagement:'ongoing'});
assert.equal(business.queue,'BUSINESS');
assert.equal(business.priority,'HIGH');
assert.ok(business.routing_flags.includes('CROSS_BORDER_REVIEW'));
assert.equal(business.owner_suggestion,'MANUAL_ASSIGNMENT');

const creative=triage({pillars:'creative',services:'photo-event, streaming',name:'N',company:'C',email:'n@c.hu',project_summary:'Conference',creative_addons:'express, instant-retouch',photo_event_guests:'450',photo_parallel_tracks:'3',stream_viewers:'700'});
assert.equal(creative.queue,'CREATIVE');
assert.equal(creative.priority,'URGENT');
assert.ok(creative.routing_flags.includes('STREAMING_TECHNICAL_REVIEW'));
assert.ok(creative.routing_flags.includes('EXPRESS_DELIVERY'));

const cross=triage({pillars:'business, creative, experiences',services:'ai-automation, content-engine, corporate-event',name:'N',company:'C',email:'n@c.hu',project_summary:'Launch',deadline:'2026-09-10'});
assert.equal(cross.queue,'CROSS_PILLAR');
assert.equal(cross.priority,'URGENT');
assert.equal(cross.next_action,'ASSIGN_CROSS_PILLAR_LEAD');
assert.ok(cross.routing_flags.includes('MULTI_PILLAR_COORDINATION'));

const incomplete=triage({pillars:'creative',services:'photo-brand',name:'N',company:'C',email:'n@c.hu',project_summary:'Brand photos'});
assert.ok(incomplete.completeness_score<75);
assert.equal(incomplete.next_action,'REQUEST_MISSING_SCOPE_INFORMATION');

console.log('Quote routing: deterministic triage scenarios passed.');
