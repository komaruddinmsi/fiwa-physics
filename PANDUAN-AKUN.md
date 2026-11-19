# Panduan akun Fisika FIWA

Situs ini sekarang punya pintu masuk. Tamu hanya melihat laman masuk; seluruh bahan belajar baru terbuka setelah pemilik situs menyetujui akunnya.

> **Repositori ini publik.** Siapa pun dapat membaca berkas di dalamnya.
> Karena itu, alamat surel pemilik dan nilai `RAHASIA` tidak pernah dituliskan di berkas mana pun —
> keduanya hanya hidup di dasbor Cloudflare dan di basis data Anda.

---

## Bagian 1 — Pemasangan, sekali saja

Lima langkah berikut dikerjakan di dasbor Cloudflare. Sebelum selesai, situs tetap berjalan seperti biasa tanpa pintu masuk, jadi tidak ada yang rusak di tengah jalan.

### Langkah 1 — Buat basis data

1. Buka `dash.cloudflare.com`
2. Menu kiri → **Storage & Databases** → **D1 SQL Database**
3. Klik **Create** (atau **Create database**)
4. Nama: **`fiwa-physics`**
5. **Create**

### Langkah 2 — Isi tabelnya

1. Masih di basis data yang baru dibuat, buka tab **Console**
2. Buka berkas `skema.sql` dari repositori, salin **seluruh isinya**
3. Tempelkan ke kotak Console, klik **Execute**
4. Hasilnya harus `success: true` beberapa kali — itu tandanya tabel sudah jadi

> Perintahnya aman dijalankan ulang. Kalau ragu sudah jalan atau belum, jalankan lagi.

### Langkah 3 — Ikat basis data ke situs

1. Menu kiri → **Workers & Pages** → klik **fiwa-physics**
2. Tab **Settings** → cari bagian **Bindings** (pada sebagian tampilan: **Functions** → **D1 database bindings**)
3. **Add binding**:
   - Variable name: **`DB`** — harus persis ini, huruf besar semua
   - D1 database: **fiwa-physics**
4. **Save**

Kalau ada pilihan **Production** dan **Preview**, isi keduanya dengan nilai yang sama.

### Langkah 4 — Isi kunci penanda tangan

Masih di **Settings**, cari **Environment variables** (atau **Variables and Secrets**).

1. **Add variable**
   - Nama: **`RAHASIA`**
   - Nilai: teks acak panjang, **buatan Anda sendiri**, minimal 40 karakter
   - Pilih **Encrypt** / **Secret** bila tersedia
2. **Save**

Cara cepat membuat nilainya: buka tab baru, tekan F12, tempel ini di Console, tekan Enter, salin hasilnya.

```js
crypto.randomUUID() + crypto.randomUUID()
```

> Kunci ini dipakai untuk menandatangani sesi. Siapa pun yang tahu nilainya bisa membuat sesi palsu dan masuk sebagai siapa saja. **Jangan pernah menuliskannya ke dalam repositori, catatan rapat, atau pesan.** Kalau sewaktu-waktu bocor, cukup ganti nilainya di sini: semua orang diminta masuk lagi, dan tidak ada data yang hilang.

Dua peubah lain bersifat pilihan:

| Nama | Guna | Bawaan |
|---|---|---|
| `EMAIL_OWNER` | Alamat surel pemilik. Bila diisi, pemilik langsung aktif tanpa menunggu persetujuan. Isi sebagai peubah **terenkripsi** | kosong |
| `WAJIB_KODE` | Isi `1` bila anggota harus memasukkan kode enam huruf saat pertama kali | mati |

### Langkah 5 — Terbitkan ulang

Pengikatan baru berlaku pada penerbitan berikutnya.

1. Tab **Deployments** → penerbitan paling atas → menu **⋯** → **Retry deployment**
2. Atau: lakukan satu commit apa pun di GitHub

Tunggu sampai statusnya **Success**, lalu buka `https://fiwa-physics.pages.dev/`. Yang muncul seharusnya laman masuk.

### Langkah 6 — Angkat diri Anda sebagai pemilik

