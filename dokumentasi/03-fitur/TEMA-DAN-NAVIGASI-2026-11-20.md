# Tema dan navigasi FIWA Physics

Pembaruan lokal 20 November 2026 mengikuti warna dan bentuk dokumen Dinamika Rotasi serta contoh panel kiri yang diberikan pengguna. Statusnya siap ditinjau pada sumber lokal; belum diterbitkan ke GitHub atau Cloudflare.

## Tampilan

Tema Terang menjadi bawaan: latar biru langit, kartu putih, tulisan navy, aksen kuning hangat dan bidang bersudut membulat. Font Nunito diambil dari font tertanam dalam referensi pengguna, sehingga antarmuka tidak bergantung pada Google Fonts. Ikon atom, gelombang, vektor dan orbit dibuat sebagai SVG ringan, dengan dekorasi dibatasi pada tempat yang membantu mengenali jalur dan orientasi belajar.

Tema Teduh menggunakan biru slate sedang, bukan hitam pekat. Pilihan Terang atau Teduh tersedia pada kepala situs, juga pada layar masuk. Nilainya disimpan pada kunci peramban `fiwa-theme-v1`, terpisah dari progres murid. Pergantian tema tidak merender ulang halaman atau mengganti sumber iframe. Nama aksesibel tetap ada ketika label teks disembunyikan pada layar kecil.

## Alur di sisi kiri

Halaman TP dan halaman tiap tahapan memakai panel kiri vertikal. Daftarnya tetap S1, S2, S2b, S2c, lalu S3–S14, bernomor satu sampai enam belas bila seluruh tahapan ada. Tahap aktif, bukti selesai dan akses terkunci dibedakan. Penguatan dan remediasi tetap mengikuti hasil S2; urutan, penilaian dan syarat kelulusan tidak diubah.

Panel kiri dapat digulir terpisah pada desktop dan mengikuti tinggi kepala situs. Di bawah 900 piksel, daftar dapat dibuka melalui Urutan tahapan agar dokumen tidak terdesak. Berpindah tahap mempertahankan posisi gulir daftar; perubahan skor menyegarkan penanda tanpa membuang lembar isian yang sedang terbuka.

## Dokumen tertanam

HTML milik FIWA memperoleh lapisan warna bersama melalui `tema-konten.css`; konten soal dan skrip penilaian tidak disunting. PDF dan iframe dari situs luar mempertahankan penampil aslinya. Kecocokan visual seluruh variasi dokumen tertanam masih memerlukan pemeriksaan di peramban.

Perbaikan berikutnya pada tanggal yang sama menambahkan bidang baca abu-biru dengan tinta navy untuk dokumen pembelajaran saat mode Teduh aktif. Pemeriksaan peramban pada lima dokumen perwakilan sudah dilakukan; lihat [catatan keterbacaan](KETERBACAAN-TEDUH-2026-11-20.md). Pemeriksaan ini tidak menyatakan seluruh variasi dokumen telah diaudit.

## Berkas aplikasi

- Diubah: `index.html`, `assets/app.js`.
- Ditambahkan: `assets/tema.css`, `assets/tema.js`, `assets/tema-konten.css`, `assets/physics-orbit.svg`, `assets/fonts/nunito.woff2`.
- `assets/app.css` dan semua berkas sumber konten, bank soal, API, skema serta migrasi dipertahankan.

Pratinjau HTML mandiri pada folder outputs memakai data contoh. Salinan ini tidak menjalankan layanan akun produksi dan tidak dimaksudkan menggantikan berkas aplikasi untuk Cloudflare.
