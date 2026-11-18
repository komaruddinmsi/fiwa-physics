/* Penjaga berkas Fisika FIWA.
   Berjalan pada setiap permintaan ke situs, termasuk permintaan berkas statis.

   Yang dijaga: seluruh bahan belajar. Yang dibiarkan terbuka hanya kulit situs —
   cukup untuk menampilkan laman masuk, tidak lebih.

   Tanda tangan sesi diperiksa di sini tanpa menyentuh D1 sama sekali, supaya
   memuat 36 halaman tahapan tidak berubah menjadi 36 pertanyaan ke basis data.  */

const NAMA_KUKI = 'fims_sesi';

// Awalan jalur yang hanya boleh dibuka anggota aktif.
const DIJAGA = ['/konten/', '/aset-f-use/', '/media-f-use/', '/katalog.json',
                '/skema.sql', '/skema-ringkas.sql', '/migrasi-sandi.sql', '/PANDUAN-AKUN.md', '/PANDUAN-MEDIA.md'];

const dijaga = jalur => DIJAGA.some(a => jalur === a || jalur.startsWith(a));

async function tandaTangan(isi, rahasia) {
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(rahasia),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const buf = await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(isi));
  return btoa(String.fromCharCode(...new Uint8Array(buf)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function sesiSah(kuki, rahasia) {
  if (!kuki) return null;
  const [b, sig] = String(kuki).split('.');
  if (!b || !sig) return null;
  let isi;
  try { isi = new TextDecoder().decode(Uint8Array.from(atob(b.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0))); }
  catch { return null; }
  if (await tandaTangan(isi, rahasia) !== sig) return null;
  const [email, peran, exp] = isi.split('|');
  if (!email || !(+exp > Math.floor(Date.now() / 1000))) return null;
  return { email, peran };
}

const LAMAN_TOLAK = `<!doctype html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Perlu masuk dulu</title>
<style>
 body{margin:0;min-height:100vh;display:grid;place-items:center;text-align:center;padding:28px;
   font:16px/1.6 "Source Sans 3","Segoe UI",system-ui,sans-serif;color:#eaf0ff;
   background:radial-gradient(900px 500px at 10% -10%,rgba(26,73,196,.6),transparent 60%),
              radial-gradient(700px 420px at 95% 0,rgba(0,180,156,.32),transparent 58%),
              linear-gradient(180deg,#061233,#040c24)}
 .k{max-width:46ch;background:rgba(16,38,96,.72);border:1px solid rgba(120,160,255,.24);
   border-radius:16px;padding:30px 28px}
 h1{font:700 1.4rem/1.2 "Bricolage Grotesque","Segoe UI",system-ui,sans-serif;margin:0 0 10px}
 p{color:#cfdcff;margin:0 0 18px}
 a{display:inline-block;background:linear-gradient(135deg,#3f7bff,#00c9a7);color:#04142e;
   text-decoration:none;font-weight:600;border-radius:10px;padding:11px 20px}
</style></head><body><div class="k">
 <h1>Bahan ini hanya untuk anggota</h1>
 <p>Masuk dengan alamat surelmu lebih dulu. Bila akunmu baru, pemilik situs perlu menyetujuinya sekali saja.</p>
 <a href="/" target="_top">Ke laman masuk</a>
</div></body></html>`;

export async function onRequest(ctx) {
  const { request, env, next } = ctx;
  const jalur = new URL(request.url).pathname;

  // Jalur yang tidak dijaga lewat begitu saja, termasuk /api/ yang menjaga dirinya sendiri.
  if (!dijaga(jalur)) return next();

  // Belum dipasang: biarkan situs tetap hidup supaya pemasangan D1 tidak membuat
  // seluruh situs gelap sebelum pengikatan selesai.
  if (!env.DB || !env.RAHASIA) return next();

  const c = request.headers.get('cookie') || '';
  const m = c.match(new RegExp('(?:^|;\\s*)' + NAMA_KUKI + '=([^;]*)'));
  const sesi = await sesiSah(m ? decodeURIComponent(m[1]) : null, env.RAHASIA);
  if (sesi) return next();

  const mintaHtml = (request.headers.get('accept') || '').includes('text/html');
  return mintaHtml
    ? new Response(LAMAN_TOLAK, { status: 401, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } })
    : new Response(JSON.stringify({ galat: 'Perlu masuk dulu.' }), {
        status: 401, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
}
