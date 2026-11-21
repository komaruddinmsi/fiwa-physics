# Peta fitur FIWA Physics

Keberadaan fitur dibedakan dari kelulusan pengujian produksi. Daftar ini menjadi acuan pemilihan pemeriksaan saat ada update, tanpa mengirim perubahan ke akun atau progres murid.

| Fitur | Cakupan | Status pemeriksaan | Sumber |
| --- | --- | --- | --- |
| Navigasi dan bahasa | Belajar, Papan Guru, ID/EN, kartu jalur | Teramati UI; perubahan bahasa belum diuji menyeluruh | index.html; assets/app.js |
| TKA | F.USE 2 TP; F.MEK 4 TP | Teramati UI dan katalog | katalog.json |
| IGCSE dan AS/A | Kartu tersedia, konten ditandai Segera hadir | Teramati UI; belum ada topik pada katalog | assets/app.js; katalog.json |
| Olimpiade | PRI SMP 6 paket, PRI SMA 6 paket, e-book 3 entri | Teramati UI dan katalog | konten/*/paket; katalog.json |
| Pembuka topik | Fenomena dunia nyata sebelum TP pertama | Teramati pada topik F.USE; berkas kedua topik tersedia | konten/*/pembuka/index.html |
| Alur ketuntasan | Gerbang, rute S2b/S2c, tier, kuis tertunda, pengulangan | Didukung kode; tidak mengerjakan soal produksi | assets/app.js |
| Registrasi dan login | Surel, kata sandi dan persetujuan pemilik | Didukung kode; API siap; tanpa uji registrasi | assets/akun.js; functions/api/[[rute]].js |
| Peran dan mode | Siswa, guru, owner; pilihan mode guru/siswa | Mode guru terlihat; perubahan peran tidak dicoba | assets/akun.js |
| Anggota dan notifikasi | Daftar permintaan dan lonceng bagi owner | Kontrol terlihat; daftar personal tidak dibuka | PANDUAN-AKUN.md; assets/akun.js |
| Pembimbingan | Hubungan guru–murid banyak ke banyak | Didukung API dan panduan; tidak mengubah pasangan | migrasi-bimbing.sql; functions/api/[[rute]].js |
| Penilaian guru | Antrean S8 skor 0–100 dan S12 tier 1–4 | Didukung kode; penyimpanan nilai tidak diuji | functions/api/[[rute]].js |
| Simpan progres | D1 per akun, salinan peramban dan sinkronisasi | Didukung kode; lintas perangkat belum diuji ulang | assets/akun.js |
| Simpan jawaban dokumen | Isian, skor, waktu dan status; kait pemulihan khusus | Didukung kode dan panduan; bukan semua elemen tersimpan otomatis | assets/fims-simpan.js |
| Reset dokumen | Pemilihan murid/topik, pratinjau, alasan dan epoch | Didukung kode dan panduan; tidak dijalankan | PANDUAN-AKUN.md; functions/api/[[rute]].js |
| Media | Video, audio rekaman/TTS, simulasi lokal, bacaan dan tautan | Struktur lolos; semua pemutaran belum diuji | media-f-*/media.json |
| Akses tamu | Penolakan bahan belajar oleh middleware | 401 teramati pada tiga contoh jalur; bukan audit semua jalur | functions/_middleware.js |

Penyimpanan otomatis memerlukan id/name isian yang stabil. `contenteditable`, kanvas dan keadaan yang hanya ada pada variabel JavaScript memerlukan kait khusus. Nilai dokumen paket tidak otomatis menjadi status ketuntasan TP.
