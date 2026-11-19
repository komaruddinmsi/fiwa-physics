-- OPSIONAL. Function membuat tabel ini sendiri saat pertama dipakai, jadi berkas ini tidak wajib dijalankan.
-- Bila ingin membuatnya lebih dulu: Console D1 Cloudflare, SATU PERNYATAAN PER KIRIM.

-- Pernyataan 1 dari 2
CREATE TABLE IF NOT EXISTS lembar (email TEXT NOT NULL, kunci TEXT NOT NULL, data TEXT NOT NULL, skor REAL, selesai INTEGER NOT NULL DEFAULT 0, terisi INTEGER, total INTEGER, epoch INTEGER NOT NULL DEFAULT 0, diubah INTEGER NOT NULL, oleh TEXT, PRIMARY KEY (email, kunci));

-- Pernyataan 2 dari 2
CREATE INDEX IF NOT EXISTS lembar_kunci ON lembar (kunci);
