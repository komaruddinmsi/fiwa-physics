# Inventaris dokumen FIWA Physics

Inventaris bertanggal 20 November 2026 mencakup seluruh berkas yang ditemukan pada folder `CMS FISIKA` saat pemindaian awal. Cakupan utama ialah `fiwa-physics`; folder sejajar dibedakan sebagai sumber pendukung, bukan dianggap salinan produksi.

## Cakupan dan tingkat penelaahan

405 berkas tercatat: 238 di `fiwa-physics`, 97 di `Piloting-F.USE`, 20 di `Prompt-Generator`, 49 di `vertical-academy-f-use`, dan 1 di `_to_delete`. Label `_to_delete` berasal dari folder yang sudah ada; tidak ada berkas dihapus.

Teks berkas Markdown, HTML, JSON, SQL dan kode diekstrak; seluruh halaman PDF serta isi DOCX/PPTX juga diekstrak tanpa kegagalan ekstraksi tingkat berkas. Ringkasan memusatkan perhatian pada panduan pengembangan, keputusan, struktur fitur, kontrak, log dan dependensi konten. Ekstraksi ribuan halaman buku rujukan bukan audit seluruh soal atau pengesahan ketepatan ilmiah; sebagian simbol PDF dapat kehilangan ketepatan encoding. Tata letak seluruh PDF/DOCX/PPTX tidak diaudit ulang.

Daftar lengkap berada di [INVENTARIS-BERKAS.csv](INVENTARIS-BERKAS.csv); kolomnya memuat kategori, jalur, ukuran, sidik SHA-256, jumlah halaman PDF, tingkat ekstraksi dan kecocokan dengan GitHub. Metadata waktu modifikasi lokal tidak dipakai sebagai tanggal riwayat pengembangan.

## Kategori berkas proyek

| Kategori | Jumlah berkas |
| --- | --- |
| Alat pembangun dan bank soal | 14 |
| Bahan ajar dan asesmen | 23 |
| Basis data dan migrasi | 5 |
| Buku rujukan | 6 |
| Kerangka situs dan katalog | 3 |
| Konten pembelajaran dan metadata | 137 |
| Layanan akun dan akses | 2 |
| Media pendukung dan metadata | 23 |
| Mesin tampilan dan identitas | 12 |
| Panduan pengembangan dan operasional | 8 |
| Pegangan guru dan RPP | 5 |

## Delapan panduan proyek

