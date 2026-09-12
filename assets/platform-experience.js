(() => {
  const body = document.body;
  const overlay = document.getElementById('site-menu');
  const toggle = document.querySelector('.menu-toggle');
  const closeButton = document.querySelector('.menu-close');
  let lastFocused = null;

  const focusable = () => overlay ? Array.from(overlay.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')).filter(el => !el.hasAttribute('hidden')) : [];

  function openMenu() {
    if (!overlay || !toggle) return;
    lastFocused = document.activeElement;
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
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  }

  if (toggle && overlay && closeButton) {
    toggle.addEventListener('click', openMenu);
    closeButton.addEventListener('click', closeMenu);
    overlay.addEventListener('click', event => {
      if (event.target === overlay) closeMenu();
    });
    overlay.querySelectorAll('a[href]').forEach(link => link.addEventListener('click', closeMenu));
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

  const hero = document.querySelector('.hero-film[data-hero-video-id]');
  const play = hero && hero.querySelector('[data-hero-play]');
  const frame = hero && hero.querySelector('[data-hero-frame]');
  let playerLoaded = false;

  function loadHeroFilm() {
    if (!hero || !play || !frame || playerLoaded) return;
    const videoId = hero.dataset.heroVideoId;
    if (!/^[A-Za-z0-9_-]{11}$/.test(videoId)) return;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const iframe = document.createElement('iframe');
    const params = new URLSearchParams({
      autoplay: reduceMotion ? '0' : '1',
      mute: '1',
      loop: '1',
      playlist: videoId,
      controls: reduceMotion ? '1' : '0',
      playsinline: '1',
      rel: '0',
      modestbranding: '1'
    });
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?${params.toString()}`;
    iframe.title = 'HIPStudio reference film';
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    iframe.allowFullscreen = true;
    frame.replaceChildren(iframe);
    hero.classList.add('is-playing');
    play.setAttribute('aria-pressed', 'true');
    playerLoaded = true;
  }

  if (play) {
    play.setAttribute('aria-pressed', 'false');
    play.addEventListener('click', loadHeroFilm, { once: true });
  }
})();
