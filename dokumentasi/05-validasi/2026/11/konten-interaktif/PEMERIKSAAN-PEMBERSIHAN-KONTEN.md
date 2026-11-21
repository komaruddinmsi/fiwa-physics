# Pemeriksaan pembersihan folder konten

Tanggal 21 November 2026. 106 HTML lama dikeluarkan; 171 HTML dan 14 metadata JSON tetap ada di konten. Seluruh 162 halaman keluaran edisi 3, metadata, entri katalog aktif dan API nilai/isian identik dengan sebelum pembersihan.

Build katalog, pemeriksaan standar, 2.615 pemeriksaan model fisika, delapan skenario runtime, 27 skenario alur serta pemeriksaan media F.MEK/F.USE lulus. Uji middleware memeriksa tautan lama beserta variasi index/slash, rute aktif yang tidak boleh dialihkan dan penolakan akses tanpa sesi ke materi aktif. Log aktual ada pada hasil-pembersihan-konten.txt.

Pengalihan diuji melalui objek HTTP dan middleware asli secara lokal, belum melalui deployment Cloudflare. Tidak ada pengujian atau perubahan akun produksi, serta tidak ada penerbitan. Tautan lama menuju halaman baru tidak memindahkan jawaban historis ke formulir baru; HTML asli tersedia pada cadangan di luar proyek.
