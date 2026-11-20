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


/* ---------- dwibahasa: teks antarmuka akun ----------
   Isi pelajaran (nama topik, CP/TP, naskah soal) tidak diterjemahkan —
   redaksinya memang berbahasa Indonesia. Yang diterjemahkan hanya antarmuka. */
const EN = {
"Fitrah Islamic World Academy": "Fitrah Islamic World Academy",
"Masuk ke Fisika FIWA": "Sign in to Physics FIWA",
"Cukup dengan alamat surelmu — tidak perlu kata sandi dan tidak perlu mendaftar. Bila ini pertama kalinya, pemilik situs akan menyetujui akunmu sekali saja.": "Your email address is enough — no password, no registration. If this is your first time, the site owner approves your account once.",
"Alamat surel": "Email address",
"nama@contoh.sch.id": "name@example.sch.id",
"Nama": "Name",
"(opsional, membantu gurumu mengenali)": "(optional, helps your teacher recognise you)",
"Nama lengkap": "Full name",
"Masuk sebagai apa?": "Sign in as what?",
"Masuk sebagai Siswa": "Sign in as Student",
"Masuk sebagai Guru": "Sign in as Teacher",
"Alamat surel hanya dipakai sebagai tanda pengenal di situs ini. Tidak dikirimi apa pun, dan tidak dibagikan ke mana pun.": "Your email address is only used to identify you on this site. Nothing is ever sent to it, and it is never shared.",
"Tidak dapat masuk. Coba lagi sebentar.": "Could not sign in. Try again shortly.",
"Permintaan terkirim": "Request sent",
"Menunggu persetujuan": "Awaiting approval",
"Akun %s sudah masuk antrean. Pemilik situs perlu menyetujuinya satu kali; sesudah itu kamu langsung bisa belajar dan tidak akan ditanya lagi.": "The account %s is now in the queue. The site owner needs to approve it once; after that you can start learning and will not be asked again.",
"Beri tahu gurumu bahwa kamu sudah mendaftar, lalu tekan tombol di bawah untuk memeriksa apakah sudah disetujui.": "Tell your teacher that you have registered, then press the button below to check whether it has been approved.",
"Periksa lagi": "Check again",
"Kembali ke laman masuk": "Back to the sign-in page",
"Masukkan alamat surel dan kata sandi akunmu. Tampilan akan menyesuaikan sendiri dengan peranmu, sebagai siswa atau sebagai guru.": "Enter your email address and password. The site adjusts itself to your role, student or teacher.",
"Kata sandi": "Password",
"Lihat": "Show",
"Sembunyikan": "Hide",
"Masuk": "Sign in",
"Belum punya akun?": "No account yet?",
"Daftar di sini": "Register here",
"Sudah punya akun?": "Already have an account?",
"Masuk di sini": "Sign in here",
"Akun baru": "New account",
"Registrasi anggota": "Member registration",
"Isi data di bawah ini sekali saja. Akunmu baru dapat dipakai setelah pemilik situs menyetujuinya.": "Fill this in once. Your account can only be used after the site owner approves it.",
"(minimal 8 karakter)": "(at least 8 characters)",
"Ulangi kata sandi": "Repeat password",
"Daftar sebagai apa?": "Register as what?",
"Kirim registrasi": "Submit registration",
"Kata sandi minimal 8 karakter.": "The password must be at least 8 characters.",
"Kedua kata sandi belum sama.": "The two passwords do not match yet.",
"Registrasi gagal. Coba lagi sebentar.": "Registration failed. Try again shortly.",
"Akun guru": "Teacher accounts",
"Akun siswa": "Student accounts",
"Belum ada akun guru.": "No teacher accounts yet.",
"Belum ada akun siswa.": "No student accounts yet.",
"Memeriksa…": "Checking…",
"Belum disetujui. Coba lagi beberapa saat lagi.": "Not approved yet. Try again in a little while.",
"Permintaan tidak disetujui": "Request declined",
"Akun belum dapat dipakai": "This account cannot be used yet",
"Permintaan untuk %s tidak disetujui pemilik situs. Bila menurutmu ini keliru, tanyakan kepada gurumu.": "The request for %s was declined by the site owner. If you think this is a mistake, ask your teacher.",
"Coba alamat lain": "Try another address",
"Langkah terakhir": "Last step",
"Masukkan kode akun": "Enter your account code",
"Akun %s sudah disetujui. Mintalah kode enam huruf kepada gurumu, lalu masukkan di sini. Cukup sekali pada perangkat ini.": "The account %s has been approved. Ask your teacher for the six-letter code and enter it here. Once on this device is enough.",
"Kode akun": "Account code",
"Aktifkan": "Activate",
"Kode tidak cocok.": "That code does not match.",
"Pemasangan belum selesai": "Setup is not finished",
"Basis data belum tersambung": "The database is not connected",
"Proyek Pages ini belum diikat ke basis data D1.": "This Pages project is not bound to a D1 database yet.",
"Langkahnya ada di %s pada repositori: buat basis data D1, ikat dengan nama %s, lalu isi peubah %s. Sesudah itu muat ulang halaman ini.": "The steps are in %s in the repository: create a D1 database, bind it under the name %s, then set the %s variable. Reload this page afterwards.",
"Guru": "Teacher",
"Siswa": "Student",
"Pemilik": "Owner",
"Mode tampilan": "View mode",
"Anggota": "Members",
"Pembimbing": "Mentors",
"Atur pembimbing": "Set mentors",
"Pembimbing %s": "Mentors for %s",
"Centang guru yang membimbing murid ini. Satu murid boleh punya beberapa guru, dan satu guru boleh membimbing banyak murid.": "Tick the teachers who mentor this student. A student may have several teachers, and a teacher may mentor many students.",
"Belum ada akun guru yang aktif.": "No active teacher accounts yet.",
"Belum ada": "None yet",
"Simpan pembimbing": "Save mentors",
"Batal": "Cancel",
"Gagal menyimpan pembimbing.": "Could not save the mentors.",
"Memuat daftar guru…": "Loading the teacher list…",
"%s anggota menunggu persetujuan": "%s members awaiting approval",
"1 anggota menunggu persetujuan": "1 member awaiting approval",
"Notifikasi": "Notifications",
"Notifikasi anggota": "Member notifications",
"Tidak ada anggota yang menunggu persetujuan.": "No members are awaiting approval.",
"Tidak dapat memuat notifikasi.": "Could not load notifications.",
"Tinjau di halaman Anggota": "Review on the Members page",
"dan %s lainnya": "and %s more",
"Keluar": "Sign out",
"Memuat…": "Loading…",
"Tidak dapat memuat daftar anggota.": "Could not load the member list.",
"Beranda": "Home",
"Keanggotaan": "Membership",
"Anggota situs": "Site members",
"Anda yang memutuskan siapa yang boleh masuk. Halaman ini hanya terbuka untuk pemilik situs — guru dan siswa tidak melihatnya.": "You decide who may sign in. This page is open to the site owner only — teachers and students never see it.",
"<b>Tolak</b> menutup akses tetapi menyimpan datanya, dan bisa dibatalkan kapan saja. <b>Hapus</b> membuang akun beserta seluruh progres belajarnya, dan tidak dapat dikembalikan. Untuk murid yang sedang belajar, hampir selalu Tolak yang Anda maksud.": "<b>Decline</b> closes access but keeps the data, and can be undone at any time. <b>Delete</b> removes the account together with all of its learning progress, and cannot be undone. For a student who is still learning, Decline is almost always what you mean.",
"Permintaan baru muncul di sini. Periksa alamat surelnya sebelum menyetujui.": "New requests appear here. Check the email address before approving.",
"Aktif": "Active",
"Ditolak": "Declined",
"Peran": "Role",
"Daftar": "Joined",
"Terakhir": "Last seen",
"Kode": "Code",
"Tindakan": "Actions",
"Belum ada.": "None yet.",
"Setujui": "Approve",
"Tolak": "Decline",
"Jadikan guru": "Make teacher",
"Jadikan siswa": "Make student",
"Hapus": "Delete",
"Ubah nama": "Rename",
"Ubah sandi": "Reset password",
"Kata sandi baru, minimal 8 karakter": "New password, at least 8 characters",
"Kata sandi baru": "New password",
"Kata sandi minimal 8 karakter.": "The password must be at least 8 characters.",
"Gagal menyimpan kata sandi.": "Could not save the password.",
"Kata sandi %s sudah diganti. Beri tahu yang bersangkutan.": "The password for %s has been changed. Let them know.",
"Simpan": "Save",
"Batal": "Cancel",
"Menyimpan…": "Saving…",
"Menghapus…": "Deleting…",
"Klik lagi — hapus permanen": "Click again — delete permanently",
"Nama anggota": "Member name",
"Peran dan akses pemilik tidak dapat diubah": "The owner's role and access cannot be changed",
"Gagal menyimpan nama.": "Could not save the name.",
"Gagal menghapus.": "Could not delete.",
"Gagal menyimpan.": "Could not save."
};
let BHS = 'id';
try { const d = JSON.parse(localStorage.getItem(KUNCI_PROG)) || {};
      BHS = (d.opsi && d.opsi.bahasa) === 'en' ? 'en' : 'id'; } catch {}
