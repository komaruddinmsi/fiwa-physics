/* Vertical Academy — mesin alur Pembelajaran Tuntas (CMS FIMS), versi statis.
   Data kurikulum: katalog.json (dibuat build.js). Progres siswa: localStorage perangkat ini.
   Halaman tahapan boleh melapor skor:  parent.postMessage({fims:'skor', skor:85}, '*')
   atau selesai tanpa skor:              parent.postMessage({fims:'selesai'}, '*')            */
(function () {
'use strict';

/* ---------- dwibahasa: teks antarmuka Indonesia (asal) dan Inggris ---------- */
const EN = {
"Sembunyikan": "Hide",
"Tampilkan": "Show",
"Butuh penilaian": "Awaiting grading",
"Memuat antrean penilaian…": "Loading the grading queue…",
"Tidak ada yang menunggu penilaianmu.": "Nothing is awaiting your grading.",
"Tidak dapat memuat antrean penilaian.": "Could not load the grading queue.",
"Murid di bawah ini sudah sampai pada tahapan yang nilainya diisi guru. Yang paling lama menunggu berada di atas.": "The students below have reached a stage whose score is entered by a teacher. The longest waiting are at the top.",
"Tahapan": "Stage",
"Menunggu sejak": "Waiting since",
"Nilai": "Grade",
"Skor 0–100": "Score 0–100",
"Simpan": "Save",
"Tersimpan.": "Saved.",
"Gagal menyimpan nilai.": "Could not save the grade.",
"Skor harus 0–100.": "The score must be 0–100.",
"Hanya murid bimbinganmu yang tampil di sini. Pemilik situs melihat seluruh murid.": "Only your own mentees appear here. The site owner sees every student.",
"Fenomena Dunia Nyata": "Real-World Phenomena",
"Mulai dari sini": "Start here",
"Lihat dulu untuk apa semua ini dipakai, sebelum masuk ke tujuan pembelajaran pertama.": "See what all of this is for before entering the first learning objective.",
"Buka pembuka topik": "Open the topic opener",
"Belum membaca pembukanya? Lihat fenomena dunia nyata topik ini lebih dulu.": "Haven't read the opener? Look at this topic's real-world phenomena first.",
"Halaman pembuka belum diunggah.": "The opener page has not been uploaded yet.",
"Kembali ke daftar TP": "Back to the objective list",
"Lanjut ke": "Continue to",
"Paket soal": "Question packs",
"Paket": "Pack",
"%s paket": "%s packs",
"1 paket": "1 pack",
"%s topik · %s paket": "%s topics · %s packs",
"1 topik · %s paket": "1 topic · %s packs",
"Belum ada paket soal pada topik ini.": "No question packs in this topic yet.",
"Penyisihan": "Preliminary",
"Semifinal": "Semifinal",
"Final": "Final",
"Lainnya": "Other",
"%s soal": "%s questions",
"Buka penuh di tab baru": "Open full in a new tab",
"Dokumen ini berdiri sendiri: nilai dan pembahasan muncul di dalam lembar itu sendiri, tidak masuk ke progres jalur belajar.": "This document stands alone: the score and worked solutions appear inside the sheet itself and do not enter the learning-path progress.",
"Kembali ke daftar paket": "Back to the pack list",
"Dokumen tidak ditemukan.": "Document not found.",
"Peta & Tujuan Pembelajaran": "Map & Learning Objective",
"Gerbang Prasyarat": "Prerequisite Gate",
"Penguatan Prasyarat": "Prerequisite Reinforcement",
"Remediasi Prasyarat": "Prerequisite Remediation",
"Pemantik & Prakonsepsi": "Hook & Preconceptions",
"Penyajian Konsep Awal": "First Concept Exposure",
"Pembahasan Prakonsepsi": "Preconception Debrief",
"Inti Terbimbing": "Guided Core",
"Praktik Terstruktur": "Structured Practice",
"Gerbang Formatif Kelas": "Class Formative Gate",
"Diferensiasi T1–T4": "Differentiation T1–T4",
"Konsolidasi & Jangkar": "Consolidation & Anchor",
"Latihan Bertingkat": "Tiered Practice",
"Tugas Kinerja": "Performance Task",
"Gerbang Ketuntasan TP": "LO Mastery Gate",
"Pengulangan Berjarak": "Spaced Retrieval",
"Dibuka": "Opened",
"≥80% lanjut · 60–79% → S2b · <60% → S2c": "≥80% proceed · 60–79% → S2b · <60% → S2c",
"Ulang S2 satu kali": "Retake S2 once",
"Ulang S2": "Retake S2",
"Terkirim (tidak dinilai)": "Submitted (ungraded)",
"Cek sisipan terjawab": "Embedded checks answered",
"Dipimpin guru": "Teacher-led",
"Lembar kerja terisi": "Worksheet completed",
"≥80% benar": "≥80% correct",
"Sesuai cabang S8": "Per the S8 branch",
"Jangkar terkirim": "Anchor submitted",
"Benar 3 dari 4 (≥75%) · H+0–H+2": "3 of 4 correct (≥75%) · D+0–D+2",
"Minimal T3 (dinilai guru) · H+1–H+5": "At least T3 (teacher-graded) · D+1–D+5",
"Butir baru, sekali jalan · H+2–H+7": "Fresh items, one attempt · D+2–D+7",
"H+14, +30, +60 · gagal → turun": "D+14, +30, +60 · fail → drop",
"Kuis Blok": "Block Quiz",
"Setiap 2–4 TP": "Every 2–4 LOs",
"Muara Topik": "Topic Synthesis",
"Setelah TP terakhir": "After the final LO",
"Tes Topik": "Topic Test",
"Akhir topik": "End of topic",
"Tantangan Mata Pelajaran": "Subject Challenge",
"Berkala, lintas topik": "Periodic, across topics",
"Fase 0 · Pra-KBM": "Phase 0 · Pre-class",
"Fase 1 · KBM": "Phase 1 · In class",
"Fase 2 · Pasca-KBM": "Phase 2 · Post-class",
"Belum Mulai": "Not Started",
"Siap": "Ready",
"Mencoba": "Attempting",
"Akrab": "Familiar",
"Mahir": "Proficient",
"Tuntas": "Mastered",
" Stabil": " Stable",
"Kurikulum Nasional · persiapan TKA": "Indonesian national curriculum · TKA preparation",
"OSN · pembinaan olimpiade fisika": "OSN · physics olympiad training",
"Seleksi sekolah hingga nasional": "From school selection to the national round",
"PHYSICS OLYMPIAD": "PHYSICS OLYMPIAD",
"Kelas 9–10 · jalur internasional": "Grades 9–10 · international track",
"Kelas 11–12 · jalur internasional": "Grades 11–12 · international track",
"Fase E–F · jalur nasional": "Phases E–F · national track",
"Hanya untuk skor S2 60–79%": "Only for an S2 score of 60–79%",
"Hanya untuk skor S2 di bawah 60%": "Only for an S2 score below 60%",
"Lulus Gerbang Prasyarat (S2 ≥ 80%) dulu": "Pass the Prerequisite Gate (S2 ≥ 80%) first",
"Kirim prakonsepsi S3 sebelum tatap muka": "Submit the S3 preconceptions before the lesson",
"Kerjakan Gerbang Formatif S8 di kelas": "Sit the S8 Class Formative Gate in class",
"Kerjakan Latihan Bertingkat S11 dulu": "Do the S11 Tiered Practice first",
"Kerjakan S11 dulu": "Do S11 first",
"Selesaikan dulu %s · %s": "Finish %s · %s first",
"Tugas Kinerja S12 harus dinilai minimal T3": "The S12 Performance Task must be graded at least T3",
"Kuis tertunda dibuka %s (H+2 setelah S11)": "The delayed quiz opens %s (D+2 after S11)",
"Sudah dikerjakan (sekali jalan). Gagal? Ulangi S11 dulu": "Already attempted (one attempt only). Failed? Redo S11 first",
"Terbuka setelah status Tuntas": "Opens once the status is Mastered",
"Tiga interval lulus: Tuntas Stabil": "Three intervals passed: Mastered & Stable",
"Interval %s jatuh tempo %s": "Interval %s is due %s",
"Belajar Fisika sampai tuntas": "Learning physics to mastery",
"Tiga jalur, satu cara kerja: setiap tujuan pembelajaran ditempuh bertahap dari Pra-KBM sampai Pasca-KBM, dan baru dinyatakan tuntas bila lulus gerbang akhirnya.": "Three tracks, one way of working: every learning objective is walked through stage by stage, from pre-class to post-class, and counts as mastered only once its final gate is passed.",
"Pilih jalur": "Choose a track",
"Lanjutkan belajar": "Continue learning",
"Mulai": "Start",
"Topik lain": "Other topics",
"Segera hadir": "Coming soon",
"%s topik · %s TP": "%s topics · %s LOs",
"1 topik · %s TP": "1 topic · %s LOs",
"1 TP": "1 LO",
"1 TP Tuntas": "1 LO mastered",
"%s TP Tuntas": "%s LOs mastered",
"%s dari %s TP Tuntas": "%s of %s LOs mastered",
"%s TP": "%s LOs",
"Fase ": "Phase ",
"Topik": "Topics",
"Materi jalur ini sedang disiapkan. Jalur yang sudah terbuka bisa dilihat di <a href=\"#\">beranda</a>.": "Materials for this track are being prepared. The tracks already open are listed on the <a href=\"#\">home page</a>.",
"Guru: tambahkan folder topik di <span class=\"mono\">konten/</span> dengan <span class=\"mono\">\"jalur\": \"%s\"</span> pada <span class=\"mono\">topik.json</span>.": "Teacher: add a topic folder under <span class=\"mono\">konten/</span> with <span class=\"mono\">\"jalur\": \"%s\"</span> in its <span class=\"mono\">topik.json</span>.",
"Tujuan Pembelajaran": "Learning Objectives",
"Lapis topik": "Topic layers",
"Belum ada TP.": "No learning objectives yet.",
"Belum diunggah": "Not uploaded yet",
"Belum diunggah.": "Not uploaded yet.",
"Beranda": "Home",
"Status turun ke Mahir: pengulangan berjarak gagal. Jadwal diulang dari H+14.": "Status dropped to Proficient: a spaced retrieval was failed. The schedule restarts at D+14.",
"Tier T%s: perlu pendampingan pada konteks baru, bukan tambahan latihan soal.": "Tier T%s: needs coaching on unfamiliar contexts, not more practice questions.",
"Kelengkapan: tahapan rangka belum diunggah — %s.": "Completeness: core stages not yet uploaded — %s.",
"Jadwal pengulangan berjarak (S14)": "Spaced retrieval schedule (S14)",
"Interval": "Interval",
"Hari": "Day",
"Jatuh tempo": "Due",
"Hasil": "Result",
"Interval %s": "Interval %s",
"berikutnya": "next",
"lulus": "passed",
"gagal": "failed",
"Tahapan %s belum diunggah.": "Stage %s has not been uploaded.",
"Lulus apabila: %s": "Passes when: %s",
"Mode guru: tahapan ini masih terkunci untuk siswa (%s).": "Teacher mode: this stage is still locked for students (%s).",
"Tandai bukti terkirim": "Mark evidence submitted",
"Tier diisi guru (rubrik T1–T4).": "The tier is set by the teacher (T1–T4 rubric).",
"Skor (%)": "Score (%)",
"Simpan skor": "Save score",
"Terisi otomatis bila halaman kuis mengirim skor.": "Filled in automatically when the quiz page reports a score.",
"Tandai selesai": "Mark done", "Tandai sudah mengikuti": "Mark as attended", "Mode guru. Siswa tidak dapat mengetik skornya sendiri.": "Teacher mode. Students cannot type their own score.", "Skor tahapan ini dinilai dan diisi gurumu di kelas.": "Your teacher marks and enters the score for this stage in class.", "Skormu terisi sendiri begitu kamu menekan tombol periksa pada lembar di atas. Tidak ada angka yang bisa diketik sendiri di sini.": "Your score is filled in automatically the moment you press the check button on the sheet above. There is no figure to type in here.", "Skor tercatat: %s": "Score on record: %s", "Langkah berikutnya": "Next step", "Semua butir sudah benar.": "Every item is correct.", "Benar %s dari %s butir.": "%s of %s items correct.", "%s nomor masih salah": "%s items are still wrong", "Skormu %s, ambangnya %s. Kurang %s poin lagi.": "Your score is %s and the threshold is %s. You are %s points short.", "Buka kembali nomor-nomor itu pada lembar di atas, kerjakan ulang langkahnya, lalu periksa lagi. Kunci jawaban sengaja tidak ditampilkan.": "Open those items again on the sheet above, work through them afresh, then check once more. The answer key is deliberately not shown.", "Ke %s · %s": "Go to %s · %s", "%s · %s": "%s · %s", "Sesudah ini: kerjakan ulang Gerbang Prasyarat": "Next: sit the Prerequisite Gate again", "Penguatan dan remediasi tidak mengubah statusmu dengan sendirinya. Status baru naik setelah kamu lulus Gerbang Prasyarat, yaitu skor minimal 80%. Kerjakan ulang gerbangnya sekarang.": "Reinforcement and remediation do not change your status by themselves. Your status only rises once you pass the Prerequisite Gate with at least 80%. Sit the gate again now.",
"Panel guru · %s": "Teacher panel · %s",
"Tier dari rubrik S9/S12": "Tier from the S9/S12 rubric",
"Hapus progres TP ini": "Clear progress for this LO",
"Selisih S11 − S13: %s · Riwayat status: %s": "S11 − S13 gap: %s · Status history: %s",
"%s poin": "%s points",
"belum ada data": "no data yet",
"Papan guru": "Teacher board", "Memuat papan kelas…": "Loading the class board…", "Tidak dapat memuat papan kelas.": "Could not load the class board.", "Belum ada murid aktif. Setujui anggota lebih dulu di laman Anggota.": "No active students yet. Approve members on the Members page first.", "Murid": "Students", "Warna = status, angka = tier. Baris paling atas adalah progres pada perangkat ini; baris berikutnya diambil dari akun tiap murid.": "Colour = status, number = tier. The top row is progress on this device; the rows below come from each student's account.", "Anggota": "Members", "Keluar": "Sign out", "Guru": "Teacher", "Siswa": "Student",
"Kelengkapan & posisi": "Completeness & standing",
"Kelengkapan tahapan": "Stage completeness",
"✕ = tahapan rangka (S1, S2, S3, S5, S8, S10, S12, S13, S14) belum diunggah. TP dengan ✕ belum boleh terbit.": "✕ = a core stage (S1, S2, S3, S5, S8, S10, S12, S13, S14) has not been uploaded. An LO with any ✕ is not ready to publish.",
"Papan posisi": "Standing board",
"Warna = status, angka = tier. Versi statis hanya membaca progres di perangkat ini. Papan seluruh kelas butuh login dan database (Tahap 6 panduan).": "Colour = status, number = tier. This static version only reads progress stored on this device. A whole-class board needs sign-in and a database (Stage 6 of the guide).",
"Simulasi waktu": "Time simulation",
"Untuk uji alur kuis tertunda (H+2) dan pengulangan (H+14). Sekarang digeser %s hari.": "For testing the delayed-quiz (D+2) and spaced-retrieval (D+14) flows. Currently shifted by %s days.",
"+2 hari": "+2 days",
"+14 hari": "+14 days",
"Kembali ke hari ini": "Back to today",
"Siswa": "Student",
"Perangkat ini": "This device",
"Terbit": "Publish",
"Belum": "Not yet",
"TP": "LO",
"Belajar": "Learn",
"Papan Guru": "Teacher Board",
"Mode guru": "Teacher mode",
"Alur Konten Pembelajaran Tuntas · CMS FIMS · Fitrah Islamic World Academy. Progres belajar tersimpan pada akunmu.": "Mastery Learning Content Flow · CMS FIMS · Fitrah Islamic World Academy. Your progress is saved to your account.",
"Bahan pendukung": "Supporting material", "Memuat bahan pendukung…": "Loading supporting material…", "Belum ada bahan pendukung untuk tahapan ini.": "No supporting material for this stage yet.", "Gerbang penilaian — bahan bantu sengaja tidak disediakan.": "Assessment gate — support material is withheld on purpose.", "Video": "Video", "Audio": "Audio", "Simulasi": "Simulation", "Bacaan": "Reading", "Tautan": "Link", "Buka di YouTube": "Open on YouTube", "Buka penuh di tab baru": "Open full size in a new tab", "Sumber luar": "External source",
"Bahan ini dari situs luar. Bila kotaknya tetap kosong, situs itu menolak ditampilkan di dalam halaman — pakai tautan di atas.": "This material comes from an external site. If the box stays empty, that site refuses to be shown inside a page — use the link above.", "Putar": "Play", "Jeda": "Pause", "Lanjut": "Resume", "Hentikan": "Stop", "Peramban ini belum dapat membacakan naskah. Silakan baca teksnya langsung.": "This browser cannot read the script aloud. Please read the text instead.", "Naskah dibacakan oleh peramban. Guru dapat menggantinya dengan rekaman suara sendiri.": "The script is read aloud by the browser. A teacher can replace it with their own recording.", "Bahan pendukung belum diatur untuk topik ini.": "Supporting material has not been set up for this topic yet.", "Memuat katalog…": "Loading the catalogue…",
"katalog.json belum ada. Jalankan <span class=\"mono\">node build.js</span> (Cloudflare menjalankannya otomatis).": "katalog.json is missing. Run <span class=\"mono\">node build.js</span> (Cloudflare runs it automatically).",
"Fisika FIWA — beranda": "Fisika FIWA — home",
"Tuntaskan dulu %s · %s": "Complete %s · %s first",
"Tuntaskan dulu %s": "Complete %s first",
"Lapis ini belum terbuka.": "This layer is not open yet.",
"TP ini belum terbuka.": "This objective is not open yet.",
"Kembali ke daftar TP": "Back to the objective list",
"Lanjut ke": "Continue to",
"Tujuan Pembelajaran ditempuh berurutan. TP berikutnya terbuka sendiri begitu TP sebelumnya berstatus Tuntas.": "Learning objectives are taken in order. The next one opens by itself once the previous one reaches Mastered.",
"Latihan Unit Test": "Unit Test Practice",
"Soal Unit Test": "Unit Test",
"berlatih dulu · tidak dinilai": "practise first · not graded",
"sekali jalan · dinilai": "one attempt · graded",
"Redaksi soal pada keduanya berbeda, tetapi langkah penyelesaiannya sama. Kerjakan latihannya sampai lancar, baru buka soal yang dinilai. Keduanya tidak memerlukan kalkulator.": "The two sets are worded differently but solved the same way. Work through the practice set until it flows, then open the graded one. Neither needs a calculator.",
"%s nomor masih salah": "%s item numbers still wrong",
"%s · %s": "%s · %s",
"Bahan pendukung belum diatur untuk topik ini.": "No supporting material has been set up for this topic yet.",
"Belum ada murid aktif. Setujui anggota lebih dulu di laman Anggota.": "No active students yet. Approve members on the Members page first.",
"Benar %s dari %s butir.": "%s of %s items correct.",
"Buka di YouTube": "Open on YouTube",
"Buka kembali nomor-nomor itu pada lembar di atas, kerjakan ulang langkahnya, lalu periksa lagi. Kunci jawaban sengaja tidak ditampilkan.": "Go back to those numbers on the sheet above, redo the steps, then check again. The answer key is deliberately not shown.",
"Buka penuh di tab baru": "Open full size in a new tab",
"Hentikan": "Stop",
"Jeda": "Pause",
"Ke %s · %s": "Go to %s · %s",
"Langkah berikutnya": "Next step",
"Memuat bahan pendukung…": "Loading supporting material…",
"Memuat papan kelas…": "Loading the class board…",
"Mode guru. Siswa tidak dapat mengetik skornya sendiri.": "Teacher mode. Students cannot type their own score.",
"Murid": "Student",
"Penguatan dan remediasi tidak mengubah statusmu dengan sendirinya. Status baru naik setelah kamu lulus Gerbang Prasyarat, yaitu skor minimal 80%. Kerjakan ulang gerbangnya sekarang.": "Reinforcement and remediation do not change your status by themselves. Your status only rises once you pass the Prerequisite Gate, that is a score of at least 80%. Take the gate again now.",
"Naskah dibacakan oleh peramban. Guru dapat menggantinya dengan rekaman suara sendiri.": "The text is read aloud by the browser. A teacher can replace this with their own recording.",
"Peramban ini belum dapat membacakan naskah. Silakan baca teksnya langsung.": "This browser cannot read the text aloud. Please read the text itself.",
"Putar": "Play",
"Semua butir sudah benar.": "Every item is correct.",
"Sesudah ini: kerjakan ulang Gerbang Prasyarat": "Next: take the Prerequisite Gate again",
"Skor tahapan ini dinilai dan diisi gurumu di kelas.": "Your teacher marks and enters the score for this stage in class.",
"Skor tercatat: %s": "Score recorded: %s",
"Skormu %s, ambangnya %s. Kurang %s poin lagi.": "Your score is %s, the threshold is %s. %s points short.",
"Skormu terisi sendiri begitu kamu menekan tombol periksa pada lembar di atas. Tidak ada angka yang bisa diketik sendiri di sini.": "Your score fills in by itself as soon as you press the check button on the sheet above. No number can be typed in here.",
"Sumber luar": "External source",
"Tandai sudah mengikuti": "Mark as attended",
"Tidak dapat memuat papan kelas.": "Could not load the class board.",
"Warna = status, angka = tier. Baris paling atas adalah progres pada perangkat ini; baris berikutnya diambil dari akun tiap murid.": "Colour = status, number = tier. The top row is the progress on this device; the rows below come from each student's account."

};
Object.assign(EN, {
"Atur ulang dokumen murid": "Reopen a student document",
"Murid terlanjur menekan Selesai, atau dokumennya sudah diskor? Pilih muridnya, lalu topiknya, lalu klik dokumen yang mau dibuka ulang: tahapan S1–S14, lapis L1–L4, paket (termasuk PRI UIN), atau dokumen isian lain. Hanya hasil dan isian dokumen itu yang dihapus; dokumen lain dan progres TP tetap utuh. Murid bisa langsung mengerjakan ulang.": "A student pressed Finish by accident, or the document was already scored? Pick the student, then the topic, then click the document to reopen: stages S1–S14, layers L1–L4, packages (including PRI UIN), or any other fillable document. Only that document’s result and answers are removed; other documents and the LO progress stay intact. The student can redo it right away.",
"Pilih murid…": "Choose a student…",
"Topik yang dikerjakan": "Topic worked on",
"Pilih topik…": "Choose a topic…",
"%s dokumen": "%s documents",
"1 dokumen": "1 document",
"Murid ini belum mengerjakan topik apa pun.": "This student has not worked on any topic yet.",
"Pilih topik di atas untuk melihat dokumen yang sudah dikerjakan murid ini.": "Choose a topic above to see the documents this student has worked on.",
"Tidak ada lagi dokumen terisi pada topik ini.": "No filled-in documents left in this topic.",
"Murid ini belum punya hasil tercatat.": "This student has no recorded results yet.",
"Lapis, paket, dan dokumen isian lain": "Layers, packages and other fillable documents",
"Dokumen lain": "Other documents",
"Memuat dokumen isian…": "Loading fillable documents…",
"Dokumen isian (lapis, paket) belum dapat dimuat. Tahapan di atas tetap bisa dibuka ulang.": "Fillable documents (layers, packages) could not be loaded. The stages above can still be reopened.",
"hasil dokumen (skor %s)": "document result (score %s)",
"hasil dokumen (selesai)": "document result (finished)",
"terisi %s": "filled %s",
"isian yang sudah diisi (%s)": "answers already entered (%s)",
"Tetap utuh: dokumen lain dan progres TP murid.": "Kept: all other documents and the student’s LO progress.",
"Buka ulang %s untuk %s?": "Reopen %s for %s?",
"Dihapus: %s": "Removed: %s",
"Tetap utuh: dokumen lain dan progres TP ini.": "Kept: all other documents and this LO’s progress.",
"Status %s: %s → %s": "Status %s: %s → %s",
"Status TP tidak berubah.": "The LO status does not change.",
"Terkunci lagi untuk murid: %s": "Locked again for the student: %s",
"Terbuka lagi untuk murid: %s": "Unlocked again for the student: %s",
"Alasan (opsional, terlihat oleh murid)": "Reason (optional, visible to the student)",
"Ya, buka ulang": "Yes, reopen",
"Batal": "Cancel",
"%s sudah dibuka ulang untuk %s. Murid melihatnya paling lambat 45 detik lagi.": "%s has been reopened for %s. The student sees it within 45 seconds.",
"Gagal membuka ulang.": "Could not reopen.",
"%s membuka ulang tahapan ini pada %s%s. Kerjakan lagi dari awal.": "%s reopened this stage on %s%s. Please do it again from the start.",
"Gurumu": "Your teacher",
"Hapus progres TP ini (hanya milikmu)": "Delete this LO’s progress (yours only)",
"skor %s%": "score %s%",
"tanda selesai": "completion mark",
"bukti terkirim": "evidence sent",
"dan tier T%s": "and tier T%s",
"hasil pengulangan terakhir (%s)": "latest repeat result (%s)",
"Murid": "Student",
"lulus": "passed",
"gagal": "failed"
});
Object.assign(EN, {
  'Empat jalur, satu cara kerja: setiap tujuan pembelajaran ditempuh bertahap dari Pra-KBM sampai Pasca-KBM, dan baru dinyatakan tuntas bila lulus gerbang akhirnya.': 'Four tracks, one way of working: every learning objective is walked through stage by stage, from pre-class to post-class, and counts as mastered only once its final gate is passed.',
  'Urutan tahapan': 'Learning stages', 'Tahapan selesai': 'Stages completed',
  'Tujuan pembelajaran lain': 'Other learning objectives', 'Terkunci': 'Locked',
  'Selesai': 'Completed', 'Sedang dibuka': 'Currently open', 'Tahapan bersyarat': 'Conditional stage',
  'Pra-KBM': 'Before class', 'KBM': 'In class', 'Pasca-KBM': 'After class',
  'Pilih tahapan, lanjutkan perjalananmu.': 'Choose a stage and continue your journey.',
  'Urutan belajar ada di panel kiri. Pada layar kecil, buka Urutan tahapan untuk memilih bagian yang ingin dipelajari.': 'Your learning sequence is in the left panel. On smaller screens, expand Learning stages to choose a stage.',
  'Pilih tahapan yang terbuka pada daftar. Beberapa bagian menunggu kegiatan kelas, penilaian guru, atau jadwal berikutnya.': 'Choose an available stage. Some parts wait for class activities, teacher assessment, or the next scheduled session.'
});
let BHS = 'id';
const tr  = x => (BHS === 'id' || EN[x] === undefined) ? x : EN[x];
const trf = (x, ...v) => { let i = 0; return tr(x).replace(/%s/g, () => v[i++]); };

const TAHAPAN = [
  { id:'S1',  f:0, nama:'Peta & Tujuan Pembelajaran',            lulus:'Dibuka',                         rangka:1 },
  { id:'S2',  f:0, nama:'Gerbang Prasyarat',       lulus:'≥80% lanjut · 60–79% → S2b · <60% → S2c', gate:1, skor:1, rangka:1 },
  { id:'S2b', f:0, nama:'Penguatan Prasyarat',     lulus:'Ulang S2 satu kali', cabang:1 },
  { id:'S2c', f:0, nama:'Remediasi Prasyarat',     lulus:'Ulang S2', cabang:1 },
  { id:'S3',  f:0, nama:'Pemantik & Prakonsepsi',  lulus:'Terkirim (tidak dinilai)', rangka:1 },
  { id:'S4',  f:0, nama:'Penyajian Konsep Awal',   lulus:'Cek sisipan terjawab' },
  { id:'S5',  f:1, nama:'Pembahasan Prakonsepsi',  lulus:'Dipimpin guru', rangka:1 },
  { id:'S6',  f:1, nama:'Inti Terbimbing',         lulus:'Dipimpin guru' },
  { id:'S7',  f:1, nama:'Praktik Terstruktur',     lulus:'Lembar kerja terisi' },
  { id:'S8',  f:1, nama:'Gerbang Formatif Kelas',  lulus:'≥80% benar', gate:1, skor:1, guruIsi:1, rangka:1 },
  { id:'S9',  f:1, nama:'Diferensiasi T1–T4',      lulus:'Sesuai cabang S8' },
  { id:'S10', f:1, nama:'Konsolidasi & Jangkar',   lulus:'Jangkar terkirim', rangka:1 },
  { id:'S11', f:2, nama:'Latihan Bertingkat',      lulus:'Benar 3 dari 4 (≥75%) · H+0–H+2', skor:1 },
  { id:'S12', f:2, nama:'Tugas Kinerja',           lulus:'Minimal T3 (dinilai guru) · H+1–H+5', gate:1, tier:1, rangka:1 },
  { id:'S13', f:2, nama:'Gerbang Ketuntasan TP',   lulus:'Butir baru, sekali jalan · H+2–H+7', gate:1, skor:1, rangka:1 },
  { id:'S14', f:2, nama:'Pengulangan Berjarak',    lulus:'H+14, +30, +60 · gagal → turun', gate:1, rangka:1 }
];
const LAPIS = [
  { id:'L1', nama:'Kuis Blok',              kapan:'Setiap 2–4 TP' },
  { id:'L2', nama:'Muara Topik',            kapan:'Setelah TP terakhir' },
  { id:'L3', nama:'Tes Topik',              kapan:'Akhir topik', gate:1 },
  { id:'L4', nama:'Tantangan Mata Pelajaran', kapan:'Berkala, lintas topik' }
];
const JALUR = [
  { slug:'igcse', kode:'IGCSE', nama:'PHYSICS IGCSE', teks:'Cambridge IGCSE Physics 0625',
    sub:'Kelas 9–10 · jalur internasional', cocok:/^igcse$/i },
  { slug:'as-a',  kode:'AS/A',  nama:'PHYSICS AS/A',  teks:'Cambridge AS &amp; A Level Physics 9702',
    sub:'Kelas 11–12 · jalur internasional', cocok:/^(as\/?-?a([\s-]?level)?|a[\s-]?level|as)$/i },
  { slug:'tka',   kode:'TKA',   nama:'PHYSICS TKA',   teks:'Kurikulum Nasional · persiapan TKA',
    sub:'Fase E–F · jalur nasional', cocok:/^tka$/i },
  { slug:'olimpiade', kode:'OSN', nama:'PHYSICS OLYMPIAD', teks:'OSN &middot; pembinaan olimpiade fisika',
    sub:'Seleksi sekolah hingga nasional', cocok:/^(olimpiade|olympiad|osn|ksn)$/i }
];
const FASE = ['Fase 0 · Pra-KBM', 'Fase 1 · KBM', 'Fase 2 · Pasca-KBM'];
const STATUS = ['Belum Mulai', 'Siap', 'Mencoba', 'Akrab', 'Mahir', 'Tuntas'];
// Fase KBM ditempuh berurutan: tiap tahapan baru terbuka setelah tahapan sebelumnya selesai.
// Gerbang Formatif S8 karena itu tidak dapat dibuka sebelum S7 dikerjakan.
const RANTAI_KBM = { S5:'S3', S6:'S5', S7:'S6', S8:'S7', S9:'S8', S10:'S9' };
const HARI = 864e5;
const T = id => TAHAPAN.find(s => s.id === id);

/* ---------- penyimpanan ---------- */
const KEY = 'va-fims-v1';
let db = {};
try { db = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { db = {}; }
db.tp = db.tp || {}; db.opsi = db.opsi || {};
BHS = db.opsi.bahasa === 'en' ? 'en' : 'id';
const simpan = () => {
  try { localStorage.setItem(KEY, JSON.stringify(db)); } catch (e) {}
  if (window.FIMS && FIMS.aku) FIMS.dorong(db);        // progres mengikuti akun, bukan peramban
};
const prog = slug => (db.tp[slug] = db.tp[slug] || { ev: {}, tier: null, s14: [], riwayat: [] });
const now = () => Date.now() + (db.opsi.geser || 0) * HARI;   // "geser hari" = simulasi waktu untuk uji coba

/* ---------- mesin status ---------- */
function hitungP(p, tp) {                      // murni: tidak menyentuh penyimpanan
  p = p || {}; const e = p.ev || {}, amb = tp.ambang || 75, s14 = p.s14 || [];
  const sk = id => (e[id] && e[id].skor != null) ? e[id].skor : null;
  const ok = id => !!e[id];
  let s = 0;
  if (sk('S2') != null && sk('S2') >= 80) s = 1;
  if (s >= 1 && ok('S4')) s = 2;
  if (s >= 2 && sk('S8') != null && sk('S8') >= 80) s = 3;
  const tier = p.tier || 0;
  if (s >= 3 && sk('S11') != null && sk('S11') >= 75 && tier >= 3) s = 4;
  let stabil = false;
  if (s >= 4 && sk('S13') != null && sk('S13') >= amb) {
    const gagalTerakhir = s14.length && s14[s14.length - 1].hasil === 'gagal';
    s = gagalTerakhir ? 4 : 5;
    stabil = s === 5 && s14.filter(x => x.hasil === 'lulus').length >= 3;
  }
  return { s, stabil, tier: p.tier || null };
}

function hitung(tp) {
  const p = prog(tp.slug), e = p.ev, amb = tp.ambang || 75;
  const sk = id => (e[id] && e[id].skor != null) ? e[id].skor : null;
  const ok = id => !!e[id];
  let s = 0;
  if (sk('S2') != null && sk('S2') >= 80) s = 1;
  if (s >= 1 && ok('S4')) s = 2;
  if (s >= 2 && sk('S8') != null && sk('S8') >= 80) s = 3;
  const tier = p.tier || 0;
  if (s >= 3 && sk('S11') != null && sk('S11') >= 75 && tier >= 3) s = 4;
  let stabil = false;
  if (s >= 4 && sk('S13') != null && sk('S13') >= amb) {
    const gagalTerakhir = p.s14.length && p.s14[p.s14.length - 1].hasil === 'gagal';
    s = gagalTerakhir ? 4 : 5;
    stabil = s === 5 && p.s14.filter(x => x.hasil === 'lulus').length >= 3;
  }
  // catat riwayat bila berubah (status tidak ditimpa, jejak disimpan)
  const last = p.riwayat.length ? p.riwayat[p.riwayat.length - 1].ke : 0;
  if (last !== s) { p.riwayat.push({ dari: last, ke: s, waktu: now() }); simpan(); }
  return { s, stabil, tier: p.tier, e, p, amb };
}

// apakah tahapan terbuka? kembalikan null bila terbuka, atau alasan terkunci
function kunci(tp, id, h) {
  const e = h.e, sk = x => e[x] && e[x].skor;
  if (['S1', 'S2'].includes(id)) return null;
  if (id === 'S2b') return (sk('S2') != null && sk('S2') >= 60 && sk('S2') < 80) ? null : tr('Hanya untuk skor S2 60–79%');
  if (id === 'S2c') return (sk('S2') != null && sk('S2') < 60) ? null : tr('Hanya untuk skor S2 di bawah 60%');
  if (h.s < 1) return tr('Lulus Gerbang Prasyarat (S2 ≥ 80%) dulu');
  if (['S3', 'S4'].includes(id)) return null;
  if (RANTAI_KBM[id]) {
    if (!e.S3) return tr('Kirim prakonsepsi S3 sebelum tatap muka');
    const b = RANTAI_KBM[id];
    if (b !== 'S3' && !e[b]) return trf('Selesaikan dulu %s · %s', b, tr(T(b).nama));
    return null;
  }
  if (id === 'S11') return e.S8 ? null : tr('Kerjakan Gerbang Formatif S8 di kelas');
  if (id === 'S12') return e.S11 ? null : tr('Kerjakan Latihan Bertingkat S11 dulu');
  if (id === 'S13') {
    if (!e.S11) return tr('Kerjakan S11 dulu');
    if ((h.tier || 0) < 3) return tr('Tugas Kinerja S12 harus dinilai minimal T3');
    const buka = e.S11.waktu + 2 * HARI;
    if (now() < buka) return trf('Kuis tertunda dibuka %s (H+2 setelah S11)', tgl(buka));
    if (e.S13 && e.S13.waktu > e.S11.waktu) return tr('Sudah dikerjakan (sekali jalan). Gagal? Ulangi S11 dulu');
    return null;
  }
  if (id === 'S14') {
    if (!(e.S13 && e.S13.skor >= h.amb && h.s >= 4)) return tr('Terbuka setelah status Tuntas');
    const j = jadwalS14(h).find(x => x.berikut);
    if (!j) return tr('Tiga interval lulus: Tuntas Stabil');
    if (now() < j.jatuh) return trf('Interval %s jatuh tempo %s', j.ke, tgl(j.jatuh));
    return null;
  }
  return null;
}

function jadwalS14(h) {
  const awal = (h.p.s14Mulai || (h.e.S13 && h.e.S13.waktu));
  if (!awal) return [];
  const iv = [14, 30, 60];
  const done = h.p.s14.filter(x => x.waktu >= awal).length;
  return iv.map((d, i) => ({ ke: i + 1, hari: d, jatuh: awal + d * HARI, hasil: (h.p.s14.filter(x => x.waktu >= awal)[i] || {}).hasil, berikut: i === done }));
}

function catat(tp, id, data) {
  const p = prog(tp.slug);
  if (id === 'S14') {
    const lulus = data.skor == null ? true : data.skor >= (tp.ambang || 75);
    p.s14.push({ hasil: lulus ? 'lulus' : 'gagal', waktu: now() });
    if (!lulus) p.s14Mulai = now();               // turun ke Mahir & jadwal ulang dari interval pertama
  } else {
    const lama = p.ev[id];
    p.ev[id] = { waktu: now(),
      skor: data.skor == null ? (lama && lama.skor != null ? lama.skor : null) : Math.round(data.skor) };
    // daftar nomor yang masih salah, dikirim halaman lembarnya
    if (Array.isArray(data.salah)) {
      p.ev[id].salah = data.salah.slice(0, 60);
      if (data.benar != null) p.ev[id].benar = data.benar;
      if (data.total != null) p.ev[id].total = data.total;
    } else if (lama && lama.salah && data.skor == null) {
      p.ev[id].salah = lama.salah; p.ev[id].benar = lama.benar; p.ev[id].total = lama.total;
    }
    if (id === 'S2' && p.ev.S2.skor >= 80) { delete p.ev.S2b; delete p.ev.S2c; }
  }
  simpan();
}

// satu langkah berikutnya untuk satu TP
function langkah(tp) {
  const h = hitung(tp), e = h.e, sk = x => e[x] && e[x].skor;
  const ada = id => !!tp.tahapan[id];
  if (!e.S1 && ada('S1')) return 'S1';
  if (h.s < 1) {
    if (sk('S2') != null && sk('S2') < 60 && !e.S2c && ada('S2c')) return 'S2c';
    if (sk('S2') != null && sk('S2') < 80 && sk('S2') >= 60 && !e.S2b && ada('S2b')) return 'S2b';
    return 'S2';
  }
  for (const id of ['S3', 'S4']) if (!e[id] && ada(id)) return id;
  if (!e.S8) return null;                          // menunggu tatap muka
  if (!e.S11) return 'S11';
  if (!e.S12) return 'S12';
  if (!kunci(tp, 'S13', h)) return 'S13';
  if (h.s === 5 || (h.s === 4 && e.S13)) {
    const j = jadwalS14(h).find(x => x.berikut);
    if (j && now() >= j.jatuh) return 'S14';
  }
  return null;
}

/* ---------- utilitas tampilan ---------- */
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tgl = w => new Date(w).toLocaleDateString(BHS === 'en' ? 'en-GB' : 'id-ID', { day: 'numeric', month: 'short' });
const chip = (s, stabil) => `<span class="chip st${s}"><span class="dot"></span>${tr(STATUS[s])}${stabil ? tr(' Stabil') : ''}</span>`;
const tierTag = t => t ? `<span class="tier">T${t}</span>` : '<span class="tier muted">T–</span>';
let K = { topik: [] };
const semuaTP = () => K.topik.flatMap(t => t.tp.map(tp => Object.assign({ _t: t }, tp)));
const cariTP = slug => semuaTP().find(x => x.slug === slug);
const cariTopik = slug => K.topik.find(x => x.slug === slug);
const guru = () => (window.FIMS && FIMS.aku) ? FIMS.modeGuru() : !!db.opsi.guru;
const cariJalur = slug => JALUR.find(j => j.slug === slug);
const topikJalur = j => K.topik.filter(t => j.cocok.test(String(t.jalur || '').trim()));
const jalurTopik = t => JALUR.find(j => j.cocok.test(String(t.jalur || '').trim())) || null;
const topikLepas = () => K.topik.filter(t => !jalurTopik(t));

/* TP ditempuh berurutan: TP ke-n baru terbuka setelah seluruh TP sebelumnya Tuntas.
   Contoh: F.USE.1 hanya terbuka bila F.USE.1-pra sudah Tuntas. */
function kunciTP(tp) {
  if (guru()) return null;
  const t = topikDariTP(tp);
  if (!t || !t.tp) return null;
  const i = t.tp.findIndex(x => x.slug === tp.slug);
  if (i <= 0) return null;
  for (let j = 0; j < i; j++) {
    if (hitung(t.tp[j]).s < 5) return trf('Tuntaskan dulu %s · %s', t.tp[j].kode, t.tp[j].judul);
  }
  return null;
}

/* Lapis topik (L1–L4) baru terbuka setelah seluruh TP topik itu Tuntas. */
function kunciLapis(t) {
  if (guru()) return null;
  const belum = (t.tp || []).filter(tp => hitung(tp).s < 5);
  if (!belum.length) return null;
  return trf('Tuntaskan dulu %s', belum.map(x => x.kode).join(', '));
}
const remah = t => { const j = t && jalurTopik(t);
  return `<a href="#">${tr('Beranda')}</a> / ${j ? `<a href="#jalur-${j.slug}">${esc(j.kode)}</a> / ` : ''}`; };
const kartuTopik = t => { if (t.jenis === 'paket') return kartuPaketTopik(t);
  const n = t.tp.length, tuntas = t.tp.filter(tp => hitung(tp).s === 5).length;
  return `<a class="card" href="#topik-${t.slug}"><div class="eyebrow">${esc(t.mapel)}${t.fase ? ' · ' + tr('Fase ') + esc(t.fase) : ''}</div>
    <h3>${esc(t.nama)}</h3><div class="mono muted">${esc(t.kode)} · ${n === 1 ? tr('1 TP') : trf('%s TP', n)}</div>
    <div class="meter"><i style="width:${n ? Math.round(tuntas / n * 100) : 0}%"></i></div>
    <div class="muted" style="font-size:.85rem">${trf('%s dari %s TP Tuntas', tuntas, n)}</div></a>`; };

const kartuPaketTopik = t => { const n = (t.paket || []).length;
  return `<a class="card" href="#topik-${t.slug}"><div class="eyebrow">${esc(t.mapel)}${t.fase ? ' · ' + tr('Fase ') + esc(t.fase) : ''}</div>
    <h3>${esc(t.nama)}</h3><div class="mono muted">${esc(t.kode)} · ${n === 1 ? tr('1 paket') : trf('%s paket', n)}</div>
    ${t.ringkas ? `<div class="muted" style="font-size:.85rem">${esc(t.ringkas)}</div>` : ''}</a>`; };

/* ---------- tampilan: beranda ---------- */
function physicsIcon(name) {
  const paths = {
    atom: '<ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/><circle cx="12" cy="12" r="1.7" fill="currentColor" stroke="none"/>',
    wave: '<path d="M2 12c3-12 7-12 10 0s7 12 10 0M2 20h20"/>',
    vector: '<path d="M5 19V4m0 15h15M5 19 18 6m-5 0h5v5M2 7l3-3 3 3m9 9 3 3-3 3"/>',
    orbit: '<circle cx="12" cy="12" r="4"/><ellipse cx="12" cy="12" rx="12" ry="5" transform="rotate(-30 12 12)"/><path d="m17 3 2 3m-1-1 3-1"/>',
    book: '<path d="M12 5v15M3 4c3-1 6-1 9 1 3-2 6-2 9-1v15c-3-1-6-1-9 1-3-2-6-2-9-1Z"/>',
    clipboard: '<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4V2h6v2M9 10h6M9 14h6M9 18h4"/>',
    bulb: '<path d="M9 18h6m-5 3h4M8 15a7 7 0 1 1 8 0c-1 1-1 2-1 3H9c0-1 0-2-1-3Z"/>',
    flag: '<path d="M5 22V3m0 0h14l-4 5 4 5H5"/>',
    trophy: '<path d="M7 3h10v7a5 5 0 0 1-10 0Zm5 12v6m-4 0h8M7 5H3v3a4 4 0 0 0 4 4m10-7h4v3a4 4 0 0 1-4 4"/>',
    repeat: '<path d="M20 8a8 8 0 0 0-13-4L3 8m0-5v5h5m-4 8a8 8 0 0 0 13 4l4-4m0 5v-5h-5"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V6a4 4 0 0 1 8 0v4m-4 5v2"/>',
    chevron: '<path d="m6 9 6 6 6-6"/>'
  };
  return `<svg class="physics-icon" viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.atom}</svg>`;
}

function kotakJalur() {
  return JALUR.map(j => {
    const ts = topikJalur(j), n = ts.length;
    const tps = ts.flatMap(t => t.tp);
    const pks = ts.flatMap(t => t.paket || []);
    const tuntas = tps.filter(tp => hitung(tp).s === 5).length;
    const isi = !n
      ? `<span class="jm segera">${tr('Segera hadir')}</span>`
      : tps.length
        ? `<span class="jm">${n === 1 ? trf('1 topik · %s TP', tps.length) : trf('%s topik · %s TP', n, tps.length)}</span>`
        : `<span class="jm">${n === 1 ? trf('1 topik · %s paket', pks.length) : trf('%s topik · %s paket', n, pks.length)}</span>`;
    return `<a class="jalur j-${j.slug}" href="#jalur-${j.slug}">
      <span class="jk"><span class="jalur-ikon">${physicsIcon({igcse:'atom','as-a':'wave',tka:'vector',olimpiade:'orbit'}[j.slug])}</span>${esc(j.kode)}</span>
      <span class="jn">${j.nama}</span>
      <span class="jt">${tr(j.teks)}</span>
      <span class="jb">${isi}${tps.length ? `<span class="jm">${tuntas === 1 ? tr('1 TP Tuntas') : trf('%s TP Tuntas', tuntas)}</span>` : ''}</span>
    </a>`;
  }).join('');
}

function beranda() {
  const tps = semuaTP();
  let next = null;
  for (const tp of tps) { const l = langkah(tp); if (l) { next = { tp, id: l }; break; } }
  const mulai = Object.keys(db.tp || {}).some(k => Object.keys((db.tp[k] || {}).ev || {}).length);
  const lanjut = (mulai && next)
    ? `<a class="next" href="#tp-${next.tp.slug}-${next.id.toLowerCase()}"><span class="what">
         <span class="eyebrow">${tr('Lanjutkan belajar')}</span>
         <b>${esc(tr(T(next.id).nama))}</b>
         <span class="muted"><span class="mono">${esc(next.tp.kode)} · ${next.id}</span> — ${esc(next.tp.judul)}</span></span>
       <span class="btn">${tr('Mulai')}</span></a>`
    : '';
  const lepas = topikLepas();
  const lain = lepas.length
    ? `<section class="stack"><h2>${tr('Topik lain')}</h2><div class="grid-topik">${lepas.map(kartuTopik).join('')}</div></section>`
    : '';
  return `<div class="stack">
    <section class="hero"><p class="eyebrow">Fitrah Islamic World Academy</p>
      <h1>${tr('Belajar Fisika sampai tuntas')}</h1>
      <p class="lede">${tr('Empat jalur, satu cara kerja: setiap tujuan pembelajaran ditempuh bertahap dari Pra-KBM sampai Pasca-KBM, dan baru dinyatakan tuntas bila lulus gerbang akhirnya.')}</p></section>
    <section class="stack"><h2 class="sr-tajuk">${tr('Pilih jalur')}</h2><div class="grid-jalur">${kotakJalur()}</div></section>
    ${lanjut}${lain}</div>`;
}

/* ---------- tampilan: jalur ---------- */
function halJalur(j) {
  const ts = topikJalur(j);
  const kartu = ts.map(kartuTopik).join('');
  return `<div class="stack"><div class="crumbs"><a href="#">${tr('Beranda')}</a> / ${esc(j.kode)}</div>
    <section class="hero mini j-${j.slug}"><p class="eyebrow">${tr(j.sub)}</p><h1>${j.nama}</h1><p class="lede">${tr(j.teks)}</p></section>
    <section class="stack"><h2>${tr('Topik')}</h2>
      ${kartu ? `<div class="grid-topik">${kartu}</div>`
              : `<div class="note">${tr('Materi jalur ini sedang disiapkan. Jalur yang sudah terbuka bisa dilihat di <a href="#">beranda</a>.')}${guru() ? ` <span class="muted">${trf('Guru: tambahkan folder topik di <span class="mono">konten/</span> dengan <span class="mono">"jalur": "%s"</span> pada <span class="mono">topik.json</span>.', esc(j.kode))}</span>` : ''}</div>`}
    </section></div>`;
}

/* ---------- tampilan: topik berjenis paket (tanpa alur pembelajaran) ---------- */
const NAMA_TAHAP = t => (t && t.nama) || 'Lainnya';

function halTopikPaket(t) {
  const daftar = t.paket || [];
  const tahap = (t.tahap || []).slice();
  const sisa = daftar.filter(p => !tahap.some(x => x.kode === p.tahap));
  const kel = tahap.map(th => ({ th, isi: daftar.filter(p => p.tahap === th.kode) }))
    .concat(sisa.length ? [{ th: { kode: '', nama: 'Lainnya' }, isi: sisa }] : [])
    .filter(g => g.isi.length);
  const blok = kel.map(g => `<section class="stack"><h2>${esc(tr(NAMA_TAHAP(g.th)))}</h2><div class="list">${
    g.isi.map(p => `<a class="item" href="#topik-${t.slug}-p-${p.slug}">
      <span class="code">${esc((p.tahap || '·').slice(0, 3).toUpperCase())}</span>
      <span class="t"><b>${esc(p.judul)}</b>${p.ringkas ? `<br><span class="muted">${esc(p.ringkas)}</span>` : ''}</span>
      <span class="row">${p.soal ? `<span class="tier">${trf('%s soal', p.soal)}</span>` : ''}</span></a>`).join('')
  }</div></section>`).join('');
  return `<div class="stack"><div class="crumbs">${remah(t)}${esc(t.kode)}</div>
    <div><div class="eyebrow">${esc(t.mapel)}${t.jalur ? ' · ' + esc(t.jalur) : ''}</div><h1>${esc(t.nama)}</h1>
    ${t.ringkas ? `<p class="muted">${esc(t.ringkas)}</p>` : ''}</div>
    ${blok || `<p class="muted">${tr('Belum ada paket soal pada topik ini.')}</p>`}</div>`;
}

function halPaket(t, slugP) {
  const p = (t.paket || []).find(x => x.slug === slugP);
  const kepala = `<div class="stack"><div class="crumbs">${remah(t)}<a href="#topik-${t.slug}">${esc(t.kode)}</a> / ${tr('Paket')}</div>`;
  if (!p) return `${kepala}<div class="note">${tr('Dokumen tidak ditemukan.')} <a href="#topik-${t.slug}">${tr('Kembali ke daftar paket')}</a></div></div>`;
  return `${kepala}
    <div><h1>${esc(p.judul)}</h1>
      <p class="muted">${[p.bentuk, p.soal ? trf('%s soal', p.soal) : '', p.catatan].filter(Boolean).map(esc).join(' · ')}</p></div>
    <div class="row" style="justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem">
      <span class="muted" style="font-size:.85rem">${tr('Dokumen ini berdiri sendiri: nilai dan pembahasan muncul di dalam lembar itu sendiri, tidak masuk ke progres jalur belajar.')}</span>
      <a class="btn ghost" href="${esc(p.berkas)}" target="_blank" rel="noopener">${tr('Buka penuh di tab baru')} ↗</a></div>
    <iframe class="frame frame-penuh" src="${esc(p.berkas)}" title="${esc(p.judul)}"></iframe>
    <p><a class="btn ghost" href="#topik-${t.slug}">← ${tr('Kembali ke daftar paket')}</a></p></div>`;
}

/* ---------- tampilan: pembuka topik ---------- */
function halPembuka(t) {
  const kepala = `<div class="stack"><div class="crumbs">${remah(t)}<a href="#topik-${t.slug}">${esc(t.kode)}</a> / ${tr('Fenomena Dunia Nyata')}</div>
    <div><div class="eyebrow">${tr('Mulai dari sini')}</div><h1>${tr('Fenomena Dunia Nyata')}</h1>
    <p class="muted">${tr('Lihat dulu untuk apa semua ini dipakai, sebelum masuk ke tujuan pembelajaran pertama.')}</p></div>`;
  if (!t.pembuka) return `${kepala}<div class="note">${tr('Halaman pembuka belum diunggah.')}</div></div>`;
  const tp1 = t.tp[0];
  return `${kepala}
    <div class="row" style="justify-content:flex-end"><a class="btn ghost" href="${esc(t.pembuka.berkas)}" target="_blank" rel="noopener">${tr('Buka penuh di tab baru')} ↗</a></div>
    <iframe class="frame frame-penuh" src="${esc(t.pembuka.berkas)}" title="${tr('Fenomena Dunia Nyata')}"></iframe>
    <div id="bahan" class="bahan" data-topik="${esc(t.slug)}" data-tahapan="PEMBUKA"><p class="muted mkosong">${tr('Memuat bahan pendukung…')}</p></div>
    <p class="row" style="gap:.5rem;flex-wrap:wrap">
      ${tp1 ? `<a class="btn" href="#tp-${tp1.slug}">${tr('Lanjut ke')} ${esc(tp1.kode)} · S1 →</a>` : ''}
      <a class="btn ghost" href="#topik-${t.slug}">${tr('Kembali ke daftar TP')}</a></p></div>`;
}

const kartuPembuka = t => t.pembuka
  ? `<a class="item pembuka-kartu" href="#topik-${t.slug}-pembuka">
       <span class="code">▶</span>
       <span class="t"><b>${tr('Fenomena Dunia Nyata')}</b><br><span class="muted">${tr('Lihat dulu untuk apa semua ini dipakai, sebelum masuk ke tujuan pembelajaran pertama.')}</span></span>
       <span class="row"><span class="tier">${tr('Mulai dari sini')}</span></span></a>`
  : '';

/* ---------- tampilan: topik ---------- */
function halTopik(t) {
  if (t.jenis === 'paket') return halTopikPaket(t);
  const tps = t.tp.map(tp => { const h = hitung(tp), k = kunciTP(tp);
    const isi = `<span class="code">${esc(tp.kode)}</span>
      <span class="t"><b>${esc(tp.judul)}</b>${tp.teks ? `<br><span class="muted">${esc(tp.teks)}</span>` : ''}${k ? `<br><span class="gembok">🔒 ${esc(k)}</span>` : ''}</span>
      <span class="row">${chip(h.s, h.stabil)}${tierTag(h.tier)}</span>`;
    return k ? `<div class="item terkunci" title="${esc(k)}">${isi}</div>`
             : `<a class="item" href="#tp-${tp.slug}">${isi}</a>`; }).join('');
  const kl = kunciLapis(t);
  const lapis = LAPIS.map(l => { const ada = t.tahapan[l.id];
    if (!ada) return `<div class="tile miss"><span class="sid">${l.id}</span><span class="nm">${esc(tr(l.nama))}<small>${tr('Belum diunggah')}</small></span><span></span></div>`;
    if (kl) return `<div class="tile terkunci" title="${esc(kl)}"><span class="sid">${l.id} 🔒</span><span class="nm">${esc(tr(l.nama))}<small>${esc(kl)}</small></span><span></span></div>`;
    return `<a class="tile${l.gate ? ' gate' : ''}" href="#topik-${t.slug}-${l.id.toLowerCase()}"><span class="sid">${l.id}${l.gate ? ' ▲' : ''}</span><span class="nm">${esc(tr(l.nama))}<small>${esc(tr(l.kapan))}</small></span><span></span></a>`; }).join('');
  return `<div class="stack"><div class="crumbs">${remah(t)}${esc(t.kode)}</div>
    <div><div class="eyebrow">${esc(t.mapel)}${t.jalur ? ' · ' + esc(t.jalur) : ''}</div><h1>${esc(t.nama)}</h1></div>
    ${t.pembuka ? `<section class="stack"><h2>${tr('Fenomena Dunia Nyata')}</h2><div class="list">${kartuPembuka(t)}</div></section>` : ''}
    <section class="stack"><h2>${tr('Tujuan Pembelajaran')}</h2><div class="list">${tps || `<p class="muted">${tr('Belum ada TP.')}</p>`}</div></section>
    <section class="stack"><h2>${tr('Lapis topik')}</h2><div class="layer">${lapis}</div></section></div>`;
}

/* ---------- tampilan: TP ---------- */
// Penanda visual memakai bukti dan ambang yang sama; tidak menulis progres.
function tahapSelesai(tp, s, h) {
  if (s.id === 'S12') return h.tier >= 3;
  if (s.id === 'S14') return !!h.stabil;
  const ev = h.e[s.id];
  if (!ev) return false;
  const amb = ambangTahapan(tp, s.id);
  return amb == null || (ev.skor != null && ev.skor >= amb);
}

function navigasiTahapan(tp, aktif, h) {
  const t = topikDariTP(tp);
  const tahap = TAHAPAN.filter(s => !s.cabang || tp.tahapan[s.id]);
  const selesai = tahap.filter(s => tahapSelesai(tp, s, h)).length;
  const icons = { S1:'book', S2:'clipboard', S2b:'book', S2c:'book', S3:'bulb', S4:'bulb',
    S5:'wave', S6:'vector', S7:'clipboard', S8:'trophy', S9:'vector', S10:'book',
    S11:'clipboard', S12:'flag', S13:'trophy', S14:'repeat' };
  const phases = ['Pra-KBM', 'KBM', 'Pasca-KBM'];
  const items = tahap.map((s, i) => {
    const ada = tp.tahapan[s.id], k = kunci(tp, s.id, h), done = tahapSelesai(tp, s, h);
    const active = aktif === s.id, canOpen = ada && (!k || guru());
    const status = !ada ? tr('Belum diunggah') : active ? tr('Sedang dibuka') : done ? tr('Selesai') : k ? tr('Terkunci') : s.cabang ? tr('Tahapan bersyarat') : tr(phases[s.f]);
    const title = !ada ? tr('Belum diunggah') : k || tr(s.lulus);
    const state = k && !guru() ? physicsIcon('lock') : done ? physicsIcon('check') : '';
    const ev = h.e[s.id];
    const result = s.id === 'S12' && h.tier ? 'T' + h.tier : s.id === 'S14' && h.p.s14.length ? h.p.s14.length + '×' : ev && ev.skor != null ? ev.skor + '%' : '';
    const inner = `${physicsIcon(icons[s.id])}<span class="step-label">${esc(tr(s.nama))}<small>${s.id}${result ? ' · '+esc(result) : ''} · ${esc(status)}</small></span><span class="step-state">${state}</span>`;
    const item = canOpen
      ? `<a class="step-link" href="#tp-${tp.slug}-${s.id.toLowerCase()}"${active ? ' aria-current="step"' : ''} title="${esc(title)}">${inner}</a>`
      : `<div class="step-link" role="link" aria-disabled="true" title="${esc(title)}">${inner}</div>`;
    const cls = ['study-step', active ? 'active' : '', done ? 'done' : '', k ? 'locked' : '', !ada ? 'missing' : '', s.gate ? 'gate' : '',
      ['S3','S4','S5','S6'].includes(s.id) ? 'concept' : '', i && tahap[i-1].f !== s.f ? 'phase-start' : ''].filter(Boolean).join(' ');
    return `<li class="${cls}"><span class="step-number" aria-hidden="true">${i+1}</span>${item}</li>`;
  }).join('');
  const others = t.tp.length > 1 ? `<nav class="study-other" aria-label="${tr('Tujuan pembelajaran lain')}">${t.tp.map(p => {
    const k = kunciTP(p), current = p.slug === tp.slug;
    const content = `<small>${esc(p.kode)}${current ? ' · '+tr('Sedang dibuka') : k ? ' · '+tr('Terkunci') : ''}</small><strong>${esc(p.judul)}</strong>`;
    return k ? `<div title="${esc(k)}">${content}</div>` : `<a${current ? ' class="current"' : ''} href="#tp-${p.slug}">${content}</a>`;
  }).join('')}</nav>` : '';
  return `<aside class="study-rail" data-study-tp="${esc(tp.slug)}" aria-label="${esc(tr('Urutan tahapan'))}">
    <a class="study-course" href="#topik-${t.slug}">${physicsIcon('atom')}<span><strong>${esc(t.nama)}</strong><small>${esc(tp.kode)} · ${trf('%s TP', t.tp.length)}</small></span></a>
    <div class="study-progress"><div class="row"><span id="stage-progress-label">${tr('Tahapan selesai')}</span><b>${selesai} / ${tahap.length}</b></div><progress max="${tahap.length}" value="${selesai}" aria-labelledby="stage-progress-label"></progress></div>
    <button class="study-rail-toggle" type="button" data-study-toggle aria-expanded="${window.matchMedia('(min-width: 900px)').matches}" aria-controls="study-rail-list">${tr('Urutan tahapan')}${physicsIcon('chevron')}</button>
    <div class="study-rail-scroll" id="study-rail-list"${window.matchMedia('(min-width: 900px)').matches ? '' : ' hidden'}><nav aria-label="${esc(tr('Urutan tahapan'))}"><ol class="study-steps">${items}</ol></nav>${others}</div>
    <div class="study-rail-footer" aria-hidden="true">${physicsIcon('wave')}</div></aside>`;
}

function bukaDaftarTahapan(rail, open) {
  rail.querySelector('.study-rail-scroll').hidden = !open;
  rail.querySelector('[data-study-toggle]').setAttribute('aria-expanded', String(open));
}

function posisikanTahapan(rail, scrollTop) {
  if (!rail) return;
  const scroll = rail.querySelector('.study-rail-scroll');
  if (scrollTop != null) scroll.scrollTop = scrollTop;
  const active = rail.querySelector('[aria-current="step"]');
  if (!active || scroll.hidden) return;
  const bounds = scroll.getBoundingClientRect(), box = active.getBoundingClientRect();
  if (box.top < bounds.top) scroll.scrollTop -= bounds.top - box.top + 8;
  else if (box.bottom > bounds.bottom) scroll.scrollTop += box.bottom - bounds.bottom + 8;
}

function segarkanNavigasiTahapan(tp, id, h) {
  const rail = document.querySelector('.study-rail');
  if (!rail) return;
  const top = rail.querySelector('.study-rail-scroll').scrollTop, open = !rail.querySelector('.study-rail-scroll').hidden;
  rail.outerHTML = navigasiTahapan(tp, id, h);
  const baru = document.querySelector('.study-rail'); bukaDaftarTahapan(baru, open);
  posisikanTahapan(baru, top);
}

function pengantarTP(tp) {
  const next = langkah(tp);
  return `<section class="study-intro">${physicsIcon('atom')}<h2>${tr('Pilih tahapan, lanjutkan perjalananmu.')}</h2>
    <p>${tr('Urutan belajar ada di panel kiri. Pada layar kecil, buka Urutan tahapan untuk memilih bagian yang ingin dipelajari.')}</p>
    <div class="study-phase-key">${FASE.map(f => `<span>${esc(tr(f))}</span>`).join('')}</div>
    ${next && tp.tahapan[next] ? `<a class="next" href="#tp-${tp.slug}-${next.toLowerCase()}"><span class="what"><span class="eyebrow">${tr('Langkah berikutnya')}</span><b>${esc(tr(T(next).nama))}</b><span class="muted">${next}</span></span><span class="btn">${tr('Mulai')}</span></a>` : `<p>${tr('Pilih tahapan yang terbuka pada daftar. Beberapa bagian menunggu kegiatan kelas, penilaian guru, atau jadwal berikutnya.')}</p>`}</section>`;
}

function halTP(tp, aktif) {
  const kTP = kunciTP(tp);
  if (kTP) {
    const tt = topikDariTP(tp);
    return `<div class="stack"><div class="crumbs">${remah(tt)}<a href="#topik-${tt.slug}">${esc(tt.kode)}</a> / ${esc(tp.kode)}</div>
      <h1>${esc(tp.kode)} · ${esc(tp.judul)}</h1>
      <div class="panel terkunci-panel"><p class="gembok-besar">🔒</p>
        <p><b>${tr('TP ini belum terbuka.')}</b></p><p class="muted">${esc(kTP)}</p>
        <p class="muted">${tr('Tujuan Pembelajaran ditempuh berurutan. TP berikutnya terbuka sendiri begitu TP sebelumnya berstatus Tuntas.')}</p>
        <p><a class="btn" href="#topik-${tt.slug}">${tr('Kembali ke daftar TP')}</a></p></div></div>`;
  }
  const h = hitung(tp), t = tp._t;
  const ladder = STATUS.map((n, i) => `<div class="${i <= h.s && i > 0 ? 'on st' + i : ''}${i === 0 && h.s === 0 ? ' on' : ''}">${tr(n)}</div>`).join('');
  const lengkap = TAHAPAN.filter(s => s.rangka && !tp.tahapan[s.id]).map(s => s.id);
  return `<div class="stack"><div class="crumbs">${remah(t)}<a href="#topik-${t.slug}">${esc(t.kode)}</a> / ${esc(tp.kode)}</div>
    <div class="study-layout">${navigasiTahapan(tp, aktif, h)}<div class="study-main">
    <header class="study-heading"><div class="row"><span class="tp-label">${esc(tp.kode)}${tp.bloom ? ' · Bloom ' + esc(tp.bloom) : ''}</span><span class="row">${chip(h.s, h.stabil)}${tierTag(h.tier)}</span></div>
      <h1>${esc(tp.judul)}</h1>${tp.teks ? `<p class="muted">${esc(tp.teks)}</p>` : ''}
      <div class="ladder">${ladder}</div></header>
    ${h.s === 4 && h.p.s14.length && h.p.s14[h.p.s14.length - 1].hasil === 'gagal' ? `<div class="note">${tr('Status turun ke Mahir: pengulangan berjarak gagal. Jadwal diulang dari H+14.')}</div>` : ''}
    ${(h.tier && h.tier < 3) ? `<div class="note">${trf('Tier T%s: perlu pendampingan pada konteks baru, bukan tambahan latihan soal.', h.tier)}</div>` : ''}
    ${guru() && lengkap.length ? `<div class="note">${trf('Kelengkapan: tahapan rangka belum diunggah — %s.', lengkap.join(', '))}</div>` : ''}
    ${aktif ? viewer(tp, aktif, h) : pengantarTP(tp)}
    ${h.e.S13 && h.e.S13.skor >= h.amb && h.s >= 4 ? s14Panel(h) : ''}
    ${guru() ? panelGuruTP(tp, h) : ''}</div></div></div>`;
}

function s14Panel(h) {
  const rows = jadwalS14(h).map(j => `<tr><td>${trf('Interval %s', j.ke)}</td><td>${BHS === 'en' ? 'D' : 'H'}+${j.hari}</td><td>${tgl(j.jatuh)}</td><td class="${j.hasil === 'lulus' ? 'y' : j.hasil === 'gagal' ? 'n' : 'o'}">${j.hasil ? tr(j.hasil) : (j.berikut ? tr('berikutnya') : '—')}</td></tr>`).join('');
  return `<section class="panel stack"><h3>${tr('Jadwal pengulangan berjarak (S14)')}</h3><div class="scroll"><table><tr><th>${tr('Interval')}</th><th>${tr('Hari')}</th><th>${tr('Jatuh tempo')}</th><th>${tr('Hasil')}</th></tr>${rows}</table></div></section>`;
}

// Ambang kelulusan tiap tahapan berskor; null berarti tidak ada ambang.
function ambangTahapan(tp, id) {
  if (id === 'S2' || id === 'S8') return 80;
  if (id === 'S11') return 75;
  if (id === 'S13' || id === 'S14') return tp.ambang || 75;
  return null;
}

// Keterangan nomor-nomor yang masih salah sesudah lembar diperiksa.
function petunjukSalah(tp, id, h) {
  const e = h.e[id];
  if (!e || !Array.isArray(e.salah)) return '';
  const amb = ambangTahapan(tp, id);
  const skor = e.skor;
  const cukup = amb == null || (skor != null && skor >= amb);
  if (!e.salah.length) {
    return `<div class="periksa lulus"><b>${tr('Semua butir sudah benar.')}</b>
      <p>${e.total != null ? trf('Benar %s dari %s butir.', e.benar, e.total) : ''}</p></div>`;
  }
  const keping = e.salah.map(t => `<span class="nomor">${esc(t)}</span>`).join('');
  const jarak = (amb != null && skor != null && skor < amb)
    ? `<p class="jarak">${trf('Skormu %s, ambangnya %s. Kurang %s poin lagi.', skor, amb, amb - skor)}</p>` : '';
  return `<div class="periksa ${cukup ? 'cukup' : 'kurang'}">
    <b>${trf('%s nomor masih salah', e.salah.length)}</b>
    ${e.total != null ? `<p>${trf('Benar %s dari %s butir.', e.benar, e.total)}</p>` : ''}
    <div class="nomor-daftar">${keping}</div>
    ${jarak}
    <p class="saran">${tr('Buka kembali nomor-nomor itu pada lembar di atas, kerjakan ulang langkahnya, lalu periksa lagi. Kunci jawaban sengaja tidak ditampilkan.')}</p>
  </div>`;
}

// Tahapan mana yang mesti dikerjakan sesudah tahapan ini.
function berikutnya(tp, id) {
  if (id === 'S2b' || id === 'S2c') return 'S2';     // penguatan dan remediasi selalu bermuara ke gerbangnya
  const l = langkah(tp);
  return (l && l !== id) ? l : null;
}

function petunjukLanjut(tp, id) {
  const b = berikutnya(tp, id);
  if (!b || !tp.tahapan[b]) return '';
  const nm = esc(tr(T(b).nama));
  const tautan = `<a class="btn" href="#tp-${tp.slug}-${b.toLowerCase()}">${trf('Ke %s · %s', b, nm)}</a>`;
  if (id === 'S2b' || id === 'S2c') {
    return `<div class="lanjut kuat"><div><b>${tr('Sesudah ini: kerjakan ulang Gerbang Prasyarat')}</b>
      <p>${tr('Penguatan dan remediasi tidak mengubah statusmu dengan sendirinya. Status baru naik setelah kamu lulus Gerbang Prasyarat, yaitu skor minimal 80%. Kerjakan ulang gerbangnya sekarang.')}</p></div>${tautan}</div>`;
  }
  return `<div class="lanjut"><div><b>${tr('Langkah berikutnya')}</b>
    <p>${trf('%s · %s', b, nm)}</p></div>${tautan}</div>`;
}

function bagianBawah(tp, id, h, aksi) {
  return `${aksi}
    ${petunjukSalah(tp, id, h)}
    ${petunjukLanjut(tp, id)}`;
}

// Menyegarkan tampilan sesudah skor masuk TANPA memuat ulang lembarnya,
// supaya jawaban yang sudah diketik siswa tidak hilang saat ia diminta memperbaiki nomor tertentu.
function segarkanSetelahSkor() {
  const bawah = document.getElementById('viewer-bawah');
  if (!cur || !bawah) return render();
  const h = hitung(cur.tp);
  segarkanNavigasiTahapan(cur.tp, cur.id, h);
  const s = T(cur.id);
  bawah.innerHTML = bagianBawah(cur.tp, cur.id, h, barisAksi(cur.tp, cur.id, h, s));
  const kep = document.querySelector('.row .chip');
  if (kep) kep.outerHTML = chip(h.s, h.stabil);
  const tangga = document.querySelector('.ladder');
  if (tangga) tangga.innerHTML = STATUS.map((n, i) =>
    `<div class="${i <= h.s && i > 0 ? 'on st' + i : ''}${i === 0 && h.s === 0 ? ' on' : ''}">${tr(n)}</div>`).join('');
}

function barisAksi(tp, id, h, s) {
  const tercatat = h.e[id] && h.e[id].skor != null ? h.e[id].skor : null;
  const nilaiTercatat = tercatat != null
    ? `<span class="skor-tercatat">${trf('Skor tercatat: %s', tercatat)}</span>` : '';
  if (s.tier)
    return `<div class="row"><button class="btn" data-aksi="selesai">${tr('Tandai bukti terkirim')}</button><span class="muted">${tr('Tier diisi guru (rubrik T1–T4).')}</span></div>`;
  if (s.skor || id === 'S14') {
    if (guru())
      return `<div class="row"><label for="skorIn">${tr('Skor (%)')}</label><input type="number" id="skorIn" min="0" max="100" style="width:90px"><button class="btn" data-aksi="skor">${tr('Simpan skor')}</button><span class="muted">${tr('Mode guru. Siswa tidak dapat mengetik skornya sendiri.')}</span>${nilaiTercatat}</div>`;
    if (s.guruIsi)
      return `<div class="row"><button class="btn" data-aksi="selesai">${tr('Tandai sudah mengikuti')}</button><span class="muted">${tr('Skor tahapan ini dinilai dan diisi gurumu di kelas.')}</span>${nilaiTercatat}</div>`;
    return `<div class="row kunci-skor"><span class="muted">${tr('Skormu terisi sendiri begitu kamu menekan tombol periksa pada lembar di atas. Tidak ada angka yang bisa diketik sendiri di sini.')}</span>${nilaiTercatat}</div>`;
  }
  return `<div class="row"><button class="btn" data-aksi="selesai">${tr('Tandai selesai')}</button></div>`;
}

function viewer(tp, id, h) {
  const s = T(id), f = tp.tahapan[id];
  if (!f) return `<div class="panel">${trf('Tahapan %s belum diunggah.', id)}</div>`;
  const k = kunci(tp, id, h);
  if (k && !guru()) return `<div class="note">🔒 ${esc(k)}</div>`;
  const aksi = barisAksi(tp, id, h, s);
  // S1 pada TP pertama: ingatkan halaman pembuka topik dibuka lebih dulu.
  const tt = topikDariTP(tp);
  const awal = id === 'S1' && tt.pembuka && tt.tp && tt.tp[0] && tt.tp[0].slug === tp.slug
    ? `<a class="note pembuka-ingat" href="#topik-${tt.slug}-pembuka">▶ ${tr('Belum membaca pembukanya? Lihat fenomena dunia nyata topik ini lebih dulu.')}</a>` : '';
  // Guru membuka ulang tahapan ini dan murid belum mengerjakannya lagi: jelaskan, jangan biarkan bingung.
  const rs = (h.p.reset || []).filter(x => x.t === id).pop();
  const bukaUlang = (rs && id !== 'S14' && !h.e[id])
    ? `<div class="note reset-info">↺ ${trf('%s membuka ulang tahapan ini pada %s%s. Kerjakan lagi dari awal.',
        esc(rs.nama || tr('Gurumu')), tgl(rs.pada), rs.alasan ? ' — ' + esc(rs.alasan) : '')}</div>` : '';
  return `<section class="viewer" id="viewer">${awal}${bukaUlang}<div class="row" style="justify-content:space-between"><h2>${id} · ${esc(tr(s.nama))}</h2><span class="muted">${trf('Lulus apabila: %s', esc(tr(s.lulus)))}</span></div>
    ${k ? `<div class="note">${trf('Mode guru: tahapan ini masih terkunci untuk siswa (%s).', esc(k))}</div>` : ''}
    <iframe class="frame" src="${esc(f.berkas)}" title="${esc(tr(s.nama))}"></iframe>
    <div id="viewer-bawah">${bagianBawah(tp, id, h, aksi)}</div>
    <div id="bahan" class="bahan" data-topik="${esc(topikDariTP(tp).slug)}" data-tp="${esc(tp.kode)}" data-tahapan="${id}"><p class="muted mkosong">${tr('Memuat bahan pendukung…')}</p></div></section>`;
}

function panelGuruTP(tp, h) {
  const opsi = [0, 1, 2, 3, 4].map(n => `<option value="${n}"${(h.tier || 0) === n ? ' selected' : ''}>${n ? 'T' + n : '—'}</option>`).join('');
  const selisih = h.e.S11 && h.e.S13 && h.e.S11.skor != null && h.e.S13.skor != null
    ? trf('%s poin', h.e.S11.skor - h.e.S13.skor) : tr('belum ada data');
  return `<section class="panel stack"><h3>${trf('Panel guru · %s', esc(tp.kode))}</h3>
    <div class="row"><label for="tierIn">${tr('Tier dari rubrik S9/S12')}</label><select id="tierIn">${opsi}</select>
    <button class="btn ghost" data-aksi="reset">${tr('Hapus progres TP ini (hanya milikmu)')}</button></div>
    <div class="muted" style="font-size:.85rem">${trf('Selisih S11 − S13: %s · Riwayat status: %s', selisih, h.p.riwayat.map(r => tr(STATUS[r.ke])).join(' → ') || '—')}</div></section>`;
}

/* ---------- tampilan: lapis topik ---------- */
function halLapis(t, id, sub) {
  const l = LAPIS.find(x => x.id === id), f = t.tahapan[id];
  const kepala = `<div class="stack"><div class="crumbs">${remah(t)}<a href="#topik-${t.slug}">${esc(t.kode)}</a> / ${id}</div>
    <h1>${id} · ${esc(tr(l.nama))}</h1><p class="muted">${esc(tr(l.kapan))}</p>`;

  const k = kunciLapis(t);
  if (k) return `${kepala}<div class="panel terkunci-panel"><p class="gembok-besar">🔒</p>
    <p><b>${tr('Lapis ini belum terbuka.')}</b></p><p class="muted">${esc(k)}</p>
    <p><a class="btn" href="#topik-${t.slug}">${tr('Kembali ke daftar TP')}</a></p></div></div>`;

  if (!f) return `${kepala}<p>${tr('Belum diunggah.')}</p></div>`;

  // Sebagian lapis punya dua konten: latihan dulu, baru soal yang dinilai.
  const punyaLatihan = !!f.latihan;
  const pilih = (sub === 'latihan' && punyaLatihan) ? 'latihan' : 'utama';
  const berkas = pilih === 'latihan' ? f.latihan.berkas : f.berkas;
  const tab = punyaLatihan ? `<div class="tab-konten">
      <a class="tabk${pilih === 'latihan' ? ' on' : ''}" href="#topik-${t.slug}-${id.toLowerCase()}-latihan">${tr('Latihan Unit Test')}<small>${tr('berlatih dulu · tidak dinilai')}</small></a>
      <a class="tabk${pilih === 'utama' ? ' on' : ''}" href="#topik-${t.slug}-${id.toLowerCase()}">${tr('Soal Unit Test')}<small>${tr('sekali jalan · dinilai')}</small></a>
    </div>
    <p class="note kecilan">${tr('Redaksi soal pada keduanya berbeda, tetapi langkah penyelesaiannya sama. Kerjakan latihannya sampai lancar, baru buka soal yang dinilai. Keduanya tidak memerlukan kalkulator.')}</p>` : '';

  return `${kepala}${tab}
    <iframe class="frame" src="${esc(berkas)}" title="${esc(tr(l.nama))}"></iframe>
    <div id="bahan" class="bahan" data-topik="${esc(t.slug)}" data-tahapan="${id}"><p class="muted mkosong">${tr('Memuat bahan pendukung…')}</p></div></div>`;
}

/* ---------- tampilan: papan guru ---------- */
function halGuru() {
  const ids = TAHAPAN.map(s => s.id);
  const kel = K.topik.map(t => {
    const rows = t.tp.map(tp => `<tr><td class="l mono">${esc(tp.kode)}</td>${ids.map(id => {
      const s = T(id), ada = !!tp.tahapan[id];
      return `<td class="${ada ? 'y' : s.rangka ? 'n' : 'o'}">${ada ? '✓' : s.rangka ? '✕' : '·'}</td>`; }).join('')}
      <td class="${TAHAPAN.some(s => s.rangka && !tp.tahapan[s.id]) ? 'n' : 'y'}">${TAHAPAN.some(s => s.rangka && !tp.tahapan[s.id]) ? tr('Belum') : tr('Siap')}</td></tr>`).join('');
    return `<h3>${esc(t.kode)} · ${esc(t.nama)}</h3><div class="scroll"><table><tr><th class="l">${tr('TP')}</th>${ids.map(i => `<th>${i}</th>`).join('')}<th>${tr('Terbit')}</th></tr>${rows}</table></div>`;
  }).join('');
  const tps = semuaTP();
  const papan = `<div class="scroll"><table><tr><th class="l">${tr('Siswa')}</th>${tps.map(tp => `<th class="mono">${esc(tp.kode)}</th>`).join('')}</tr>
    <tr><td class="l">${tr('Perangkat ini')}</td>${tps.map(tp => { const h = hitung(tp); return `<td class="cell st${h.s}" title="${tr(STATUS[h.s])}">${h.tier ? 'T' + h.tier : ''}</td>`; }).join('')}</tr></table></div>
    <div class="row" style="font-size:.8rem">${STATUS.map((n, i) => chip(i)).join('')}</div>`;
  const geser = db.opsi.geser || 0;
  /* Panel yang bisa dilipat. <details> dipakai supaya bekerja tanpa JavaScript
     dan tetap dapat dijangkau papan tik. Keadaan buka/tutup hanya kenyamanan
     per peramban, jadi aman bila penyimpanannya kosong atau menolak. */
  const terbuka = (kunci, baku) => {
    let v = null;
    try { v = localStorage.getItem('fims.lipat.' + kunci); } catch {}
    return v === null ? baku : v === 'buka';
  };
  const lipat = (kunci, judul, isi, bakuTutup) => `<details class="panel stack lipat" data-lipat="${kunci}"${
      terbuka(kunci, !bakuTutup) ? ' open' : ''}>
      <summary><h2>${judul}</h2><span class="lipat-tanda" aria-hidden="true"></span></summary>
      <div class="lipat-isi stack">${isi}</div></details>`;
  return `<div class="stack"><div><div class="eyebrow">${tr('Papan guru')}</div><h1>${tr('Kelengkapan & posisi')}</h1></div>
    ${lipat('kelengkapan', tr('Kelengkapan tahapan'),
      `<p class="muted" style="margin:0">${tr('✕ = tahapan rangka (S1, S2, S3, S5, S8, S10, S12, S13, S14) belum diunggah. TP dengan ✕ belum boleh terbit.')}</p>${kel}`, true)}
    <section class="panel stack"><h2>${tr('Butuh penilaian')}</h2>
      <p class="muted" style="margin:0">${tr('Murid di bawah ini sudah sampai pada tahapan yang nilainya diisi guru. Yang paling lama menunggu berada di atas.')} ${tr('Hanya murid bimbinganmu yang tampil di sini. Pemilik situs melihat seluruh murid.')}</p>
      <div id="antrean-nilai"><p class="muted" style="margin:0">${tr('Memuat antrean penilaian…')}</p></div></section>
    <section class="panel stack" id="reset-guru"><h2>${tr('Atur ulang dokumen murid')}</h2>
      <p class="muted" style="margin:0">${tr('Murid terlanjur menekan Selesai, atau dokumennya sudah diskor? Pilih muridnya, lalu topiknya, lalu klik dokumen yang mau dibuka ulang: tahapan S1–S14, lapis L1–L4, paket (termasuk PRI UIN), atau dokumen isian lain. Hanya hasil dan isian dokumen itu yang dihapus; dokumen lain dan progres TP tetap utuh. Murid bisa langsung mengerjakan ulang.')}</p>
      <div class="row"><label for="reset-murid">${tr('Murid')}</label><select id="reset-murid"><option value="">${tr('Memuat papan kelas…')}</option></select></div>
      <div class="row" id="reset-topik-baris" hidden><label for="reset-topik">${tr('Topik yang dikerjakan')}</label><select id="reset-topik"></select></div>
      <div id="reset-isi"></div><div id="reset-konfirmasi" hidden></div><div id="reset-pesan" role="status"></div></section>
    <section class="panel stack"><h2>${tr('Papan posisi')}</h2><p class="muted" style="margin:0">${tr('Warna = status, angka = tier. Baris paling atas adalah progres pada perangkat ini; baris berikutnya diambil dari akun tiap murid.')}</p>${papan}
      <div id="papan-kelas"><p class="muted" style="margin:0">${tr('Memuat papan kelas…')}</p></div></section>
    <section class="panel stack"><h2>${tr('Simulasi waktu')}</h2><p class="muted" style="margin:0">${trf('Untuk uji alur kuis tertunda (H+2) dan pengulangan (H+14). Sekarang digeser %s hari.', geser)}</p>
      <div class="row"><button class="btn ghost" data-geser="2">${tr('+2 hari')}</button><button class="btn ghost" data-geser="14">${tr('+14 hari')}</button><button class="btn ghost" data-geser="0">${tr('Kembali ke hari ini')}</button></div></section></div>`;
}

/* ---------- router ---------- */
let cur = null;
function rangka() {
  document.documentElement.lang = BHS;
  const pasang = (sel, teks) => { const el = document.querySelector(sel); if (el) el.textContent = teks; };
  pasang('#nav-belajar', tr('Belajar'));
  pasang('#nav-guru', tr('Papan Guru'));
  pasang('#lbl-guru', tr('Mode guru'));
  pasang('#kaki', tr('Alur Konten Pembelajaran Tuntas · CMS FIMS · Fitrah Islamic World Academy. Progres belajar tersimpan pada akunmu.'));
  const merek = document.querySelector('.brand'); if (merek) merek.setAttribute('aria-label', tr('Fisika FIWA — beranda'));
  document.querySelectorAll('[data-bhs]').forEach(b => {
    const on = b.dataset.bhs === BHS;
    b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
}

/* ---------- bahan pendukung: video, audio, simulasi, bacaan ---------- */
const MEDIA = {};                                   // tembolok per topik
const topikDariTP = tp => tp._t || K.topik.find(t => t.tp.some(x => x.slug === tp.slug)) || { slug: '' };

function muatMedia(slugTopik) {
  if (MEDIA[slugTopik]) return MEDIA[slugTopik];
  MEDIA[slugTopik] = fetch('media-' + slugTopik + '/media.json')
    .then(r => r.ok ? r.json() : null).catch(() => null);
  return MEDIA[slugTopik];
}

const JENIS = { video:'Video', audio:'Audio', simulasi:'Simulasi', bacaan:'Bacaan', tautan:'Tautan' };
const IKON  = { video:'▶', audio:'♪', simulasi:'⚙', bacaan:'▤', tautan:'↗' };

function kartuBahan(it, i) {
  const jenis = JENIS[it.tipe] ? it.tipe : 'tautan';
  return `<article class="mkartu m-${jenis}" data-i="${i}">
    <button class="mkepala" type="button" data-media="${i}" aria-expanded="false">
      <span class="mikon" aria-hidden="true">${IKON[jenis]}</span>
      <span class="mjudul">${esc(it.judul || tr(JENIS[jenis]))}${it.catatan ? `<small>${esc(it.catatan)}</small>` : ''}</span>
      <span class="mjenis">${tr(JENIS[jenis])}${it.luar ? ' · ' + tr('Sumber luar') : ''}</span>
      <span class="mtanda" aria-hidden="true">+</span>
    </button>
    <div class="misi" hidden></div>
  </article>`;
}

function isiPemutar(el, it) {
  if (el.dataset.siap) return;
  el.dataset.siap = '1';
  if (it.tipe === 'video' && it.yt) {
    const mulai = it.mulai ? '&start=' + (+it.mulai | 0) : '';
    el.innerHTML = `<div class="m16by9"><iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(it.yt)}?rel=0&modestbranding=1&playsinline=1${mulai}"
        title="${esc(it.judul || '')}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen></iframe></div>
      <p class="mkaki"><a href="https://www.youtube.com/watch?v=${encodeURIComponent(it.yt)}" target="_blank" rel="noopener">${tr('Buka di YouTube')} ↗</a></p>`;
    return;
  }
  if (it.tipe === 'audio') {
    if (it.berkas) {
      el.innerHTML = `<audio class="maudio" controls preload="none" src="${esc(it.berkas)}"></audio>`;
    } else {
      el.innerHTML = `<div class="mnarasi">
          <div class="mtombol"><button class="btn" type="button" data-narasi="putar">${tr('Putar')}</button>
          <button class="btn ghost" type="button" data-narasi="jeda">${tr('Jeda')}</button>
          <button class="btn ghost" type="button" data-narasi="henti">${tr('Hentikan')}</button></div>
          <p class="mnaskah">${esc(it.naskah || '')}</p>
          <p class="mkaki">${tr('Naskah dibacakan oleh peramban. Guru dapat menggantinya dengan rekaman suara sendiri.')}</p>
        </div>`;
    }
    return;
  }
  const alamat = it.berkas || it.url;
  if (!alamat) { el.innerHTML = ''; return; }
  if (it.tipe === 'tautan') {
    el.innerHTML = `<p class="mkaki"><a class="btn" href="${esc(alamat)}" target="_blank" rel="noopener">${tr('Buka penuh di tab baru')} ↗</a></p>`;
    return;
  }
  const luar = /^https?:/i.test(alamat);
  el.innerHTML = `<iframe class="mbingkai ${it.tipe === 'bacaan' ? 'mbaca' : ''}" src="${esc(alamat)}"
      title="${esc(it.judul || '')}" loading="lazy" allowfullscreen></iframe>
    <p class="mkaki"><a href="${esc(alamat)}" target="_blank" rel="noopener">${tr('Buka penuh di tab baru')} ↗</a>${
      luar ? `<br><span class="mluar">${tr('Bahan ini dari situs luar. Bila kotaknya tetap kosong, situs itu menolak ditampilkan di dalam halaman — pakai tautan di atas.')}</span>` : ''}</p>`;
}

/* narasi dibacakan peramban */
let ucap = null;
function narasi(aksi, teks) {
  const S = window.speechSynthesis;
  if (!S) return alert(tr('Peramban ini belum dapat membacakan naskah. Silakan baca teksnya langsung.'));
  if (aksi === 'henti') { S.cancel(); ucap = null; return; }
  if (aksi === 'jeda') { S.speaking && !S.paused ? S.pause() : S.resume(); return; }
  S.cancel();
  ucap = new SpeechSynthesisUtterance(teks);
  ucap.lang = 'id-ID'; ucap.rate = 0.96; ucap.pitch = 1;
  const suara = (S.getVoices() || []).find(v => /^id/i.test(v.lang));
  if (suara) ucap.voice = suara;
  else if (!narasi._tunggu) {                 // daftar suara kadang baru siap sesudah peristiwa ini
    narasi._tunggu = true;
    S.addEventListener && S.addEventListener('voiceschanged', () => { narasi._tunggu = false; }, { once: true });
  }
  S.speak(ucap);
}

function isiBahan() {
  const wadah = document.getElementById('bahan');
  if (!wadah) return;
  const slugTopik = wadah.dataset.topik, kunciTP = wadah.dataset.tp, idT = wadah.dataset.tahapan;
  muatMedia(slugTopik).then(m => {
    const w = document.getElementById('bahan');
    if (!w || w.dataset.tahapan !== idT) return;             // halaman sudah berpindah
    if (!m) { w.innerHTML = `<p class="muted mkosong">${tr('Bahan pendukung belum diatur untuk topik ini.')}</p>`; return; }
    const daftar = (kunciTP ? ((m.tp || {})[kunciTP] || {})[idT] : (m.topik || {})[idT]) || [];
    if (!daftar.length) {
      const gerbang = ['S2', 'S8', 'S13'].indexOf(idT) >= 0;
      w.innerHTML = `<p class="muted mkosong">${tr(gerbang
        ? 'Gerbang penilaian — bahan bantu sengaja tidak disediakan.'
        : 'Belum ada bahan pendukung untuk tahapan ini.')}</p>`;
      return;
    }
    w.innerHTML = `<h3 class="mtajuk">${tr('Bahan pendukung')} <span class="mcacah">${daftar.length}</span></h3>
      <div class="mdaftar">${daftar.map(kartuBahan).join('')}</div>`;
    w.__daftar = daftar;
    const pertama = w.querySelector('.mkepala');
    if (pertama) pertama.click();                            // buka bahan pertama
  });
}

function isiPapanKelas() {
  const w = document.getElementById('papan-kelas');
  if (!w || !(window.FIMS && FIMS.aku && FIMS.aku.guru)) return;
  const tps = semuaTP();
  FIMS.papan().then(r => {
    const w2 = document.getElementById('papan-kelas'); if (!w2) return;
    if (!r.murid) { w2.innerHTML = `<p class="muted" style="margin:0">${esc(r.galat || tr('Tidak dapat memuat papan kelas.'))}</p>`; return; }
    papanMurid = r.murid || []; isiResetGuru();
    if (!r.murid.length) { w2.innerHTML = `<p class="muted" style="margin:0">${tr('Belum ada murid aktif. Setujui anggota lebih dulu di laman Anggota.')}</p>`; return; }
    const baris = m => `<tr><td class="l">${esc(m.nama || m.email.split('@')[0])}<br><span class="mono muted" style="font-size:.78em">${esc(m.email)}</span></td>` +
      tps.map(tp => { const h = hitungP((m.tp || {})[tp.slug], tp);
        return `<td class="cell st${h.s}" title="${tr(STATUS[h.s])}">${h.tier ? 'T' + h.tier : ''}</td>`; }).join('') +
      `</tr>`;
    w2.innerHTML = `<div class="scroll"><table><tr><th class="l">${tr('Murid')} <span class="mcacah">${r.murid.length}</span></th>` +
      tps.map(tp => `<th class="mono">${esc(tp.kode)}</th>`).join('') + `</tr>${r.murid.map(baris).join('')}</table></div>`;
  }).catch(() => {});

  muatAntrean();
}

/* ---------- guru: buka ulang SATU dokumen murid ----------
   Dua macam dokumen. (1) Tahapan S1–S14 pada satu TP: hasilnya tercatat di progres TP (skor/tanda selesai;
   S12 juga tier; S14 hasil terakhir). (2) Dokumen isian apa pun: lapis L1–L4, paket PRI UIN, pembuka, dokumen
   baru. Isiannya tersimpan per akun murid di tabel "lembar" dan ditunjuk lewat "kunci" (alamat berkas).
   Tahapan yang punya keduanya dibuka ulang sekaligus. Dokumen lain dan progres TP tetap.
   Penghapusan dikerjakan peladen (jalur guru/reset), yang memeriksa bahwa murid itu bimbingan guru ini atau
   yang memanggil adalah pemilik. Peramban murid menyusul sendiri dalam paling lama 30–45 detik. */
let resetTopikSengaja = false;                       // guru sudah memilih topik dengan tangan: jangan dipilihkan otomatis lagi
let papanMurid = [], resetMurid = '', resetTopik = '', resetPilih = null, resetPesan = '';   // resetTopik: slug topik, atau '~lain' = dokumen tanpa topik
let resetLembar = null, resetMemuat = false, resetLembarGalat = false;   // null = belum/sedang dimuat

const dekodeEntitas = s => { const e = document.createElement('textarea'); e.innerHTML = String(s == null ? '' : s); return e.value; };
const kunciBerkas = b => (window.FIMS && FIMS.kunciLembar) ? FIMS.kunciLembar(b) : '';

/* Kunci dokumen → nama yang dikenal guru (dari katalog). Kunci yang tak dikenal tetap ditampilkan apa adanya,
   jadi dokumen baru yang belum masuk katalog pun bisa dibuka ulang. */
function petaDokumen() {
  const peta = {};
  for (const t of K.topik) {
    if (t.pembuka && t.pembuka.berkas) peta[kunciBerkas(t.pembuka.berkas)] = { topik: t, label: tr('Fenomena Dunia Nyata') };
    for (const [id, l] of Object.entries(t.tahapan || {})) {
      if (!l) continue;
      if (l.berkas) peta[kunciBerkas(l.berkas)] = { topik: t, label: id + ' · ' + dekodeEntitas(l.judul || '') };
      if (l.latihan && l.latihan.berkas) peta[kunciBerkas(l.latihan.berkas)] = { topik: t, label: id + ' · ' + tr('Latihan Unit Test') };
    }
    for (const q of t.paket || []) if (q.berkas) peta[kunciBerkas(q.berkas)] = { topik: t, label: dekodeEntitas(q.judul || '') };
    for (const tp of t.tp || []) for (const [id, f] of Object.entries(tp.tahapan || {}))
      if (f && f.berkas) peta[kunciBerkas(f.berkas)] = { topik: t, tp, id };
  }
  return peta;
}

function ringkasLembar(l) {                          // satu baris untuk tombol dan konfirmasi
  const kecil = l.diubah ? tgl(l.diubah * 1000) : '';
  const skor = l.skor != null ? Math.round(l.skor) + '%' : null;
  if (l.selesai) return { besar: skor || '✓', kecil, frasa: skor ? trf('hasil dokumen (skor %s)', skor) : tr('hasil dokumen (selesai)') };
  const n = l.total ? `${l.terisi || 0}/${l.total}` : '…';
  return { besar: trf('terisi %s', n), kecil, frasa: trf('isian yang sudah diisi (%s)', n) };
}

function adaHasilTahapan(p, id) {
  return id === 'S14' ? !!(p.s14 || []).length : !!((p.ev || {})[id] || (id === 'S12' && p.tier));
}

function hasilDokumen(p, id) {                       // ringkas: apa yang akan hilang
  if (id === 'S14') {
    const a = (p.s14 || [])[(p.s14 || []).length - 1];
    return { besar: a ? tr(a.hasil) : '—', kecil: a ? tgl(a.waktu) : '', frasa: trf('hasil pengulangan terakhir (%s)', a ? tr(a.hasil) : '—') };
  }
  const e = (p.ev || {})[id] || {};
  const bukti = id === 'S12' && p.tier ? 'T' + p.tier : null;
  const besar = bukti || (e.skor != null ? e.skor + '%' : '✓');
  const frasa = id === 'S12'
    ? tr('bukti terkirim') + (p.tier ? ' ' + trf('dan tier T%s', p.tier) : '')
    : (e.skor != null ? trf('skor %s%', e.skor) : tr('tanda selesai'));
  return { besar, kecil: e.waktu ? tgl(e.waktu) : '', frasa };
}

function simulasiReset(p, id) {                      // cermin aturan peladen; hanya untuk pratinjau
  const q = JSON.parse(JSON.stringify(p)); q.ev = q.ev || {}; q.s14 = q.s14 || [];
  if (id === 'S14') {
    const c = q.s14.pop();
    if (c && c.hasil === 'gagal') {
      const g = [...q.s14].reverse().find(x => x.hasil === 'gagal');
      if (g) q.s14Mulai = (g.waktu || 0) + 1; else delete q.s14Mulai;
    }
  } else { delete q.ev[id]; if (id === 'S12') q.tier = null; }
  return q;
}

function dampakReset(tp, p, id) {
  const ukur = q => { const st = hitungP(q, tp);
    return { st, h: { e: q.ev || {}, s: st.s, tier: q.tier || 0, p: q, amb: tp.ambang || 75 } }; };
  const a = ukur(p), b = ukur(simulasiReset(p, id));
  const ids = TAHAPAN.map(s => s.id).filter(x => tp.tahapan[x] && x !== id);
  const kA = Object.fromEntries(ids.map(x => [x, kunci(tp, x, a.h)])), kB = Object.fromEntries(ids.map(x => [x, kunci(tp, x, b.h)]));
  return {
    status: a.st.s !== b.st.s || a.st.stabil !== b.st.stabil ? [a.st, b.st] : null,
    terkunci: ids.filter(x => kB[x] && !kA[x]),
    terbuka: ids.filter(x => kA[x] && !kB[x])
  };
}

async function muatLembar() {
  const murid = resetMurid;
  resetLembar = null; resetLembarGalat = false;
  if (!murid) { gambarResetIsi(); return; }
  resetMemuat = true; gambarResetIsi();
  let r; try { r = await FIMS.API('guru/lembar?murid=' + encodeURIComponent(murid)); } catch (e) { r = {}; }
  resetMemuat = false;
  if (murid !== resetMurid) return;                  // guru sudah memilih murid lain
  resetLembarGalat = !(r && r.ok && Array.isArray(r.lembar));
  resetLembar = resetLembarGalat ? [] : r.lembar;
  gambarResetIsi(true);                               // true: bila hanya satu topik yang dikerjakan, pilih otomatis
}

function isiResetGuru() {
  const sel = document.getElementById('reset-murid'); if (!sel) return;
  sel.innerHTML = `<option value="">${tr('Pilih murid…')}</option>` + papanMurid.map(m =>
    `<option value="${esc(m.email)}"${m.email === resetMurid ? ' selected' : ''}>${esc(m.nama || m.email.split('@')[0])}${m.kelas ? ' · ' + esc(m.kelas) : ''}</option>`).join('');
  if (!papanMurid.some(m => m.email === resetMurid)) { resetMurid = ''; resetLembar = null; }
  gambarResetIsi();
  if (resetMurid && resetLembar === null && !resetMemuat) muatLembar();
}

function gambarResetIsi(otomatis) {
  const isi = document.getElementById('reset-isi'), pes = document.getElementById('reset-pesan');
  const bar = document.getElementById('reset-topik-baris'), selT = document.getElementById('reset-topik');
  if (!isi) return;
  if (pes) pes.innerHTML = resetPesan ? `<div class="note reset-ok">${esc(resetPesan)}</div>` : '';
  const m = papanMurid.find(x => x.email === resetMurid);
  if (!m) { isi.innerHTML = ''; if (bar) bar.hidden = true; gambarResetKonfirmasi(); return; }

  const peta = petaDokumen(), lemTahapan = {}, lain = [];
  for (const l of (resetLembar || [])) {
    if (!l.adaIsi) continue;                         // sudah dikosongkan guru: tidak ada yang bisa dibuka ulang
    const d = peta[l.kunci];
    if (d && d.tp) lemTahapan[d.tp.slug + '|' + d.id] = l; else lain.push({ l, d });
  }
  const idsTP = (tp, p) => TAHAPAN.map(s => s.id).filter(id => adaHasilTahapan(p, id) || lemTahapan[tp.slug + '|' + id]);

  /* Topik yang SUDAH dikerjakan murid ini (ada hasil atau isian yang bisa dibuka ulang), beserta jumlah dokumennya. */
  const jmlDok = n => n === 1 ? tr('1 dokumen') : trf('%s dokumen', n);
  const jumlah = {}, nTanpaTopik = lain.filter(x => !x.d).length;
  for (const t of K.topik) {
    let n = 0;
    for (const tp of t.tp || []) n += idsTP(tp, (m.tp || {})[tp.slug] || {}).length;
    n += lain.filter(x => x.d && x.d.topik.slug === t.slug).length;
    if (n) jumlah[t.slug] = n;
  }
  const opsi = K.topik.filter(t => jumlah[t.slug]).map(t => ({ v: t.slug, teks: `${t.kode} · ${t.nama} — ${jmlDok(jumlah[t.slug])}` }));
  if (nTanpaTopik) opsi.push({ v: '~lain', teks: `${tr('Dokumen lain')} — ${jmlDok(nTanpaTopik)}` });
  const siap = resetLembar !== null;                 // daftar dokumen isian sudah sampai
  const lama = resetTopik;
  if (!opsi.some(o => o.v === resetTopik)) resetTopik = (otomatis && siap && !resetTopikSengaja && opsi.length === 1) ? opsi[0].v : '';
  if (resetTopik !== lama) resetPilih = null;

  if (bar && selT) {
    bar.hidden = false;
    selT.disabled = !opsi.length;
    selT.innerHTML = `<option value="">${tr(opsi.length ? 'Pilih topik…' : (siap ? 'Murid ini belum mengerjakan topik apa pun.' : 'Memuat dokumen isian…'))}</option>` +
      opsi.map(o => `<option value="${esc(o.v)}"${o.v === resetTopik ? ' selected' : ''}>${esc(o.teks)}</option>`).join('');
  }

  const dipilih = (tp, id, kunci) => !!resetPilih && (kunci ? resetPilih.kunci === kunci : (resetPilih.tp === tp && resetPilih.id === id));

  /* Hanya TP dari topik yang dipilih. Topik lain tidak digambar sama sekali. */
  const blokTP = !resetTopik || resetTopik === '~lain' ? '' : semuaTP().filter(tp => tp._t.slug === resetTopik).map(tp => {
    const p = (m.tp || {})[tp.slug] || {};
    const ids = idsTP(tp, p);
    if (!ids.length) return '';
    const h = hitungP(p, tp);
    const tombol = ids.map(id => {
      const l = lemTahapan[tp.slug + '|' + id], r = adaHasilTahapan(p, id) ? hasilDokumen(p, id) : ringkasLembar(l);
      const on = resetPilih && resetPilih.tp === tp.slug && resetPilih.id === id;
      return `<button type="button" class="rs-doc" data-rs="pilih" data-tp="${esc(tp.slug)}" data-id="${id}" data-kunci="${l ? esc(l.kunci) : ''}" aria-pressed="${on ? 'true' : 'false'}">
        <span class="rs-id">${id}</span><span class="rs-nm">${esc(tr(T(id).nama))}</span>
        <span class="rs-hasil">${esc(r.besar)}${r.kecil ? ` <small>· ${esc(r.kecil)}</small>` : ''}</span><span class="rs-ikon" aria-hidden="true">↺</span></button>`; }).join('');
    return `<div class="rs-tp"><div class="row" style="justify-content:space-between"><h3>${esc(tp.kode)} · ${esc(tp.judul)}</h3>${chip(h.s, h.stabil)}</div>
      <div class="rs-daftar">${tombol}</div></div>`;
  }).join('');

  const lainIni = !resetTopik ? [] : lain.filter(x => resetTopik === '~lain' ? !x.d : (x.d && x.d.topik.slug === resetTopik));
  const blokLain = !lainIni.length ? '' :
    `<div class="rs-tp"><h3>${esc(resetTopik === '~lain' ? tr('Dokumen lain') : (K.topik.find(t => t.slug === resetTopik) || {}).kode)} · ${tr('Lapis, paket, dan dokumen isian lain')}</h3><div class="rs-daftar">${lainIni.map(({ l, d }) => {
      const r = ringkasLembar(l);
      return `<button type="button" class="rs-doc" data-rs="pilih" data-kunci="${esc(l.kunci)}" aria-pressed="${dipilih('', '', l.kunci) ? 'true' : 'false'}">
        <span class="rs-nm">${esc(d ? d.label : l.kunci)}</span>
        <span class="rs-hasil">${esc(r.besar)}${r.kecil ? ` <small>· ${esc(r.kecil)}</small>` : ''}</span><span class="rs-ikon" aria-hidden="true">↺</span></button>`; }).join('')}</div></div>`;

  const status = resetLembar === null ? `<p class="muted" style="margin:0">${tr('Memuat dokumen isian…')}</p>`
    : (resetLembarGalat ? `<p class="muted" style="margin:0">${tr('Dokumen isian (lapis, paket) belum dapat dimuat. Tahapan di atas tetap bisa dibuka ulang.')}</p>` : '');
  let badan = blokTP + blokLain;
  if (!badan) {
    const kata = resetTopik ? 'Tidak ada lagi dokumen terisi pada topik ini.'
      : opsi.length ? 'Pilih topik di atas untuk melihat dokumen yang sudah dikerjakan murid ini.'
      : (siap && !resetLembarGalat ? 'Murid ini belum punya hasil tercatat.' : '');
    if (kata) badan = `<p class="muted" style="margin:0">${tr(kata)}</p>`;
  }
  isi.innerHTML = badan + status;
  gambarResetKonfirmasi();
}

function namaDokumenReset(pil) {
  if (pil.tp && pil.id) return pil.id + ' · ' + tr(T(pil.id).nama);
  const d = petaDokumen()[pil.kunci];
  return d ? d.label : pil.kunci;
}

function gambarResetKonfirmasi() {
  const k = document.getElementById('reset-konfirmasi'); if (!k) return;
  const m = papanMurid.find(x => x.email === resetMurid);
  if (!m || !resetPilih) { k.hidden = true; k.innerHTML = ''; return; }
  const pil = resetPilih, tp = pil.tp ? cariTP(pil.tp) : null, p = pil.tp ? ((m.tp || {})[pil.tp] || {}) : null;
  const l = pil.kunci ? (resetLembar || []).find(x => x.kunci === pil.kunci) : null;
  const adaTahap = !!(tp && adaHasilTahapan(p, pil.id));
  if (!adaTahap && !l) { k.hidden = true; k.innerHTML = ''; return; }
  const nm = m.nama || m.email.split('@')[0];
  const hasil = adaTahap ? hasilDokumen(p, pil.id) : null, d = adaTahap ? dampakReset(tp, p, pil.id) : null;
  const baris = [
    adaTahap ? `<li>${trf('Dihapus: %s', `<b>${esc(hasil.frasa)}</b>${hasil.kecil ? ' (' + esc(hasil.kecil) + ')' : ''}`)}</li>` : '',
    l ? `<li>${trf('Dihapus: %s', `<b>${esc(ringkasLembar(l).frasa)}</b>${l.diubah ? ' (' + esc(tgl(l.diubah * 1000)) + ')' : ''}`)}</li>` : '',
    `<li>${tr(tp ? 'Tetap utuh: dokumen lain dan progres TP ini.' : 'Tetap utuh: dokumen lain dan progres TP murid.')}</li>`,
    d ? `<li>${d.status ? trf('Status %s: %s → %s', esc(tp.kode), chip(d.status[0].s, d.status[0].stabil), chip(d.status[1].s, d.status[1].stabil)) : tr('Status TP tidak berubah.')}</li>` : '',
    d && d.terkunci.length ? `<li>${trf('Terkunci lagi untuk murid: %s', esc(d.terkunci.join(', ')))}</li>` : '',
    d && d.terbuka.length ? `<li>${trf('Terbuka lagi untuk murid: %s', esc(d.terbuka.join(', ')))}</li>` : ''
  ].join('');
  k.hidden = false;
  k.innerHTML = `<div class="note rs-konfirm"><b>${trf('Buka ulang %s untuk %s?', esc(namaDokumenReset(pil)), esc(nm))}</b>
    <ul>${baris}</ul>
    <div class="row"><label for="rs-alasan">${tr('Alasan (opsional, terlihat oleh murid)')}</label>
      <input type="text" id="rs-alasan" maxlength="160" style="flex:1;min-width:200px"></div>
    <div class="row"><button type="button" class="btn" data-rs="ya">${tr('Ya, buka ulang')}</button>
      <button type="button" class="btn ghost" data-rs="batal">${tr('Batal')}</button></div></div>`;
}

async function jalankanReset(tombol) {
  const m = papanMurid.find(x => x.email === resetMurid); if (!m || !resetPilih) return;
  const pil = resetPilih, alasan = (document.getElementById('rs-alasan') || {}).value || '';
  const badan = { murid: m.email, alasan };
  if (pil.tp && pil.id) { badan.tp = pil.tp; badan.tahapan = pil.id; }
  if (pil.kunci) badan.kunci = pil.kunci;
  tombol.disabled = true;
  let r;
  try { r = await FIMS.API('guru/reset', { method: 'POST', body: JSON.stringify(badan) }); }
  catch (e) { r = { galat: String(e) }; }
  if (r && r.ok) {
    if (r.data && pil.tp) { m.tp = m.tp || {}; m.tp[pil.tp] = r.data; }
    resetPesan = trf('%s sudah dibuka ulang untuk %s. Murid melihatnya paling lambat 45 detik lagi.', namaDokumenReset(pil), m.nama || m.email.split('@')[0]);
    resetPilih = null;
    await muatLembar();                               // daftar dokumen isian ikut segar
    isiPapanKelas();                                  // papan dan antrean ikut segar
  } else {
    tombol.disabled = false;
    const pes = document.getElementById('reset-pesan');
    if (pes) pes.innerHTML = `<div class="note reset-gagal">${esc((r && r.galat) || tr('Gagal membuka ulang.'))}</div>`;
  }
}

document.addEventListener('click', ev => {
  const b = ev.target.closest('[data-rs]'); if (!b) return;
  const a = b.dataset.rs;
  if (a === 'pilih') { resetPilih = { tp: b.dataset.tp || '', id: b.dataset.id || '', kunci: b.dataset.kunci || '' }; resetPesan = ''; gambarResetIsi(); return; }
  if (a === 'batal') { resetPilih = null; gambarResetIsi(); return; }
  if (a === 'ya') jalankanReset(b);
});
document.addEventListener('change', ev => {
  if (ev.target.id === 'reset-murid') { resetMurid = ev.target.value; resetPilih = null; resetPesan = ''; resetTopikSengaja = false; muatLembar(); }
  if (ev.target.id === 'reset-topik') { resetTopik = ev.target.value; resetTopikSengaja = true; resetPilih = null; resetPesan = ''; gambarResetIsi(); }
});

/* ---------- murid: salinan terbaru dari peladen (guru menilai atau membuka ulang) ---------- */
document.addEventListener('fims:progres', ev => {
  const tp = (ev.detail && ev.detail.tp) || {};
  let tahapanIniBerubah = false;
  for (const [slug, data] of Object.entries(tp)) {
    if (cur && cur.tp.slug === slug) {
      const lama = db.tp[slug] || {}, id = cur.id;
      if (JSON.stringify([(lama.ev || {})[id], lama.tier, lama.s14]) !== JSON.stringify([(data.ev || {})[id], data.tier, data.s14])) tahapanIniBerubah = true;
    }
    db.tp[slug] = data;
  }
  try { localStorage.setItem(KEY, JSON.stringify(db)); } catch (e) {}     // data dari peladen: tidak didorong balik
  // Lembar isian yang sedang terbuka (paket, lapis, pembuka) jangan dimuat ulang: jawaban yang diketik akan hilang.
  if (/-p-|-l[1-4](-latihan)?$|-pembuka$/.test(location.hash)) return;
  if (cur && !tahapanIniBerubah) { segarkanSetelahSkor(); return; }       // lembar tahapan tetap hidup
  render();
});

/* Mengingat panel mana yang dilipat, per peramban. */
function pasangLipat() {
  document.querySelectorAll('details.lipat[data-lipat]').forEach(d => {
    if (d.dataset.lipatSiap) return;
    d.dataset.lipatSiap = '1';
    d.addEventListener('toggle', () => {
      try { localStorage.setItem('fims.lipat.' + d.dataset.lipat, d.open ? 'buka' : 'tutup'); } catch {}
    });
  });
}

/* Antrean penilaian guru: S12 menunggu tier, S8 menunggu skor gerbang kelas. */
function muatAntrean() {
  const w = document.getElementById('antrean-nilai');
  if (!w || !(window.FIMS && FIMS.aku && FIMS.aku.guru)) return;
  const judulTP = slug => { const tp = semuaTP().find(x => x.slug === slug); return tp ? tp.kode : slug; };
  const tgl = d => d ? new Date(d * 1000).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }) : '—';

  FIMS.API('guru/antrean').then(r => {
    const w2 = document.getElementById('antrean-nilai'); if (!w2) return;
    if (!r.antrean) { w2.innerHTML = `<p class="muted" style="margin:0">${esc(r.galat || tr('Tidak dapat memuat antrean penilaian.'))}</p>`; return; }
    if (!r.antrean.length) { w2.innerHTML = `<p class="muted" style="margin:0">${tr('Tidak ada yang menunggu penilaianmu.')}</p>`; return; }
    w2.innerHTML = `<div class="scroll"><table><tr>
        <th class="l">${tr('Murid')} <span class="mcacah">${r.antrean.length}</span></th>
        <th class="l">${tr('Tujuan Pembelajaran')}</th><th>${tr('Tahapan')}</th>
        <th>${tr('Menunggu sejak')}</th><th class="l">${tr('Nilai')}</th></tr>` +
      r.antrean.map((x, i) => `<tr data-antre="${i}">
        <td class="l">${esc(x.nama || x.email.split('@')[0])}<br><span class="mono muted" style="font-size:.78em">${esc(x.email)}</span></td>
        <td class="l mono">${esc(judulTP(x.tp))}</td>
        <td class="mono">${esc(x.tahapan)}</td>
        <td>${tgl(x.diubah)}</td>
        <td class="l nilai-sel">${x.minta === 'tier'
          ? `<select class="nilai-isi" aria-label="Tier"><option value="">T?</option><option value="1">T1</option><option value="2">T2</option><option value="3">T3</option><option value="4">T4</option></select>`
          : `<input class="nilai-isi" type="number" min="0" max="100" step="1" placeholder="${tr('Skor 0–100')}" aria-label="${tr('Skor 0–100')}">`}
          <button class="btn kecil" data-simpan-nilai="${i}">${tr('Simpan')}</button></td></tr>`).join('') +
      `</table></div>`;

    w2.addEventListener('click', async ev => {
      const b = ev.target.closest('[data-simpan-nilai]'); if (!b) return;
      const x = r.antrean[+b.dataset.simpanNilai]; if (!x) return;
      const isi = b.closest('.nilai-sel').querySelector('.nilai-isi');
      const v = String(isi.value || '').trim();
      if (!v) { isi.focus(); return; }
      const badan = { murid: x.email, tp: x.tp, tahapan: x.tahapan };
      if (x.minta === 'tier') badan.tier = Number(v);
      else {
        const n = Number(v);
        if (!isFinite(n) || n < 0 || n > 100) { alert(tr('Skor harus 0–100.')); isi.focus(); return; }
        badan.skor = n;
      }
      b.disabled = true;
      const r2 = await FIMS.API('guru/nilai', { method: 'POST', body: JSON.stringify(badan) });
      if (!r2.ok) { b.disabled = false; alert(r2.galat || tr('Gagal menyimpan nilai.')); return; }
      const tr0 = b.closest('tr');
      tr0.querySelector('.nilai-sel').innerHTML = `<span class="muted">${tr('Tersimpan.')}</span>`;
      tr0.classList.add('sudah');
    }, { once: false });
  }).catch(() => {});
}

function render() {
  rangka();
  const priorRail = document.querySelector('.study-rail');
  const prior = priorRail ? { tp: priorRail.dataset.studyTp, top: priorRail.querySelector('.study-rail-scroll').scrollTop, open: !priorRail.querySelector('.study-rail-scroll').hidden } : null;
  const h = decodeURIComponent(location.hash.slice(1));
  let html, m; cur = null;
  $('#nav-guru').classList.toggle('on', h === 'guru');
  $('#nav-belajar').classList.toggle('on', h !== 'guru');
  if (h === 'anggota' && window.FIMS && FIMS.aku && FIMS.aku.owner) { rangka(); FIMS.halAnggota(); return; }
  if (h === 'guru') html = halGuru();
  else if ((m = h.match(/^jalur-(.+)$/)) && cariJalur(m[1])) html = halJalur(cariJalur(m[1]));
  else if ((m = h.match(/^topik-(.+)-pembuka$/)) && cariTopik(m[1])) html = halPembuka(cariTopik(m[1]));
  else if ((m = h.match(/^topik-(.+?)-p-(.+)$/)) && cariTopik(m[1])) html = halPaket(cariTopik(m[1]), m[2]);
  else if ((m = h.match(/^topik-(.+)-(l[1-4])(?:-(latihan))?$/)) && cariTopik(m[1])) html = halLapis(cariTopik(m[1]), m[2].toUpperCase(), m[3]);
  else if ((m = h.match(/^topik-(.+)$/)) && cariTopik(m[1])) html = halTopik(cariTopik(m[1]));
  else if ((m = h.match(/^tp-(.+)-(s\d+[bc]?)$/)) && cariTP(m[1])) { const id = m[2].toUpperCase().replace(/([BC])$/, c => c.toLowerCase()); cur = { tp: cariTP(m[1]), id }; html = halTP(cur.tp, id); }
  else if ((m = h.match(/^tp-(.+)$/)) && cariTP(m[1])) html = halTP(cariTP(m[1]));
  else html = beranda();
  $('#app').innerHTML = html;
  const rail = document.querySelector('.study-rail');
  if (rail && prior && prior.tp === rail.dataset.studyTp) bukaDaftarTahapan(rail, prior.open);
  posisikanTahapan(rail, rail && prior && prior.tp === rail.dataset.studyTp ? prior.top : 0);
  pasangLipat();
  if (window.speechSynthesis) window.speechSynthesis.cancel();   // hentikan narasi halaman sebelumnya
  isiBahan();
  isiPapanKelas();
  window.scrollTo(0, 0);
}

function tpDariHash() { const m = location.hash.match(/^#tp-(.+?)(-s\d+[bc]?)?$/); return m ? cariTP(m[1]) : null; }

document.addEventListener('click', ev => {
  const toggle = ev.target.closest('[data-study-toggle]');
  if (toggle) {
    const rail = toggle.closest('.study-rail');
    bukaDaftarTahapan(rail, toggle.getAttribute('aria-expanded') !== 'true');
    posisikanTahapan(rail);
    return;
  }
  const lb = ev.target.closest('[data-bhs]');
  if (lb) { const v = lb.dataset.bhs === 'en' ? 'en' : 'id';
    if (v !== BHS) { BHS = v; db.opsi.bahasa = v; simpan();
      document.dispatchEvent(new CustomEvent('fims:bahasa', { detail: v }));
      render(); } return; }
  const mk = ev.target.closest('[data-media]');
  if (mk) {
    const kartu = mk.closest('.mkartu'), isi = kartu.querySelector('.misi');
    const w = document.getElementById('bahan'), daftar = (w && w.__daftar) || [];
    const buka = isi.hasAttribute('hidden');
    if (buka) { isiPemutar(isi, daftar[+mk.dataset.media] || {}); isi.removeAttribute('hidden'); }
    else { isi.setAttribute('hidden', ''); if (window.speechSynthesis) window.speechSynthesis.cancel(); }
    kartu.classList.toggle('buka', buka);
    mk.setAttribute('aria-expanded', buka ? 'true' : 'false');
    mk.querySelector('.mtanda').textContent = buka ? '−' : '+';
    return;
  }
  const nb = ev.target.closest('[data-narasi]');
  if (nb) {
    const teks = nb.closest('.mnarasi').querySelector('.mnaskah').textContent;
    narasi(nb.dataset.narasi, teks);
    return;
  }
  const b = ev.target.closest('[data-aksi],[data-geser]'); if (!b) return;
  if (b.dataset.geser != null) { db.opsi.geser = +b.dataset.geser ? (db.opsi.geser || 0) + +b.dataset.geser : 0; simpan(); return render(); }
  const a = b.dataset.aksi, tp = tpDariHash(); if (!tp) return;
  if (a === 'selesai' && cur) catat(tp, cur.id, {});
  if (a === 'skor' && cur) { const v = parseFloat($('#skorIn').value); if (isNaN(v)) return $('#skorIn').focus(); catat(tp, cur.id, { skor: Math.max(0, Math.min(100, v)) }); }
  if (a === 'reset') { delete db.tp[tp.slug]; simpan(); }
  render();
});
document.addEventListener('change', ev => {
  if (ev.target.id === 'tierIn') { const tp = tpDariHash(); if (tp) { prog(tp.slug).tier = +ev.target.value || null; simpan(); render(); } }
  if (ev.target.id === 'modeGuru') { db.opsi.guru = ev.target.checked; simpan(); render(); }
});
// jembatan skor dari halaman HTML tahapan
window.addEventListener('message', ev => {
  const d = ev.data;
  // Dokumen isian yang melapor selesai/skor: teruskan ke penyimpan per akun di dalam dokumen itu,
  // di rute mana pun (tahapan, lapis, paket), supaya skor ikut tersimpan di akun murid.
  if (d && (d.fims === 'skor' || d.fims === 'selesai') && ev.source) {
    try { if (ev.source.FIMS_LEMBAR) ev.source.FIMS_LEMBAR.lapor(d.fims === 'skor' && typeof d.skor === 'number' ? { selesai: true, skor: d.skor } : { selesai: true }); } catch (e) {}
  }
  if (!d || !d.fims || !cur) return;
  const s = T(cur.id);
  if (d.fims === 'skor' && typeof d.skor === 'number' && (s.skor || cur.id === 'S14'))
    catat(cur.tp, cur.id, { skor: d.skor, salah: d.salah, benar: d.benar, total: d.total });
  else if (d.fims === 'selesai') catat(cur.tp, cur.id, {});   // skor yang sudah ada tidak tertimpa
  else return;
  segarkanSetelahSkor();     // lembar di dalam bingkai dibiarkan hidup
});
/* Dokumen isian yang tampil di dalam situs dipasangi penyimpan jawaban per akun (assets/fims-simpan.js)
   bila belum punya. Jadi dokumen baru yang kelak diunggah ikut tersimpan walau tag-nya lupa ditambahkan. */
document.addEventListener('load', ev => {
  const f = ev.target; if (!f || f.tagName !== 'IFRAME' || !f.classList.contains('frame')) return;
  try {
    const w = f.contentWindow, d = f.contentDocument;
    if (!w || !d || !d.body || w.FIMS_LEMBAR || d.getElementById('fims-simpan-js')) return;
    if (!d.querySelector('input, select, textarea')) return;
    const s = d.createElement('script'); s.id = 'fims-simpan-js';
    s.src = new URL('assets/fims-simpan.js', location.href).href;
    d.body.appendChild(s);
  } catch (e) {}
}, true);
window.addEventListener('hashchange', render);
document.addEventListener('fims:mode', render);        // guru menukar mode tampilan

fetch('katalog.json').then(r => r.json()).then(k => {
  K = k;
  const kotak = $('#modeGuru'); if (kotak) kotak.checked = guru();   // kotak lama, tidak ada lagi sesudah akun dipasang
  render();
}).catch(() => { rangka(); $('#app').innerHTML = `<div class="note">${tr('katalog.json belum ada. Jalankan <span class="mono">node build.js</span> (Cloudflare menjalankannya otomatis).')}</div>`; });
})();
