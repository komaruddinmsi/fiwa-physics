# alat/ — pembangun halaman tahapan

```
alat/
  bangun.py          mesin: menulis seluruh halaman tahapan satu topik
  bank/data_tp.py    identitas topik, TP, sub-bab, miskonsepsi, bekal
  bank/bank_s2.py    bank Gerbang Prasyarat
  bank/bank_s11.py   bank Latihan Bertingkat
  bank/bank_s13.py   bank Gerbang Ketuntasan
  bank/gerbang.json  naskah butir gerbang kelas, hasil ekstraksi dari RPP
  bacaan.py          menulis halaman bacaan konsep milik sendiri
  periksa-media.py   memeriksa kelengkapan bahan pendukung tiap TP
  sumber/            worksheet asli yang dipakai apa adanya sebagai S7
```

Menjalankan:

```bash
cd alat && python3 bangun.py && python3 bacaan.py
cd ..   && node build.js
python3 alat/periksa-media.py f-mek     # wajib bersih sebelum selesai
```

`bangun.py` menulis ke `konten/<slug-topik>/` dan `aset-<slug-topik>/`.
Ia menimpa tanpa bertanya, jadi jangan menyunting halaman hasilnya langsung —
sunting banknya, lalu bangun ulang.

Untuk topik baru: salin `bank/data_tp.py` dan ketiga bank soalnya, ganti
isinya, lalu sesuaikan nama folder di bagian atas `bangun.py`.

Panduan lengkap: `../PANDUAN-TOPIK-BARU.md`.

- `ebook.py` — menulis halaman topik Kumpulan E-Book (jalur Olimpiade) dari daftar `BUKU`. Lihat PANDUAN-TOPIK-BARU.md bagian 8.7.
- `pecah-pdf.py` — memotong PDF besar jadi bagian di bawah 25 MiB, lengkap dengan bookmark per bagian. Dipakai untuk Halliday (1.450 halaman → 4 berkas).
