# coding: utf-8
"""Static regression checks for the unified full-screen platform navigation."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist-platform'

REQUIRED=(
 'data-menu-toggle','data-menu-overlay','data-menu-close','aria-controls="site-menu"',
 'platform-menu.css','platform-menu.mjs','class="menu-primary"','class="menu-item-copy"'
)
FORBIDDEN=(
 '<nav class="nav"','<details class="mobile-menu"','purple','glassmorphism'
)


def fail(msg): raise SystemExit(msg)


def main():
 css=DIST/'assets/platform-menu.css'; js=DIST/'assets/platform-menu.mjs'
 if not css.exists() or not js.exists(): fail('Fullscreen menu assets missing from dist-platform')
 pages=[]
 for page in sorted(DIST.rglob('*.html')):
  text=page.read_text(encoding='utf-8')
  if '<header class="header">' not in text: continue
  pages.append(page)
  missing=[token for token in REQUIRED if token not in text]
  if missing: fail(f'Menu contract missing in {page}: {missing}')
  if '<nav class="nav"' in text: fail(f'Classic desktop nav remains in {page}')
  if text.count('id="site-menu"')!=1: fail(f'Menu id must be unique in {page}')
  if text.count('data-menu-toggle')!=1 or text.count('data-menu-close')!=1: fail(f'Menu controls duplicated in {page}')
  language=re.search(r'<html lang="(hu|en|de)"',text)
  if not language: fail(f'Missing supported language in {page}')
  for fragment in {'hu':['Üzleti működés','Kreatív tartalom','Vállalati élmények','Hogyan dolgozunk','Konzultáció'],
                   'en':['Business operations','Creative content','Corporate experiences','How we work','Consultation'],
                   'de':['Business Operations','Creative Content','Unternehmenserlebnisse','So arbeiten wir','Beratung']}[language.group(1)]:
   if fragment not in text: fail(f'Missing localized menu copy {fragment!r} in {page}')
 if len(pages)<3: fail(f'Too few platform pages checked: {len(pages)}')
 js_text=js.read_text(encoding='utf-8')
 for token in ['Escape','aria-expanded','menu-open','event.key===\'Tab\'']:
  if token not in js_text: fail(f'Menu interaction contract missing: {token}')
 css_text=css.read_text(encoding='utf-8')
 if '@media(prefers-reduced-motion:reduce)' not in css_text: fail('Reduced-motion menu rule missing')
 print(f'Fullscreen menu contract valid across {len(pages)} platform pages')

if __name__=='__main__': main()
