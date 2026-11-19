# Panduan bahan pendukung — Fisika FIWA

Semua video, audio, simulasi, dan bacaan yang muncul di bawah setiap tahapan diatur dari **satu berkas**: `media-f-mek/media.json`. Tidak ada kode yang perlu Anda sentuh.

Setiap kali berkas itu di-commit ke `komaruddinmsi/fiwa-physics`, Cloudflare menerbitkan ulang situs dalam satu sampai dua menit.

---

## Isi folder ini

```
media-f-mek/
├── media.json          ← satu-satunya berkas yang Anda edit
├── PANDUAN-MEDIA.md    ← panduan ini
├── simulasi/           ← simulasi HTML buatan sendiri
│   ├── sim.css
│   ├── usaha-gaya.html
│   ├── energi-kinetik-potensial.html
│   ├── grafik-gaya-perpindahan.html
│   ├── kekekalan-energi-mekanik.html
│   └── ayunan-bandul.html
├── bacaan/             ← halaman bacaan konsep
│   ├── bacaan.css
│   ├── bacaan-tp1.html
│   └── bacaan-tp2.html
└── audio/              ← tempat rekaman suara (mp3/ogg)
```

---

## Cara kerja `media.json`

Susunannya hanya tiga lapis: **TP → tahapan → daftar bahan**.

```json
{
  "tp": {
    "F.MEK.1-pra": {
      "S4": [ { bahan }, { bahan } ],
      "S6": [ { bahan } ]
    }
  }
}
```

- Kunci TP ditulis persis seperti pada `tp.json`, misalnya `F.MEK.1-pra` dan `F.MEK.1`.
- Kunci tahapan: `S1` sampai `S14`, termasuk `S2b` dan `S2c`.
- Bagian `"topik"` dipakai untuk lapis topik `L1`–`L4`.
- Tahapan yang tidak disebut berarti tidak punya bahan pendukung — tidak apa-apa.
- Kunci apa pun yang diawali garis bawah (`_baca_ini_dulu` dan sebagainya) diabaikan situs. Gunakan untuk catatan Anda sendiri.

---

## Lima jenis bahan

### 1. Video YouTube

```json
{
  "tipe": "video",
  "judul": "Penyajian konsep: usaha dan energi",
  "yt": "qXSFmDzYWnE",
  "mulai": 95,
  "catatan": "Jeda di tiap contoh soal, kerjakan sendiri dulu."
}
```

- **`yt`** diisi **kode videonya saja**, bukan alamat lengkap.
  Dari `https://www.youtube.com/watch?v=qXSFmDzYWnE` ambil `qXSFmDzYWnE`.
  Dari `https://youtu.be/qXSFmDzYWnE` ambil bagian yang sama.
- **`mulai`** opsional, dalam detik. `95` berarti video langsung dimulai pada menit 1:35.
- Video diputar **di dalam panel**, lengkap dengan tombol putar, jeda, dan layar penuh. Tidak membuka tab baru.
- Di bawah pemutar selalu ada tautan **Buka di YouTube**, untuk berjaga-jaga bila pemilik video melarang penayangan tertanam.

> **Bila video tidak mau tampil**, hampir selalu sebabnya satu: pengunggahnya mematikan izin penayangan di situs lain. Ganti dengan video lain — cukup ubah satu baris `yt`.

### 2. Audio

Ada dua cara.

**a. Rekaman suara Anda sendiri** — cara yang paling baik.

```json
{
  "tipe": "audio",
  "judul": "Rangkuman tiga menit",
  "berkas": "media-f-mek/audio/rangkuman-tp1.mp3"
}
```

Rekam dengan ponsel atau aplikasi perekam mana pun, simpan sebagai `.mp3`, unggah ke folder `media-f-mek/audio/`, lalu tulis namanya di `berkas`. Muncul sebagai pemutar dengan tombol putar, jeda, dan penggeser waktu.

**b. Naskah yang dibacakan peramban** — dipakai sekarang, sebagai jembatan.

```json
{
  "tipe": "audio",
  "judul": "Kilas balik sebelum pengulangan",
  "naskah": "Ini pengulangan berjarak, jadi jangan membuka catatan dulu…"
}
```

Peramban membacakan naskahnya, dan teksnya tetap ditampilkan agar bisa dibaca. Mutu suaranya tentu di bawah rekaman manusia. **Begitu Anda punya rekaman, ganti `naskah` menjadi `berkas`** — naskah yang ada sekarang bisa langsung dipakai sebagai teks bacaan saat merekam.

### 3. Simulasi

**Milik sendiri** (ada di folder `simulasi/`, pasti jalan):

```json
{
  "tipe": "simulasi",
  "judul": "Lintasan lengkung: Ep dan Ek bertukar",
  "berkas": "media-f-mek/simulasi/kekekalan-energi-mekanik.html",
  "catatan": "Setel gesekan ke nol dulu."
}
```

**Dari situs luar** (PhET dan sejenisnya):

```json
{
  "tipe": "simulasi",
  "judul": "Taman seluncur PhET",
  "url": "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_all.html?locale=in",
  "luar": true,
  "catatan": "Sumber luar."
}
```

`"luar": true` hanya menambah penanda **Sumber luar** pada kartunya, supaya siswa tahu bahannya bukan buatan sekolah.

