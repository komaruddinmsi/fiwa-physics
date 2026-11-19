# Menambahkan topik baru ke situs

Ada **dua jenis topik**. Pilih dulu yang mana, karena strukturnya berbeda.

| Jenis | Untuk apa | Bagian panduan |
|---|---|---|
| **Alur** (`"jenis"` tidak diisi) | Topik pembelajaran penuh: TP, tahapan S1–S14, lapis L1–L4, media wajib. Contoh: F.MEK, F.USE. | Bagian 1–7 |
| **Paket** (`"jenis": "paket"`) | Kumpulan dokumen lepas tanpa alur pembelajaran: paket soal simulasi, arsip ujian, bank latihan. Contoh: PRI UIN SMP & SMA. | Bagian 8 |

Bagian 1–7 merekam pola topik **alur** yang dipakai **F.MEK (Mekanika: Gaya & Gerak)**.
Ikuti urutannya dan topik barumu akan hidup di situs tanpa menyentuh `app.js`.

---

## 1 · Struktur folder yang harus ada

Satu topik memerlukan tiga folder dan satu kode topik. Contoh untuk topik
berkode `F.XYZ` dengan slug folder `f-xyz`:

```
konten/f-xyz/
  topik.json                     ← identitas topik
  pembuka/index.html             ← WAJIB · fenomena dunia nyata (lihat bagian 9)
  <slug-tp>/tp.json              ← satu per TP
  <slug-tp>/S1 … S14/index.html  ← 16 tahapan per TP
  L1/index.html                  ← kuis blok
  L2/index.html                  ← muara topik
  L3/index.html                  ← tes topik (dinilai)
  L3/latihan.html                ← tes topik (latihan, opsional)
  L4/index.html                  ← tantangan mapel

aset-f-xyz/                      ← PDF, kunci guru, papan mini
media-f-xyz/media.json           ← peta bahan pendukung tiap tahapan
```

Penjaga berkas di `functions/_middleware.js` sudah berpola `/aset-*` dan
`/media-*`, jadi folder barumu otomatis terkunci untuk tamu. Tidak perlu
menyunting berkas itu.

### topik.json

```json
{ "kode": "F.XYZ", "nama": "Nama Topik", "mapel": "Fisika",
  "fase": "F", "jalur": "TKA", "urutan": 4 }
```

`jalur` menentukan topik ini muncul di menu mana: `IGCSE`, `AS/A`, `TKA`,
atau `OSN`. `urutan` mengatur posisinya di dalam jalur itu.

### tp.json

```json
{ "kode": "F.XYZ.1", "judul": "Judul singkat", "teks": "Rumusan TP apa adanya.",
  "bloom": "C3", "urutan_ajar": 1, "prasyarat": ["slug-tp-sebelumnya"],
  "ambang": 75 }
```

**`urutan_ajar` mengikuti urutan mengajar di RPP, bukan abjad.** Pada F.MEK
urutannya `1-pra → 2 → 1a → 1b`. TP ke-n baru terbuka setelah seluruh TP
sebelumnya berstatus Tuntas; lapis L1–L4 terbuka setelah semua TP tuntas.

---

## 2 · Kerangka satu halaman tahapan

Jangan menyalin CSS atau mesin penilaian ke tiap halaman. Dua berkas bersama
sudah mengurus semuanya:

```html
<link rel="stylesheet" href="../../../../assets/tahapan.css">
...
<script>window.FIMS_KUNCI = { ... };</script>
<script src="../../../../assets/fims-shim.js"></script>
```

`assets/fims-shim.js` menangani: membaca bilangan (koma dan titik sama-sama
diterima), menilai, bilah bawah yang dapat dilipat, daftar nomor yang masih
salah, dan pelaporan skor ke mesin alur. Halaman cukup menulis markah soalnya.

### Markah soal yang dikenali mesin