const t  = x => (BHS === 'id' || EN[x] === undefined) ? x : EN[x];
const tf = (x, ...v) => { let i = 0; return t(x).replace(/%s/g, () => v[i++]); };
FIMS.bahasa = () => BHS;

let layarKini = null;                       // penggambar layar akun yang sedang tampil

function setBahasa(v) {
  BHS = v === 'en' ? 'en' : 'id';
  document.documentElement.lang = BHS;
  document.querySelectorAll('[data-bhs]').forEach(b =>
    b.setAttribute('aria-pressed', b.dataset.bhs === BHS ? 'true' : 'false'));
  const blok = document.getElementById('akun-blok');
  if (blok) { blok.remove(); pasangBilah(); }
  const app = $('#app');
  if (layarKini && app && app.querySelector('[data-akun-layar]')) layarKini();
}

/* Sebelum app.js dimuat (yaitu di layar masuk), tombol ID/EN ditangani di sini. */
document.addEventListener('click', ev => {
  const b = ev.target.closest('[data-bhs]');
  if (!b || window.__appDimuat) return;
  const v = b.dataset.bhs === 'en' ? 'en' : 'id';
  if (v === BHS) return;
  const d = bacaLokal(); d.opsi = d.opsi || {}; d.opsi.bahasa = v; tulisLokal(d);
  setBahasa(v);
});
/* Sesudah app.js dimuat, app.js yang mengabarkan pergantian bahasa. */
document.addEventListener('fims:bahasa', ev => setBahasa(ev.detail));

/* ---------- gambar layar ---------- */
const bungkus = isi => `<div class="masuk-bingkai" data-akun-layar><section class="masuk-kotak">${isi}</section></div>`;