> Sebagian situs menolak ditampilkan di dalam halaman lain. Bila panelnya kosong atau putih, ubah `"tipe"` menjadi `"tautan"` — kartunya berubah menjadi tombol yang membuka tab baru.

### 4. Bacaan

```json
{
  "tipe": "bacaan",
  "judul": "Bacaan konsep lengkap TP1",
  "berkas": "media-f-mek/bacaan/bacaan-tp1.html"
}
```

Sama seperti simulasi: boleh `berkas` (milik sendiri) atau `url` (situs luar).

### 5. Tautan

Untuk situs yang memang harus dibuka di tab baru.

```json
{
  "tipe": "tautan",
  "judul": "Soal latihan tambahan",
  "url": "https://contoh.sch.id/latihan",
  "catatan": "Dibuka di tab baru."
}
```

---

## Membuat simulasi baru

Cara tercepat: salin salah satu berkas di `simulasi/`, ganti isinya, simpan dengan nama baru, lalu tunjuk dari `media.json`.

Yang perlu ada di setiap simulasi:

```html
<link rel="stylesheet" href="sim.css">
```

Itu saja. Seluruh gaya tampilan — warna, tombol, penggeser, kotak hasil — sudah diatur di `sim.css` dan otomatis selaras dengan tema situs. Kelas yang tersedia: `.kotak`, `.grid`, `.atur`, `.baris`, `.angka`, `.rumus`, `.catatan`, `.sel`, `.tombol`, `.kaki`.

---

## Tiga hal yang sengaja dibiarkan kosong

Tahapan **S2 (Gerbang Prasyarat)**, **S8 (Gerbang Formatif Kelas)**, dan **S13 (Gerbang Ketuntasan TP)** tidak diberi bahan pendukung, dan panelnya menampilkan keterangan "Gerbang penilaian — bahan bantu sengaja tidak disediakan."

Ini mengikuti Kontrak Tahapan Ketuntasan: gerbang mengukur apa yang sudah dikuasai, bukan apa yang bisa dicari saat itu juga. Bila bahan bantu disediakan di gerbang, angka ketuntasannya berhenti bermakna.

Kalau Anda tetap ingin mengisinya, cukup tambahkan daftar pada kunci `"S2"`, `"S8"`, atau `"S13"` — situs tidak akan menolak. Tetapi pertimbangkan dulu akibatnya pada indikator ketuntasan semu (selisih S11 − S13).

---

## Langkah memperbarui lewat GitHub

Untuk **mengganti satu video atau menambah satu bahan**:

1. Buka `https://github.com/komaruddinmsi/fiwa-physics/blob/main/media-f-mek/media.json`
2. Klik ikon pensil di kanan atas
3. Ubah barisnya
4. Gulir ke bawah, isi pesan perubahan, klik **Commit changes**

Untuk **menambah berkas baru** (rekaman audio, simulasi baru, bacaan baru):

1. Buka folder tujuannya, misalnya `media-f-mek/audio/`
2. **Add file** → **Upload files**
3. Seret berkasnya, lalu **Commit changes**
4. Baru sesudah itu, sebut berkas tadi di `media.json` dengan cara yang sama seperti di atas

Dua menit kemudian situs sudah memakai bahan yang baru.

### Bila situs tidak berubah

Kalau sesudah lima menit tampilannya masih yang lama, periksa dua hal ini lebih dulu:

- **Tanda koma.** JSON tidak memaafkan koma yang hilang antar-bahan, atau koma berlebih sesudah bahan terakhir. GitHub akan menandai barisnya dengan garis merah saat Anda mengedit.
- **Riwayat penerbitan.** Buka Cloudflare → Workers & Pages → `fiwa-physics` → Deployments. Bila penerbitan terakhir berstatus gagal, pesannya ada di situ.

Untuk memeriksa susunan JSON sebelum commit, tempelkan isinya ke `jsonlint.com` atau buka berkasnya di VS Code — keduanya langsung menunjuk baris yang salah.

---

## Daftar bahan yang terpasang sekarang

| Tahapan | TP1 — Usaha, Ek, Ep | TP2 — Hukum Kekekalan Energi Mekanik |
|---|---|---|
| S1 | audio, bacaan | audio, bacaan |
| S2 | *gerbang* | *gerbang* |
| S2b | video, simulasi | simulasi, video |
| S2c | video, audio, bacaan | video, audio, simulasi |
| S3 | video, simulasi | simulasi, video |
| S4 | video, bacaan, 2 simulasi | bacaan, video, 2 simulasi |
| S5 | simulasi | simulasi, video |
| S6 | video, simulasi | simulasi, bacaan |
| S7 | 2 simulasi | 2 simulasi |
| S8 | *gerbang* | *gerbang* |
| S9 | video, simulasi, PhET | video, simulasi, PhET |
| S10 | audio, bacaan | audio, bacaan |
| S11 | video | video |
| S12 | bacaan | simulasi, bacaan |
| S13 | *gerbang* | *gerbang* |
| S14 | audio, simulasi | audio, simulasi |

Delapan video YouTube yang dipakai sudah diperiksa satu per satu dan semuanya masih tayang pada 18 November 2026. Bila suatu hari salah satunya dihapus pengunggahnya, kartunya akan kosong — ganti kode `yt`-nya dengan video lain, dan selesai.
