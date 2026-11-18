# Folder rekaman suara

Letakkan berkas `.mp3` atau `.ogg` di sini, lalu sebut namanya di `media-f-use/media.json`:

```json
{
  "tipe": "audio",
  "judul": "Rangkuman tiga menit",
  "berkas": "media-f-use/audio/rangkuman-tp1.mp3"
}
```

Saran nama berkas: `<tahapan>-<tp>.mp3`, misalnya `s10-tp1-rangkuman.mp3`.

Naskah yang sekarang dibacakan peramban ada di `media.json` pada bagian `"naskah"`.
Teks itu bisa langsung Anda pakai saat merekam. Sesudah rekamannya siap,
ganti `"naskah"` menjadi `"berkas"` pada bahan yang bersangkutan.

Saran teknis: satu menit suara mono 128 kbps berukuran sekitar 1 MB.
Usahakan tiap rekaman di bawah 5 MB supaya cepat dimuat di jaringan sekolah.