function layarMasuk(pesan, isian) {
  const v = isian || {};
  layarKini = () => layarMasuk(pesan, v);
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">${t('Fitrah Islamic World Academy')}</p>
    <h1>${t('Masuk ke Fisika FIWA')}</h1>
    <p class="lede">${t('Masukkan alamat surel dan kata sandi akunmu. Tampilan akan menyesuaikan sendiri dengan peranmu, sebagai siswa atau sebagai guru.')}</p>
    ${pesan ? `<div class="note galat">${esc(pesan)}</div>` : ''}
    <form id="f-masuk" class="masuk-form" autocomplete="on">
      <label for="m-email">${t('Alamat surel')}</label>
      <input id="m-email" name="email" type="email" inputmode="email" autocomplete="username"
             placeholder="${t('nama@contoh.sch.id')}" value="${esc(v.email || '')}" required>
      <label for="m-sandi">${t('Kata sandi')}</label>
      <div class="sandi-baris">
        <input id="m-sandi" name="password" type="password" autocomplete="current-password" required>
        <button type="button" class="btn ghost kecil" id="b-lihat" aria-pressed="false">${t('Lihat')}</button>
      </div>
      <div class="masuk-pilih"><button class="btn" type="submit">${t('Masuk')}</button></div>
      <p class="muted masuk-kaki">${t('Belum punya akun?')}
        <a href="#" id="b-ke-daftar" class="tautan-kuat">${t('Daftar di sini')}</a></p>
    </form>`);

  const lihat = $('#b-lihat');
  lihat.addEventListener('click', () => {
    const i = $('#m-sandi'), buka = i.type === 'password';
    i.type = buka ? 'text' : 'password';
    lihat.textContent = buka ? t('Sembunyikan') : t('Lihat');
    lihat.setAttribute('aria-pressed', buka ? 'true' : 'false');
    i.focus();
  });
  $('#b-ke-daftar').addEventListener('click', ev => { ev.preventDefault(); layarDaftar(); });

  $('#f-masuk').addEventListener('submit', async ev => {
    ev.preventDefault();
    const email = $('#m-email').value.trim(), sandi = $('#m-sandi').value;
    const tombol = $('#f-masuk').querySelectorAll('button');
    tombol.forEach(b => b.disabled = true);
    const r = await API('masuk', { method: 'POST', body: JSON.stringify({ email, sandi }) });
    tombol.forEach(b => b.disabled = false);
    if (r.status === 'masuk') return mulai();
    if (r.status === 'menunggu') return layarMenunggu(email, sandi);
    if (r.status === 'ditolak') return layarDitolak(email);
    if (r.status === 'perlu_kode') return layarKode(email);
    layarMasuk(r.galat || t('Tidak dapat masuk. Coba lagi sebentar.'), { email });
  });
}

/* ---------- registrasi ----------
   Akun yang baru dibuat berstatus menunggu; pemilik situs menyetujuinya sekali. */
function layarDaftar(pesan, isian) {
  const v = isian || {};
  layarKini = () => layarDaftar(pesan, v);
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">${t('Akun baru')}</p>
    <h1>${t('Registrasi anggota')}</h1>
    <p class="lede">${t('Isi data di bawah ini sekali saja. Akunmu baru dapat dipakai setelah pemilik situs menyetujuinya.')}</p>
    ${pesan ? `<div class="note galat">${esc(pesan)}</div>` : ''}
    <form id="f-daftar" class="masuk-form" autocomplete="on">
      <label for="d-nama">${t('Nama lengkap')}</label>
      <input id="d-nama" type="text" autocomplete="name" maxlength="80" value="${esc(v.nama || '')}" required>

      <label for="d-email">${t('Alamat surel')}</label>
      <input id="d-email" type="email" inputmode="email" autocomplete="username"
             placeholder="${t('nama@contoh.sch.id')}" value="${esc(v.email || '')}" required>

      <label for="d-sandi">${t('Kata sandi')} <span class="muted">${t('(minimal 8 karakter)')}</span></label>
      <div class="sandi-baris">
        <input id="d-sandi" type="password" autocomplete="new-password" minlength="8" required>
        <button type="button" class="btn ghost kecil" id="b-lihat-d" aria-pressed="false">${t('Lihat')}</button>
      </div>

      <label for="d-ulang">${t('Ulangi kata sandi')}</label>
      <input id="d-ulang" type="password" autocomplete="new-password" minlength="8" required>

      <p class="muted masuk-tanya">${t('Daftar sebagai apa?')}</p>
      <div class="masuk-pilih peran-pilih" role="group">
        <button type="button" class="btn peran on" data-peran="siswa">${t('Siswa')}</button>
        <button type="button" class="btn ghost peran" data-peran="guru">${t('Guru')}</button>
      </div>

      <div class="masuk-pilih"><button class="btn" type="submit" id="b-kirim-daftar">${t('Kirim registrasi')}</button></div>
      <p class="muted masuk-kaki">${t('Sudah punya akun?')}
        <a href="#" id="b-ke-masuk" class="tautan-kuat">${t('Masuk di sini')}</a></p>
    </form>`);

  let peran = v.peran === 'guru' ? 'guru' : 'siswa';
  const tombolPeran = $('#f-daftar').querySelectorAll('.peran');
  const segarPeran = () => tombolPeran.forEach(b => {
    const on = b.dataset.peran === peran;
    b.classList.toggle('on', on); b.classList.toggle('ghost', !on);
  });
  tombolPeran.forEach(b => b.addEventListener('click', () => { peran = b.dataset.peran; segarPeran(); }));
  segarPeran();

  const lihat = $('#b-lihat-d');
  lihat.addEventListener('click', () => {
    const buka = $('#d-sandi').type === 'password';
    $('#d-sandi').type = $('#d-ulang').type = buka ? 'text' : 'password';
    lihat.textContent = buka ? t('Sembunyikan') : t('Lihat');
    lihat.setAttribute('aria-pressed', buka ? 'true' : 'false');
  });
  $('#b-ke-masuk').addEventListener('click', ev => { ev.preventDefault(); layarMasuk(); });

  $('#f-daftar').addEventListener('submit', async ev => {
    ev.preventDefault();
    const nama = $('#d-nama').value.trim(), email = $('#d-email').value.trim();
    const sandi = $('#d-sandi').value, ulang = $('#d-ulang').value;
    const simpan = { nama, email, peran };
    if (sandi.length < 8) return layarDaftar(t('Kata sandi minimal 8 karakter.'), simpan);
    if (sandi !== ulang)  return layarDaftar(t('Kedua kata sandi belum sama.'), simpan);

    const tombol = $('#f-daftar').querySelectorAll('button');
    tombol.forEach(b => b.disabled = true);
    const r = await API('daftar', { method: 'POST', body: JSON.stringify({ nama, email, sandi, peran }) });
    tombol.forEach(b => b.disabled = false);
    if (r.status === 'masuk') return mulai();
    if (r.status === 'menunggu') return layarMenunggu(email, sandi);
    if (r.status === 'ditolak') return layarDitolak(email);
    layarDaftar(r.galat || t('Registrasi gagal. Coba lagi sebentar.'), simpan);
  });
}

