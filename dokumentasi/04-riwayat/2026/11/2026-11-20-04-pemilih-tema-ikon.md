# Pemilih tema dengan ikon saja

Tanggal: 20 November 2026, WIB. Status: **tervalidasi lokal** melalui pemeriksaan sintaks dan logika; belum diterbitkan.

Permintaan pengguna: hilangkan teks Terang dan Teduh pada panel pemilih tema, sisakan ikon.

## Perubahan

- Ikon matahari untuk Terang dan bulan untuk Teduh tampil tanpa teks pada desktop maupun ponsel.
- Tombol tetap memiliki nama untuk pembaca layar, keterangan saat disorot (`title`), dan penanda tema aktif (`aria-pressed`). Keterangan mengikuti pilihan bahasa Indonesia/Inggris.
- Ukuran tombol 36 × 36 piksel, dengan ikon 17 × 17 piksel. Penyimpanan pilihan tema dan tampilan dokumen tetap memakai perilaku sebelumnya.

## Berkas aplikasi untuk GitHub

1. `index.html`, menggantikan berkas di akar repositori.
2. `assets/tema.css`, menggantikan berkas di folder `assets`.
3. `assets/tema.js`, menggantikan berkas di folder `assets`.

Berkas disimpan langsung di proyek. Catatan ini berada dalam kategori riwayat; tidak ada ZIP, push, atau penerbitan.

## Pemeriksaan

- Pemeriksaan sintaks `assets/tema.js` lulus.
- Seluruh 16 pemeriksaan logika antarmuka yang sudah ada lulus, termasuk pergantian tema, penyimpanan pilihan, terjemahan nama tombol dan tema dokumen tertanam.
- Belum dilakukan pemeriksaan visual peramban baru untuk perubahan kecil ini. Pemeriksaan tampilan dokumen Teduh pada update sebelumnya tetap tercatat terpisah.
