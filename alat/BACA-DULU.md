# Alat pembangun dan pemeriksaan Physics FIWA

Sumber aktif materi ada pada bank/lesson_*.py. Metadata topik dan TP berada pada konten/<topik>/topik.json serta tp.json. Baca ../STANDAR-KONTEN-FISIKA.md dan ../PANDUAN-TOPIK-BARU.md sebelum menambah isi.

Jalankan dari akar proyek:

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
python alat/periksa-media.py f-mek
python alat/periksa-media.py f-use
```

alur_p.py adalah pintu masuk kompatibel ke generator aktif. konten_interaktif.py membangun seluruh P1–P10, bacaan interaktif, pembuka serta L1–L4. Jangan membuat kembali generator S lama atau memakai bank lama.

ebook.py dan pecah-pdf.py tetap untuk topik buku yang terpisah. PDF Halliday disimpan di aset-ebook/ sesuai tautan situs. RPP sumber kurikulum ada di aset-f-mek/GURU_RPP-F.MEK.docx dan aset-f-use/GURU_RPP-F.USE.docx; worksheet sumber versi lama sudah dikeluarkan. Tidak ada alat yang perlu dijalankan untuk menghapus progres atau jawaban siswa.

Periksa seluruh paket sebelum unggah dengan python alat/periksa-paket-upload.py. Cadangan dan berkas sementara disimpan di luar fiwa-physics.

Versi 4 menggunakan revisi_rpp.py dan alignment_*.py untuk materi dan soal P7/P9. gating_contract.json/unit_contract.json dihasilkan dari metadata RPP dan unit_practice.json; jangan menyunting salinan kontrak di Functions tanpa memperbarui generator. Pengujian server memakai Node 24+ dan SQLite dalam memori.

Versi 4.1 memperbaiki tanda lereng pada gerak energi, menempatkan kontrol sebelum diagram, memulihkan dependensi pada halaman utama lama, membedakan kegiatan antartahap dan menyesuaikan bunyi referensi Chemistry. Sumber kasus baru: alat/bank/kegiatan_unik.py. Uji kasus memerlukan Python pada PATH; FIWA_PYTHON dapat menunjuk executable Python bila diperlukan. Daftar unggah khusus: dokumentasi/06-operasional/2026/11/2026-11-21-OPENING-SUARA-BERKAS.csv.

Versi 4.2 menambahkan maskot pembuka tahap dengan bendera logo asli dan tombol menyembunyikan seluruh panel tahapan. Pilihan panel tersimpan di peramban; isian aktif tetap hidup saat panel dilipat. Jalankan `node alat/uji-teman-belajar.cjs`. Gunakan daftar unggah gabungan terbaru di `dokumentasi/06-operasional/2026/11/2026-11-21-BERKAS-UPDATE-GITHUB.md`; daftar khusus 4.1 adalah riwayat dan belum mencakup fitur 4.2.