function layarMenunggu(email, sandi) {
  layarKini = () => layarMenunggu(email, sandi);
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">${t('Permintaan terkirim')}</p>
    <h1>${t('Menunggu persetujuan')}</h1>
    <p class="lede">${tf('Akun %s sudah masuk antrean. Pemilik situs perlu menyetujuinya satu kali; sesudah itu kamu langsung bisa belajar dan tidak akan ditanya lagi.', '<b>' + esc(email) + '</b>')}</p>
    <div class="note">${t('Beri tahu gurumu bahwa kamu sudah mendaftar, lalu tekan tombol di bawah untuk memeriksa apakah sudah disetujui.')}</div>
    <div class="masuk-pilih">
      <button class="btn" id="b-periksa">${t('Periksa lagi')}</button>
      <button class="btn ghost" id="b-ganti">${t('Kembali ke laman masuk')}</button>
    </div>`);
  $('#b-periksa').addEventListener('click', async () => {
    const b = $('#b-periksa'); b.disabled = true; b.textContent = t('Memeriksa…');
    const r = sandi
      ? await API('masuk', { method: 'POST', body: JSON.stringify({ email, sandi }) })
      : { status: 'menunggu' };
    if (r.status === 'masuk') return mulai();
    if (r.status === 'ditolak') return layarDitolak(email);
    if (r.status === 'perlu_kode') return layarKode(email);
    b.disabled = false; b.textContent = t('Periksa lagi');
    $('#app').querySelector('.note').textContent = t('Belum disetujui. Coba lagi beberapa saat lagi.');
  });
  $('#b-ganti').addEventListener('click', () => layarMasuk());
}

function layarDitolak(email) {
  layarKini = () => layarDitolak(email);
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">${t('Permintaan tidak disetujui')}</p>
    <h1>${t('Akun belum dapat dipakai')}</h1>
    <p class="lede">${tf('Permintaan untuk %s tidak disetujui pemilik situs. Bila menurutmu ini keliru, tanyakan kepada gurumu.', '<b>' + esc(email) + '</b>')}</p>
    <div class="masuk-pilih"><button class="btn ghost" id="b-ganti">${t('Coba alamat lain')}</button></div>`);
  $('#b-ganti').addEventListener('click', () => layarMasuk());
}

