(() => {
  const body = document.body;
  const overlay = document.getElementById('site-menu');
  const toggle = document.querySelector('.menu-toggle');
  const close = document.querySelector('.menu-close');
  let previousFocus = null;

  const focusable = () => overlay ? Array.from(overlay.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')) : [];

  function openMenu() {
    if (!overlay || !toggle) return;
    previousFocus = document.activeElement;
    overlay.hidden = false;
    body.classList.add('menu-open');
    toggle.setAttribute('aria-expanded', 'true');
    const items = focusable();
    if (items.length) items[0].focus();
  }

  function closeMenu() {
    if (!overlay || !toggle) return;
    overlay.hidden = true;
    body.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    if (previousFocus && previousFocus.focus) previousFocus.focus();
  }

  if (toggle && close && overlay) {
    toggle.addEventListener('click', openMenu);
    close.addEventListener('click', closeMenu);
    overlay.addEventListener('click', event => {
      if (event.target === overlay) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (overlay.hidden) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        closeMenu();
        return;
      }
      if (event.key !== 'Tab') return;
      const items = focusable();
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  document.querySelectorAll('[data-hero-video]').forEach(hero => {
    const button = hero.querySelector('.hero-film-activate');
    const frame = hero.querySelector('.hero-film-frame');
    if (!button || !frame) return;
    button.addEventListener('click', () => {
      const src = frame.getAttribute('data-src');
      if (!src || frame.getAttribute('src')) return;
      frame.setAttribute('src', src);
      hero.classList.add('hero--playing');
      button.setAttribute('aria-pressed', 'true');
      button.blur();
    }, { once: true });
  });
})();
