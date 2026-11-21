# Berkas unggah GitHub — versi 4

Sumber lokal: `C:\Users\user\Claude\Projects\CMS FISIKA\fiwa-physics`. Unggah isi folder ini sebagai akar repositori `komaruddinmsi/fiwa-physics`; jangan menambahkan satu folder pembungkus lagi. Semua perubahan masih lokal, belum commit/push/terbit.

| Lokasi tujuan GitHub | Berkas yang diunggah |
| --- | --- |
| Akar repositori | index.html, build.js, katalog.json, README.md, STANDAR-KONTEN-FISIKA.md, AGENTS.md, CLAUDE.md, GEMINI.md, PANDUAN-TOPIK-BARU.md dan berkas konfigurasi/panduan/skema yang masih ada. |
| assets/ | Seluruh isi; khusus pembaruan ini app.js, akun.js, tema.js, kelas-visual.js, kelas-konten.js, kelas-konten.css, kelas-animasi.js, gating.js, unit-test.js dan alur-p.css. Sertakan juga font, logo dan aset lain yang masih ada. |
| functions/ | _middleware.js dan api/[[rute]].js. Unggah keduanya bersama konten agar gerbang guru dan Unit Test bekerja. |
| konten/ | Seluruh folder aktif: 153 HTML dan 14 JSON. Dua topik TKA serta paket lain tetap pada jalurnya. |
| media-f-mek/ | Peta media, bacaan, panduan dan lima simulasi yang telah diperbarui. |
| media-f-use/ | Peta media, bacaan, panduan dan enam simulasi yang telah diperbarui. |
| aset-f-mek/ | GURU_RPP-F.MEK.docx sebagai sumber kurikulum. |
| aset-f-use/ | GURU_RPP-F.USE.docx; kini diperlukan kembali untuk gerbang RPP F.USE. |
| aset-ebook/ | Seluruh PDF yang masih dipakai, termasuk empat bagian Halliday. |
| alat/ | Seluruh generator/pemeriksa/bank yang masih ada, termasuk revisi_rpp.py, alignment_*.py, gating_rpp.json, gating_contract.json, unit_practice.json, unit_real_redaksi.py, unit_contract.json, uji-animasi.cjs dan uji-gating-unit.cjs. |
| .github/ | copilot-instructions.md. |
| dokumentasi/ | Seluruh kategori aktif, standar, provenance, riwayat, hasil uji, bukti gambar dan daftar unggah ini. |

MANIFEST-UPLOAD-PER-FOLDER.csv mencantumkan setiap berkas, folder tujuan dan hash. Kolom hash manifes itu sendiri kosong untuk menghindari hash yang merujuk dirinya. 2026-11-21-BERKAS-UPDATE.csv adalah daftar kumulatif perubahan; hash kedua daftar yang saling merujuk dikosongkan. Untuk unggah ulang per folder, gunakan seluruh isi yang tersisa.

Pengunggahan berkas baru tidak menghapus berkas lama di GitHub. Hapus jalur yang tercantum pada 2026-11-21-BERKAS-DIHAPUS.csv jika masih ada di repositori, terutama 18 bentuk P5 form-2/3/4 dan CSS simulasi F.MEK lama. Jangan mengunggah cadangan dari luar proyek. Jangan menghapus basis data/progres siswa atau menjalankan ulang skema pada D1 hanya untuk mengganti konten ini. Pengaturan DB/RAHASIA dan kolom yang diwajibkan pemasangan akun sebelumnya tetap diperlukan; tidak ada migrasi tabel baru untuk versi 4.

Sebelum menerbitkan, ingat bahwa unggah/commit ke cabang Cloudflare yang terhubung dapat memicu penerbitan. Pekerjaan lokal ini tidak mengubah pengaturan Cloudflare. Unit Test real memakai redaksi mandiri, dengan angka dan metode pasangan tetap; bukan paket angka baru. Syarat ketuntasan TP untuk L3 tetap berlaku selain syarat latihan selesai.
