import {chromium} from 'playwright';

const origin='http://127.0.0.1:4174';
const browser=await chromium.launch({...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),headless:true});
const failures=[];
const results=[];

for(const width of [390,1440]){
  const context=await browser.newContext({viewport:{width,height:900}});
  const page=await context.newPage();
  await page.goto(origin+'/hu/',{waitUntil:'networkidle'});
  const trigger=page.locator('[data-menu-toggle]');
  const overlay=page.locator('[data-menu-overlay]');
  const classicNav=page.locator('header .nav');
  const initial={
    trigger:await trigger.count()===1,
    classicNav:await classicNav.count(),
    hidden:await overlay.getAttribute('hidden')!==null,
    expanded:await trigger.getAttribute('aria-expanded')
  };
  if(!initial.trigger||initial.classicNav!==0||!initial.hidden||initial.expanded!=='false') failures.push({width,stage:'initial',initial});

  await trigger.click();
  const opened={
    visible:await overlay.isVisible(),
    expanded:await trigger.getAttribute('aria-expanded'),
    bodyLocked:await page.locator('body').evaluate(el=>el.classList.contains('menu-open')),
    activeInMenu:await overlay.evaluate(el=>el.contains(document.activeElement)),
    descriptions:await overlay.locator('.menu-item-copy').count()
  };
  if(!opened.visible||opened.expanded!=='true'||!opened.bodyLocked||!opened.activeInMenu||opened.descriptions<5) failures.push({width,stage:'open',opened});

  const first=overlay.locator('a[href],button:not([disabled])').first();
  const last=overlay.locator('a[href],button:not([disabled])').last();
  await first.focus();
  await page.keyboard.press('Shift+Tab');
  const shiftTrap=await last.evaluate(el=>document.activeElement===el);
  if(!shiftTrap) failures.push({width,stage:'shift-tab-trap'});

  await page.keyboard.press('Escape');
  const closed={
    hidden:await overlay.getAttribute('hidden')!==null,
    expanded:await trigger.getAttribute('aria-expanded'),
    bodyUnlocked:await page.locator('body').evaluate(el=>!el.classList.contains('menu-open')),
    focusRestored:await trigger.evaluate(el=>document.activeElement===el)
  };
  if(!closed.hidden||closed.expanded!=='false'||!closed.bodyUnlocked||!closed.focusRestored) failures.push({width,stage:'escape-close',closed});

  await trigger.click();
  const closeButton=page.locator('[data-menu-close]');
  await closeButton.click();
  const closeButtonWorks=await overlay.getAttribute('hidden')!==null;
  if(!closeButtonWorks) failures.push({width,stage:'button-close'});

  results.push({width,initial,opened,shiftTrap,closed,closeButtonWorks});
  await context.close();
}

console.log(JSON.stringify({results,failures},null,2));
await browser.close();
if(failures.length)process.exitCode=1;
