import {calculate} from './pricing-engine.mjs';
const root=document.querySelector('[data-calculator]');
if(root){
 const lang=document.documentElement.lang;
 const labels={hu:{net:'Nettó',vat:'Áfa (27%)',gross:'Bruttó összesen',error:'Ellenőrizd a mezők értékeit.',custom:'Az utazás külön ajánlatot igényel; nem része az összegnek.',people:'Tervezett fotóslétszám',note:'Tájékoztató összeg, nem megrendelés.'},en:{net:'Net',vat:'VAT (27%)',gross:'Gross total',error:'Please check the field values.',custom:'Travel requires a separate quote and is not included.',people:'Planned photographers',note:'Indicative estimate, not an order.'},de:{net:'Netto',vat:'USt. (27%)',gross:'Brutto gesamt',error:'Bitte prüfe die Eingaben.',custom:'Reisen benötigen ein separates Angebot und sind nicht enthalten.',people:'Geplante Fotografen',note:'Unverbindliche Schätzung, keine Bestellung.'}}[lang];
 try{
  const response=await fetch(new URL('../pricing.json',import.meta.url));if(!response.ok)throw new Error('pricing_load');
  const data=await response.json(),get=id=>root.querySelector(`[name="${id}"]`),amount=n=>new Intl.NumberFormat(lang,{style:'currency',currency:'HUF',maximumFractionDigits:0}).format(n);
  const refresh=()=>{
   const code=get('package').value,p=[...data.packages,...data.wixPackages].find(p=>p.code===code),group=code==='group'?'group':p.group,fixed=code==='headshotcv'||group==='wix';
   for(const node of root.querySelectorAll('[data-groups]'))node.hidden=!node.dataset.groups.split(' ').includes(group)||fixed;
   root.querySelector('[data-extras]').hidden=fixed;
   root.querySelector('[data-travel]').hidden=fixed||!get('travel').checked;
   try{
    for(const node of root.querySelectorAll('input:not([type=checkbox])'))if(!node.closest('[hidden]')&&!node.checkValidity())throw new Error('invalid');
    const result=calculate(data,{code,people:get('people').value,hours:get('hours').value,images:get('images').value,guests:get('guests').value,tracks:get('tracks').value,extra:get('extra').value,addons:fixed?[]:[...root.querySelectorAll('[name=addon]:checked')].map(n=>n.value),travel:!fixed&&get('travel').checked,country:get('country').value,crew:get('crew').value});
    root.querySelector('output').textContent=`${labels.net}: ${amount(result.netHUF)} · ${labels.vat}: ${amount(result.vatHUF)} · ${labels.gross}: ${amount(result.grossHUF)}. ${labels.people}: ${result.photographers}. ${labels.note} ${result.custom.length?labels.custom:''}`;
   }catch{root.querySelector('output').textContent=labels.error}
  };
  root.hidden=false;root.addEventListener('input',refresh);refresh();
 }catch{root.hidden=true}
}
