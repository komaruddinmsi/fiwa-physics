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
