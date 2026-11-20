"""Materi baru F.USE.1-pra dan F.USE.1 untuk alur P1–P10.

Data pembelajaran, bukan pengendali progres. Semua model memakai g = 10 m/s².
Gesekan pada lab energy hanya berada pada segmen mendatar, sehingga N = mg.
Butir P9 ditulis dalam konteks berbeda dari P7; form memberi data baru.
"""

from math import sqrt


def _lab(kind, **params):
    return {"kind": kind, "params": params}


def _n(qid, indicator, prompt, label, answer, unit="J", *, explain,
       level="C3", seconds=180, tol=0.05, diagram=None, steps=None):
    q = dict(id=qid, indicator=indicator, prompt=prompt, kind="num", label=label,
             unit=unit, answer=answer, tol=tol, explain=explain, level=level,
             seconds=max(seconds, {"C1":120,"C2":120,"C3":180,"C4":240,"C5":300,"C6":300}.get(level,120)))
    if diagram is not None:
        q["diagram"] = diagram
    if steps is not None:
        q["steps"] = steps
    return q


def _c(qid, indicator, prompt, options, answer, *, explain,
       level="C2", seconds=120, diagram=None):
    q = dict(id=qid, indicator=indicator, prompt=prompt, kind="choice",
             label="Pilih satu jawaban", unit="", options=options, answer=answer,
             tol=0, explain=explain, level=level, seconds=max(seconds, {"C1":120,"C2":120,"C3":180,"C4":240,"C5":300,"C6":300}.get(level,120)))
    if diagram is not None:
        q["diagram"] = diagram
    return q


