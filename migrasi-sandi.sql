-- Migrasi untuk pemasangan yang tabel anggota-nya sudah ada sebelum kata sandi dipakai.
-- Jalankan sekali di Console D1. Bila tabelnya memang baru dibuat dari skema.sql,
-- berkas ini tidak perlu dijalankan.
--
-- Kedua perintah di bawah akan melaporkan "duplicate column name" bila kolomnya
-- sudah ada. Pesan itu aman diabaikan: artinya migrasinya memang sudah pernah jalan.

ALTER TABLE anggota ADD COLUMN sandi TEXT;
ALTER TABLE anggota ADD COLUMN garam TEXT;
