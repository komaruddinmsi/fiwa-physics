// build.js — Vertical Academy (CMS FIMS)
// Memindai folder konten/ dan menulis katalog.json.
// Struktur: konten/<topik>/<tp>/<TAHAPAN>/index.html  (atau <TAHAPAN>.html)
//           konten/<topik>/<L1..L4>/index.html        (lapis topik)
// Opsional: konten/<topik>/topik.json dan konten/<topik>/<tp>/tp.json
const fs = require('fs');
const path = require('path');
const ROOT = 'konten';
// Kunci lama menjaga kesinambungan progres akun; navigasi publik memakai P.
const TAHAPAN_TP = ['S1','S2','S2b','S2c','S3','S4','S5','S6','S7','S8','S9','S11','S12','S13','S14'];
const TAHAPAN_TOPIK = ['L1','L2','L3','L4'];

const isDir = p => fs.existsSync(p) && fs.statSync(p).isDirectory();
const readJSON = p => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return {}; } };
const judulDari = f => {
  const m = fs.readFileSync(f, 'utf8').match(/<title>([^<]*)<\/title>/i);
  return m ? m[1].trim() : '';
};
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Cari berkas tahapan: <dir>/<ID>/index.html atau <dir>/<ID>.html (tidak peka huruf besar/kecil)
function cariTahapan(dir, daftar) {
  const hasil = {};
  const isi = fs.readdirSync(dir);
  for (const id of daftar) {
    const nama = isi.find(n => n.toLowerCase() === id.toLowerCase() || n.toLowerCase() === id.toLowerCase() + '.html');
    if (!nama) continue;
    const p = path.join(dir, nama);
    const f = isDir(p) ? path.join(p, 'index.html') : p;
    const interaktif=path.join(dir,nama,'interaktif.html');
    const aktif=fs.existsSync(interaktif)?interaktif:f;
    if (!fs.existsSync(aktif)) continue;
    hasil[id] = { berkas: aktif.split(path.sep).join('/'), judul: judulDari(aktif),...(aktif===interaktif?{versi:4}:{}) };
    // Konten kedua untuk satu tahapan: <ID>/latihan.html (dipakai L3: latihan unit test)
    if (isDir(p)) {
      const baruLat=path.join(p,'latihan-interaktif.html');
      const lat=fs.existsSync(baruLat)?baruLat:path.join(p,'latihan.html');
      if (fs.existsSync(lat)) hasil[id].latihan = { berkas: lat.split(path.sep).join('/'), judul: judulDari(lat) };
    }
  }
  return hasil;
}

// Topik berjenis "paket": kumpulan dokumen lepas tanpa alur pembelajaran.
// Struktur: konten/<topik>/paket/*.html  (+ paket.json untuk keterangan tiap berkas)
function cariPaket(dirT) {
  const dirP = path.join(dirT, 'paket');
  if (!isDir(dirP)) return { tahap: [], daftar: [] };
  const meta = readJSON(path.join(dirP, 'paket.json'));
  const ket = meta.berkas || {};
  const tahap = (meta.tahap || []).slice().sort((a, b) => (a.urutan ?? 999) - (b.urutan ?? 999));
  const urutTahap = k => { const i = tahap.findIndex(t => t.kode === k); return i < 0 ? 999 : i; };
  const daftar = fs.readdirSync(dirP)
    .filter(n => n.toLowerCase().endsWith('.html'))
    .map(n => {
      const f = path.join(dirP, n), m = ket[n] || {};
      return {
        slug: slug(n.replace(/\.html$/i, '')),
        berkas: f.split(path.sep).join('/'),
        judul: m.judul || judulDari(f) || n,
        tahap: m.tahap || '',
        soal: m.soal ?? null,
        bentuk: m.bentuk || '',
        ringkas: m.ringkas || '',
        catatan: m.catatan || '',
        urutan: m.urutan ?? 999
      };
    })
    .sort((a, b) => urutTahap(a.tahap) - urutTahap(b.tahap) || a.urutan - b.urutan || a.slug.localeCompare(b.slug));
  return { tahap, daftar };
}

