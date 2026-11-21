# Tema terang dan teduh serta navigasi tahapan di kiri

- ID: 2026-11-20-01
- Status: implementasi lokal selesai; pemeriksaan visual belum terverifikasi
- Kategori: tampilan, fitur dan dokumentasi
- Dasar: permintaan pengguna serta Dinamika Rotasi guided self study dan tangkapan layar yang dilampirkan.
- Baseline pembanding: [baseline awal](../../../01-baseline/BASELINE-2026-11-20.md).

## Perubahan

Tema biru langit, putih, navy dan kuning, versi Teduh, switch tema persisten, ikon fisika ringan, dan satu urutan tahapan vertikal di kiri. Layout ponsel memakai daftar tahapan yang dapat dibuka. Redaksi Tiga jalur diperbaiki menjadi Empat jalur sesuai kartu yang tersedia. Rincian: [tema dan navigasi](../../../03-fitur/TEMA-DAN-NAVIGASI-2026-11-20.md).

## Pemeriksaan

16 pemeriksaan logika lulus, termasuk pemisahan pilihan tema dari progres, pemulihan pilihan, nama aksesibel, urutan dan penguncian tahapan, pratinjau guru, serta resolusi stylesheet dokumen tertanam. Bagian aturan bisnis dan penyimpanan di app.js identik dengan sumber sebelum perubahan. Sintaks JavaScript lolos pemeriksaan.

Pratinjau peramban belum dapat dilakukan: akses koneksi loopback ditolak oleh lingkungan dan permintaan izin ditolak otomatis; URL file juga ditolak kebijakan browser. Tidak ada screenshot hasil baru atau klaim uji visual. Pratinjau HTML mandiri disediakan untuk peninjauan manual dengan data contoh.

## Dampak dan penerbitan

Tidak ada migrasi, perubahan API atau data produksi. Tidak ada commit, push, atau deployment. Dua berkas sumber lama berubah; 236 berkas sumber lama lain tetap sama dan tidak ada yang hilang. Salinan sebelum perubahan berada di folder work lokal, tidak ikut paket update.

TL-10 pada daftar tindak lanjut awal, tentang redaksi Tiga jalur, telah diperbaiki pada sumber lokal saja. Keadaan situs produksi tetap mengikuti baseline sampai perubahan diterbitkan.