LESSONS = {
    "f-use-1-pra": {
        "bloom": "C2",
        "objective": "Menjelaskan konsep usaha, energi kinetik, dan energi potensial, serta hubungan usaha dengan perubahan energi.",
        "hook": {
            "title": "Kotak yang sama, tarikan yang berbeda",
            "scene": "Di studio kerajinan, sebuah kotak digeser 2 m di atas ubin. Pita penarik dapat diarahkan mendatar atau dimiringkan ke atas. Ketika kotak masuk ke karpet, tarikan yang sama menghasilkan pertambahan kelajuan lebih kecil. Pada layar, ikuti panah gaya, perpindahan kotak, dan perubahan batang energi.",
            "question": "Dengan besar gaya dan perpindahan yang sama, apakah semua arah tarikan memindahkan energi yang sama banyak kepada kotak?",
            "bridge": "Kita mulai dari komponen gaya yang searah perpindahan, lalu mengenali energi karena gerak dan kedudukan. Pada akhir TP, kamu dapat menjelaskan mengapa jumlah usaha semua gaya menentukan perubahan energi kinetik.",
            "lab": _lab("work", F=18, s=2, theta=60),
        },
        "goals": [
            "Menjelaskan konsep usaha, energi kinetik, dan energi potensial, serta hubungan usaha dengan perubahan energi.",
            "Membaca sudut antara gaya dan perpindahan serta menjelaskan tanda usaha.",
            "Membandingkan energi kinetik dan energi potensial dengan besaran serta acuan yang tepat.",
            "Menghubungkan usaha neto positif, nol, atau negatif dengan perubahan kelajuan.",
        ],
        "concepts": [
            {
                "id": "usaha",
                "title": "Usaha: energi berpindah melalui gaya",
                "question": "Mengapa tarikan miring tidak memberi usaha sebesar tarikan mendatar?",
                "explain": [
                    "Pilih benda yang ditinjau dan dua posisinya. Dalam model gaya tetap pada gerak lurus, usaha oleh suatu gaya adalah hasil kali komponen gaya yang searah perpindahan dengan besar perpindahan. Pada kotak yang bergeser mendatar, hanya komponen mendatar tarikan yang masuk ke perhitungan usaha tarikan. Komponen vertikal tetap dapat memengaruhi gaya normal, tetapi bukan usaha langsung tarikan sepanjang perpindahan mendatar.",
                    "Sudut θ diukur dari arah perpindahan menuju arah gaya, bukan selalu dari permukaan atau dari garis vertikal. Di lab, panah perpindahan menunjuk ke kanan. Saat θ = 0°, seluruh gaya searah perpindahan dan W = Fs. Saat θ = 60°, hanya separuh besar gaya sejajar perpindahan. Saat θ = 90°, proyeksinya nol, sehingga usaha gaya itu nol walaupun gaya bekerja.",
                    "Usaha bertanda positif jika gaya membantu perpindahan, negatif jika komponen gaya melawannya, dan nol jika perpindahan atau komponen sejajarnya nol. Contohnya, gaya gesek ke kiri pada kotak yang bergeser ke kanan melakukan usaha negatif. Tanda negatif menyatakan arah perpindahan energi dari gerak benda; tanda itu bukan berarti besar gaya bernilai negatif.",
                    "Satuan usaha adalah joule, dengan 1 J = 1 N·m. Persamaan W = Fs cos θ berlaku langsung jika gaya dan sudut tetap selama perpindahan. Untuk gaya yang berubah, ruas lintasan perlu dianalisis lebih lanjut. Satu usaha juga belum menyatakan perubahan gerak: usaha tarikan, gesekan, gravitasi, dan normal harus dibedakan sebelum dijumlahkan.",
                ],
                "formula": "W = F s cos θ; W_net = jumlah aljabar usaha semua gaya",
                "quantities": ["W: usaha suatu gaya (J)", "F: besar gaya tetap (N)", "s: besar perpindahan lurus (m)", "θ: sudut gaya terhadap perpindahan (°)"],
                "assumptions": ["Benda dimodelkan sebagai partikel dan perpindahan lurus.", "Gaya dan sudut tetap selama ruas yang dihitung.", "Lab ini menampilkan usaha satu gaya, bukan otomatis usaha neto."],
                "lab": _lab("work", F=24, s=3, theta=60),
                "explore": [
                    "Prediksi: dengan F dan s tetap, urutkan usaha pada θ = 0°, 60°, 90°, dan 180°.",
                    "Ubah: geser hanya θ melalui empat nilai itu; pertahankan F = 24 N dan s = 3 m.",
                    "Amati: cocokkan arah panah dan proyeksi mendatarnya dengan tanda serta tinggi batang usaha. Coba juga s = 0.",
                    "Jelaskan: tulis mengapa panah gaya yang panjang belum menjamin usaha besar, dan mengapa pada 180° hasilnya negatif.",
                ],
                "misconception": {"claim": "Jika ada gaya, pasti ada usaha positif.", "explain": "Usaha memerlukan perpindahan dan komponen gaya sepanjang perpindahan. Gaya tegak lurus dapat melakukan usaha nol; gaya yang melawan perpindahan melakukan usaha negatif. Mulailah dengan menggambar dua panah sebelum memilih tanda."},
                "worked": {
                    "scenario": "Peti perlengkapan ditarik 30 N dengan sudut 60° terhadap perpindahan mendatar 1,6 m. Tentukan usaha gaya tarik saja; cos 60° = 0,5.",
                    "steps": [
                        "Model: tinjau peti sebagai partikel; gaya tarik dan sudutnya tetap. Yang dicari usaha tarikan, sehingga gesekan belum dijumlahkan.",
                        "Data: F = 30 N, s = 1,6 m, θ = 60°; sudut diukur antara panah gaya dan perpindahan ke kanan.",
                        "Alasan: komponen sejajar perpindahan adalah F cos θ = 30 × 0,5 = 15 N; komponen vertikal tidak berpindah vertikal.",
                        "Persamaan: W_tarikan = F s cos θ = 30 × 1,6 × 0,5.",
                        "Hasil: W_tarikan = +24 J. Tarikan memindahkan energi sebesar 24 J melalui komponen mendatarnya.",
                        "Cek: batas maksimum untuk data ini Fs = 48 J. Hasil 24 J masuk akal karena sudut 60° menyisakan setengah proyeksi gaya.",
                    ],
                    "result": "Usaha gaya tarik = +24 J; perubahan energi kinetik baru diketahui jika usaha gaya lain juga dihitung.",
                },
                "checks": [
                    _n("pra-cp-usaha-1", "usaha", "Sebuah laci didorong 16 N searah perpindahannya sejauh 1,5 m. Berapa usaha gaya dorong?", "Usaha gaya dorong", 24, explain="W = Fs = 16 × 1,5 = +24 J. Gaya searah perpindahan.", diagram=_lab("work", F=16, s=1.5, theta=0)),
                    _c("pra-cp-usaha-2", "usaha", "Gaya penahan mengarah ke kiri ketika objek berpindah ke kanan. Apa tanda usaha gaya penahan?", ["Positif karena objek tetap bergerak.", "Negatif karena gaya berlawanan perpindahan.", "Nol karena arah keduanya berbeda."], 1, explain="Sudutnya 180°, sehingga cos θ = −1. Arah berbeda belum tentu tegak lurus.", diagram=_lab("work", F=12, s=2, theta=180)),
                ],
            },
            {
                "id": "kinetik",
                "title": "Energi kinetik: kelajuan berpengaruh kuadrat",
                "question": "Dua paket bergerak sama cepat; mengapa paket lebih berat lebih sulit dihentikan?",
                "explain": [
                    "Energi kinetik adalah energi yang terkait dengan gerak benda. Dalam model partikel yang bergerak translasi, nilainya Ek = ½mv². Massa menyatakan banyaknya inersia benda, sedangkan kelajuan v menyatakan besar kecepatan terhadap pengamat yang dipilih. Di sini pengamat diam terhadap lantai, sehingga nilai kelajuan dapat dibandingkan secara konsisten.",
                    "Massa masuk secara linear: pada kelajuan sama, massa dua kali memberi energi kinetik dua kali. Kelajuan masuk sebagai kuadrat: pada massa sama, kelajuan dua kali memberi energi empat kali. Ini menjelaskan mengapa peningkatan kelajuan yang tampak kecil dapat menambah banyak energi yang harus dipindahkan ketika benda dihentikan.",
                    "Energi kinetik tidak memuat tanda arah gerak. Paket yang bergerak ke kiri atau ke kanan dengan massa dan kelajuan sama mempunyai Ek sama. Nilainya nol ketika benda diam terhadap pengamat itu, dan tidak dapat negatif. Kelajuan dalam m/s harus dikuadratkan seluruhnya sebelum dikalikan setengah massa dalam kg; satuannya menjadi kg·m²/s² = J.",
                    "Besaran Ek bukan gaya dan bukan pula usaha. Energi kinetik adalah keadaan gerak pada satu saat, sementara usaha merupakan pemindahan energi sepanjang proses. Model ini mengabaikan putaran roda atau putaran benda. Jika benda berotasi, energi rotasinya perlu dicatat terpisah; visual paket di halaman ini sengaja memakai model partikel yang meluncur.",
                ],
                "formula": "Ek = ½ m v²; Ek_baru / Ek_awal = (m_baru / m_awal)(v_baru / v_awal)²",
                "quantities": ["Ek: energi kinetik translasi (J)", "m: massa (kg)", "v: kelajuan terhadap lantai (m/s)"],
                "assumptions": ["Gerak translasi dalam model partikel.", "Massa tetap dan semua kelajuan diukur terhadap lantai.", "Energi putaran dan deformasi benda diabaikan."],
                "lab": _lab("kinetic", m=2, v=3),
                "explore": [
                    "Prediksi: mana yang menggandakan Ek, menggandakan massa atau menggandakan kelajuan?",
                    "Ubah: dari m = 2 kg dan v = 3 m/s, ubah massa menjadi 4 kg. Reset, kemudian ubah kelajuan menjadi 6 m/s.",
                    "Amati: bandingkan ukuran objek, jejak gerak, dan batang Ek pada kedua perubahan. Kembalikan kelajuan ke nol sebagai cek batas.",
                    "Jelaskan: gunakan satu perbandingan angka untuk membedakan pengaruh m dan pengaruh v²; sebutkan mengapa Ek tidak negatif.",
                ],
                "misconception": {"claim": "Kelajuan tiga kali berarti energi kinetik tiga kali.", "explain": "Untuk massa tetap, kuadrat kelajuan memberi faktor 3² = 9. Bandingkan rumus sebelum menghitung nilai mutlak agar faktor kuadrat tidak terlewat."},
                "worked": {
                    "scenario": "Sebuah paket 1,2 kg meluncur dengan kelajuan 5 m/s terhadap lantai. Berapa energi kinetiknya?",
                    "steps": [
                        "Model: paket dianggap partikel tanpa putaran, sehingga hanya energi kinetik translasi yang dihitung.",
                        "Data: m = 1,2 kg dan v = 5 m/s; massa dan kelajuan sudah memakai satuan SI.",
                        "Alasan: energi gerak bergantung pada kelajuan kuadrat, bukan arah. Gunakan Ek = ½mv².",
                        "Hitung: v² = 25 m²/s², lalu Ek = 0,5 × 1,2 × 25 = 15 kg·m²/s².",
                        "Hasil: energi kinetik paket = 15 J terhadap pengamat di lantai.",
                        "Cek: jika kelajuan 10 m/s dengan massa sama, Ek = 60 J, yaitu empat kali hasil awal; hubungan kuadrat terpenuhi.",
                    ],
                    "result": "Ek = 15 J. Arah gerak berlawanan pada kelajuan sama tetap menghasilkan Ek sebesar ini.",
                },
                "checks": [
                    _n("pra-cp-kinetik-1", "kinetik", "Wadah 0,8 kg meluncur dengan kelajuan 5 m/s terhadap lantai. Berapa Ek translasi wadah?", "Energi kinetik", 10, explain="Ek = ½ × 0,8 × 5² = 10 J.", diagram=_lab("kinetic", m=.8, v=5)),
                    _c("pra-cp-kinetik-2", "kinetik", "Massa tetap. Kelajuan suatu benda berubah dari 2 m/s menjadi 6 m/s. Energi kinetik akhirnya berapa kali energi kinetik awal?", ["3 kali.", "6 kali.", "9 kali."], 2, explain="Perbandingan Ek = (6/2)² = 9. Yang dikuadratkan adalah faktor perubahan kelajuan.", seconds=180),
                ],
            },
            {
                "id": "potensial",
                "title": "Energi potensial: ketinggian memerlukan acuan",
                "question": "Apakah wadah di rak dapat mempunyai Ep nol jika acuannya diganti?",
                "explain": [
                    "Energi potensial gravitasi berhubungan dengan kedudukan dalam interaksi benda–Bumi. Di dekat permukaan Bumi dengan g dianggap tetap, kita memakai Ep = mg(h − h_ref). Posisi vertikal benda dinyatakan oleh h, sementara h_ref adalah posisi acuan yang disepakati mempunyai Ep = 0. Di lab, garis acuan dapat digeser tanpa memindahkan benda.",
                    "Jika acuan adalah lantai, benda 2 m di atas lantai mempunyai tinggi relatif +2 m. Jika acuan dinaikkan tepat ke posisi benda, tinggi relatif dan Ep menjadi nol. Jika garis acuan lebih tinggi daripada benda, Ep negatif. Nilai negatif dibolehkan untuk energi potensial karena nolnya merupakan pilihan; ini berbeda dengan energi kinetik yang tidak negatif.",
                    "Walaupun nilai Ep bergantung pada acuan, perubahan Ep antara dua posisi tidak bergantung pada pilihan acuan yang tetap. Untuk kenaikan Δh, ΔEp = mgΔh positif. Ketika benda turun, ΔEp negatif, dan gravitasi melakukan usaha W_g = −ΔEp. Tanda ini menjelaskan pertukaran energi: saat gravitasi membantu benda turun, energi potensial berkurang.",
                    "Perhatikan bahwa tinggi adalah selisih vertikal, bukan panjang papan miring yang ditempuh. Papan lebih panjang tidak otomatis memberikan perubahan Ep lebih besar jika kedua ujungnya sama tinggi. Model mgh berlaku pada rentang tinggi yang cukup kecil sehingga g konstan; tidak langsung dipakai untuk perpindahan jauh dari Bumi. Selalu tuliskan acuan dan gunakan g = 10 m/s² dalam kegiatan ini.",
                ],
                "formula": "Ep = m g (h − h_ref); ΔEp = m g (h_akhir − h_awal); W_g = −ΔEp",
                "quantities": ["Ep: energi potensial gravitasi relatif terhadap acuan (J)", "m: massa (kg)", "g: percepatan gravitasi, 10 m/s²", "h dan h_ref: posisi vertikal benda dan acuan (m)"],
                "assumptions": ["Dekat permukaan Bumi dengan g tetap.", "Acuan yang sama dipakai ketika membandingkan dua posisi.", "Tinggi diukur vertikal; sistem energi potensial mencakup interaksi benda–Bumi."],
                "lab": _lab("potential", m=2, h=3, ref=0),
                "explore": [
                    "Prediksi: jika benda tetap di h = 3 m, apa yang terjadi pada Ep ketika garis acuan dinaikkan dari 0 m ke 3 m?",
                    "Ubah: pertahankan m = 2 kg dan h = 3 m; geser hanya ref dari 0 ke 3 lalu 4 m.",
                    "Amati: posisi benda tetap, tetapi jarak vertikal bertanda terhadap garis acuan dan batang Ep berubah dari positif ke nol lalu negatif.",
                    "Jelaskan: bandingkan perubahan Ep saat benda berpindah dari h = 3 m ke h = 2 m untuk dua acuan. Mengapa selisihnya tetap −20 J?",
                ],
                "misconception": {"claim": "Mengganti acuan mengubah energi yang diperlukan untuk mengangkat benda antara dua tempat.", "explain": "Pergantian acuan menambah konstanta yang sama pada nilai Ep awal dan akhir. Konstanta itu saling menghilangkan dalam ΔEp. Posisi fisik serta perubahan energi saat pengangkatan tetap sama."},
                "worked": {
                    "scenario": "Wadah 1,5 kg dipindahkan dari rak h = 0,8 m ke rak h = 2 m. Kedua tinggi diukur dari lantai. Tentukan perubahan Ep; g = 10 m/s².",
                    "steps": [
                        "Model: gunakan interaksi wadah–Bumi dengan g tetap; yang ditanyakan perubahan energi potensial.",
                        "Data dan acuan: m = 1,5 kg, h_awal = 0,8 m, h_akhir = 2 m; lantai adalah h_ref = 0.",
                        "Alasan: yang diperlukan adalah selisih tinggi vertikal, Δh = 2 − 0,8 = +1,2 m, bukan panjang jalur pengangkatan.",
                        "Persamaan: ΔEp = mgΔh = 1,5 × 10 × 1,2.",
                        "Hasil: ΔEp = +18 J. Tanda positif menunjukkan energi potensial meningkat ketika wadah dinaikkan.",
                        "Cek: Ep awal = 12 J dan Ep akhir = 30 J, sehingga selisih 18 J. Memilih rak awal sebagai acuan juga memberi selisih 18 J.",
                    ],
                    "result": "Perubahan Ep = +18 J; usaha gravitasi selama perpindahan tersebut = −18 J.",
                },
                "checks": [
                    _n("pra-cp-potensial-1", "potensial", "Benda 0,6 kg berada pada h = 2,5 m. Garis acuan Ep = 0 berada pada h_ref = 0,5 m. g = 10 m/s². Berapa Ep benda terhadap acuan itu?", "Energi potensial", 12, explain="Tinggi relatif = 2,5 − 0,5 = 2 m; Ep = 0,6 × 10 × 2 = 12 J.", diagram=_lab("potential", m=.6, h=2.5, ref=.5)),
                    _c("pra-cp-potensial-2", "potensial", "Sebuah wadah tetap di tempat. Garis acuan Ep dinaikkan tepat ke posisi wadah. Pernyataan yang tepat adalah…", ["Ep menjadi nol; posisi wadah tetap.", "Wadah kehilangan semua energi kinetik.", "Gaya gravitasi menjadi nol."], 0, explain="Nol Ep adalah pilihan acuan. Mengubah acuan tidak mengubah posisi, gerak, atau gaya gravitasi pada wadah.", diagram=_lab("potential", m=1, h=2, ref=2)),
                ],
            },
            {
                "id": "usaha-neto",
                "title": "Usaha neto adalah perubahan energi kinetik",
                "question": "Mengapa kotak di karpet bertambah cepat lebih sedikit meskipun usaha tariknya sama?",
                "explain": [
                    "Satu benda dapat menerima beberapa gaya sekaligus. Teorema usaha–energi menyatakan jumlah aljabar usaha semua gaya sama dengan perubahan energi kinetik: W_net = Ek_akhir − Ek_awal. Jadi usaha tarikan yang positif dapat sebagian diimbangi usaha gesekan yang negatif. Pada lintasan mendatar, gravitasi dan gaya normal tidak melakukan usaha karena keduanya tegak lurus perpindahan.",
                    "Usaha neto positif berarti Ek bertambah, sehingga kelajuan meningkat untuk massa tetap. Usaha neto negatif berarti Ek berkurang dan benda melambat. Usaha neto nol berarti Ek awal dan akhir sama. Pernyataan terakhir tidak menuntut setiap gaya nol: dorongan dan gesekan dapat mempunyai usaha yang saling meniadakan.",
                    "Hitung selisih energi dengan urutan akhir dikurangi awal. Bila benda 2 kg berubah dari 3 m/s ke 1 m/s, ΔEk = ½ × 2 × (1² − 3²) = −8 J. Tanda negatif berasal dari pengurangan energi gerak, bukan dari kelajuan yang negatif. Jika yang diketahui usaha dan kelajuan awal, susun Ek_akhir = Ek_awal + W_net sebelum mencari akar kelajuan akhir.",
                    "Lab memakai F sebagai gaya neto mendatar tetap, bukan satu gaya tarik yang masih harus dikurangi gesekan. Dengan W_net = Fs, energi akhir tidak boleh negatif. Jika gaya pengerem akan menghentikan benda sebelum jarak pilihan tercapai, gerak yang benar berhenti lebih awal; rumus kelajuan untuk keadaan yang tidak terjangkau tidak boleh diteruskan. Seluruh pembahasan tetap pada translasi partikel dengan massa tetap.",
                ],
                "formula": "W_net = ΔEk = ½ m v_akhir² − ½ m v_awal²; Ek_akhir = Ek_awal + W_net",
                "quantities": ["W_net: jumlah usaha semua gaya (J)", "Ek_awal dan Ek_akhir: energi kinetik pada dua keadaan (J)", "m: massa tetap (kg)", "v_awal dan v_akhir: kelajuan (m/s)", "F pada lab: gaya neto mendatar bertanda (N)"],
                "assumptions": ["Model partikel translasi dengan massa tetap.", "Lab memakai gaya neto konstan, F positif searah perpindahan dan negatif melawannya.", "Gerak hanya dianalisis sampai berhenti; tidak ada Ek negatif."],
                "lab": _lab("workenergy", F=6, s=2, m=2, v0=2),
                "explore": [
                    "Prediksi: mulai dengan m = 2 kg dan v0 = 2 m/s. Apakah tambahan W_net = 12 J membuat kelajuan menjadi dua kali?",
                    "Ubah: pertahankan massa, kelajuan awal, dan s = 2 m; ubah F_net dari 6 N ke 0 N lalu −1 N.",
                    "Amati: bandingkan batang Ek awal, usaha bertanda, dan Ek akhir; periksa perubahan kelajuan dengan nilai kuadratnya.",
                    "Jelaskan: mengapa W_net = 0 tidak berarti benda diam? Hubungkan keadaan itu dengan energi awal yang tetap ada.",
                ],
                "misconception": {"claim": "Usaha gaya tarik selalu sama dengan perubahan energi kinetik.", "explain": "Teorema memakai usaha neto. Jika tarikan melakukan +20 J dan gesekan −8 J, ΔEk hanya +12 J. Buat daftar usaha per gaya terlebih dahulu, lalu jumlahkan dengan tandanya."},
                "worked": {
                    "scenario": "Kotak 2 kg mula-mula bergerak 2 m/s. Dalam perpindahan mendatar, tarikan melakukan +18 J dan gesekan −6 J. Normal dan berat tidak melakukan usaha. Tentukan kelajuan akhirnya.",
                    "steps": [
                        "Model: partikel bermassa tetap pada lintasan mendatar; gunakan jumlah usaha semua gaya.",
                        "Data: m = 2 kg, v_awal = 2 m/s; W_tarikan = +18 J, W_gesek = −6 J, W_normal = W_berat = 0.",
                        "Neraca usaha: W_net = 18 − 6 = +12 J. Usaha tarikan saja tidak boleh langsung dijadikan ΔEk.",
                        "Energi awal dan akhir: Ek_awal = ½ × 2 × 2² = 4 J; Ek_akhir = 4 + 12 = 16 J.",
                        "Hasil: ½ × 2 × v_akhir² = 16, maka v_akhir = 4 m/s. Dipilih akar positif karena yang dicari kelajuan.",
                        "Cek: ΔEk = 16 − 4 = +12 J sama dengan W_net. Kelajuan meningkat sesuai tanda usaha neto, dan satuan energi tetap joule.",
                    ],
                    "result": "Kelajuan akhir = 4 m/s; usaha neto = +12 J.",
                },
                "checks": [
                    _n("pra-cp-neto-1", "usaha-neto", "Energi kinetik sebuah objek berubah dari 14 J menjadi 9 J. Berapa usaha neto pada objek?", "Usaha neto", -5, explain="W_net = Ek_akhir − Ek_awal = 9 − 14 = −5 J. Objek kehilangan energi kinetik.", level="C2", seconds=120),
                    _n("pra-cp-neto-2", "usaha-neto", "Wadah 2 kg mula-mula bergerak 3 m/s. Gaya neto 4 N searah gerak bekerja sepanjang 4 m. Berapa kelajuan akhirnya?", "Kelajuan akhir", 5, "m/s", explain="Ek_awal = 9 J; W_net = 16 J; Ek_akhir = 25 J. Karena ½m = 1 kg, v_akhir = √25 = 5 m/s.", seconds=240, diagram=_lab("workenergy", F=4, s=4, m=2, v0=3)),
                ],
            },
        ],
        "prediction": [
            "Kotak bergeser mendatar dengan besar gaya tarik tetap. Jika sudut tarik dinaikkan dari 0° ke 60° tanpa mengubah perpindahan, prediksikan perubahan usaha tarikan dan berikan alasan melalui komponen gaya.",
            "Dua wadah bermassa sama memiliki kelajuan 2 m/s dan 4 m/s. Apakah usaha untuk menghentikannya pada lantai mendatar sama besar? Nyatakan prediksi tanda serta perbandingannya, lalu jelaskan alasan awalmu.",
        ],
        "performance": {
            "scenario": "Jadilah penyusun petunjuk pemindahan kotak pameran. Kotak 2 kg mula-mula bergerak 2 m/s di lantai mendatar, lalu ditarik 12 N mendatar sepanjang 1 m dan mengalami gaya gesek tetap 4 N. Setelah itu kotak diletakkan diam di panggung setinggi 0,6 m terhadap lantai. Gunakan g = 10 m/s². Jelaskan setiap tahap tanpa menyamakan usaha satu gaya, energi gerak, dan energi kedudukan. Pengangkatan adalah tahap terpisah; cara kotak dihentikan tidak perlu dirancang.",
            "deliverables": [
                "Satu diagram tahap mendatar dengan panah gaya dan perpindahan serta satu gambar ketinggian panggung dengan acuan lantai.",
                "Perhitungan usaha tarik, usaha gesek, dan usaha neto, serta alasan usaha berat dan normal nol pada tahap mendatar.",
                "Neraca Ek awal dan akhir beserta makna perubahannya; perhitungan kelajuan akhir boleh dipakai untuk mendukung penjelasan.",
                "Perhitungan Ep kotak diam di panggung terhadap lantai dan penjelasan perubahan nilainya jika acuan dipilih di panggung, sementara posisi fisiknya tetap.",
                "Satu perbaikan terhadap klaim: semua usaha tarik menjadi energi kinetik dan benda diam selalu tidak mempunyai energi.",
            ],
            "rubric": {
                "T1": "Menyebut rumus atau angka secara terpisah, tetapi arah usaha, energi gerak, dan acuan Ep masih tertukar.",
                "T2": "Diagram dan sebagian perhitungan benar; satu alasan penting tentang usaha neto atau acuan Ep belum tepat sehingga hubungan antartahap belum utuh.",
                "T3": "Diagram berlabel, tanda usaha dan neraca Ek benar, Ep memakai acuan jelas, serta kedua klaim diperbaiki dengan alasan fisika dan satuan yang tepat.",
                "T4": "Memenuhi T3 serta memeriksa hasil melalui selisih energi, menunjukkan acuan Ep alternatif secara konsisten, dan menyebut batas model partikel serta tahap pengangkatan yang terpisah.",
            },
        },
    },
    "f-use-1": {
        "bloom": "C6",
        "objective": "Menerapkan usaha, energi, dan Hukum Kekekalan Energi Mekanik untuk menyelesaikan masalah gerak nyata pada lintasan berlapis.",
        "hook": {
            "title": "Paket tiba, tetapi jangan terlalu cepat",
            "scene": "Sebuah pusat pengiriman merancang jalur luncur paket tanpa motor: menurun dari meja sortir, melewati bantalan mendatar yang kasar, lalu menuju baki penerima yang lebih tinggi. Paket harus mencapai baki dengan kelajuan yang cukup kecil. Ubah tinggi awal dan panjang bantalan; perhatikan batang energi gerak, energi potensial, serta energi internal.",
            "question": "Apakah mempertinggi meja selalu menjadi keputusan terbaik, atau justru dapat membuat paket tiba terlalu cepat?",
            "bridge": "Kita akan memilih sistem, mengikuti perubahan bentuk energi di setiap lapisan lintasan, lalu merancang tinggi atau panjang bantalan berdasarkan syarat kedatangan. Keberhasilan rancangan harus dibuktikan dengan neraca energi dan batas model.",
            "lab": _lab("energy", m=1, h0=1.5, h=.4, mu=.15, s=4, v0=0, shape="ramp", mode="friction"),
        },
        "goals": [
            "Menerapkan usaha, energi, dan Hukum Kekekalan Energi Mekanik untuk menyelesaikan masalah gerak nyata pada lintasan berlapis.",
            "Menetapkan sistem, acuan ketinggian, serta kondisi kekekalan energi mekanik.",
            "Menganalisis kelajuan dan keterjangkauan titik pada lintasan ideal maupun lintasan dengan segmen mendatar kasar.",
            "Merancang tinggi pelepasan atau panjang bantalan untuk memenuhi syarat kelajuan, lalu mengecek neraca energi dan asumsi.",
        ],
        "concepts": [
            {
                "id": "mekanik",
                "title": "Energi mekanik: satu neraca, dua bentuk",
                "question": "Ketika paket turun dan bertambah cepat, energi apa yang sebenarnya tetap?",
                "explain": [
                    "Energi mekanik adalah jumlah energi kinetik dan energi potensial yang relevan. Pada jalur luncur tanpa pegas, Em = Ek + Ep = ½mv² + mgh jika lantai menjadi acuan. Kita mengamati gerak paket dan interaksi gravitasi paket–Bumi. Kedua bentuk energi perlu dicatat pada posisi yang sama; energi potensial berkurang ketika paket turun, sementara energi kinetiknya dapat bertambah.",
                    "Pada lintasan ideal yang licin, gravitasi merupakan gaya konservatif dan gaya normal selalu tegak lurus gerak sehingga tidak melakukan usaha. Jika tidak ada motor, dorongan tambahan, atau hambatan lain, energi mekanik tetap: Em_awal = Em_akhir. Kekekalan ini tidak berarti Ek tetap atau Ep tetap secara terpisah. Batang Ek dapat naik sementara batang Ep turun dengan jumlah yang sama.",
                    "Pilih acuan ketinggian satu kali dan gunakan pada seluruh neraca. Menggeser acuan menambah konstanta pada Ep di semua titik, sehingga nilai Em numeriknya berubah dengan konstanta itu, tetapi hasil kelajuan dari neraca tidak berubah. Dalam halaman ini g = 10 m/s² dan paket dimodelkan meluncur sebagai partikel tanpa energi putaran.",
                    "Sebelum memakai tanda sama antara energi mekanik awal dan akhir, periksa gaya yang melakukan usaha. Gesekan, rem, atau motor dapat mengubah Em, sehingga harus dimasukkan sebagai usaha nonkonservatif. Hukum kekekalan energi total tetap berlaku jika bentuk lain dan pertukaran dengan lingkungan ikut dicatat; syarat untuk Em tetap lebih khusus daripada syarat energi total kekal.",
                ],
                "formula": "Em = Ek + Ep = ½ m v² + m g h; pada lintasan ideal Em_awal = Em_akhir",
                "quantities": ["Em: energi mekanik (J)", "Ek: energi kinetik translasi (J)", "Ep: energi potensial gravitasi (J)", "m: massa (kg)", "v: kelajuan (m/s)", "h: tinggi vertikal terhadap acuan (m)", "g = 10 m/s²"],
                "assumptions": ["Paket meluncur sebagai partikel; putaran diabaikan.", "Lintasan ideal licin, tanpa motor atau hambatan udara.", "Normal tegak lurus perpindahan; acuan dan g tetap."],
                "lab": _lab("energy", m=2, h0=2, h=1.2, mu=0, s=0, v0=2, shape="ramp", mode="ideal"),
                "explore": [
                    "Prediksi: ketika paket bergerak dari h0 = 2 m ke h = 1,2 m, batang energi mana yang naik dan mana yang turun?",
                    "Ubah: pertahankan m = 2 kg dan v0 = 2 m/s; turunkan hanya tinggi titik pengamatan h bertahap dari 2 m ke 0 m.",
                    "Amati: catat Ek + Ep pada tiga titik. Bandingkan pertambahan Ek dengan berkurangnya Ep, bukan hanya panjang masing-masing batang.",
                    "Jelaskan: mengapa kelajuan bertambah ketika Em tetap? Nyatakan gaya yang tidak melakukan usaha dalam model ini.",
                ],
                "misconception": {"claim": "Energi mekanik kekal berarti kelajuan benda selalu tetap.", "explain": "Yang tetap adalah jumlah Ek dan Ep. Ketika tinggi berubah, kedua suku dapat saling bertukar. Kelajuan tetap hanya terjadi jika Ek tetap, misalnya pada bagian mendatar licin tanpa perubahan energi potensial."},
                "worked": {
                    "scenario": "Paket 1,5 kg berada pada tinggi 1,2 m dan bergerak 4 m/s di jalur licin. Lantai menjadi acuan, g = 10 m/s². Tentukan energi mekaniknya pada titik itu.",
                    "steps": [
                        "Model: paket adalah partikel, dengan energi mekanik berupa energi translasi dan gravitasi; lantai menjadi acuan Ep = 0.",
                        "Data: m = 1,5 kg, h = 1,2 m, v = 4 m/s, g = 10 m/s².",
                        "Energi gerak: Ek = ½ × 1,5 × 4² = 12 J. Kelajuan dikuadratkan sebelum dikalikan massa.",
                        "Energi kedudukan: Ep = 1,5 × 10 × 1,2 = 18 J. Tinggi adalah jarak vertikal dari lantai.",
                        "Hasil: Em = Ek + Ep = 12 + 18 = 30 J; kedua bentuk dihitung pada titik yang sama.",
                        "Cek: di titik lantai pada jalur licin, Ep = 0 dan Ek = 30 J. Jumlahnya tetap 30 J meskipun pembagiannya berubah.",
                    ],
                    "result": "Em = 30 J terhadap lantai. Pada lintasan ideal, jumlah ini sama di titik lain yang dapat dicapai.",
                },
                "checks": [
                    _n("use-cp-mekanik-1", "mekanik", "Kapsul 2 kg di jalur licin berada pada tinggi 0,8 m dan bergerak 3 m/s. Acuan adalah lantai; g = 10 m/s². Berapa Em kapsul?", "Energi mekanik", 25, explain="Ek = ½ × 2 × 3² = 9 J; Ep = 2 × 10 × 0,8 = 16 J; Em = 25 J.", diagram=_lab("energy", m=2, h0=.8, h=.8, mu=0, s=0, v0=3, shape="ramp", mode="ideal")),
                    _c("use-cp-mekanik-2", "mekanik", "Paket meluncur turun pada lintasan licin tanpa motor. Pernyataan tentang energi yang tepat adalah…", ["Ek dan Ep masing-masing tetap.", "Ep berkurang, Ek bertambah, dan jumlahnya tetap.", "Em bertambah karena gravitasi bekerja."], 1, explain="Gravitasi menukar energi potensial menjadi energi kinetik. Dalam sistem paket–Bumi tanpa kerja nonkonservatif, Em tetap."),
                ],
            },
            {
                "id": "lintasan-ideal",
                "title": "Tinggi menentukan kelajuan; bentuk menentukan perjalanan",
                "question": "Dua jalur licin berbeda bentuk berakhir sama tinggi. Apakah kelajuan akhirnya berbeda?",
                "explain": [
                    "Tuliskan neraca ideal antara titik pelepasan dan titik pengamatan: ½mv0² + mgh0 = ½mv² + mgh. Setelah dibagi massa, diperoleh v² = v0² + 2g(h0 − h). Kelajuan di titik akhir ditentukan oleh kelajuan awal dan selisih tinggi vertikal. Bentuk jalur dan panjang jalur tidak muncul dalam hubungan ini jika semua syarat model ideal dipenuhi.",
                    "Massa juga saling menghilangkan. Dua paket berbeda massa dengan kelajuan awal serta tinggi awal dan akhir sama akan mempunyai kelajuan akhir sama pada jalur ideal. Namun energi dalam joule tetap lebih besar untuk paket yang massanya lebih besar. Menyamakan kelajuan tidak berarti menyamakan semua besaran energinya.",
                    "Kesamaan kelajuan akhir tidak menjamin waktu tempuh sama. Jalur yang lebih curam di awal dapat membuat benda lebih cepat memperoleh kelajuan, sehingga riwayat gerak dan waktu tiba berbeda. Model energi antara dua titik tidak langsung menentukan waktu tempuh atau besar gaya normal. Hindari menyimpulkan bahwa semua aspek gerak pasti sama hanya karena energinya sama.",
                    "Titik yang dimasukkan ke rumus harus dapat dicapai melalui seluruh lintasan. Syarat v² ≥ 0 di titik akhir saja belum cukup jika ada puncak sebelumnya yang terlalu tinggi. Tinggi maksimum ideal adalah h_max = h0 + v0²/(2g) ketika v = 0; benda dari diam tidak dapat menyeberangi puncak yang lebih tinggi dari pelepasan. Lab hanya membandingkan bentuk jalur yang tidak menambah penghalang lebih tinggi daripada energi yang tersedia.",
                ],
                "formula": "v² = v0² + 2 g (h0 − h); h_max = h0 + v0²/(2g)",
                "quantities": ["v0 dan v: kelajuan awal dan pada titik pengamatan (m/s)", "h0 dan h: tinggi awal dan titik pengamatan dari acuan sama (m)", "h_max: tinggi maksimum ideal (m)", "g = 10 m/s²"],
                "assumptions": ["Lintasan licin dan paket tetap mengikuti lintasan.", "Tidak ada motor, hambatan, atau energi rotasi.", "Setiap puncak perantara harus dapat dicapai; bentuk jalur bukan penentu waktu dari neraca dua titik saja."],
                "lab": _lab("energy", m=1, h0=1.8, h=.55, mu=0, s=0, v0=0, shape="valley", mode="ideal"),
                "explore": [
                    "Prediksi: jika tinggi awal 1,8 m dan titik akhir 0,55 m, apakah mengganti jalur ramp menjadi valley mengubah kelajuan akhir?",
                    "Ubah: pertahankan h0, h, dan v0; ubah hanya bentuk lintasan. Kemudian reset bentuk dan ubah hanya massa dari 1 ke 3 kg.",
                    "Amati: posisi jalur dapat berubah dan energi dalam joule mengikuti massa, tetapi kelajuan pada tinggi akhir yang sama tetap.",
                    "Jelaskan: bedakan pernyataan tentang kelajuan akhir, energi dalam joule, dan waktu tiba; sebutkan informasi yang belum ditentukan oleh neraca dua titik.",
                ],
                "misconception": {"claim": "Lintasan licin yang lebih panjang selalu menghasilkan kelajuan akhir lebih besar.", "explain": "Usaha gravitasi ditentukan selisih tinggi, bukan panjang lintasan. Jika titik awal, titik akhir, dan v0 sama, kelajuan akhir sama. Panjang dan bentuk masih dapat memengaruhi waktu tempuh serta gaya normal."},
                "worked": {
                    "scenario": "Dua jalur licin dengan bentuk berbeda membawa paket dari h0 = 1,8 m ke h = 0,55 m. Paket dilepas dari diam, semua puncak perantara lebih rendah dari 1,8 m, dan g = 10 m/s². Tentukan kelajuan pada ujung kedua jalur.",
                    "steps": [
                        "Model: kedua jalur ideal tanpa energi rotasi; semua puncak perantara terjangkau. Gunakan kekekalan energi mekanik.",
                        "Data dan acuan: v0 = 0, h0 = 1,8 m, h = 0,55 m, sehingga penurunan vertikal 1,25 m.",
                        "Neraca: mgh0 = ½mv² + mgh. Massa dapat dibagi dari kedua ruas.",
                        "Hitung: v² = 2 × 10 × 1,25 = 25 m²/s².",
                        "Hasil: kelajuan di ujung masing-masing jalur = √25 = 5 m/s. Bentuk jalur tidak masuk ke hasil kelajuan akhir.",
                        "Cek: energi kinetik per kilogram bertambah 12,5 J/kg, tepat sama dengan penurunan energi potensial per kilogram. Waktu tiba belum ditentukan oleh perhitungan ini.",
                    ],
                    "result": "Kedua kelajuan akhir = 5 m/s; waktu tempuh keduanya belum tentu sama.",
                },
                "checks": [
                    _n("use-cp-ideal-1", "lintasan-ideal", "Objek dilepas dari diam pada h0 = 1,8 m dan meluncur licin ke h = 1 m. Semua titik perantara terjangkau. g = 10 m/s². Berapa kelajuan akhirnya?", "Kelajuan akhir", 4, "m/s", explain="v² = 2g(h0 − h) = 20 × 0,8 = 16, jadi v = 4 m/s.", diagram=_lab("energy", m=1, h0=1.8, h=1, mu=0, s=0, v0=0, shape="wave", mode="ideal")),
                    _c("use-cp-ideal-2", "lintasan-ideal", "Dua jalur ideal mempunyai h0, h, dan v0 sama, serta semua puncaknya terjangkau. Apa yang dapat dipastikan dari neraca energi?", ["Kelajuan akhirnya sama; waktu tempuh belum tentu sama.", "Kelajuan dan waktu tempuh pasti sama.", "Jalur yang lebih panjang pasti memberi kelajuan akhir lebih tinggi."], 0, explain="Neraca menentukan kelajuan dari selisih tinggi dan v0. Waktu tempuh memerlukan riwayat gerak sepanjang lintasan."),
                ],
            },
            {
                "id": "gesekan",
                "title": "Lintasan kasar: Em berkurang, energi total tetap dicatat",
                "question": "Ke mana energi mekanik berpindah ketika paket melintasi bantalan kasar?",
                "explain": [
                    "Pada segmen mendatar kasar, gaya gesek kinetik melawan gerak. Jika tidak ada gaya vertikal tambahan dan percepatan vertikal nol, N = mg sehingga f_k = μ_kmg. Untuk panjang segmen s yang benar-benar dilalui, usaha gesek W_f = −μ_kmgs. Tanda negatif menyatakan pengurangan energi mekanik paket–Bumi. Rumus N = mg ini tidak boleh dipindahkan begitu saja ke permukaan miring.",
                    "Bila hanya gesekan yang melakukan usaha nonkonservatif, neracanya Em_akhir = Em_awal − μ_kmgs. Semua bagian menurun dan naik di luar bantalan dianggap licin. Energi kinetik pada akhir diperoleh setelah energi potensial pada tinggi akhir juga dikurangkan. Karena itu, tinggi akhir dan panjang bantalan memiliki peran berbeda dalam neraca.",
                    "Energi mekanik yang berkurang tidak lenyap. Untuk sistem yang mencakup paket, Bumi, dan bantalan, kita mencatat kenaikan energi internal ΔE_internal = μ_kmgs dalam model ini. Jumlah Ek + Ep + kenaikan energi internal tetap sama dengan energi awal, jika tidak ada transfer lain keluar sistem. Dalam proses nyata sebagian energi dapat menjadi bunyi atau deformasi; kategori internal di sini adalah penyederhanaan disipasi.",
                    "Neraca harus dihentikan ketika paket berhenti. Jika perhitungan sepanjang seluruh bantalan memberikan Ek akhir negatif, paket tidak pernah mencapai ujung yang diminta. Pada lantai mendatar, jarak henti adalah s_henti = v_masuk²/(2μ_kg). Panjang s dalam usaha gesek adalah jarak yang sudah dilalui, bukan otomatis seluruh panjang bantalan yang tersedia.",
                ],
                "formula": "W_f = −μ_k m g s; Em_akhir + ΔE_internal = Em_awal; ΔE_internal = μ_k m g s",
                "quantities": ["μ_k: koefisien gesek kinetik (tanpa satuan)", "N dan f_k: gaya normal dan gesek (N)", "s: panjang segmen mendatar kasar yang dilalui (m)", "ΔE_internal: kenaikan energi internal paket dan bantalan (J)", "Em: Ek + Ep (J)", "g = 10 m/s²"],
                "assumptions": ["Gesekan hanya di segmen mendatar dan μ_k konstan.", "Tidak ada gaya vertikal lain sehingga N = mg.", "Bagian lain licin; tidak ada motor atau hambatan udara.", "Kenaikan energi internal adalah besaran relatif, dimulai dari nol pada pelepasan."],
                "lab": _lab("energy", m=2, h0=1.6, h=.4, mu=.2, s=3, v0=0, shape="valley", mode="friction"),
                "explore": [
                    "Prediksi: jika panjang bantalan mendatar bertambah dengan koefisien tetap, apa yang terjadi pada Em akhir dan kenaikan energi internal?",
                    "Ubah: pertahankan m = 2 kg, h0 = 1,6 m, h = 0,4 m, v0 = 0, μ = 0,2; ubah hanya s dari 0 ke 3 lalu 5 m.",
                    "Amati: cocokkan penurunan batang Em dengan kenaikan batang internal. Periksa jumlah keduanya dan apakah paket masih mampu mencapai tinggi akhir.",
                    "Jelaskan: mengapa grafik Em turun tidak membuktikan energi total hilang? Nyatakan batas sistem dan lokasi permukaan kasar.",
                ],
                "misconception": {"claim": "Ketika gesekan bekerja, hukum kekekalan energi tidak berlaku.", "explain": "Energi total tetap kekal jika semua bentuk dan transfer diperhitungkan. Yang berkurang adalah energi mekanik. Perluas sistem ke paket dan bantalan untuk mencatat kenaikan energi internal, lalu periksa jumlahnya."},
                "worked": {
                    "scenario": "Paket 2 kg dilepas dari diam pada h0 = 1,6 m, melintasi bantalan mendatar kasar sepanjang 3 m dengan μ_k = 0,2, lalu sampai pada h = 0,4 m. Bagian lain licin dan tidak ada puncak penghalang. g = 10 m/s². Tentukan kelajuan di titik akhir.",
                    "steps": [
                        "Model: sistem paket–Bumi untuk Em; paket dan bantalan ikut dihitung saat mencatat energi internal. Gesekan hanya di lantai mendatar, N = mg.",
                        "Data dan acuan: m = 2 kg, v0 = 0, h0 = 1,6 m, h = 0,4 m, μ = 0,2, s = 3 m; lantai adalah acuan.",
                        "Energi awal: Em_awal = 2 × 10 × 1,6 = 32 J. Usaha gesek = −0,2 × 2 × 10 × 3 = −12 J.",
                        "Energi pada titik akhir: Em_akhir = 32 − 12 = 20 J; Ep_akhir = 2 × 10 × 0,4 = 8 J, sehingga Ek_akhir = 12 J.",
                        "Hasil: ½ × 2 × v² = 12, jadi v = √12 ≈ 3,46 m/s. Ek positif menandakan titik akhir terjangkau pada jalur tanpa puncak penghalang ini.",
                        "Cek total: Ek 12 J + Ep 8 J + kenaikan internal 12 J = 32 J, sama dengan energi awal. Em sendiri turun dari 32 J ke 20 J.",
                    ],
                    "result": "Kelajuan akhir ≈ 3,46 m/s; Em berkurang 12 J dan kenaikan energi internal = 12 J.",
                },
                "checks": [
                    _n("use-cp-gesek-1", "gesekan", "Paket 1,5 kg melintasi seluruh bantalan mendatar kasar 2 m. μ_k = 0,2, N = mg, dan g = 10 m/s². Berapa usaha gaya gesek?", "Usaha gesek", -6, explain="W_f = −μ_kmgs = −0,2 × 1,5 × 10 × 2 = −6 J. Panjang yang diberikan sudah benar-benar dilalui.", diagram=_lab("energy", m=1.5, h0=1.4, h=0, mu=.2, s=2, v0=0, shape="ramp", mode="friction")),
                    _c("use-cp-gesek-2", "gesekan", "Em paket–Bumi berkurang 7 J pada bantalan kasar. Sistem paket–Bumi–bantalan tidak menerima atau melepaskan energi lain. Pernyataan yang tepat adalah…", ["Energi total sistem berkurang 7 J.", "Energi potensial pasti bertambah 7 J.", "Energi internal sistem bertambah 7 J."], 2, explain="Dalam model disipasi ini, penurunan Em sama dengan kenaikan energi internal. Jumlah energi seluruh sistem tetap."),
                ],
            },
            {
                "id": "rancang",
                "title": "Merancang lintasan dari syarat kedatangan",
                "question": "Bagaimana memilih tinggi awal agar paket mencapai baki dengan kelajuan yang diminta?",
                "explain": [
                    "Merancang berarti bergerak dari syarat hasil menuju pilihan besaran. Tetapkan dulu massa paket, kelajuan awal, tinggi baki, koefisien dan panjang bantalan mendatar kasar, serta kelajuan yang diinginkan saat tiba. Untuk model ini, neraca per satuan massa adalah ½v0² + gh0 = ½v_tiba² + gh_baki + μ_kgs. Bentuk persamaan memperlihatkan bagian mana yang dapat diubah dan bagian mana yang merupakan syarat.",
                    "Jika yang dapat diatur adalah tinggi pelepasan, susun h0 = h_baki + (v_tiba² − v0²)/(2g) + μ_ks. Tinggi awal dipakai untuk menyediakan energi gerak akhir, ketinggian baki, dan energi yang terdisipasi di bantalan. Jika yang dapat diatur panjang bantalan, susun s = [½(v0² − v_tiba²) + g(h0 − h_baki)]/(μ_kg), untuk μ_k > 0.",
                    "Hasil rancangan perlu diuji keterjangkauannya sepanjang jalur. Tidak cukup mendapat angka di ujung: cek apakah paket dapat mencapai awal bantalan, menyeberanginya, dan naik ke baki. Nilai v² negatif menunjukkan ada segmen yang gagal dicapai, bukan kelajuan negatif. Periksa pula panjang atau tinggi pilihan masih berada dalam batas ruang yang tersedia, serta semua puncak perantara tidak membutuhkan energi melebihi yang tersisa.",
                    "Jika syaratnya kelajuan paling besar, gunakan pertidaksamaan; jika harus berada dalam rentang, periksa kedua batas. Kesamaan persis adalah model nominal, bukan jaminan rancangan nyata: koefisien gesek dan kelajuan awal dapat bervariasi. Uji beberapa nilai yang masih masuk akal dan jelaskan batasnya. Rancangan di sini adalah model belajar skala kecil, sehingga tidak menggantikan pengujian prototipe atau penilaian teknis peralatan nyata.",
                ],
                "formula": "½v0² + gh0 = ½v_tiba² + gh_baki + μ_kgs; h0 = h_baki + (v_tiba² − v0²)/(2g) + μ_ks",
                "quantities": ["h0: tinggi pelepasan yang dirancang (m)", "h_baki: tinggi tujuan terhadap lantai (m)", "v0 dan v_tiba: kelajuan awal dan saat tiba (m/s)", "μ_k: koefisien gesek kinetik bantalan (tanpa satuan)", "s: panjang bantalan mendatar kasar (m)", "g = 10 m/s²"],
                "assumptions": ["Segmen turun dan naik licin; gesekan konstan hanya pada bantalan mendatar.", "Paket meluncur tanpa putaran, deformasi besar, atau motor.", "Tidak ada puncak perantara lebih tinggi daripada yang dapat dicapai.", "Syarat kelajuan dan batas ruang harus diperiksa setelah memperoleh hasil nominal."],
                "lab": _lab("energy", m=1.5, h0=1.05, h=.4, mu=.15, s=3, v0=0, shape="valley", mode="friction"),
                "explore": [
                    "Prediksi: untuk baki 0,4 m dan bantalan 3 m dengan μ = 0,15, apakah h0 = 1,05 m memberi v_tiba = 2 m/s?",
                    "Ubah: dari rancangan nominal itu, ubah hanya h0 ke 0,95 lalu 1,15 m. Reset, kemudian ubah hanya μ menjadi 0,20.",
                    "Amati: bandingkan kelajuan tiba dengan target 2 m/s dan cek apakah energi yang tersisa cukup untuk naik ke baki. Catat bila titik akhir tidak terjangkau.",
                    "Jelaskan: tulis pilihan revisi tinggi atau panjang bantalan beserta alasan energinya. Jangan menyebut kelajuan awal dan target akhir sebagai sesuatu yang otomatis tetap ketika rancangan berubah.",
                ],
                "misconception": {"claim": "Semakin tinggi pelepasan, semakin baik rancangan lintasan.", "explain": "Tinggi lebih besar meningkatkan energi tersedia dan biasanya kelajuan tiba. Jika tujuan memiliki batas kelajuan, rancangan dapat melampauinya. Pilih tinggi berdasarkan syarat terukur lalu periksa beberapa kondisi gesekan, bukan berdasarkan kecepatan maksimum saja."},
                "worked": {
                    "scenario": "Paket dilepas dari diam. Baki tujuan berada pada h_baki = 0,4 m. Bantalan mendatar kasar panjangnya 3 m dengan μ_k = 0,15; bagian lain licin. Target kelajuan tiba 2 m/s. g = 10 m/s². Tentukan tinggi pelepasan nominal tanpa puncak penghalang.",
                    "steps": [
                        "Model dan keputusan: pilih h0 sebagai besaran rancangan. Gesekan hanya di bantalan mendatar; massa tetap dapat dibagi dari neraca.",
                        "Data dan acuan: v0 = 0, v_tiba = 2 m/s, h_baki = 0,4 m, μ = 0,15, s = 3 m; lantai adalah acuan.",
                        "Alasan energi: tinggi awal harus menyediakan energi potensial tujuan, energi gerak tujuan, serta kenaikan energi internal μmgs.",
                        "Susun dan hitung: h0 = 0,4 + (2² − 0²)/(2 × 10) + 0,15 × 3 = 0,4 + 0,2 + 0,45 = 1,05 m.",
                        "Hasil nominal: pilih pelepasan 1,05 m. Setelah bantalan, sisa energi per kilogram 10,5 − 4,5 = 6 J/kg; cukup untuk Ep tujuan 4 J/kg dan Ek tujuan 2 J/kg.",
                        "Cek dan batas: substitusi memberi v_tiba² = 20(1,05 − 0,4 − 0,45) = 4. Coba variasi μ sebelum menyatakan rancangan memenuhi rentang target; hasil nominal bukan jaminan kondisi nyata.",
                    ],
                    "result": "Tinggi awal nominal = 1,05 m untuk v_tiba = 2 m/s pada data model yang diberikan.",
                },
                "checks": [
                    _n("use-cp-rancang-1", "rancang", "Paket dilepas dari diam menuju baki setinggi 0,5 m. Bantalan mendatar kasar panjang 2 m memiliki μ_k = 0,1; bagian lain licin. Target kelajuan tiba 2 m/s, g = 10 m/s², dan tidak ada puncak penghalang. Berapa tinggi pelepasan nominal?", "Tinggi pelepasan", .9, "m", explain="h0 = h_baki + v²/(2g) + μs = 0,5 + 0,2 + 0,2 = 0,9 m.", seconds=240),
                    _c("use-cp-rancang-2", "rancang", "Rancangan nominal tepat memenuhi target kelajuan tiba. Ketika μ bantalan mendatar lebih kecil dari perkiraan dan semua data lain tetap, perubahan apa yang diprediksi?", ["Kelajuan tiba lebih kecil karena bantalan lebih licin.", "Kelajuan tiba lebih besar karena disipasi lebih sedikit.", "Kelajuan tiba tetap karena energi total kekal."], 1, explain="Disipasi μmgs berkurang; lebih banyak energi tersedia sebagai Ek pada tinggi tujuan yang sama. Kekekalan energi total tidak memaksa Ek tetap.", level="C4", seconds=240),
                ],
            },
        ],
        "prediction": [
            "Dua jalur licin berbeda bentuk menghubungkan pelepasan dan baki pada ketinggian yang sama. Kelajuan awal sama dan semua puncak terjangkau. Prediksikan hubungan kelajuan tiba dan waktu tempuh; jelaskan mana yang bisa ditentukan dari energi saja.",
            "Sebuah paket telah dirancang tiba dengan kelajuan tertentu setelah bantalan kasar mendatar. Prediksikan akibat memperpanjang bantalan, termasuk kemungkinan tidak mencapai baki. Jelaskan nasib energi mekanik yang berkurang.",
        ],
        "performance": {
            "scenario": "Rancang model jalur pengiriman untuk paket 1,5 kg yang dilepas dari diam. Baki berada 0,4 m di atas lantai. Bantalan kasar mendatar panjangnya 3 m; μ_k dapat berkisar 0,12–0,18. Bagian turun dan naik licin, tanpa puncak perantara yang melebihi tinggi pelepasan. Kelajuan tiba harus berada dalam 1–3 m/s untuk seluruh rentang μ_k. Tinggi awal dapat dipilih pada 0,8–1,4 m. Gunakan g = 10 m/s². Pilih satu tinggi yang memenuhi syarat dan buktikan pada dua batas μ_k.",
            "deliverables": [
                "Sketsa lintasan berlabel tinggi awal, lantai acuan, bantalan mendatar 3 m, dan baki 0,4 m; nyatakan model paket meluncur tanpa energi putaran.",
                "Neraca energi yang memisahkan Ek, Ep, dan kenaikan energi internal, termasuk alasan N = mg hanya pada segmen mendatar.",
                "Satu tinggi pilihan beserta perhitungan kelajuan pada μ = 0,12 dan μ = 0,18. Buktikan bahwa pilihanmu memenuhi seluruh rentang gesekan; jelaskan batas mana yang mengontrol kelajuan terbesar dan terkecil.",
                "Pemeriksaan keterjangkauan bantalan dan baki, satuan, serta batas ruang. Tunjukkan bahwa Ek tidak menjadi negatif pada segmen yang harus dilalui.",
                "Penjelasan mengapa pilihan lebih tinggi belum tentu lebih baik, serta satu usul pengujian prototipe untuk memeriksa variasi gesekan dan asumsi model.",
            ],
            "rubric": {
                "T1": "Ada sketsa atau angka tinggi, tetapi syarat target, lokasi gesekan, dan neraca energi belum digunakan dengan benar.",
                "T2": "Neraca dasar benar dan satu keadaan dihitung, tetapi belum membuktikan kedua batas μ atau masih ada kesalahan keterjangkauan, satuan, atau acuan.",
                "T3": "Memilih tinggi dalam rentang yang memenuhi, membuktikan kelajuan pada dua batas μ berada 1–3 m/s, memisahkan Em dari energi internal, serta memeriksa keterjangkauan dan batas model dengan diagram jelas.",
                "T4": "Memenuhi T3 serta menurunkan seluruh rentang tinggi yang memenuhi dari pertidaksamaan, menjelaskan batas yang mengontrol tiap sisi, dan merancang pengujian variasi yang dapat menguatkan atau merevisi model.",
            },
        },
    },
}


