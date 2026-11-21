# Hasil pemeriksaan versi 4

21 November 2026. Pemeriksaan lokal; tidak memakai siswa atau basis data produksi.

| Pemeriksaan | Hasil aktual |
| --- | --- |
| Struktur konten | 6 TP, 24 konsep, 144 halaman keluaran, 343 kemunculan visual, 516 kemunculan butir/checkpoint; 192 butir P9 berhash. P5 dan Unit Test dimuat dari server. |
| Durasi dan jumlah | Prasyarat mudah 30–60 detik. Tiga gerbang inti RPP per TP. P6 dua/tiga soal; P7 tepat 10; P9 8 per bentuk; P10 4 per sesi. |
| Model fisika | 2.615 pemeriksaan lulus. |
| Animasi | 4.257 pemeriksaan lulus: 13 model, waktu, SVG, neraca energi lintas bentuk lintasan/gesekan, berhenti dan momen nol. |
| Alur P | 27 skenario lulus; 8 pemeriksaan runtime konten lulus. |
| Gating dan Unit Test | 264 pemeriksaan pada SQLite dalam memori lulus: gerbang berurutan, T2 tetap, T3/T4 lanjut, guru pembimbing, revisi usang, pemalsuan PUT, reset, kunci Unit Test dan review setelah reload. |
| Tautan dan paket | 171 HTML aplikasi diperiksa, 921 rujukan lokal ditemukan. Konten berisi 153 HTML dan 14 metadata JSON. |
| Media | F.MEK 8 item dan F.USE 4 item pendukung pada P4; pemeriksa tidak menemukan pengulangan atau berkas hilang. |
| Pengalihan | Uji rute lama dan penjagaan akses lulus; bentuk P5 lama dialihkan ke P5 aktif. |

## Pemeriksaan peramban

Pratinjau loopback memakai siswa/guru fiktif. Pengiriman jawaban G1, kartu bukti di Papan Guru, respon T3, dan terbukanya G2 terlihat di antarmuka. Simulasi troli menunjukkan waktu berjalan, jeda, kembali 0 saat Stop dan parameter awal saat Reset. Bandul berubah sudut/energi lalu kembali awal; motor dan pemindaian grafik diuji tombolnya. Mesin bersama dipakai untuk halaman simulasi lainnya.

Latihan F.MEK dikerjakan melalui kontrol antarmuka pada seluruh 25 nomor, termasuk PGK dan benar–salah, lalu dikirim dan mendapat 100%. Unit Test F.MEK kemudian dapat diambil; Unit Test F.USE yang belum berlatih menampilkan kondisi terkunci. Kiriman latihan yang belum lengkap diarahkan ke nomor kosong. Pembahasan mempunyai tujuh elemen daftar; SVG geometri soal tetap tampil setelah penyaringan HTML.

Terang/Teduh, teks isian dan opening diperiksa. Pada lebar 390 piksel, materi, Unit Test dan panel tahapan dapat digunakan tanpa luapan horizontal; panel tahapan dapat dibuka. Override ukuran layar dikembalikan. Bukti visual: preview-opening-v4.jpg dan preview-opening-teduh-v4.jpg.

## Batas pemeriksaan

Ini bukan uji langsung Cloudflare D1 yang telah diterbitkan, uji beban, atau tinjauan pedagogis setiap butir oleh guru. Bank real mempertahankan data numerik pasangan dengan redaksi mandiri; bukan variasi angka baru. Ketersediaan video eksternal dan suara narasi bergantung layanan/peramban, tidak semuanya diputar sampai selesai. Bentuk P9 berputar sehingga bukan persediaan butir tanpa batas. Hasil terdahulu dipertahankan; jawaban HTML edisi lama tidak otomatis dipindahkan ke struktur baru.
