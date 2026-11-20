# -*- coding: utf-8 -*-
"""Materi mandiri Newton sebab–akibat dan analisis struktur.

Data lokal untuk P1/P3/P4/P8 serta bank P2/P5/P7/P9/P10. Konvensi:
kanan/atas positif; momen berlawanan jarum jam positif; g = 10 m/s².
Gambar penilaian hanya menyatakan data, bukan hasil perhitungan.
"""

from copy import deepcopy


def _lab(kind, **params):
    return {"kind": kind, "params": params}


def _choice(indicator, prompt, options, answer, explain, *, level="C2", seconds=120, diagram=None):
    q = {"indicator": indicator, "prompt": prompt, "kind": "choice",
         "label": "Pilih satu jawaban", "unit": "", "options": list(options),
         "answer": answer, "explain": explain, "level": level, "seconds": max(seconds, {"C1":120,"C2":120,"C3":180,"C4":240,"C5":300,"C6":300}.get(level,120))}
    if diagram:
        q["diagram"] = diagram
    return q


def _num(indicator, prompt, label, answer, unit, explain, *, tol=0.05,
         level="C3", seconds=180, diagram=None, steps=None):
    q = {"indicator": indicator, "prompt": prompt, "kind": "num", "label": label,
         "unit": unit, "answer": answer, "tol": tol, "explain": explain,
         "level": level, "seconds": max(seconds, {"C1":120,"C2":120,"C3":180,"C4":240,"C5":300,"C6":300}.get(level,120))}
    if diagram:
        q["diagram"] = diagram
    if steps:
        q["steps"] = steps
    return q


