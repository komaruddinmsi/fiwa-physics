# Gating RPP dan Unit Test versi 4

21 November 2026. Aturan aktif: STANDAR-KONTEN-FISIKA.md. Panel kiri P1–P10 dipertahankan.

P5 mengambil satu gerbang aktif dari server. Setelah siswa mengirim uraian, guru pembimbing menilai lewat kartu Butuh penilaian di Papan Guru: pilih T1–T4 dan tuliskan respon. T1/T2 meminta revisi, T3/T4 membuka soal berikutnya. Tiga gerbang inti per TP harus mencapai minimal T3. Soal transfer T4 opsional ditempatkan pada P8. Nilai numerik P5 adalah pemetaan untuk kompatibilitas: T3=80, T4=100; minimum seluruh gerbang dipakai ketika lengkap. Skor 40/60 menandai T1/T2 pada diagnosis yang perlu tindak lanjut. Menyelesaikan P6 tidak otomatis mengesahkan P5.

API: GET gating, POST gating/jawab, POST guru/gating. Revisi bukti dan penulisan bersyarat mencegah nilai usang menimpa respon. PUT progres umum mempertahankan nilai/bukti milik server. Atur ulang P5 oleh guru juga memulai kembali gerbang pertama. Pratinjau guru tidak mengirim penilaian sebagai siswa.

Latihan Unit Test dan Unit Test masing-masing 25 nomor per topik dengan PG, PGK dan benar–salah. Jawaban semua latihan harus lengkap dan dikirim. Setelah itu syarat latihan terpenuhi; akses L3 melalui aplikasi tetap mengikuti syarat ketuntasan TP yang sudah berlaku. URL/API Unit Test juga ditolak sebelum latihan selesai. Latihan boleh diperiksa per nomor; pembahasan Unit Test terbuka setelah kiriman akhir. PG dan PGK dinilai tepat; benar–salah mendapat proporsi pernyataan benar di nomor tersebut. Semua nomor berbobot sama. Unit Test satu kiriman per sesi.

API: GET unit (atau status=1), POST unit/periksa (latihan saja), POST unit/kirim. Nilai dan tanda selesai berada di server; PUT progres umum tidak dapat membuka Unit Test. Hasil dan review dapat dimuat ulang.

Bank latihan berasal dari dua referensi Latihan-TKA. Real memakai redaksi mandiri per nomor dengan data numerik/kunci/metode tetap, bukan transkripsi CBT. Variasi angka baru memerlukan penghitungan ulang seluruh kunci/pembahasan. Kunci tidak dikirim sebelum waktunya melalui API, tetapi repositori publik memuat sumber bank; versi ini bukan bank rahasia untuk ujian berisiko tinggi.

Tiga belas model utama mempunyai Play/Pause/Stop/Reset dan pilihan kecepatan. Model gerak memakai waktu fisika; vektor/kabel memakai konstruksi diagram, putaran memakai arah kualitatif dengan label batas model. Momen nol tidak berputar. Sebelas halaman simulasi lama memakai mesin bersama atau kontrol lengkap untuk bandul, motor listrik dan pemindaian grafik.
