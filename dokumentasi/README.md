# Dokumentasi proyek FIWA Physics

Baseline pemeriksaan 20 November 2026, zona waktu Asia/Jakarta. Folder sumber proyek ditemukan di `C:\Users\user\Claude\Projects\CMS FISIKA\fiwa-physics`; folder induknya memuat sumber piloting, generator dan paket integrasi terdahulu.

Situs aktif, layanan akun memberi respons siap, dan katalog yang terlihat memuat lima topik: dua topik TKA dengan enam TP serta tiga topik olimpiade dengan lima belas paket. Inventaris merekam 238 berkas proyek dan 167 berkas pendukung. Tidak ada kode, basis data produksi, commit, atau penerbitan yang diubah dalam pemeriksaan ini.

## Mulai membaca

1. [Baseline proyek](01-baseline/BASELINE-2026-11-20.md) untuk kondisi situs, repositori dan batas pemeriksaan.
2. [Inventaris dokumen](00-inventaris/INVENTARIS-DOKUMEN.md) untuk kategori dan ringkasan sumber, serta [inventaris semua berkas](00-inventaris/INVENTARIS-BERKAS.csv).
3. [Keputusan teknis yang tercatat](02-teknis/REGISTER-KEPUTUSAN.md), [peta fitur](03-fitur/PETA-FITUR.md), dan [riwayat proyek](04-riwayat/RIWAYAT-PROYEK.md).
4. [Hasil pemeriksaan](05-validasi/HASIL-PEMERIKSAAN-2026-11-20.md) serta [tindak lanjut](09-tindak-lanjut/DAFTAR-TINDAK-LANJUT.md).
5. [Cara mencatat update berkala](06-operasional/PANDUAN-UPDATE-BERKALA.md) dan templat di `08-template/`.

## Susunan folder

| Folder | Isi |
| --- | --- |
| `00-inventaris` | Daftar dokumen dan berkas lokal, daftar berkas GitHub, jejak perbedaan |
| `01-baseline` | Kondisi proyek pada tanggal pemeriksaan |
| `02-teknis` | Ringkasan keputusan arsitektur, data dan aturan pembelajaran |
| `03-fitur` | Fitur teramati, dukungan kode dan batas verifikasi |
| `04-riwayat` | Ringkasan sejarah dan daftar commit |
| `05-validasi` | Hasil pemeriksaan baca dan bukti ringkas |
| `06-operasional` | Prosedur pendokumentasian update berikutnya |
| `07-konten-media` | Pemetaan bahan ajar, sumber dan catatan media |
| `08-template` | Templat update, keputusan teknis dan pemeriksaan |
| `09-tindak-lanjut` | Masalah yang terbukti dan pekerjaan lanjutan |
| `99-arsip` | Aturan penyimpanan dokumen yang telah digantikan |

## Cara membaca status

**Teramati** berarti terlihat di situs atau respons HTTP saat pemeriksaan. **Didukung kode** berarti terdapat pada berkas yang dibaca, belum tentu telah diuji seluruh alurnya di produksi. **Tercatat sumber** berarti pernyataan dokumen lama, bukan hasil pengujian ulang. **Belum terverifikasi** tidak boleh diperlakukan sebagai sudah selesai.

Semua berkas asli dipertahankan di lokasinya. Pengelompokan dilakukan melalui indeks, bukan pemindahan bahan ajar. Dokumentasi ini adalah catatan lokal; belum diunggah ke GitHub atau Cloudflare. Tidak ada jadwal otomatis yang dibuat.

## Pembaruan tampilan 20 November 2026

Tema Terang dan Teduh serta panel tahapan vertikal telah diimplementasikan pada sumber lokal. [Rincian fitur](03-fitur/TEMA-DAN-NAVIGASI-2026-11-20.md) dan [catatan update](04-riwayat/2026/11/2026-11-20-01-tema-terang-teduh.md). Belum diterbitkan. Perbaikan keterbacaan dokumen pada mode Teduh sudah diperiksa di peramban lokal pada lima dokumen perwakilan; lihat [rincian perbaikan](03-fitur/KETERBACAAN-TEDUH-2026-11-20.md). Baseline di atas tetap merekam keadaan sebelum perubahan ini.

Pemilih tema kini hanya menampilkan ikon matahari dan bulan pada semua ukuran layar. Keterangan aksesibilitas dan saat disorot tetap tersedia; lihat [catatan pemilih tema ikon](04-riwayat/2026/11/2026-11-20-04-pemilih-tema-ikon.md).

## Riwayat rancangan alur

[Rekomendasi alur konsep dan latihan menuju ketuntasan](03-fitur/RANCANGAN-ALUR-KONSEP-S9-S11-2026-11-20.md) menyiapkan penghapusan S10, cabang S9 menurut hasil S8, sepuluh soal S11, dan susunan Konsep–Checkpoint seperti lampiran Dinamika Rotasi. Rancangan awal ini telah digantikan penerapan P1–P10 dan konten interaktif edisi 3 pada 21 November 2026. [Catatan rancangan](04-riwayat/2026/11/2026-11-20-05-rancangan-alur-konsep.md).

## Kondisi lokal terbaru

Konten interaktif edisi 3 sudah diterapkan secara lokal untuk enam TP. Acuan aktif: [standar konten](../STANDAR-KONTEN-FISIKA.md), [hasil pemeriksaan](05-validasi/2026/11/konten-interaktif/HASIL-PEMERIKSAAN.md), dan [panduan unggah terbaru](06-operasional/2026/11/2026-11-21-BERKAS-UPDATE-GITHUB.md). Pembersihan menyingkirkan generator, bank dan pengujian yang telah digantikan. Pada pembersihan lanjutan, HTML S dan L lama dipindahkan ke cadangan di luar proyek. Tautan lama menuju halaman aktif. Data akun/nilai tetap tersimpan, tetapi isian dokumen lama memerlukan pemulihan HTML dari cadangan untuk ditampilkan dalam format aslinya.

## Acuan terbaru: versi 4, 21 November 2026

Standar aktif adalah [STANDAR-KONTEN-FISIKA.md](../STANDAR-KONTEN-FISIKA.md). Penerapan terbaru: [Gating RPP dan Unit Test](03-fitur/GATING-RPP-DAN-UNIT-TEST-V4.md), [riwayat versi 4](04-riwayat/2026/11/2026-11-21-04-penyelarasan-rpp-v4.md), [hasil pemeriksaan versi 4](05-validasi/2026/11/konten-interaktif/HASIL-PEMERIKSAAN-V4.md) dan [daftar unggah](06-operasional/2026/11/2026-11-21-BERKAS-UPDATE-GITHUB.md). Pernyataan edisi 3 di atas adalah catatan penerapan terdahulu dan digantikan versi 4.