function layarKode(email) {
  layarKini = () => layarKode(email);
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">${t('Langkah terakhir')}</p>
    <h1>${t('Masukkan kode akun')}</h1>
    <p class="lede">${tf('Akun %s sudah disetujui. Mintalah kode enam huruf kepada gurumu, lalu masukkan di sini. Cukup sekali pada perangkat ini.', '<b>' + esc(email) + '</b>')}</p>
    <form id="f-kode" class="masuk-form">
      <label for="m-kode">${t('Kode akun')}</label>
      <input id="m-kode" type="text" maxlength="6" required autocomplete="one-time-code"
             style="text-transform:uppercase;letter-spacing:.3em;font-family:var(--mono)">
      <div class="masuk-pilih"><button class="btn" type="submit">${t('Aktifkan')}</button></div>
      <p class="note" id="k-pesan" hidden></p>
    </form>`);
  $('#f-kode').addEventListener('submit', async ev => {
    ev.preventDefault();
    const r = await API('aktivasi', { method: 'POST', body: JSON.stringify({ email, kode: $('#m-kode').value }) });
    if (r.status === 'masuk') return mulai();
    const p = $('#k-pesan'); p.hidden = false; p.textContent = r.galat || t('Kode tidak cocok.');
  });
}

function layarPasang(galat) {
  layarKini = () => layarPasang(galat);
  const mono = x => `<span class="mono">${x}</span>`;
  $('#app').innerHTML = bungkus(`
    <p class="eyebrow">${t('Pemasangan belum selesai')}</p>
    <h1>${t('Basis data belum tersambung')}</h1>
    <p class="lede">${esc(galat || t('Proyek Pages ini belum diikat ke basis data D1.'))}</p>
    <div class="note">${tf('Langkahnya ada di %s pada repositori: buat basis data D1, ikat dengan nama %s, lalu isi peubah %s. Sesudah itu muat ulang halaman ini.',
      mono('PANDUAN-AKUN.md'), mono('DB'), mono('RAHASIA'))}</div>`);
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

let jadwalDorong = null, belumTerkirim = false;
FIMS.dorong = function (db) {
  if (!FIMS.aku) return;
  belumTerkirim = true;
  clearTimeout(jadwalDorong);
  jadwalDorong = setTimeout(() => {
    const d = db || bacaLokal();
    belumTerkirim = false;
    API('progres', { method: 'PUT', body: JSON.stringify({ tp: d.tp || {} }) })
      .then(r => { if (r && r.usang && Object.keys(r.usang).length) adopsiDariPeladen(r.usang); })
      .catch(() => { belumTerkirim = true; });
  }, 1200);
};

/* ---------- guru mengubah progres murid: peramban murid menyusul ----------
   Guru bisa menilai atau mereset satu dokumen murid. Peladen menaikkan nomor "epoch" TP itu.
   Peramban murid yang masih memegang salinan lama (a) ditolak saat mengirim, lalu diberi salinan
   baru dalam jawabannya, dan (b) mengecek nomor epoch tiap 30 detik serta saat tab kembali tampak.
   Salinan baru dipasang ke penyimpanan lokal dan diumumkan ke app.js lewat peristiwa fims:progres. */
function adopsiDariPeladen(peta) {
  const lokal = bacaLokal(); lokal.tp = lokal.tp || {};
  for (const [slug, data] of Object.entries(peta)) lokal.tp[slug] = data;
  tulisLokal(lokal);
  document.dispatchEvent(new CustomEvent('fims:progres', { detail: { tp: peta } }));
}

async function segarProgres() {
  if (!FIMS.aku) return;
  const r = await API('progres?epoch=1');
  if (!r.epoch) return;
  const lokal = (bacaLokal().tp) || {};
  const perlu = Object.keys(r.epoch).filter(slug => (r.epoch[slug] || 0) > ((lokal[slug] && lokal[slug].epoch) || 0));
  if (!perlu.length) return;
  const p = await API('progres');
  if (!p.tp) return;
  const ambil = {};
  for (const slug of perlu) if (p.tp[slug]) ambil[slug] = p.tp[slug];
  if (Object.keys(ambil).length) adopsiDariPeladen(ambil);
}
setInterval(() => { if (document.visibilityState === 'visible') segarProgres().catch(() => {}); }, 30000);
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') segarProgres().catch(() => {});
});

/* Tab ditutup, ponsel dikunci, atau pindah aplikasi: kirim sekarang juga.
   Tanpa ini, perubahan pada 1,2 detik terakhir sebelum halaman ditinggalkan
   tidak pernah sampai ke peladen, dan hilang di perangkat berikutnya. */
function dorongSegera() {
  if (!FIMS.aku || !belumTerkirim) return;
  clearTimeout(jadwalDorong);
  const isi = JSON.stringify({ tp: bacaLokal().tp || {} });
  belumTerkirim = false;
  try {
    if (navigator.sendBeacon &&
        navigator.sendBeacon('/api/progres', new Blob([isi], { type: 'application/json' }))) return;
  } catch {}
  try {
    fetch('/api/progres', { method: 'PUT', body: isi, keepalive: true,
      credentials: 'same-origin', headers: { 'content-type': 'application/json' } }).catch(() => {});
  } catch {}
}
window.addEventListener('pagehide', dorongSegera);
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') dorongSegera();
});

FIMS.papan = () => API('papan');
/* Dibuka untuk app.js: antrean penilaian dan penyimpanan nilai oleh guru. */
FIMS.API = (jalur, opsi) => API(jalur, opsi);
/* Kunci dokumen isian = alamat berkas tanpa "/" depan, tanpa ".html", tanpa "index". Harus identik dengan
   bentukKunci() di assets/fims-simpan.js: keduanya menunjuk baris yang sama di tabel "lembar". */
FIMS.kunciLembar = jalur => {
  let p = String(jalur || '').replace(/[?#].*$/, '').replace(/^\/+/, '');
  try { p = decodeURIComponent(p); } catch {}
  p = p.replace(/\/index\.html?$/i, '').replace(/\.html?$/i, '').replace(/\/+$/, '');
  return p.replace(/[^A-Za-z0-9._\-\/]/g, '_').replace(/\/{2,}/g, '/').replace(/\.\.+/g, '.').slice(0, 200);
};

/* ---------- panel anggota ---------- */
/* Dipakai bersama oleh penggambar tabel dan pendengar klik yang tetap.
   Diperbarui setiap kali daftar anggota dimuat ulang. */
let _daftarGuru = [], _bimbingan = {};

FIMS.halAnggota = async function () {
  const app = $('#app');
  app.innerHTML = `<div class="stack" data-akun-layar><div class="crumbs"><a href="#">${t('Beranda')}</a> / ${t('Anggota')}</div>
    <div><div class="eyebrow">${t('Keanggotaan')}</div><h1>${t('Anggota situs')}</h1></div>
    <p class="muted">${t('Memuat…')}</p></div>`;
  const r = await API('anggota');
  if (!r.anggota) {
    app.querySelector('.muted').textContent = r.galat || t('Tidak dapat memuat daftar anggota.');
    return;
  }
  const tgl = w => w ? new Date(w * 1000).toLocaleDateString(BHS === 'en' ? 'en-GB' : 'id-ID', { day: 'numeric', month: 'short', year: '2-digit' }) : '—';
  const kelompok = { menunggu: [], aktif: [], ditolak: [] };
  r.anggota.forEach(a => (kelompok[a.status] || kelompok.ditolak).push(a));
  FIMS.setMenunggu(kelompok.menunggu.length);

  /* Pembimbingan: satu murid boleh punya beberapa guru, satu guru banyak murid.
     Dimuat sekali di sini, lalu dipakai oleh setiap baris siswa. */
  const rb = await API('bimbing').catch(() => ({}));
  _daftarGuru = rb.guru || [];
  const namaGuru = e => { const g = _daftarGuru.find(x => x.email === e); return (g && g.nama) || e; };
  _bimbingan = {};                            // murid -> [surel guru]
  (rb.pasangan || []).forEach(x => (_bimbingan[x.murid] = _bimbingan[x.murid] || []).push(x.guru));
  const namaPembimbing = email => {
    const d = _bimbingan[email] || [];
    return d.length ? d.map(g => `<span class="cip">${esc(namaGuru(g))}</span>`).join(' ')
                    : `<span class="muted">${t('Belum ada')}</span>`;
  };

  const baris = a => `<tr data-email="${esc(a.email)}">
      <td class="l"><b class="nm-teks">${esc(a.nama || '—')}</b><br><span class="mono muted">${esc(a.email)}</span></td>
      <td>${a.peran === 'owner' ? t('Pemilik') : a.peran === 'guru' ? t('Guru') : t('Siswa')}</td>
      <td>${tgl(a.dibuat)}</td>
      <td>${tgl(a.terakhir)}</td>
      <td>${a.kode ? `<span class="mono">${esc(a.kode)}</span>` : '—'}</td>
      ${a.peran === 'siswa' ? `<td class="l bimb-sel">${namaPembimbing(a.email)}</td>` : ''}
      <td class="l">
        ${a.peran === 'siswa' ? `<button class="btn ghost kecil" data-bimbing="1">${t('Atur pembimbing')}</button>` : ''}
        <button class="btn ghost kecil" data-nama="1">${t('Ubah nama')}</button>
        <button class="btn ghost kecil" data-sandi="1">${t('Ubah sandi')}</button>
        ${a.peran !== 'owner' ? `
        ${a.status !== 'aktif' ? `<button class="btn kecil" data-putus="aktif">${t('Setujui')}</button>` : ''}
        ${a.status !== 'ditolak' ? `<button class="btn ghost kecil" data-putus="ditolak">${t('Tolak')}</button>` : ''}
        <button class="btn ghost kecil" data-peran="${a.peran === 'guru' ? 'siswa' : 'guru'}">${a.peran === 'guru' ? t('Jadikan siswa') : t('Jadikan guru')}</button>
        <button class="btn ghost kecil bahaya" data-hapus="1">${t('Hapus')}</button>
      ` : `<span class="muted">${t('Peran dan akses pemilik tidak dapat diubah')}</span>`}</td></tr>`;

  const tabelKecil = (daftar, kosong, siswa) => daftar.length
    ? `<div class="scroll"><table><tr><th class="l">${t('Anggota')}</th><th>${t('Peran')}</th><th>${t('Daftar')}</th><th>${t('Terakhir')}</th><th>${t('Kode')}</th>${siswa ? `<th class="l">${t('Pembimbing')}</th>` : ''}<th class="l">${t('Tindakan')}</th></tr>
        ${daftar.map(baris).join('')}</table></div>`
    : `<p class="muted" style="margin:0">${kosong}</p>`;

  /* Guru dan siswa dipisahkan ke dalam dua tabel pada setiap kelompok status.
     Pemilik situs ikut pada tabel guru, karena perannya memang mengajar. */
  const tabel = (judul, daftar, catatan) => {
    const guru  = daftar.filter(a => a.peran === 'guru' || a.peran === 'owner');
    const siswa = daftar.filter(a => a.peran !== 'guru' && a.peran !== 'owner');
    return `<section class="panel stack">
      <h2>${judul} <span class="mcacah">${daftar.length}</span></h2>
      ${catatan ? `<p class="muted" style="margin:0">${catatan}</p>` : ''}
      <h3 class="mjudul">${t('Akun guru')} <span class="mcacah">${guru.length}</span></h3>
      ${tabelKecil(guru, t('Belum ada akun guru.'), false)}
      <h3 class="mjudul">${t('Akun siswa')} <span class="mcacah">${siswa.length}</span></h3>
      ${tabelKecil(siswa, t('Belum ada akun siswa.'), true)}
    </section>`;
  };

  app.innerHTML = `<div class="stack" data-akun-layar><div class="crumbs"><a href="#">${t('Beranda')}</a> / ${t('Anggota')}</div>
    <div><div class="eyebrow">${t('Keanggotaan')}</div><h1>${t('Anggota situs')}</h1>
      <p class="muted">${t('Anda yang memutuskan siapa yang boleh masuk. Halaman ini hanya terbuka untuk pemilik situs — guru dan siswa tidak melihatnya.')}</p>
      <div class="note">${t('<b>Tolak</b> menutup akses tetapi menyimpan datanya, dan bisa dibatalkan kapan saja. <b>Hapus</b> membuang akun beserta seluruh progres belajarnya, dan tidak dapat dikembalikan. Untuk murid yang sedang belajar, hampir selalu Tolak yang Anda maksud.')}</div></div>
    ${tabel(t('Menunggu persetujuan'), kelompok.menunggu, t('Permintaan baru muncul di sini. Periksa alamat surelnya sebelum menyetujui.'))}
    ${tabel(t('Aktif'), kelompok.aktif)}
    ${tabel(t('Ditolak'), kelompok.ditolak)}</div>`;

  /* Satu pendengar tetap untuk seluruh panel. Dahulu dipasang dengan
     { once: true } dan dipasang ulang di tiap cabang; akibatnya klik apa pun
     yang tidak cocok — mencentang kotak, misalnya — ikut mencopot pendengarnya
     dan panel berhenti menanggapi. */
  function pasangKlik() {
  if (app.dataset.klikTerpasang) return;
  app.dataset.klikTerpasang = '1';
  app.addEventListener('click', async ev => {
    const b = ev.target.closest('[data-putus],[data-peran],[data-hapus],[data-nama],[data-simpan-nama],[data-batal-nama],[data-sandi],[data-simpan-sandi],[data-batal-sandi],[data-bimbing],[data-simpan-bimbing],[data-batal-bimbing]');
    if (!b) return;
    const email = b.closest('tr').dataset.email;

    /* Mengatur guru pembimbing seorang murid. Daftarnya dikirim utuh, bukan
       satu-satu, supaya tidak ada keadaan setengah tersimpan bila jaringan putus. */
    if (b.dataset.bimbing) {
      const sel = b.closest('tr').querySelector('.bimb-sel');
      if (!sel || sel.querySelector('.bimb-atur')) { pasangKlik(); return; }
      const kini = _bimbingan[email] || [];
      sel.innerHTML = _daftarGuru.length
        ? `<div class="bimb-atur">
             <p class="muted" style="margin:0 0 .4rem">${t('Centang guru yang membimbing murid ini. Satu murid boleh punya beberapa guru, dan satu guru boleh membimbing banyak murid.')}</p>
             ${_daftarGuru.map(g => `<label class="bimb-baris"><input type="checkbox" value="${esc(g.email)}"${kini.includes(g.email) ? ' checked' : ''}> ${esc(g.nama || g.email)} <span class="mono muted">${esc(g.email)}</span></label>`).join('')}
             <div class="row" style="gap:.4rem;margin-top:.5rem">
               <button class="btn kecil" data-simpan-bimbing="1">${t('Simpan pembimbing')}</button>
               <button class="btn ghost kecil" data-batal-bimbing="1">${t('Batal')}</button></div></div>`
        : `<span class="muted">${t('Belum ada akun guru yang aktif.')}</span>`;
      pasangKlik(); return;
    }
    if (b.dataset.batalBimbing) { FIMS.halAnggota(); return; }
    if (b.dataset.simpanBimbing) {
      const kotak = [...b.closest('.bimb-atur').querySelectorAll('input[type=checkbox]')];
      const pilih = kotak.filter(k => k.checked).map(k => k.value);
      b.disabled = true;
      const rb2 = await API('bimbing/atur', { method: 'POST', body: JSON.stringify({ murid: email, guru: pilih }) });
      if (!rb2.ok) { b.disabled = false; alert(rb2.galat || t('Gagal menyimpan pembimbing.')); pasangKlik(); return; }
      FIMS.halAnggota(); return;
    }

    /* Menyetel ulang kata sandi anggota. Sandi lama tidak dapat dibaca siapa pun,
       termasuk pemilik situs — yang ada hanyalah menggantinya dengan yang baru. */
    if (b.dataset.sandi) {
      const sel = b.closest('tr').querySelector('.nm-teks');
      if (!sel || sel.querySelector('.sd-isi')) { pasangKlik(); return; }
      sel.innerHTML = `<input class="nm-isi sd-isi" type="text" minlength="8" maxlength="72"
          placeholder="${t('Kata sandi baru, minimal 8 karakter')}" aria-label="${t('Kata sandi baru')}">
        <button class="btn kecil" data-simpan-sandi="1">${t('Simpan')}</button>
        <button class="btn ghost kecil" data-batal-sandi="1">${t('Batal')}</button>`;
      const inp = sel.querySelector('.sd-isi');
      inp.addEventListener('keydown', e => {
        if (e.key === 'Enter') { e.preventDefault(); sel.querySelector('[data-simpan-sandi]').click(); }
        if (e.key === 'Escape') { e.preventDefault(); FIMS.halAnggota(); }
      });
      inp.focus();
      pasangKlik(); return;
    }
    if (b.dataset.batalSandi) return FIMS.halAnggota();
    if (b.dataset.simpanSandi) {
      const inp = b.closest('tr').querySelector('.sd-isi');
      const sandi = inp.value || '';
      if (sandi.length < 8) { alert(t('Kata sandi minimal 8 karakter.')); inp.focus(); pasangKlik(); return; }
      b.disabled = true; b.textContent = t('Menyimpan…');
      const rs = await API('anggota/sandi', { method: 'POST', body: JSON.stringify({ email, sandi }) });
      if (!rs.ok) alert(rs.galat || t('Gagal menyimpan kata sandi.'));
      else alert(tf('Kata sandi %s sudah diganti. Beri tahu yang bersangkutan.', email));
      return FIMS.halAnggota();
    }

    // Mengubah nama anggota: sel nama berganti menjadi kolom isian di tempat.
    if (b.dataset.nama) {
      const sel = b.closest('tr').querySelector('.nm-teks');
      if (!sel || sel.querySelector('.nm-isi')) { pasangKlik(); return; }
      const lama = sel.textContent.trim() === '—' ? '' : sel.textContent.trim();
      sel.innerHTML = `<input class="nm-isi" type="text" maxlength="80" value="${esc(lama)}" aria-label="${t('Nama anggota')}">
        <button class="btn kecil" data-simpan-nama="1">${t('Simpan')}</button>
        <button class="btn ghost kecil" data-batal-nama="1">${t('Batal')}</button>`;
      const inp = sel.querySelector('.nm-isi');
      inp.addEventListener('keydown', e => {
        if (e.key === 'Enter') { e.preventDefault(); sel.querySelector('[data-simpan-nama]').click(); }
        if (e.key === 'Escape') { e.preventDefault(); FIMS.halAnggota(); }
      });
      inp.focus(); inp.select();
      pasangKlik(); return;
    }
    if (b.dataset.batalNama) return FIMS.halAnggota();
    if (b.dataset.simpanNama) {
      const inp = b.closest('tr').querySelector('.nm-isi');
      const nama = (inp.value || '').trim();
      if (!nama) { inp.focus(); pasangKlik(); return; }
      b.disabled = true; b.textContent = t('Menyimpan…');
      const rn = await API('anggota/putusan', { method: 'POST', body: JSON.stringify({ email, nama }) });
      if (!rn.ok) alert(rn.galat || t('Gagal menyimpan nama.'));
      return FIMS.halAnggota();
    }

    // Menghapus tidak dapat dibatalkan, jadi butuh dua klik: klik pertama meminta kepastian.
    if (b.dataset.hapus) {
      if (b.dataset.siap !== '1') {
        app.querySelectorAll('[data-hapus][data-siap="1"]').forEach(x => {
          x.dataset.siap = '0'; x.textContent = t('Hapus'); x.classList.remove('pasti');
        });
        b.dataset.siap = '1'; b.textContent = t('Klik lagi — hapus permanen'); b.classList.add('pasti');
        clearTimeout(b._jeda);
        b._jeda = setTimeout(() => {
          b.dataset.siap = '0'; b.textContent = t('Hapus'); b.classList.remove('pasti');
        }, 6000);
        pasangKlik();                                   // pasang ulang, klik kedua masih ditangkap
        return;
      }
      b.disabled = true; b.textContent = t('Menghapus…');
      const rh = await API('anggota/hapus', { method: 'POST', body: JSON.stringify({ email }) });
      if (!rh.ok) { b.disabled = false; b.textContent = t('Hapus'); alert(rh.galat || t('Gagal menghapus.')); pasangKlik(); return; }
      return FIMS.halAnggota();
    }

    b.disabled = true;
    const isi = b.dataset.putus ? { email, status: b.dataset.putus } : { email, peran: b.dataset.peran };
    const r2 = await API('anggota/putusan', { method: 'POST', body: JSON.stringify(isi) });
    if (!r2.ok) { b.disabled = false; alert(r2.galat || t('Gagal menyimpan.')); pasangKlik(); return; }
    if (r2.menunggu !== undefined) FIMS.setMenunggu(r2.menunggu);
    FIMS.halAnggota();
  });
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
    ${a.guru ? `<div class="mode-alih" role="group" aria-label="${t('Mode tampilan')}">
        <button type="button" data-mode="guru">${t('Guru')}</button><button type="button" data-mode="siswa">${t('Siswa')}</button>
      </div>` : ''}
    ${a.owner ? `<a href="#anggota" class="akun-tautan" id="t-anggota">${t('Anggota')}</a>` : ''}
    ${a.owner ? `<div class="lonceng" id="lonceng">
        <button type="button" class="lonceng-tbl" id="lonceng-tbl" aria-haspopup="true" aria-expanded="false" aria-controls="lonceng-panel" aria-label="${t('Notifikasi anggota')}">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
          <span class="lencana lonceng-lencana" id="lencana-menunggu" hidden></span>
        </button>
        <div class="lonceng-panel" id="lonceng-panel" role="region" aria-label="${t('Notifikasi')}" hidden></div>
      </div>` : ''}
    <span class="akun-nama" title="${esc(a.email)}">${esc(a.nama || a.email.split('@')[0])}</span>
    <button type="button" class="akun-keluar" id="b-keluar">${t('Keluar')}</button>`;
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
  segarLencana();
  if (a.owner) pasangLonceng();
}

