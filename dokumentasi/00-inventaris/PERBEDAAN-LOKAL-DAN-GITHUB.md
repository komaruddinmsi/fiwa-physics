# Perbedaan sumber lokal dan GitHub

Perbandingan memakai sidik blob Git atas seluruh berkas lokal dan pohon GitHub pada commit `a6794d774bb88ca39a97199711448254b678b553`. Folder lokal tidak memiliki `.git`, sehingga status branch, perubahan belum dicommit dan hubungan dengan clone Git tidak tersedia.

| Hasil | Jumlah |
| --- | --- |
| Berkas lokal proyek | 238 |
| Berkas di pohon GitHub | 239 |
| Sama pada jalur dan isi | 233 |
| Jalur sama tetapi isi berbeda | 1 |
| Hanya pada jalur lokal | 4 |
| Hanya pada jalur GitHub | 5 |

Empat PDF `fundamentals-of-physics-halliday-1.pdf` hingga `-4.pdf` berada di `alat/` secara lokal, sedangkan GitHub menempatkannya di `aset-ebook/`. Keempat pasangan identik isinya. Halaman buku menunjuk ke `aset-ebook/`, sehingga lokasi lokalnya belum selaras. Ini temuan salinan lokal; tidak membuktikan PDF situs produksi hilang.

`app.js` di akar hanya ada di GitHub. Titik masuk yang aktif ialah `index.html` → `assets/akun.js` → `assets/app.js`, sehingga keberadaan dua nama app.js harus dibedakan saat pembaruan.

`aset-f-use/L04_Tanya-Jawab-Topik-F.USE.html` berbeda isi antara lokal dan GitHub; asal atau maksud perbedaannya belum ditetapkan. Tidak ada salinan yang ditimpa.

`index.html`, `assets/app.css`, `assets/app.js` dan `assets/akun.js` yang dilayani situs cocok byte demi byte dengan berkas lokal; berkas lokal tersebut juga cocok dengan pohon GitHub. Kecocokan empat berkas bukan bukti seluruh deployment atau basis data identik dengan commit ini.
