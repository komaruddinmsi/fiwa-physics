# Tindak lanjut FIWA Physics

Seluruh item berstatus **terbuka pada baseline 20 November 2026**. Prioritas adalah urutan kajian yang diusulkan, bukan penetapan tenggat atau persetujuan perubahan kode. Tidak ada pemilik pekerjaan atau tanggal selesai yang dikarang.

| ID | Prioritas kajian | Temuan | Bukti dan akibat | Langkah berikutnya |
| --- | --- | --- | --- | --- |
| TL-01 | Tinggi | Sumber publik memuat bank dan pegangan guru | README menyatakan kunci tidak masuk repo, tetapi GURU_ dan alat/bank ada di pohon publik; middleware statis tidak membedakan peran berdasarkan nama GURU_. | Tetapkan kebutuhan kerahasiaan dan sumber penyimpanan bahan guru sebelum perubahan akses; belum ada perubahan pada baseline. |
| TL-02 | Tinggi | Panduan akun belum mengikuti kata sandi | Bagian awal PANDUAN-AKUN menjelaskan login surel saja; assets/akun.js dan API mewajibkan kata sandi. | Susun revisi panduan pemasangan/login dan alur akun lama berdasarkan implementasi, lalu uji dengan akun uji saat diminta. |
| TL-03 | Sedang | Sumber lokal tidak identik dengan GitHub | 233 sama; satu HTML berbeda; Halliday berbeda folder; app.js akar hanya ada pada GitHub. | Pilih versi kanonis sebelum perubahan. Telusuri beda FAQ dan jelaskan app.js aktif; jangan menimpa otomatis. |
| TL-04 | Sedang | README tertinggal | 18 versus 16 tahapan; progres lokal versus D1; aturan kunci tidak sesuai berkas publik. | Perbarui orientasi README pada tugas dokumentasi sumber berikutnya. |
| TL-05 | Sedang | Pernyataan akses e-book tidak selaras | PANDUAN-TOPIK-BARU menyatakan PDF statis tidak melewati login; middleware menjaga aset-* dan contoh PDF anonim memberi 401. | Bedakan akses situs yang dijaga dari berkas GitHub publik; koreksi panduan sesuai bukti. |
| TL-06 | Sedang | Panduan media F.MEK tersalin dari F.USE | Contoh daftar TP/berkas pada PANDUAN-MEDIA serta audio/README F.MEK belum sesuai struktur aktual. | Selaraskan contoh dengan empat TP dan media.json F.MEK. |
| TL-07 | Sedang | Pemetaan bank dan profil tier perlu rekonsiliasi | Kontrak menempatkan L1 pada kuis-tertunda; ringkasan panduan baru menyebut L1 bersama latihan. RPP meminta profil per-proses, API menyimpan tier tunggal. | Bandingkan kontrak, rubrik dan log sebelum merancang asesmen baru; belum disimpulkan sebagai kegagalan produksi. |
| TL-08 | Sedang | Utang piloting belum berstatus akhir | Log mencatat butir pengganti, rekaman, perangkat/alat, FAQ berbasis panen dan ambang rancangan. | Beri status per item setelah ada bukti kelas atau bahan pengganti; jangan menyatakan selesai dari keberadaan situs. |
| TL-09 | Sedang | Konfigurasi dan perilaku produksi belum seluruhnya diuji | Dasbor Cloudflare, backup D1, identitas deployment, login baru, reset dan simpan lintas perangkat belum diperiksa. | Lakukan pemeriksaan berikutnya dengan akses dan akun uji yang sesuai ruang lingkup. |
| TL-10 | Rendah | Pengantar beranda menyebut Tiga jalur | Empat kartu terlihat: IGCSE, AS/A, TKA dan OSN. | Selaraskan redaksi saat pembaruan tampilan berikutnya. |
| TL-11 | Sedang | Sebagian sumber primer log tidak ditemukan | RPP.txt, BRIEF.md, Modul-TP1.txt dan Modul-TP2.txt disebut log, tetapi nama persisnya tidak ada pada pemindaian. | Minta atau temukan sumber aslinya bila perubahan berikutnya bergantung pada kutipan verbatim; jangan mengarang penggantinya. |
