-- Jalankan di Console D1 Cloudflare, SATU PERNYATAAN PER KIRIM.
-- Console D1 hanya menjalankan satu perintah tiap kali tombol kirim ditekan;
-- menempelkan seluruh berkas sekaligus tidak menjalankan apa pun.

-- Pernyataan 1 dari 3
CREATE TABLE IF NOT EXISTS bimbing (guru TEXT NOT NULL, murid TEXT NOT NULL, dibuat INTEGER NOT NULL, oleh TEXT, PRIMARY KEY (guru, murid));

-- Pernyataan 2 dari 3
CREATE INDEX IF NOT EXISTS bimbing_murid ON bimbing (murid);

-- Pernyataan 3 dari 3 — memastikan kolom catatan penilaian ada pada progres
ALTER TABLE progres ADD COLUMN oleh TEXT;
