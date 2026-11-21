# Hasil pemeriksaan FIWA Physics

Pemeriksaan tanggal 20 November 2026 dilakukan dengan membaca berkas dan mengakses halaman, tanpa menjalankan pembangun yang menulis ulang sumber atau mengirim operasi perubahan ke produksi.

## Hasil utama

| Pemeriksaan | Hasil | Batas |
| --- | --- | --- |
| Penelusuran sumber lokal | 405 berkas dicatat, termasuk 238 berkas proyek | Cakupan folder CMS FISIKA, bukan seluruh komputer |
| Ekstraksi teks dokumen | Tidak ada kegagalan ekstraksi tingkat berkas | Simbol PDF dan tata letak belum disahkan; buku tidak diaudit seluruh perhitungannya |
| JSON proyek | 18 berkas berhasil diparse | Keterbacaan JSON bukan validasi semua aturan bisnis |
| Katalog | 5 topik; 6 TP × 16 tahapan; 15 paket | Katalog dibaca, tidak dibangun ulang |
| Referensi berkas dalam katalog | Seluruh berkas yang dirujuk katalog tersedia lokal | PDF dalam halaman paket dapat dirujuk di luar metadata katalog |
| Bahan pendukung F.USE | Jenis wajib dan media lokal tersedia; gerbang bersih; pembuka ada | Pemutaran video/suara/simulasi tidak diuji seluruhnya |
| Bahan pendukung F.MEK | Jenis wajib dan media lokal tersedia; gerbang bersih; pembuka ada | Sama seperti di atas |
| Referensi HTML statis lokal | 293 referensi diperiksa; 2 referensi gagal menuju satu PDF yang sama | Tidak mencakup seluruh alamat yang dibangun JavaScript atau tautan eksternal |
| Perbedaan lokasi Halliday | 4 pasangan PDF lokal/GitHub identik isi, berbeda folder | Tidak dipindahkan atau diperbaiki |
| Aset situs dibandingkan sumber | 4 dari 4 berkas yang dipilih cocok byte demi byte | Tidak menetapkan SHA seluruh deployment |
| UI | Beranda, TKA, topik F.USE dan olimpiade memuat isi | Sesi yang sudah login mode guru; tidak menguji login baru |

Dua referensi HTML yang gagal berada pada halaman Halliday dan menunjuk bagian pertama melalui `aset-ebook/`. Bagian 2–4 dipilih melalui data JavaScript; seluruh empat jalur PDF target tersebut tidak ada pada lokasi lokal yang diharapkan, tetapi tersedia di pohon GitHub. Karena itu temuan ini tidak dinyatakan sebagai kerusakan produksi.

## Respons situs tanpa login

| URL | HTTP | Jenis isi | Waktu UTC |
| --- | --- | --- | --- |
| [https://fiwa-physics.pages.dev/](https://fiwa-physics.pages.dev/) | 200 | text/html; charset=utf-8 | 2026-11-20T09:06:09.3663382Z |
| [https://fiwa-physics.pages.dev/assets/app.css](https://fiwa-physics.pages.dev/assets/app.css) | 200 | text/css; charset=utf-8 | 2026-11-20T09:06:09.5064606Z |
| [https://fiwa-physics.pages.dev/assets/app.js](https://fiwa-physics.pages.dev/assets/app.js) | 200 | application/javascript | 2026-11-20T09:06:09.7308505Z |
| [https://fiwa-physics.pages.dev/assets/akun.js](https://fiwa-physics.pages.dev/assets/akun.js) | 200 | application/javascript | 2026-11-20T09:06:09.8640593Z |
| [https://fiwa-physics.pages.dev/katalog.json](https://fiwa-physics.pages.dev/katalog.json) | 401 | application/json; charset=utf-8 | 2026-11-20T09:06:09.9791373Z |
| [https://fiwa-physics.pages.dev/konten/f-use/topik.json](https://fiwa-physics.pages.dev/konten/f-use/topik.json) | 401 | application/json; charset=utf-8 | 2026-11-20T09:06:10.1117260Z |
| [https://fiwa-physics.pages.dev/aset-ebook/modul-praktis-master-fisika.pdf](https://fiwa-physics.pages.dev/aset-ebook/modul-praktis-master-fisika.pdf) | 401 | application/json; charset=utf-8 | 2026-11-20T09:06:10.2614361Z |
| [https://fiwa-physics.pages.dev/api/saya](https://fiwa-physics.pages.dev/api/saya) | 200 | application/json; charset=utf-8 | 2026-11-20T09:06:10.3853456Z |

## Yang belum diuji ulang

Registrasi, kata sandi, persetujuan, pergantian peran, penilaian S8/S12, simpan lintas perangkat, pengatur waktu, reset dan konflik epoch memerlukan skenario uji dengan akun uji serta data yang disepakati. Pemeriksaan baseline ini tidak mengubah data untuk membuktikannya. Semua tautan YouTube, bacaan luar, PhET, ukuran seluler, aksesibilitas dan performa juga belum diaudit menyeluruh.

Daftar pengujian dalam log historis tidak dihitung sebagai hasil uji sesi ini. Pengaturan deployment serta basis data pada dasbor Cloudflare belum diverifikasi.
