# Physics FIWA

Situs pembelajaran tuntas fisika untuk Fitrah Islamic World Academy. Alur siswa memakai P1–P10, dengan L1–L4 sebagai kegiatan lintas-TP. Physics TKA saat ini mencakup F.MEK (empat TP) dan F.USE (dua TP).

## Sebelum mengubah materi

Baca [AGENTS.md](AGENTS.md), [STANDAR-KONTEN-FISIKA.md](STANDAR-KONTEN-FISIKA.md), dan [PANDUAN-TOPIK-BARU.md](PANDUAN-TOPIK-BARU.md). Aturan berlaku untuk seluruh materi sekarang dan topik baru, termasuk jika dikerjakan AI lain. Setiap konsep esensial memerlukan visual interaktif, penjelasan model, contoh bertahap, miskonsepsi dan checkpoint.

## Berkas utama

| Lokasi | Fungsi |
| --- | --- |
| `index.html`, `assets/app.js` | Kerangka, panel kiri dan progres. |
| `assets/kelas-visual.js` | Tiga belas model fisika, SVG, kontrol dan batang energi. |
| `assets/kelas-konten.js`, `kelas-konten.css` | Materi interaktif, penilaian, waktu dan pemulihan isian. |
| `alat/bank/lesson_*.py` | Sumber isi enam TP dan bank soal. |
| `alat/konten_interaktif.py` | Membuat halaman P, bacaan, pembuka topik dan L1–L4. |
| `konten/<topik>/<tp>/P*` | Halaman aktif edisi 4. |
| `media-<topik>/media.json` | Video, narasi, simulasi dan bacaan pendukung. |
| `functions/` | Layanan akun, isian, progres dan penilaian guru. |
| `dokumentasi/` | Inventaris, keputusan, riwayat, validasi dan panduan unggah. |

## Membangun dan memeriksa

Jalankan dari akar proyek, menggunakan Python 3 dan Node 24+ (pengujian server memakai SQLite sementara di memori):

```text
node build.js
python alat/konten_interaktif.py
node build.js
python alat/periksa-standar-konten.py
node alat/uji-model-fisika.cjs
node alat/uji-animasi.cjs
node alat/uji-suara.cjs
node alat/uji-kasus-unik.cjs
python alat/periksa-pengulangan.py
node alat/uji-gating-unit.cjs
node alat/uji-kelas-konten.cjs
node alat/uji-alur-p.cjs
node alat/uji-teman-belajar.cjs
node alat/uji-konten-bersih.cjs
python alat/periksa-paket-upload.py
```

`alat/alur_p.py` tetap tersedia sebagai pintu masuk kompatibel ke generator edisi 4. HTML S dan L lama yang sudah digantikan telah dikeluarkan dari konten. Tautan lama dialihkan ke halaman aktif melalui functions/_middleware.js. Kunci S pada progres/API tetap dipakai. Jangan menghapus progres lama atau mengembalikan S10 sebagai tahap wajib.

## Penilaian dan penyimpanan

Isian disimpan per akun melalui layanan lembar. Progres lokal memakai kunci `va-fims-v1` dan diselaraskan ke akun. P5 memuat tiga gerbang inti RPP per TP, muncul satu per satu. Guru pembimbing memberi respon T1–T4 di Papan Guru; T3/T4 membuka soal selanjutnya. Nilai dan urutan dimiliki server. Latihan Unit Test dan Unit Test masing-masing 25 nomor per topik; seluruh latihan harus dikirim sebelum Unit Test dapat diambil dari server. P7 tepat sepuluh soal. P9 memiliki empat bentuk dan memakai jeda serta syarat P8. P10 memakai tiga sesi berjarak. Bentuk yang berputar bukan bank soal tanpa batas.

Pemeriksaan jawaban P9 di peramban menyimpan hash, tetapi pembatasan alur dan hash bukan pengamanan ujian berisiko tinggi. Sumber generator berisi kunci dan rumus; repositori publik tidak dapat dijadikan tempat rahasia guru. Data pribadi, kredensial dan kunci rahasia ujian tidak boleh ditambahkan ke repositori.

## Pembaruan lokal

Simpan setiap hasil langsung di kategori proyek yang sesuai. Catatan terbaru dan daftar jalur unggah tersedia di `dokumentasi/06-operasional/2026/11/`. Penyimpanan lokal tidak berarti commit, push atau penerbitan. Versi 21 November 2026 ini belum diterbitkan.

Untuk unggah ulang lengkap per folder, gunakan panduan dokumentasi/06-operasional/2026/11/2026-11-21-BERKAS-UPDATE-GITHUB.md dan MANIFEST-UPLOAD-PER-FOLDER.csv. PDF Halliday berada di aset-ebook/, RPP sumber berada di aset-f-mek/ dan aset-f-use/, dan bahan versi lama yang tidak dirujuk sudah dikeluarkan.

Standar terbaru dan asal adaptasi: `STANDAR-KONTEN-FISIKA.md` dan `dokumentasi/07-konten-media/SUMBER-DAN-ADAPTASI-V4.json`. Bank Unit Test versi 4 mengubah konteks/redaksi pasangan dengan data numerik tetap. Pembahasan CBT lama tidak disalin ketika datanya berbeda.

Versi 4.1 memperbaiki tanda lereng pada gerak energi, menempatkan kontrol sebelum diagram, memulihkan dependensi pada halaman utama lama, membedakan kegiatan antartahap dan menyesuaikan bunyi referensi Chemistry. Sumber kasus baru: alat/bank/kegiatan_unik.py. Uji kasus memerlukan Python pada PATH; FIWA_PYTHON dapat menunjuk executable Python bila diperlukan. Daftar unggah khusus: dokumentasi/06-operasional/2026/11/2026-11-21-OPENING-SUARA-BERKAS.csv.

Versi 4.2 menambahkan maskot pembuka tahap dengan bendera logo asli dan tombol menyembunyikan seluruh panel tahapan. Pilihan panel tersimpan di peramban; isian aktif tetap hidup saat panel dilipat. Jalankan `node alat/uji-teman-belajar.cjs`. Gunakan daftar unggah gabungan terbaru di `dokumentasi/06-operasional/2026/11/2026-11-21-BERKAS-UPDATE-GITHUB.md`; daftar khusus 4.1 adalah riwayat dan belum mencakup fitur 4.2.
