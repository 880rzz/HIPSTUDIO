(()=>{
  const style=document.createElement('style');
  style.textContent=`
    .header>.nav{display:none!important}
    .header{align-items:center!important;flex-wrap:nowrap!important;border-radius:24px!important}
    .header>.langs{margin-left:auto}
    .menu-toggle{width:48px;height:48px;border:1px solid rgba(11,23,54,.14);border-radius:50%;background:#fff;color:#0b1736;display:inline-flex;flex-direction:column;justify-content:center;gap:6px;padding:0 14px;cursor:pointer;box-shadow:0 8px 24px rgba(11,23,54,.08)}
    .menu-toggle span{display:block;height:1.5px;background:currentColor;border-radius:1px}
    .menu-overlay[hidden]{display:none!important}
    .menu-overlay{position:fixed;inset:0;z-index:100;background:rgba(7,15,34,.985);color:#fff;opacity:0;transition:opacity .18s ease;overflow:auto}
    .menu-overlay.is-open{opacity:1}
    .menu-shell{width:min(1240px,calc(100% - 40px));min-height:100dvh;margin:auto;padding:26px 0 38px;display:flex;flex-direction:column}
    .menu-top{display:flex;align-items:center;justify-content:space-between;padding-bottom:clamp(2rem,5vw,4rem);border-bottom:1px solid rgba(255,255,255,.12)}
    .menu-brand{font-weight:760;font-size:1.08rem;letter-spacing:-.03em;text-decoration:none;color:#fff}
    .menu-close{width:48px;height:48px;border:1px solid rgba(255,255,255,.22);border-radius:50%;background:transparent;color:#fff;font-size:2rem;line-height:1;cursor:pointer}
    .menu-layout{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(260px,.65fr);gap:clamp(2.5rem,8vw,8rem);padding-top:clamp(2.2rem,5vw,4.5rem);flex:1}
    .menu-primary{display:grid;align-content:start}
    .menu-link{display:block;padding:1.15rem 0 1.35rem;border-bottom:1px solid rgba(255,255,255,.12);text-decoration:none;color:#fff}
    .menu-title{display:block;font-size:clamp(1.8rem,4vw,4rem);line-height:1;letter-spacing:-.045em;font-weight:620}
    .menu-copy{display:block;margin-top:.55rem;max-width:58ch;color:rgba(255,255,255,.62);font-size:.96rem;line-height:1.55}
    .menu-link:hover .menu-title,.menu-link:focus-visible .menu-title{color:#d4bb7c}
    .menu-aside{align-self:end;padding-bottom:1rem;color:rgba(255,255,255,.68);max-width:38ch}
    .menu-aside p{font-size:1rem;line-height:1.7}
    .menu-langs{display:flex;gap:1rem;margin-top:1.5rem}
    .menu-langs a{color:#fff;text-decoration:none;opacity:.62}
    .menu-langs a[aria-current=page]{opacity:1;text-decoration:underline;text-decoration-color:#b59655}
    .menu-open{overflow:hidden}
    .menu-toggle:focus-visible,.menu-close:focus-visible,.menu-link:focus-visible{outline:3px solid rgba(212,187,124,.55);outline-offset:4px}
    @media(max-width:820px){.header>.langs{display:none}.menu-layout{grid-template-columns:1fr}.menu-aside{align-self:start}.menu-copy{font-size:.9rem}.menu-shell{width:min(100% - 24px,1240px)}}
    @media(prefers-reduced-motion:reduce){.menu-overlay{transition:none}}
  `;
  document.head.appendChild(style);

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
  if(!links.length)return;

  const button=document.createElement('button');
  button.className='menu-toggle';button.type='button';button.setAttribute('aria-expanded','false');button.setAttribute('aria-controls','site-menu');button.setAttribute('aria-label',t.menu);button.innerHTML='<span></span><span></span>';

  const overlay=document.createElement('div');
  overlay.className='menu-overlay';overlay.id='site-menu';overlay.hidden=true;
  overlay.innerHTML=`<div class="menu-shell" role="dialog" aria-modal="true" aria-label="${t.label}"><div class="menu-top"><a class="menu-brand" href="${header.querySelector('.brand')?.getAttribute('href')||'/'}">HIPStudio</a><button class="menu-close" type="button" aria-label="${t.close}">×</button></div><div class="menu-layout"><nav class="menu-primary" aria-label="${t.label}"></nav><aside class="menu-aside"><p>${t.note}</p><div class="menu-langs"></div></aside></div></div>`;
  const target=overlay.querySelector('.menu-primary');
  links.forEach(a=>{const x=a.cloneNode(true);x.className='menu-link';const label=(a.textContent||'').trim();const desc=t.descriptions[label]||'';x.innerHTML=`<span class="menu-title">${label}</span>${desc?`<span class="menu-copy">${desc}</span>`:''}`;target.appendChild(x);});
  if(langs)overlay.querySelector('.menu-langs').append(...[...langs.querySelectorAll('a')].map(a=>a.cloneNode(true)));
  header.appendChild(button);document.body.appendChild(overlay);

  const close=overlay.querySelector('.menu-close');let lastFocus=null;
  const focusables=()=>[...overlay.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')];
  function openMenu(){lastFocus=document.activeElement;overlay.hidden=false;document.body.classList.add('menu-open');button.setAttribute('aria-expanded','true');requestAnimationFrame(()=>overlay.classList.add('is-open'));(focusables()[0]||close).focus();}
  function closeMenu(){overlay.classList.remove('is-open');document.body.classList.remove('menu-open');button.setAttribute('aria-expanded','false');overlay.hidden=true;lastFocus?.focus?.();}
  button.addEventListener('click',openMenu);close.addEventListener('click',closeMenu);overlay.addEventListener('click',e=>{if(e.target===overlay)closeMenu();});
  document.addEventListener('keydown',e=>{if(overlay.hidden)return;if(e.key==='Escape'){e.preventDefault();closeMenu();return;}if(e.key!=='Tab')return;const f=focusables();if(!f.length)return;const first=f[0],last=f[f.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}});
})();