LESSONS = {
    "f-mek-1a": {
        "hook": {
            "title": "Dua papan beroda, satu interaksi",
            "scene": "Pada ilustrasi, dua tokoh berdiri di atas papan beroda ideal yang mula-mula diam. Ketika tangan mereka saling menekan, keduanya menjauh. Tokoh dengan massa total lebih kecil berubah kecepatan lebih cepat. Ini adalah model di layar untuk dipelajari, bukan petunjuk mencoba kegiatan di atas papan.",
            "question": "Jika gaya saling tekan sama besar, mengapa perubahan gerak kedua tokoh bisa berbeda? Setelah tangan terpisah, apakah mereka harus langsung berhenti?",
            "bridge": "Pisahkan tiga pertanyaan: apa yang mempertahankan gerak, apa yang mengubah gerak, dan benda mana yang menerima tiap gaya. Tiga Hukum Newton menjawab pertanyaan yang berbeda tetapi saling terhubung.",
            "lab": _lab("reaction", F=60, m1=30, m2=60, t=2),
        },
        "goals": [
            "Menjelaskan bahwa gaya neto nol mempertahankan kecepatan, termasuk keadaan diam.",
            "Menjelaskan bagaimana gaya neto dan massa menentukan perubahan kecepatan, dengan membedakan percepatan dari kecepatan.",
            "Menamai pasangan aksi–reaksi dengan pemberi dan penerimanya, lalu menjelaskan mengapa percepatan dua benda dapat berbeda.",
            "Memilih dan menulis contoh baru berdasarkan mekanisme sebab–akibat tiap hukum, disertai asumsi yang masuk akal.",
        ],
        "concepts": [
            {
                "id": "n1", "title": "Hukum I: yang bertahan adalah kecepatan",
                "question": "Sebuah kereta sensor terus melaju walau pendorongnya sudah lepas. Gaya apa yang diperlukan agar kecepatannya tetap?",
                "explain": [
                    "Kecepatan menyatakan seberapa cepat sekaligus ke arah mana posisi berubah. Percepatan menyatakan perubahan kecepatan per satuan waktu. Benda yang terus berpindah belum tentu mengalami percepatan: gerak lurus dengan kecepatan tetap mempunyai a = 0. Kata lurus penting karena perubahan arah juga merupakan perubahan kecepatan.",
                    "Hukum I menyatakan bahwa, dalam kerangka inersial, benda mempertahankan keadaan diam atau gerak lurus dengan kecepatan tetap bila gaya netonya nol. Gaya neto adalah jumlah vektor semua gaya pada benda yang dipilih. Nol tidak berarti setiap gaya harus tidak ada; dua gaya yang sama besar dan berlawanan arah dapat menghasilkan jumlah nol.",
                    "Pilih kereta sebagai benda tinjauan. Panah gaya horizontal harus mempunyai pemberi, misalnya tangan, tali, atau lintasan. Setelah tangan terpisah, tidak ada lagi gaya tangan pada kereta. Pada model lintasan tanpa gesekan, kecepatan awalnya bertahan. Berat ke bawah dan normal lintasan ke atas tetap ada, tetapi saling menyeimbangkan pada arah tegak.",
                    "Kelembaman adalah sifat benda mempertahankan keadaan geraknya, bukan gaya tersembunyi yang mendorong ke depan. Pada lintasan nyata, hambatan membuat kereta melambat setelah dilepas. Penyebab perlambatan adalah gaya hambatan; berakhirnya dorongan hanya menghilangkan satu interaksi. Karena itu model tanpa hambatan harus selalu disebutkan ketika memprediksi gerak terus-menerus.",
                ],
                "formula": "ΣF = 0 ⇒ a = 0 ⇒ v tetap; untuk gaya tetap: v = v₀ + at",
                "quantities": ["ΣF: gaya neto pada satu benda (N)", "a: percepatan (m/s²)", "v dan v₀: kecepatan beserta tanda arah (m/s)", "t: selang waktu (s)"],
                "assumptions": ["Pengamatan dari lantai/laboratorium yang dianggap kerangka inersial.", "Gerak horizontal satu dimensi; normal dan berat seimbang.", "Gaya yang dimasukkan adalah seluruh gaya horizontal; hambatan boleh diabaikan hanya jika dinyatakan."],
                "lab": _lab("motion", right=12, left=12, m=4, v0=3, t=4),
                "explore": ["Prediksi: apakah kereta yang v₀ = 3 m/s berhenti ketika dua gaya 12 N seimbang?", "Ubah hanya kecepatan awal menjadi 0 lalu −3 m/s, dengan gaya tetap seimbang.", "Amati bahwa a tetap nol, tetapi keadaan diam, gerak kanan, dan gerak kiri dapat berbeda.", "Jelaskan mengapa gaya neto nol tidak cukup untuk menyimpulkan posisi atau arah gerak awal."],
                "misconception": {"claim": "Kalau benda masih bergerak, pasti masih ada gaya neto searah gerak.", "explain": "Gerak yang sudah ada dapat bertahan tanpa gaya neto. Gaya neto dibutuhkan untuk mengubah kecepatan; untuk melawan gesekan pada kecepatan tetap, dorongan hanya menyeimbangkan hambatan."},
                "worked": {
                    "scenario": "Kereta pengukur bergerak ke kanan 2 m/s. Tali menariknya ke kanan 9 N dan hambatan ke kiri 9 N selama 5 s. Jelaskan keadaan geraknya pada akhir selang itu.",
                    "steps": ["Model: tinjau kereta saja dalam kerangka lantai, dengan gaya horizontal tetap.", "Data: Fkanan = 9 N, Fkiri = 9 N, v₀ = +2 m/s, Δt = 5 s.", "Diagram: gambar dua panah horizontal sama panjang pada kereta; tandai kanan sebagai positif. Berat dan normal seimbang pada arah tegak.", "Persamaan: ΣFx = 9 − 9 = 0, sehingga a = 0 dan v = v₀ + at.", "Hitung: v = 2 + 0 × 5 = +2 m/s.", "Makna dan cek: kereta tetap bergerak ke kanan; ia tidak berhenti. Setiap detik kecepatannya tidak berubah, sesuai gaya neto nol."],
                    "result": "Kecepatan akhir tetap +2 m/s. Gaya-gaya ada, tetapi tidak ada perubahan kecepatan.",
                },
                "checks": [
                    _choice("n1", "Sebuah peluncur sudah bergerak ke kiri di lintasan tanpa hambatan. Kedua gaya horizontal pada gambar sama besar. Penjelasan yang tepat adalah…", ["Peluncur berhenti karena gaya neto nol.", "Peluncur tetap bergerak ke kiri dengan kecepatan tetap.", "Peluncur berbalik ke kanan karena panah kanan ada."], 1, "Gaya neto nol memberi a = 0. Tanda kecepatan awal tetap, sehingga gerak kiri bertahan.", diagram=_lab("motion", right=8, left=8, m=2, v0=-2, t=3)),
                    _choice("n1", "Yang paling tepat menjelaskan kata kelembaman adalah…", ["Gaya tambahan ke arah gerak.", "Sifat mempertahankan keadaan gerak ketika gaya neto nol.", "Kecenderungan semua benda berhenti tanpa sebab."], 1, "Kelembaman adalah sifat benda, bukan panah gaya baru. Untuk memperbaiki diagram, periksa pemberi setiap gaya."),
                ],
            },
            {
                "id": "n2", "title": "Hukum II: sebabnya gaya neto, akibatnya percepatan",
                "question": "Mengapa gaya neto yang sama lebih banyak mengubah gerak kereta ringan dibanding kereta penuh muatan?",
                "explain": [
                    "Hukum II menghubungkan gaya neto dengan percepatan: ΣF = ma untuk massa tetap. Resultan semua gaya pada satu benda menentukan arah perubahan kecepatannya. Massa mengukur kelembaman: untuk gaya neto sama, massa lebih besar menghasilkan percepatan lebih kecil. Satu newton sama dengan satu kg·m/s².",
                    "Perbandingan harus mengendalikan variabel. Jika massa tetap dan gaya neto digandakan, percepatan menjadi dua kali. Jika gaya neto tetap dan massa digandakan, percepatan menjadi separuh. Yang dibandingkan adalah gaya neto, bukan hanya gaya tarik. Kereta yang ditarik lebih kuat bisa tetap berpercepatan kecil jika hambatannya juga besar.",
                    "Arah percepatan tidak selalu sama dengan arah kecepatan. Kereta yang sedang bergerak ke kanan tetapi mempunyai gaya neto ke kiri mula-mula melambat. Sesudah kecepatannya mencapai nol, ia dapat berbalik bila gaya neto ke kiri terus bekerja. Saat kecepatan sesaat nol, percepatannya bahkan dapat tetap tidak nol.",
                    "Rangkaian penjelasan yang lengkap dimulai dari interaksi, dilanjutkan jumlah gaya, kemudian percepatan, baru perubahan kecepatan selama suatu waktu. Besar gaya saja tidak cukup untuk menyimpulkan kelajuan: kita juga perlu massa, kecepatan awal, dan lama gaya bekerja. Persamaan v = v₀ + at hanya digunakan pada selang dengan percepatan tetap.",
                ],
                "formula": "a = ΣF/m; pada sumbu kanan positif: a = (Fkanan − Fkiri)/m; Δv = aΔt",
                "quantities": ["m: massa/inersia (kg)", "Fkanan dan Fkiri: besar gaya horizontal berlawanan (N)", "a: perubahan kecepatan per detik (m/s²)", "Δv: selisih kecepatan akhir dan awal (m/s)"],
                "assumptions": ["Massa tetap selama pengamatan.", "Gaya horizontal dianggap tetap untuk membaca perubahan selama t.", "Positif ke kanan; kecepatan dan percepatan diberi tanda secara terpisah."],
                "lab": _lab("motion", right=18, left=6, m=3, v0=-4, t=1),
                "explore": ["Prediksi: kecepatan awal ke kiri dan gaya neto ke kanan; apakah kereta langsung bergerak ke kanan?", "Ubah hanya massa dari 3 kg menjadi 6 kg; pertahankan kedua gaya dan waktu.", "Amati arah percepatan dan perubahan kecepatan. Bandingkan perubahan per detik, bukan hanya posisi akhir.", "Jelaskan mengapa massa dua kali menghasilkan perubahan kecepatan separuh untuk gaya dan waktu yang sama."],
                "misconception": {"claim": "Percepatan ke kanan berarti benda pasti sedang bergerak ke kanan.", "explain": "Percepatan menunjukkan arah perubahan kecepatan. Kecepatan awal ke kiri dapat menjadi kurang negatif, sehingga benda masih ke kiri sambil melambat."},
                "worked": {
                    "scenario": "Kereta 4 kg bergerak ke kanan 6 m/s. Gaya 4 N ke kanan dan 12 N ke kiri bekerja selama 2 s. Apa yang berubah?",
                    "steps": ["Model: tinjau satu kereta, massa dan kedua gaya tetap; kanan positif.", "Data: m = 4 kg, v₀ = +6 m/s, Fkanan = 4 N, Fkiri = 12 N, t = 2 s.", "Diagram: panah 12 N ke kiri lebih panjang daripada panah 4 N ke kanan; panah kecepatan ke kanan digambar terpisah dari gaya.", "Persamaan sebab: ΣFx = 4 − 12 = −8 N; a = ΣFx/m = −8/4 = −2 m/s².", "Hitung akibat selama 2 s: v = 6 + (−2)(2) = +2 m/s.", "Makna: gaya neto dan percepatan ke kiri, tetapi kereta masih bergerak ke kanan sambil melambat.", "Cek: kecepatannya berkurang 2 m/s tiap detik. Waktu untuk mencapai nol adalah 3 s, lebih lama daripada 2 s yang diamati."],
                    "result": "Percepatan −2 m/s² dan kecepatan akhir +2 m/s: perubahan gerak berlawanan dengan arah gerak saat itu.",
                },
                "checks": [
                    _choice("n2", "Dua kereta mendapat gaya neto sama selama waktu sama dan mulai dari diam. Massa B dua kali massa A. Mengapa kecepatan B bertambah lebih sedikit?", ["Gaya pada B pasti lebih kecil.", "Massa B lebih besar, sehingga percepatannya separuh A.", "B menerima gaya hanya sesudah A bergerak."], 1, "a = ΣF/m. Gaya dan waktu dikendalikan; massa dua kali membuat a dan Δv separuh.", seconds=180),
                    _choice("n2", "Benda bergerak ke kiri, lalu gaya netonya ke kanan. Pada awal selang benda…", ["Dapat tetap ke kiri sambil melambat.", "Pasti langsung melompat ke arah kanan.", "Tidak mempunyai percepatan sampai berhenti."], 0, "Gaya neto kanan menghasilkan percepatan kanan sejak awal; kecepatan kiri berkurang besarnya secara bertahap.", seconds=180),
                ],
            },
            {
                "id": "n3", "title": "Hukum III: satu interaksi, dua penerima gaya",
                "question": "Jika kedua papan saling menekan sama kuat, mengapa papan yang lebih ringan mempunyai percepatan lebih besar?",
                "explain": [
                    "Gaya adalah interaksi antara dua benda. Jika A mengerjakan gaya pada B, B secara bersamaan mengerjakan gaya pada A dengan besar sama dan arah berlawanan. Nama lengkapnya penting: gaya A pada B berpasangan dengan gaya B pada A. Keduanya timbul dari satu interaksi, bukan satu gaya yang bekerja dahulu lalu menunggu balasan.",
                    "Dua panah pasangan ini berada pada dua diagram benda yang berbeda. Pada diagram A hanya masuk gaya dari B pada A; gaya dari A pada B masuk diagram B. Oleh sebab itu pasangan aksi–reaksi tidak saling menghapus dalam persamaan gaya untuk satu benda. Ketika A dan B dipandang sebagai satu sistem, pasangan tersebut menjadi gaya internal yang jumlahnya nol; gerak tiap bagian tetap bisa berubah.",
                    "Kesamaan gaya tidak menjamin kesamaan percepatan. Jika hambatan horizontal diabaikan, |aA| = F/mA dan |aB| = F/mB. Untuk gaya interaksi sama, benda yang massanya lebih kecil mempunyai percepatan lebih besar. Sesudah kontak berakhir, gaya kontak hilang; gerak setelahnya ditentukan gaya yang masih bekerja, sesuai Hukum I dan II.",
                    "Berat buku adalah gaya gravitasi Bumi pada buku. Pasangannya ialah gaya gravitasi buku pada Bumi, bukan gaya normal meja pada buku. Normal adalah gaya kontak meja pada buku, yang berpasangan dengan gaya buku pada meja. Berat dan normal bisa seimbang pada buku, tetapi berasal dari interaksi berbeda dan bekerja pada penerima yang sama.",
                ],
                "formula": "FA pada B = −FB pada A; |aA| = F/mA dan |aB| = F/mB jika itulah gaya neto horizontalnya",
                "quantities": ["FA pada B: gaya A yang diterima B (N)", "FB pada A: gaya B yang diterima A (N)", "mA, mB: massa masing-masing sistem benda termasuk papan (kg)", "aA, aB: percepatan masing-masing benda (m/s²)"],
                "assumptions": ["Papan dan penumpangnya dianggap satu benda untuk tiap sisi.", "Hambatan horizontal diabaikan; gaya saling tekan konstan selama t.", "Kedua benda mula-mula diam pada lab; gaya pada benda kiri ke kiri dan pada benda kanan ke kanan."],
                "lab": _lab("reaction", F=48, m1=24, m2=48, t=2),
                "explore": ["Prediksi: jika massa kanan dua kali massa kiri, apakah panah gaya kontaknya berbeda panjang?", "Ubah hanya massa kanan menjadi sama dengan massa kiri, lalu menjadi tiga kali massa kiri.", "Amati kedua panah gaya tetap sama besar, sedangkan percepatan dan jarak setelah waktu sama berubah.", "Jelaskan memakai dua persamaan gaya untuk dua benda, bukan menjumlah kedua panah pada satu papan."],
                "misconception": {"claim": "Aksi dan reaksi selalu saling meniadakan sehingga tidak mungkin ada gerak.", "explain": "Pasangan tersebut diterima dua benda berbeda. Gaya yang dapat saling menyeimbangkan pada diagram satu benda harus sama-sama bekerja pada benda itu."},
                "worked": {
                    "scenario": "Dua modul beroda A dan B bermassa 20 kg dan 50 kg. Mekanisme pegas di antara keduanya memberikan gaya 100 N pada masing-masing modul selama 0,5 s. Hambatan diabaikan; mula-mula diam.",
                    "steps": ["Model: buat dua diagram, satu untuk A di kiri dan satu untuk B di kanan. Massa tiap modul sudah termasuk roda.", "Data: F = 100 N, mA = 20 kg, mB = 50 kg, t = 0,5 s, v₀A = v₀B = 0.", "Diagram: gaya B pada A ke kiri; gaya A pada B ke kanan. Kedua panah sama panjang, tetapi tidak diletakkan pada benda yang sama.", "Persamaan: aA = −F/mA dan aB = +F/mB dengan kanan positif.", "Hitung: aA = −100/20 = −5 m/s²; aB = 100/50 = +2 m/s². Perubahan kecepatan berturut-turut −2,5 dan +1 m/s.", "Makna: A berubah gerak lebih cepat karena massanya lebih kecil, meskipun kedua gaya interaksi sama besar.", "Cek: 20 × 2,5 = 50 × 1 dalam besar perubahan momentum. Tidak ada gaya luar horizontal pada sistem gabungan."],
                    "result": "Gaya sama besar 100 N; percepatan berbeda besar, 5 m/s² pada A dan 2 m/s² pada B, dengan arah berlawanan.",
                },
                "checks": [
                    _choice("n3", "Bumi menarik sebuah buku ke bawah. Pasangan aksi–reaksi gaya ini adalah…", ["Meja menekan buku ke atas.", "Buku menarik Bumi ke arah buku.", "Berat buku menekan meja."], 1, "Balik pemberi dan penerima dari interaksi gravitasi yang sama: Bumi pada buku ↔ buku pada Bumi. Normal meja berasal dari interaksi kontak lain."),
                    _choice("n3", "Dua modul bermassa berbeda saling berinteraksi tanpa hambatan. Kesimpulan yang selalu benar tentang pasangan gaya interaksinya adalah…", ["Benda berat memberi gaya lebih besar.", "Keduanya menerima gaya sama besar, berlawanan arah, pada dua benda berbeda.", "Kedua benda mempunyai percepatan sama."], 1, "Hukum III menyamakan gaya pasangan, sedangkan Hukum II menentukan percepatan tiap massa.", diagram=_lab("reaction", F=36, m1=12, m2=24, t=1), seconds=180),
                ],
            },
            {
                "id": "n4", "title": "Memilih hukum dari mekanisme peristiwa",
                "question": "Bagaimana membedakan contoh yang benar-benar menjelaskan hukum dari contoh yang hanya menyebut nama bendanya?",
                "explain": [
                    "Satu peristiwa dapat dijelaskan dengan lebih dari satu Hukum Newton. Agar penjelasan terarah, tentukan pertanyaan yang sedang dijawab. Jika pertanyaannya mengapa gerak tetap, periksa gaya neto nol dan Hukum I. Jika pertanyaannya mengapa perubahan gerak berbeda, hubungkan gaya neto dan massa melalui Hukum II. Jika pertanyaannya siapa memberi gaya balasan, cari dua benda pada interaksi yang sama melalui Hukum III.",
                    "Mulai dengan kalimat 'benda yang saya tinjau adalah …'. Sesudah itu sebutkan pemberi tiap gaya yang relevan. Jangan menganggap arah gerak sebagai gaya baru. Misalnya, benda bergerak ke kanan sambil ditarik ke kiri dapat melambat; arah gerak menerangkan keadaan awal, sedangkan resultan gaya menerangkan perubahan keadaan itu.",
                    "Sebab dan akibat tidak boleh tertukar. Pernyataan 'kereta mendapat gaya neto karena ia cepat' belum menjelaskan interaksi yang memberi gaya. Penjelasan yang dapat diperiksa berbunyi 'tali menarik lebih kuat daripada hambatan, sehingga ada gaya neto ke kanan; massa tetap membuat percepatan ke kanan'. Untuk memprediksi kecepatan akhirnya, tambahkan data kecepatan awal dan selang waktu.",
                    "Contoh baru yang baik menyebut situasi, benda tinjauan, interaksi, asumsi, serta akibat yang sesuai. Mengganti 'bus' menjadi 'mobil' tanpa mengubah alasan belum menunjukkan pemahaman baru. Sebaliknya, melacak mengapa sampel meluncur tetap di atas bantalan udara, mengapa muatan mengubah percepatan robot, atau mengapa gas dan roket saling menerima gaya menunjukkan mekanisme yang dapat dipindahkan ke konteks lain.",
                ],
                "formula": "Interaksi → ΣF pada benda → a = ΣF/m → perubahan v; pasangan gaya selalu diberi dua nama benda",
                "quantities": ["Benda tinjauan: penerima gaya yang dianalisis", "ΣF (N), m (kg), a (m/s²): hubungan sebab dan akibat perubahan gerak", "v₀ (m/s), t (s): informasi tambahan untuk memprediksi kecepatan"],
                "assumptions": ["Pilih sistem dan arah positif sebelum menyusun alasan.", "Hubungan a = ΣF/m digunakan untuk massa tetap.", "Contoh ideal harus menyatakan hambatan yang diabaikan; contoh nyata harus menyebut gaya hambatan jika penting."],
                "lab": _lab("motion", right=14, left=6, m=4, v0=-3, t=1),
                "explore": ["Prediksi: hukum mana yang menjelaskan mengapa benda bermassa lebih besar mengalami perubahan gerak lebih kecil?", "Ubah hanya gaya kiri sampai sama dengan gaya kanan.", "Amati kapan percepatan nol dan kapan tidak, sambil mempertahankan kecepatan awal ke kiri.", "Tulis dua kalimat sebab–akibat untuk dua keadaan itu; sebutkan gaya neto, massa, dan arah perubahan kecepatan."],
                "misconception": {"claim": "Setiap peristiwa harus diberi tepat satu label hukum, tanpa menjelaskan mekanismenya.", "explain": "Hukum-hukum itu saling melengkapi. Yang dinilai ialah apakah penjelasan menjawab pertanyaan: keadaan gerak bertahan, gerak berubah, atau gaya pada dua benda saling berpasangan."},
                "worked": {
                    "scenario": "Sebuah robot inspeksi bergerak ke kiri 3 m/s. Motor menarik ke kanan 14 N, hambatan pada selang ini ke kanan 6 N, dan massanya 5 kg. Pilih penjelasan sebab–akibat yang sesuai untuk 0,5 s pertama.",
                    "steps": ["Model: tinjau robot saja. Karena robot sedang bergerak ke kiri, hambatan ke kanan masuk akal pada selang sebelum robot berhenti.", "Data: m = 5 kg, v₀ = −3 m/s, dua gaya ke kanan 14 N dan 6 N; t yang ditinjau 0,5 s agar robot belum berbalik.", "Diagram: kedua panah gaya ke kanan, panah kecepatan ke kiri. Panah kecepatan tidak ikut dijumlah sebagai gaya.", "Persamaan: ΣFx = 14 + 6 = +20 N; a = 20/5 = +4 m/s².", "Hitung untuk 0,5 s: Δv = +2 m/s dan v = −3 + 2 = −1 m/s.", "Makna: Hukum II menjelaskan perlambatan gerak kiri. Hukum III dapat dipakai untuk menamai pasangan gaya motor melalui interaksi roda–lantai, tetapi pasangan itu berada di luar diagram robot.", "Cek: dengan model gaya sementara ini robot mencapai nol pada 0,75 s. Sesudah itu arah hambatan harus ditinjau ulang; jangan meneruskan model hambatan tetap ke kanan tanpa batas."],
                    "result": "Penjelasan menyebut gaya neto ke kanan sebagai sebab percepatan ke kanan; robot masih bergerak ke kiri pada t = 0,5 s.",
                },
                "checks": [
                    _choice("n4", "Pilih contoh baru yang paling lengkap untuk menjelaskan Hukum I.", ["Sebuah robot cepat karena punya motor.", "Sampel meluncur lurus pada bantalan udara; hambatan diabaikan dan gaya tegaknya seimbang, sehingga kecepatan yang sudah ada bertahan.", "Dua magnet saling menarik karena semuanya mempunyai berat."], 1, "Contoh kedua menyatakan sistem, gaya neto nol, asumsi, dan keadaan gerak yang bertahan. Itulah mekanisme Hukum I.", seconds=180),
                    _choice("n4", "Seorang siswa menjelaskan: 'Roket dan gas saling memberi gaya sama besar pada dua benda; massa berbeda membuat percepatan berbeda.' Penjelasan ini menghubungkan…", ["Hukum III untuk pasangan gaya dan Hukum II untuk percepatan tiap benda.", "Hukum I saja karena semuanya diam.", "Berat dan normal sebagai pasangan aksi–reaksi."], 0, "Pasangan interaksi dijelaskan oleh Hukum III; hubungan gaya neto dengan percepatan masing-masing benda dijelaskan oleh Hukum II. Analisis roket lengkap memerlukan perhatian pada massa yang berubah.", seconds=180),
                ],
            },
        ],
        "prediction": [
            "Dalam ilustrasi dua papan, massa total kanan dua kali massa kiri. Prediksi hubungan besar gaya dan percepatan keduanya, lalu tulis alasan sebelum mengubah kontrol.",
            "Setelah kedua tokoh tidak bersentuhan lagi, hambatan horizontal diabaikan. Prediksi gerak keduanya dan sebutkan informasi yang masih diperlukan untuk menentukan arah serta kecepatannya.",
        ],
        "performance": {
            "scenario": "Buat panduan satu halaman untuk pengelola pameran gerak. Pilih tiga situasi baru di museum atau rumah: satu untuk gerak yang bertahan, satu untuk perubahan gerak akibat gaya neto dan massa, satu untuk pasangan interaksi dua benda. Gunakan ilustrasi atau simulasi, tanpa melakukan percobaan yang berisiko.",
            "deliverables": ["Tiga ilustrasi dengan benda tinjauan dan nama pemberi tiap gaya; pisahkan panah kecepatan dari panah gaya.", "Satu penjelasan sebab–akibat 3–4 kalimat untuk tiap situasi, memakai istilah gaya neto, massa, dan percepatan dengan tepat.", "Pada contoh Hukum III, dua diagram benda dan penjelasan mengapa gaya pasangan tidak saling meniadakan pada satu benda.", "Satu perubahan variabel pada tiap contoh, prediksi akibatnya, dan satu batas model yang dipakai."],
            "rubric": {"T1": "Menyebut nama hukum atau menggambar situasi, tetapi pemberi gaya, benda tinjauan, atau sebab–akibat belum jelas.", "T2": "Dua contoh mempunyai mekanisme yang benar; masih ada satu kekeliruan penting tentang gaya neto, arah percepatan, atau pasangan dua benda.", "T3": "Ketiga contoh sesuai mekanisme, diagram dan istilah benar; penjelasan membedakan kecepatan dari percepatan serta gaya pasangan dari gaya seimbang, dan menyebut asumsi.", "T4": "Memenuhi T3 serta menjelaskan perubahan satu variabel secara konsisten dan menunjukkan kapan model perlu diperbaiki dalam keadaan nyata."},
        },
    },
    "f-mek-1b": {
        "hook": {
            "title": "Mengapa rak buku membutuhkan penyangga?",
            "scene": "Ilustrasi menampilkan papan rak mendatar yang berengsel pada dinding dan ditahan kabel diagonal di ujungnya. Tumpukan buku bisa digeser mendekati dinding atau ke ujung. Kabel yang tampak lebih landai harus menanggung tegangan lebih besar, walaupun berat buku tidak berubah.",
            "question": "Mana yang lebih memengaruhi tuntutan pada kabel: warna papan, letak buku, atau sudut penyangga? Bagaimana membuktikannya dengan gaya dan momen?",
            "bridge": "Tentukan poros, bedakan jarak sepanjang batang dari lengan momen, lalu gunakan keseimbangan gaya dan momen untuk menilai rancangan. Model ini menjelaskan mekanisme; kekuatan bahan tetap perlu diperiksa.",
            "lab": _lab("cable", W=120, theta=30, fraction=0.6, L=1.2),
        },
        "goals": [
            "Memilah informasi yang mengubah gaya, lengan momen, atau kemampuan bahan menahan gaya, dan menjelaskan alasan pemilihannya.",
            "Memeriksa kedua syarat kesetimbangan benda tegar, ΣF = 0 dan Στ = 0, dengan tanda yang konsisten.",
            "Menguraikan gaya kabel miring untuk menentukan tegangan dan reaksi engsel pada rak ideal.",
            "Membandingkan letak beban dan sudut diagonal untuk memilih struktur yang memenuhi batas gaya pada model yang dinyatakan.",
        ],
        "concepts": [
            {
                "id": "s1", "title": "Faktor relevan: gaya, letak, arah, dan batas bahan",
                "question": "Berat buku sama. Mengapa kabel rak bekerja lebih berat ketika buku digeser menjauhi dinding?",
                "explain": [
                    "Struktur menerima gaya dari beban, penyangga, dan tumpuan. Analisis dimulai dengan memilih benda yang ditinjau, menggambar semua gaya luar, lalu menentukan poros acuan. Informasi relevan adalah informasi yang mengubah besar atau arah gaya, jarak garis kerjanya dari poros, atau kemampuan komponen menahan gaya. Warna cat semata tidak mengubah model tersebut; luas penampang dan jenis bahan dapat mengubah batas kekuatannya.",
                    "Momen gaya, atau torsi, mengukur kecenderungan gaya mengubah gerak rotasi terhadap poros. Besarnya |τ| = Fd, dengan d jarak tegak lurus poros ke garis kerja gaya. Jika titik tangkap terletak sejauh r pada batang mendatar dan gaya membentuk sudut θ dari arah batang ke kanan, τ = rF sin θ. Nilai r bukan selalu lengan momen; hanya pada gaya tegak lurus batang keduanya sama.",
                    "Pilih momen berlawanan jarum jam positif. Gaya ke bawah pada bagian kanan poros memberi momen negatif. Gaya ke atas di tempat yang sama memberi momen positif. Gaya sejajar batang, termasuk gaya besar sekalipun, tidak memberi momen terhadap engsel bila garis kerjanya melalui engsel. Sudut bertanda membantu membaca pembalikan arah tanpa menghilangkan informasi.",
                    "Untuk rak mendatar dengan beban vertikal, memindahkan beban menjauhi engsel memperbesar momen beban karena d bertambah. Menilai apakah rak aman memerlukan langkah lain: bandingkan gaya yang dibutuhkan dengan batas kabel, sambungan, dan bahan. Kesetimbangan ideal menerangkan gaya yang harus tersedia; persamaan itu sendiri belum menjamin komponen nyata tidak patah, melengkung, atau kehilangan kestabilan.",
                ],
                "formula": "τ = rF sin θ; |τ| = Fd; d = r|sin θ|; berlawanan jarum jam (+)",
                "quantities": ["τ: momen gaya terhadap poros (N·m)", "F: besar gaya (N)", "r: jarak poros ke titik tangkap sepanjang batang (m)", "d: jarak tegak lurus poros ke garis kerja gaya (m)", "θ: sudut bertanda gaya dari batang ke kanan (°)"],
                "assumptions": ["Batang dianggap tegar dan terletak mendatar ke kanan dari poros.", "Poros ideal dipilih di engsel; r ≥ 0.", "Tanda sudut −180° sampai 180°; pada θ = 0° atau ±180°, momen nol."],
                "lab": _lab("torque", F=80, r=0.6, theta=-90),
                "explore": ["Prediksi: jika beban digeser dua kali lebih jauh dari engsel dengan gaya dan arah sama, apa yang terjadi pada momen?", "Ubah hanya r, lalu kembalikan dan ubah hanya θ dari −90° ke −30° dan 0°.", "Amati panjang lengan tegak lurus serta tanda dan besar momen. Uji juga θ = 90° dan 180°.", "Jelaskan mengapa jarak titik tangkap yang panjang belum tentu memberi momen besar ketika garis kerja hampir melewati poros."],
                "misconception": {"claim": "Momen selalu F dikali panjang batang, berapa pun arah gayanya.", "explain": "Yang mengalikan F adalah jarak tegak lurus ke garis kerja. Pada gaya miring, komponen sejajar batang tidak memutar terhadap engsel, sehingga faktor sin θ diperlukan."},
                "worked": {
                    "scenario": "Beban 80 N bekerja ke bawah pada rak, 0,60 m dari engsel kiri. Rak dicat ulang tanpa mengubah bahan atau bentuk, lalu beban dipindah ke 0,30 m. Perubahan mana yang mengurangi momen beban?",
                    "steps": ["Model: rak mendatar, engsel sebagai poros, beban vertikal; abaikan perubahan cat terhadap massa dan kekuatan.", "Data: W = 80 N; xawal = 0,60 m; xakhir = 0,30 m; sudut gaya −90°.", "Diagram: engsel di kiri, panah W ke bawah; garis kerja vertikal berjarak mendatar x dari engsel.", "Persamaan: τ = xW sin(−90°) = −Wx.", "Hitung: τawal = −80 × 0,60 = −48 N·m; τakhir = −80 × 0,30 = −24 N·m.", "Makna: memindahkan beban ke dekat engsel mengurangi besar momen separuh; cat yang hanya berubah warna tidak mengubah F atau d.", "Cek: arah putar tetap searah jarum jam. Batas kekuatan bahan harus diperiksa terpisah; perubahan warna bukan bukti penguatan."],
                    "result": "Perpindahan beban mengubah besar momen dari 48 menjadi 24 N·m; warna saja tidak mengubah model gaya dan momen.",
                },
                "checks": [
                    _num("s1", "Gaya 50 N bekerja pada r = 0,40 m dari engsel rak dengan θ = −30° dari batang mendatar. sin(−30°) = −0,5. Berapa momen bertandanya?", "Momen terhadap engsel", -10, "N·m", "τ = rF sin θ = 0,40 × 50 × (−0,5) = −10 N·m. Tanda negatif menyatakan searah jarum jam.", diagram=_lab("torque", F=50, r=0.4, theta=-30)),
                    _choice("s1", "Dua rak mempunyai bentuk dan beban sama. Informasi tambahan mana yang langsung diperlukan untuk membandingkan kemungkinan kabel putus?", ["Warna label kabel.", "Batas tegangan yang dapat ditahan kabel dan tegangan yang dibutuhkan.", "Nama ruangan tanpa data fisik lain."], 1, "Persamaan memberi gaya yang dibutuhkan, lalu gaya itu harus dibandingkan dengan batas bahan/sambungan. Identitas dekoratif tidak cukup.", level="C4", seconds=180),
                ],
            },
            {
                "id": "s2", "title": "Dua pemeriksaan: tidak bergeser dan tidak berputar",
                "question": "Bisakah dua gaya berlawanan yang jumlahnya nol tetap membuat batang berputar?",
                "explain": [
                    "Kesetimbangan statis berarti benda mula-mula diam dan tetap diam terhadap kerangka yang dipilih. Untuk benda tegar dalam bidang, diperlukan ΣFx = 0, ΣFy = 0, dan Στ = 0. Jumlah gaya nol mencegah percepatan translasi pusat massa; jumlah momen nol mencegah percepatan rotasi. Keduanya memeriksa akibat yang berbeda.",
                    "Dua gaya sejajar yang sama besar, berlawanan arah, dan memiliki garis kerja berbeda membentuk pasangan gaya atau kopel. Jumlah gayanya nol, tetapi momennya tidak nol. Jika jarak tegak lurus kedua garis kerja d, besar momen pasangan adalah Fd. Untuk pasangan murni, hasil ini sama terhadap poros mana pun karena resultan gayanya nol.",
                    "Sebaliknya, jumlah momen nol terhadap satu titik saja belum membuktikan jumlah gaya nol. Satu gaya yang garis kerjanya melalui poros mempunyai momen nol terhadap poros tersebut, tetapi tetap dapat menggerakkan benda bebas secara translasi. Karena itu gambar yang kelihatan tidak berputar belum menyelesaikan pemeriksaan seluruh keseimbangan.",
                    "Memilih poros di engsel memudahkan perhitungan karena gaya reaksi engsel bekerja melalui poros dan momennya nol. Reaksi itu tetap masuk penjumlahan gaya. Setelah memperoleh gaya penyangga dari persamaan momen, kembali ke ΣFx dan ΣFy untuk menentukan atau memeriksa reaksi engsel. Jangan membuang gaya hanya karena momennya nol terhadap poros pilihan.",
                ],
                "formula": "ΣFx = 0; ΣFy = 0; Στ = 0; besar momen pasangan gaya = Fd",
                "quantities": ["ΣFx, ΣFy: jumlah komponen gaya pada satu benda (N)", "Στ: jumlah aljabar momen terhadap poros yang sama (N·m)", "d pada kopel: jarak tegak lurus antara dua garis kerja gaya (m)", "F: besar salah satu gaya pasangan (N)"],
                "assumptions": ["Benda tegar dua dimensi, mula-mula diam untuk pembahasan statis.", "Semua momen dijumlah terhadap poros yang sama.", "Lab kopel menampilkan dua gaya sama besar berlawanan pada garis kerja yang terpisah."],
                "lab": _lab("couple", F=20, d=0.5),
                "explore": ["Prediksi: ketika dua panah gaya sama panjang dan berlawanan, apakah batang pasti setimbang?", "Ubah hanya jarak tegak lurus d antara garis kerja menjadi setengah lalu mendekati nol.", "Amati resultan gaya tetap nol sementara besar momen berubah sebanding d.", "Jelaskan mengapa kalimat 'kedua gaya sudah seimbang' belum cukup untuk menyatakan kesetimbangan benda tegar."],
                "misconception": {"claim": "Jika ΣF = 0, semua bagian benda pasti diam dan struktur pasti setimbang.", "explain": "Resultan gaya nol hanya memeriksa translasi. Dua gaya berlawanan pada garis kerja berbeda dapat memberi momen total yang memutar benda; Στ juga harus nol."},
                "worked": {
                    "scenario": "Pada batang bebas, dua gaya horizontal 30 N bekerja berlawanan pada garis sejajar yang berjarak tegak lurus 0,40 m. Pasangan itu cenderung memutar searah jarum jam. Apakah batang mula-mula diam akan tetap setimbang?",
                    "steps": ["Model: batang tegar bebas; tidak ada momen penahan lain. Berlawanan jarum jam positif.", "Data: kedua gaya 30 N, arahnya berlawanan, jarak antara garis kerja d = 0,40 m.", "Diagram: letakkan satu gaya pada garis atas dan satu pada garis bawah sehingga keduanya memutar searah jarum jam.", "Persamaan gaya: ΣFx = 30 − 30 = 0. Persamaan momen pasangan: Στ = −Fd.", "Hitung: Στ = −30 × 0,40 = −12 N·m.", "Makna: pusat massa tidak mendapat percepatan translasi akibat pasangan ini, tetapi batang mendapat kecenderungan percepatan rotasi searah jarum jam.", "Cek: jika d dijadikan nol, kedua gaya segaris dan momen pasangan menjadi nol. Pada d = 0,40 m, syarat momen belum terpenuhi."],
                    "result": "Batang tidak setimbang statis: ΣF = 0 tetapi Στ = −12 N·m.",
                },
                "checks": [
                    _choice("s2", "Dua gaya sejajar berlawanan masing-masing 25 N mempunyai garis kerja terpisah 0,20 m. Tidak ada gaya atau momen lain. Kesimpulan yang tepat adalah…", ["Setimbang karena jumlah gaya nol.", "Jumlah gaya nol, tetapi ada momen pasangan sebesar 5 N·m.", "Jumlah gaya 50 N dan momen nol."], 1, "Jumlah vektor gayanya nol; besar momen pasangan Fd = 25 × 0,20 = 5 N·m. Kedua syarat kesetimbangan harus diperiksa.", level="C4", seconds=240, diagram=_lab("couple", F=25, d=0.2)),
                    _choice("s2", "Gaya engsel tidak muncul dalam Στ terhadap engsel. Apa alasan yang tepat?", ["Gaya engsel selalu nol.", "Lengan momennya nol terhadap engsel, tetapi komponennya tetap masuk ΣF.", "Semua gaya tumpuan boleh dihapus dari diagram."], 1, "Momen nol tidak sama dengan gaya nol. Garis kerja reaksi melalui poros sehingga d = 0.", level="C4", seconds=180),
                ],
            },
            {
                "id": "s3", "title": "Kabel miring: pisahkan komponen dan momen",
                "question": "Mengapa gaya kabel tidak selalu sama dengan berat buku, dan ke mana komponen mendatarnya pergi?",
                "explain": [
                    "Tinjau rak mendatar panjang L dengan engsel di kiri. Kabel di ujung kanan menarik ke atas menuju dinding dan membentuk sudut θ terhadap batang. Jika T adalah besar tegangan, komponen mendatarnya ke kiri sebesar T cos θ dan komponen tegaknya ke atas sebesar T sin θ. Sudut acuan harus disebutkan: karena diukur dari mendatar, komponen tegak memakai sinus.",
                    "Beban W ditempatkan pada x = fL dari engsel, dengan f fraksi panjang rak. Ambil momen terhadap engsel. Komponen mendatar kabel segaris batang sehingga tidak memberi momen. Komponen tegaknya bekerja dengan lengan L, sedangkan berat bekerja dengan lengan x. Kesetimbangan momen memberi (T sin θ)L − Wx = 0, sehingga T = Wf/sin θ pada model rak tanpa berat sendiri.",
                    "Setelah T ditemukan, keseimbangan gaya memberi reaksi engsel. Dengan kanan dan atas positif, Rx = T cos θ dan Ry = W − T sin θ. Engsel menahan tarikan mendatar kabel dan juga bagian beban vertikal yang tidak ditopang komponen kabel. Karena itu menyamakan T sin θ dengan W hanya benar pada model khusus ketika beban berada di ujung, f = 1, dan tidak ada beban lain.",
                    "Ketika kabel semakin landai, sin θ mengecil sehingga T yang dibutuhkan bertambah untuk menyediakan momen sama. Pada θ = 0°, kabel segaris rak tidak dapat menahan momen beban yang berada di luar engsel; membagi dengan nol bukan jawaban fisik. Model ini juga perlu diperluas bila rak mempunyai berat sendiri, beberapa beban, kabel melendut, atau engsel nyata dapat menahan momen.",
                ],
                "formula": "T sin θ · L = WfL; T = Wf/sin θ; Rx = T cos θ; Ry = W − T sin θ",
                "quantities": ["T: tegangan kabel (N)", "W: berat seluruh beban titik (N), W = mg dengan g = 10 m/s²", "L: panjang rak dari engsel ke sambungan kabel (m)", "f: fraksi letak beban, x/L (tanpa satuan)", "Rx, Ry: komponen reaksi engsel pada rak (N)", "θ: sudut lancip kabel terhadap rak mendatar (°)"],
                "assumptions": ["Rak tegar tanpa berat sendiri; satu beban titik dengan 0 ≤ f ≤ 1.", "Engsel ideal memberi gaya, tidak memberi momen penahan.", "Kabel lurus tanpa massa hanya menarik, terpasang di ujung; 0° < θ ≤ 90°.", "Untuk keadaan nyata, berat rak dan batas bahan harus ditambahkan bila signifikan."],
                "lab": _lab("cable", W=160, theta=53.130102, fraction=0.75, L=2),
                "explore": ["Prediksi: pada W tetap, apakah memindahkan beban dari f = 1 ke f = 0,5 membuat seluruh berat hilang atau hanya membagi peran kabel dan engsel?", "Ubah hanya fraksi letak beban, lalu kembalikan dan ubah hanya sudut kabel.", "Amati T, komponen tegak kabel, dan reaksi engsel; cocokkan momen gaya terhadap engsel.", "Jelaskan mengapa panjang L saling menghilangkan ketika f tetap, tetapi tidak bila jarak x dijaga tetap sementara L berubah."],
                "misconception": {"claim": "Seluruh tegangan kabel miring menahan berat, sehingga T selalu sama dengan W.", "explain": "Hanya komponen tegak memberi momen penahan pada rak mendatar. Engsel juga dapat menahan beban vertikal; posisi beban menentukan T sin θ = Wf, bukan selalu W."},
                "worked": {
                    "scenario": "Rak ideal panjang 2,0 m menahan beban 160 N pada jarak 1,5 m dari engsel. Kabel di ujung membentuk sudut dengan sin θ = 0,80 dan cos θ = 0,60. Tentukan gaya kabel dan peran engsel.",
                    "steps": ["Model: rak tanpa berat sendiri, engsel ideal, satu kabel ke atas-kiri. Pilih poros di engsel, kanan/atas dan putaran berlawanan jarum jam positif.", "Data: L = 2,0 m, x = 1,5 m, f = 0,75, W = 160 N, sin θ = 0,80, cos θ = 0,60.", "Diagram: W ke bawah di x = 1,5 m; di ujung ada Tx ke kiri dan Ty ke atas; di engsel ada Rx ke kanan dan Ry ke atas.", "Persamaan momen: (T × 0,80)(2,0) − (160)(1,5) = 0, sehingga T = 240/1,60 = 150 N.", "Persamaan gaya: Rx = 150 × 0,60 = 90 N; Ry = 160 − 150 × 0,80 = 40 N.", "Makna: kabel memberi 120 N ke atas dan engsel memberi 40 N ke atas; engsel juga menyeimbangkan tarikan mendatar 90 N.", "Cek: ΣFy = 120 + 40 − 160 = 0 dan Στ = 120 × 2 − 160 × 1,5 = 0; √(90² + 120²) = 150 N sesuai besar tegangan."],
                    "result": "T = 150 N, Rx = 90 N ke kanan, Ry = 40 N ke atas; semua syarat kesetimbangan model terpenuhi.",
                },
                "checks": [
                    _num("s3", "Rak ideal tanpa berat menahan W = 180 N pada f = 0,50. Kabel ujung membentuk θ = 30° terhadap mendatar (sin 30° = 0,5). Berapa tegangan kabel?", "Tegangan kabel", 180, "N", "Dari momen terhadap engsel: T sin θ = Wf = 90 N; T = 90/0,5 = 180 N. Jangan memakai T sin θ = 180 N karena beban tidak di ujung.", seconds=240, level="C4", diagram=_lab("cable", W=180, theta=30, fraction=0.5, L=1.4)),
                    _num("s3", "Rak ideal mempunyai beban W = 200 N pada f = 0,40. Kabel di ujung menyediakan komponen tegak 80 N. Berapa komponen vertikal reaksi engsel pada rak (atas positif)?", "Reaksi vertikal engsel", 120, "N", "ΣFy = Ry + 80 − 200 = 0, maka Ry = +120 N. Gaya kabel dan engsel bersama-sama menyeimbangkan berat.", seconds=180),
                ],
            },
            {
                "id": "s4", "title": "Penyangga diagonal: keputusan harus menyebut mekanisme",
                "question": "Bagaimana memilih sudut penyangga yang memenuhi batas gaya tanpa hanya berkata 'lebih kokoh'?",
                "explain": [
                    "Pada rak berengsel, beban di kanan engsel memberi momen searah jarum jam. Kabel yang ditarik ke arah dinding atas memberi komponen ke atas pada ujung rak, sehingga menyediakan momen lawan. Batang diagonal dari dinding bawah juga dapat menahan melalui gaya tekan ke atas pada rak; arah gaya sepanjang batang dan jenis sambungannya harus digambar. Kabel hanya dapat menarik, sedangkan batang perlu diperiksa terhadap tekuk ketika menahan tekan.",
                    "Diagonal tidak membuat beban menghilang. Ia mengalihkan sebagian gaya dan momen menuju dinding dan sambungan. Untuk model kabel atas, kebutuhan komponen tegak adalah Ty = Wf. Sudut yang lebih besar terhadap rak memberi komponen tegak lebih besar untuk T yang sama, sehingga T yang diperlukan lebih kecil. Sudut juga mengubah tarikan mendatar dan reaksi engsel, jadi kedua persamaan gaya tetap diperiksa.",
                    "Keputusan desain menghubungkan hasil model dengan batas komponen. Jika tegangan yang dihitung melebihi batas yang diizinkan, rancangan tidak memenuhi kriteria model. Pilihan yang dapat diuji antara lain memperbesar sudut kabel, menggeser beban mendekati engsel, mengurangi beban, atau mengganti komponen dengan batas gaya lebih tinggi. Jelaskan variabel mana yang berubah dan mengapa kebutuhan gaya berkurang.",
                    "Jika T masih di bawah batas kabel, kesimpulan yang tepat adalah 'memenuhi batas kabel pada model ini'. Untuk menilai struktur nyata, data kekuatan engsel, baut, dinding, penampang rak, dan faktor keselamatan juga diperlukan. Persamaan kesetimbangan bukan pengganti data bahan. Analisis yang baik menyatakan bagian yang sudah diperiksa dan data yang masih belum tersedia.",
                ],
                "formula": "Ty = Wf; T = Wf/sin θ; kriteria model kabel: T ≤ Tizin; Rx = T cos θ",
                "quantities": ["Tizin: batas tegangan yang diizinkan pada kabel/sambungan dalam soal (N)", "Wf: komponen tegak kabel yang diperlukan oleh keseimbangan momen (N)", "θ: sudut diagonal terhadap batang mendatar (°)", "Rx: reaksi mendatar yang juga harus dapat diterima sambungan (N)"],
                "assumptions": ["Perbandingan interaktif memakai kabel di atas rak, bukan batang tekan di bawah.", "Batas Tizin yang diberikan sudah merupakan batas kerja yang dipakai dalam soal.", "Model tanpa berat rak, satu beban titik dan engsel ideal; keputusan tentang struktur nyata memerlukan data tambahan."],
                "lab": _lab("cable", W=120, theta=30, fraction=0.5, L=1.2),
                "explore": ["Prediksi: kabel berkapasitas 100 N, beban 120 N pada f = 0,5; apakah sudut 30° memenuhi batas?", "Ubah hanya sudut dari 30° ke 60° dengan beban dan letaknya tetap.", "Amati tegangan yang diperlukan dan reaksi engsel. Bandingkan tegangan terhadap batas 100 N, bukan hanya bentuk segitiganya.", "Jelaskan keputusan memakai momen penahan dan komponen tegak; sebutkan satu komponen nyata yang belum dinilai kekuatannya."],
                "misconception": {"claim": "Menambah diagonal selalu membuat struktur aman, apa pun sudut dan bahannya.", "explain": "Diagonal harus menyediakan komponen yang cukup untuk menahan momen beban. Sudut terlalu landai menuntut gaya besar, dan bahan atau sambungan tetap dapat melampaui batasnya."},
                "worked": {
                    "scenario": "Rak ideal menahan 120 N pada setengah panjangnya. Pilihan kabel A bersudut 30° dan B bersudut 60° dari rak. Kedua kabel mempunyai batas kerja 100 N. Pilih yang memenuhi batas kabel; sin 30° = 0,5 dan sin 60° ≈ 0,866.",
                    "steps": ["Model: rak tanpa berat, kabel di ujung, engsel tidak menahan momen. Batas yang dinilai hanya tegangan kabel.", "Data: W = 120 N, f = 0,50, Tizin = 100 N; θA = 30° dan θB = 60°.", "Diagram: kedua rancangan memerlukan momen penahan sama, sehingga Ty = Wf = 60 N pada ujung rak.", "Persamaan: T = Ty/sin θ. Maka TA = 60/0,5 dan TB = 60/0,866.", "Hitung: TA = 120 N, TB ≈ 69,3 N.", "Makna keputusan: A melebihi batas 100 N; B memenuhi batas kabel model. Gaya lebih kecil pada B terjadi karena komponen tegak per satu newton tegangan lebih besar.", "Cek dan batas: Ty pada keduanya tetap 60 N dan Ry = 60 N. Kapasitas engsel, baut, dinding, serta lendutan rak belum diberikan sehingga keselamatan struktur nyata belum dapat disimpulkan."],
                    "result": "Pilih B untuk memenuhi batas kabel pada model ini: 69,3 N ≤ 100 N. Rancangan A memerlukan 120 N dan tidak memenuhi batas.",
                },
                "checks": [
                    _choice("s4", "Rak ideal memiliki beban dan fraksi letak beban tetap. Kabel 30° memerlukan 140 N, sedangkan batasnya 120 N. Perubahan mana pasti mengurangi tegangan yang diperlukan pada model?", ["Mengecat rak lebih gelap.", "Memperbesar sudut kabel menjadi 60° terhadap rak.", "Menggeser beban lebih jauh dari engsel."], 1, "T = Wf/sin θ. Memperbesar sudut dari 30° ke 60° memperbesar sinus dan menurunkan T. Memindahkan beban menjauh justru memperbesar f.", level="C4", seconds=240),
                    _choice("s4", "Tegangan kabel hasil hitungan lebih kecil daripada batasnya. Kesimpulan yang paling dapat dipertanggungjawabkan adalah…", ["Semua bagian rak pasti aman untuk selamanya.", "Batas kabel terpenuhi dalam model; kapasitas engsel, dinding, dan rak perlu data tersendiri.", "Persamaan gaya tidak perlu diperiksa lagi."], 1, "Kesetimbangan dan batas satu komponen belum memeriksa semua cara struktur bisa gagal. Kesimpulan harus sesuai data yang tersedia.", level="C4", seconds=180),
                ],
            },
        ],
        "prediction": [
            "Beban pada ilustrasi digeser dari setengah panjang ke ujung rak, tanpa mengubah berat atau sudut kabel. Prediksi tegangan kabel dan jelaskan lewat momen terhadap engsel.",
            "Dua gaya pada batang sama besar dan berlawanan arah tetapi garis kerjanya terpisah. Prediksi apakah batang yang mula-mula diam tetap diam; tulis syarat keseimbangan yang perlu diperiksa.",
        ],
        "performance": {
            "scenario": "Analisis dua rancangan rak pajangan ideal, panjang 1,5 m dan berat rak diabaikan. Keduanya berengsel di kiri dan kabel berada di ujung kanan. Beban 180 N terletak 0,90 m dari engsel. Rancangan A memakai kabel 30°, B memakai 60°. Batas kerja kabel 160 N; batas kerja resultan gaya engsel 180 N. Gunakan sin 30° = 0,5, cos 30° ≈ 0,866, sin 60° ≈ 0,866, cos 60° = 0,5. Rekomendasikan rancangan menurut dua batas model itu.",
            "deliverables": ["Diagram benda untuk kedua rancangan: poros, sumbu, sudut acuan, W, T serta dua komponen reaksi engsel.", "Tabel faktor relevan beserta alasannya; bedakan kebutuhan gaya dari batas kekuatan komponen.", "Perhitungan momen, tegangan, Rx, Ry dan besar reaksi engsel √(Rx² + Ry²) untuk tiap rancangan, disertai cek ΣF dan Στ.", "Keputusan terhadap dua batas kerja dan satu perubahan yang dapat memperbaiki rancangan yang gagal, dengan alasan mekanisme.", "Pernyataan keterbatasan: jenis sambungan, berat rak, lendutan, dan kekuatan dinding yang belum diberikan."],
            "rubric": {"T1": "Menyebut lebih kokoh atau memilih rancangan tanpa diagram dan hubungan gaya–momen yang dapat diperiksa.", "T2": "Menentukan momen atau komponen dengan sebagian benar, tetapi belum memakai kedua syarat keseimbangan atau belum membandingkan kedua batas komponen.", "T3": "Diagram, tanda dan satuan konsisten; kedua syarat keseimbangan dipakai; tegangan serta reaksi engsel dibandingkan dengan batas; keputusan dijelaskan lewat komponen dan momen serta sesuai batas model.", "T4": "Memenuhi T3 serta membandingkan perubahan satu variabel secara kuantitatif, memeriksa kewajaran batas sudut/letak beban, dan membedakan hasil model dari data struktur nyata yang belum tersedia."},
        },
    },
}


