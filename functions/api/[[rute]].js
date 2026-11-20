/* API akun Fisika FIWA — berjalan di Cloudflare Pages Functions.
   Satu berkas, satu perute kecil. Semua jalur di bawah /api/.

   Pengikatan yang dibutuhkan di proyek Pages:
     DB         — basis data D1 (wajib)
     RAHASIA    — teks acak panjang untuk menandatangani sesi (wajib)
     EMAIL_OWNER— alamat surel pemilik situs (opsional; bila diisi, pemilik langsung aktif
                  tanpa menunggu persetujuan siapa pun. Isi sebagai peubah terenkripsi,
                  jangan pernah dituliskan ke dalam repositori yang bersifat publik)
     WAJIB_KODE — "1" bila anggota harus memasukkan kode aktivasi (opsional; bawaan mati)  */

const NAMA_KUKI = 'fims_sesi';
const UMUR_SESI = 60 * 60 * 24 * 30;              // 30 hari

/* ---------- alat kecil ---------- */
const json = (data, status = 200, kepala = {}) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...kepala }
  });

const rapi = e => String(e || '').trim().toLowerCase();
const sahEmail = e => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e);
const kini = () => Math.floor(Date.now() / 1000);

const b64url = buf => btoa(String.fromCharCode(...new Uint8Array(buf)))
  .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

async function tandaTangan(isi, rahasia) {
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(rahasia),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64url(await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(isi)));
}

/* Sesi disimpan di dalam kuki bertanda tangan, bukan di basis data:
   penjaga berkas pada _middleware.js jadi tidak perlu menyentuh D1 sama sekali. */
export async function buatSesi(email, peran, rahasia) {
  const isi = `${email}|${peran}|${kini() + UMUR_SESI}`;
  return `${b64url(new TextEncoder().encode(isi))}.${await tandaTangan(isi, rahasia)}`;
}

export async function bacaSesi(kuki, rahasia) {
  if (!kuki || !rahasia) return null;
  const [b, sig] = String(kuki).split('.');
  if (!b || !sig) return null;
  let isi;
  try { isi = new TextDecoder().decode(Uint8Array.from(atob(b.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0))); }
  catch { return null; }
  if (await tandaTangan(isi, rahasia) !== sig) return null;
  const [email, peran, exp] = isi.split('|');
  if (!email || !(+exp > kini())) return null;
  return { email, peran };
}

export function ambilKuki(req, nama) {
  const c = req.headers.get('cookie') || '';
  const m = c.match(new RegExp('(?:^|;\\s*)' + nama + '=([^;]*)'));
  return m ? decodeURIComponent(m[1]) : null;
}

const pasangKuki = nilai =>
  `${NAMA_KUKI}=${encodeURIComponent(nilai)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${UMUR_SESI}`;
const hapusKuki = () =>
  `${NAMA_KUKI}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`;

/* ---------- kata sandi ----------
   Disimpan sebagai turunan PBKDF2-SHA256 100.000 putaran dengan garam acak 16 bita.
   Kata sandi aslinya tidak pernah disimpan dan tidak dapat dibaca kembali dari basis data. */
const SANDI_PUTARAN = 100000;
const dariB64 = t => Uint8Array.from(atob(String(t).replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));

async function olahSandi(sandi, garamB64) {
  const garam = garamB64 ? dariB64(garamB64) : crypto.getRandomValues(new Uint8Array(16));
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(sandi), 'PBKDF2', false, ['deriveBits']);
  const bit = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', salt: garam, iterations: SANDI_PUTARAN, hash: 'SHA-256' }, k, 256);
  return { sandi: b64url(bit), garam: b64url(garam) };
}

/* Pembandingan berwaktu tetap, supaya lama jawaban tidak membocorkan isi sandi. */
function samaTetap(a, b) {
  a = String(a || ''); b = String(b || '');
  if (a.length !== b.length) return false;
  let beda = 0;
  for (let i = 0; i < a.length; i++) beda |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return beda === 0;
}

const sandiLayak = x => typeof x === 'string' && x.length >= 8 && x.length <= 200;

const kodeBaru = () => {
  const huruf = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';        // tanpa I, O, 0, 1
  return [...crypto.getRandomValues(new Uint8Array(6))].map(n => huruf[n % huruf.length]).join('');
};

/* ---------- lembar: isian dokumen per murid ----------
   Setiap dokumen yang bisa diisi murid (lembar kerja, soal, simulasi PRI UIN, dst.) menyimpan isian dan skornya
   di sini, satu baris per (murid, dokumen). "kunci" = alamat berkas tanpa awalan "/" dan tanpa ".html".
   Tabel dibuat sendiri pada pemakaian pertama, jadi tidak ada migrasi wajib. */
const KUNCI_SAH = /^[A-Za-z0-9][A-Za-z0-9._\-\/]{0,198}$/;
const kunciSah = k => typeof k === 'string' && KUNCI_SAH.test(k) && !k.includes('..') && !k.includes('//');
const lembarSiap = new WeakSet();
async function pastikanLembar(DB) {
  if (lembarSiap.has(DB)) return;
  await DB.prepare(
    'CREATE TABLE IF NOT EXISTS lembar (' +
    ' email TEXT NOT NULL, kunci TEXT NOT NULL, data TEXT NOT NULL,' +
    ' skor REAL, selesai INTEGER NOT NULL DEFAULT 0, terisi INTEGER, total INTEGER,' +
    ' epoch INTEGER NOT NULL DEFAULT 0, diubah INTEGER NOT NULL, oleh TEXT,' +
    ' PRIMARY KEY (email, kunci))').run();
  await DB.prepare('CREATE INDEX IF NOT EXISTS lembar_kunci ON lembar (kunci)').run();
  lembarSiap.add(DB);
}
const angkaAtauNull = (x, mak, bulat) => {
  if (x === null || x === undefined || x === '') return null;
  x = Number(x);
  if (!isFinite(x)) return null;
  x = Math.max(0, Math.min(mak, x));
  return bulat ? Math.round(x) : Math.round(x * 10) / 10;
};
const BATAS_LEMBAR = 60000;        // karakter JSON per dokumen
const BATAS_DOKUMEN = 400;         // dokumen tersimpan per murid