```html
<article class="soal">
  <h3 class="soal-judul"><span>Soal 1 · Judul</span></h3>
  <div class="dalam-soal">
    <div class="naskah">Teks soal.</div>
    <div class="arah"><b>Arah positif … ke kanan.</b></div>   <!-- opsional -->
    <div class="isian-grid">
      <div class="isian"><label for="a1">Pertanyaan <span class="sat">(N)</span></label>
        <input type="text" inputmode="decimal" id="a1" name="a1" data-isian="1"></div>
    </div>
  </div>
</article>
```

Lembar bergaya lama yang memakai `.kartu-soal` + `<h3>` juga dikenali.

### Tanpa penilaian

Halaman yang hanya perlu menandai "sudah dikerjakan" cukup memasang
`<button type="button" id="fims-kirim">…</button>` dan tidak menulis
`FIMS_KUNCI`. Mesin akan melapor `selesai`, bukan skor.

---

## 3 · Kunci jawaban: terbuka atau tersandi

| Tahapan | Bentuk kunci | Alasan |
|---|---|---|
| S11, L1 dan latihan lain | terbuka | boleh diulang, kunci bukan taruhan |
| **S2 dan S13 (gerbang)** | **tersandi** | sekali jalan, menentukan status tuntas |

Kunci tersandi memakai SHA-256 bergaram:

```json
{ "garam": "F.XYZ-2026-…", "faktor": 20,
  "num": { "g1": [["hash","hash","hash"], 0.2] },
  "pil": { "g2": "hash" } }
```

Hash dibentuk dari `garam|id|nilai`. Untuk butir bilangan, nilainya
dibulatkan ke `nilai × faktor`, dan daftar hash mencakup seluruh rentang
toleransi. `alat/bangun.py` punya fungsi `sandikan()` yang mengerjakan ini.

**Ini penghalang, bukan rahasia kriptografis.** Garamnya ikut terkirim ke
peramban karena penilaian memang dikerjakan di sisi murid. Yang dicegah
adalah murid yang membuka kode sumber — dan itu memang ancaman nyatanya.

---

## 4 · Aturan yang tidak boleh dilanggar

**§K-3 — pemisahan bank soal.** Butir gerbang tidak boleh muncul di lembar
murid mana pun selain gerbangnya sendiri. Tiga bank harus terpisah:

- bank latihan (S7, S11, L1) — boleh diulang
- bank gerbang kelas (S8, Papan Mini) — soal saja, tanpa kunci dan tanpa pembahasan
- bank gerbang ketuntasan (S2, S13) — butir baru, belum pernah dilihat

Pemeriksanya ada di bagian 6 di bawah. Jalankan setiap kali menambah butir.

**Kunci jawaban guru** disimpan di `aset-f-xyz/` dengan awalan `GURU_` dan
tidak pernah ditaut dari halaman murid.

**Dokumen tampil di dalam halaman.** Tiap PDF dan HTML ditanam dengan
`<iframe class="berkas">`, selalu disertai tautan `Buka penuh di tab baru ↗`
dan, untuk PDF, tombol `Unduh (PDF)`. Jangan membuat tautan yang satu-satunya
cara membukanya adalah tab baru.

---

## 5 · media.json — aturan wajib bahan pendukung

Peta bahan pendukung tiap tahapan. Tipe yang didukung: `video` (kode
YouTube), `audio` (berkas atau naskah yang dibacakan peramban), `simulasi`,
`bacaan`, `tautan`.

### Yang wajib ada pada halaman PEMBUKA

Selain tiap TP, kunci `topik` &rarr; `PEMBUKA` pada `media.json` juga wajib
memuat keempat jenis yang sama, dengan **simulasi milik sendiri**. Lihat
bagian 9.

### Yang wajib ada pada SETIAP TP

| Jenis | Wajib | Catatan |
|---|---|---|
| `audio` | ✓ | naskah yang dibacakan peramban sudah cukup; punya tombol Putar · Jeda · Hentikan |
| `video` | ✓ | kode YouTube; tertanam sebagai pemutar, bisa diputar dan dijeda di tempat |
| `simulasi` | ✓ | **minimal satu milik sendiri** di `media-f-xyz/simulasi/` |
| `bacaan` | ✓ | **minimal satu milik sendiri** di `media-f-xyz/bacaan/` |