def _newton(stage, k):
    """C2 menjadi sasaran utama; hitungan pendek dipakai untuk bekal/model."""
    a = 2 + k
    if stage == "P2":
        return [
            _num("n1", f"Pada kereta, gaya {12 + 2*k} N ke kanan dan {7 + 2*k} N ke kiri. Kanan positif. Berapa resultan gaya horizontal?", "Resultan gaya", 5, "N", "Jumlahkan dengan tanda arah: gaya kanan dikurangi gaya kiri, sehingga +5 N."),
            _num("n2", f"Gaya neto {4*a} N bekerja pada benda bermassa {a} kg. Berapa besar percepatannya?", "Percepatan", 4, "m/s²", f"a = ΣF/m = {4*a}/{a} = 4 m/s²."),
            _choice("n1", "Benda bergerak lurus dengan kecepatan tetap. Pernyataan tentang percepatannya adalah…", ["Nol.", "Sama dengan kecepatannya.", "Selalu ke arah gerak."], 0, "Tidak ada perubahan besar maupun arah kecepatan, sehingga percepatan nol."),
            _choice("n3", "Pasangan aksi–reaksi harus bekerja pada…", ["Satu benda yang sama.", "Dua benda berbeda dari satu interaksi.", "Satu benda pada waktu berbeda."], 1, "Tulis gaya A pada B dan gaya B pada A. Pasangan hadir bersamaan pada dua penerima."),
            _choice("n2", "Satuan newton setara dengan…", ["kg·m/s", "kg·m/s²", "m/s²"], 1, "Dari F = ma, satuan gaya adalah kg dikali m/s²."),
            _choice("n2", "Kecepatan benda ke kanan menjadi lebih kecil dari sebelumnya. Arah percepatan pada gerak lurus itu adalah…", ["Ke kanan.", "Ke kiri.", "Tidak dapat mempunyai percepatan."], 1, "Perubahan kecepatan berarah kiri ketika kecepatan kanan berkurang.", seconds=180),
            _choice("n4", "Bola sudah lepas dari tangan dan masih bergerak di udara; hambatan udara diabaikan. Gaya yang tetap bekerja pada bola adalah…", ["Dorongan tangan yang tersimpan.", "Berat dari interaksi gravitasi dengan Bumi.", "Gaya kecepatan ke depan."], 1, "Tangan yang sudah tidak bersentuhan tidak lagi memberi gaya kontak. Gerak bukan pemberi gaya."),
            _num("n2", f"Kecepatan berubah dari {a} m/s ke kanan menjadi {a + 6} m/s ke kanan dalam 3 s. Berapa percepatan rata-ratanya?", "Percepatan rata-rata", 2, "m/s²", "a = Δv/Δt = 6/3 = 2 m/s²."),
        ]
    if stage == "P5":
        return [
            _choice("n1", f"Kereta data bergerak lurus {a} m/s. Selama pengamatan gaya tarik dan hambatan sama besar. Mengapa kecepatannya tetap?", ["Tidak ada satu pun gaya pada kereta.", "Gaya neto nol sehingga tidak ada percepatan.", "Kecepatannya menghasilkan gaya penyeimbang."], 1, "Gaya-gaya boleh ada, tetapi jumlah vektornya nol; keadaan gerak bertahan.", diagram=_lab("motion", right=10+2*k, left=10+2*k, m=4, v0=a, t=2)),
            _choice("n2", "Pada dua kereta dengan gaya neto sama, massa B tiga kali massa A. Penjelasan hubungan percepatan yang tepat adalah…", ["Percepatan B sepertiga A karena massanya tiga kali.", "Percepatan B tiga kali A karena lebih berat.", "Percepatan keduanya sama karena gaya sama."], 0, "a = ΣF/m; massa yang lebih besar memperkecil perubahan kecepatan untuk gaya neto sama.", seconds=180),
            _choice("n3", "Dua papan saling menekan, massa totalnya berbeda. Mengapa kedua gaya kontak tidak saling menghapus pada satu papan?", ["Karena gaya pada papan berat lebih besar.", "Karena gaya pasangan bekerja pada penerima yang berbeda.", "Karena reaksi selalu terlambat."], 1, "Gaya A pada B masuk diagram B; gaya B pada A masuk diagram A. Kedua gaya sama besar dan bersamaan.", seconds=180, diagram=_lab("reaction", F=40+4*k, m1=20, m2=40, t=1)),
            _choice("n4", "Pilih penjelasan sebab–akibat yang benar untuk benda yang sedang ke kanan tetapi melambat.", ["Kecepatan kecil menyebabkan gaya ke kiri.", "Gaya neto ke kiri memberi percepatan ke kiri sehingga kecepatan kanan berkurang.", "Massa bekerja sebagai gaya ke kiri."], 1, "Urutannya interaksi → gaya neto → percepatan → perubahan kecepatan. Massa bukan gaya.", seconds=180),
            _choice("n3", "Buku diam di meja. Mengapa berat dan normal bukan pasangan aksi–reaksi?", ["Karena besarnya tidak boleh sama.", "Karena keduanya bekerja pada buku, berasal dari dua interaksi berbeda.", "Karena Hukum III tidak berlaku saat benda diam."], 1, "Pasangan berat ialah buku menarik Bumi; pasangan normal ialah buku menekan meja. Hukum III juga berlaku ketika benda diam.", seconds=180),
        ]
    if stage == "P7":
        return [
            _choice("n1", "Keping bergerak lurus di bantalan udara ideal setelah pendorong terlepas. Mengapa keping tetap melaju?", ["Dorongan tersimpan di dalam keping.", "Tidak ada gaya neto horizontal yang mengubah kecepatannya.", "Massa keping berubah menjadi gaya."], 1, "Keping mempertahankan kecepatan karena gaya neto horizontal nol, bukan karena menyimpan gaya dorong."),
            _choice("n1", f"Troli bergerak tetap {a} m/s meski ditarik tali. Apakah kalimat 'gaya tarik tidak ada karena a = 0' benar?", ["Benar; semua gaya nol.", "Tidak; gaya tarik dapat diimbangi hambatan.", "Benar; gerak selalu menghapus gaya."], 1, "a = 0 menuntut jumlah gaya nol, bukan menuntut tiap gaya nol.", seconds=180),
            _choice("n2", "Pada massa tetap, gaya neto diperbesar dua kali. Hubungan sebab–akibatnya adalah…", ["Percepatan menjadi dua kali.", "Kecepatan langsung menjadi dua kali pada saat yang sama.", "Massa menjadi setengah."], 0, "Hukum II menghubungkan gaya neto dan percepatan. Kecepatan juga bergantung kecepatan awal serta lama gaya bekerja."),
            _choice("n2", f"Robot A bermassa {3*a} kg, robot B {6*a} kg. Keduanya mendapat gaya neto sama. Penjelasan yang sesuai adalah…", ["B mengalami percepatan dua kali A.", "B mengalami percepatan separuh A karena massa dua kali.", "Kedua robot wajib mempunyai kelajuan sama."], 1, "Massa dua kali berarti a setengah untuk gaya neto sama.", seconds=180),
            _choice("n2", "Kereta bergerak ke kanan tetapi gaya netonya ke kiri. Pernyataan yang tepat pada awal perlambatan adalah…", ["Arah percepatan kiri walaupun arah kecepatan masih kanan.", "Tidak ada percepatan sebelum kereta berbalik.", "Harus ada gaya tambahan kanan karena kereta masih ke kanan."], 0, "Arah percepatan ditetapkan gaya neto. Arah kecepatan tidak otomatis sama dengan arah percepatan.", seconds=180),
            _choice("n3", "Sebuah magnet A menarik magnet B. Pasangan gaya itu ialah…", ["Berat magnet A.", "Magnet B menarik magnet A.", "Normal meja pada magnet B."], 1, "Balik pemberi dan penerima dari interaksi magnetik yang sama."),
            _choice("n3", "Dua modul beroda bermassa berbeda didorong pegas di antaranya. Mengapa modul ringan berpercepatan lebih besar?", ["Pegas memberi gaya lebih besar pada modul ringan.", "Gaya interaksi sama besar, tetapi a = F/m lebih besar untuk massa kecil.", "Modul berat tidak menerima reaksi."], 1, "Hukum III menjamin gaya pasangan sama besar; Hukum II membedakan percepatan tiap massa.", seconds=180, diagram=_lab("reaction", F=30+6*k, m1=10, m2=30, t=1)),
            _choice("n3", "Meja menekan buku ke atas. Gaya reaksinya adalah…", ["Buku menekan meja ke bawah.", "Bumi menarik buku ke bawah.", "Udara menekan semua sisi buku."], 0, "Gaya kontak meja pada buku berpasangan dengan gaya kontak buku pada meja. Berat merupakan interaksi buku–Bumi."),
            _choice("n4", "Pilih contoh yang paling tepat menerangkan peran massa menurut Hukum II.", ["Dua kereta bermassa berbeda menerima gaya neto sama; kereta lebih berat berubah kecepatan lebih lambat.", "Dua benda saling menarik, maka benda berat selalu memberi gaya lebih besar.", "Benda tetap bergerak karena membawa gaya awal."], 0, "Perbandingan mengendalikan gaya neto dan menunjukkan peran massa terhadap percepatan.", seconds=180),
            _choice("n4", "Siswa hanya tahu sebuah troli menerima gaya neto 20 N. Mengapa ia belum dapat menyimpulkan kelajuan akhir troli?", ["Karena gaya neto tidak berhubungan dengan gerak.", "Karena perlu massa untuk a, serta kecepatan awal dan selang waktu untuk v akhir.", "Karena kelajuan selalu sama dengan gaya neto."], 1, "Gaya neto menentukan percepatan bersama massa; prediksi v akhir memerlukan v₀ dan t.", seconds=180),
        ]
    if stage == "P9":
        return [
            _choice("n1", f"Dudukan lensa pada rel horizontal ideal sedang bergerak ke kiri {a+1} m/s ketika aktuator dilepas. Hambatan diabaikan. Penjelasan yang benar untuk gerak sesudahnya ialah…", ["Ia tetap ke kiri dengan kecepatan tetap karena gaya neto horizontal nol.", "Ia berhenti seketika karena aktuator terlepas.", "Ia memerlukan gaya kelembaman ke kiri."], 0, "Hukum I mempertahankan kecepatan ketika gaya neto nol; gaya kelembaman tambahan tidak dimasukkan dalam kerangka laboratorium."),
            _choice("n1", f"Kapsul pemeriksaan ditarik {18+3*k} N ke kanan dengan hambatan sama besar ke kiri. Kecepatan awalnya nol. Apa yang membedakan kapsul ini dari benda dengan gaya sama tetapi sudah melaju?", ["Resultan gaya kapsul lebih besar.", "Keadaan awal berbeda; keduanya a = 0 tetapi kapsul tetap diam.", "Kapsul harus mulai bergerak karena ada tarikan."], 1, "Jumlah gaya nol mempertahankan keadaan awal. Karena v₀ = 0, kapsul tetap diam.", seconds=180),
            _choice("n2", f"Motor uji memberi dua gerobak gaya neto sama. Gerobak K bermassa {4*a} kg dan L {12*a} kg. Alasan L berubah kecepatan lebih lambat adalah…", ["Inersia L lebih besar sehingga percepatannya sepertiga K.", "L memberi reaksi lebih besar sehingga gaya netonya hilang.", "Massa L adalah gaya yang arahnya berlawanan."], 0, "Massa L tiga kali K. Dengan gaya neto sama, aL = aK/3.", seconds=180),
            _choice("n2", "Muatan bergerak ke atas di sepanjang rel vertikal dan semakin lambat. Tentang gaya netonya, penjelasan yang tepat adalah…", ["Gaya neto ke atas karena gerak ke atas.", "Gaya neto ke bawah karena perubahan kecepatan berarah bawah.", "Gaya neto pasti nol selama belum turun."], 1, "Perlambatan gerak atas memerlukan percepatan bawah dan gaya neto bawah. Arah gerak sesaat tidak menetapkan arah gaya neto.", seconds=180),
            _choice("n3", "Dua wahana laboratorium ruang angkasa dengan massa berbeda saling menekan melalui peredam. Tentang gaya kontak dan percepatannya, pernyataan yang benar adalah…", ["Gaya kontak lebih besar pada wahana berat.", "Gaya kontak sama besar berlawanan, tetapi percepatan dapat berbeda karena massa berbeda.", "Gaya kontak saling menghapus pada masing-masing wahana."], 1, "Dua gaya pasangan berada pada dua wahana. Hukum III menyamakan gaya, Hukum II menghubungkan gaya neto dan massa dengan percepatan.", seconds=180, diagram=_lab("reaction", F=54+6*k, m1=18, m2=54, t=1)),
            _choice("n3", "Kabel menahan lampu diam. Pasangan aksi–reaksi gaya kabel pada lampu adalah…", ["Berat lampu dari Bumi.", "Gaya lampu pada kabel.", "Gaya lampu pada Bumi."], 1, "Pasangan harus berasal dari interaksi kontak kabel–lampu yang sama; balik pemberi dan penerima. Berat menyeimbangkan gaya kabel pada lampu, tetapi bukan pasangannya."),
            _choice("n4", "Pilih alasan yang cocok untuk baling-baling mendorong udara dan menerima gaya dorong dari udara.", ["Ini pasangan gaya pada dua benda dari interaksi yang sama; kedua gaya tidak berada pada diagram baling-baling saja.", "Ini contoh gaya neto nol pada setiap benda.", "Udara bereaksi lebih kecil karena massanya ringan."], 0, "Hukum III menghubungkan baling-baling pada udara dan udara pada baling-baling. Percepatan tiap sistem memerlukan resultan gaya dan massanya.", seconds=180),
            _choice("n4", "Teknisi berkata: 'Gaya yang lebih besar pasti membuat benda saat ini lebih cepat daripada benda lain.' Perbaikan yang paling tepat adalah…", ["Gaya neto lebih besar hanya menjamin percepatan lebih besar bila massa sama; kelajuan saat ini juga bergantung riwayat gerak.", "Pernyataan selalu benar karena gaya sama dengan kelajuan.", "Massa yang besar selalu lebih cepat berapa pun gayanya."], 0, "Hubungan langsung Hukum II ialah antara gaya neto dan percepatan, dengan massa diperhitungkan. Kelajuan bukan ukuran gaya.", seconds=180),
        ]
    if stage == "P10":
        return [
            _choice("n1", "Setelah jeda belajar: kereta yang bergerak lurus tetap mempunyai gaya normal dan berat seimbang serta gaya horizontal neto nol. Mengapa kereta tidak harus berhenti?", ["Karena kecepatan dapat bertahan ketika percepatan nol.", "Karena normal mendorongnya maju.", "Karena berat menjadi gaya horizontal."], 0, "Gaya neto nol mempertahankan kecepatan awal, termasuk kecepatan yang tidak nol."),
            _choice("n2", "Dalam uji ulang, massa benda dibuat tiga kali sementara gaya neto tetap. Akibat yang tepat adalah…", ["Percepatan menjadi tiga kali.", "Percepatan menjadi sepertiga.", "Kecepatan langsung menjadi nol."], 1, "a berbanding terbalik dengan m ketika ΣF tetap.", seconds=180),
            _choice("n3", "Sebuah kaki menekan lantai. Pasangan dari gaya kaki pada lantai ialah…", ["Lantai menekan kaki.", "Bumi menarik kaki.", "Kaki menarik Bumi secara gravitasi."], 0, "Pasangan satu interaksi kontak diperoleh dengan menukar pemberi dan penerima."),
            _choice("n4", "Pilih penjelasan yang dapat dipakai untuk contoh baru benda melambat.", ["Benda kehabisan gaya geraknya.", "Gaya neto berlawanan arah kecepatan memberi percepatan yang mengurangi kelajuannya pada selang itu.", "Tidak ada gaya ketika benda melambat."], 1, "Sebutkan interaksi yang menghasilkan gaya neto; perubahan kecepatan mengikuti arah percepatan.", seconds=180),
        ]
    raise ValueError(f"Tahap tidak didukung: {stage}")


