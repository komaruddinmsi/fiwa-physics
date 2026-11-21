# Register keputusan teknis FIWA Physics

Register ini merangkum pilihan yang sudah tersurat dalam sumber atau terlihat pada implementasi per 20 November 2026. Nomor KT adalah indeks dokumentasi baru, bukan nomor keputusan historis. Tanggal penetapan tidak direkonstruksi bila sumber tidak mencantumkannya; tidak ada keputusan arsitektur baru yang diterapkan.

| ID | Pilihan yang tercatat | Makna untuk update | Status bukti | Sumber relatif |
| --- | --- | --- | --- | --- |
| KT-01 | Konten mengikuti struktur folder | Topik, TP, tahapan, pembuka dan paket ditemukan dari berkas; katalog dihasilkan build.js. | Didukung kode | build.js; PANDUAN-TOPIK-BARU.md |
| KT-02 | Dua jenis topik | Alur memiliki tahapan; paket berisi dokumen lepas tanpa progres tahapan TP. | Didukung katalog dan kode | katalog.json; build.js |
| KT-03 | Enam belas tahapan per TP | S2b dan S2c dihitung tersendiri; lapis L1–L4 berada di tingkat topik. | Didukung katalog; README menyebut 18 secara tidak konsisten | katalog.json; README.md |
| KT-04 | Urutan ajar terpisah dari nama berkas | Gunakan urutan_ajar; F.MEK memakai 1-pra, 2, 1a, 1b. | Didukung metadata | konten/*/*/tp.json |
| KT-05 | Pemisahan latihan dan gerbang | Konten latihan tidak dipakai sebagai butir gerbang yang sudah dikenal; kontrak membedakan latihan, gerbang dan kuis-tertunda. | Tercatat kontrak; cakupan semua soal belum diaudit ulang | Prompt-Generator/00._KONTRAK-TAHAPAN-KETUNTASAN-IDN.md |
| KT-06 | Ketuntasan membutuhkan bukti ganda | S13 lulus dan tier tugas kinerja sekurangnya T3; status dan tier dipisahkan. Kode juga mensyaratkan rantai S2/S4/S8/S11. | Didukung sumber dan kode; agregasi per-proses perlu ditelaah | assets/app.js fungsi hitungP dan hitung; PANDUAN-TOPIK-BARU.md |
| KT-07 | Bahan bantu tidak berada di gerbang | S2, S8 dan S13 tidak diberi media bantu; setiap TP dan pembuka memiliki media pendukung. | Pemeriksaan struktur lulus pada dua topik | media-f-use/media.json; media-f-mek/media.json |
| KT-08 | Dokumen ditanam di halaman | HTML/PDF dibuka dalam iframe dengan pilihan tab penuh; PDF menyediakan unduhan. | Tercatat panduan dan didukung kode; semua bingkai belum diuji | PANDUAN-TOPIK-BARU.md; assets/app.js |
| KT-09 | Kendali akun di layanan server | Peran siswa/guru/owner, persetujuan dan pengikat DB/RAHASIA pada Cloudflare Functions. | Didukung kode; API publik memberi siap=true | functions/api/[[rute]].js; PANDUAN-AKUN.md |
| KT-10 | Kata sandi menjadi alur masuk saat ini | Login memerlukan surel dan kata sandi; turunan PBKDF2-SHA256 disimpan, bukan sandi asli. | Didukung kode; panduan awal belum selaras | assets/akun.js; functions/api/[[rute]].js; migrasi-sandi.sql |
| KT-11 | Progres dan jawaban mengikuti akun | progres dan lembar berada di D1; penyimpanan lokal menjadi salinan, bukan satu-satunya sumber. | Didukung kode; uji lintas perangkat belum diulang | assets/akun.js; assets/fims-simpan.js; skema.sql |
| KT-12 | Pembimbing menentukan cakupan guru | Owner mengelola hubungan banyak guru/banyak murid; guru menangani murid bimbingannya. | Tercatat 19 November pada panduan dan didukung API | PANDUAN-AKUN.md; migrasi-bimbing.sql |
| KT-13 | Reset memakai nomor generasi | epoch dinaikkan server saat menilai/reset; salinan lama ditolak. Panduan menyebut cek progres 30 detik dan lembar 45 detik. | Didukung kode; perilaku produksi belum diuji tulis | assets/akun.js; assets/fims-simpan.js; functions/api/[[rute]].js |
| KT-14 | Sumber generator dipisah dari keluarannya | Bank dan alat menghasilkan konten; sunting sumber sebelum regenerasi agar perubahan tidak tertimpa. | Tercatat alat/BACA-DULU.md; generator tidak dijalankan | alat/BACA-DULU.md; alat/bangun.py |
| KT-15 | PDF buku dipecah per bagian | Halliday berjumlah 1.450 halaman dalam empat PDF; buku tetap satu entri paket. | Didukung berkas lokal dan metadata buku | alat/pecah-pdf.py; alat/ebook.py; konten/kumpulan-ebook/paket/paket.json |
| KT-16 | Istilah murid diseragamkan | Panduan terbaru memakai Peta & Tujuan Pembelajaran dan prediksi; kontrak/piloting lama masih memakai istilah sebelumnya. | Tercatat panduan; penyelarasan lintas sumber belum dilakukan | PANDUAN-TOPIK-BARU.md bagian 10 |

## Hal yang belum diputuskan

Penyelarasan panduan lama, metode perlindungan bahan guru pada repositori publik, hubungan nilai tier tunggal dengan profil per-proses, dan sumber kanonis salinan lokal/GitHub masih memerlukan kajian. Catatan itu bukan izin untuk mengganti sistem atau mengubah akses pada tugas ini.
