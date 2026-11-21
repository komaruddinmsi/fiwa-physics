# Kompatibilitas materi interaktif dan progres

Edisi 3 memakai P pada antarmuka dan mempertahankan kunci lama pada progres serta API: P1=S1, P2=S2, P2a=S2b, P2b=S2c, P3=S3, P4=S4, diskusi=S5, contoh=S6, praktik=S7, P5=S8, P6=S9, P7=S11, P8=S12, P9=S13, P10=S14.

P5 otomatis mengirim `usulan-cek` dengan skor, diagnosis indikator dan fokus. Usulan tidak menimpa skor S8 yang disahkan guru. Antrean guru menampilkan usulan sebagai bukti awal. Penyelesaian P6 menandai perlunya cek ulang; tidak mengarang kelulusan.

P7 edisi 2 dan 3 membutuhkan ≥80%. Hasil lama tanpa versi mempertahankan ambang historisnya. P9 memerlukan P7, P5 lulus, P8 minimal T3 serta jeda dua hari. Percobaan berikutnya menggunakan bentuk berikut dari empat bentuk sesudah P7 diulang. P10 mempertahankan jejak hasil dan mengulang jadwal dari H+14 sesudah kegagalan.

Lembar bersiklus menambahkan akhiran `-siklus-<nilai>` pada identitas penyimpanan. Riwayat isian lama tetap ada. Daftar dokumen guru tetap dapat membuka dokumen tersebut sebagai dokumen isian lain; judulnya mungkin memuat identitas berkas bila tidak ada entri katalog langsung.

Hash penilaian sisi peramban mengurangi tampilnya kunci numerik dalam halaman P9; ini bukan pengamanan ujian. Bank sumber di alat berisi rumus/kunci. Gunakan layanan penilaian server dan sumber privat bila kelak diperlukan ujian dengan kunci rahasia. Versi ini mempertahankan layanan akun/D1 yang ada tanpa migrasi skema baru.


## Setelah pembersihan folder konten

106 HTML lama telah dikeluarkan: 96 halaman S dan 10 halaman L versi lama. Kode status S tetap diperlukan dan tidak dihapus dari API/progres. Rute langsung S/L lama dialihkan sementara (302) ke rute aplikasi P atau L yang aktif. S10 tidak lagi menjadi tahap dan dialihkan ke P1. Hash aplikasi S yang lama tetap dinormalisasi oleh alur-p.js.

Nilai dan isian akun tidak dihapus. Pengalihan menuju halaman baru tidak memigrasikan isian lama ke kolom baru. Untuk membaca kembali jawaban lama dalam format aslinya, pulihkan HTML terkait dari cadangan luar proyek. Jangan menyamakan penyimpanan data dengan tersedianya penampil dokumen historis.

Pengalihan ditempatkan di middleware karena [Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/redirects/) menjelaskan bahwa aturan _redirects tidak diterapkan pada permintaan yang dilayani Pages Functions. Pengalihan tidak menyajikan bahan belajar: ia menuju kerangka aplikasi, yang tetap menjalankan pemeriksaan akun dan gerbang materi.
