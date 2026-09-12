(() => {
  const toggle = document.querySelector('[data-menu-toggle]');
  const menu = document.getElementById('site-menu');
  const close = menu?.querySelector('[data-menu-close]');
  if (!toggle || !menu || !close) return;

  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  let previousFocus = null;

  function focusable() {
    return Array.from(menu.querySelectorAll(focusableSelector)).filter((el) => !el.hasAttribute('hidden'));
  }

  function openMenu() {
    previousFocus = document.activeElement;
    menu.hidden = false;
    document.body.classList.add('menu-open');
    toggle.setAttribute('aria-expanded', 'true');
    const items = focusable();
    (items[0] || close).focus();
  }

  function closeMenu() {
    menu.hidden = true;
    document.body.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    if (previousFocus && typeof previousFocus.focus === 'function') previousFocus.focus();
  }

  toggle.addEventListener('click', openMenu);
  close.addEventListener('click', closeMenu);
  menu.addEventListener('click', (event) => {
    if (event.target === menu) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (menu.hidden) return;
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
})();
