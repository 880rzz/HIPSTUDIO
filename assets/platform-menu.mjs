const trigger=document.querySelector('[data-menu-toggle]');
const overlay=document.querySelector('[data-menu-overlay]');
const closeButton=document.querySelector('[data-menu-close]');
if(trigger&&overlay&&closeButton){
  let lastFocused=null;
  const focusableSelector='a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])';
  const focusables=()=>[...overlay.querySelectorAll(focusableSelector)].filter(el=>!el.hasAttribute('hidden'));
  const close=()=>{
    overlay.hidden=true;
    document.body.classList.remove('menu-open');
    trigger.setAttribute('aria-expanded','false');
    if(lastFocused instanceof HTMLElement)lastFocused.focus();
  };
  const open=()=>{
    lastFocused=document.activeElement;
    overlay.hidden=false;
    document.body.classList.add('menu-open');
    trigger.setAttribute('aria-expanded','true');
    const items=focusables();
    (items[0]||closeButton).focus();
  };
  trigger.addEventListener('click',()=>overlay.hidden?open():close());
  closeButton.addEventListener('click',close);
  overlay.addEventListener('click',event=>{if(event.target===overlay)close();});
  overlay.querySelectorAll('a[href]').forEach(link=>link.addEventListener('click',close));
  document.addEventListener('keydown',event=>{
    if(overlay.hidden)return;
    if(event.key==='Escape'){
      event.preventDefault();
      close();
      return;
    }
    if(event.key!=='Tab')return;
    const items=focusables();
    if(!items.length)return;
    const first=items[0],last=items[items.length-1];
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
  });
}