def make_questions(slug, stage, form=1):
    """Kembalikan soal baru: P2=8, P5=5, P7=10, P9=8, P10=4.

    Satu butir mempunyai tepat satu kunci otomatis. Answer pilihan adalah indeks
    berbasis nol. Tol adalah toleransi absolut dalam satuan yang dicantumkan.
    Diagram hanya data stimulus; runtime assessment harus menyembunyikan hasil.
    """
    if slug not in LESSONS:
        raise ValueError(f"TP tidak didukung: {slug}")
    if not isinstance(form, int) or isinstance(form, bool) or form < 1:
        raise ValueError("form harus bilangan bulat positif")
    stage = str(stage).upper()
    if stage not in {"P2", "P5", "P7", "P9", "P10"}:
        raise ValueError(f"Tahap bank tidak didukung: {stage}")
    prefix = f"{slug}-{stage}-f{form}"
    questions = []

    def n(indicator, prompt, label, answer, unit="J", **kw):
        questions.append(_n(f"{prefix}-{len(questions)+1:02d}", indicator,
                            prompt, label, answer, unit, **kw))

    def c(indicator, prompt, options, answer, **kw):
        # Posisi opsi ikut berubah menurut form tanpa mengubah makna kunci.
        shift = (form - 1) % len(options)
        arranged = options[shift:] + options[:shift]
        questions.append(_c(f"{prefix}-{len(questions)+1:02d}", indicator,
                            prompt, arranged, (answer-shift) % len(options), **kw))

    # Variasi terbatas menjaga rentang massa, tinggi, dan kelajuan tetap realistis.
    k = (form - 1) % 5
    if slug == "f-use-1-pra":
        _pra(stage, k, n, c)
    else:
        _use(stage, k, n, c)
    return questions


