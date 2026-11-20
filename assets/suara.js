/* Efek antarmuka opt-in. Tidak mengubah volume video, audio narasi, atau progres. */
(function () {
  'use strict';
  const KEY = 'fiwa-sound-v1';
  let prefs = { on: false, volume: 0.35 }, context, last = 0;
  try { const p = JSON.parse(localStorage.getItem(KEY)); if (p) prefs = { on: p.on === true, volume: Number.isFinite(p.volume) ? Math.max(0, Math.min(1, p.volume)) : .35 }; } catch (_) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(prefs)); } catch (_) {} }
  async function pop(force) {
    if (!prefs.on || (!force && performance.now() - last < 65)) return false;
    try {
      const Audio = window.AudioContext || window.webkitAudioContext;
      if (!Audio) { status('Peramban ini belum mendukung efek suara.'); return false; }
      if (!context) context = new Audio();
      if (context.state === 'suspended') await context.resume();
      const t = context.currentTime, osc = context.createOscillator(), gain = context.createGain();
      osc.type = 'sine'; osc.frequency.setValueAtTime(620, t); osc.frequency.exponentialRampToValueAtTime(250, t + .075);
      gain.gain.setValueAtTime(.0001, t); gain.gain.exponentialRampToValueAtTime(Math.max(.0001, prefs.volume * .18), t + .008);
      gain.gain.exponentialRampToValueAtTime(.0001, t + .09);
      osc.connect(gain); gain.connect(context.destination); osc.start(t); osc.stop(t + .1);
      osc.onended = () => { osc.disconnect(); gain.disconnect(); };
      last = performance.now(); return true;
    } catch (_) { status('Efek suara belum dapat diputar. Coba tekan Uji bunyi lagi.'); return false; }
  }
  function status(text) { const el = document.getElementById('sound-status'); if (el) el.textContent = text; }
  function update() {
    const en = document.documentElement.lang === 'en', btn = document.getElementById('sound-toggle');
    if (btn) { btn.setAttribute('aria-label', en ? 'Sound settings' : 'Pengaturan bunyi'); btn.querySelector('span').textContent = en ? 'Sound' : 'Bunyi'; btn.dataset.on = String(prefs.on); }
  }
  function bind(doc) {
    if (doc.__fiwaSound) return; doc.__fiwaSound = true;
    doc.addEventListener('click', event => {
      if (!event.isTrusted) return;
      const el = event.target.closest('button,a[href],summary,input[type=checkbox],input[type=radio]');
      if (el && !el.disabled && !el.closest('#sound-panel') && el.getAttribute('aria-disabled') !== 'true') pop(false);
    }, true);
    doc.addEventListener('load', event => {
      if (event.target.tagName !== 'IFRAME') return;
      try { if (event.target.contentDocument) bind(event.target.contentDocument); } catch (_) {}
    }, true);
    doc.querySelectorAll('iframe').forEach(frame => { try { if (frame.contentDocument) bind(frame.contentDocument); } catch (_) {} });
  }
  document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('sound-toggle'), panel = document.getElementById('sound-panel');
    if (!button || !panel) return;
    const on = panel.querySelector('#sound-on'), volume = panel.querySelector('#sound-volume'), output = panel.querySelector('output');
    on.checked = prefs.on; volume.value = String(Math.round(prefs.volume * 100)); output.value = volume.value + '%';
    function close(returnFocus) { panel.hidden = true; button.setAttribute('aria-expanded', 'false'); if (returnFocus) button.focus(); }
    button.addEventListener('click', () => { const open = panel.hidden; panel.hidden = !open; button.setAttribute('aria-expanded', String(open)); if (open) on.focus(); });
    on.addEventListener('change', () => { prefs.on = on.checked; save(); update(); status(prefs.on ? 'Efek bunyi aktif.' : 'Efek bunyi nonaktif.'); if (prefs.on) pop(true); });
    volume.addEventListener('input', () => { prefs.volume = Number(volume.value) / 100; output.value = volume.value + '%'; save(); });
    panel.querySelector('#sound-test').addEventListener('click', async () => {
      if (!prefs.on) return status('Aktifkan efek bunyi untuk mencoba.');
      if (await pop(true)) status(prefs.volume === 0 ? 'Volume 0%. Naikkan volume untuk mendengar bunyi.' : 'Bunyi uji diputar.');
    });
    document.addEventListener('click', e => { if (!e.target.closest('.sound-menu')) close(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) close(true); });
    window.addEventListener('hashchange', () => close(false));
    document.addEventListener('fims:bahasa', update); bind(document); update();
  });
  window.FIWA_SOUND = { get: () => ({ ...prefs }), bind };
})();
