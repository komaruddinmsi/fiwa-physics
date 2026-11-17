# Fisika FIWA — `fiwa-physics.pages.dev`

Situs alur belajar tuntas Fisika, Fitrah Islamic World Academy.
Mesin alurnya CMS FIMS: 18 tahapan per TP (S1–S14) ditambah empat lapis topik (L1–L4).

## Isi

| Jalur | Isi |
|---|---|
| `index.html` · `assets/` | kerangka situs dan mesin alur |
| `konten/f-use/` | unit **F.USE · Usaha & Energi** — dua TP, 16 tahapan masing-masing, 4 lapis topik |
| `aset-f-use/` | PDF modul, lembar bekal, dek kelas, serta latihan TKA dan CBT |
| `katalog.json` | daftar unit, **dihasilkan `build.js`** |
| `build.js` | memindai `konten/` lalu menulis `katalog.json` |

## Menambah unit baru

1. Buat `konten/<topik>/<tp>/<TAHAPAN>/index.html`, tahapan `S1`–`S14`.
   Lapis topik di `konten/<topik>/L1`–`L4`.
2. Beri `konten/<topik>/topik.json` dan `konten/<topik>/<tp>/tp.json`.
3. Jalankan `node build.js`, atau biarkan Cloudflare menjalankannya saat terbit.

Setiap subfolder di dalam topik yang bukan `L1`–`L4` dibaca sebagai TP. Berkas
bersama seperti PDF karena itu diletakkan **di luar** `konten/`.

## Halaman tahapan melapor ke mesin

```js
parent.postMessage({fims:'skor', skor:85}, '*')   // berskor
parent.postMessage({fims:'selesai'}, '*')          // tanpa skor
```

Tanpa laporan itu status tidak pernah naik. Progres murid tersimpan di
`localStorage` perangkat masing-masing, kunci `va-fims-v1`.

## Identitas

Lambang di `assets/logo.svg`, `logo-dark.svg`, dan `logo-mark.svg` adalah lambang
sementara. Ganti ketiganya dengan lambang resmi sekolah bila sudah ada; ukuran
dan nama berkasnya biarkan sama. Warna situs diatur pada `:root` di
`assets/app.css`.

## Yang tidak boleh masuk ke sini

Cloudflare Pages menyajikan seluruh berkas repo kepada siapa pun yang menebak
alamatnya. Kunci jawaban, rubrik, dan log tinjauan **tidak pernah** diletakkan di
repo ini; semuanya disimpan di komputer sekolah.
