/* Akun Fisika FIWA — masuk dengan surel, persetujuan pemilik situs, peran siswa dan guru.
   Berkas ini berjalan lebih dulu daripada app.js. Mesin alur belajar baru dimuat
   setelah anggota benar-benar masuk, jadi tidak ada yang bocor ke tamu.

   Yang disediakan untuk app.js:
     window.FIMS.aku          — { email, nama, peran, guru, owner } atau null
     window.FIMS.modeGuru()   — true bila guru sedang memakai mode guru
     window.FIMS.dorong(db)   — menyimpan progres ke peladen (ditunda, tidak tiap ketikan)
     window.FIMS.halAnggota() — menggambar panel anggota pada #app
     window.FIMS.papan()      — janji berisi progres seluruh murid, untuk Papan Guru     */
(function () {
'use strict';

const KUNCI_PROG = 'va-fims-v1';
const KUNCI_MODE = 'fims-mode-guru';
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const API = async (jalur, opsi) => {
  const r = await fetch('/api/' + jalur, { credentials: 'same-origin', headers: { 'content-type': 'application/json' }, ...opsi });
  let d = {}; try { d = await r.json(); } catch {}
  return { ok: r.ok, status: r.status, ...d };
};

const FIMS = window.FIMS = {
  aku: null,
  modeGuru: () => {
    if (!FIMS.aku || !FIMS.aku.guru) return false;
    try { return localStorage.getItem(KUNCI_MODE) !== 'siswa'; } catch { return true; }
  },
  setMode(m) { try { localStorage.setItem(KUNCI_MODE, m); } catch {} }
};

/* ---------- gambar layar ---------- */
const bungkus = isi => `<div class="masuk-bingkai"><section class="masuk-kotak">${isi}</section></div>`;

function layarMasuk(pesan) {
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">Fitrah Islamic World Academy</p>
    <h1>Masuk ke Fisika FIWA</h1>
    <p class="lede">Cukup dengan alamat surelmu — tidak perlu kata sandi dan tidak perlu mendaftar.
      Bila ini pertama kalinya, pemilik situs akan menyetujui akunmu sekali saja.</p>
    ${pesan ? `<div class="note">${esc(pesan)}</div>` : ''}
    <form id="f-masuk" class="masuk-form" autocomplete="on">
      <label for="m-email">Alamat surel</label>
      <input id="m-email" name="email" type="email" inputmode="email" autocomplete="email"
             placeholder="nama@contoh.sch.id" required>
      <label for="m-nama">Nama <span class="muted">(opsional, membantu gurumu mengenali)</span></label>
      <input id="m-nama" name="nama" type="text" autocomplete="name" placeholder="Nama lengkap" maxlength="80">
      <p class="muted masuk-tanya">Masuk sebagai apa?</p>
      <div class="masuk-pilih">
        <button class="btn" type="submit" value="siswa" name="peran">Masuk sebagai Siswa</button>
        <button class="btn ghost" type="submit" value="guru" name="peran">Masuk sebagai Guru</button>
      </div>
      <p class="muted masuk-kaki">Alamat surel hanya dipakai sebagai tanda pengenal di situs ini.
        Tidak dikirimi apa pun, dan tidak dibagikan ke mana pun.</p>
    </form>`);

  let peran = 'siswa';
  $('#f-masuk').querySelectorAll('button[type=submit]').forEach(b =>
    b.addEventListener('click', () => { peran = b.value; }));

  $('#f-masuk').addEventListener('submit', async ev => {
    ev.preventDefault();
    const email = $('#m-email').value.trim(), nama = $('#m-nama').value.trim();
    const tombol = $('#f-masuk').querySelectorAll('button');
    tombol.forEach(b => b.disabled = true);
    const r = await API('masuk', { method: 'POST', body: JSON.stringify({ email, nama, peran }) });
    tombol.forEach(b => b.disabled = false);
    if (r.status === 'masuk') return mulai();
    if (r.status === 'menunggu') return layarMenunggu(email);
    if (r.status === 'ditolak') return layarDitolak(email);
    if (r.status === 'perlu_kode') return layarKode(email);
    layarMasuk(r.galat || 'Tidak dapat masuk. Coba lagi sebentar.');
  });
}

function layarMenunggu(email) {
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">Permintaan terkirim</p>
    <h1>Menunggu persetujuan</h1>
    <p class="lede">Akun <b>${esc(email)}</b> sudah masuk antrean. Pemilik situs perlu menyetujuinya
      satu kali; sesudah itu kamu langsung bisa belajar dan tidak akan ditanya lagi.</p>
    <div class="note">Beri tahu gurumu bahwa kamu sudah mendaftar, lalu tekan tombol di bawah
      untuk memeriksa apakah sudah disetujui.</div>
    <div class="masuk-pilih">
      <button class="btn" id="b-periksa">Periksa lagi</button>
      <button class="btn ghost" id="b-ganti">Ganti alamat surel</button>
    </div>`);
  $('#b-periksa').addEventListener('click', async () => {
    const b = $('#b-periksa'); b.disabled = true; b.textContent = 'Memeriksa…';
    const r = await API('masuk', { method: 'POST', body: JSON.stringify({ email, peran: 'siswa' }) });
    if (r.status === 'masuk') return mulai();
    if (r.status === 'ditolak') return layarDitolak(email);
    if (r.status === 'perlu_kode') return layarKode(email);
    b.disabled = false; b.textContent = 'Periksa lagi';
    $('#app').querySelector('.note').textContent = 'Belum disetujui. Coba lagi beberapa saat lagi.';
  });
  $('#b-ganti').addEventListener('click', () => layarMasuk());
}

function layarDitolak(email) {
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">Permintaan tidak disetujui</p>
    <h1>Akun belum dapat dipakai</h1>
    <p class="lede">Permintaan untuk <b>${esc(email)}</b> tidak disetujui pemilik situs.
      Bila menurutmu ini keliru, tanyakan kepada gurumu.</p>
    <div class="masuk-pilih"><button class="btn ghost" id="b-ganti">Coba alamat lain</button></div>`);
  $('#b-ganti').addEventListener('click', () => layarMasuk());
}

function layarKode(email) {
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">Langkah terakhir</p>
    <h1>Masukkan kode akun</h1>
    <p class="lede">Akun <b>${esc(email)}</b> sudah disetujui. Mintalah kode enam huruf
      kepada gurumu, lalu masukkan di sini. Cukup sekali pada perangkat ini.</p>
    <form id="f-kode" class="masuk-form">
      <label for="m-kode">Kode akun</label>
      <input id="m-kode" type="text" maxlength="6" required autocomplete="one-time-code"
             style="text-transform:uppercase;letter-spacing:.3em;font-family:var(--mono)">
      <div class="masuk-pilih"><button class="btn" type="submit">Aktifkan</button></div>
      <p class="note" id="k-pesan" hidden></p>
    </form>`);
  $('#f-kode').addEventListener('submit', async ev => {
    ev.preventDefault();
    const r = await API('aktivasi', { method: 'POST', body: JSON.stringify({ email, kode: $('#m-kode').value }) });
    if (r.status === 'masuk') return mulai();
    const p = $('#k-pesan'); p.hidden = false; p.textContent = r.galat || 'Kode tidak cocok.';
  });
}