Ada dua jalan; pilih salah satu.

**Jalan A — lewat peubah (paling mudah).** Pada Langkah 4, tambahkan peubah **terenkripsi** `EMAIL_OWNER` berisi alamat surel Anda. Buka situs, masukkan alamat itu, tekan tombol mana pun — Anda langsung masuk sebagai pemilik tanpa menunggu persetujuan siapa pun.

**Jalan B — lewat Console D1.** Buka Console basis data, ganti alamat di bawah dengan milik Anda, lalu **Execute**:

```sql
INSERT OR REPLACE INTO anggota (email, nama, peran, status, dibuat)
VALUES ('alamat-anda@contoh.com', 'Owner', 'owner', 'aktif', 0);
```

Console D1 bersifat pribadi, jadi alamat surel Anda tidak ikut terbaca siapa pun.

Sesudah salah satunya, buka situs dan masuk dengan alamat itu.

---

## Bagian 2 — Pemakaian sehari-hari

### Siswa dan guru mendaftar

Mereka membuka situs, mengisi alamat surel dan nama, lalu menekan **Masuk sebagai Siswa** atau **Masuk sebagai Guru**. Layarnya berubah menjadi "Menunggu persetujuan".

Tidak ada surel yang dikirim ke mana pun. Alamat surel hanya menjadi tanda pengenal.

### Anda menyetujui

Menu **Anggota** hanya muncul untuk pemilik situs. Guru dan siswa tidak melihatnya, dan API-nya pun menolak mereka — jadi alamat surel Anda tidak terbaca siapa pun dari dalam situs.

1. Masuk sebagai pemilik
2. Klik **Anggota** di bilah atas
3. Permintaan baru ada di bagian **Menunggu persetujuan**
4. **Setujui** atau **Tolak**

Peran bisa diubah kapan saja lewat tombol **Jadikan guru** / **Jadikan siswa**.

Yang bersangkutan cukup menekan **Periksa lagi** pada layar tunggunya, dan langsung masuk.

### Guru berpindah mode

Di bilah atas ada sakelar **Guru | Siswa**. Guru dan pemilik bebas menukarnya kapan saja, tanpa keluar dan tanpa akun kedua.

- **Mode guru** — Papan Guru, panel tier, kunci jawaban, semua tahapan terbuka untuk persiapan
- **Mode siswa** — tampilan persis seperti yang dilihat murid, lengkap dengan tahapan yang masih terkunci

Pilihan mode tersimpan di peramban, jadi tetap begitu saat dibuka lagi.

### Progres mengikuti akun

Progres belajar kini tersimpan di basis data, bukan di peramban. Murid yang berganti perangkat tetap menemukan progresnya. **Papan Guru** sekarang menampilkan seluruh murid aktif, bukan lagi hanya perangkat yang sedang dipakai.

---

## Bagian 3 — Hal yang perlu Anda tahu

### Alamat surel tidak diverifikasi

Karena tidak ada surel yang dikirim, **sistem tidak bisa membuktikan** bahwa yang mengetik `budi@fiwa.sch.id` benar-benar Budi. Pengamannya ada pada Anda: permintaan yang janggal terlihat di daftar tunggu dan bisa ditolak.

Risiko nyatanya: murid yang mengetik alamat surel temannya yang sudah disetujui bisa masuk sebagai temannya dan mengubah progresnya.

Bila ini mengganggu, nyalakan **`WAJIB_KODE = 1`**. Setiap anggota yang Anda setujui akan mendapat kode enam huruf yang tampil di kolom **Kode** pada laman Anggota; serahkan kode itu kepada orangnya, dan ia memasukkannya sekali pada perangkatnya. Sesudah itu tidak ditanya lagi.

### Apa yang benar-benar terkunci

Terkunci untuk tamu: `konten/`, `aset-f-use/`, `media-f-use/`, dan `katalog.json`. Artinya seluruh halaman tahapan, seluruh PDF termasuk berkas gerbang, seluruh simulasi dan bacaan.

