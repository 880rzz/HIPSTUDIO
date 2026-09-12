(()=>{
  const header=document.querySelector('.header');
  const sourceNav=header?.querySelector('.nav');
  const langs=header?.querySelector('.langs');
  if(!header||!sourceNav)return;

  const copy={
    hu:{menu:'Menü',close:'Bezárás',label:'Fő navigáció',note:'Azt keresd, amit meg kell oldanunk — nem azt, hogy melyik szolgáltatás nevét ismered.',descriptions:{'HIPStudio':'Innen indul minden.','Business':'Működés, kontroll és üzleti háttér.','Creative':'Fotó, film, podcast és vizuális tartalom.','Flúgos':'Kapcsolódás, esemény és vállalati élmény.','Megoldások':'Konkrét problémákra összerakott, több szakágat átfogó megoldások.','Összes megoldás':'Konkrét problémákra összerakott, több szakágat átfogó megoldások.','Hogyan dolgozunk':'Kik vagyunk, hogyan oszlik meg a felelősség, és mire számíthatsz.','Konzultáció':'Mondd el, mit kell elérni. Innen együtt rakjuk össze a szükséges formátumot.'}},
    en:{menu:'Menu',close:'Close',label:'Main navigation',note:'Start with the problem you need solved — not with the name of a service you already know.',descriptions:{'HIPStudio':'Start here.','Business':'Operations, control and business support.','Creative':'Photography, film, podcast and visual content.','Flúgos':'Connection, events and corporate experiences.','Solutions':'Cross-discipline answers built around a concrete business problem.','All solutions':'Cross-discipline answers built around a concrete business problem.','How we work':'Who is responsible for what, how we work, and what you can expect.','Consultation':'Tell us what needs to change. We will shape the right format and team from there.'}},
    de:{menu:'Menü',close:'Schließen',label:'Hauptnavigation',note:'Starte mit dem Problem, das gelöst werden muss — nicht mit dem Namen einer Leistung.',descriptions:{'HIPStudio':'Hier beginnt das System.','Business':'Betrieb, Kontrolle und geschäftliche Unterstützung.','Creative':'Fotografie, Film, Podcast und visueller Content.','Flúgos':'Verbindung, Events und Unternehmenserlebnisse.','Lösungen':'Mehrere Disziplinen, gebündelt für ein konkretes Geschäftsproblem.','Alle Lösungen':'Mehrere Disziplinen, gebündelt für ein konkretes Geschäftsproblem.','So arbeiten wir':'Wer wofür verantwortlich ist, wie wir arbeiten und was du erwarten kannst.','Beratung':'Sag uns, was erreicht werden soll. Daraus bauen wir Format und Team.'}}
  };
  const lang=(document.documentElement.lang||'en').slice(0,2);
  const t=copy[lang]||copy.en;
  const links=[...sourceNav.querySelectorAll('a')];

  const button=document.createElement('button');
  button.className='menu-toggle';
  button.type='button';
  button.setAttribute('aria-expanded','false');
  button.setAttribute('aria-controls','site-menu');
  button.setAttribute('aria-label',t.menu);
  button.innerHTML='<span></span><span></span>';

  const overlay=document.createElement('div');
  overlay.className='menu-overlay';
  overlay.id='site-menu';
  overlay.hidden=true;
  overlay.innerHTML=`<div class="menu-shell" role="dialog" aria-modal="true" aria-label="${t.label}"><div class="menu-top"><a class="menu-brand" href="${header.querySelector('.brand')?.getAttribute('href')||'/'}">HIPStudio</a><button class="menu-close" type="button" aria-label="${t.close}">×</button></div><div class="menu-layout"><nav class="menu-primary" aria-label="${t.label}"></nav><aside class="menu-aside"><p>${t.note}</p><div class="menu-langs"></div></aside></div></div>`;

  const target=overlay.querySelector('.menu-primary');
  links.forEach(a=>{
    const x=a.cloneNode(true);
    x.className='menu-link';
    const label=(a.textContent||'').trim();
    const desc=t.descriptions[label]||'';
    x.innerHTML=`<span class="menu-title">${label}</span>${desc?`<span class="menu-copy">${desc}</span>`:''}`;
    target.appendChild(x);
  });
  if(langs)overlay.querySelector('.menu-langs').append(...[...langs.querySelectorAll('a')].map(a=>a.cloneNode(true)));
  header.appendChild(button);
  document.body.appendChild(overlay);

  const close=overlay.querySelector('.menu-close');
  let lastFocus=null;
  const focusables=()=>[...overlay.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')];
  function openMenu(){lastFocus=document.activeElement;overlay.hidden=false;document.body.classList.add('menu-open');button.setAttribute('aria-expanded','true');requestAnimationFrame(()=>overlay.classList.add('is-open'));(focusables()[0]||close).focus();}
  function closeMenu(){overlay.classList.remove('is-open');document.body.classList.remove('menu-open');button.setAttribute('aria-expanded','false');overlay.hidden=true;lastFocus?.focus?.();}
  button.addEventListener('click',openMenu);
  close.addEventListener('click',closeMenu);
  overlay.addEventListener('click',e=>{if(e.target===overlay)closeMenu();});
  document.addEventListener('keydown',e=>{
    if(overlay.hidden)return;
    if(e.key==='Escape'){e.preventDefault();closeMenu();return;}
    if(e.key!=='Tab')return;
    const f=focusables();if(!f.length)return;
    const first=f[0],last=f[f.length-1];
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
  });
})();
