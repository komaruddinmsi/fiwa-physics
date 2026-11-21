# Hasil pemeriksaan konten interaktif

Tanggal 21 November 2026. Pengujian dilakukan pada salinan lokal dengan akun fiktif. Tidak ada perubahan diterbitkan dan tidak ada data siswa produksi dibaca atau diubah.

## Pemeriksaan otomatis

| Pemeriksaan | Hasil |
| --- | --- |
| Generator dan struktur aktif | Enam TP, 24 konsep, 162 halaman edisi 3. Seluruh tahap katalog TP menunjuk edisi 3; S10 tidak aktif. |
| Halaman dan tautan lokal | Tidak ada ID ganda atau tautan berkas lokal yang hilang pada keluaran baru. Ada 426 instans visual termasuk stimulus statis dan pengulangan pada bacaan. Angka ini bukan jumlah model unik. |
| Soal dan waktu | 672 kemunculan butir/checkpoint pada halaman; minimum 120 detik, dinaikkan sesuai level. P6 dua/tiga butir per cabang dan fokus, P7 tepat sepuluh, P10 empat per sesi. |
| Butir terlindungi | 210 kemunculan soal berhash pada P9 dan L3; kunci sumber P9 diterima pemeriksa hash, tidak ada hash kosong atau kunci jawaban numerik terbuka pada konfigurasi P9. |
| Model fisika | 2.615 pemeriksaan lulus, termasuk nilai acuan dan 1.296 kombinasi neraca energi: energi total konsisten, gesekan tidak menghabiskan lebih dari energi awal, posisi yang tidak terjangkau ditandai. |
| Runtime isian | Delapan skenario lulus: isian wajib, desimal berkoma, hasil awal vs perbaikan, pemulihan keadaan, P5 sebagai usulan, waktu lewat tidak otomatis gagal, ketuntasan checkpoint/P6, dan hash P9. |
| Alur dan progres | 27 skenario lulus, termasuk percabangan P6, versi 3 P7 memakai ambang baru, kompatibilitas hasil lama, syarat P8/P9, serta pengulangan berjarak. |
| Sintaks | Sepuluh berkas JavaScript yang berubah, termasuk layanan penilaian, lulus pemeriksaan sintaks. |

## Pemeriksaan isi dan peramban

Audit bank mencakup hitungan numerik, tanda dan satuan, hubungan diagram dengan pertanyaan, waktu dan keunikan ID. Perbaikan hasil audit meliputi ukuran panah vektor, batas kontrol massa, gaya berat/normal pada diagram gerak, reaksi engsel, pemisahan label, neraca energi, berhenti sebelum tujuan serta pemindahan solusi langsung dari instruksi P8.

Di peramban lokal: sudut 90° memberi usaha 0 J; isian angka mengubah model; P7 memberi 100% untuk sepuluh jawaban tepat lalu 90% sesudah satu jawaban diubah, sambil mempertahankan hasil awal 100%. P5 contoh menampilkan total 15 menit dengan alokasi 2–4 menit per butir. Skor P5 60 dengan fokus kedua membuka dua soal energi kinetik di P6a. Panel bunyi diuji melalui aktif/nonaktif dan tombol Uji bunyi, dengan status visual yang sesuai.

Terang/Teduh diperiksa pada desktop dan viewport ponsel 390×844. Isian, teks dan diagram tetap terbaca. Pada halaman ponsel yang diuji, lebar gulir sama dengan lebar tampilan, sehingga tidak ada luapan horizontal halaman. Diagram dapat diperbesar melalui dialog dan ditutup kembali. Bukti tampilan disimpan bersama catatan ini dalam tiga JPG.

## Batas pemeriksaan

Layanan D1, sinkronisasi lintas perangkat dan antrean guru pada situs terbit belum diuji dengan akun nyata. Pemulihan keadaan diuji pada runtime terkontrol; pratinjau peramban menolak penulisan akun. Video luar dipertahankan beserta tautannya; seluruh video dan audio lintas perangkat belum diputar satu per satu. Ketersediaan sumber luar mengikuti penyedianya. Estimasi durasi soal masih perlu dikalibrasi melalui penggunaan kelas.

Pemeriksaan otomatis dan audit model tidak menggantikan peninjauan pedagogis oleh guru. Empat bentuk P9 berputar dan dapat digunakan lagi; sumber generator di repositori publik tidak merahasiakan kunci ujian. Tidak ada klaim keamanan ujian berisiko tinggi.