| Sumber | Ringkasan relevan |
| --- | --- |
| [README.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/README.md) | Orientasi situs, struktur konten, build katalog dan pelaporan skor. Sebagian penjelasan penyimpanan serta jumlah tahapan sudah tertinggal dari implementasi. |
| [PANDUAN-AKUN.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/PANDUAN-AKUN.md) | Pemasangan D1 dan pengikat DB, rahasia sesi, peran, persetujuan, pembimbingan, nilai S8/S12, penyimpanan lembar dan reset berbasis epoch. Bagian awal masih menggambarkan login tanpa kata sandi. |
| [PANDUAN-TOPIK-BARU.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/PANDUAN-TOPIK-BARU.md) | Dua jenis topik, struktur 16 tahapan dan L1–L4, pembuka, metadata, pemisahan bank, media wajib, simpan lembar, e-book dan validasi. Beberapa pernyataan akses perlu rekonsiliasi. |
| [alat/BACA-DULU.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/alat/BACA-DULU.md) | Sumber generator halaman dan bank; keluaran generator dapat tertimpa saat dibangun ulang. Memuat rujukan alat pembuat bacaan, pemeriksa media dan pemecah PDF. |
| [media-f-use/PANDUAN-MEDIA.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/media-f-use/PANDUAN-MEDIA.md) | Skema TP/tahapan/daftar bahan; video, audio, simulasi, bacaan dan tautan; pengosongan bahan bantu pada S2/S8/S13. |
| [media-f-mek/PANDUAN-MEDIA.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/media-f-mek/PANDUAN-MEDIA.md) | Panduan media untuk F.MEK, tetapi beberapa daftar dan istilah masih tersalin dari F.USE; gunakan media.json aktual sebagai bukti keadaan berkas. |
| [media-f-use/audio/README.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/media-f-use/audio/README.md) | Panduan mengganti naskah suara peramban dengan MP3/OGG dan penamaan berkas. |
| [media-f-mek/audio/README.md](https://github.com/komaruddinmsi/fiwa-physics/blob/a6794d774bb88ca39a97199711448254b678b553/media-f-mek/audio/README.md) | Panduan rekaman; contoh jalurnya masih menunjuk media-f-use dan perlu disesuaikan pada pembaruan dokumentasi berikutnya. |

## Dokumen PDF dan Word di dalam proyek

| Jalur relatif proyek | Halaman PDF | Peran dokumen |
| --- | --- | --- |
| alat/fundamentals-of-physics-halliday-1.pdf | 282 | Bagian buku Fundamentals of Physics; tersimpan di alat secara lokal, konten identik dengan bagian pada aset-ebook di GitHub. |
| alat/fundamentals-of-physics-halliday-2.pdf | 352 | Bagian buku Fundamentals of Physics; tersimpan di alat secara lokal, konten identik dengan bagian pada aset-ebook di GitHub. |
| alat/fundamentals-of-physics-halliday-3.pdf | 401 | Bagian buku Fundamentals of Physics; tersimpan di alat secara lokal, konten identik dengan bagian pada aset-ebook di GitHub. |
| alat/fundamentals-of-physics-halliday-4.pdf | 415 | Bagian buku Fundamentals of Physics; tersimpan di alat secara lokal, konten identik dengan bagian pada aset-ebook di GitHub. |
| aset-ebook/introduction-to-classical-mechanics-morin.pdf | 623 | Buku rujukan mekanika klasik untuk kumpulan e-book olimpiade. |
| aset-ebook/modul-praktis-master-fisika.pdf | 401 | Buku rujukan latihan fisika dalam kumpulan e-book. |
| aset-f-mek/GURU_RPP-F.MEK.docx | DOCX, tidak dihitung | RPP Mekanika F.MEK: empat TP, urutan ajar, gerbang kelas, rubrik dan sumber. Bukan spesifikasi penerbitan web. |
| aset-f-mek/S01-S02b_Lembar-Bekal-F.MEK.1-pra.pdf | 3 | Lembar bekal prasyarat TP; bahan pendukung S1 dan penguatan. |
| aset-f-mek/S01-S02b_Lembar-Bekal-F.MEK.1a.pdf | 3 | Lembar bekal prasyarat TP; bahan pendukung S1 dan penguatan. |
| aset-f-mek/S01-S02b_Lembar-Bekal-F.MEK.1b.pdf | 3 | Lembar bekal prasyarat TP; bahan pendukung S1 dan penguatan. |
| aset-f-mek/S01-S02b_Lembar-Bekal-F.MEK.2.pdf | 3 | Lembar bekal prasyarat TP; bahan pendukung S1 dan penguatan. |
| aset-f-mek/S04_Modul-Konsep-F.MEK.1-pra.pdf | 16 | Modul konsep TP untuk tahapan S4. |
| aset-f-mek/S04_Modul-Konsep-F.MEK.1a.pdf | 16 | Modul konsep TP untuk tahapan S4. |
| aset-f-mek/S04_Modul-Konsep-F.MEK.1b.pdf | 16 | Modul konsep TP untuk tahapan S4. |
| aset-f-mek/S04_Modul-Konsep-F.MEK.2.pdf | 16 | Modul konsep TP untuk tahapan S4. |
| aset-f-use/S01-S02b_Lembar-Bekal-F.USE.1-pra.pdf | 3 | Lembar bekal prasyarat TP; bahan pendukung S1 dan penguatan. |
| aset-f-use/S01-S02b_Lembar-Bekal-F.USE.1.pdf | 4 | Lembar bekal prasyarat TP; bahan pendukung S1 dan penguatan. |
| aset-f-use/S04_Modul-Konsep-F.USE.1-pra.pdf | 18 | Modul konsep TP untuk tahapan S4. |
| aset-f-use/S04_Modul-Konsep-F.USE.1.pdf | 19 | Modul konsep TP untuk tahapan S4. |
| aset-f-use/S05-S10_Dek-Kelas-F.USE.1-pra.pdf | 34 | Dek kelas PDF; soal Gerbang Formatif dipisahkan pada riwayat 18 November. |
| aset-f-use/S05-S10_Dek-Kelas-F.USE.1.pdf | 34 | Dek kelas PDF; soal Gerbang Formatif dipisahkan pada riwayat 18 November. |
| aset-f-use/S08_Papan-Mini-F.USE.1-pra.pdf | 4 | Papan mini soal Gerbang Formatif Kelas S8. |
| aset-f-use/S08_Papan-Mini-F.USE.1.pdf | 4 | Papan mini soal Gerbang Formatif Kelas S8. |

## Sumber pendukung dalam folder induk

`Prompt-Generator` berisi 20 dokumen: dua kontrak bahasa, indeks keluarga prompt dan generator RPP, prasyarat, pemantik, modul, dek, LKPD kelas, tier, worksheet rumah, gerbang, asesmen lapis topik, pengulangan dan manifes. Dokumen generator diperlakukan sebagai spesifikasi sumber, bukan instruksi untuk menjalankan atau menerbitkan perubahan pada tugas ini.

`Piloting-F.USE` menyediakan peta awal, rencana media, catatan guru, sebelas log tinjauan, bahan ajar dan manifes. Pernyataan hasil uji di log adalah hasil historis penulisnya; pemeriksaan ini tidak mengulangi seluruh uji tersebut. `vertical-academy-f-use/PASANG.md` mengarah ke proyek Vertical Academy terdahulu; pengaturannya tidak boleh disalin sebagai fakta konfigurasi Cloudflare FIWA saat ini.

| Jalur dari CMS FISIKA | Judul dalam dokumen | Kategori |
| --- | --- | --- |
| Piloting-F.USE/00_PETA-PILOTING-F.USE.md | PETA PILOTING — UNIT F.USE | Bahan dan rencana piloting |
| Piloting-F.USE/01_RENCANA-MEDIA-DAN-ALAT-F.USE.md | RENCANA MEDIA DAN ALAT — UNIT F.USE | Bahan dan rencana piloting |
| Piloting-F.USE/GURU_Dek-Catatan-F.USE.md | BERKAS INI UNTUK GURU. JANGAN DIBAGIKAN, DITAUTKAN, ATAU DIUNGGAH KE TEMPAT YANG BISA DIAKSES MURID. | Pegangan guru piloting |
| Piloting-F.USE/LOG_DEK.md | LOG_DEK — Dek Kelas F.USE (S5 · S6 · S8 · S10) | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_L01-L03-L04.md | LOG TINJAUAN — Asesmen Lapis Topik F.USE · L1 · L3 · L4 | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_LAT-CBT.md | Log Tinjauan — LAT Latihan TKA & CBT Ujian Latihan · Unit F.USE | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S02.md | LOG TINJAUAN — Tahapan S02 · Gerbang Prasyarat · Unit F.USE | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S03.md | LOG TINJAUAN — Tahapan S03 · Pemantik dan Panen Prakonsepsi · Unit F.USE | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S07-TP1.md | LOG TINJAUAN — S7 Praktik Terstruktur · TP1 `F.USE.1-pra` | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S07-TP2.md | Log Tinjauan — S7 Praktik Terstruktur · TP2 F.USE.1 | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S09-S10.md | Log Tinjauan — Tahapan S9 (Kartu Tier) dan S10 (Konsolidasi & Jangkar) · Unit F.USE | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S11.md | LOG S11 · Latihan Bertingkat — F.USE.1-pra dan F.USE.1 | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S12-L02.md | Log Tinjauan — S12 Tugas Kinerja (dua TP) dan L2 Muara Topik · Unit F.USE | Riwayat dan tinjauan piloting |
| Piloting-F.USE/LOG_S13-S14.md | Log Tinjauan — S13 Gerbang Ketuntasan & S14 Latihan Selang-Seling · Unit F.USE | Riwayat dan tinjauan piloting |
| Prompt-Generator/00._KONTRAK-TAHAPAN-KETUNTASAN-IDN.md | KONTRAK TAHAPAN KETUNTASAN · v1 — berkas acuan bersama seluruh generator | Kontrak dan generator konten |
| Prompt-Generator/00._MASTERY-STAGE-CONTRACT-EN.md | MASTERY STAGE CONTRACT · v1 — the shared reference file for every generator | Kontrak dan generator konten |
| Prompt-Generator/01._PROMPT-Generator-Lesson-Plan-ENG.md | Prompt: rubric-based deep-learning lesson plan generator, v3 (English output) | Kontrak dan generator konten |
| Prompt-Generator/01._PROMPT-Generator-RPP-IND.md | PROMPT — GENERATOR RPP PEMBELAJARAN MENDALAM BERBASIS RUBRIK · v3 | Kontrak dan generator konten |
| Prompt-Generator/02._PROMPT-Generator-Materi-Prasyarat-IDN.md | PROMPT — GENERATOR LEMBAR BEKAL PRA-SYARAT (LaTeX) · v1 | Kontrak dan generator konten |
| Prompt-Generator/02._PROMPT-Generator-Prerequisite-Sheet-EN-v1.md | Prompt: prerequisite sheet generator (LaTeX), v1 (English output) | Kontrak dan generator konten |
| Prompt-Generator/03._PROMPT-Generator-Uji-Prasyarat-IDN.md | PROMPT — GENERATOR UJI PRASYARAT · TAHAPAN S2 · v1 | Kontrak dan generator konten |
| Prompt-Generator/04._PROMPT-Generator-Pemantik-Prakonsepsi-IDN.md | PROMPT — GENERATOR LEMBAR PEMANTIK & PANEN PRAKONSEPSI · TAHAPAN S3 · v1 | Kontrak dan generator konten |
| Prompt-Generator/05._PROMPT-Concept-Module_ENG.md | PROMPT · CONCEPT MODULE FROM A LESSON PLAN (v2, English output) | Kontrak dan generator konten |
| Prompt-Generator/05._PROMPT-Modul-Konsep-Belajar_IDN.md | PROMPT · MODUL KONSEP DARI LESSON PLAN (v2) | Kontrak dan generator konten |
| Prompt-Generator/06._PROMPT-Generator-PPT-Kelas.md | PROMPT — GENERATOR PPT KELAS SIAP TAYANG · v1 | Kontrak dan generator konten |
| Prompt-Generator/06b._PROMPT-Generator-LKPD-KBM-IDN.md | PROMPT — GENERATOR LKPD KBM · PRAKTIK TERSTRUKTUR · v1 | Kontrak dan generator konten |
| Prompt-Generator/07._PROMPT-Generator-Kartu-Tier-dan-Tugas-Kinerja-IDN.md | PROMPT — GENERATOR KARTU TIER DAN TUGAS KINERJA · v1 | Kontrak dan generator konten |
| Prompt-Generator/08._PROMPT-Generator-Worksheet-LKPD-ENG.md | Prompt: HTML worksheet generator, v2 (English output) | Kontrak dan generator konten |
| Prompt-Generator/08._PROMPT-Generator-Worksheet-LKPD-IND.md | PROMPT — GENERATOR WORKSHEET LKPD HTML · v2 | Kontrak dan generator konten |
| Prompt-Generator/09._PROMPT-Generator-Gerbang-Ketuntasan-IDN.md | PROMPT — GENERATOR GERBANG KETUNTASAN TP · v1 | Kontrak dan generator konten |
| Prompt-Generator/10._PROMPT-Generator-Asesmen-Lapis-Topik-IDN.md | PROMPT — GENERATOR ASESMEN LAPIS TOPIK DAN FAQ TOPIK · v1 | Kontrak dan generator konten |
| Prompt-Generator/11._PROMPT-Generator-Latihan-Selang-Seling-IDN.md | PROMPT — GENERATOR LATIHAN SELANG-SELING TERJADWAL (PENGULANGAN BERJARAK) · v1 | Kontrak dan generator konten |
| Prompt-Generator/12._PROMPT-Generator-Manifes-Konten-CMS-IDN.md | PROMPT — GENERATOR MANIFES KONTEN CMS · v1 | Kontrak dan generator konten |
| Prompt-Generator/README-Keluarga-Prompt.md | Keluarga Prompt Generator CMS FIMS — indeks dan urutan pakai | Kontrak dan generator konten |
| vertical-academy-f-use/PASANG.md | PASANG — unit F.USE ke Vertical Academy | Paket integrasi terdahulu |

## Batas sumber

Percakapan rujukan hanya memuat satu permintaan pengguna dan tidak memiliki lampiran atau jawaban kajian. Sejumlah log menyebut `RPP.txt`, `BRIEF.md`, `Modul-TP1.txt` dan `Modul-TP2.txt`; nama persis itu tidak ditemukan pada pemindaian folder ini. Dokumen PDF modul dan RPP F.MEK tetap tersedia sebagaimana terdaftar di atas. Ketiadaan sumber tersebut tidak diisi dengan perkiraan isi.