Terbuka untuk tamu: laman muka, logo, `assets/app.css`, `assets/app.js`, `assets/akun.js` — hanya kulit yang diperlukan untuk menampilkan laman masuk. Tidak ada bahan belajar di dalamnya.

Penguncian ini dikerjakan di peladen Cloudflare, bukan di peramban, jadi tidak bisa dilewati dengan membuka alamat berkasnya langsung.

### Sesi

Sesi bertahan 30 hari pada satu peramban. Bila Anda menolak atau menghapus seorang anggota, aksesnya berhenti pada pemuatan halaman berikutnya.

### Batas gratis Cloudflare

D1 pada paket gratis memberi 5 juta pembacaan dan 100 ribu penulisan per hari. Untuk satu sekolah, angka ini sangat lapang. Penjaga berkas sengaja dibuat tidak menyentuh basis data sama sekali — ia hanya memeriksa tanda tangan sesi — jadi membuka 36 halaman tahapan tidak menghabiskan kuota.

---

## Bila ada yang tidak beres

| Gejala | Penyebab paling sering |
|---|---|
| Laman muka berkata "Basis data belum tersambung" | Pengikatan `DB` belum dibuat, atau belum diterbitkan ulang sesudah membuatnya |
| Semua orang bisa masuk tanpa disetujui | `skema.sql` belum dijalankan, sehingga tabel `anggota` belum ada |
| Masuk berhasil tapi langsung keluar lagi | `RAHASIA` berbeda antara Production dan Preview, atau baru diganti |
| Bahan tetap terbuka untuk tamu | Penerbitan ulang belum berjalan; periksa tab Deployments |
| Laman masuk tidak muncul sama sekali | Folder `functions/` belum ikut terunggah ke GitHub |

Untuk melihat galat yang sebenarnya: **Workers & Pages → fiwa-physics → Deployments → penerbitan terakhir → Functions → Real-time logs**.

---

## Pembimbingan murid–guru dan penilaian

Ditambahkan 19 November 2026.

### Sekali jalan: siapkan tabelnya

Buka **Console D1** di dasbor Cloudflare, lalu jalankan isi `migrasi-bimbing.sql`
**satu pernyataan tiap kali tombol kirim ditekan**. Console D1 hanya menjalankan
satu perintah per kiriman; menempelkan seluruh berkas sekaligus tidak
menjalankan apa pun dan tidak memberi pesan galat.

Ada tiga pernyataan: membuat tabel `bimbing`, membuat indeksnya, dan menambah
kolom `oleh` pada tabel `progres`. Pernyataan ketiga akan menolak dengan pesan
`duplicate column name` bila kolomnya sudah ada — itu aman, lanjutkan saja.

### Siapa mengatur apa

| Peran | Yang dilihat | Yang bisa diubah |
|---|---|---|
| **Pemilik** | seluruh murid, seluruh pasangan bimbingan | menetapkan guru mana saja untuk tiap murid; menilai murid mana pun |
| **Guru** | hanya murid bimbingannya | menilai murid bimbingannya |
| **Siswa** | dirinya sendiri | — |

Hubungannya **banyak ke banyak**: satu murid boleh punya beberapa guru, satu
guru boleh membimbing banyak murid. Yang menetapkan hanya pemilik situs.

### Cara pemilik mengatur pembimbing

Laman **Anggota** → tabel **Akun siswa** → tombol **Atur pembimbing** pada baris
murid. Centang guru yang membimbing, lalu **Simpan pembimbing**. Daftarnya
dikirim utuh, jadi mencabut centang berarti mencabut pembimbingan.

Bila seorang murid diubah perannya menjadi guru, atau akunnya ditolak, seluruh
baris pembimbingannya ikut dibuang supaya papan guru tidak menyisakan nama lama.

### Bagaimana guru tahu apa yang perlu dinilai

Panel guru (`#guru`) punya bagian **Butuh penilaian**: daftar murid × TP ×
tahapan yang menunggu nilai, yang paling lama menunggu di atas. Isinya dua
macam:

