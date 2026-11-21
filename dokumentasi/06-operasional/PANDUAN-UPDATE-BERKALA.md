# Pencatatan update berkala FIWA Physics

Gunakan satu catatan untuk satu perubahan yang dapat dijelaskan dan diperiksa. Catatan dibuat saat ada pekerjaan baru; tidak ada jadwal otomatis yang diaktifkan oleh baseline ini.

## Simpan langsung ke folder proyek

Sesuai instruksi pengguna pada 20 November 2026, setiap berkas yang diubah atau ditambahkan harus langsung tersimpan di `fiwa-physics` pada kategori dan jalur yang tepat. Pengguna tidak perlu mengunduh dokumen dari chat lalu menyalinnya ke proyek. Berkas lama disunting pada lokasinya; berkas baru mengikuti struktur aplikasi yang sudah ada.

Kerangka situs tetap di akar; tampilan, skrip, gambar dan font di `assets/`; konten di `konten/`; bahan ajar di `aset-<topik>/`; media di `media-<topik>/`; layanan di `functions/`; alat dan bank sumber di `alat/`. Dokumentasi update masuk ke kategori `dokumentasi/` dalam tabel di bawah. Catatan hasil pemeriksaan menaut berkas yang benar-benar sudah disimpan.

ZIP atau salinan outputs hanya menjadi tambahan bila diperlukan, bukan lokasi utama hasil. Berkas sementara dan cadangan diletakkan di folder kerja di luar aplikasi. Aturan ini juga tercatat pada `AGENTS.md` di akar `fiwa-physics` untuk pekerjaan berikutnya.

## Nama dan status catatan

Salin `08-template/TEMPLATE-CATATAN-UPDATE.md` ke `04-riwayat/YYYY/MM/YYYY-MM-DD-NN-judul-singkat.md`. Isi tanggal dan waktu WIB, tujuan, sumber, kategori, berkas yang berubah, hasil pemeriksaan dan dampaknya. Nomor NN membedakan beberapa update pada hari yang sama.

Status yang digunakan: **direncanakan**, **dikerjakan**, **tervalidasi lokal**, **diterbitkan**, **dibatalkan**. Gunakan diterbitkan hanya setelah ada bukti deployment. Pisahkan tanggal penyusunan dokumen, tanggal commit dan waktu penerbitan; jangan menyamakan ketiganya.

## Langkah setiap update

1. Baca baseline terbaru, register keputusan dan catatan terakhir yang menyentuh kategori terkait. Catat sumber kanonis yang dipilih. Perbedaan lokal/GitHub pada baseline ini harus diperiksa sebelum menimpa berkas.
2. Buat catatan update dengan ruang lingkup yang diminta. Tulis yang belum diketahui sebagai belum terverifikasi, bukan hasil selesai.
3. Saat implementasi memang diminta pada tugas berikutnya, catat perubahan dan alasan pada kategori terkait. Perubahan alat generator dibedakan dari halaman keluarannya. Katalog yang dihasilkan tidak dijadikan satu-satunya sumber metadata.
4. Rekam pemeriksaan yang relevan di `05-validasi/YYYY/MM/`, menggunakan templat validasi. Hasil uji lama tidak disalin menjadi hasil baru. Jangan menyimpan kata sandi, nilai RAHASIA, kuki sesi, daftar surel atau jawaban murid pada dokumentasi ini.
5. Jika keputusan arsitektur atau aturan produk berubah, buat catatan keputusan di `02-teknis/`, tandai diajukan atau ditetapkan dengan tanggal dan dasar yang nyata. Satu ringkasan dapat menaut ke beberapa bukti kategori.
6. Jika penerbitan termasuk ruang lingkup tugas berikutnya, simpan SHA commit, deployment ID, URL, waktu serta hasil pemeriksaan sesudah terbit di `06-operasional/`. Pencatatan dokumentasi saja tidak menjalankan publikasi.
7. Setelah kondisi akhir diverifikasi, buat baseline baru di `01-baseline/` dengan tanggal baru dan perbarui tautan Mulai membaca pada README dokumentasi. Pertahankan baseline lama sebagai jejak.

## Tempat menyimpan tiap kategori

| Perubahan | Dokumen utama | Tautan pendukung |
| --- | --- | --- |
| Arsitektur, API, akses, skema atau migrasi | `02-teknis/` | `05-validasi/`, `06-operasional/`, catatan update |
| Perilaku fitur dan tampilan | `03-fitur/` | Bukti tampilan dan skenario di `05-validasi/` |
| TP, soal, rubrik, bank dan media | `07-konten-media/` | Sumber, pemeriksaan bank, perubahan katalog |
| Build dan deployment | `06-operasional/` | SHA, deployment ID dan pemeriksaan sesudah terbit |
| Riwayat lintas kategori | `04-riwayat/` | Tautan ke semua catatan kategori yang terkait |
| Masalah yang belum diselesaikan | `09-tindak-lanjut/` | Bukti, dampak, status, langkah berikutnya |

## Penyimpanan bukti

Gunakan jalur relatif antardokumen di dalam folder dokumentasi. Tautan sumber GitHub sebaiknya menunjuk commit yang diperiksa supaya baseline lama tetap dapat ditelusuri. Simpan bukti ringkas yang cukup untuk memeriksa klaim; buku PDF dan salinan penuh kode tidak perlu digandakan di dokumentasi.

Dokumen asli tidak dipindahkan secara otomatis. Bila dokumen baru menggantikan dokumen dokumentasi lama, simpan jejak sesuai aturan `99-arsip/README.md` dan tandai penggantinya. Catatan siswa, log pribadi dan rahasia operasional tetap di penyimpanan yang sesuai, bukan repositori publik.
