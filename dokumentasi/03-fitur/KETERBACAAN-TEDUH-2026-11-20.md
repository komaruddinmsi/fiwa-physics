# Keterbacaan dokumen isian pada mode Teduh

Perbaikan lokal 20 November 2026 menanggapi teks worksheet, LKPD dan soal yang samar saat mode Teduh dipilih. Sebagian dokumen lama memakai latar putih tetap, sementara lapisan tema sebelumnya mengganti tinta menjadi terang. Kombinasi tersebut membuat label, isi tabel dan jawaban kehilangan kontras.

## Perilaku setelah perbaikan

Antarmuka situs tetap memakai tema Teduh biru slate. HTML pembelajaran dalam `konten/` dan `aset-<topik>/` memakai bidang baca abu-biru lembut dengan tinta navy. Panel, isian, judul bagian, tabel dan bilah pemeriksaan memiliki pasangan warna yang selaras. Warna putih terang tidak dipakai sebagai latar utama lembar.

Semua jenis kotak isian tercakup, termasuk struktur `.identitas`, `.isi-item` dan `.isian`, isian tanpa pembungkus khusus, textarea serta select. Teks petunjuk, jawaban readonly dan isian disabled tetap terbaca. Kondisi perlu diperbaiki dibedakan dengan bidang hangat serta garis tepi; pilihan terisi dan tanda ragu tetap mempunyai warna status yang berbeda.

Ukuran teks bidang baca dan isian dibuat 16 piksel; label dan petunjuk mempunyai batas minimum 14 piksel. Jarak baris pada teks soal diberi ruang lebih longgar. Beberapa tinta inline lama diselaraskan secara terbatas, tanpa menyapu seluruh warna dokumen.

## Berkas aplikasi yang berubah

| Jalur relatif proyek | Perubahan |
| --- | --- |
| `assets/tema.js` | Menandai HTML pembelajaran dengan profil baca paper; media, PDF dan sumber luar tetap terpisah. |
| `assets/tema-konten.css` | Palet bidang baca, teks, isian, label, tabel, status soal, fokus dan kondisi terkunci pada mode Teduh. |

Aturan penilaian, isi soal, ID isian dan penyimpanan jawaban tidak diubah. Pergantian tema memperbarui tampilan tanpa memuat ulang lembar. PDF dan sumber luar tetap memakai penampil aslinya; tidak digunakan filter pembalik warna untuk diagram.

## Verifikasi

Pemeriksaan dilakukan pada pratinjau lokal dengan akun dan jawaban contoh. Sampel mencakup LKPD F.USE, worksheet F.MEK, latihan S11, gerbang S13 dan paket PRI SMP, termasuk status terpilih, ragu dan hasil terkunci. Kontrol readonly/disabled diuji pada halaman contoh terpisah. [Hasil pemeriksaan](../05-validasi/2026/11/kontras-teduh/HASIL-PEMERIKSAAN.md) memuat ukuran kontras dan tangkapan layar.

Status: tersimpan pada proyek lokal; belum diterbitkan ke GitHub atau Cloudflare.
