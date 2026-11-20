/* Preferensi tampilan hanya disimpan di peramban, terpisah dari progres belajar. */
(function () {
  'use strict';
  const KEY = 'fiwa-theme-v1';
  let theme = 'light';
  try { if (localStorage.getItem(KEY) === 'dim') theme = 'dim'; } catch (_) {}
  const root = document.documentElement;
  const contentCSS = new URL('tema-konten.css', document.currentScript.src);
  const desktop = window.matchMedia('(min-width: 900px)');

  function applyFrame(frame) {
    try {
      const url = new URL(frame.getAttribute('src') || '', frame.ownerDocument.baseURI);
      // Hanya halaman HTML milik situs. PDF dan media luar mempertahankan penampil aslinya.
      if (url.origin !== location.origin || !/\.html?$/i.test(url.pathname)) return;
      const doc = frame.contentDocument;
      if (!doc || !doc.head || !doc.body) return;
      // Lembar lama memuat warna tetap pada panel, tabel dan input. Gunakan
      // satu palet kertas redup yang utuh, bukan teks terang di atas panel putih.
      if (/^\/(?:konten|aset-[a-z0-9.-]+)\//i.test(url.pathname)) {
        doc.documentElement.dataset.fiwaReading = 'paper';
      } else {
        delete doc.documentElement.dataset.fiwaReading;
      }
      doc.documentElement.dataset.fiwaTheme = theme;
      if (window.FIWA_ALUR) window.FIWA_ALUR.decorate(doc);
      if (window.FIWA_SOUND) window.FIWA_SOUND.bind(doc);
      if (!doc.getElementById('fiwa-content-theme')) {
        const link = doc.createElement('link');
        link.id = 'fiwa-content-theme'; link.rel = 'stylesheet'; link.href = contentCSS.href;
        doc.head.appendChild(link);
        doc.addEventListener('load', event => {
          if (event.target.tagName === 'IFRAME') applyFrame(event.target);
        }, true);
      }
      doc.querySelectorAll('iframe').forEach(applyFrame);
    } catch (_) { /* Dokumen lintas asal tidak diakses. */ }
  }

  function labels(language) {
    const en = language === 'en';
    document.querySelectorAll('[data-theme-choice]').forEach(button => {
      const label = button.dataset.themeChoice === 'dim'
        ? (en ? 'Dim theme' : 'Tema teduh') : (en ? 'Light theme' : 'Tema terang');
      button.setAttribute('aria-label', label);
      button.setAttribute('title', label);
    });
    const group = document.querySelector('.theme-switch');
    if (group) group.setAttribute('aria-label', en ? 'Display theme' : 'Tema tampilan');
  }

  function apply(value, persist) {
    theme = value === 'dim' ? 'dim' : 'light';
    root.dataset.theme = theme;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = theme === 'dim' ? '#192a40' : '#e3f1fe';
    document.querySelectorAll('[data-theme-choice]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.themeChoice === theme));
    });
    document.querySelectorAll('iframe').forEach(applyFrame);
    if (persist) { try { localStorage.setItem(KEY, theme); } catch (_) {} }
  }

  apply(theme, false); // Sebelum CSS: hindari kilatan tema yang salah saat memuat ulang.
  window.FIWA_THEME = { applyFrame, get: () => theme };
  document.addEventListener('DOMContentLoaded', () => {
    apply(theme, false); labels(root.lang);
    const bar = document.querySelector('.bar');
    if (bar && window.ResizeObserver) new ResizeObserver(() => {
      root.style.setProperty('--header-height', Math.ceil(bar.getBoundingClientRect().height) + 'px');
    }).observe(bar);
  });
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-theme-choice]');
    if (button) apply(button.dataset.themeChoice, true);
  });
  document.addEventListener('fims:bahasa', event => labels(event.detail));
  document.addEventListener('load', event => {
    if (event.target.tagName === 'IFRAME') applyFrame(event.target);
  }, true);
  window.addEventListener('storage', event => {
    if (event.key === KEY) apply(event.newValue, false);
  });
  desktop.addEventListener('change', event => {
    document.querySelectorAll('.study-rail').forEach(rail => {
      rail.querySelector('.study-rail-scroll').hidden = !event.matches;
      rail.querySelector('[data-study-toggle]').setAttribute('aria-expanded', String(event.matches));
    });
  });
})();