Simulasi PhET dan bacaan OpenStax boleh ditambahkan, tetapi **tidak boleh
menjadi satu-satunya**. Situs luar dapat menolak ditampilkan di dalam
halaman, dan kita tidak mengendalikannya. Yang milik sendiri menjamin murid
selalu punya satu yang pasti terbuka tanpa tab baru.

### Semua ditanam, semua punya opsi tab baru

`simulasi` dan `bacaan` **ditanam** di panel beserta tautan
`Buka penuh di tab baru ↗`. Tipe `tautan` hanya membuka tab baru — pakai itu
hanya sebagai jalan terakhir.

### Jalur berkas dihitung dari AKAR SITUS

```json
{ "tipe": "simulasi", "berkas": "media-f-xyz/simulasi/namanya.html" }
```

Bukan `simulasi/namanya.html`. `app.js` memuatnya dari akar situs, bukan dari
dalam folder media. Jalur yang salah menghasilkan bingkai kosong tanpa pesan
galat apa pun — kesalahan ini pernah terjadi dan hanya tertangkap oleh
pemeriksa di bawah.

### Gerbang tetap bersih

**S2, S8, dan S13 sengaja dikosongkan.** Gerbang tidak didampingi bahan bantu.

### Pemeriksanya

```bash
python3 alat/periksa-media.py f-xyz
```

Memeriksa: keempat jenis ada pada tiap TP · simulasi dan bacaan ada yang
milik sendiri · tiap berkas benar-benar ada bila dihitung dari akar situs ·
gerbang tidak punya bahan. Jalankan sampai bersih sebelum menyatakan selesai.

Rincian tipe ada di `media-f-xyz/PANDUAN-MEDIA.md`.

---

## 6 · Membangun dan memeriksa

```bash
cd alat && python3 bangun.py     # menulis seluruh halaman tahapan
cd ..   && node build.js         # memperbarui katalog.json
```

Sebelum menganggap selesai, jalankan empat pemeriksaan ini:

1. **Hitung ulang tiap kunci numerik** dari angka pada naskahnya, dengan rumus
   yang ditulis terpisah dari bank soal. Jangan membandingkan bank dengan
   dirinya sendiri.
2. **Kunci yatim dan isian tanpa kunci** — tiap id di `FIMS_KUNCI` harus ada
   di markah, dan tiap `data-isian` yang dinilai harus punya kunci.
3. **Tautan putus** — telusuri setiap `href`, `src`, dan `data`.
4. **§K-3** — bandingkan 60 karakter pertama naskah tiap butir gerbang dengan
   seluruh halaman murid. Pemeriksaan inilah yang menemukan dua pelanggaran
   nyata pada F.MEK.
5. **Kelengkapan bahan** — `python3 alat/periksa-media.py f-xyz`.

Lalu muat tiap halaman di peramban dan pastikan nol galat JavaScript, serta
isi satu lembar bernilai sampai 100 untuk memastikan skornya sampai ke mesin
alur.

**Satu peringatan dari pengalaman.** Memeriksa bahwa sebuah `<iframe>` ada
di halaman **tidak membuktikan apa pun**. Bingkai yang memuat 404 tetap
sebuah elemen `<iframe>` yang sah. Periksa **isinya**: buka bingkainya dan
pastikan ada judul dan unsurnya, atau pantau permintaan yang berstatus 404.

---

## 7 · Isi tiap tahapan