function layarPasang(galat) {
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">Pemasangan belum selesai</p>
    <h1>Basis data belum tersambung</h1>
    <p class="lede">${esc(galat || 'Proyek Pages ini belum diikat ke basis data D1.')}</p>
    <div class="note">Langkahnya ada di <span class="mono">PANDUAN-AKUN.md</span> pada repositori:
      buat basis data D1, ikat dengan nama <span class="mono">DB</span>, lalu isi peubah
      <span class="mono">RAHASIA</span>. Sesudah itu muat ulang halaman ini.</div>`);
}

/* ---------- progres: tarik dari peladen, dorong bila berubah ---------- */
function bacaLokal() { try { return JSON.parse(localStorage.getItem(KUNCI_PROG)) || {}; } catch { return {}; } }
function tulisLokal(d) { try { localStorage.setItem(KUNCI_PROG, JSON.stringify(d)); } catch {} }

async function tarikProgres() {
  const r = await API('progres');
  if (!r.tp) return;
  const lokal = bacaLokal(); lokal.tp = lokal.tp || {};
  let adaLokalBaru = false;
  for (const [slug, data] of Object.entries(r.tp)) lokal.tp[slug] = data;   // peladen menang saat masuk
  for (const slug of Object.keys(lokal.tp)) if (!r.tp[slug]) adaLokalBaru = true;
  tulisLokal(lokal);
  if (adaLokalBaru) FIMS.dorong(lokal);     // progres yang terlanjur dibuat sebelum masuk ikut naik
}

let jadwalDorong = null;
FIMS.dorong = function (db) {
  if (!FIMS.aku) return;
  clearTimeout(jadwalDorong);
  jadwalDorong = setTimeout(() => {
    const d = db || bacaLokal();
    API('progres', { method: 'PUT', body: JSON.stringify({ tp: d.tp || {} }) }).catch(() => {});
  }, 1200);
};

FIMS.papan = () => API('papan');

/* ---------- panel anggota ---------- */
FIMS.halAnggota = async function () {
  const app = $('#app');
  app.innerHTML = `<div class="stack"><div class="crumbs"><a href="#">Beranda</a> / Anggota</div>
    <div><div class="eyebrow">Keanggotaan</div><h1>Anggota situs</h1></div>
    <p class="muted">Memuat…</p></div>`;
  const r = await API('anggota');
  if (!r.anggota) {
    app.querySelector('.muted').textContent = r.galat || 'Tidak dapat memuat daftar anggota.';
    return;
  }
  const tgl = t => t ? new Date(t * 1000).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: '2-digit' }) : '—';
  const kelompok = { menunggu: [], aktif: [], ditolak: [] };
  r.anggota.forEach(a => (kelompok[a.status] || kelompok.ditolak).push(a));

  const baris = a => `<tr data-email="${esc(a.email)}">
      <td class="l"><b>${esc(a.nama || '—')}</b><br><span class="mono muted">${esc(a.email)}</span></td>
      <td>${a.peran === 'owner' ? 'Pemilik' : a.peran === 'guru' ? 'Guru' : 'Siswa'}</td>
      <td>${tgl(a.dibuat)}</td>
      <td>${tgl(a.terakhir)}</td>
      <td>${a.kode ? `<span class="mono">${esc(a.kode)}</span>` : '—'}</td>
      <td class="l">${a.peran !== 'owner' ? `
        ${a.status !== 'aktif' ? `<button class="btn kecil" data-putus="aktif">Setujui</button>` : ''}
        ${a.status !== 'ditolak' ? `<button class="btn ghost kecil" data-putus="ditolak">Tolak</button>` : ''}
        <button class="btn ghost kecil" data-peran="${a.peran === 'guru' ? 'siswa' : 'guru'}">Jadikan ${a.peran === 'guru' ? 'siswa' : 'guru'}</button>
        <button class="btn ghost kecil bahaya" data-hapus="1">Hapus</button>
      ` : '<span class="muted">Akun pemilik tidak dapat diubah</span>'}</td></tr>`;

  const tabel = (judul, daftar, catatan) => `<section class="panel stack">
      <h2>${judul} <span class="mcacah">${daftar.length}</span></h2>
      ${catatan ? `<p class="muted" style="margin:0">${catatan}</p>` : ''}
      ${daftar.length ? `<div class="scroll"><table><tr><th class="l">Anggota</th><th>Peran</th><th>Daftar</th><th>Terakhir</th><th>Kode</th><th class="l">Tindakan</th></tr>
        ${daftar.map(baris).join('')}</table></div>` : '<p class="muted" style="margin:0">Belum ada.</p>'}
    </section>`;

  app.innerHTML = `<div class="stack"><div class="crumbs"><a href="#">Beranda</a> / Anggota</div>
    <div><div class="eyebrow">Keanggotaan</div><h1>Anggota situs</h1>
      <p class="muted">Anda yang memutuskan siapa yang boleh masuk. Halaman ini hanya terbuka untuk pemilik situs — guru dan siswa tidak melihatnya.</p>
      <div class="note"><b>Tolak</b> menutup akses tetapi menyimpan datanya, dan bisa dibatalkan kapan saja.
        <b>Hapus</b> membuang akun beserta seluruh progres belajarnya, dan tidak dapat dikembalikan.
        Untuk murid yang sedang belajar, hampir selalu Tolak yang Anda maksud.</div></div>
    ${tabel('Menunggu persetujuan', kelompok.menunggu, 'Permintaan baru muncul di sini. Periksa alamat surelnya sebelum menyetujui.')}
    ${tabel('Aktif', kelompok.aktif)}
    ${tabel('Ditolak', kelompok.ditolak)}</div>`;

  function pasangKlik() {
  app.addEventListener('click', async ev => {
    const b = ev.target.closest('[data-putus],[data-peran],[data-hapus]');
    if (!b) return;
    const email = b.closest('tr').dataset.email;

    // Menghapus tidak dapat dibatalkan, jadi butuh dua klik: klik pertama meminta kepastian.
    if (b.dataset.hapus) {
      if (b.dataset.siap !== '1') {
        app.querySelectorAll('[data-hapus][data-siap="1"]').forEach(x => {
          x.dataset.siap = '0'; x.textContent = 'Hapus'; x.classList.remove('pasti');
        });
        b.dataset.siap = '1'; b.textContent = 'Klik lagi — hapus permanen'; b.classList.add('pasti');
        clearTimeout(b._jeda);
        b._jeda = setTimeout(() => {
          b.dataset.siap = '0'; b.textContent = 'Hapus'; b.classList.remove('pasti');
        }, 6000);
        pasangKlik();                                   // pasang ulang, klik kedua masih ditangkap
        return;
      }
      b.disabled = true; b.textContent = 'Menghapus…';
      const rh = await API('anggota/hapus', { method: 'POST', body: JSON.stringify({ email }) });
      if (!rh.ok) { b.disabled = false; b.textContent = 'Hapus'; alert(rh.galat || 'Gagal menghapus.'); pasangKlik(); return; }
      return FIMS.halAnggota();
    }

    b.disabled = true;
    const isi = b.dataset.putus ? { email, status: b.dataset.putus } : { email, peran: b.dataset.peran };
    const r2 = await API('anggota/putusan', { method: 'POST', body: JSON.stringify(isi) });
    if (!r2.ok) { b.disabled = false; alert(r2.galat || 'Gagal menyimpan.'); pasangKlik(); return; }
    FIMS.halAnggota();
  }, { once: true });
  }
  pasangKlik();
};

/* ---------- bilah kepala sesudah masuk ---------- */
function pasangBilah() {
  const nav = document.querySelector('.nav'); if (!nav || document.getElementById('akun-blok')) return;
  const a = FIMS.aku;
  document.body.classList.remove('tamu');
  const blok = document.createElement('div');
  blok.id = 'akun-blok'; blok.className = 'akun';
  blok.innerHTML = `
    ${a.guru ? `<div class="mode-alih" role="group" aria-label="Mode tampilan">
        <button type="button" data-mode="guru">Guru</button><button type="button" data-mode="siswa">Siswa</button>
      </div>` : ''}
    ${a.owner ? `<a href="#anggota" class="akun-tautan">Anggota</a>` : ''}
    <span class="akun-nama" title="${esc(a.email)}">${esc(a.nama || a.email.split('@')[0])}</span>
    <button type="button" class="akun-keluar" id="b-keluar">Keluar</button>`;
  nav.appendChild(blok);

  blok.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => {
    FIMS.setMode(b.dataset.mode);
    segarMode();
    document.dispatchEvent(new CustomEvent('fims:mode'));
  }));
  $('#b-keluar').addEventListener('click', async () => {
    await API('keluar', { method: 'POST' });
    try { localStorage.removeItem(KUNCI_PROG); } catch {}
    location.hash = ''; location.reload();
  });
  segarMode();
}

function segarMode() {
  const g = FIMS.modeGuru();
  document.body.classList.toggle('guru', g);     // mode siswa menyembunyikan menu guru
  document.querySelectorAll('[data-mode]').forEach(b => {
    const on = b.dataset.mode === (g ? 'guru' : 'siswa');
    b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  const kotak = document.getElementById('modeGuru');
  if (kotak) { kotak.checked = g; kotak.closest('.mode') && (kotak.closest('.mode').hidden = true); }
}

/* ---------- jalankan ---------- */
function muatApp() {
  const s = document.createElement('script');
  s.src = 'assets/app.js'; s.defer = true;
  document.body.appendChild(s);
}

async function mulai() {
  const r = await API('saya');
  if (r.siap === false) return layarPasang(r.galat);
  if (!r.masuk) {
    if (r.status === 'menunggu') return layarMenunggu(r.email);
    if (r.status === 'ditolak') return layarDitolak(r.email);
    return layarMasuk();
  }
  FIMS.aku = { email: r.email, nama: r.nama, peran: r.peran, guru: !!r.guru, owner: !!r.owner };
  if (FIMS.aku.guru && !localStorage.getItem(KUNCI_MODE)) FIMS.setMode('guru');
  await tarikProgres();
  pasangBilah();
  if (!window.__appDimuat) { window.__appDimuat = true; muatApp(); }
  else document.dispatchEvent(new CustomEvent('fims:segar'));
}

document.addEventListener('DOMContentLoaded', mulai);
})();
