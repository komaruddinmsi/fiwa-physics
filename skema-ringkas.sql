CREATE TABLE IF NOT EXISTS anggota (email TEXT PRIMARY KEY, nama TEXT, peran TEXT NOT NULL, status TEXT NOT NULL, kelas TEXT, kode TEXT, dibuat INTEGER NOT NULL, diputus INTEGER, oleh TEXT, terakhir INTEGER);
CREATE INDEX IF NOT EXISTS anggota_status ON anggota (status, peran);
CREATE TABLE IF NOT EXISTS progres (email TEXT NOT NULL, tp TEXT NOT NULL, data TEXT NOT NULL, diubah INTEGER NOT NULL, PRIMARY KEY (email, tp));
CREATE INDEX IF NOT EXISTS progres_tp ON progres (tp);
CREATE TABLE IF NOT EXISTS pengaturan (kunci TEXT PRIMARY KEY, nilai TEXT NOT NULL);
