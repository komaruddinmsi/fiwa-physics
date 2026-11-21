# Aturan kerja proyek FIWA Physics

## Peran dan standar konten wajib

Baca dan ikuti [STANDAR-KONTEN-FISIKA.md](STANDAR-KONTEN-FISIKA.md) sebelum membuat, mengganti, atau meregenerasi topik dan TP. Standar ini berlaku untuk seluruh Physics TKA sekarang dan topik berikutnya, termasuk ketika dikerjakan AI lain. Peran: perancang pembelajaran fisika sekaligus pengembang visual interaktif. Materi harus kaya representasi yang benar-benar dapat diubah siswa, penjelasan yang mudah dipahami, contoh bertahap, serta checkpoint yang relevan. Mengubah nama, menambah ringkasan, atau memasang satu simulasi di akhir belum memenuhi standar.

Pertahankan panel kiri P1–P10; S10 tidak kembali. Ikuti standar versi 4.2, 21 November 2026: prasyarat mudah 30–60 detik; P5 memakai soal gating RPP satu per satu dan menunggu respon guru T3/T4; T1/T2 tetap pada soal sama. Simulasi memiliki Play/Pause/Stop/Reset dan perubahan visual yang nyata. Setiap pembahasan memakai tujuh judul langkah pada standar. Opening, konsep dan rangkuman konsisten mengikuti referensi. P7 tepat 10 soal, Unit Test terkunci sampai seluruh latihan selesai; media pendukung hanya bila diperlukan tanpa pengulangan. Simpan aturan, bank, generator dan bukti pemeriksaan bersama proyek. Catatan edisi sebelumnya adalah riwayat, bukan aturan aktif.

## Penyimpanan hasil perubahan

Instruksi pengguna, 20 November 2026: setiap perubahan dan tambahan berkas harus langsung disimpan pada folder proyek `fiwa-physics`, sesuai kategori dan jalur yang tepat, agar pengguna tidak perlu mengunduh lalu menyalin berkas dari chat.

- Edit berkas aplikasi yang sudah ada langsung pada lokasinya. Tambahkan berkas baru pada struktur aplikasi yang sesuai; jangan membuat folder pembungkus tambahan.
- Kerangka situs dan konfigurasi yang memang berada di akar tetap di akar. Gaya, skrip tampilan, gambar dan font masuk ke `assets/` sesuai subkategorinya; konten ke `konten/`; bahan ajar ke `aset-<topik>/`; media ke `media-<topik>/`; layanan server ke `functions/`; alat dan bank sumber ke `alat/`.
- Catatan hasil update, keputusan, fitur, pemeriksaan dan operasional disimpan langsung dalam kategori yang sesuai di `dokumentasi/`. Ikuti `dokumentasi/06-operasional/PANDUAN-UPDATE-BERKALA.md`.
- Hasil utama harus sudah berada di proyek. ZIP, tautan unduhan dan salinan dalam folder outputs bukan pengganti penyimpanan langsung. Buat paket unduhan hanya bila diminta atau memang diperlukan untuk distribusi.
- Simpan berkas kerja sementara dan cadangan di luar folder aplikasi, misalnya folder `work/` pada workspace induk, agar tidak tercampur dengan berkas situs.
- Setelah menyimpan, periksa jalur dan keberadaan berkas, lalu laporkan ringkasan perubahan serta lokasi kategori. Pertahankan bagian yang tidak termasuk ruang lingkup perubahan.
- Penyimpanan langsung pada proyek adalah tindakan lokal. Commit, push dan penerbitan mengikuti ruang lingkup instruksi pengguna yang berlaku.

Tambahan 4.1: uji perubahan geometri pada semua opening, hindari salinan kasus/pembahasan utuh antartahap, dan gunakan nada kontekstual referensi Chemistry. Ikuti aturan tambahan STANDAR-KONTEN-FISIKA.md serta jalankan alat/periksa-pengulangan.py, alat/uji-suara.cjs dan alat/uji-kasus-unik.cjs.

Tambahan 4.2: pertahankan burung hantu kecil pembuka tahap, durasi maksimum 15 detik/klik untuk menutup, bendera logo asli, penghormatan pengurangan gerak, serta tombol sembunyikan/tampilkan panel tanpa memuat ulang lembar. Baca rincian kanonis di STANDAR-KONTEN-FISIKA.md dan jalankan alat/uji-teman-belajar.cjs. Perayaan tidak mengubah nilai atau syarat ketuntasan.