/* Lonceng notifikasi (khusus pemilik): lencana merah berisi jumlah anggota yang menunggu persetujuan.
   Angkanya mengikuti peladen: dimuat saat masuk, disegarkan tiap 30 detik selagi tab terlihat dan setiap kali
   tab kembali dibuka, serta langsung diperbarui oleh halaman Anggota. Klik lonceng menampilkan daftarnya. */
FIMS.setMenunggu = function (n) {
  const lama = (FIMS.aku && Number(FIMS.aku.menunggu)) || 0;
  n = Number(n) || 0;
  if (FIMS.aku) FIMS.aku.menunggu = n;
  segarLencana(n > lama);
};

function labelLonceng(n) {
  return n < 1 ? t('Notifikasi anggota')
    : (n === 1 ? t('1 anggota menunggu persetujuan') : tf('%s anggota menunggu persetujuan', n));
}

function segarLencana(baru) {
  const b = document.getElementById('lencana-menunggu');
  if (!b) return;
  const n = (FIMS.aku && Number(FIMS.aku.menunggu)) || 0;
  b.textContent = n < 1 ? '' : (n > 99 ? '99+' : String(n));
  b.hidden = n < 1;
  const tbl = document.getElementById('lonceng-tbl');
  if (tbl) { tbl.setAttribute('aria-label', labelLonceng(n)); tbl.title = labelLonceng(n); }
  if (baru && n > 0) {                                   // ada permintaan baru: denyut singkat
    b.classList.remove('baru'); void b.offsetWidth; b.classList.add('baru');
  }
  if (document.getElementById('lonceng-panel') && !document.getElementById('lonceng-panel').hidden) isiLonceng();
}

