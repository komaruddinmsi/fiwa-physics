-- Skema basis data akun Fisika FIWA (Cloudflare D1).
-- Jalankan sekali lewat Console D1 di dasbor Cloudflare.
-- Aman dijalankan ulang: semua perintah memakai IF NOT EXISTS.
--
-- Berkas ini sengaja tidak memuat alamat surel siapa pun, karena repositori
-- ini publik. Cara mengangkat pemilik situs ada di PANDUAN-AKUN.md Langkah 6.

CREATE TABLE IF NOT EXISTS anggota (
  email       TEXT PRIMARY KEY,          -- huruf kecil semua, menjadi identitas
  nama        TEXT,
  peran       TEXT NOT NULL,             -- 'siswa' | 'guru' | 'owner'
  status      TEXT NOT NULL,             -- 'menunggu' | 'aktif' | 'ditolak'
  kelas       TEXT,
  sandi       TEXT,                      -- turunan PBKDF2-SHA256 dari kata sandi, bukan sandinya
  garam       TEXT,                      -- garam acak 16 bita untuk turunan di atas
  kode        TEXT,                      -- kode aktivasi, dipakai bila WAJIB_KODE menyala
  dibuat      INTEGER NOT NULL,
  diputus     INTEGER,
  oleh        TEXT,
  terakhir    INTEGER
);

CREATE INDEX IF NOT EXISTS anggota_status ON anggota (status, peran);

-- Progres belajar mengikuti akun, bukan peramban.
CREATE TABLE IF NOT EXISTS progres (
  email   TEXT NOT NULL,
  tp      TEXT NOT NULL,                 -- slug TP, misalnya 'f-use-1-pra'
  data    TEXT NOT NULL,                 -- JSON: { ev, tier, s14, riwayat }
  diubah  INTEGER NOT NULL,
  PRIMARY KEY (email, tp)
);

CREATE INDEX IF NOT EXISTS progres_tp ON progres (tp);

CREATE TABLE IF NOT EXISTS pengaturan (
  kunci TEXT PRIMARY KEY,
  nilai TEXT NOT NULL
);

-- Pembimbingan: satu murid boleh punya banyak guru, satu guru banyak murid.
-- Hanya pemilik situs yang mengubah isinya.
CREATE TABLE IF NOT EXISTS bimbing (
  guru   TEXT NOT NULL,                -- surel akun berperan 'guru'
  murid  TEXT NOT NULL,                -- surel akun berperan 'siswa'
  dibuat INTEGER NOT NULL,
  oleh   TEXT,                         -- surel pemilik yang menetapkan
  PRIMARY KEY (guru, murid)
);

CREATE INDEX IF NOT EXISTS bimbing_murid ON bimbing (murid);