def _statika(stage, k):
    W = 100 + 20*k
    if stage == "P2":
        return [
            _num("s1", f"Gaya tegak lurus {20+5*k} N bekerja {0.4:.2f} m dari poros. Berapa besar momennya?", "Besar momen", (20+5*k)*0.4, "N·m", "Untuk gaya tegak lurus, d = r dan |τ| = Fd."),
            _choice("s1", "Lengan momen adalah…", ["Panjang benda berapa pun arah gayanya.", "Jarak tegak lurus poros ke garis kerja gaya.", "Besar gaya dibagi massa."], 1, "Garis kerja gaya harus ditarik dahulu; d diukur tegak lurus terhadap garis itu."),
            _num("s3", f"Gaya kabel {W} N bersudut 30° terhadap mendatar. sin 30° = 0,5. Berapa besar komponen tegaknya?", "Komponen tegak", W*0.5, "N", "Sudut dari mendatar, maka Fy = T sin θ = 0,5T."),
            _num("s3", f"Gaya {W} N bersudut 60° dari mendatar. cos 60° = 0,5. Berapa besar komponen mendatarnya?", "Komponen mendatar", W*0.5, "N", "Komponen yang menempel pada sudut dari mendatar memakai cosinus."),
            _choice("s2", "Benda tegar mula-mula diam akan setimbang statis bila…", ["Hanya jumlah gaya nol.", "Jumlah gaya dan jumlah momen keduanya nol.", "Hanya momen salah satu gaya nol."], 1, "Periksa translasi dan rotasi; dua syarat tersebut saling melengkapi."),
            _choice("s2", "Gaya ke bawah pada ujung kanan batang berporos di kiri cenderung memutar…", ["Searah jarum jam.", "Berlawanan jarum jam.", "Tidak memutar karena gayanya tegak."], 0, "Ujung kanan terdorong ke bawah, sehingga arah putar searah jarum jam."),
            _num("s1", f"Buku bermassa {2+k} kg diam di rak. Gunakan g = 10 m/s². Berapa berat buku?", "Berat buku", (2+k)*10, "N", "W = mg; massa dan berat berbeda besaran serta satuan."),
            _choice("s4", "Batang ideal berengsel tanpa penahan momen diberi beban di ujung. Agar dapat tetap mendatar, penyangga harus…", ["Memberi momen lawan yang menyeimbangkan momen beban.", "Menghilangkan gravitasi pada beban.", "Hanya mengubah warna batang."], 0, "Penyangga mengalihkan gaya ke tumpuan dan menyediakan momen penahan; beban tetap ada.", seconds=180),
        ]
    if stage == "P5":
        F = 40+10*k
        return [
            _choice("s1", "Dua rak memiliki beban sama. Pilih perubahan yang langsung memperbesar besar momen beban terhadap engsel.", ["Menggeser beban menjauhi engsel.", "Mengganti label tanpa mengubah sifat bahan.", "Mengecat warna lain dengan perubahan massa diabaikan."], 0, "Untuk berat vertikal, |τ| = Wx. Memperbesar x memperbesar momen, sedangkan perubahan dekoratif tidak masuk model.", level="C4", seconds=180),
            _num("s2", f"Dua gaya sejajar berlawanan masing-masing {F} N membentuk pasangan gaya dengan jarak tegak lurus 0,30 m. Berapa besar momen yang harus dilawan agar setimbang?", "Besar momen lawan", F*0.3, "N·m", f"Resultan gaya pasangan nol, tetapi besar momennya Fd = {F} × 0,30. Diperlukan momen lawan sama besar.", level="C4", seconds=240, diagram=_lab("couple", F=F, d=0.3)),
            _num("s3", f"Rak ideal panjang 1,6 m mempunyai beban {W} N di tengah. Kabel ujung bersudut 30° dari rak, sin 30° = 0,5. Berapa tegangannya?", "Tegangan kabel", W, "N", "Στengsel = 0 memberi T sin 30° × L = W × (L/2), sehingga T = W.", level="C4", seconds=240, diagram=_lab("cable", W=W, theta=30, fraction=0.5, L=1.6)),
            _num("s3", f"Pada rak ideal, beban {W} N diletakkan pada f = 0,60. Keseimbangan momen mengharuskan komponen tegak kabel 0,60W. Berapa komponen vertikal reaksi engsel (atas positif)?", "Reaksi vertikal", W*0.4, "N", "ΣFy = 0 ⇒ Ry = W − Ty = W − 0,60W = 0,40W.", level="C4", seconds=240),
            _choice("s4", "Dua kabel pada rak yang sama bersudut 30° dan 60°. Beban dan letaknya tetap. Keduanya memiliki batas kerja sama. Mengapa kabel 60° membutuhkan tegangan lebih kecil?", ["Komponen tegak per newton tegangan lebih besar, sementara momen penahan yang diperlukan tetap.", "Gravitasi lebih lemah pada sudut besar.", "Engsel tidak lagi menerima gaya apa pun."], 0, "Ty = Wf tetap, tetapi sin 60° > sin 30°, sehingga T = Ty/sin θ lebih kecil.", level="C4", seconds=240),
        ]
    if stage == "P7":
        F = 30+10*k
        return [
            _choice("s1", "Perancang ingin mengurangi momen buku pada rak tanpa mengubah beratnya. Pilih usulan yang mekanismenya tepat.", ["Dekatkan buku ke engsel agar lengan berat mengecil.", "Ganti nama rak agar lebih kuat.", "Jauhkan buku agar gaya lebih tersebar, tanpa perubahan lain."], 0, "Momen berat terhadap engsel adalah Wx; mendekatkan beban mengurangi x.", level="C4", seconds=180),
            _num("s1", f"Gaya {F} N bekerja pada batang mendatar ke kanan dari engsel, r = 0,60 m dan θ = −30°. sin(−30°) = −0,5. Tentukan momen bertanda.", "Momen bertanda", -0.3*F, "N·m", "τ = rF sin θ = −0,30F. Tanda negatif menyatakan putaran searah jarum jam.", level="C3", seconds=180, diagram=_lab("torque", F=F, r=0.6, theta=-30)),
            _choice("s1", "Gaya besar menarik sepanjang sumbu batang mendatar, dengan garis kerja melewati engsel. Mengapa momennya nol?", ["Gaya tersebut hilang.", "Jarak tegak lurus engsel ke garis kerja gaya nol.", "Setiap gaya mendatar selalu nol."], 1, "Momen ditentukan Fd. Gaya bisa tidak nol walaupun d = 0.", level="C4", seconds=180),
            _num("s2", f"Dua gaya {F} N berlawanan membentuk kopel dengan d = 0,50 m. Berapa besar momen pasangan itu?", "Momen pasangan", F*0.5, "N·m", "Besar momen pasangan = Fd; tidak perlu menggandakan lagi menjadi 2Fd.", level="C3", seconds=180, diagram=_lab("couple", F=F, d=0.5)),
            _choice("s2", "Audit struktur menemukan ΣFx = ΣFy = 0, tetapi Στengsel = −18 N·m dan tidak ada momen penahan lain. Keputusan yang tepat adalah…", ["Sudah setimbang karena gaya nol.", "Belum setimbang; masih ada kecenderungan rotasi searah jarum jam.", "Momen boleh diabaikan karena satuannya berbeda dari gaya."], 1, "Kesetimbangan benda tegar memerlukan syarat momen juga; tanda negatif menunjukkan arah putar.", level="C4", seconds=240),
            _num("s3", f"Rak ideal 2,0 m menahan beban {W} N di ujung. Kabel di ujung memiliki sin θ = 0,80. Berapa besar T?", "Tegangan", W/0.8, "N", "Momen terhadap engsel: T sin θ × 2 = W × 2, jadi T = W/0,80.", level="C3", seconds=240, diagram=_lab("cable", W=W, theta=53.130102, fraction=1, L=2)),
            _num("s3", f"Beban {W} N berada pada 0,40 panjang rak ideal. Kabel ujung bersudut 30°, sin 30° = 0,5. Berapa tegangan yang diperlukan?", "Tegangan", W*0.8, "N", "Ty = 0,40W dari momen; T = 0,40W/0,5 = 0,80W.", level="C4", seconds=240, diagram=_lab("cable", W=W, theta=30, fraction=0.4, L=1.5)),
            _num("s3", f"Beban {W} N berada di f = 0,70 pada rak ideal. Berapa komponen vertikal reaksi engsel jika kabel ujung menyeimbangkan momen?", "Ry (atas positif)", W*0.3, "N", "Momen memberi Ty = 0,70W; keseimbangan gaya memberi Ry = W − Ty = 0,30W.", level="C4", seconds=240),
            _choice("s4", "Dua rancangan rak memerlukan Ty = 80 N di ujung. A bersudut 30°, B bersudut 90°; batas kabel keduanya 120 N. Keputusan model yang benar adalah…", ["A memenuhi, B tidak.", "B memenuhi (T = 80 N); A tidak (T = 160 N).", "Keduanya memenuhi karena Ty < 120 N."], 1, "Batas membatasi tegangan penuh T, bukan hanya Ty. TA = 80/0,5 = 160 N; TB = 80/1 = 80 N.", level="C4", seconds=300),
            _choice("s4", "Analisis rak ideal memberi T di bawah batas kabel. Data mana masih diperlukan untuk menyimpulkan semua sambungan memenuhi batas?", ["Kapasitas engsel, baut, dan dinding terhadap gaya yang diterimanya.", "Warna katalog rak.", "Nama produsen tanpa data kekuatan."], 0, "Masing-masing komponen menerima gaya dan mempunyai batas sendiri. Lulus batas kabel tidak otomatis memeriksa sambungan lain.", level="C4", seconds=240),
        ]
    if stage == "P9":
        # Konteks dan angka berbeda dari latihan: papan tanda, lengan sensor, kanopi.
        Q = 90+30*k
        return [
            _choice("s1", "Panel tanda yang berengsel menerima beban titik tetap. Pernyataan mana merupakan alasan fisik untuk memasukkan letak beban dalam analisis?", ["Letak menentukan lengan terhadap poros dan mengubah momen beban.", "Letak hanya memengaruhi tampilan panel.", "Semakin jauh dari engsel selalu semakin kecil gaya gravitasi."], 0, "Untuk berat vertikal pada panel mendatar, momen terhadap engsel bergantung jarak mendatar x.", level="C4", seconds=180),
            _num("s1", f"Lengan sensor mendatar ke kanan berporos di kiri menerima gaya {Q} N pada r = 0,25 m, θ = 90°. Berapa momen bertandanya (berlawanan jarum jam positif)?", "Momen bertanda", Q*0.25, "N·m", "τ = rF sin 90° = +0,25F. Gaya ke atas di kanan poros memberi momen positif.", level="C3", seconds=180, diagram=_lab("torque", F=Q, r=0.25, theta=90)),
            _choice("s2", "Pada panel bebas, dua gaya sama besar berlawanan bekerja pada garis sejajar terpisah. Seorang teknisi hanya memeriksa ΣF = 0. Apa kekurangan analisisnya?", ["Ia belum memeriksa momen pasangan yang dapat menyebabkan rotasi.", "Ia harus menjumlah kedua besar gaya tanpa arah.", "Ia boleh menyimpulkan diam bila panel mula-mula diam."], 0, "Gaya pasangan mempunyai resultan gaya nol tetapi momen Fd tidak nol; keadaan awal diam tidak menjamin akan tetap diam.", level="C4", seconds=240),
            _num("s2", f"Sepasang gaya pada alat kalibrasi masing-masing {Q/3:g} N membentuk momen {Q*0.12:g} N·m. Berapa jarak tegak lurus kedua garis kerja?", "Jarak garis kerja", 0.36, "m", f"Momen pasangan = Fd, sehingga d = {Q*0.12:g}/({Q/3:g}) = 0,36 m.", tol=0.005, level="C3", seconds=180),
            _num("s3", f"Papan pajangan ideal 1,8 m berengsel di dinding. Beban {Q} N berada 1,08 m dari engsel. Kabel pada ujung mempunyai sin θ = 0,75. Berapa tegangannya?", "Tegangan kabel", Q*0.8, "N", "f = 1,08/1,8 = 0,60; T = Wf/sin θ = W × 0,60/0,75 = 0,80W.", level="C4", seconds=300, diagram=_lab("cable", W=Q, theta=48.590378, fraction=0.6, L=1.8)),
            _num("s3", f"Kanopi ideal tanpa berat sendiri menahan beban {Q} N pada 0,25 panjangnya. Kabel ujung telah memenuhi Στ = 0. Berapa reaksi vertikal engsel, dengan atas positif?", "Reaksi vertikal", Q*0.75, "N", "Dari momen Ty = 0,25W, lalu ΣFy = 0 memberi Ry = W − Ty = 0,75W.", level="C4", seconds=240),
            _choice("s4", "Sebuah papan peraga memerlukan Ty = 72 N di ujung. Rancangan C mempunyai sin θ = 0,60, D sin θ = 0,90. Batas tegangan keduanya 100 N. Pilih keputusan yang benar.", ["C memenuhi dan D gagal.", "D memenuhi dengan T = 80 N; C gagal dengan T = 120 N.", "Keduanya memenuhi karena 72 N lebih kecil dari 100 N."], 1, "Tegangan penuh: TC = 72/0,60 = 120 N; TD = 72/0,90 = 80 N. Momen penahan ditentukan Ty, tetapi batas kabel memeriksa T.", level="C4", seconds=300),
            _choice("s4", "Penyangga diagonal diganti batang tekan di bawah kanopi. Penjelasan yang paling memadai untuk melanjutkan analisis adalah…", ["Semua diagonal sama; data bahan tidak diperlukan.", "Gambar arah gaya tekan sepanjang batang, periksa momen lawannya, lalu periksa batas tekan/tekuk dan sambungan.", "Batang menghilangkan berat beban sehingga ΣF tidak diperlukan."], 1, "Mekanisme gaya dan tanda momennya harus diperiksa. Batang tekan juga dapat gagal karena tekuk; kabel tarik dan batang tekan tidak mempunyai batas yang otomatis sama.", level="C4", seconds=300),
        ]
    if stage == "P10":
        B = 140+20*k
        return [
            _num("s1", f"Saat mengulang materi, beban {B} N pada batang mendatar berada 0,35 m dari engsel dan arahnya ke bawah. Berapa besar momen bebannya?", "Besar momen", B*0.35, "N·m", "Garis kerja vertikal memiliki lengan mendatar 0,35 m, sehingga |τ| = W × 0,35.", level="C3", seconds=180),
            _choice("s2", "Sebuah benda bebas menerima satu gaya melalui titik acuan. Momen terhadap titik itu nol. Apakah itu cukup untuk membuktikan kesetimbangan?", ["Ya, karena semua momen nol berarti semua gaya nol.", "Tidak; resultan gaya masih harus diperiksa dan dapat tidak nol.", "Ya, jika arah gaya mendatar."], 1, "Satu gaya melalui poros acuan memberi τ = 0 tetapi masih dapat mempercepat translasi benda.", level="C4", seconds=240),
            _num("s3", f"Rak ideal menahan beban {B} N di f = 0,60. Kabel ujung mempunyai sin θ = 0,80. Berapa T yang dibutuhkan?", "Tegangan kabel", B*0.75, "N", "Momen memberi Ty = 0,60W; T = Ty/0,80 = 0,75W.", level="C4", seconds=240, diagram=_lab("cable", W=B, theta=53.130102, fraction=0.6, L=1.1)),
            _choice("s4", "Beban dan panjang rak tetap; kabel tidak boleh melebihi batas. Jika beban digeser mendekati engsel, mengapa tegangan yang dibutuhkan turun?", ["Momen berat mengecil sehingga kebutuhan komponen tegak kabel mengecil.", "Massa beban otomatis berkurang.", "Sudut kabel otomatis menjadi 90°."], 0, "Pada sudut tetap, T = Wf/sin θ; mengurangi f menurunkan kebutuhan momen penahan dan tegangan.", level="C4", seconds=240),
        ]
    raise ValueError(f"Tahap tidak didukung: {stage}")


