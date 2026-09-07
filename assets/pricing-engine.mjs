// HUF-only pricing. Preserve approved BANHALMI gross amounts; split 27% VAT.
export function calculate(data,input){
 const integer=(value,min=0)=>{const n=Number(value);if(!Number.isSafeInteger(n)||n<min||n>100000)throw new Error('invalid_input');return n};
 const c=data.components,code=input.code;
 const p=[...data.packages,...data.wixPackages].find(p=>p.code===code);
 if(!p&&code!=='group')throw new Error('unknown_package');
 let gross=p?.grossHUF||0,photographers=1,custom=[];
 if(code==='group'){
  const people=integer(input.people,1),hours=Number(input.hours),images=integer(input.images,1);
  if(!Number.isFinite(hours)||hours<=0||hours>24)throw new Error('invalid_hours');
  photographers=Math.max(1,Math.ceil(people/(6*hours)));
  gross=c.groupSetupLaterRetouching+people*c.groupPerPersonLaterRetouching+people*Math.max(0,images-1)*c.retouchedImageGroup+Math.max(0,photographers-1)*c.additionalPhotographer;
 }else if(p.group==='portrait'&&code!=='headshotcv'){
  gross+=Math.max(0,integer(input.images,1)-1)*c.retouchedImagePortrait;
 }else if(p.group==='brand-visual-positioning'){
  gross+=Math.max(0,integer(input.people,1)*integer(input.images,1)-3)*c.retouchedImagePortrait;
 }else if(p.group==='fine-art'){
  gross+=Math.max(0,integer(input.images,1)-2)*c.retouchedImageFineArt;
 }else if(p.group==='event'){
  const guests=integer(input.guests,1),tracks=integer(input.tracks,1),extra=integer(input.extra,0);
  photographers=1+Math.max(extra,tracks-1,Math.ceil(guests/250)-1);
  gross+=(photographers-1)*(p.durationMinutes/60)*c.additionalPhotographerEventPerHour;
 }
 // Fixed headshot and Wix packages must not receive automatic extra options.
 if(code==='headshotcv'||p?.group==='wix'){
  if((input.addons||[]).length||input.travel)throw new Error('fixed_package_options');
 }else{
  const allowed=['stylist','hair','makeup','expressDelivery','mobileStudio','artDirection'];
  for(const addon of new Set(input.addons||[])){if(!allowed.includes(addon))throw new Error('unknown_addon');gross+=c[addon]}
  if(input.travel){
   if(['HU','AT'].includes(input.country))gross+=Math.ceil(integer(input.crew,1)/4)*c.travelPerVehicleGross;
   else custom.push('travel');
  }
 }
 if(!Number.isSafeInteger(gross)||gross<0)throw new Error('invalid_total');
 const net=Math.round(gross/1.27),vat=gross-net;
 return {currency:'HUF',grossHUF:gross,netHUF:net,vatHUF:vat,photographers,custom};
}