// Halaman pembuka topik: fenomena dunia nyata, dibuka sebelum S1 pada TP pertama.
function cariPembuka(dirT) {
  const f = path.join(dirT, 'pembuka', 'index.html');
  if (!fs.existsSync(f)) return null;
  return { berkas: f.split(path.sep).join('/'), judul: judulDari(f) };
}

const topik = [];
if (isDir(ROOT)) {
  for (const t of fs.readdirSync(ROOT).filter(n => isDir(path.join(ROOT, n)))) {
    const dirT = path.join(ROOT, t);
    const metaT = readJSON(path.join(dirT, 'topik.json'));
    const jenis = metaT.jenis === 'paket' ? 'paket' : 'alur';
    if (jenis === 'paket') {
      const { tahap, daftar } = cariPaket(dirT);
      topik.push({
        slug: slug(t), kode: metaT.kode || t, nama: metaT.nama || t,
        mapel: metaT.mapel || 'Umum', fase: metaT.fase || '', jalur: metaT.jalur || '',
        urutan: metaT.urutan ?? 999, jenis: 'paket', ringkas: metaT.ringkas || '',
        tahap, paket: daftar, tahapan: {}, tp: []
      });
      continue;
    }
    const daftarTP = [];
    for (const p of fs.readdirSync(dirT).filter(n => isDir(path.join(dirT, n)) && n.toLowerCase() !== 'pembuka' && !TAHAPAN_TOPIK.includes(n.toUpperCase()))) {
      const dirP = path.join(dirT, p);
      const metaP = readJSON(path.join(dirP, 'tp.json'));
      const tahapan = cariTahapan(dirP, TAHAPAN_TP);
      for (const [lama,baru] of [['S1','P1'],['S2','P2'],['S2b','P2a'],['S2c','P2b'],['S3','P3'],['S4','P4'],['S5','P4/diskusi.html'],['S6','P4/contoh.html'],['S7','P4/praktik.html'],['S8','P5'],['S9','P6a'],['S11','P7'],['S12','P8'],['S13','P9/form-1.html']]) {
        const f=path.join(dirP,...(baru.endsWith('.html')?[baru]:[baru,'index.html']));
        if(fs.existsSync(f)) tahapan[lama]={berkas:f.split(path.sep).join('/'),judul:judulDari(f),versi:4};
      }
      const review=path.join(dirP,'P10','sesi-1.html');
      if(fs.existsSync(review))tahapan.S14={berkas:review.split(path.sep).join('/'),judul:'Ulangi Materi',versi:4};
      daftarTP.push({
        slug: slug(p),
        kode: metaP.kode || p,
        judul: metaP.judul || (tahapan.S1 && tahapan.S1.judul) || p,
        teks: metaP.teks || '',
        bloom: metaP.bloom || '',
        urutan_ajar: metaP.urutan_ajar ?? 999,
        prasyarat: metaP.prasyarat || [],
        ambang: metaP.ambang || 75,
        tahapan
      });
    }
    daftarTP.sort((a, b) => a.urutan_ajar - b.urutan_ajar || a.kode.localeCompare(b.kode));
    topik.push({
      slug: slug(t),
      kode: metaT.kode || t,
      nama: metaT.nama || t,
      mapel: metaT.mapel || 'Umum',
      fase: metaT.fase || '',
      jalur: metaT.jalur || '',
      urutan: metaT.urutan ?? 999,
      jenis: 'alur',
      pembuka: cariPembuka(dirT),
      tahapan: cariTahapan(dirT, TAHAPAN_TOPIK),
      tp: daftarTP
    });
  }
}
topik.sort((a, b) => a.urutan - b.urutan || a.kode.localeCompare(b.kode));
fs.writeFileSync('katalog.json', JSON.stringify({ dibuat: new Date().toISOString(), topik }, null, 2));
const nPaket = topik.reduce((n, t) => n + (t.paket ? t.paket.length : 0), 0);
const tanpaPembuka = topik.filter(t => t.jenis === 'alur' && !t.pembuka).map(t => t.kode);
console.log(`${topik.length} topik, ${topik.reduce((n, t) => n + t.tp.length, 0)} TP, ${nPaket} paket ditemukan`);
if (tanpaPembuka.length) console.warn(`PERINGATAN: topik tanpa halaman pembuka: ${tanpaPembuka.join(', ')} — tambahkan konten/<topik>/pembuka/index.html`);