| | Tahapan | Isi | Dinilai |
|---|---|---|---|
| S1 | Peta & Tujuan Pembelajaran | tujuan, indikator, bekal, lembar bekal | – |
| S2 | Gerbang Prasyarat | 8 butir menguji **bekal**, bukan materi baru | ✓ 80 |
| S2b / S2c | Penguatan / Remediasi | kartu bekal yang goyah | – |
| S3 | Pemantik & Prakonsepsi | tebakan terbuka atas miskonsepsi | – |
| S4 | Penyajian Konsep Awal | modul konsep | – |
| S5 | Pembahasan Prakonsepsi | dipimpin guru | – |
| S6 | Inti Terbimbing | dipimpin guru | – |
| S7 | Praktik Terstruktur | lembar kerja | ✓ |
| S8 | Gerbang Formatif Kelas | papan mini, skor diisi guru | guru |
| S9 | Diferensiasi T1–T4 | jalur sesuai hasil S8 | – |
| S10 | Konsolidasi & Jangkar | tiga jangkar terbuka | – |
| S11 | Latihan Bertingkat | H+0–H+2, boleh diulang | ✓ 75 |
| S12 | Tugas Kinerja | rubrik, dinilai guru, minimal T3 | guru |
| S13 | Gerbang Ketuntasan | butir baru, sekali jalan | ✓ 75 |
| S14 | Pengulangan Berjarak | H+14, +30, +60 | ✓ |

Tuntas menuntut **dua-duanya**: lulus S13 **dan** S12 minimal T3.

---

## 8 · Topik jenis "paket" — dokumen lepas tanpa alur pembelajaran

Dipakai saat kamu hanya ingin menaruh dokumen HTML yang sudah berdiri sendiri
(paket soal simulasi, arsip ujian, bank latihan) di dalam situs: tidak ada TP,
tidak ada tahapan S1–S14, tidak ada lapis L1–L4, tidak ada kunci berurutan,
dan tidak ada media wajib. Nilai dan pembahasan muncul di dalam lembar itu
sendiri dan **tidak** masuk ke progres jalur belajar.

### 8.1 · Struktur folder

```
konten/<slug-topik>/
├── topik.json
└── paket/
    ├── paket.json
    ├── penyisihan-v1.html
    ├── penyisihan-v2.html
    ├── semifinal-v1.html        ← tinggal jatuhkan berkas baru di sini
    └── final-v1.html
```

Tidak ada folder `aset-*` atau `media-*` yang wajib untuk jenis ini.

### 8.2 · `topik.json`

```json
{
  "kode": "PRI.SMP",
  "nama": "PRI UIN — SMP",
  "mapel": "Fisika",
  "jalur": "Olimpiade",
  "urutan": 1,
  "jenis": "paket",
  "ringkas": "Satu kalimat yang tampil di kartu topik dan di kepala halaman."
}
```

`"jenis": "paket"` adalah satu-satunya penanda. Tanpa baris itu, `build.js`
memperlakukan folder sebagai topik alur dan akan mencari TP yang tidak ada.

Nilai `"jalur"` yang dikenali: `IGCSE`, `AS/A`, `TKA`, `Olimpiade`
(juga `Olympiad`, `OSN`, `KSN`).

### 8.3 · `paket/paket.json`

```json
{
  "tahap": [
    { "kode": "penyisihan", "nama": "Penyisihan", "urutan": 1 },
    { "kode": "semifinal",  "nama": "Semifinal",  "urutan": 2 },
    { "kode": "final",      "nama": "Final",      "urutan": 3 }
  ],
  "berkas": {
    "penyisihan-v1.html": {
      "judul": "Simulasi Penyisihan · Versi 1",
      "tahap": "penyisihan",
      "soal": 30,
      "bentuk": "Pilihan ganda 5 opsi",
      "ringkas": "Keterangan isi paket, tampil di bawah judul pada daftar.",
      "catatan": "Tanpa kalkulator. Tidak ada pengurangan nilai untuk jawaban salah."
    }
  }
}
```

- `tahap` menentukan **urutan dan nama kelompok** di halaman topik. Berkas yang
  `tahap`-nya tidak ada di daftar dikumpulkan di kelompok "Lainnya" paling bawah.
- `berkas` memberi keterangan per nama berkas. Berkas HTML yang tidak disebut di
  sini tetap tampil — judulnya diambil dari `<title>` dokumen, keterangannya kosong.
