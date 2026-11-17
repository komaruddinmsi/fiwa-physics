/* Vertical Academy — mesin alur Pembelajaran Tuntas (CMS FIMS), versi statis.
   Data kurikulum: katalog.json (dibuat build.js). Progres siswa: localStorage perangkat ini.
   Halaman tahapan boleh melapor skor:  parent.postMessage({fims:'skor', skor:85}, '*')
   atau selesai tanpa skor:              parent.postMessage({fims:'selesai'}, '*')            */
(function () {
'use strict';

/* ---------- dwibahasa: teks antarmuka Indonesia (asal) dan Inggris ---------- */
const EN = {
"Peta & Janji": "Map & Pledge",
"Gerbang Prasyarat": "Prerequisite Gate",
"Penguatan Prasyarat": "Prerequisite Reinforcement",
"Remediasi Prasyarat": "Prerequisite Remediation",
"Pemantik & Prakonsepsi": "Hook & Preconceptions",
"Penyajian Konsep Awal": "First Concept Exposure",
"Pembahasan Prakonsepsi": "Preconception Debrief",
"Inti Terbimbing": "Guided Core",
"Praktik Terstruktur": "Structured Practice",
"Gerbang Formatif Kelas": "Class Formative Gate",
"Diferensiasi T1–T4": "Differentiation T1–T4",
"Konsolidasi & Jangkar": "Consolidation & Anchor",
"Latihan Bertingkat": "Tiered Practice",
"Tugas Kinerja": "Performance Task",
"Gerbang Ketuntasan TP": "LO Mastery Gate",
"Pengulangan Berjarak": "Spaced Retrieval",
"Dibuka": "Opened",
"≥80% lanjut · 60–79% → S2b · <60% → S2c": "≥80% proceed · 60–79% → S2b · <60% → S2c",
"Ulang S2 satu kali": "Retake S2 once",
"Ulang S2": "Retake S2",
"Terkirim (tidak dinilai)": "Submitted (ungraded)",
"Cek sisipan terjawab": "Embedded checks answered",
"Dipimpin guru": "Teacher-led",
"Lembar kerja terisi": "Worksheet completed",
"≥80% benar": "≥80% correct",
"Sesuai cabang S8": "Per the S8 branch",
"Jangkar terkirim": "Anchor submitted",
"Benar 3 dari 4 (≥75%) · H+0–H+2": "3 of 4 correct (≥75%) · D+0–D+2",
"Minimal T3 (dinilai guru) · H+1–H+5": "At least T3 (teacher-graded) · D+1–D+5",
"Butir baru, sekali jalan · H+2–H+7": "Fresh items, one attempt · D+2–D+7",
"H+14, +30, +60 · gagal → turun": "D+14, +30, +60 · fail → drop",
"Kuis Blok": "Block Quiz",
"Setiap 2–4 TP": "Every 2–4 LOs",
"Muara Topik": "Topic Synthesis",
"Setelah TP terakhir": "After the final LO",
"Tes Topik": "Topic Test",
"Akhir topik": "End of topic",
"Tantangan Mata Pelajaran": "Subject Challenge",
"Berkala, lintas topik": "Periodic, across topics",
"Fase 0 · Pra-KBM": "Phase 0 · Pre-class",
"Fase 1 · KBM": "Phase 1 · In class",
"Fase 2 · Pasca-KBM": "Phase 2 · Post-class",
"Belum Mulai": "Not Started",
"Siap": "Ready",
"Mencoba": "Attempting",
"Akrab": "Familiar",
"Mahir": "Proficient",
"Tuntas": "Mastered",
" Stabil": " Stable",
"Kurikulum Nasional · persiapan TKA": "Indonesian national curriculum · TKA preparation",
"Kelas 9–10 · jalur internasional": "Grades 9–10 · international track",
"Kelas 11–12 · jalur internasional": "Grades 11–12 · international track",
"Fase E–F · jalur nasional": "Phases E–F · national track",
"Hanya untuk skor S2 60–79%": "Only for an S2 score of 60–79%",
"Hanya untuk skor S2 di bawah 60%": "Only for an S2 score below 60%",
"Lulus Gerbang Prasyarat (S2 ≥ 80%) dulu": "Pass the Prerequisite Gate (S2 ≥ 80%) first",
"Kirim prakonsepsi S3 sebelum tatap muka": "Submit the S3 preconceptions before the lesson",
"Kerjakan Gerbang Formatif S8 di kelas": "Sit the S8 Class Formative Gate in class",
"Kerjakan Latihan Bertingkat S11 dulu": "Do the S11 Tiered Practice first",
"Kerjakan S11 dulu": "Do S11 first",
"Tugas Kinerja S12 harus dinilai minimal T3": "The S12 Performance Task must be graded at least T3",
"Kuis tertunda dibuka %s (H+2 setelah S11)": "The delayed quiz opens %s (D+2 after S11)",
"Sudah dikerjakan (sekali jalan). Gagal? Ulangi S11 dulu": "Already attempted (one attempt only). Failed? Redo S11 first",
"Terbuka setelah status Tuntas": "Opens once the status is Mastered",
"Tiga interval lulus: Tuntas Stabil": "Three intervals passed: Mastered & Stable",
"Interval %s jatuh tempo %s": "Interval %s is due %s",
"Belajar Fisika sampai tuntas": "Learning physics to mastery",
"Tiga jalur, satu cara kerja: setiap tujuan pembelajaran ditempuh bertahap dari Pra-KBM sampai Pasca-KBM, dan baru dinyatakan tuntas bila lulus gerbang akhirnya.": "Three tracks, one way of working: every learning objective is walked through stage by stage, from pre-class to post-class, and counts as mastered only once its final gate is passed.",
"Pilih jalur": "Choose a track",
"Lanjutkan belajar": "Continue learning",
"Mulai": "Start",
"Topik lain": "Other topics",
"Segera hadir": "Coming soon",
"%s topik · %s TP": "%s topics · %s LOs",
"1 topik · %s TP": "1 topic · %s LOs",
"1 TP": "1 LO",
"1 TP Tuntas": "1 LO mastered",
"%s TP Tuntas": "%s LOs mastered",
"%s dari %s TP Tuntas": "%s of %s LOs mastered",
"%s TP": "%s LOs",
"Fase ": "Phase ",
"Topik": "Topics",
"Materi jalur ini sedang disiapkan. Jalur yang sudah terbuka bisa dilihat di <a href=\"#\">beranda</a>.": "Materials for this track are being prepared. The tracks already open are listed on the <a href=\"#\">home page</a>.",
"Guru: tambahkan folder topik di <span class=\"mono\">konten/</span> dengan <span class=\"mono\">\"jalur\": \"%s\"</span> pada <span class=\"mono\">topik.json</span>.": "Teacher: add a topic folder under <span class=\"mono\">konten/</span> with <span class=\"mono\">\"jalur\": \"%s\"</span> in its <span class=\"mono\">topik.json</span>.",
"Tujuan Pembelajaran": "Learning Objectives",
"Lapis topik": "Topic layers",
"Belum ada TP.": "No learning objectives yet.",
"Belum diunggah": "Not uploaded yet",
"Belum diunggah.": "Not uploaded yet.",
"Beranda": "Home",
"Status turun ke Mahir: pengulangan berjarak gagal. Jadwal diulang dari H+14.": "Status dropped to Proficient: a spaced retrieval was failed. The schedule restarts at D+14.",
"Tier T%s: perlu pendampingan pada konteks baru, bukan tambahan latihan soal.": "Tier T%s: needs coaching on unfamiliar contexts, not more practice questions.",
"Kelengkapan: tahapan rangka belum diunggah — %s.": "Completeness: core stages not yet uploaded — %s.",
"Jadwal pengulangan berjarak (S14)": "Spaced retrieval schedule (S14)",
"Interval": "Interval",
"Hari": "Day",
"Jatuh tempo": "Due",
"Hasil": "Result",
"Interval %s": "Interval %s",
"berikutnya": "next",
"lulus": "passed",
"gagal": "failed",
"Tahapan %s belum diunggah.": "Stage %s has not been uploaded.",
"Lulus apabila: %s": "Passes when: %s",
"Mode guru: tahapan ini masih terkunci untuk siswa (%s).": "Teacher mode: this stage is still locked for students (%s).",
"Tandai bukti terkirim": "Mark evidence submitted",
"Tier diisi guru (rubrik T1–T4).": "The tier is set by the teacher (T1–T4 rubric).",
"Skor (%)": "Score (%)",
"Simpan skor": "Save score",
"Terisi otomatis bila halaman kuis mengirim skor.": "Filled in automatically when the quiz page reports a score.",
"Tandai selesai": "Mark done",
"Panel guru · %s": "Teacher panel · %s",
"Tier dari rubrik S9/S12": "Tier from the S9/S12 rubric",
"Hapus progres TP ini": "Clear progress for this LO",
"Selisih S11 − S13: %s · Riwayat status: %s": "S11 − S13 gap: %s · Status history: %s",
"%s poin": "%s points",
"belum ada data": "no data yet",
"Papan guru": "Teacher board",
"Kelengkapan & posisi": "Completeness & standing",
"Kelengkapan tahapan": "Stage completeness",
"✕ = tahapan rangka (S1, S2, S3, S5, S8, S10, S12, S13, S14) belum diunggah. TP dengan ✕ belum boleh terbit.": "✕ = a core stage (S1, S2, S3, S5, S8, S10, S12, S13, S14) has not been uploaded. An LO with any ✕ is not ready to publish.",
"Papan posisi": "Standing board",
"Warna = status, angka = tier. Versi statis hanya membaca progres di perangkat ini. Papan seluruh kelas butuh login dan database (Tahap 6 panduan).": "Colour = status, number = tier. This static version only reads progress stored on this device. A whole-class board needs sign-in and a database (Stage 6 of the guide).",
"Simulasi waktu": "Time simulation",
"Untuk uji alur kuis tertunda (H+2) dan pengulangan (H+14). Sekarang digeser %s hari.": "For testing the delayed-quiz (D+2) and spaced-retrieval (D+14) flows. Currently shifted by %s days.",
"+2 hari": "+2 days",
"+14 hari": "+14 days",
"Kembali ke hari ini": "Back to today",
"Siswa": "Student",
"Perangkat ini": "This device",
"Terbit": "Publish",
"Belum": "Not yet",
"TP": "LO",
"Belajar": "Learn",
"Papan Guru": "Teacher Board",
"Mode guru": "Teacher mode",
"Alur Konten Pembelajaran Tuntas · CMS FIMS · Fitrah Islamic World Academy. Progres tersimpan di perangkat ini.": "Mastery Learning Content Flow · CMS FIMS · Fitrah Islamic World Academy. Progress is stored on this device.",
"Memuat katalog…": "Loading the catalogue…",
"katalog.json belum ada. Jalankan <span class=\"mono\">node build.js</span> (Cloudflare menjalankannya otomatis).": "katalog.json is missing. Run <span class=\"mono\">node build.js</span> (Cloudflare runs it automatically).",
"Fisika FIWA — beranda": "Fisika FIWA — home"
};
let BHS = 'id';
const tr  = x => (BHS === 'id' || EN[x] === undefined) ? x : EN[x];
const trf = (x, ...v) => { let i = 0; return tr(x).replace(/%s/g, () => v[i++]); };

const TAHAPAN = [
  { id:'S1',  f:0, nama:'Peta & Janji',            lulus:'Dibuka',                         rangka:1 },
  { id:'S2',  f:0, nama:'Gerbang Prasyarat',       lulus:'≥80% lanjut · 60–79% → S2b · <60% → S2c', gate:1, skor:1, rangka:1 },
  { id:'S2b', f:0, nama:'Penguatan Prasyarat',     lulus:'Ulang S2 satu kali', cabang:1 },
  { id:'S2c', f:0, nama:'Remediasi Prasyarat',     lulus:'Ulang S2', cabang:1 },
  { id:'S3',  f:0, nama:'Pemantik & Prakonsepsi',  lulus:'Terkirim (tidak dinilai)', rangka:1 },
  { id:'S4',  f:0, nama:'Penyajian Konsep Awal',   lulus:'Cek sisipan terjawab' },
  { id:'S5',  f:1, nama:'Pembahasan Prakonsepsi',  lulus:'Dipimpin guru', rangka:1 },
  { id:'S6',  f:1, nama:'Inti Terbimbing',         lulus:'Dipimpin guru' },
  { id:'S7',  f:1, nama:'Praktik Terstruktur',     lulus:'Lembar kerja terisi' },
  { id:'S8',  f:1, nama:'Gerbang Formatif Kelas',  lulus:'≥80% benar', gate:1, skor:1, rangka:1 },
  { id:'S9',  f:1, nama:'Diferensiasi T1–T4',      lulus:'Sesuai cabang S8' },
  { id:'S10', f:1, nama:'Konsolidasi & Jangkar',   lulus:'Jangkar terkirim', rangka:1 },
  { id:'S11', f:2, nama:'Latihan Bertingkat',      lulus:'Benar 3 dari 4 (≥75%) · H+0–H+2', skor:1 },
  { id:'S12', f:2, nama:'Tugas Kinerja',           lulus:'Minimal T3 (dinilai guru) · H+1–H+5', gate:1, tier:1, rangka:1 },
  { id:'S13', f:2, nama:'Gerbang Ketuntasan TP',   lulus:'Butir baru, sekali jalan · H+2–H+7', gate:1, skor:1, rangka:1 },
  { id:'S14', f:2, nama:'Pengulangan Berjarak',    lulus:'H+14, +30, +60 · gagal → turun', gate:1, rangka:1 }
];
const LAPIS = [
  { id:'L1', nama:'Kuis Blok',              kapan:'Setiap 2–4 TP' },
  { id:'L2', nama:'Muara Topik',            kapan:'Setelah TP terakhir' },
  { id:'L3', nama:'Tes Topik',              kapan:'Akhir topik', gate:1 },
  { id:'L4', nama:'Tantangan Mata Pelajaran', kapan:'Berkala, lintas topik' }
];
const JALUR = [
  { slug:'igcse', kode:'IGCSE', nama:'PHYSICS IGCSE', teks:'Cambridge IGCSE Physics 0625',
    sub:'Kelas 9–10 · jalur internasional', cocok:/^igcse$/i },
  { slug:'as-a',  kode:'AS/A',  nama:'PHYSICS AS/A',  teks:'Cambridge AS &amp; A Level Physics 9702',
    sub:'Kelas 11–12 · jalur internasional', cocok:/^(as\/?-?a([\s-]?level)?|a[\s-]?level|as)$/i },
  { slug:'tka',   kode:'TKA',   nama:'PHYSICS TKA',   teks:'Kurikulum Nasional · persiapan TKA',
    sub:'Fase E–F · jalur nasional', cocok:/^tka$/i }
];
const FASE = ['Fase 0 · Pra-KBM', 'Fase 1 · KBM', 'Fase 2 · Pasca-KBM'];
const STATUS = ['Belum Mulai', 'Siap', 'Mencoba', 'Akrab', 'Mahir', 'Tuntas'];
const HARI = 864e5;
const T = id => TAHAPAN.find(s => s.id === id);

/* ---------- penyimpanan ---------- */
const KEY = 'va-fims-v1';
let db = {};
try { db = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { db = {}; }
db.tp = db.tp || {}; db.opsi = db.opsi || {};
BHS = db.opsi.bahasa === 'en' ? 'en' : 'id';
const simpan = () => { try { localStorage.setItem(KEY, JSON.stringify(db)); } catch (e) {} };
const prog = slug => (db.tp[slug] = db.tp[slug] || { ev: {}, tier: null, s14: [], riwayat: [] });
const now = () => Date.now() + (db.opsi.geser || 0) * HARI;   // "geser hari" = simulasi waktu untuk uji coba

/* ---------- mesin status ---------- */
function hitung(tp) {
  const p = prog(tp.slug), e = p.ev, amb = tp.ambang || 75;
  const sk = id => (e[id] && e[id].skor != null) ? e[id].skor : null;
  const ok = id => !!e[id];
  let s = 0;
  if (sk('S2') != null && sk('S2') >= 80) s = 1;
  if (s >= 1 && ok('S4')) s = 2;
  if (s >= 2 && sk('S8') != null && sk('S8') >= 80) s = 3;
  const tier = p.tier || 0;
  if (s >= 3 && sk('S11') != null && sk('S11') >= 75 && tier >= 3) s = 4;
  let stabil = false;
  if (s >= 4 && sk('S13') != null && sk('S13') >= amb) {
    const gagalTerakhir = p.s14.length && p.s14[p.s14.length - 1].hasil === 'gagal';
    s = gagalTerakhir ? 4 : 5;
    stabil = s === 5 && p.s14.filter(x => x.hasil === 'lulus').length >= 3;
  }
  // catat riwayat bila berubah (status tidak ditimpa, jejak disimpan)
  const last = p.riwayat.length ? p.riwayat[p.riwayat.length - 1].ke : 0;
  if (last !== s) { p.riwayat.push({ dari: last, ke: s, waktu: now() }); simpan(); }
  return { s, stabil, tier: p.tier, e, p, amb };
}

// apakah tahapan terbuka? kembalikan null bila terbuka, atau alasan terkunci
function kunci(tp, id, h) {
  const e = h.e, sk = x => e[x] && e[x].skor;
  if (['S1', 'S2'].includes(id)) return null;
  if (id === 'S2b') return (sk('S2') != null && sk('S2') >= 60 && sk('S2') < 80) ? null : tr('Hanya untuk skor S2 60–79%');
  if (id === 'S2c') return (sk('S2') != null && sk('S2') < 60) ? null : tr('Hanya untuk skor S2 di bawah 60%');
  if (h.s < 1) return tr('Lulus Gerbang Prasyarat (S2 ≥ 80%) dulu');
  if (['S3', 'S4'].includes(id)) return null;
  if (['S5', 'S6', 'S7', 'S8', 'S9', 'S10'].includes(id)) return e.S3 ? null : tr('Kirim prakonsepsi S3 sebelum tatap muka');
  if (id === 'S11') return e.S8 ? null : tr('Kerjakan Gerbang Formatif S8 di kelas');
  if (id === 'S12') return e.S11 ? null : tr('Kerjakan Latihan Bertingkat S11 dulu');
  if (id === 'S13') {
    if (!e.S11) return tr('Kerjakan S11 dulu');
    if ((h.tier || 0) < 3) return tr('Tugas Kinerja S12 harus dinilai minimal T3');
    const buka = e.S11.waktu + 2 * HARI;
    if (now() < buka) return trf('Kuis tertunda dibuka %s (H+2 setelah S11)', tgl(buka));
    if (e.S13 && e.S13.waktu > e.S11.waktu) return tr('Sudah dikerjakan (sekali jalan). Gagal? Ulangi S11 dulu');
    return null;
  }
  if (id === 'S14') {
    if (!(e.S13 && e.S13.skor >= h.amb && h.s >= 4)) return tr('Terbuka setelah status Tuntas');
    const j = jadwalS14(h).find(x => x.berikut);
    if (!j) return tr('Tiga interval lulus: Tuntas Stabil');
    if (now() < j.jatuh) return trf('Interval %s jatuh tempo %s', j.ke, tgl(j.jatuh));
    return null;
  }
  return null;
}

function jadwalS14(h) {
  const awal = (h.p.s14Mulai || (h.e.S13 && h.e.S13.waktu));
  if (!awal) return [];
  const iv = [14, 30, 60];
  const done = h.p.s14.filter(x => x.waktu >= awal).length;
  return iv.map((d, i) => ({ ke: i + 1, hari: d, jatuh: awal + d * HARI, hasil: (h.p.s14.filter(x => x.waktu >= awal)[i] || {}).hasil, berikut: i === done }));
}

function catat(tp, id, data) {
  const p = prog(tp.slug);
  if (id === 'S14') {
    const lulus = data.skor == null ? true : data.skor >= (tp.ambang || 75);
    p.s14.push({ hasil: lulus ? 'lulus' : 'gagal', waktu: now() });
    if (!lulus) p.s14Mulai = now();               // turun ke Mahir & jadwal ulang dari interval pertama
  } else {
    p.ev[id] = { waktu: now(), skor: data.skor == null ? null : Math.round(data.skor) };
    if (id === 'S2' && p.ev.S2.skor >= 80) { delete p.ev.S2b; delete p.ev.S2c; }
  }
  simpan();
}

// satu langkah berikutnya untuk satu TP
function langkah(tp) {
  const h = hitung(tp), e = h.e, sk = x => e[x] && e[x].skor;
  const ada = id => !!tp.tahapan[id];
  if (!e.S1 && ada('S1')) return 'S1';
  if (h.s < 1) {
    if (sk('S2') != null && sk('S2') < 60 && !e.S2c && ada('S2c')) return 'S2c';
    if (sk('S2') != null && sk('S2') < 80 && sk('S2') >= 60 && !e.S2b && ada('S2b')) return 'S2b';
    return 'S2';
  }
  for (const id of ['S3', 'S4']) if (!e[id] && ada(id)) return id;
  if (!e.S8) return null;                          // menunggu tatap muka
  if (!e.S11) return 'S11';
  if (!e.S12) return 'S12';
  if (!kunci(tp, 'S13', h)) return 'S13';
  if (h.s === 5 || (h.s === 4 && e.S13)) {
    const j = jadwalS14(h).find(x => x.berikut);
    if (j && now() >= j.jatuh) return 'S14';
  }
  return null;
}

/* ---------- utilitas tampilan ---------- */
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tgl = w => new Date(w).toLocaleDateString(BHS === 'en' ? 'en-GB' : 'id-ID', { day: 'numeric', month: 'short' });
const chip = (s, stabil) => `<span class="chip st${s}"><span class="dot"></span>${tr(STATUS[s])}${stabil ? tr(' Stabil') : ''}</span>`;
const tierTag = t => t ? `<span class="tier">T${t}</span>` : '<span class="tier muted">T–</span>';
let K = { topik: [] };
const semuaTP = () => K.topik.flatMap(t => t.tp.map(tp => Object.assign({ _t: t }, tp)));
const cariTP = slug => semuaTP().find(x => x.slug === slug);
const cariTopik = slug => K.topik.find(x => x.slug === slug);
const guru = () => !!db.opsi.guru;
const cariJalur = slug => JALUR.find(j => j.slug === slug);
const topikJalur = j => K.topik.filter(t => j.cocok.test(String(t.jalur || '').trim()));
const jalurTopik = t => JALUR.find(j => j.cocok.test(String(t.jalur || '').trim())) || null;
const topikLepas = () => K.topik.filter(t => !jalurTopik(t));
const remah = t => { const j = t && jalurTopik(t);
  return `<a href="#">${tr('Beranda')}</a> / ${j ? `<a href="#jalur-${j.slug}">${esc(j.kode)}</a> / ` : ''}`; };
const kartuTopik = t => { const n = t.tp.length, tuntas = t.tp.filter(tp => hitung(tp).s === 5).length;
  return `<a class="card" href="#topik-${t.slug}"><div class="eyebrow">${esc(t.mapel)}${t.fase ? ' · ' + tr('Fase ') + esc(t.fase) : ''}</div>
    <h3>${esc(t.nama)}</h3><div class="mono muted">${esc(t.kode)} · ${n === 1 ? tr('1 TP') : trf('%s TP', n)}</div>
    <div class="meter"><i style="width:${n ? Math.round(tuntas / n * 100) : 0}%"></i></div>
    <div class="muted" style="font-size:.85rem">${trf('%s dari %s TP Tuntas', tuntas, n)}</div></a>`; };

/* ---------- tampilan: beranda ---------- */
function kotakJalur() {
  return JALUR.map(j => {
    const ts = topikJalur(j), n = ts.length;
    const tps = ts.flatMap(t => t.tp);
    const tuntas = tps.filter(tp => hitung(tp).s === 5).length;
    const isi = n
      ? `<span class="jm">${n === 1 ? trf('1 topik · %s TP', tps.length) : trf('%s topik · %s TP', n, tps.length)}</span>`
      : `<span class="jm segera">${tr('Segera hadir')}</span>`;
    return `<a class="jalur j-${j.slug}" href="#jalur-${j.slug}">
      <span class="jk">${esc(j.kode)}</span>
      <span class="jn">${j.nama}</span>
      <span class="jt">${tr(j.teks)}</span>
      <span class="jb">${isi}${tps.length ? `<span class="jm">${tuntas === 1 ? tr('1 TP Tuntas') : trf('%s TP Tuntas', tuntas)}</span>` : ''}</span>
    </a>`;
  }).join('');
}

function beranda() {
  const tps = semuaTP();
  let next = null;
  for (const tp of tps) { const l = langkah(tp); if (l) { next = { tp, id: l }; break; } }
  const mulai = Object.keys(db.tp || {}).some(k => Object.keys((db.tp[k] || {}).ev || {}).length);
  const lanjut = (mulai && next)
    ? `<a class="next" href="#tp-${next.tp.slug}-${next.id.toLowerCase()}"><span class="what">
         <span class="eyebrow">${tr('Lanjutkan belajar')}</span>
         <b>${esc(tr(T(next.id).nama))}</b>
         <span class="muted"><span class="mono">${esc(next.tp.kode)} · ${next.id}</span> — ${esc(next.tp.judul)}</span></span>
       <span class="btn">${tr('Mulai')}</span></a>`
    : '';
  const lepas = topikLepas();
  const lain = lepas.length
    ? `<section class="stack"><h2>${tr('Topik lain')}</h2><div class="grid-topik">${lepas.map(kartuTopik).join('')}</div></section>`
    : '';
  return `<div class="stack">
    <section class="hero"><p class="eyebrow">Fitrah Islamic World Academy</p>
      <h1>${tr('Belajar Fisika sampai tuntas')}</h1>
      <p class="lede">${tr('Tiga jalur, satu cara kerja: setiap tujuan pembelajaran ditempuh bertahap dari Pra-KBM sampai Pasca-KBM, dan baru dinyatakan tuntas bila lulus gerbang akhirnya.')}</p></section>
    <section class="stack"><h2 class="sr-tajuk">${tr('Pilih jalur')}</h2><div class="grid-jalur">${kotakJalur()}</div></section>
    ${lanjut}${lain}</div>`;
}

/* ---------- tampilan: jalur ---------- */
function halJalur(j) {
  const ts = topikJalur(j);
  const kartu = ts.map(kartuTopik).join('');
  return `<div class="stack"><div class="crumbs"><a href="#">${tr('Beranda')}</a> / ${esc(j.kode)}</div>
    <section class="hero mini j-${j.slug}"><p class="eyebrow">${tr(j.sub)}</p><h1>${j.nama}</h1><p class="lede">${tr(j.teks)}</p></section>
    <section class="stack"><h2>${tr('Topik')}</h2>
      ${kartu ? `<div class="grid-topik">${kartu}</div>`
              : `<div class="note">${tr('Materi jalur ini sedang disiapkan. Jalur yang sudah terbuka bisa dilihat di <a href="#">beranda</a>.')}${guru() ? ` <span class="muted">${trf('Guru: tambahkan folder topik di <span class="mono">konten/</span> dengan <span class="mono">"jalur": "%s"</span> pada <span class="mono">topik.json</span>.', esc(j.kode))}</span>` : ''}</div>`}
    </section></div>`;
}

/* ---------- tampilan: topik ---------- */
function halTopik(t) {
  const tps = t.tp.map(tp => { const h = hitung(tp);
    return `<a class="item" href="#tp-${tp.slug}"><span class="code">${esc(tp.kode)}</span>
      <span class="t"><b>${esc(tp.judul)}</b>${tp.teks ? `<br><span class="muted">${esc(tp.teks)}</span>` : ''}</span>
      <span class="row">${chip(h.s, h.stabil)}${tierTag(h.tier)}</span></a>`; }).join('');
  const lapis = LAPIS.map(l => { const ada = t.tahapan[l.id];
    return ada ? `<a class="tile${l.gate ? ' gate' : ''}" href="#topik-${t.slug}-${l.id.toLowerCase()}"><span class="sid">${l.id}${l.gate ? ' ▲' : ''}</span><span class="nm">${esc(tr(l.nama))}<small>${esc(tr(l.kapan))}</small></span><span></span></a>`
               : `<div class="tile miss"><span class="sid">${l.id}</span><span class="nm">${esc(tr(l.nama))}<small>${tr('Belum diunggah')}</small></span><span></span></div>`; }).join('');
  return `<div class="stack"><div class="crumbs">${remah(t)}${esc(t.kode)}</div>
    <div><div class="eyebrow">${esc(t.mapel)}${t.jalur ? ' · ' + esc(t.jalur) : ''}</div><h1>${esc(t.nama)}</h1></div>
    <section class="stack"><h2>${tr('Tujuan Pembelajaran')}</h2><div class="list">${tps || `<p class="muted">${tr('Belum ada TP.')}</p>`}</div></section>
    <section class="stack"><h2>${tr('Lapis topik')}</h2><div class="layer">${lapis}</div></section></div>`;
}

/* ---------- tampilan: TP ---------- */
function halTP(tp, aktif) {
  const h = hitung(tp), t = tp._t;
  const ladder = STATUS.map((n, i) => `<div class="${i <= h.s && i > 0 ? 'on st' + i : ''}${i === 0 && h.s === 0 ? ' on' : ''}">${tr(n)}</div>`).join('');
  const lanes = [0, 1, 2].map(f => {
    const tiles = TAHAPAN.filter(s => s.f === f).map(s => {
      const ada = tp.tahapan[s.id], k = kunci(tp, s.id, h), ev = h.e[s.id];
      if (s.cabang && !ada) return '';
      let mark = '';
      if (s.id === 'S12') mark = h.tier ? 'T' + h.tier : (ev ? 'menunggu nilai' : '');
      else if (s.id === 'S14') mark = h.p.s14.length ? h.p.s14.length + '× ' : '';
      else if (ev) mark = ev.skor != null ? ev.skor + '%' : '✓';
      const cls = ['tile', s.gate ? 'gate' : '', s.cabang ? 'branch' : '', !ada ? 'miss' : '', ada && k ? 'lock' : '', aktif === s.id ? 'cur' : ''].join(' ');
      const sub = !ada ? tr('Belum diunggah') : (k ? '🔒 ' + k : tr(s.lulus));
      const inner = `<span class="sid">${s.id}${s.gate ? ' ▲' : ''}</span><span class="nm">${esc(tr(s.nama))}<small>${esc(sub)}</small></span><span class="mark${ev ? ' ok' : ''}">${esc(mark)}</span>`;
      return ada && (!k || guru()) ? `<a class="${cls}" href="#tp-${tp.slug}-${s.id.toLowerCase()}">${inner}</a>` : `<div class="${cls}">${inner}</div>`;
    }).join('');
    return `<div class="phase"><h3>${tr(FASE[f])}</h3>${tiles}</div>`;
  }).join('');
  const lengkap = TAHAPAN.filter(s => s.rangka && !tp.tahapan[s.id]).map(s => s.id);
  return `<div class="stack"><div class="crumbs">${remah(t)}<a href="#topik-${t.slug}">${esc(t.kode)}</a> / ${esc(tp.kode)}</div>
    <div class="row" style="justify-content:space-between"><div style="min-width:0"><div class="eyebrow mono">${esc(tp.kode)}${tp.bloom ? ' · Bloom ' + esc(tp.bloom) : ''}</div>
      <h1>${esc(tp.judul)}</h1>${tp.teks ? `<p class="muted" style="margin:.4em 0 0;max-width:65ch">${esc(tp.teks)}</p>` : ''}</div>
      <div class="row">${chip(h.s, h.stabil)}${tierTag(h.tier)}</div></div>
    <div class="ladder">${ladder}</div>
    ${h.s === 4 && h.p.s14.length && h.p.s14[h.p.s14.length - 1].hasil === 'gagal' ? `<div class="note">${tr('Status turun ke Mahir: pengulangan berjarak gagal. Jadwal diulang dari H+14.')}</div>` : ''}
    ${(h.tier && h.tier < 3) ? `<div class="note">${trf('Tier T%s: perlu pendampingan pada konteks baru, bukan tambahan latihan soal.', h.tier)}</div>` : ''}
    ${guru() && lengkap.length ? `<div class="note">${trf('Kelengkapan: tahapan rangka belum diunggah — %s.', lengkap.join(', '))}</div>` : ''}
    <div class="phases">${lanes}</div>
    ${aktif ? viewer(tp, aktif, h) : ''}
    ${h.e.S13 && h.e.S13.skor >= h.amb && h.s >= 4 ? s14Panel(h) : ''}
    ${guru() ? panelGuruTP(tp, h) : ''}</div>`;
}

function s14Panel(h) {
  const rows = jadwalS14(h).map(j => `<tr><td>${trf('Interval %s', j.ke)}</td><td>${BHS === 'en' ? 'D' : 'H'}+${j.hari}</td><td>${tgl(j.jatuh)}</td><td class="${j.hasil === 'lulus' ? 'y' : j.hasil === 'gagal' ? 'n' : 'o'}">${j.hasil ? tr(j.hasil) : (j.berikut ? tr('berikutnya') : '—')}</td></tr>`).join('');
  return `<section class="panel stack"><h3>${tr('Jadwal pengulangan berjarak (S14)')}</h3><div class="scroll"><table><tr><th>${tr('Interval')}</th><th>${tr('Hari')}</th><th>${tr('Jatuh tempo')}</th><th>${tr('Hasil')}</th></tr>${rows}</table></div></section>`;
}

function viewer(tp, id, h) {
  const s = T(id), f = tp.tahapan[id];
  if (!f) return `<div class="panel">${trf('Tahapan %s belum diunggah.', id)}</div>`;
  const k = kunci(tp, id, h);
  if (k && !guru()) return `<div class="note">🔒 ${esc(k)}</div>`;
  let aksi;
  if (s.tier) aksi = `<div class="row"><button class="btn" data-aksi="selesai">${tr('Tandai bukti terkirim')}</button><span class="muted">${tr('Tier diisi guru (rubrik T1–T4).')}</span></div>`;
  else if (s.skor || id === 'S14') aksi = `<div class="row"><label for="skorIn">${tr('Skor (%)')}</label><input type="number" id="skorIn" min="0" max="100" style="width:90px"><button class="btn" data-aksi="skor">${tr('Simpan skor')}</button><span class="muted">${tr('Terisi otomatis bila halaman kuis mengirim skor.')}</span></div>`;
  else aksi = `<div class="row"><button class="btn" data-aksi="selesai">${tr('Tandai selesai')}</button></div>`;
  return `<section class="viewer" id="viewer"><div class="row" style="justify-content:space-between"><h2>${id} · ${esc(tr(s.nama))}</h2><span class="muted">${trf('Lulus apabila: %s', esc(tr(s.lulus)))}</span></div>
    ${k ? `<div class="note">${trf('Mode guru: tahapan ini masih terkunci untuk siswa (%s).', esc(k))}</div>` : ''}
    <iframe class="frame" src="${esc(f.berkas)}" title="${esc(tr(s.nama))}"></iframe>${aksi}</section>`;
}

function panelGuruTP(tp, h) {
  const opsi = [0, 1, 2, 3, 4].map(n => `<option value="${n}"${(h.tier || 0) === n ? ' selected' : ''}>${n ? 'T' + n : '—'}</option>`).join('');
  const selisih = h.e.S11 && h.e.S13 && h.e.S11.skor != null && h.e.S13.skor != null
    ? trf('%s poin', h.e.S11.skor - h.e.S13.skor) : tr('belum ada data');
  return `<section class="panel stack"><h3>${trf('Panel guru · %s', esc(tp.kode))}</h3>
    <div class="row"><label for="tierIn">${tr('Tier dari rubrik S9/S12')}</label><select id="tierIn">${opsi}</select>
    <button class="btn ghost" data-aksi="reset">${tr('Hapus progres TP ini')}</button></div>
    <div class="muted" style="font-size:.85rem">${trf('Selisih S11 − S13: %s · Riwayat status: %s', selisih, h.p.riwayat.map(r => tr(STATUS[r.ke])).join(' → ') || '—')}</div></section>`;
}

/* ---------- tampilan: lapis topik ---------- */
function halLapis(t, id) {
  const l = LAPIS.find(x => x.id === id), f = t.tahapan[id];
  return `<div class="stack"><div class="crumbs">${remah(t)}<a href="#topik-${t.slug}">${esc(t.kode)}</a> / ${id}</div>
    <h1>${id} · ${esc(tr(l.nama))}</h1><p class="muted">${esc(tr(l.kapan))}</p>
    ${f ? `<iframe class="frame" src="${esc(f.berkas)}" title="${esc(tr(l.nama))}"></iframe>` : `<p>${tr('Belum diunggah.')}</p>`}</div>`;
}

/* ---------- tampilan: papan guru ---------- */
function halGuru() {
  const ids = TAHAPAN.map(s => s.id);
  const kel = K.topik.map(t => {
    const rows = t.tp.map(tp => `<tr><td class="l mono">${esc(tp.kode)}</td>${ids.map(id => {
      const s = T(id), ada = !!tp.tahapan[id];
      return `<td class="${ada ? 'y' : s.rangka ? 'n' : 'o'}">${ada ? '✓' : s.rangka ? '✕' : '·'}</td>`; }).join('')}
      <td class="${TAHAPAN.some(s => s.rangka && !tp.tahapan[s.id]) ? 'n' : 'y'}">${TAHAPAN.some(s => s.rangka && !tp.tahapan[s.id]) ? tr('Belum') : tr('Siap')}</td></tr>`).join('');
    return `<h3>${esc(t.kode)} · ${esc(t.nama)}</h3><div class="scroll"><table><tr><th class="l">${tr('TP')}</th>${ids.map(i => `<th>${i}</th>`).join('')}<th>${tr('Terbit')}</th></tr>${rows}</table></div>`;
  }).join('');
  const tps = semuaTP();
  const papan = `<div class="scroll"><table><tr><th class="l">${tr('Siswa')}</th>${tps.map(tp => `<th class="mono">${esc(tp.kode)}</th>`).join('')}</tr>
    <tr><td class="l">${tr('Perangkat ini')}</td>${tps.map(tp => { const h = hitung(tp); return `<td class="cell st${h.s}" title="${tr(STATUS[h.s])}">${h.tier ? 'T' + h.tier : ''}</td>`; }).join('')}</tr></table></div>
    <div class="row" style="font-size:.8rem">${STATUS.map((n, i) => chip(i)).join('')}</div>`;
  const geser = db.opsi.geser || 0;
  return `<div class="stack"><div><div class="eyebrow">${tr('Papan guru')}</div><h1>${tr('Kelengkapan & posisi')}</h1></div>
    <section class="panel stack"><h2>${tr('Kelengkapan tahapan')}</h2><p class="muted" style="margin:0">${tr('✕ = tahapan rangka (S1, S2, S3, S5, S8, S10, S12, S13, S14) belum diunggah. TP dengan ✕ belum boleh terbit.')}</p>${kel}</section>
    <section class="panel stack"><h2>${tr('Papan posisi')}</h2><p class="muted" style="margin:0">${tr('Warna = status, angka = tier. Versi statis hanya membaca progres di perangkat ini. Papan seluruh kelas butuh login dan database (Tahap 6 panduan).')}</p>${papan}</section>
    <section class="panel stack"><h2>${tr('Simulasi waktu')}</h2><p class="muted" style="margin:0">${trf('Untuk uji alur kuis tertunda (H+2) dan pengulangan (H+14). Sekarang digeser %s hari.', geser)}</p>
      <div class="row"><button class="btn ghost" data-geser="2">${tr('+2 hari')}</button><button class="btn ghost" data-geser="14">${tr('+14 hari')}</button><button class="btn ghost" data-geser="0">${tr('Kembali ke hari ini')}</button></div></section></div>`;
}

/* ---------- router ---------- */
let cur = null;
function rangka() {
  document.documentElement.lang = BHS;
  const pasang = (sel, teks) => { const el = document.querySelector(sel); if (el) el.textContent = teks; };
  pasang('#nav-belajar', tr('Belajar'));
  pasang('#nav-guru', tr('Papan Guru'));
  pasang('#lbl-guru', tr('Mode guru'));
  pasang('#kaki', tr('Alur Konten Pembelajaran Tuntas · CMS FIMS · Fitrah Islamic World Academy. Progres tersimpan di perangkat ini.'));
  const merek = document.querySelector('.brand'); if (merek) merek.setAttribute('aria-label', tr('Fisika FIWA — beranda'));
  document.querySelectorAll('[data-bhs]').forEach(b => {
    const on = b.dataset.bhs === BHS;
    b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
}

function render() {
  rangka();
  const h = decodeURIComponent(location.hash.slice(1));
  let html, m; cur = null;
  $('#nav-guru').classList.toggle('on', h === 'guru');
  $('#nav-belajar').classList.toggle('on', h !== 'guru');
  if (h === 'guru') html = halGuru();
  else if ((m = h.match(/^jalur-(.+)$/)) && cariJalur(m[1])) html = halJalur(cariJalur(m[1]));
  else if ((m = h.match(/^topik-(.+)-(l[1-4])$/)) && cariTopik(m[1])) html = halLapis(cariTopik(m[1]), m[2].toUpperCase());
  else if ((m = h.match(/^topik-(.+)$/)) && cariTopik(m[1])) html = halTopik(cariTopik(m[1]));
  else if ((m = h.match(/^tp-(.+)-(s\d+[bc]?)$/)) && cariTP(m[1])) { const id = m[2].toUpperCase().replace(/([BC])$/, c => c.toLowerCase()); cur = { tp: cariTP(m[1]), id }; html = halTP(cur.tp, id); }
  else if ((m = h.match(/^tp-(.+)$/)) && cariTP(m[1])) html = halTP(cariTP(m[1]));
  else html = beranda();
  $('#app').innerHTML = html;
  if (cur && document.getElementById('viewer')) document.getElementById('viewer').scrollIntoView({ block: 'start', behavior: 'smooth' });
  else window.scrollTo(0, 0);
}

function tpDariHash() { const m = location.hash.match(/^#tp-(.+?)(-s\d+[bc]?)?$/); return m ? cariTP(m[1]) : null; }

document.addEventListener('click', ev => {
  const lb = ev.target.closest('[data-bhs]');
  if (lb) { const v = lb.dataset.bhs === 'en' ? 'en' : 'id';
    if (v !== BHS) { BHS = v; db.opsi.bahasa = v; simpan(); render(); } return; }
  const b = ev.target.closest('[data-aksi],[data-geser]'); if (!b) return;
  if (b.dataset.geser != null) { db.opsi.geser = +b.dataset.geser ? (db.opsi.geser || 0) + +b.dataset.geser : 0; simpan(); return render(); }
  const a = b.dataset.aksi, tp = tpDariHash(); if (!tp) return;
  if (a === 'selesai' && cur) catat(tp, cur.id, {});
  if (a === 'skor' && cur) { const v = parseFloat($('#skorIn').value); if (isNaN(v)) return $('#skorIn').focus(); catat(tp, cur.id, { skor: Math.max(0, Math.min(100, v)) }); }
  if (a === 'reset') { delete db.tp[tp.slug]; simpan(); }
  render();
});
document.addEventListener('change', ev => {
  if (ev.target.id === 'tierIn') { const tp = tpDariHash(); if (tp) { prog(tp.slug).tier = +ev.target.value || null; simpan(); render(); } }
  if (ev.target.id === 'modeGuru') { db.opsi.guru = ev.target.checked; simpan(); render(); }
});
// jembatan skor dari halaman HTML tahapan
window.addEventListener('message', ev => {
  const d = ev.data; if (!d || !d.fims || !cur) return;
  const s = T(cur.id);
  if (d.fims === 'skor' && typeof d.skor === 'number' && (s.skor || cur.id === 'S14')) catat(cur.tp, cur.id, { skor: d.skor });
  else if (d.fims === 'selesai' && !s.skor) catat(cur.tp, cur.id, {});
  else return;
  render();
});
window.addEventListener('hashchange', render);

fetch('katalog.json').then(r => r.json()).then(k => {
  K = k; $('#modeGuru').checked = guru(); render();
}).catch(() => { rangka(); $('#app').innerHTML = `<div class="note">${tr('katalog.json belum ada. Jalankan <span class="mono">node build.js</span> (Cloudflare menjalankannya otomatis).')}</div>`; });
})();