/* Menghapus hasil SATU tahapan dari data progres TP (diubah di tempat). Mengembalikan {dulu} atau {galat}. */
function bukaTahapan(d, id) {
  d.ev = d.ev || {};
  if (id === 'S14') {
    const arr = Array.isArray(d.s14) ? d.s14 : [];
    if (!arr.length) return { galat: 'S14 belum punya hasil tercatat.' };
    const copot = arr.pop(); d.s14 = arr;
    const dulu = { hasil: copot.hasil || null, waktu: copot.waktu || null };
    if (copot.hasil === 'gagal') {                 // gagal tadi sempat memajukan jadwal dari nol; kembalikan
      const g = [...arr].reverse().find(x => x.hasil === 'gagal');
      if (g) d.s14Mulai = (g.waktu || 0) + 1; else delete d.s14Mulai;
    }
    return { dulu };
  }
  const ev = d.ev[id];
  const adaTier = id === 'S12' && d.tier;
  if (!ev && !adaTier) return { galat: 'Tahapan ini belum punya hasil tercatat.' };
  const dulu = { skor: ev && ev.skor != null ? ev.skor : null, waktu: ev && ev.waktu ? ev.waktu : null };
  if (id === 'S12') { dulu.tier = d.tier || null; d.tier = null; }
  if(id==='S8'&&d.p5Usulan)d.p5Usulan.menunggu=false;
  delete d.ev[id];
  return { dulu };
}