def _pra(stage, k, n, c):
    if stage == "P2":
        cm = 140 + 20*k
        n("satuan-panjang", f"Sebuah penggaris lintasan menunjukkan {cm} cm. Berapa panjang itu dalam meter?", "Panjang", cm/100, "m", explain=f"1 m = 100 cm, sehingga {cm}/100 = {cm/100:g} m.", level="C2", seconds=120)
        mass = 750 + 50*k
        n("satuan-massa", f"Massa sebuah wadah adalah {mass} g. Nyatakan dalam kg.", "Massa", mass/1000, "kg", explain=f"1 kg = 1000 g; massa = {mass/1000:g} kg.", level="C2", seconds=120, tol=.005)
        v = 3+k
        n("kuadrat", f"Kelajuan terukur v = {v} m/s. Berapa nilai v²?", "Kuadrat kelajuan", v*v, "m²/s²", explain=f"v² = {v} × {v} = {v*v} m²/s².", level="C2", seconds=120)
        c("arah-gaya", "Sebuah benda berpindah mendatar ke timur. Gaya yang tegak lurus perpindahan adalah…", ["Gaya ke timur.", "Gaya vertikal ke atas.", "Gaya ke barat."], 1, explain="Sudut antara arah mendatar dan vertikal adalah 90°. Gaya ke barat justru berlawanan arah, 180°.")
        c("komponen", "Suatu gaya membentuk sudut 60° terhadap arah mendatar. cos 60° = 0,5. Berapa bagian besar gaya yang merupakan komponen mendatar?", ["Seluruh besar gaya.", "Setengah besar gaya.", "Dua kali besar gaya."], 1, explain="Komponen sejajar mendatar adalah F cos 60° = 0,5F.")
        e0, e1 = 11+2*k, 27+3*k
        n("selisih", f"Sebuah pembacaan energi berubah dari {e0} J menjadi {e1} J. Hitung perubahan akhir dikurangi awal.", "Perubahan energi", e1-e0, explain=f"Perubahan = {e1} − {e0} = {e1-e0} J.", level="C2", seconds=120)
        c("tinggi-vertikal", "Papan miring panjangnya 2 m; ujung atasnya 0,7 m di atas ujung bawah. Besaran yang menyatakan kenaikan vertikal adalah…", ["2 m.", "2,7 m.", "0,7 m."], 2, explain="Kenaikan vertikal adalah selisih posisi ke atas, bukan panjang papan yang dilalui.")
        c("kelajuan-arah", "Dua objek memiliki besar kecepatan 4 m/s, satu ke kiri dan satu ke kanan. Pernyataan tentang kelajuannya adalah…", ["Keduanya berkelajuan sama.", "Objek ke kiri berkelajuan negatif.", "Kelajuan keduanya tidak dapat dibandingkan."], 0, explain="Kelajuan adalah besar kecepatan dan tidak memuat tanda arah.")
    elif stage == "P5":
        F, s = 22+2*k, 1.5
        n("usaha", f"Rak alat didorong gaya {F} N searah perpindahan {s} m. Berapa usaha dorongan?", "Usaha dorongan", F*s, explain=f"Sudut 0°; W = Fs = {F} × {s} = {F*s:g} J.", diagram=_lab("work", F=F, s=s, theta=0))
        c("usaha", "Layar menunjukkan perpindahan mendatar dan gaya vertikal. Apa usaha gaya vertikal itu?", ["Positif karena gaya tidak nol.", "Nol karena gaya tegak lurus perpindahan.", "Negatif karena arah berbeda."], 1, explain="θ = 90°, cos θ = 0, sehingga W = 0.", diagram=_lab("work", F=20, s=2, theta=90))
        m, v = 1+.2*k, 4
        n("kinetik", f"Wadah bermassa {m:g} kg bergerak {v} m/s terhadap lantai. Berapa energi kinetiknya?", "Energi kinetik", .5*m*v*v, explain=f"Ek = ½mv² = 0,5 × {m:g} × 16 = {.5*m*v*v:g} J.", diagram=_lab("kinetic", m=m, v=v))
        h = 1.4+.2*k
        n("potensial", f"Objek 2 kg berada pada h = {h:g} m. Acuan Ep = 0 berada pada h_ref = 0,4 m. g = 10 m/s². Berapa Ep objek?", "Energi potensial", 20*(h-.4), explain=f"Tinggi relatif = {h:g} − 0,4 = {h-.4:g} m; Ep = 2 × 10 × {h-.4:g} = {20*(h-.4):g} J.", diagram=_lab("potential", m=2, h=h, ref=.4))
        w1,w2 = 26+2*k, -10-k
        n("usaha-neto", f"Pada perpindahan mendatar, dorongan melakukan usaha +{w1} J dan gesekan {w2} J. Usaha gaya lain nol. Berapa perubahan energi kinetik benda?", "Perubahan energi kinetik", w1+w2, explain=f"ΔEk = W_net = {w1} + ({w2}) = {w1+w2} J. Gunakan jumlah usaha, bukan usaha dorongan saja.", seconds=240)
    elif stage == "P7":
        c("usaha", "Petugas menekan tutup wadah yang tidak berpindah selama penekanan. Ditinjau selama tidak ada perpindahan, usaha gaya tekan pada tutup adalah…", ["Nol.", "Positif selama petugas menekan.", "Negatif karena tutup diam."], 0, explain="Perpindahan tutup nol, sehingga W = Fs cos θ = 0. Kelelahan petugas bukan ukuran usaha pada tutup.")
        F=28+2*k
        n("usaha", f"Rel kamera mendapat tarikan {F} N pada sudut 60° terhadap perpindahan mendatar 2,5 m. cos 60° = 0,5. Berapa usaha tarikan?", "Usaha tarikan", F*1.25, explain=f"W = {F} × 2,5 × 0,5 = {F*1.25:g} J.", diagram=_lab("work", F=F, s=2.5, theta=60))
        f=7+k
        n("usaha", f"Baki bergeser 3 m ke kanan, sementara gaya gesek tetap {f} N ke kiri. Berapa usaha gaya gesek?", "Usaha gesek", -3*f, explain=f"θ = 180°; W_f = −fs = −{f} × 3 = {-3*f} J.", diagram=_lab("work", F=f, s=3, theta=180))
        m=.5+.1*k
        n("kinetik", f"Kantong bibit {m:g} kg meluncur dengan kelajuan 6 m/s. Berapa Ek translasi kantong terhadap lantai?", "Energi kinetik", .5*m*36, explain=f"Ek = ½ × {m:g} × 6² = {18*m:g} J.", diagram=_lab("kinetic", m=m, v=6))
        c("kinetik", "Sebuah alat penghantar mengganti wadah dengan massa dua kali semula, tetapi kelajuannya menjadi setengah semula. Dibanding sebelumnya, energi kinetiknya menjadi…", ["Setengah.", "Sama.", "Dua kali."], 0, explain="Faktor Ek = 2 × (½)² = ½.", level="C4", seconds=240)
        h=1.7+.1*k
        n("potensial", f"Pot tanaman 1,4 kg berada {h:g} m di atas lantai yang menjadi acuan. g = 10 m/s². Berapa energi potensialnya?", "Energi potensial", 14*h, explain=f"Ep = mgh = 1,4 × 10 × {h:g} = {14*h:g} J.", diagram=_lab("potential", m=1.4, h=h, ref=0))
        c("potensial", "Acuan energi potensial diganti dari lantai ke meja, sedangkan dua posisi objek tetap. Apa akibatnya pada ΔEp antara kedua posisi?", ["ΔEp bertambah sebesar tinggi meja.", "ΔEp tetap sama.", "ΔEp selalu menjadi nol."], 1, explain="Perubahan acuan menambah konstanta pada kedua nilai Ep. Konstanta saling menghilangkan dalam selisihnya.", seconds=180)
        e0,e1=13+k,31+2*k
        n("usaha-neto", f"Energi kinetik penggeser pajangan naik dari {e0} J ke {e1} J. Berapa usaha neto selama proses itu?", "Usaha neto", e1-e0, explain=f"W_net = ΔEk = {e1} − {e0} = {e1-e0} J.", level="C2", seconds=120)
        c("usaha-neto", "Wadah meluncur mendatar dengan kelajuan tetap. Dorongan melakukan +15 J, berat dan normal melakukan nol usaha. Berapa usaha gesekan dalam proses itu?", ["0 J.", "+15 J.", "−15 J."], 2, explain="Kelajuan tetap memberi ΔEk = 0. Maka W_gesek harus −15 J agar jumlah usaha nol.", level="C4", seconds=240)
        v0=2+k
        W=9+2*k
        vf=sqrt(v0*v0+W)
        n("usaha-neto", f"Penggeser 2 kg mula-mula bergerak {v0} m/s. Gaya neto 3 N searah gerak bekerja sepanjang {W/3:g} m. Berapa kelajuan akhirnya?", "Kelajuan akhir", vf, "m/s", explain=f"Ek_awal = {v0*v0} J dan W_net = {W} J. Ek_akhir = {v0*v0+W} J = ½ × 2 × v², sehingga v = √{v0*v0+W} ≈ {vf:.2f} m/s.", seconds=240, diagram=_lab("workenergy", F=3, s=W/3, m=2, v0=v0))
    elif stage == "P9":
        # Konteks baru: layanan pengembalian buku, pemindai bagasi, serta lift sampel.
        F=34+2*k
        n("usaha", f"Di stasiun pengembalian buku, lengan pendorong memberi gaya {F} N pada sudut 60° terhadap perpindahan mendatar buku 1,2 m. cos 60° = 0,5. Berapa usaha lengan?", "Usaha lengan", F*.6, explain=f"W = Fs cos θ = {F} × 1,2 × 0,5 = {F*.6:g} J.", diagram=_lab("work", F=F, s=1.2, theta=60))
        c("usaha", "Di pemindai bandara, gaya penopang vertikal bekerja pada bagasi yang bergeser mendatar tanpa naik atau turun. Usaha gaya penopang adalah…", ["Positif karena menopang berat.", "Negatif karena melawan gravitasi.", "Nol karena tegak lurus perpindahan."], 2, explain="Usaha harus ditentukan dari arah gaya terhadap perpindahan. Komponen penopang sepanjang perpindahan mendatar nol.")
        m,v=.7+.1*k,7
        n("kinetik", f"Kapsul sampel bermassa {m:g} kg bergerak dengan kelajuan 7 m/s terhadap laboratorium. Berapa energi kinetiknya?", "Energi kinetik", .5*m*v*v, explain=f"Ek = ½ × {m:g} × 7² = {.5*m*v*v:g} J.", diagram=_lab("kinetic", m=m, v=v))
        c("kinetik", "Mesin pengemas membuat massa isi suatu kantong tetap, tetapi kelajuannya naik dari 1,5 m/s ke 4,5 m/s. Perbandingan Ek akhir terhadap awal adalah…", ["3 : 1.", "9 : 1.", "1 : 3."], 1, explain="Kelajuan menjadi tiga kali, sehingga energi kinetik menjadi sembilan kali.", seconds=180)
        h=2.6+.1*k
        ep=16*(h-.6)
        n("potensial", f"Dalam lift sampel, wadah 1,6 kg berada pada h = {h:g} m. Acuan Ep = 0 berada pada h_ref = 0,6 m. g = 10 m/s². Berapa energi potensial wadah terhadap acuan itu?", "Energi potensial", ep, explain=f"Ep = mg(h − h_ref) = 1,6 × 10 × ({h:g} − 0,6) = {ep:g} J.", diagram=_lab("potential", m=1.6, h=h, ref=.6))
        c("potensial", "Sampel berada 0,3 m di bawah garis acuan Ep = 0. Pernyataan yang benar adalah…", ["Ep sampel negatif terhadap acuan itu.", "Massa sampel harus negatif.", "Sampel tidak mengalami gravitasi."], 0, explain="Tinggi relatif bernilai negatif dan m serta g positif, sehingga Ep negatif. Nol Ep dipilih, bukan batas bawah mutlak energi potensial.")
        e0,e1=42+3*k,17+k
        n("usaha-neto", f"Sistem pengerem jalur arsip menurunkan Ek suatu benda dari {e0} J menjadi {e1} J. Berapa usaha neto pada benda?", "Usaha neto", e1-e0, explain=f"W_net = Ek_akhir − Ek_awal = {e1} − {e0} = {e1-e0} J. Tanda negatif sesuai perlambatan.", seconds=180)
        pull,brake=38+2*k,11+k
        n("usaha-neto", f"Robot pemindah botol melakukan usaha +{pull} J pada satu botol. Gaya hambat melakukan −{brake} J; semua gaya lain melakukan nol usaha. Berapa pertambahan Ek botol?", "Pertambahan energi kinetik", pull-brake, explain=f"ΔEk = W_net = {pull} − {brake} = {pull-brake} J.", level="C4", seconds=240)
    else:  # P10: recall setelah jeda, ringkas dan bervariasi.
        F,s=19+2*k,2.2
        n("usaha", f"Pada jalur pengeringan, klip digerakkan gaya tetap {F} N searah perpindahan {s} m. Berapa usaha gaya itu?", "Usaha", F*s, explain=f"W = Fs = {F} × {s} = {F*s:g} J.", diagram=_lab("work", F=F, s=s, theta=0))
        c("kinetik", "Massa benda tetap, sedangkan kelajuannya dikurangi menjadi setengah. Energi kinetiknya menjadi…", ["Setengah semula.", "Seperempat semula.", "Dua kali semula."], 1, explain="Ek sebanding v², sehingga faktor energinya (½)² = ¼.")
        m,dh=1.1+.1*k,.9
        n("potensial", f"Kotak kecil {m:g} kg dinaikkan vertikal {dh} m. Acuan tetap, g = 10 m/s². Berapa perubahan energi potensialnya?", "Perubahan Ep", m*10*dh, explain=f"ΔEp = mgΔh = {m:g} × 10 × {dh} = {m*10*dh:g} J. Positif karena dinaikkan.")
        c("usaha-neto", "Energi kinetik benda pada akhir proses sama dengan pada awal. Kesimpulan yang pasti adalah…", ["Semua gaya pada benda nol.", "Benda selalu diam selama proses.", "Usaha neto selama proses nol."], 2, explain="W_net = ΔEk = 0. Gaya atau usaha per gaya dapat tidak nol dan saling meniadakan.", seconds=180)