let _daftarLonceng = null, _galatLonceng = false, _memuatLonceng = false;

function isiLonceng() {
  const w = document.getElementById('lonceng-panel'); if (!w) return;
  const n = (FIMS.aku && Number(FIMS.aku.menunggu)) || 0;
  const tgl = x => x ? new Date(x * 1000).toLocaleDateString(BHS === 'en' ? 'en-GB' : 'id-ID', { day: 'numeric', month: 'short' }) : '';
  let isi;
  if (_galatLonceng) isi = `<p class="lonceng-kosong">${t('Tidak dapat memuat notifikasi.')}</p>`;
  else if (n < 1 && _daftarLonceng && !_daftarLonceng.length) isi = `<p class="lonceng-kosong">${t('Tidak ada anggota yang menunggu persetujuan.')}</p>`;
  else if (!_daftarLonceng) isi = `<p class="lonceng-kosong">${t('Memuat…')}</p>`;
  else {
    const tampil = _daftarLonceng.slice(0, 6), sisa = _daftarLonceng.length - tampil.length;
    isi = `<ul class="lonceng-daftar">${tampil.map(m => {
      const nm = m.nama || String(m.email).split('@')[0];
      return `<li><a href="#anggota" class="lonceng-baris" data-tutup>
        <span class="lonceng-avatar" aria-hidden="true">${esc(nm.trim().charAt(0).toUpperCase() || '?')}</span>
        <span class="lonceng-teks"><b>${esc(nm)}</b><small>${esc(m.email)}</small></span>
        <span class="lonceng-sisi"><span class="lonceng-peran">${t(m.peran === 'guru' ? 'Guru' : 'Siswa')}</span><small>${esc(tgl(m.dibuat))}</small></span></a></li>`; }).join('')}</ul>` +
      (sisa > 0 ? `<p class="lonceng-sisa">${tf('dan %s lainnya', sisa)}</p>` : '');
  }
  w.innerHTML = `<div class="lonceng-kepala"><b>${t('Notifikasi')}</b>${n > 0 ? `<span class="lonceng-jml">${esc(labelLonceng(n))}</span>` : ''}</div>${isi}
    <a href="#anggota" class="lonceng-semua" data-tutup>${t('Tinjau di halaman Anggota')} →</a>`;
}