/* ---------- perute ---------- */
export async function onRequest(ctx) {
  const { request, env, params } = ctx;
  const rute = (Array.isArray(params.rute) ? params.rute.join('/') : params.rute || '');
  const metode = request.method.toUpperCase();

  if (!env.DB) return json({ siap: false, galat: 'D1 belum terikat. Ikat basis data dengan nama DB pada pengaturan proyek Pages.' }, 503);
  if (!env.RAHASIA) return json({ siap: false, galat: 'Peubah RAHASIA belum diisi pada pengaturan proyek Pages.' }, 503);

  const DB = env.DB;
  const owner = rapi(env.EMAIL_OWNER || '');   // kosong = tidak ada yang diangkat otomatis
  const wajibKode = String(env.WAJIB_KODE || '') === '1';

  const sesi = await bacaSesi(ambilKuki(request, NAMA_KUKI), env.RAHASIA);
  const aku = sesi ? await DB.prepare('SELECT * FROM anggota WHERE email = ?').bind(sesi.email).first() : null;
  const aktif = aku && aku.status === 'aktif' ? aku : null;
  const isOwner = !!aktif && (aktif.peran === 'owner' || (!!owner && aktif.email === owner));
  const isGuru = !!aktif && (isOwner || aktif.peran === 'guru');

  const badan = async () => { try { return await request.json(); } catch { return {}; } };

  try {
    /* ---- siapa saya ---- */
    if (rute === 'saya' && metode === 'GET') {
      if (!aku) return json({ siap: true, masuk: false, wajibKode });
      if (aku.status !== 'aktif')
        return json({ siap: true, masuk: false, status: aku.status, email: aku.email, peran: aku.peran, wajibKode },
          200, { 'set-cookie': aku.status === 'ditolak' ? hapusKuki() : '' });
      let menunggu = 0;
      if (isOwner) {
        try {
          const c = await DB.prepare("SELECT COUNT(*) AS n FROM anggota WHERE status = 'menunggu'").first();
          menunggu = (c && c.n) || 0;
        } catch {}
      }
      return json({
        siap: true, masuk: true, email: aku.email, nama: aku.nama, peran: aku.peran,
        kelas: aku.kelas, owner: isOwner, guru: isGuru, wajibKode, menunggu
      });
    }

    /* ---- registrasi: nama, surel, kata sandi, pilihan peran ---- */
    if (rute === 'daftar' && metode === 'POST') {
      const b = await badan();
      const email = rapi(b.email);
      const nama = String(b.nama || '').trim().slice(0, 80);
      const peranMinta = b.peran === 'guru' ? 'guru' : 'siswa';
      if (nama.length < 2)      return json({ galat: 'Nama lengkap belum diisi.' }, 400);
      if (!sahEmail(email))     return json({ galat: 'Alamat surel tidak sah.' }, 400);
      if (!sandiLayak(b.sandi)) return json({ galat: 'Kata sandi minimal 8 karakter.' }, 400);

      const ada = await DB.prepare('SELECT email, sandi FROM anggota WHERE email = ?').bind(email).first();
      if (ada && ada.sandi) return json({ galat: 'Alamat surel ini sudah terdaftar. Silakan masuk.' }, 409);

      const h = await olahSandi(b.sandi, null);
      const jadiOwner = !!owner && email === owner;
      if (ada) {
        // Baris lama dari masa sebelum ada kata sandi: lengkapi, jangan hilangkan progresnya.
        await DB.prepare('UPDATE anggota SET nama = ?, sandi = ?, garam = ?, terakhir = ? WHERE email = ?')
          .bind(nama, h.sandi, h.garam, kini(), email).run();
      } else {
        await DB.prepare(
          'INSERT INTO anggota (email, nama, peran, status, sandi, garam, kode, dibuat, terakhir) VALUES (?,?,?,?,?,?,?,?,?)'
        ).bind(email, nama, jadiOwner ? 'owner' : peranMinta, jadiOwner ? 'aktif' : 'menunggu',
               h.sandi, h.garam, wajibKode && !jadiOwner ? kodeBaru() : null, kini(), kini()).run();
      }
      const a = await DB.prepare('SELECT * FROM anggota WHERE email = ?').bind(email).first();
      if (a.status === 'aktif' && !(wajibKode && a.kode)) {
        const kuki = await buatSesi(email, a.peran, env.RAHASIA);
        return json({ status: 'masuk', email, peran: a.peran }, 200, { 'set-cookie': pasangKuki(kuki) });
      }
      return json({ status: a.status === 'ditolak' ? 'ditolak' : 'menunggu', email });
    }

    /* ---- masuk dengan surel dan kata sandi ----
       Peran tidak diminta di sini: ia diambil dari akun yang sudah disetujui pemilik. */
    if (rute === 'masuk' && metode === 'POST') {
      const b = await badan();
      const email = rapi(b.email);
      if (!sahEmail(email)) return json({ galat: 'Alamat surel tidak sah.' }, 400);
      if (!b.sandi)         return json({ galat: 'Kata sandi belum diisi.' }, 400);

      const a = await DB.prepare('SELECT * FROM anggota WHERE email = ?').bind(email).first();
      // Jawaban yang sama untuk surel tak dikenal dan sandi salah, supaya daftar
      // anggota tidak bisa ditebak satu per satu dari luar.
      const tolak = () => json({ galat: 'Alamat surel atau kata sandi tidak cocok.' }, 403);
      if (!a) return tolak();

      if (!a.sandi) {
        // Akun lama dari masa sebelum ada kata sandi (termasuk baris pemilik yang
        // dibuat lewat Console D1): kata sandi pertama yang dipakai menjadi miliknya.
        if (!sandiLayak(b.sandi)) return json({ galat: 'Akun ini belum punya kata sandi. Tetapkan satu, minimal 8 karakter.' }, 400);
        const h = await olahSandi(b.sandi, null);
        await DB.prepare('UPDATE anggota SET sandi = ?, garam = ? WHERE email = ?').bind(h.sandi, h.garam, email).run();
      } else {
        const h = await olahSandi(b.sandi, a.garam);
        if (!samaTetap(h.sandi, a.sandi)) return tolak();
      }

      await DB.prepare('UPDATE anggota SET terakhir = ? WHERE email = ?').bind(kini(), email).run();

      if (a.status === 'ditolak') return json({ status: 'ditolak' }, 403);
      if (a.status !== 'aktif')   return json({ status: 'menunggu', email });
      if (wajibKode && a.kode)    return json({ status: 'perlu_kode', email });

      const kuki = await buatSesi(email, a.peran, env.RAHASIA);
      return json({ status: 'masuk', email, peran: a.peran }, 200, { 'set-cookie': pasangKuki(kuki) });
    }

    /* ---- aktivasi dengan kode (hanya bila WAJIB_KODE menyala) ---- */
    if (rute === 'aktivasi' && metode === 'POST') {
      const b = await badan();
      const email = rapi(b.email), kode = String(b.kode || '').trim().toUpperCase();
      const a = await DB.prepare('SELECT * FROM anggota WHERE email = ?').bind(email).first();
      if (!a || a.status !== 'aktif') return json({ galat: 'Akun belum disetujui.' }, 403);
      if (!a.kode || a.kode !== kode) return json({ galat: 'Kode tidak cocok.' }, 403);
      await DB.prepare('UPDATE anggota SET kode = NULL WHERE email = ?').bind(email).run();
      const kuki = await buatSesi(email, a.peran, env.RAHASIA);
      return json({ status: 'masuk', email, peran: a.peran }, 200, { 'set-cookie': pasangKuki(kuki) });
    }

    /* ---- keluar ---- */
    if (rute === 'keluar' && metode === 'POST')
      return json({ ok: true }, 200, { 'set-cookie': hapusKuki() });

    /* ---- daftar anggota: hanya pemilik situs ----
       Guru pun tidak melihatnya, supaya alamat surel pemilik tidak tersebar. */
    if (rute === 'anggota' && metode === 'GET') {
      if (!isOwner) return json({ galat: 'Khusus pemilik situs.' }, 403);
      const r = await DB.prepare(
        'SELECT email, nama, peran, status, kelas, kode, dibuat, diputus, terakhir FROM anggota ORDER BY ' +
        "CASE status WHEN 'menunggu' THEN 0 WHEN 'aktif' THEN 1 ELSE 2 END, dibuat DESC"
      ).all();
      return json({ anggota: r.results || [], owner: isOwner });
    }

    if (rute === 'anggota/putusan' && metode === 'POST') {
      if (!isOwner) return json({ galat: 'Hanya pemilik situs yang boleh memutuskan.' }, 403);
      const b = await badan();
      const email = rapi(b.email);
      const status = ['aktif', 'ditolak', 'menunggu'].includes(b.status) ? b.status : null;
      const peran = ['siswa', 'guru'].includes(b.peran) ? b.peran : null;
      // Nama boleh diubah pemilik, termasuk pada akun pemilik sendiri.
      const nama = b.nama === undefined ? null : rapi(String(b.nama)).slice(0, 80);
      if (nama !== null && !nama) return json({ galat: 'Nama tidak boleh kosong.' }, 400);
      if (!email || (!status && !peran && nama === null)) return json({ galat: 'Permintaan tidak lengkap.' }, 400);
      const a = await DB.prepare('SELECT * FROM anggota WHERE email = ?').bind(email).first();
      if (!a) return json({ galat: 'Anggota tidak ditemukan.' }, 404);
      if ((a.peran === 'owner' || (!!owner && email === owner)) && ((status && status !== 'aktif') || peran))
        return json({ galat: 'Akun pemilik tidak dapat dinonaktifkan atau diturunkan perannya.' }, 400);

      let kode = a.kode;
      if (status === 'aktif' && wajibKode && !kode) kode = kodeBaru();
      await DB.prepare('UPDATE anggota SET status = ?, peran = ?, nama = ?, kode = ?, diputus = ?, oleh = ? WHERE email = ?')
        .bind(status || a.status, peran || a.peran, nama === null ? a.nama : nama, kode, kini(), aktif.email, email).run();

      // Peran berubah atau akun dinonaktifkan: buang baris pembimbingan yang
      // sudah tidak bermakna, supaya papan guru tidak menampilkan sisa lama.
      try {
        const peranBaru = peran || a.peran, statusBaru = status || a.status;
        if (peranBaru !== 'siswa' || statusBaru !== 'aktif')
          await DB.prepare('DELETE FROM bimbing WHERE murid = ?').bind(email).run();
        if (!['guru', 'owner'].includes(peranBaru) || statusBaru !== 'aktif')
          await DB.prepare('DELETE FROM bimbing WHERE guru = ?').bind(email).run();
      } catch {}
      let menunggu = 0;
      try {
        const c = await DB.prepare("SELECT COUNT(*) AS n FROM anggota WHERE status = 'menunggu'").first();
        menunggu = (c && c.n) || 0;
      } catch {}
      return json({ ok: true, email, status: status || a.status, peran: peran || a.peran,
                    nama: nama === null ? a.nama : nama, kode, menunggu });
    }

    /* ---- pemilik menyetel ulang kata sandi anggota ----
       Dipakai bila ada yang lupa sandinya. Sandi lama tidak pernah bisa dibaca,
       hanya diganti; sesi yang sedang berjalan milik orang itu tetap sah sampai
       kedaluwarsa, karena tanda tangannya tidak bergantung pada kata sandi. */
    if (rute === 'anggota/sandi' && metode === 'POST') {
      if (!isOwner) return json({ galat: 'Hanya pemilik situs.' }, 403);
      const b = await badan();
      const email = rapi(b.email);
      if (!sahEmail(email))     return json({ galat: 'Alamat surel tidak sah.' }, 400);
      if (!sandiLayak(b.sandi)) return json({ galat: 'Kata sandi minimal 8 karakter.' }, 400);

      const a = await DB.prepare('SELECT email FROM anggota WHERE email = ?').bind(email).first();
      if (!a) return json({ galat: 'Anggota tidak ditemukan.' }, 404);

      const h = await olahSandi(b.sandi, null);
      await DB.prepare('UPDATE anggota SET sandi = ?, garam = ?, diputus = ?, oleh = ? WHERE email = ?')
        .bind(h.sandi, h.garam, kini(), aktif.email, email).run();
      return json({ ok: true, email });
    }

    if (rute === 'anggota/hapus' && metode === 'POST') {
      if (!isOwner) return json({ galat: 'Hanya pemilik situs.' }, 403);
      const email = rapi((await badan()).email);
      if (!email) return json({ galat: 'Alamat tidak diberikan.' }, 400);
      if (email === aktif.email) return json({ galat: 'Akun Anda sendiri tidak dapat dihapus dari sini.' }, 400);
      const sasaran = await DB.prepare('SELECT peran FROM anggota WHERE email = ?').bind(email).first();
      if (!sasaran) return json({ galat: 'Anggota tidak ditemukan.' }, 404);
      if (sasaran.peran === 'owner' || (!!owner && email === owner))
        return json({ galat: 'Akun pemilik tidak dapat dihapus.' }, 400);
      await pastikanLembar(DB);
      await DB.batch([
        DB.prepare('DELETE FROM progres WHERE email = ?').bind(email),
        DB.prepare('DELETE FROM lembar WHERE email = ?').bind(email),
        DB.prepare('DELETE FROM anggota WHERE email = ?').bind(email)
      ]);
      return json({ ok: true, email });
    }

    /* ---- progres: mengikuti akun, bukan peramban ---- */
    if (rute === 'progres' && metode === 'GET') {
      if (!aktif) return json({ galat: 'Belum masuk.' }, 401);
      const r = await DB.prepare('SELECT tp, data, diubah FROM progres WHERE email = ?').bind(aktif.email).all();
      const tp = {}, epoch = {};
      for (const row of r.results || []) {
        try { tp[row.tp] = JSON.parse(row.data); epoch[row.tp] = Number(tp[row.tp].epoch) || 0; } catch {}
      }
      // ?epoch=1: hanya nomor generasi tiap TP — murah, dipakai peramban murid untuk mengecek
      // apakah guru mengubah sesuatu sejak terakhir ia menyinkron.
      if (new URL(request.url).searchParams.get('epoch') === '1') return json({ epoch });
      return json({ tp });
    }

    /* PUT dari pemakaian biasa; POST dipakai navigator.sendBeacon saat tab ditutup,
       karena sendBeacon hanya bisa mengirim POST. */
    if (rute === 'progres' && (metode === 'PUT' || metode === 'POST')) {
      if (!aktif) return json({ galat: 'Belum masuk.' }, 401);
      const b = await badan();
      const tp = b.tp || {};
      /* Pengaman terhadap data usang. Setiap kali guru mengubah progres muridnya (menilai, atau
         mereset satu dokumen) nomor "epoch" TP itu naik. Peramban murid yang masih memegang salinan
         lama membawa epoch lama; kirimannya ditolak dan ia diberi salinan terbaru. Tanpa ini, tab murid
         yang kebetulan masih terbuka akan menimpa reset guru dengan data sebelum reset. "epoch" dan
         "reset" milik peladen: nilai dari peramban tidak dipercaya. */
      const ada = {};
      const sudah = await DB.prepare('SELECT tp, data FROM progres WHERE email = ?').bind(aktif.email).all();
      for (const row of sudah.results || []) { try { ada[row.tp] = JSON.parse(row.data); } catch {} }
      const usang = {};
      const perintah = [];
      for (const [slugMentah, data] of Object.entries(tp).slice(0, 200)) {
        const slug = String(slugMentah).slice(0, 80);
        const lama = ada[slug] || null;
        const e0 = lama ? Number(lama.epoch) || 0 : 0;
        const e1 = data && typeof data === 'object' ? Number(data.epoch) || 0 : 0;
        if (lama && e1 < e0) { usang[slug] = lama; continue; }
        const baru = (data && typeof data === 'object') ? { ...data } : {};
        if (e0) baru.epoch = e0; else delete baru.epoch;
        if (lama && lama.reset) baru.reset = lama.reset; else delete baru.reset;
        perintah.push(
          DB.prepare('INSERT INTO progres (email, tp, data, diubah) VALUES (?,?,?,?) ' +
                     'ON CONFLICT(email, tp) DO UPDATE SET data = excluded.data, diubah = excluded.diubah')
            .bind(aktif.email, slug, JSON.stringify(baru).slice(0, 20000), kini()));
      }
      if (perintah.length) await DB.batch(perintah);
      return json({ ok: true, jumlah: perintah.length, usang });
    }

    /* ---- lembar: isian & skor satu dokumen, per akun murid ---- */
    if (rute === 'lembar' && metode === 'GET') {
      if (!aktif) return json({ galat: 'Belum masuk.' }, 401);
      const kunci = new URL(request.url).searchParams.get('kunci') || '';
      if (!kunciSah(kunci)) return json({ galat: 'Kunci dokumen tidak sah.' }, 400);
      // Guru dan pemilik hanya melihat-lihat dokumen: tidak ada yang disimpan atas nama mereka.
      if (isGuru) return json({ simpan: false, peran: aktif.peran, ada: false, epoch: 0 });
      await pastikanLembar(DB);
      const r = await DB.prepare(
        'SELECT data, skor, selesai, terisi, total, epoch, diubah FROM lembar WHERE email = ? AND kunci = ?'
      ).bind(aktif.email, kunci).first();
      if (!r) return json({ simpan: true, ada: false, epoch: 0 });
      if (new URL(request.url).searchParams.get('epoch') === '1') return json({ simpan: true, ada: true, epoch: r.epoch || 0 });
      let data = {}; try { data = JSON.parse(r.data) || {}; } catch {}
      return json({ simpan: true, ada: true, epoch: r.epoch || 0, data, skor: r.skor, selesai: r.selesai ? 1 : 0,
                    terisi: r.terisi, total: r.total, diubah: r.diubah });
    }

    /* PUT biasa; POST dari navigator.sendBeacon saat tab ditutup. */
    if (rute === 'lembar' && (metode === 'PUT' || metode === 'POST')) {
      if (!aktif) return json({ galat: 'Belum masuk.' }, 401);
      const b = await badan();
      if (isGuru) return json({ ok: true, simpan: false });
      if (!kunciSah(b.kunci)) return json({ galat: 'Kunci dokumen tidak sah.' }, 400);
      if (!b.data || typeof b.data !== 'object' || Array.isArray(b.data))
        return json({ galat: 'Isi dokumen tidak sah.' }, 400);
      await pastikanLembar(DB);
      const lama = await DB.prepare('SELECT data, epoch FROM lembar WHERE email = ? AND kunci = ?')
        .bind(aktif.email, b.kunci).first();
      const e0 = lama ? Number(lama.epoch) || 0 : 0;
      // Pengaman data usang, sama seperti pada progres: bila guru membuka ulang dokumen ini, nomor epoch naik,
      // dan tab murid yang masih memegang isian lama ditolak (ia diminta memuat ulang).
      if (lama && (Number(b.epoch) || 0) < e0) return json({ usang: true, epoch: e0 });
      if (!lama) {
        const n = await DB.prepare('SELECT COUNT(*) AS n FROM lembar WHERE email = ?').bind(aktif.email).first();
        if (n && n.n >= BATAS_DOKUMEN) return json({ galat: 'Terlalu banyak dokumen tersimpan.' }, 429);
      }
      const baru = { ...b.data };
      delete baru.reset;                                           // milik peladen
      if (lama) { try { const dl = JSON.parse(lama.data); if (dl && dl.reset) baru.reset = dl.reset; } catch {} }
      const teks = JSON.stringify(baru);
      if (teks.length > BATAS_LEMBAR) return json({ galat: 'Isian terlalu besar untuk disimpan.' }, 413);
      const t = kini();
      await DB.prepare(
        'INSERT INTO lembar (email, kunci, data, skor, selesai, terisi, total, epoch, diubah, oleh) VALUES (?,?,?,?,?,?,?,?,?,?) ' +
        'ON CONFLICT(email, kunci) DO UPDATE SET data = excluded.data, skor = excluded.skor, selesai = excluded.selesai, ' +
        'terisi = excluded.terisi, total = excluded.total, diubah = excluded.diubah'
      ).bind(aktif.email, b.kunci, teks, angkaAtauNull(b.skor, 1000, false), b.selesai ? 1 : 0,
             angkaAtauNull(b.terisi, 100000, true), angkaAtauNull(b.total, 100000, true), e0, t, aktif.nama || null).run();
      return json({ ok: true, epoch: e0, diubah: t });
    }

    /* ---- guru: ringkasan dokumen isian satu murid ---- */
    if (rute === 'guru/lembar' && metode === 'GET') {
      if (!isGuru) return json({ galat: 'Khusus guru.' }, 403);
      const murid = rapi(new URL(request.url).searchParams.get('murid'));
      if (!murid) return json({ galat: 'Murid tidak disebut.' }, 400);
      if (!isOwner) {
        const ikat = await DB.prepare('SELECT 1 AS a FROM bimbing WHERE guru = ? AND murid = ?')
          .bind(aktif.email, murid).first();
        if (!ikat) return json({ galat: 'Murid ini bukan bimbingan Anda.' }, 403);
      }
      await pastikanLembar(DB);
      const r = await DB.prepare(
        'SELECT kunci, data, skor, selesai, terisi, total, epoch, diubah FROM lembar WHERE email = ? ORDER BY diubah DESC LIMIT 500'
      ).bind(murid).all();
      const lembar = (r.results || []).map(x => {
        let d = {}; try { d = JSON.parse(x.data) || {}; } catch {}
        const adaIsi = !!((d.f && Object.keys(d.f).length) || d.x != null || x.selesai || x.skor != null);
        return { kunci: x.kunci, skor: x.skor, selesai: x.selesai ? 1 : 0, terisi: x.terisi, total: x.total,
                 epoch: x.epoch || 0, diubah: x.diubah, adaIsi, reset: d.reset || null };
      });
      return json({ lembar });
    }

    /* ---- papan kelas: seluruh siswa, hanya untuk guru ---- */
    if (rute === 'papan' && metode === 'GET') {
      if (!isGuru) return json({ galat: 'Khusus guru.' }, 403);
      const semua = isOwner && new URL(request.url).searchParams.get('semua') !== '0';
      const r = semua
        ? await DB.prepare(
            "SELECT a.email, a.nama, a.kelas, p.tp, p.data FROM anggota a " +
            "LEFT JOIN progres p ON p.email = a.email " +
            "WHERE a.status = 'aktif' AND a.peran = 'siswa' ORDER BY a.nama, a.email").all()
        : await DB.prepare(
            "SELECT a.email, a.nama, a.kelas, p.tp, p.data FROM anggota a " +
            "JOIN bimbing b ON b.murid = a.email AND b.guru = ? " +
            "LEFT JOIN progres p ON p.email = a.email " +
            "WHERE a.status = 'aktif' AND a.peran = 'siswa' ORDER BY a.nama, a.email").bind(aktif.email).all();
      const murid = {};
      for (const row of r.results || []) {
        const m = murid[row.email] || (murid[row.email] = { email: row.email, nama: row.nama, kelas: row.kelas, tp: {} });
        if (row.tp) { try { m.tp[row.tp] = JSON.parse(row.data); } catch {} }
      }
      return json({ murid: Object.values(murid) });
    }

    /* ---------- pembimbingan: murid ↔ guru, banyak ke banyak ---------- */

    // Daftar pasangan. Pemilik melihat semuanya; guru hanya muridnya sendiri.
    if (rute === 'bimbing' && metode === 'GET') {
      if (!isGuru) return json({ galat: 'Khusus guru.' }, 403);
      const r = isOwner
        ? await DB.prepare('SELECT guru, murid FROM bimbing').all()
        : await DB.prepare('SELECT guru, murid FROM bimbing WHERE guru = ?').bind(aktif.email).all();
      const guru = await DB.prepare(
        "SELECT email, nama FROM anggota WHERE peran IN ('guru','owner') AND status = 'aktif' ORDER BY nama, email"
      ).all();
      return json({ pasangan: r.results || [], guru: guru.results || [] });
    }

    // Menetapkan seluruh daftar guru untuk SATU murid sekaligus.
    // Dikirim utuh supaya tidak ada keadaan setengah tersimpan.
    if (rute === 'bimbing/atur' && metode === 'POST') {
      if (!isOwner) return json({ galat: 'Hanya pemilik situs yang mengatur pembimbing.' }, 403);
      const b = await badan();
      const murid = rapi(b.murid);
      if (!murid) return json({ galat: 'Murid tidak disebut.' }, 400);
      const m = await DB.prepare("SELECT peran, status FROM anggota WHERE email = ?").bind(murid).first();
      if (!m) return json({ galat: 'Murid tidak ditemukan.' }, 404);
      if (m.peran !== 'siswa') return json({ galat: 'Pembimbing hanya untuk akun siswa.' }, 400);

      const minta = [...new Set((Array.isArray(b.guru) ? b.guru : []).map(rapi).filter(Boolean))].slice(0, 50);
      let sah = [];
      if (minta.length) {
        const tanda = minta.map(() => '?').join(',');
        const g = await DB.prepare(
          `SELECT email FROM anggota WHERE email IN (${tanda}) AND status = 'aktif' AND peran IN ('guru','owner')`
        ).bind(...minta).all();
        sah = (g.results || []).map(x => x.email);
      }
      const tolak = minta.filter(e => !sah.includes(e));

      const perintah = [DB.prepare('DELETE FROM bimbing WHERE murid = ?').bind(murid)];
      for (const g of sah) {
        perintah.push(DB.prepare('INSERT INTO bimbing (guru, murid, dibuat, oleh) VALUES (?,?,?,?)')
          .bind(g, murid, kini(), aktif.email));
      }
      await DB.batch(perintah);
      return json({ ok: true, murid, guru: sah, ditolak: tolak });
    }

    /* ---------- penilaian oleh guru ---------- */

    // Antrean: apa saja yang menunggu nilai guru.
    // Pemilik melihat seluruh murid; guru hanya murid bimbingannya.
    if (rute === 'guru/antrean' && metode === 'GET') {
      if (!isGuru) return json({ galat: 'Khusus guru.' }, 403);
      const r = isOwner
        ? await DB.prepare(
            "SELECT a.email, a.nama, a.kelas, p.tp, p.data, p.diubah FROM anggota a " +
            "JOIN progres p ON p.email = a.email " +
            "WHERE a.status = 'aktif' AND a.peran = 'siswa'").all()
        : await DB.prepare(
            "SELECT a.email, a.nama, a.kelas, p.tp, p.data, p.diubah FROM anggota a " +
            "JOIN bimbing b ON b.murid = a.email AND b.guru = ? " +
            "JOIN progres p ON p.email = a.email " +
            "WHERE a.status = 'aktif' AND a.peran = 'siswa'").bind(aktif.email).all();

      const antre = [];
      for (const row of r.results || []) {
        let d; try { d = JSON.parse(row.data); } catch { continue; }
        const ev = (d && d.ev) || {};
        const sk = id => (ev[id] && ev[id].skor != null) ? ev[id].skor : null;
        const dasar = { email: row.email, nama: row.nama, kelas: row.kelas, tp: row.tp, diubah: row.diubah };
        // S12 Tugas Kinerja: murid sudah mengirim bukti, tier belum diisi guru.
        if (ev.S12 && !d.tier) antre.push({ ...dasar, tahapan: 'S12', minta: 'tier' });
        // S8 Gerbang Formatif Kelas: murid sudah lulus S4, skor gerbang belum masuk.
        if (ev.S4 && sk('S2') != null && sk('S2') >= 80 && (sk('S8') == null || (ev.S8 && ev.S8.cekUlang) || (d.p5Usulan&&d.p5Usulan.menunggu)))
          antre.push({ ...dasar, tahapan: 'S8', minta: 'skor', usulan:d.p5Usulan&&d.p5Usulan.menunggu?d.p5Usulan:null });
      }
      antre.sort((x, y) => (x.diubah || 0) - (y.diubah || 0));
      return json({ antrean: antre.slice(0, 500), jumlah: antre.length });
    }

    // Guru menuliskan nilai ke progres muridnya.
    if (rute === 'guru/nilai' && metode === 'POST') {
      if (!isGuru) return json({ galat: 'Khusus guru.' }, 403);
      const b = await badan();
      const murid = rapi(b.murid), slug = String(b.tp || '').slice(0, 80);
      const tahapan = String(b.tahapan || '').toUpperCase();
      if (!murid || !slug || !['S8', 'S12'].includes(tahapan))
        return json({ galat: 'Permintaan tidak lengkap. Tahapan yang dapat dinilai guru hanya P5 dan P8.' }, 400);

      if (!isOwner) {
        const ikat = await DB.prepare('SELECT 1 AS a FROM bimbing WHERE guru = ? AND murid = ?')
          .bind(aktif.email, murid).first();
        if (!ikat) return json({ galat: 'Murid ini bukan bimbingan Anda.' }, 403);
      }

      const baris = await DB.prepare('SELECT data FROM progres WHERE email = ? AND tp = ?').bind(murid, slug).first();
      let d = { ev: {}, tier: null, s14: [], riwayat: [] };
      if (baris) { try { d = JSON.parse(baris.data) || d; } catch {} }
      d.ev = d.ev || {};

      if (tahapan === 'S8') {
        const skor = Number(b.skor);
        if (!isFinite(skor) || skor < 0 || skor > 100) return json({ galat: 'Skor harus 0–100.' }, 400);
        d.ev.S8 = { ...(d.ev.S8 || {}), skor: Math.round(skor), oleh: aktif.nama || 'Guru', pada: kini() };
        delete d.ev.S8.cekUlang;
        if(d.p5Usulan)d.p5Usulan.menunggu=false;
        const fokus=Number(b.fokus||0);
        d.ev.S8.fokus=Number.isInteger(fokus)&&fokus>=0&&fokus<=4?fokus:0;
      } else {
        const tier = Number(b.tier);
        if (!Number.isInteger(tier) || tier < 1 || tier > 4) return json({ galat: 'Tier harus 1–4.' }, 400);
        d.tier = tier;
        d.ev.S12 = { ...(d.ev.S12 || {}), oleh: aktif.nama || 'Guru', pada: kini() };
      }
      d.epoch = (Number(d.epoch) || 0) + 1;   // salinan murid yang usang tidak boleh menimpa nilai ini

      await DB.prepare(
        'INSERT INTO progres (email, tp, data, diubah, oleh) VALUES (?,?,?,?,?) ' +
        'ON CONFLICT(email, tp) DO UPDATE SET data = excluded.data, diubah = excluded.diubah, oleh = excluded.oleh'
      ).bind(murid, slug, JSON.stringify(d).slice(0, 20000), kini(), aktif.email).run();

      return json({ ok: true, murid, tp: slug, tahapan, data: d });
    }

    /* Guru membuka ulang SATU dokumen murid. Hanya hasil dokumen itu yang dihapus: skor/tanda selesai
       (S12: juga tier-nya; S14: hasil pengulangan terakhir) dan/atau isian lembarnya. Tahapan lain dan
       TP-nya tetap utuh. Murid bisa langsung mengerjakan ulang. Siapa pun yang boleh menilai muridnya
       boleh mereset.
       Dua cara menunjuk dokumen: (tp + tahapan) untuk S1–S14, dan/atau "kunci" untuk dokumen isian
       (lapis L1–L4, paket, tahapan). Bila keduanya diberikan, keduanya dibuka ulang sekaligus. */
    if (rute === 'guru/reset' && metode === 'POST') {
      if (!isGuru) return json({ galat: 'Khusus guru.' }, 403);
      const b = await badan();
      const murid = rapi(b.murid), slug = String(b.tp || '').slice(0, 80);
      const id = String(b.tahapan || '').toUpperCase().replace(/([BC])$/, c => c.toLowerCase());
      const kunci = (b.kunci === undefined || b.kunci === null) ? '' : String(b.kunci);
      const alasan = String(b.alasan || '').replace(/\s+/g, ' ').trim().slice(0, 160);
      const SAH = ['S1', 'S2', 'S2b', 'S2c', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14'];
      const adaTahapan = !!slug && SAH.includes(id);
      if (!murid || (!adaTahapan && !kunci))
        return json({ galat: 'Permintaan tidak lengkap: murid serta tahapan atau dokumen wajib diisi.' }, 400);
      if (kunci && !kunciSah(kunci)) return json({ galat: 'Kunci dokumen tidak sah.' }, 400);

      if (!isOwner) {
        const ikat = await DB.prepare('SELECT 1 AS a FROM bimbing WHERE guru = ? AND murid = ?')
          .bind(aktif.email, murid).first();
        if (!ikat) return json({ galat: 'Murid ini bukan bimbingan Anda.' }, 403);
      }

      const perintah = [];
      let dataTP = null, adaLembar = false;

      // (a) hasil tahapan pada progres TP
      if (adaTahapan) {
        const baris = await DB.prepare('SELECT data FROM progres WHERE email = ? AND tp = ?').bind(murid, slug).first();
        if (!baris) {
          if (!kunci) return json({ galat: 'Murid ini belum punya progres pada TP tersebut.' }, 404);
        } else {
          let d = {}; try { d = JSON.parse(baris.data) || {}; } catch {}
          const r = bukaTahapan(d, id);
          if (r.galat) {
            if (!kunci) return json({ galat: r.galat }, 400);
          } else {
            // Catatan untuk guru dan murid. Hanya nama tampilan, tidak pernah surel (surel pemilik dirahasiakan).
            const catatan = Array.isArray(d.reset) ? d.reset : [];
            catatan.push({ t: id, pada: Date.now(), nama: aktif.nama || 'Guru', alasan, dulu: r.dulu });
            d.reset = catatan.slice(-15);
            d.epoch = (Number(d.epoch) || 0) + 1;
            dataTP = d;
            perintah.push(DB.prepare(
              'INSERT INTO progres (email, tp, data, diubah, oleh) VALUES (?,?,?,?,?) ' +
              'ON CONFLICT(email, tp) DO UPDATE SET data = excluded.data, diubah = excluded.diubah, oleh = excluded.oleh'
            ).bind(murid, slug, JSON.stringify(d).slice(0, 20000), kini(), aktif.email));
          }
        }
      }

      // (b) isian lembar: diganti batu nisan {reset:{...}} dan epoch dinaikkan
      if (kunci) {
        await pastikanLembar(DB);
        const l = await DB.prepare('SELECT data, skor, selesai, terisi, total, epoch FROM lembar WHERE email = ? AND kunci = ?')
          .bind(murid, kunci).first();
        if (l) {
          let dl = {}; try { dl = JSON.parse(l.data) || {}; } catch {}
          const adaIsi = !!((dl.f && Object.keys(dl.f).length) || dl.x != null || l.selesai || l.skor != null);
          if (adaIsi) {
            const nisan = { reset: { pada: Date.now(), nama: aktif.nama || 'Guru', alasan,
                                     dulu: { skor: l.skor, terisi: l.terisi, total: l.total, selesai: l.selesai ? 1 : 0 } } };
            perintah.push(DB.prepare(
              'UPDATE lembar SET data = ?, skor = NULL, selesai = 0, terisi = 0, epoch = ?, diubah = ?, oleh = ? WHERE email = ? AND kunci = ?'
            ).bind(JSON.stringify(nisan), (Number(l.epoch) || 0) + 1, kini(), aktif.email, murid, kunci));
            adaLembar = true;
          }
        }
      }

      if (!perintah.length)
        return json({ galat: 'Dokumen ini belum punya hasil atau isian tersimpan, jadi tidak ada yang perlu dibuka ulang.' }, 400);
      await DB.batch(perintah);

      return json({ ok: true, murid, tp: slug || null, tahapan: adaTahapan ? id : null, kunci: kunci || null,
                    data: dataTP, lembar: adaLembar });
    }

    return json({ galat: 'Jalur tidak dikenal: ' + rute }, 404);
  } catch (e) {
    return json({ galat: 'Galat peladen: ' + (e && e.message ? e.message : String(e)) }, 500);
  }
}