| Tahapan | Menunggu apa | Syarat masuk antrean |
|---|---|---|
| **S12** Tugas Kinerja | tier T1–T4 | murid sudah menandai bukti terkirim, tier masih kosong |
| **S8** Gerbang Formatif Kelas | skor 0–100 | murid sudah lulus S2 (≥80) dan menyelesaikan S4, skor S8 belum masuk |

Guru mengetik nilainya langsung di baris antrean, lalu **Simpan**. Nilainya
ditulis ke progres murid beserta catatan siapa yang menilai dan kapan, pada
`ev.S8.oleh` / `ev.S12.oleh` (berisi **nama tampilan**, bukan surel, supaya surel pemilik tidak
sampai ke peramban murid) dan kolom `progres.oleh` (surel, hanya di peladen).

Di bawahnya, **Papan posisi** menampilkan posisi tiap murid pada seluruh TP —
untuk guru hanya murid bimbingannya, untuk pemilik seluruh murid.

### Jawaban dan skor tersimpan per akun

Semua dokumen yang bisa diisi murid kini menyimpan **isian, waktu mulai, status
terkunci, dan skornya** di akun murid, bukan lagi di peramban. Murid yang menutup
tab, berganti perangkat, atau memuat ulang melanjutkan dari tempat terakhir:
pengatur waktu PRI UIN tetap berjalan dari tenggatnya, dan lembar yang sudah
dikumpulkan tetap terkunci dengan nilainya.

- Berlaku untuk 12 dokumen PRI UIN, lapis L1–L4 (utama dan latihan), pembuka, dan
  semua lembar tahapan. Dokumen yang diunggah kelak ikut otomatis (lihat
  `PANDUAN-TOPIK-BARU.md`, bagian "Jawaban tersimpan per murid").
- Isian disimpan sekitar 3 detik setelah murid berhenti mengubah, dan seketika saat
  tab ditutup. Di atas halaman ada bilah kecil: "Jawabanmu tersimpan di akunmu".
- Tersimpan di tabel D1 `lembar` (satu baris per murid per dokumen). Tabel itu
  **dibuat sendiri** saat dipakai pertama kali; `migrasi-lembar.sql` hanya bila ingin
  membuatnya lebih dulu. Satu dokumen maksimal 60 KB dan satu murid maksimal 400 dokumen.
- Guru dan pemilik yang membuka dokumen hanya melihat-lihat: tidak ada yang disimpan
  atas nama mereka, dan bilah menulis "Mode guru: jawaban tidak disimpan".
- Isian tidak pernah dikirim sebelum isian lama selesai dimuat, supaya lembar kosong
  tidak menimpa jawaban yang sudah ada. Bila peladen tidak terjangkau, murid diberi
  tahu dan lembar tetap bisa dipakai.
- Menghapus anggota di laman Anggota ikut menghapus semua isiannya.
- Skor yang tampil di daftar guru hanya untuk dokumen yang sudah dikumpulkan
  (ditekan Selesai atau waktu habis). Yang belum, tampil sebagai "terisi 12/30".
- Tombol **Hapus progres TP ini (hanya milikmu)** di halaman TP hanya menghapus
  progres TP di perangkat itu; isian dokumen yang sudah tersimpan tidak ikut hilang.
  Untuk mengosongkan isian, guru memakai "Atur ulang dokumen murid".

### Membuka ulang satu dokumen murid

Murid tidak sengaja menekan Selesai, atau dokumennya sudah terlanjur diskor?
Guru tidak perlu menghapus progres satu TP. Di **Papan Guru → Atur ulang dokumen
murid**: pilih murid, klik dokumen yang ingin dibuka ulang, baca pratinjau, lalu
**Ya, buka ulang**.

- Yang dihapus hanya hasil dokumen itu (skor atau tanda selesai). Untuk **S12**
  tier-nya ikut dihapus; untuk **S14** yang dicopot adalah hasil pengulangan terakhir.
- Dokumen lain dan progres TP tetap utuh.
- Pratinjau menunjukkan apa yang hilang, perubahan status TP (misalnya Tuntas →
  Mencoba), dan tahapan mana yang terkunci atau terbuka lagi. Contoh: mereset S13
  melepas kunci "sekali jalan" sehingga murid bisa mengerjakannya lagi.