function aturLonceng() {                                 // letakkan panel di bawah lonceng, tetap di dalam layar
  const w = document.getElementById('lonceng'), p = document.getElementById('lonceng-panel');
  if (!w || !p) return;
  const vw = document.documentElement.clientWidth, lebar = Math.min(360, vw - 32);
  const r = w.getBoundingClientRect();
  const kiri = Math.max(16, Math.min(r.right - lebar, vw - lebar - 16));
  p.style.width = lebar + 'px';
  p.style.left = (kiri - r.left) + 'px';
}

function tutupLonceng(balik) {
  const p = document.getElementById('lonceng-panel'), b = document.getElementById('lonceng-tbl');
  if (!p || p.hidden) return;
  p.hidden = true; if (b) { b.setAttribute('aria-expanded', 'false'); if (balik) b.focus(); }
}

async function muatDaftarLonceng() {
  if (_memuatLonceng) return;
  _memuatLonceng = true;
  const r = await API('anggota').catch(() => ({}));
  _memuatLonceng = false;
  if (Array.isArray(r.anggota)) {
    _galatLonceng = false;
    _daftarLonceng = r.anggota.filter(m => m.status === 'menunggu').sort((x, y) => (y.dibuat || 0) - (x.dibuat || 0));
    FIMS.setMenunggu(_daftarLonceng.length);             // daftar adalah kebenaran terbaru: angka ikut menyesuaikan
  } else { _galatLonceng = true; _daftarLonceng = null; }
  const p = document.getElementById('lonceng-panel');
  if (p && !p.hidden) isiLonceng();
}

function bukaLonceng() {
  const p = document.getElementById('lonceng-panel'), b = document.getElementById('lonceng-tbl');
  if (!p || !b) return;
  p.hidden = false; b.setAttribute('aria-expanded', 'true');
  aturLonceng(); isiLonceng();
  muatDaftarLonceng();
}

async function cekMenunggu() {
  if (!FIMS.aku || !FIMS.aku.owner || document.hidden) return;
  const r = await API('saya').catch(() => null);
  if (!(r && r.ok && r.masuk && r.menunggu !== undefined)) return;
  const lama = Number(FIMS.aku.menunggu) || 0;
  FIMS.setMenunggu(r.menunggu);
  const p = document.getElementById('lonceng-panel');
  if (p && !p.hidden && Number(r.menunggu) !== lama) muatDaftarLonceng();   // panel terbuka: daftarnya ikut disegarkan
}

let _loncengSiap = false;
function pasangLonceng() {
  const b = document.getElementById('lonceng-tbl'); if (!b) return;
  _daftarLonceng = null; _galatLonceng = false;
  b.addEventListener('click', ev => {
    ev.stopPropagation();
    const p = document.getElementById('lonceng-panel');
    if (p.hidden) bukaLonceng(); else tutupLonceng(false);
  });
  document.getElementById('lonceng-panel').addEventListener('click', ev => {
    const x = ev.target.closest('[data-tutup]'); if (!x) return;
    tutupLonceng(false);
    if (location.hash === '#anggota') { ev.preventDefault(); FIMS.halAnggota(); }   // sudah di sana: segarkan saja
  });
  if (_loncengSiap) return;                              // pendengar global dipasang sekali saja
  _loncengSiap = true;
  document.addEventListener('click', ev => { if (!ev.target.closest('#lonceng')) tutupLonceng(false); });
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape') tutupLonceng(true); });
  window.addEventListener('resize', () => { const p = document.getElementById('lonceng-panel'); if (p && !p.hidden) aturLonceng(); });
  window.addEventListener('hashchange', () => tutupLonceng(false));
  window.addEventListener('focus', cekMenunggu);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) cekMenunggu(); });
  setInterval(cekMenunggu, 30000);
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
  FIMS.aku = { email: r.email, nama: r.nama, peran: r.peran, guru: !!r.guru, owner: !!r.owner, menunggu: Number(r.menunggu) || 0 };
  if (FIMS.aku.guru && !localStorage.getItem(KUNCI_MODE)) FIMS.setMode('guru');
  await tarikProgres();
  pasangBilah();
  if (!window.__appDimuat) { window.__appDimuat = true; muatApp(); }
  else document.dispatchEvent(new CustomEvent('fims:segar'));
}

document.addEventListener('DOMContentLoaded', mulai);
})();