- `urutan` opsional, untuk mengatur urutan di dalam satu tahap.

### 8.4 · Syarat dokumen HTML-nya

1. **Berdiri sendiri.** Seluruh CSS dan JS di dalam satu berkas. Jangan
   menautkan `assets/tahapan.css` atau `assets/fims-shim.js` — dokumen paket
   tidak memakai mesin tahapan.
2. **Jangan mengirim `postMessage` ke induk.** Dokumen paket tidak melapor skor;
   kalau ia mengirim `{fims:'skor'}`, pesan itu diabaikan karena tidak ada TP
   yang aktif, tetapi lebih baik tidak dikirim sama sekali.
3. **Tanpa `target="_blank"` di dalam dokumen.** Situs sudah menyediakan tombol
   "Buka penuh di tab baru" di luar bingkai.
4. **Kunci jawaban jangan ditulis terbuka.** Paket PRI UIN memakai geseran
   Caesar (`GESER = 7`) pada `KUNCI_PIL`, `PEMBAHASAN`, dan `REVIEW`. Itu
   penghalang terhadap View Source, bukan kerahasiaan kriptografis — cukup untuk
   simulasi, tidak cukup untuk ujian yang menentukan.

### 8.5 · Menambah berkas berikutnya

Cukup dua langkah:

1. Salin berkas HTML-nya ke `konten/<slug-topik>/paket/`.
2. Tambahkan keteranganya di `paket.json` → `berkas`.

Lalu `node build.js`. Tidak perlu menyentuh `app.js`, `build.js`, atau
`_middleware.js`. Folder `konten/` sudah terjaga oleh pola yang ada, jadi
dokumen baru otomatis hanya bisa dibuka anggota yang sudah masuk.

### 8.6 · Pemeriksaan sesudah build

```bash
node build.js
python3 -c "import json;k=json.load(open('katalog.json'));[print(t['slug'],t.get('jenis'),len(t.get('paket',[]))) for t in k['topik']]"
```

Lalu di situs, pastikan empat hal ini:

1. Kartu topik muncul di jalurnya dan menyebut jumlah paket.
2. Halaman topik mengelompokkan paket per tahap, dengan urutan sesuai `paket.json`.
3. Tiap paket terbuka **di dalam** halaman situs, bukan tab baru.
4. Tombol "Buka penuh di tab baru" ada dan menunjuk ke berkas yang benar.

Memeriksa bahwa elemen `<iframe>` ada **tidak membuktikan apa pun**. Buka
bingkainya dan pastikan isinya benar-benar termuat — jumlah soal, tombol
"Mulai mengerjakan", dan hasil penilaian setelah "Selesai" ditekan.

---

## 9 · ATURAN WAJIB · halaman pembuka "Fenomena Dunia Nyata"

Setiap topik **alur** wajib punya satu halaman pembuka yang dibuka **sebelum
S1 Peta &amp; Tujuan Pembelajaran pada TP pertama**. Tujuannya satu: murid
tahu untuk apa semua ini dipakai sebelum bertemu rumus, sehingga ia punya
alasan untuk menuntaskan topiknya.

### 9.1 · Berkasnya

```
konten/f-xyz/pembuka/index.html
```

`build.js` mendeteksinya sendiri dan menaruhnya di `katalog.json` sebagai
`topik.pembuka`. `app.js` lalu menampilkan dua hal tanpa disuruh:

1. Kartu **Fenomena Dunia Nyata** di paling atas halaman topik, di atas
   daftar Tujuan Pembelajaran.
2. Pengingat kecil di atas lembar **S1 pada TP pertama** yang menaut balik ke
   halaman pembuka.

Kalau berkasnya tidak ada, `node build.js` mencetak peringatan dengan nama
topiknya.

### 9.2 · Isinya

Kerangka yang dipakai F.MEK dan F.USE, tiga cerita lalu penutup:

