-- Skema basis data akun Fisika FIWA (Cloudflare D1).
-- Jalankan sekali lewat Console D1 di dasbor Cloudflare, atau:
--   npx wrangler d1 execute fiwa-physics --remote --file=skema.sql
-- Aman dijalankan ulang: semua perintah memakai IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS anggota (
  email       TEXT PRIMARY KEY,          -- huruf kecil semua, menjadi identitas
  nama        TEXT,                      -- diisi sendiri saat masuk pertama kali
  peran       TEXT NOT NULL,             -- 'siswa' | 'guru' | 'owner'
  status      TEXT NOT NULL,             -- 'menunggu' | 'aktif' | 'ditolak'
  kelas       TEXT,                      -- opsional, diisi guru
  kode        TEXT,                      -- kode aktivasi, hanya dipakai bila WAJIB_KODE menyala
  dibuat      INTEGER NOT NULL,
  diputus     INTEGER,                   -- kapan owner memutuskan
  oleh        TEXT,                      -- siapa yang memutuskan
  terakhir    INTEGER                    -- kapan terakhir masuk
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

-- Satu baris untuk tiap pengaturan yang boleh berubah tanpa menyunting kode.
CREATE TABLE IF NOT EXISTS pengaturan (
  kunci TEXT PRIMARY KEY,
  nilai TEXT NOT NULL
);

-- Owner disiapkan langsung supaya tidak ada ayam-dan-telur:
-- ia tidak perlu menunggu persetujuan siapa pun.
INSERT OR IGNORE INTO anggota (email, nama, peran, status, dibuat)
VALUES ('komaruddinmsi@gmail.com', 'Owner', 'owner', 'aktif', 0);
