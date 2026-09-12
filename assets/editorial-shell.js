(() => {
  const body = document.body;
  const overlay = document.querySelector('[data-menu-overlay]');
  const toggle = document.querySelector('[data-menu-toggle]');
  const close = document.querySelector('[data-menu-close]');
  let previousFocus = null;

  const focusable = () => overlay ? [...overlay.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')] : [];

  function openMenu() {
    if (!overlay || !toggle) return;
    previousFocus = document.activeElement;
    overlay.hidden = false;
    body.classList.add('menu-open');
    toggle.setAttribute('aria-expanded', 'true');
    const items = focusable();
    (items[0] || close)?.focus();
  }

  function closeMenu() {
    if (!overlay || !toggle) return;
    overlay.hidden = true;
    body.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    if (previousFocus && typeof previousFocus.focus === 'function') previousFocus.focus();
  }

  toggle?.addEventListener('click', openMenu);
  close?.addEventListener('click', closeMenu);

  document.addEventListener('keydown', (event) => {
    if (!overlay || overlay.hidden) return;
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

  overlay?.addEventListener('click', (event) => {
    if (event.target === overlay) closeMenu();
  });

  const hero = document.querySelector('[data-hero-film]');
  const play = document.querySelector('[data-hero-play]');
  const stage = document.querySelector('[data-hero-video-stage]');
  const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

  play?.addEventListener('click', () => {
    if (!hero || !stage || reduceMotion || stage.querySelector('iframe')) return;
    const source = stage.dataset.embed;
    if (!source || !source.startsWith('https://www.youtube-nocookie.com/embed/')) return;
    const frame = document.createElement('iframe');
    frame.src = source;
    frame.title = play.dataset.frameTitle || 'HIPStudio showreel';
    frame.allow = 'autoplay; encrypted-media; picture-in-picture';
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.setAttribute('allowfullscreen', '');
    frame.setAttribute('tabindex', '-1');
    stage.appendChild(frame);
    hero.classList.add('is-playing');
    play.hidden = true;
  });
})();
