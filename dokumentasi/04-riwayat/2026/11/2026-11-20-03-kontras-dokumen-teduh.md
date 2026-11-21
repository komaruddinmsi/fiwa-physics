# Perbaikan kontras dokumen isian pada mode Teduh

- ID: 2026-11-20-03
- Tanggal: 20 November 2026
- Status: tervalidasi lokal
- Kategori: fitur, tampilan dan validasi
- Dasar: laporan pengguna bahwa teks dokumen isian tidak terbaca jelas saat mode Teduh aktif.

## Penyebab dan perbaikan

Lapisan tema sebelumnya mencampurkan teks terang dengan panel serta input putih tetap pada template lama. HTML pembelajaran kini memakai profil bidang baca abu-biru dengan tinta navy pada mode Teduh. Penyesuaian mencakup label, tabel, textarea, select, placeholder, readonly/disabled, pilihan terisi, tanda ragu dan hasil terkunci.

## Berkas yang diunggah untuk perbaikan ini

Ganti `assets/tema.js` dan `assets/tema-konten.css` di GitHub dengan dua berkas pada lokasi yang sama di folder proyek lokal. Tidak diperlukan paket unduhan atau pemindahan dokumen soal.

## Hasil pemeriksaan

Pemeriksaan visual dan warna terhitung pada lima dokumen perwakilan serta kontrol uji telah dilakukan di peramban lokal. Tidak ada sampel teks terukur di bawah rasio 4,5:1; placeholder diukur terpisah sekitar 4,99:1. Jawaban contoh tetap utuh setelah beralih Terang–Teduh. Enam belas pemeriksaan logika antarmuka sebelumnya tetap lulus dan sintaks JavaScript valid.

Rincian: [fitur keterbacaan](../../../03-fitur/KETERBACAAN-TEDUH-2026-11-20.md) dan [bukti pemeriksaan](../../../05-validasi/2026/11/kontras-teduh/HASIL-PEMERIKSAAN.md).

## Penerbitan

Belum ada commit, push atau deployment. Pengujian memakai data contoh pada loopback lokal dan tidak menyentuh nilai maupun jawaban produksi. Sumber soal dan kode penilaiannya tidak disunting.
