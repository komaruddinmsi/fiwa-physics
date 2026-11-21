# Menambahkan topik Physics FIWA

Standar wajib berada di [STANDAR-KONTEN-FISIKA.md](STANDAR-KONTEN-FISIKA.md). Panduan ini menggantikan panduan struktur S1–S14. Salinan panduan yang tidak berlaku sudah dikeluarkan dari proyek saat pembersihan 21 November 2026.

## Topik pembelajaran penuh

1. Baca standar, metadata, kurikulum/RPP yang tersedia, dan sumber fisika primer. Tetapkan TP serta indikator sebelum menulis halaman.
2. Buat `konten/<topik>/topik.json` dan `konten/<topik>/<slug-tp>/tp.json`. Pertahankan format metadata dari F.MEK/F.USE, termasuk kode, urutan ajar, Bloom dan ambang.
3. Tambahkan `alat/bank/lesson_<nama>.py` yang mengekspor `LESSONS` dan `make_questions(slug, stage, form=1)`. Ikuti skema sumber yang ada; jangan menyalin fenomena atau soal dengan sekadar mengganti judul.
4. Isi hook TP, tujuan, prediksi, konsep, tugas penerapan dan rubrik. Setiap konsep mempunyai penjelasan utuh, besaran/satuan, asumsi, lab yang dapat diubah, kegiatan prediksi–amati–jelaskan, miskonsepsi, contoh bertahap dan checkpoint.
5. Tambahkan hook topik ke `TOPICS` di `alat/konten_interaktif.py`, lengkap dengan model visual dan transisi menuju TP. Jika model yang diperlukan belum tersedia, implementasikan dan uji; jangan menggantinya dengan diagram dekoratif.
6. Isi bank: P2 delapan soal bekal; P5 gerbang inti dari RPP yang muncul satu per satu, wajib respon T3/T4 guru untuk lanjut; P7 tepat sepuluh soal; P9 delapan soal pada konteks baru dalam empat bentuk; P10 empat soal per sesi. P6 mengambil dua/tiga soal menurut cabang dan indikator. Bila lingkup baru menuntut jumlah selain pola ini, ubah kontrak generator, tampilan waktu dan pemeriksaan secara selaras sambil mempertahankan ketentuan pengguna untuk P6/P7.
7. Tambahkan video/audio/simulasi/bacaan yang relevan pada `media-<topik>/media.json`. Kunci tahap S pada peta media dan penyimpanan adalah kompatibilitas; label siswa memakai P. Materi bantu tidak muncul pada P2/P5/P9.
8. Jalankan rangkaian build dan pemeriksaan di README. Generator berhenti jika TP belum mempunyai sumber. Periksa lagi bahwa semua tahap katalog menunjuk edisi yang baru.
9. Periksa di peramban: variabel, keadaan batas, ketepatan diagram, isian, penilaian, pemulihan, layar kecil, Terang/Teduh dan bunyi opsional. Simpan hasil aktual di `dokumentasi/05-validasi/`.
10. Catat perubahan dan jalur berkas unggah di kategori dokumentasi. Jangan menerbitkan tanpa instruksi yang mengizinkannya.

## Susunan hasil

```text
konten/<topik>/pembuka/index.html
konten/<topik>/<tp>/tp.json
konten/<topik>/<tp>/P1/index.html
konten/<topik>/<tp>/P2/index.html
konten/<topik>/<tp>/P2a/index.html dan P2b/index.html
konten/<topik>/<tp>/P3/index.html
konten/<topik>/<tp>/P4/index.html
konten/<topik>/<tp>/P4/diskusi.html, contoh.html, praktik.html
konten/<topik>/<tp>/P5/index.html (soal aktif diambil dari server)
konten/<topik>/<tp>/P6a/index.html dan P6b/index.html
konten/<topik>/<tp>/P7/index.html
konten/<topik>/<tp>/P8/index.html
konten/<topik>/<tp>/P9/form-1.html sampai form-4.html
konten/<topik>/<tp>/P10/sesi-1.html sampai sesi-3.html
konten/<topik>/L1 sampai L4/interaktif.html
konten/<topik>/L3/latihan-interaktif.html
```

Katalog memetakan P ke kunci status lama untuk mempertahankan hasil siswa. HTML S lama yang sudah tergantikan tidak lagi disertakan dalam konten; kode status S tetap dipakai dalam progres/API. S10 tidak kembali sebagai tahap wajib. Untuk topik baru, `build.js` mengenali halaman P tanpa harus membuat salinan S.

## Topik paket

Paket dokumen lepas tetap memakai `topik.json` dengan `"jenis":"paket"`, folder `paket/`, dan `paket.json`. Paket tidak otomatis menjadi alur P1–P10. Perubahan paket perlu ruang lingkup tersendiri.

Versi 4: lengkapi metadata alignment, provider P7/P9, kontrak gating RPP dan pasangan Unit Test melalui `alat/revisi_rpp.py` serta `alat/bank/`. Gunakan tujuh langkah pembahasan kanonis. Bahan pendukung hanya jika diperlukan, tidak perlu empat jenis di setiap tahap. Prasyarat mudah 30–60 detik. Simulasi wajib Play/Pause/Stop/Reset.
