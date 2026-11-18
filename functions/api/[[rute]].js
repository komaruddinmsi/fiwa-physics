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

const kodeBaru = () => {
  const huruf = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';        // tanpa I, O, 0, 1
  return [...crypto.getRandomValues(new Uint8Array(6))].map(n => huruf[n % huruf.length]).join('');
};

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
      return json({
        siap: true, masuk: true, email: aku.email, nama: aku.nama, peran: aku.peran,
        kelas: aku.kelas, owner: isOwner, guru: isGuru, wajibKode
      });
    }

    /* ---- masuk dengan email ---- */
    if (rute === 'masuk' && metode === 'POST') {
      const b = await badan();
      const email = rapi(b.email);
      const peranMinta = b.peran === 'guru' ? 'guru' : 'siswa';
      const nama = String(b.nama || '').trim().slice(0, 80);
      if (!sahEmail(email)) return json({ galat: 'Alamat surel tidak sah.' }, 400);

      let a = await DB.prepare('SELECT * FROM anggota WHERE email = ?').bind(email).first();

      if (!a) {
        const jadiOwner = email === owner;
        const kode = wajibKode && !jadiOwner ? kodeBaru() : null;
        await DB.prepare(
          'INSERT INTO anggota (email, nama, peran, status, kode, dibuat, terakhir) VALUES (?,?,?,?,?,?,?)'
        ).bind(email, nama || null, jadiOwner ? 'owner' : peranMinta,
               jadiOwner ? 'aktif' : 'menunggu', kode, kini(), kini()).run();
        a = await DB.prepare('SELECT * FROM anggota WHERE email = ?').bind(email).first();
      } else {
        if (nama && !a.nama) await DB.prepare('UPDATE anggota SET nama = ? WHERE email = ?').bind(nama, email).run();
        await DB.prepare('UPDATE anggota SET terakhir = ? WHERE email = ?').bind(kini(), email).run();
      }

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
      return json({ ok: true, email, status: status || a.status, peran: peran || a.peran,
                    nama: nama === null ? a.nama : nama, kode });
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
      await DB.batch([
        DB.prepare('DELETE FROM progres WHERE email = ?').bind(email),
        DB.prepare('DELETE FROM anggota WHERE email = ?').bind(email)
      ]);
      return json({ ok: true, email });
    }

    /* ---- progres: mengikuti akun, bukan peramban ---- */
    if (rute === 'progres' && metode === 'GET') {
      if (!aktif) return json({ galat: 'Belum masuk.' }, 401);
      const r = await DB.prepare('SELECT tp, data, diubah FROM progres WHERE email = ?').bind(aktif.email).all();
      const tp = {};
      for (const row of r.results || []) { try { tp[row.tp] = JSON.parse(row.data); } catch {} }
      return json({ tp });
    }

    if (rute === 'progres' && metode === 'PUT') {
      if (!aktif) return json({ galat: 'Belum masuk.' }, 401);
      const b = await badan();
      const tp = b.tp || {};
      const perintah = Object.entries(tp).slice(0, 200).map(([slug, data]) =>
        DB.prepare('INSERT INTO progres (email, tp, data, diubah) VALUES (?,?,?,?) ' +
                   'ON CONFLICT(email, tp) DO UPDATE SET data = excluded.data, diubah = excluded.diubah')
          .bind(aktif.email, String(slug).slice(0, 80), JSON.stringify(data).slice(0, 20000), kini()));
      if (perintah.length) await DB.batch(perintah);
      return json({ ok: true, jumlah: perintah.length });
    }

    /* ---- papan kelas: seluruh siswa, hanya untuk guru ---- */
    if (rute === 'papan' && metode === 'GET') {
      if (!isGuru) return json({ galat: 'Khusus guru.' }, 403);
      const r = await DB.prepare(
        "SELECT a.email, a.nama, a.kelas, p.tp, p.data FROM anggota a " +
        "LEFT JOIN progres p ON p.email = a.email " +
        "WHERE a.status = 'aktif' AND a.peran = 'siswa' ORDER BY a.nama, a.email"
      ).all();
      const murid = {};
      for (const row of r.results || []) {
        const m = murid[row.email] || (murid[row.email] = { email: row.email, nama: row.nama, kelas: row.kelas, tp: {} });
        if (row.tp) { try { m.tp[row.tp] = JSON.parse(row.data); } catch {} }
      }
      return json({ murid: Object.values(murid) });
    }

    return json({ galat: 'Jalur tidak dikenal: ' + rute }, 404);
  } catch (e) {
    return json({ galat: 'Galat peladen: ' + (e && e.message ? e.message : String(e)) }, 500);
  }
}
