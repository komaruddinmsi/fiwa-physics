# Panduan media F.USE

Folder ini hanya berisi peta media, bacaan interaktif dan simulasi yang masih digunakan. Seluruh bahan yang muncul pada situs diatur melalui media.json. Acuan isi wajib ada di ../STANDAR-KONTEN-FISIKA.md.

## Susunan aktif

- media.json: peta bahan tiap TP dan pembuka topik.
- bacaan/: halaman konsep interaktif yang memakai assets/kelas-konten.css dan kelas-visual.js.
- simulasi/: simulasi pendukung dan sim.css yang masih dirujuk media.json.

TP pada topik ini: F.USE.1-pra, F.USE.1. Nama TP pada media.json harus persis sama dengan kode metadata.

## Menambah bahan

Gunakan tipe video, audio, simulasi atau bacaan dengan judul dan tujuan pemakaian yang jelas. Jalur berkas lokal dihitung dari akar situs, misalnya media-f-use/bacaan/bacaan-tp1.html.

Antarmuka siswa memakai P1–P10. Kunci tahap di media.json tetap memakai pemetaan kompatibel S: P1=S1, P2a=S2b, P2b=S2c, P3=S3, P4=S4, diskusi=S5, contoh=S6, praktik=S7, P6=S9, P7=S11, P8=S12, P10=S14. P2/S2, P5/S8 dan P9/S13 adalah gerbang tanpa bahan bantu. Jangan membuat tahap S10 baru.

Video luar memakai kode yt dan dibuka melalui pemutar yang tersedia. Narasi audio saat ini memakai naskah yang dibacakan peramban setelah siswa menekan Putar; teksnya tetap tersedia. Jika ada rekaman nyata, buat folder audio/ ketika diperlukan, simpan mp3/ogg di sana lalu ganti naskah dengan berkas pada entri terkait. Folder kosong tidak perlu disertakan dalam unggahan.

Pertahankan bahan yang masih dirujuk. Jalankan python alat/periksa-media.py f-use dari akar proyek sesudah mengubah peta. Unggah sesuai jalur semula; penerbitan mengikuti pengaturan integrasi GitHub/Cloudflare, bukan perubahan lokal saja.
