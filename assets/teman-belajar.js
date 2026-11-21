/* Maskot dan ruang baca: tidak mengubah nilai, kunci, maupun jawaban siswa. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else if (!root.FIWA_STUDY) root.FIWA_STUDY = api.mount(root);
})(typeof window === 'undefined' ? globalThis : window, function () {
  'use strict';
  const DURATION = 15000;
  function gained(previous, entries) {
    if (!previous) return [];
    const before = new Set(previous);
    return entries.filter(x => !before.has(x.key));
  }
  function tracker() {
    const accounts = new Map();
    return { observe(account, entries) {
      if (!account) return [];
      const result = gained(accounts.get(account), entries);
      accounts.set(account, entries.map(x => x.key));
      return result;
    } };
  }
  function mount(win) {
    const doc = win.document, track = tracker();
    const script = doc.currentScript;
    const logo = new URL('logo.png', script ? script.src : new URL('assets/', win.location.href)).href;
    let hidden = false, owl = null, end = 0, account = null, route = '', timer = null;
    try { hidden = win.localStorage.getItem('fiwa.panel-tahapan') === 'sembunyi'; } catch (_) {}
    const reduced = win.matchMedia('(prefers-reduced-motion: reduce)');
    function dismiss() {
      if (timer != null) win.clearTimeout(timer);
      timer = null; end = 0;
      if (owl) owl.remove();
      owl = null;
    }
    function applyPanel() {
      const layout = doc.querySelector('.study-layout'), rail = doc.querySelector('.study-rail');
      const button = doc.querySelector('[data-study-panel]');
      if (!layout || !rail || !button) return;
      layout.classList.toggle('is-rail-hidden', hidden);
      rail.hidden = hidden;
      button.setAttribute('aria-expanded', String(!hidden));
      const en = doc.documentElement.lang === 'en';
      button.querySelector('span').textContent = hidden ? (en ? 'Show stages' : 'Tampilkan tahapan') : (en ? 'Hide stages' : 'Sembunyikan tahapan');
      button.title = button.querySelector('span').textContent;
      position();
    }
    function position() {
      if (!owl) return;
      const rail = doc.querySelector('.study-rail'), toggle = doc.querySelector('[data-study-panel]');
      const anchor = !hidden && rail ? rail : toggle;
      if (!anchor) { dismiss(); return; }
      const rect = anchor.getBoundingClientRect();
      const header = doc.querySelector('.bar');
      const top = Math.max((header ? header.getBoundingClientRect().bottom : 0) + 8, rect.top + (hidden ? rect.height + 6 : 55));
      const left = Math.max(8, Math.min(rect.left + 4, win.innerWidth - 130));
      const width = Math.max(120, Math.min(hidden ? 248 : rect.width - 8, win.innerWidth - left - 8));
      owl.style.left = left + 'px';
      owl.style.top = Math.min(top, win.innerHeight - 154) + 'px';
      owl.style.width = width + 'px';
      owl.style.setProperty('--owl-travel', Math.max(0, width - 112) + 'px');
    }
    function celebrate(entries) {
      if (!doc.querySelector('[data-study-panel]') || doc.hidden) return;
      const en = doc.documentElement.lang === 'en';
      const label = [...new Set(entries.map(x => x.label))].slice(0, 3).join(', ');
      if (!owl) {
        owl = doc.createElement('div');
        owl.className = 'study-owl' + (reduced.matches ? ' reduced-motion' : '');
        owl.innerHTML = `<div class="owl-flight"><button type="button" class="owl-dismiss"><svg viewBox="0 0 112 140" aria-hidden="true" focusable="false">
          <g class="owl-body">
            <path class="owl-wing owl-wing-left" d="M31 40Q6 34 5 66Q21 67 34 56Z" fill="#307a96" stroke="#153851" stroke-width="2"/>
            <path class="owl-wing owl-wing-right" d="M81 40Q106 34 107 66Q91 67 78 56Z" fill="#307a96" stroke="#153851" stroke-width="2"/>
            <path d="M25 30 23 12 40 21Q56 13 72 21L89 12 87 34Q99 74 78 87Q56 98 34 87Q13 74 25 30Z" fill="#25627c" stroke="#153851" stroke-width="2"/>
            <path d="M34 68Q56 59 78 68L77 82Q56 96 35 82Z" fill="#f2d69b"/>
            <path d="M33 31Q18 49 34 62Q48 69 56 55Q64 69 78 62Q94 49 79 31Q67 23 56 36Q45 23 33 31Z" fill="#fff5df"/>
            <g class="owl-eyes"><circle cx="40" cy="46" r="8" fill="#153851"/><circle cx="72" cy="46" r="8" fill="#153851"/><circle cx="42" cy="43" r="3" fill="#fff"/><circle cx="74" cy="43" r="3" fill="#fff"/></g>
            <path d="M50 55 56 64 62 55Z" fill="#f4b445"/>
            <path d="M44 75l3 3m7-2 3 3m7-4 3 3" stroke="#b88240" stroke-width="2" stroke-linecap="round"/>
            <path d="M29 92H99" stroke="#153851" stroke-width="3" stroke-linecap="round"/>
            <path d="M42 85v8m5-8v8m18-8v8m5-8v8" stroke="#efad3f" stroke-width="3" stroke-linecap="round"/>
            <g class="owl-flag"><path d="M31 94H98V132Q66 125 31 132Z" fill="white" stroke="#7ab9d4" stroke-width="1.5"/>
              <image href="${logo}" x="35" y="96" width="59" height="32" preserveAspectRatio="xMidYMid meet"/>
            </g>
          </g></svg><span class="owl-close" aria-hidden="true">×</span></button></div><p class="owl-caption" role="status" aria-live="polite"></p>`;
        doc.body.appendChild(owl);
        owl.querySelector('button').addEventListener('click', dismiss);
        end = Date.now() + DURATION;
        timer = win.setTimeout(dismiss, DURATION);
      }
      owl.querySelector('button').setAttribute('aria-label', (en ? 'New stage unlocked: ' : 'Tahap baru terbuka: ') + label + (en ? '. Dismiss celebration' : '. Tutup perayaan'));
      owl.querySelector('.owl-caption').textContent = en ? label + ' unlocked!' : label + ' terbuka!';
      position();
    }
    function sync(state) {
      applyPanel();
      if (account !== state.account || route !== win.location.hash) dismiss();
      account = state.account; route = win.location.hash;
      if (!account) { dismiss(); return; }
      const next = track.observe(account, state.entries);
      if (next.length) celebrate(next);
      else if (owl && Date.now() >= end) dismiss();
    }
    doc.addEventListener('click', event => {
      const button = event.target.closest('[data-study-panel]');
      if (!button) return;
      hidden = !hidden;
      try { win.localStorage.setItem('fiwa.panel-tahapan', hidden ? 'sembunyi' : 'tampil'); } catch (_) {}
      applyPanel();
    });
    doc.addEventListener('visibilitychange', () => { if (doc.hidden) dismiss(); });
    win.addEventListener('hashchange', dismiss);
    win.addEventListener('pagehide', dismiss);
    win.addEventListener('resize', position, {passive:true});
    win.addEventListener('scroll', position, {passive:true});
    reduced.addEventListener('change', () => { if (owl) owl.classList.toggle('reduced-motion', reduced.matches); });
    return {sync, applyPanel, dismiss};
  }
  return {DURATION, gained, tracker, mount};
});