- Alasan boleh diisi (maksimal 160 karakter). Murid melihatnya di halaman tahapan
  itu: "*Bu Sari membuka ulang tahapan ini pada 19 Nov — alasan. Kerjakan lagi dari awal.*"
- Berlaku untuk **semua tahapan S1–S14 (termasuk S2b/S2c) di semua topik berjenis alur**,
  dibaca dari katalog; topik baru otomatis ikut, tanpa pengaturan tambahan.
- Guru hanya melihat dan mereset muridnya sendiri; pemilik melihat semua murid.

**Dokumen isian lain (lapis L1–L4, paket PRI UIN, pembuka, dokumen baru)** juga
muncul di daftar yang sama, dalam kotak "Lapis, paket, dan dokumen isian lain" per
topik. Klik, baca pratinjau, **Ya, buka ulang**: isian dan skor dokumen itu dihapus
dan murid mulai dari kosong (untuk PRI UIN: layar pengaturan waktu muncul lagi).
Tahapan S1–S14 yang juga punya isian tersimpan dibuka ulang dua-duanya sekaligus
dengan satu klik. Dokumen yang belum terdaftar di katalog tetap muncul, memakai
alamat berkasnya sebagai nama.

#### Mengapa ada nomor epoch

Progres murid disimpan di peramban lalu disinkronkan ke peladen, dan dulu
kirimannya selalu menimpa. Akibatnya tab murid yang masih terbuka bisa
menghidupkan lagi dokumen yang baru direset guru. Sekarang tiap TP punya nomor
`epoch` yang naik setiap kali guru menilai atau mereset. Kiriman dengan epoch lebih
lama ditolak dan murid diberi salinan terbaru; peramban murid juga mengecek epoch
tiap 30 detik dan saat tab kembali terlihat. `epoch` dan catatan `reset` dimiliki
peladen, nilai kiriman dari peramban diabaikan.

Aturan yang sama berlaku untuk isian dokumen (tabel `lembar`): tiap dokumen punya
`epoch` sendiri. Tab murid yang masih memegang isian lama ditolak, lalu halaman
dokumen itu memuat ulang sendiri dan murid melihat lembar kosong beserta catatan
guru. Pemeriksaannya tiap 45 detik dan saat tab kembali terlihat.

Satu konsekuensi yang wajar: pekerjaan murid yang tercatat pada salinan usang,
di jeda sebelum peramban menyusul (paling lama 30 detik untuk tahapan, 45 detik
untuk isian dokumen), ikut dibuang.

Tombol lama **Hapus progres TP ini** di halaman TP kini berlabel "(hanya milikmu)":
ia hanya menghapus progres akun yang sedang dipakai, bukan milik murid.

### Batas yang dijaga di sisi server

Semuanya diperiksa ulang di API, bukan hanya disembunyikan di tampilan:

- guru tidak dapat menilai murid yang bukan bimbingannya (403);
- guru tidak dapat mengatur pembimbing (403);
- siswa tidak dapat membuka antrean maupun papan (403);
- hanya S8 dan S12 yang boleh dinilai guru — tahapan lain ditolak;
- guru hanya boleh mereset dokumen murid bimbingannya (403 untuk selain itu); murid tidak dapat mereset dirinya sendiri;
- skor dibatasi 0–100, tier 1–4;
- isian dokumen hanya bisa ditulis oleh murid pemiliknya (guru dan pemilik tidak menyimpan apa pun lewat jalur itu), `reset` dari peramban dibuang, dan kunci dokumen yang tak wajar (`..`, `//`, karakter aneh) ditolak;
- guru hanya bisa melihat daftar dokumen isian murid bimbingannya (`guru/lembar`); isian mentah tidak pernah dikirim ke guru, hanya ringkasan;
- pembimbing hanya boleh ditetapkan untuk akun berperan siswa, dan hanya akun
  guru atau pemilik yang aktif yang boleh menjadi pembimbing. Surel lain dalam
  permintaan dibuang dan dikembalikan pada medan `ditolak`.