| Bagian | Isi |
|---|---|
| Pembuka satu paragraf | satu kalimat yang mengikat ketiga cerita ke inti topik |
| 3 kartu fenomena | satu peristiwa **nyata, terkini, dan bisa dilihat murid**, masing-masing ditutup kotak `.miskon` berisi miskonsepsi yang diincar |
| Kartu simulasi | simulasi milik sendiri, ditanam dengan `<iframe class="berkas">` + `Buka penuh di tab baru ↗` |
| Kartu penutup | daftar &ldquo;yang akan kamu bisa&rdquo;, satu baris per TP |

Syarat isi:

- **Konkret dan terkini.** Sebutkan hal yang benar-benar ada sekarang —
  nama, angka, tahun. F.MEK memakai Whoosh (350 km/jam, 15 juta penumpang,
  kereta tercepat ASEAN 2026), motor ojol di tanjakan, dan crane proyek.
  F.USE memakai peralihan ojol ke motor listrik mulai 2027, PLTS atap, dan
  tangga asrama.
- **Periksa ulang angkanya.** Angka yang basi lebih buruk daripada tidak ada
  angka. Telusuri sumbernya sebelum ditulis, dan tulis tahunnya supaya
  ketahuan kapan perlu diperbarui.
- **Jangan mengajar di sini.** Tidak ada rumus, tidak ada soal, tidak ada
  nilai. Halaman ini hanya membuka selera.
- **Setiap kartu menyebut satu miskonsepsi** yang nanti dibongkar di TP-nya.

### 9.3 · Bahannya di media.json

```json
"topik": {
  "PEMBUKA": [
    { "tipe": "video",    "judul": "…", "yt": "KODE_YOUTUBE" },
    { "tipe": "simulasi", "judul": "…",
      "berkas": "media-f-xyz/simulasi/namanya.html" },
    { "tipe": "audio",    "judul": "Pembuka topik — dibacakan", "naskah": "…" },
    { "tipe": "bacaan",   "judul": "…", "berkas": "media-f-xyz/bacaan/namanya.html" }
  ],
  "L1": [ … ]
}
```

Keempat jenis wajib ada, simulasinya wajib milik sendiri, dan jalur berkasnya
dihitung dari **akar situs** — aturan yang sama dengan bagian 5.

### 9.4 · Pemeriksaannya

`python3 alat/periksa-media.py f-xyz` sekarang ikut menolak kalau:

- `konten/f-xyz/pembuka/index.html` tidak ada;
- `topik.PEMBUKA` kurang salah satu dari empat jenis bahan;
- simulasinya hanya dari situs luar;
- ada `berkas` yang jalurnya tidak ketemu dari akar situs.

Setelah itu buka halamannya di peramban dan pastikan simulasi di dalam
pembuka **benar-benar termuat** — gulirkan sampai bingkainya kelihatan,
jalankan animasinya, dan lihat angkanya berubah. Bingkai yang memuat 404
tetap elemen `<iframe>` yang sah.

---

## 10 · Istilah yang dipakai di seluruh dokumen

Dua istilah ini tidak boleh berubah-ubah. Pakai yang kanan, jangan yang kiri.

| Jangan | Pakai |
|---|---|
| Peta &amp; Janji | **Peta &amp; Tujuan Pembelajaran** |
| ramalan, ramalkan, meramalkan | **prediksi, prediksikan, memprediksi** |

Berlaku untuk seluruh teks yang dilihat murid: nama tahapan di `app.js`,
judul halaman, naskah soal, pembahasan, bacaan, dan panduan. Pengenal di
dalam kode (`id="q1_ramalan"`, `for="pr_ramal"`) boleh dibiarkan — murid
tidak melihatnya, dan menggantinya berisiko memutus penilaian.

Pemeriksaan cepat sebelum menyatakan selesai:

```bash
grep -rn "Janji" --include=*.html --include=*.js konten/ assets/ aset-*/ media-*/
grep -rniE "ramalan|ramalkan|meramalkan" --include=*.html konten/ aset-*/ media-*/ | grep -vE '(id|for|name)="'
```

Keduanya harus tidak menghasilkan apa pun.