def _use(stage, k, n, c):
    if stage == "P2":
        F=14+2*k
        n("usaha", f"Gaya mendatar {F} N searah gerak bekerja sepanjang 0,8 m. Berapa usaha gaya itu?", "Usaha", .8*F, explain=f"W = Fs = {F} × 0,8 = {.8*F:g} J.", diagram=_lab("work", F=F, s=.8, theta=0))
        m,v=1+.2*k,3
        n("kinetik", f"Benda {m:g} kg bergerak 3 m/s. Berapa energi kinetiknya?", "Ek", .5*m*v*v, explain=f"Ek = ½ × {m:g} × 9 = {4.5*m:g} J.", diagram=_lab("kinetic", m=m, v=v))
        h=1.3+.1*k
        n("potensial", f"Benda 2 kg berada {h:g} m di atas lantai acuan. g = 10 m/s². Berapa energi potensialnya?", "Ep", 20*h, explain=f"Ep = mgh = 2 × 10 × {h:g} = {20*h:g} J.", diagram=_lab("potential", m=2, h=h, ref=0))
        c("acuan", "Ketika menghitung perubahan Ep antara dua posisi, acuan ketinggian harus…", ["Diubah pada tiap posisi agar Ep selalu nol.", "Konsisten pada kedua posisi.", "Selalu berada di titik tertinggi."], 1, explain="Acuan boleh dipilih bebas, tetapi harus dipakai konsisten pada kedua keadaan.")
        e0,e1=8+k,23+2*k
        n("usaha-neto", f"Ek benda berubah dari {e0} J ke {e1} J. Berapa usaha neto?", "Usaha neto", e1-e0, explain=f"W_net = ΔEk = {e1} − {e0} = {e1-e0} J.", level="C2", seconds=120)
        c("tanda-gesek", "Objek meluncur ke kanan di lantai kasar. Gaya gesek ke kiri melakukan usaha…", ["Positif.", "Nol.", "Negatif."], 2, explain="Sudut gaya terhadap perpindahan 180°, sehingga usaha gesekan negatif.")
        x=9+7*k
        n("akar", f"Hasil neraca memberi v² = {x} m²/s². Berapa kelajuan v?", "Kelajuan", sqrt(x), "m/s", explain=f"Kelajuan adalah akar positif: v = √{x} ≈ {sqrt(x):.2f} m/s.", level="C2", seconds=120)
        c("tinggi", "Sebuah jalur miring panjangnya 3 m, tetapi ujungnya hanya turun 0,9 m secara vertikal. Untuk mgΔh, besar penurunan tinggi yang dipakai adalah…", ["0,9 m.", "3 m.", "3,9 m."], 0, explain="Perubahan energi potensial bergantung pada selisih tinggi vertikal, bukan panjang jalur.")
    elif stage == "P5":
        m,h,v=1+.2*k,1.1,2
        em=m*10*h+.5*m*v*v
        n("mekanik", f"Kapsul {m:g} kg berada pada tinggi {h} m dan bergerak {v} m/s. Lantai menjadi acuan, g = 10 m/s². Berapa energi mekaniknya?", "Em", em, explain=f"Em = mgh + ½mv² = {11*m:g} + {2*m:g} = {em:g} J.", diagram=_lab("energy", m=m, h0=h, h=h, mu=0, s=0, v0=v, shape="ramp", mode="ideal"))
        drop=.45+.1*k
        vf=sqrt(4+20*drop)
        n("lintasan-ideal", f"Sebuah objek masuk jalur licin dengan kelajuan 2 m/s lalu turun vertikal {drop:g} m. Tidak ada puncak penghalang. g = 10 m/s². Berapa kelajuan akhirnya?", "Kelajuan akhir", vf, "m/s", explain=f"v² = v0² + 2gΔh = 4 + {20*drop:g} = {4+20*drop:g}; v ≈ {vf:.2f} m/s.", diagram=_lab("energy", m=1, h0=1+drop, h=1, mu=0, s=0, v0=2, shape="ramp", mode="ideal"))
        c("lintasan-ideal", "Dua paket berbeda massa dilepas dengan v0 sama dari h0 sama. Pada jalur ideal yang terjangkau, kelajuan pada tinggi akhir sama adalah…", ["Sama untuk keduanya.", "Lebih besar untuk paket berat.", "Lebih besar untuk paket ringan."], 0, explain="Massa membagi semua suku neraca. Kelajuan akhir bergantung pada v0 dan selisih tinggi, bukan massa.")
        s=2+.5*k
        w=-.2*1.2*10*s
        n("gesekan", f"Paket 1,2 kg melewati seluruh segmen mendatar kasar sepanjang {s:g} m. μ_k = 0,2 dan N = mg. g = 10 m/s². Berapa usaha gesekan?", "Usaha gesek", w, explain=f"W_f = −μmgs = −0,2 × 1,2 × 10 × {s:g} = {w:g} J.", diagram=_lab("energy", m=1.2, h0=2, h=0, mu=.2, s=s, v0=0, shape="ramp", mode="friction"))
        target=2+.5*k
        h0=.3+target*target/20+.12*2.5
        n("rancang", f"Paket dilepas dari diam menuju baki setinggi 0,3 m dengan target kelajuan {target:g} m/s. Bantalan mendatar kasar panjang 2,5 m memiliki μ_k = 0,12; bagian lain licin dan tidak ada puncak penghalang. g = 10 m/s². Berapa tinggi awal nominal?", "Tinggi awal", h0, "m", explain=f"h0 = h_baki + v²/(2g) + μs = 0,3 + {target*target/20:g} + 0,3 = {h0:g} m.", level="C4", seconds=300)
    elif stage == "P7":
        c("mekanik", "Pada model gelang peluncur di kawat licin tanpa motor, gelang turun. Pernyataan yang tepat adalah…", ["Em tetap, tetapi Ek dapat bertambah.", "Ek tetap karena lintasan licin.", "Ep tetap karena massa tetap."], 0, explain="Pada gerak turun, Ep berkurang dan Ek bertambah dengan jumlah Em tetap.")
        m,v,h=1.4+.2*k,3,.9
        em=.5*m*v*v+m*10*h
        n("mekanik", f"Slider pajangan bermassa {m:g} kg bergerak {v} m/s pada tinggi {h} m terhadap lantai. g = 10 m/s². Berapa Em slider?", "Energi mekanik", em, explain=f"Ek = {4.5*m:g} J; Ep = {9*m:g} J; Em = {em:g} J.", diagram=_lab("energy", m=m, h0=h, h=h, mu=0, s=0, v0=v, shape="ramp", mode="ideal"))
        drop=.8+.15*k
        vf=sqrt(20*drop)
        n("lintasan-ideal", f"Manik dilepas dari diam pada jalur licin dan turun vertikal {drop:g} m menuju ujung. Seluruh jalur terjangkau. g = 10 m/s². Berapa kelajuan di ujung?", "Kelajuan akhir", vf, "m/s", explain=f"v² = 2gΔh = {20*drop:g}, sehingga v ≈ {vf:.2f} m/s.", diagram=_lab("energy", m=.2, h0=drop+.2, h=.2, mu=0, s=0, v0=0, shape="valley", mode="ideal"))
        c("lintasan-ideal", "Dua jalur licin berbentuk lengkung berbeda mempunyai h0, h, dan v0 sama, tanpa puncak penghalang. Apa simpulan yang tepat?", ["Jalur pendek memberi kelajuan akhir lebih besar.", "Kelajuan akhir sama, tetapi waktu tiba dapat berbeda.", "Waktu tiba sama, tetapi kelajuan akhir dapat berbeda."], 1, explain="Energi menentukan kelajuan dari dua tinggi dan v0. Waktu tempuh bergantung pada gerak sepanjang bentuk lintasan.", seconds=180)
        dh=.2+.05*k
        vmax=sqrt(20*dh)
        n("lintasan-ideal", f"Slider di h0 = 0,7 m harus mencapai puncak licin setinggi {0.7+dh:g} m dengan kelajuan tepat nol di puncak. Tidak ada hambatan atau puncak lain. g = 10 m/s². Berapa kelajuan minimum awal yang diperlukan?", "Kelajuan awal minimum", vmax, "m/s", explain=f"½mv0² = mgΔh, sehingga v0 = √(20 × {dh:g}) ≈ {vmax:.2f} m/s. Nol di puncak adalah batas keterjangkauan, bukan syarat menyeberang dengan kelajuan positif.", level="C4", seconds=240)
        m,s=1.8+.2*k,1.5
        thermal=.16*m*10*s
        n("gesekan", f"Baki komponen {m:g} kg melintasi seluruh alas mendatar kasar {s} m dengan μ_k = 0,16 dan N = mg. g = 10 m/s². Dalam model tanpa disipasi lain, berapa kenaikan energi internal baki dan alas?", "Kenaikan energi internal", thermal, explain=f"ΔE_internal = μmgs = 0,16 × {m:g} × 10 × 1,5 = {thermal:g} J.", diagram=_lab("energy", m=m, h0=1.5, h=0, mu=.16, s=s, v0=0, shape="ramp", mode="friction"))
        c("gesekan", "Sebuah objek–Bumi memiliki Em awal 32 J dan Em akhir 23 J setelah alas kasar. Sistem mencakup alas dan tidak bertukar energi lain dengan lingkungan. Apa yang terjadi?", ["Energi total hilang 9 J.", "Energi internal bertambah 9 J.", "Energi internal berkurang 9 J."], 1, explain="Penurunan Em sebesar 9 J dicatat sebagai kenaikan energi internal, sehingga energi total tetap.", seconds=180)
        mu=.2
        v=3+.5*k
        stop=v*v/(20*mu)
        n("gesekan", f"Keranjang sampel masuk lantai mendatar kasar dengan kelajuan {v:g} m/s. μ_k = 0,2, N = mg, g = 10 m/s². Tidak ada gaya pendorong. Berapa jarak sampai berhenti?", "Jarak henti", stop, "m", explain=f"½mv² = μmgs_henti; s_henti = {v:g}²/(2 × 0,2 × 10) = {stop:g} m.", level="C4", seconds=240)
        target=1.5+.25*k
        initial=.5+.15*2+target*target/20
        n("rancang", f"Rancang tinggi pelepasan dari diam untuk pembawa kartu menuju rak 0,5 m dengan kelajuan tiba {target:g} m/s. Pembawa melewati bantalan mendatar 2 m dengan μ_k = 0,15; bagian lain licin dan semua puncak terjangkau. g = 10 m/s². Berapa tinggi awal nominal?", "Tinggi awal", initial, "m", explain=f"h0 = 0,5 + 0,15 × 2 + {target:g}²/20 = {initial:g} m.", level="C4", seconds=300)
        c("rancang", "Model penghantar suku cadang tepat memenuhi target kelajuan tiba pada μ tertentu. Panjang bantalan ditambah, sedangkan tinggi, μ, dan v0 tetap. Selama tujuan masih terjangkau, kelajuan tiba akan…", ["Naik karena jalur lebih panjang.", "Tetap karena massa tetap.", "Turun karena disipasi lebih besar."], 2, explain="Usaha gesekan bertambah besar negatif seiring panjang bantalan. Pada tinggi tujuan sama, energi kinetik dan kelajuan tiba berkurang.", level="C4", seconds=240)
    elif stage == "P9":
        # Konteks P9 mandiri: jalur obat, alat inspeksi, wahana mini, dan kapsul pos.
        m,h,v=2.3+.1*k,1.3,2.5
        em=m*(13+.5*v*v)
        n("mekanik", f"Wadah obat {m:g} kg berada pada h = 1,3 m dan bergerak 2,5 m/s di jalur klinik. Acuan adalah lantai dan g = 10 m/s². Berapa energi mekaniknya?", "Energi mekanik", em, explain=f"Em = m(gh + ½v²) = {m:g}(13 + 3,125) = {em:g} J.", diagram=_lab("energy", m=m, h0=h, h=h, mu=0, s=0, v0=v, shape="ramp", mode="ideal"))
        d=.55+.1*k
        vf=sqrt(2.5**2+20*d)
        n("lintasan-ideal", f"Kepala inspeksi meluncur licin dengan kelajuan awal 2,5 m/s lalu turun vertikal {d:g} m. Seluruh jalur dapat diikuti tanpa puncak penghalang. g = 10 m/s². Berapa kelajuan akhirnya?", "Kelajuan akhir", vf, "m/s", explain=f"v² = 2,5² + 20 × {d:g} = {6.25+20*d:g}; v ≈ {vf:.2f} m/s.", diagram=_lab("energy", m=.9, h0=d+.65, h=.65, mu=0, s=0, v0=2.5, shape="wave", mode="ideal"))
        c("lintasan-ideal", "Wahana mini ideal menghubungkan dua titik pada tinggi sama dengan kelajuan awal sama melalui dua jalur berbeda. Keduanya terjangkau. Pengelola mengklaim waktu tiba pasti sama karena kelajuan akhirnya sama. Penilaian yang tepat adalah…", ["Benar; kelajuan akhir menentukan seluruh waktu perjalanan.", "Keliru; energi dua titik tidak menentukan riwayat kelajuan sepanjang jalur.", "Keliru; jalur panjang selalu memberi kelajuan akhir lebih besar."], 1, explain="Dua jalur dapat memberi kelajuan akhir sama, tetapi kelajuan pada bagian-bagian sebelumnya serta panjang lintasan berbeda. Waktu tempuh memerlukan informasi gerak lebih lanjut.", level="C4", seconds=240)
        # Puncak tidak terjangkau: data akhir di bawah awal saja tidak cukup.
        h0=1.25+.05*k
        peak=h0+.2
        c("lintasan-ideal", f"Kapsul pos dilepas dari diam pada h0 = {h0:g} m di lintasan licin. Sebelum tujuan pada h = 0,2 m, ada puncak setinggi {peak:g} m. Tidak ada motor. Apa yang terjadi menurut model energi?", ["Pasti sampai tujuan karena tujuan lebih rendah.", "Berhenti sebelum puncak; tujuan tidak dapat dicapai lewat jalur itu.", "Melewati puncak dengan Ek negatif."], 1, explain=f"Tinggi maksimum dari diam adalah {h0:g} m. Puncak {peak:g} m lebih tinggi, sehingga tidak terjangkau. Ek negatif bukan keadaan fisik.", level="C4", seconds=240)
        mu,s,m=.18,2.7+.2*k,2.1
        lost=mu*m*10*s
        n("gesekan", f"Paket alat diagnostik {m} kg melewati seluruh bantalan mendatar {s:g} m. μ_k = 0,18, N = mg, dan g = 10 m/s². Berapa besar kenaikan energi internal paket dan bantalan jika tidak ada transfer lain?", "Kenaikan energi internal", lost, explain=f"ΔE_internal = μmgs = 0,18 × 2,1 × 10 × {s:g} = {lost:g} J.", diagram=_lab("energy", m=m, h0=1.85, h=0, mu=mu, s=s, v0=0, shape="ramp", mode="friction"))
        # Neraca lintasan berlapis yang berbeda nilai dari latihan.
        H=1.75+.1*k
        mu,s,h=.14,3.5,.35
        v2=20*(H-h-mu*s)
        n("gesekan", f"Kotak suku alat ukur dilepas dari diam pada tinggi {H:g} m. Ia melewati lantai mendatar kasar 3,5 m dengan μ_k = 0,14, lalu naik licin ke h = 0,35 m. Bagian lain licin dan tidak ada puncak penghalang. N = mg di lantai kasar, g = 10 m/s². Berapa kelajuan di titik akhir?", "Kelajuan akhir", sqrt(v2), "m/s", explain=f"v² = 2g(h0 − h − μs) = 20({H:g} − 0,35 − 0,49) = {v2:g}; v ≈ {sqrt(v2):.2f} m/s.", level="C4", seconds=300, diagram=_lab("energy", m=1.7, h0=H, h=h, mu=mu, s=s, v0=0, shape="valley", mode="friction"))
        # Balik masalah: cari panjang, bukan tinggi seperti pada P7.
        h0,h,v0,target,mu=1.65+.05*k,.45,0,2.5,.16
        length=(10*(h0-h)-.5*target*target)/(mu*10)
        n("rancang", f"Sebuah pembawa dokumen dilepas dari diam pada h0 = {h0:g} m menuju kotak penerima h = 0,45 m. Target kelajuan tiba 2,5 m/s. Rancang panjang bantalan mendatar dengan μ_k = 0,16; bagian lain licin tanpa puncak penghalang. g = 10 m/s². Berapa panjang bantalan nominal?", "Panjang bantalan", length, "m", explain=f"μgs = g(h0 − h) − ½v_tiba². s = [10({h0:g} − 0,45) − 3,125]/1,6 = {length:g} m. Energi sisa positif dan cukup untuk tinggi tujuan.", level="C4", seconds=300)
        c("rancang", "Jalur pengantar kemasan dirancang tepat pada batas maksimum kelajuan tiba. Ternyata μ aktual pada bantalan mendatar lebih kecil dari perkiraan, sementara tinggi dan panjang tetap. Apa simpulan yang paling tepat?", ["Target batas maksimum pasti lebih aman karena gesekan mengecil.", "Target kelajuan tidak dipengaruhi μ karena energi total kekal.", "Kelajuan tiba naik; tinggi atau panjang bantalan perlu diperiksa ulang."], 2, explain="Gesekan lebih kecil mengurangi kenaikan energi internal. Pada tinggi akhir sama, energi kinetik bertambah sehingga batas maksimum dapat terlampaui.", level="C4", seconds=240)
    else:  # P10
        c("mekanik", "Pada bagian mendatar licin tanpa motor, bagaimana Ek, Ep, dan Em benda yang tetap meluncur?", ["Ek tetap, Ep tetap, Em tetap.", "Ek naik, Ep turun, Em tetap.", "Ek turun, Ep tetap, Em turun."], 0, explain="Tinggi tetap memberi Ep tetap. Tidak ada usaha nonkonservatif, sehingga Em dan Ek juga tetap.")
        hmax=.95+.1*k+2.8**2/20
        n("lintasan-ideal", f"Sebuah peluncur berada pada h = {.95+.1*k:g} m dengan kelajuan 2,8 m/s dan kemudian menanjak licin. g = 10 m/s². Berapa tinggi maksimum yang dapat dicapai terhadap acuan semula?", "Tinggi maksimum", hmax, "m", explain=f"Di puncak v = 0. h_max = h + v²/(2g) = {.95+.1*k:g} + 7,84/20 = {hmax:g} m.", seconds=240)
        m,s,mu=1.3,2.4+.2*k,.125
        end=28-mu*m*10*s
        n("gesekan", f"Sebuah objek–Bumi mempunyai Em awal 28 J. Objek bermassa 1,3 kg melintasi seluruh segmen mendatar kasar {s:g} m dengan μ_k = 0,125; N = mg dan g = 10 m/s². Berapa Em setelah segmen itu?", "Em akhir", end, explain=f"ΔE_internal = μmgs = {mu*m*10*s:g} J; Em_akhir = 28 − {mu*m*10*s:g} = {end:g} J.", seconds=240)
        c("rancang", "Paket direncanakan tiba dalam rentang kelajuan tertentu, tetapi koefisien gesek bantalan memiliki rentang ketidakpastian. Pemeriksaan rancangan yang paling tepat adalah…", ["Menghitung hanya nilai tengah μ.", "Menguji kedua batas μ dan memastikan tujuan tetap terjangkau.", "Mengabaikan μ karena massa saling menghilangkan."], 1, explain="Untuk model ini v_tiba² menurun saat μ meningkat. Dua batas μ menguji kelajuan terbesar dan terkecil, sekaligus kemungkinan paket tidak sampai.", level="C4", seconds=240)
