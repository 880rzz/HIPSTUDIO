import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {calculate} from '../assets/pricing-engine.mjs';
const p=JSON.parse(readFileSync(new URL('../content/pricing.json',import.meta.url)));
const base={images:1,people:1,hours:1,guests:100,tracks:1,extra:0,addons:[],travel:false};
const calc=x=>calculate(p,{...base,...x});
assert.equal(calc({code:'guided60',images:5}).grossHUF,224000);
assert.equal(calc({code:'group',people:12,images:2,hours:1}).grossHUF,667200);
assert.equal(calc({code:'brand120',people:2,images:3}).grossHUF,358000);
assert.equal(calc({code:'event240',guests:400,tracks:2}).grossHUF,788000);
assert.equal(calc({code:'event240',guests:400,tracks:2,images:1000}).grossHUF,788000);
assert.equal(calc({code:'headshotcv',images:500}).grossHUF,48000);
assert.equal(calc({code:'art60',images:4}).grossHUF,312000);
assert.equal(calc({code:'guided60',travel:true,country:'HU',crew:5}).grossHUF,360000);
assert.equal(calc({code:'guided60',addons:['makeup','makeup']}).grossHUF,256000);
assert.deepEqual(calc({code:'guided60',travel:true,country:'US',crew:1}).custom,['travel']);
assert.throws(()=>calc({code:'group',people:0}));
assert.throws(()=>calc({code:'group',hours:0}));
assert.throws(()=>calc({code:'unknown'}));
assert.throws(()=>calc({code:'headshotcv',addons:['makeup']}));
assert.throws(()=>calc({code:'guided60',images:NaN}));
assert.throws(()=>calc({code:'guided60',addons:['invented']}));
for(const pack of [...p.packages,...p.wixPackages]){
 const r=calc({code:pack.code});assert.equal(r.grossHUF,r.netHUF+r.vatHUF);assert.ok(Math.abs(r.netHUF*1.27-r.grossHUF)<1);
}
console.log('Pricing: 16 scenarios plus all 22 tax invariants passed.');