def make_questions(slug, stage, form=1):
    """Kembalikan butir mandiri; form baru mengubah data dan/atau urutan opsi.

    Jumlah tepat: P2=8, P5=5, P7=10, P9=8, P10=4. Soal P9 dibuat
    tersendiri dari latihan. Tidak ada jawaban hasil yang disisipkan di diagram.
    """
    if slug not in LESSONS:
        raise KeyError(f"TP tidak didukung: {slug}")
    stage = str(stage).strip().upper()
    if not stage.startswith("P"):
        stage = "P" + stage
    if stage not in {"P2", "P5", "P7", "P9", "P10"}:
        raise ValueError(f"Tahap tidak didukung: {stage}")
    if isinstance(form, bool) or not isinstance(form, int) or form < 1:
        raise ValueError("form harus bilangan bulat positif")
    questions = deepcopy((_newton if slug == "f-mek-1a" else _statika)(stage, form-1))
    for i, q in enumerate(questions, 1):
        q["id"] = f"{slug}-{stage.lower()}-f{form}-{i:02d}"
        if q["kind"] == "choice":
            # Rotasi memperbarui indeks kunci tanpa mengubah makna opsi.
            shift = (form-1+i) % len(q["options"])
            q["options"] = q["options"][shift:] + q["options"][:shift]
            q["answer"] = (q["answer"]-shift) % len(q["options"])
    return questions


# ID checkpoint stabil untuk penyimpanan jawaban terpisah dari semua bank tahap.
for _slug, _lesson in LESSONS.items():
    for _node in _lesson["concepts"]:
        for _i, _q in enumerate(_node["checks"], 1):
            _q["id"] = f"{_slug}-cp-{_node['id']}-{_i}"

