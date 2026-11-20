# -*- coding: utf-8 -*-
"""Materi mandiri dan bank baru F.MEK.1-pra / F.MEK.2.

Tujuan mengikuti metadata konten/f-mek/<tp>/tp.json. Bank P2 hanya menguji bekal;
P5/P7/P9/P10 menguji materi TP. Diagram penilaian berisi data awal saja.
Tidak ada skrip referensi HTML yang dijalankan untuk menyusun sumber ini.
"""

from copy import deepcopy
from math import cos, sin, radians, hypot


def _lab(kind, **params):
    return {"kind": kind, "params": params}


def _n(qid, indicator, prompt, label, answer, unit="", *, level="C3",
       seconds=180, explain="", diagram=None, tol=0.06, steps=None):
    q = dict(id=qid, indicator=indicator, prompt=prompt, kind="num",
             label=label, unit=unit, answer=round(float(answer), 6), tol=tol,
             explain=explain, level=level, seconds=max(seconds, {"C1":120,"C2":120,"C3":180,"C4":240,"C5":300,"C6":300}.get(level,120)))
    if diagram is not None:
        q["diagram"] = diagram
    if steps is not None:
        q["steps"] = steps
    return q


def _c(qid, indicator, prompt, options, answer, explain, *, level="C2",
       seconds=120, diagram=None, form=1):
    # Putaran opsi mempertahankan tepat satu kunci dan membedakan bentuk tes.
    shift = (int(form) - 1) % len(options)
    rotated = list(options[shift:]) + list(options[:shift])
    q = dict(id=qid, indicator=indicator, prompt=prompt, kind="choice",
             label="Pilih satu jawaban", unit="", options=rotated,
             answer=(answer - shift) % len(options), tol=0,
             explain=explain, level=level, seconds=max(seconds, {"C1":120,"C2":120,"C3":180,"C4":240,"C5":300,"C6":300}.get(level,120)))
    if diagram is not None:
        q["diagram"] = diagram
    return q


LESSONS = {
    "f-mek-1-pra": {
        "hook": {
            "title": "Robot pengantar: meter perjalanan atau panah menuju tujuan?",
            "scene": "Robot membawa sensor dari lemari alat ke meja praktikum. Ia maju 6 m ke timur, lalu 8 m ke utara untuk menghindari meja panjang. Petugas lain perlu mengirim robot kedua langsung dari lemari menuju titik akhir itu. Layar peta menampilkan dua ruas rute dan satu panah penghubung titik awal–akhir.",
            "question": "Apakah robot kedua harus menempuh 14 m juga? Geser satu ruas rute dan perhatikan apa yang berubah pada panah menuju tujuan.",
            "bridge": "Panjang lintasan menjawab seberapa jauh robot berjalan. Vektor perpindahan menjawab perubahan posisi beserta arahnya. Kita akan menyambung panah, membaca acuan sudut, dan memilih sumbu agar satu peristiwa dapat digambar sekaligus dihitung dengan konsisten.",
            "lab": _lab("vector", ax=6, ay=0, bx=0, by=8),
        },
        "goals": [
            "menyambung dua panah dan membaca panjang hasilnya, bukan menjumlah panjangnya;",
            "menguraikan satu gaya miring menjadi komponen mendatar dan tegak dengan memeriksa sudutnya diukur dari sumbu mana;",
            "memilih sumbu sejajar dan tegak lurus bidang pada bidang miring, lalu menguraikan berat ke sumbu itu.",
        ],
        "concepts": [
            {
                "id": "vektor-sambung",
                "title": "Dua perjalanan, satu panah hasil",
                "question": "Bagaimana memberi petunjuk langsung menuju robot tanpa mengulangi seluruh belokan rutenya?",
                "explain": [
                    "Vektor adalah besaran yang memerlukan besar dan arah. Pada peta, perpindahan digambar sebagai panah dari posisi awal menuju posisi akhir; panjang panah mengikuti skala meter yang dipilih. Memutar panah mengubah perpindahan, walaupun panjangnya tetap. Jarak tempuh berbeda: ia menjumlah panjang setiap ruas lintasan dan tidak menyimpan arah.",
                    "Untuk menjumlah A dan B dengan cara ujung–pangkal, salin panah B tanpa memutar atau mengubah panjangnya, lalu letakkan pangkal B pada ujung A. Resultan R ditarik dari pangkal A menuju ujung B. Kedua ruas itu adalah perjalanan berurutan, sedangkan R adalah satu perpindahan yang mempunyai titik awal dan akhir yang sama. Pada vektor perpindahan, salinan panah boleh digeser sejajar; jangan menerapkan kebebasan ini untuk memindahkan titik kerja gaya pada analisis putaran benda tegar.",
                    "Bila kedua panah tegak lurus, gambar hasilnya adalah sisi miring segitiga siku-siku, sehingga R² = A² + B². Jika searah, R = A + B. Jika berlawanan, besarnya |A − B| dan arahnya mengikuti panah yang lebih besar. Jadi penjumlahan besar A + B hanya menjadi besar resultan pada keadaan searah. Dua panah berlawanan tidak otomatis habis; keduanya habis hanya bila besarnya sama.",
                    "Lab menampilkan A, B, dan R pada satu skala. Perhatikan titik akhir, bukan hanya angka panjang. Pertukaran urutan A dan B mengubah bentuk rute, tetapi titik akhir tetap sama bila kedua vektornya sama. Untuk dua panah sembarang, besar resultan tidak melebihi jumlah besar kedua panah dan tidak lebih kecil daripada nilai mutlak selisih besar keduanya. Pemeriksaan batas ini membantu menemukan hasil hitung yang tidak mungkin sebelum melanjutkan.",
                ],
                "formula": "R = A + B; untuk A ⟂ B: |R| = √(|A|² + |B|²). Secara umum ||A| − |B|| ≤ |R| ≤ |A| + |B|.",
                "quantities": ["A, B, R: vektor perpindahan (m)", "|A|, |B|, |R|: besar perpindahan (m)", "Jarak tempuh: jumlah panjang ruas lintasan (m)"],
                "assumptions": ["Peta datar dua dimensi dengan timur +x dan utara +y.", "Skala panjang sama untuk kedua sumbu.", "Panah yang disalin digeser sejajar tanpa mengubah arah atau panjang."],
                "lab": _lab("vector", ax=6, ay=0, bx=0, by=8),
                "explore": [
                    "Prediksi: ketika B semula (0,8) m diganti menjadi (−8,0) m, apakah R lebih panjang atau lebih pendek daripada semula? Tulis alasan dari arah panah.",
                    "Ubah hanya arah B: pertahankan besar 8 m dengan pasangan (0,8), (8,0), dan (−8,0). Biarkan A = (6,0) m.",
                    "Amati titik akhir dan panjang R pada tiga keadaan. Bandingkan dengan jumlah panjang lintasan yang selalu 14 m.",
                    "Jelaskan mengapa R dapat 10 m, 14 m, atau 2 m walaupun panjang kedua ruas tidak berubah. Sebutkan arah hasil pada keadaan terakhir.",
                ],
                "misconception": {
                    "claim": "Kalau robot menempuh 6 m lalu 8 m, perpindahannya pasti 14 m.",
                    "explain": "14 m adalah jarak lintasan. Untuk ruas saling tegak lurus, garis penghubung titik awal–akhir adalah √(6² + 8²) = 10 m. Mengganti arah ruas kedua dapat mengubah perpindahan tanpa mengubah panjang lintasan.",
                },
                "worked": {
                    "scenario": "Robot inspeksi bergerak 9 m ke timur lalu 12 m ke utara. Tentukan besar perpindahan langsungnya.",
                    "steps": [
                        "Model: perlakukan robot sebagai titik pada peta datar; yang dicari perpindahan, bukan panjang rute.",
                        "Data: A = 9 m ke timur, B = 12 m ke utara. Pilih timur +x dan utara +y.",
                        "Diagram: gambar A ke kanan; di ujungnya gambar B ke atas. Tarik R dari pangkal A menuju ujung B. Sudut antara A dan B adalah 90°.",
                        "Persamaan: segitiga siku-siku memberi |R|² = 9² + 12².",
                        "Hitung: |R| = √(81 + 144) = √225 = 15 m.",
                        "Makna: titik akhir berada di timur laut. Jarak lintasannya 21 m, tetapi satu perpindahan penggantinya sepanjang 15 m.",
                        "Cek: 3 m ≤ 15 m ≤ 21 m, dan sisi miring 15 m lebih besar daripada masing-masing sisi 9 m dan 12 m.",
                    ],
                    "result": "Besar perpindahan 15 m menuju timur laut; 21 m adalah jarak tempuhnya.",
                },
                "checks": [
                    _n("f-mek-1-pra-CP1-1", "vektor-sambung", "Robot bergerak 8 m ke barat lalu 15 m ke utara. Berapa besar perpindahannya?", "Besar perpindahan", 17, "m", explain="Kedua ruas tegak lurus. √(8² + 15²) = √289 = 17 m; 23 m adalah jarak tempuh.", diagram=_lab("vector", ax=-8, ay=0, bx=0, by=15)),
                    _c("f-mek-1-pra-CP1-2", "vektor-sambung", "A = 7 m ke kanan dan B = 7 m ke kiri disambung ujung–pangkal. Apa yang tampak pada titik akhir?", ["Kembali ke titik awal; R = 0.", "Berada 14 m di kanan titik awal.", "R = 7 m ke kiri karena B digambar terakhir."], 0, "Dua panah sama besar dan berlawanan memberi resultan nol. Urutan perjalanan tidak membuat panah terakhir menjadi seluruh hasil.", diagram=_lab("vector", ax=7, ay=0, bx=-7, by=0)),
                ],
            },
            {
                "id": "vektor-acuan",
                "title": "Komponen: periksa dulu sudut itu berangkat dari mana",
                "question": "Mengapa gaya yang sama dapat dihitung dengan kosinus atau sinus untuk komponen mendatarnya?",
                "explain": [
                    "Satu gaya miring F dapat diwakili oleh dua komponen saling tegak lurus, Fx dan Fy. Jika kedua komponen disambung ujung–pangkal, hasilnya tepat F. Komponen adalah proyeksi bertanda pada sumbu: ia menunjukkan seberapa kuat bagian gaya itu pada arah sumbu yang dipilih. Dua komponen ini menggantikan satu gaya dalam hitungan; jangan menjumlah F, Fx, dan Fy sebagai tiga gaya terpisah.",
                    "Pada segitiga komponen, F selalu sisi miring. Sisi yang menempel pada sudut adalah sisi samping, sedangkan sisi yang berhadapan dengan sudut adalah sisi depan. Kosinus mengambil samping/miring dan sinus mengambil depan/miring. Jika θ diukur dari +x, maka Fx = F cos θ dan Fy = F sin θ. Hubungan ini berlaku untuk sudut arah penuh dengan tanda sinus dan kosinus yang sesuai kuadrannya.",
                    "Untuk vektor di kuadran I, sudut lancip φ terhadap +y memenuhi φ = 90° − θ. Komponen mendatar kini berada di depan φ, sehingga Fx = F sin φ, sementara Fy = F cos φ. Vektor tidak berubah ketika label acuan diganti. Pada lab, kontrol θ selalu menyatakan arah vektor dari +x; pilihan acuan x/y hanya mengganti sudut yang ditampilkan. Karena itu jangan mengira pilihan acuan y memutar gaya.",
                    "Periksa tanda dari gambar sebelum menyelesaikan hitungan: kanan dan atas positif, kiri dan bawah negatif. Besar tiap komponen tidak dapat melebihi besar F. Untuk memeriksa konsistensi, kuadratkan kedua komponen dan jumlahkan: Fx² + Fy² harus sama dengan F², dengan selisih kecil karena pembulatan. Jika θ = 0°, semua gaya sejajar +x; jika 90°, komponen x nol. Kedua keadaan batas lebih kuat daripada hafalan ‘mendatar selalu kosinus’.",
                ],
                "formula": "θ dari +x: Fx = F cos θ, Fy = F sin θ; kuadran I dan φ dari +y: Fx = F sin φ, Fy = F cos φ; F = √(Fx² + Fy²).",
                "quantities": ["F: besar gaya (N)", "Fx, Fy: komponen gaya bertanda (N)", "θ: arah vektor dari +x (°)", "φ: sudut lancip dari +y untuk vektor kuadran I (°)"],
                "assumptions": ["Sumbu x dan y saling tegak lurus; kanan dan atas positif.", "Sudut masukan lab selalu dari +x, termasuk ketika acuan tampilan y dipilih.", "Pertukaran sinus/kosinus dengan φ = 90° − θ dijelaskan untuk kuadran I; di kuadran lain baca tanda dan geometri terlebih dahulu."],
                "lab": _lab("components", F=50, theta=53.130102, ref="x"),
                "explore": [
                    "Prediksi: F tetap dan vektornya tidak diputar. Jika acuan sudut diganti dari x menjadi y, apakah Fx dan Fy berubah?",
                    "Ubah hanya acuan tampilan x menjadi y pada F = 50 N, θ ≈ 53,13°. Setelah mencatat hasil, kembalikan x lalu ubah θ menjadi 0° dan 90° satu per satu.",
                    "Amati panah utama, sisi segitiga, sudut yang tertulis, dan dua nilai komponen. Bedakan perubahan label acuan dari perubahan arah fisik.",
                    "Jelaskan dengan kata samping, depan, dan miring mengapa Fx dapat ditulis 50 cos 53,13° atau 50 sin 36,87°, dengan hasil sama sekitar 30 N.",
                ],
                "misconception": {
                    "claim": "Komponen mendatar selalu F cos sudut yang tertulis pada gambar.",
                    "explain": "Kosinus memilih sisi yang menempel pada sudut, bukan memilih mendatar. Jika sudut lancip diukur dari garis tegak, komponen mendatar berada di depan sudut dan memakai sinus. Cari dua garis pembentuk sudut sebelum memilih fungsi.",
                },
                "worked": {
                    "scenario": "Tali menarik sensor dengan gaya 40 N ke kanan atas, membentuk sudut 30° terhadap garis tegak +y. Tentukan komponen mendatarnya. sin 30° = 0,5.",
                    "steps": [
                        "Model: ganti satu gaya tali dengan dua proyeksi pada sumbu mendatar–tegak yang tegak lurus.",
                        "Data: F = 40 N dan φ = 30° dari +y. Arah gaya berada di kanan atas, maka Fx positif.",
                        "Diagram: tandai φ di antara tali dan garis tegak, lalu buat segitiga siku-siku. Sisi mendatar berhadapan dengan φ; tali adalah sisi miring.",
                        "Persamaan: sin φ = Fx/F, sehingga Fx = F sin φ. Jika memakai sudut dari +x, θ = 60° dan Fx = F cos 60°.",
                        "Hitung: Fx = 40 × 0,5 = +20 N.",
                        "Makna: pengaruh gaya pada sumbu mendatar setara 20 N ke kanan; bukan seluruh 40 N bekerja mendatar.",
                        "Cek: Fy = 40 cos 30° ≈ 34,64 N; √(20² + 34,64²) ≈ 40 N. Tiap komponen lebih kecil daripada F.",
                    ],
                    "result": "Fx = +20 N, yaitu 20 N ke kanan.",
                },
                "checks": [
                    _n("f-mek-1-pra-CP2-1", "vektor-acuan", "Satu gaya 60 N mengarah ke kanan atas dan membuat sudut 30° terhadap +y. sin 30° = 0,5. Berapa komponen mendatarnya?", "Fx", 30, "N", explain="Sudut dari +y membuat sisi x berada di depan sudut: Fx = 60 sin 30° = +30 N.", diagram=_lab("components", F=60, theta=60, ref="y")),
                    _c("f-mek-1-pra-CP2-2", "vektor-acuan", "Tanpa memutar panah gaya, acuan label sudut di lab diganti dari x menjadi y. Apa yang harus tetap?", ["Kedua komponen dan arah panah gaya.", "Angka sudut terhadap kedua sumbu harus sama.", "Fx dan Fy saling bertukar nilainya."], 0, "Acuan sudut hanya mengubah cara mendeskripsikan arah. Vektor yang sama pada sumbu yang sama mempunyai komponen yang sama.", seconds=180),
                ],
            },
            {
                "id": "vektor-tanda",
                "title": "Jumlahkan bagian searah sumbu, lengkap dengan tandanya",
                "question": "Bagaimana menemukan hasil dua panah miring tanpa menebak arah dari gambar kecil?",
                "explain": [
                    "Saat panah-panah tidak membentuk segitiga sederhana, gunakan komponen. Pilih satu sistem sumbu untuk semua panah. Pada peta kita, timur +x, barat −x, utara +y, dan selatan −y. Tuliskan setiap komponen bersama tandanya. Komponen −4 m berarti perubahan posisi 4 m ke arah negatif; besar vektor itu sendiri tetap bilangan tak negatif.",
                    "Jumlahkan hanya komponen yang sejajar: Rx = Ax + Bx dan Ry = Ay + By. Jangan menggabungkan Ax dengan By hanya karena angkanya berdekatan. Metode ini sebenarnya mengumpulkan seluruh gerakan mendatar dan seluruh gerakan tegak dari rute yang sama. Pergeseran kembali ke barat mengurangi perpindahan timur, bukan menambahnya sebagai panjang lintasan.",
                    "Setelah Rx dan Ry ditemukan, bangun satu segitiga siku-siku baru. Besar resultan adalah √(Rx² + Ry²). Kuadrat menghilangkan tanda di dalam hitungan panjang, tetapi tanda aslinya tetap diperlukan untuk arah. Misalnya Rx negatif dan Ry positif menempatkan ujung resultan di kiri atas. Sudut lancip dari perbandingan |Ry|/|Rx| harus ditempatkan pada kuadran itu, bukan langsung dianggap sudut dari +x.",
                    "Lab menghubungkan tabel komponen dengan panah yang disambung. Gunakan kontrol untuk membuat satu komponen resultan nol: panah hasil harus tepat sejajar sumbu yang lain. Jika Rx = Ry = 0, hasil tidak memiliki arah tunggal. Hindari pembagian dengan Rx saat Rx = 0; cukup baca arah vertikal dari tanda Ry. Cara ini membantu memeriksa hasil sekaligus menangani keadaan khusus dengan benar.",
                ],
                "formula": "Rx = Ax + Bx; Ry = Ay + By; |R| = √(Rx² + Ry²). Arah dibaca dari tanda Rx dan Ry sebelum menentukan sudut.",
                "quantities": ["Ax, Ay, Bx, By: komponen masing-masing perpindahan (m)", "Rx, Ry: komponen resultan bertanda (m)", "|R|: besar resultan, selalu ≥ 0 (m)"],
                "assumptions": ["Semua vektor memakai sumbu dan satuan yang sama.", "Sumbu x dan y ortogonal dengan skala sama.", "Tanda komponen menyatakan arah, bukan nilai panjang negatif."],
                "lab": _lab("vector", ax=8, ay=3, bx=-12, by=0),
                "explore": [
                    "Prediksi: A = (8,3) m dan B = (−12,0) m. Di kuadran mana ujung R akan berada?",
                    "Ubah hanya Bx dari −12 menjadi −8, lalu menjadi −4. Biarkan komponen lainnya tetap.",
                    "Amati Rx saat negatif, nol, dan positif. Periksa apakah panah R melewati garis +y ketika Rx = 0.",
                    "Jelaskan mengapa hasil akhir tidak dapat ditentukan dari jumlah besar A dan besar B saja, serta mengapa komponen negatif harus dipertahankan sebelum dikuadratkan.",
                ],
                "misconception": {
                    "claim": "Supaya mendapatkan panjang, semua komponen boleh dibuat positif sejak awal.",
                    "explain": "Membuat semua komponen positif sebelum dijumlahkan mengubah arah panah. A = (8,3) m dan B = (−12,0) m memberi R = (−4,3) m, bukan (20,3) m. Tanda baru hilang pada kuadrat untuk menghitung besar, setelah penjumlahan bertanda selesai.",
                },
                "worked": {
                    "scenario": "Peta robot mencatat perpindahan A = (8,3) m dan B = (−12,0) m. Tentukan besar perpindahan gabungan.",
                    "steps": [
                        "Model: semua perpindahan dinyatakan pada sumbu timur +x dan utara +y yang sama.",
                        "Data: Ax = +8 m, Ay = +3 m, Bx = −12 m, By = 0 m.",
                        "Diagram: A menuju kanan atas; B disalin 12 m ke kiri dari ujung A. Ujung akhir berada di kiri atas titik awal.",
                        "Persamaan: Rx = Ax + Bx dan Ry = Ay + By; besar R = √(Rx² + Ry²).",
                        "Hitung: Rx = 8 − 12 = −4 m, Ry = 3 m, lalu |R| = √(16 + 9) = 5 m.",
                        "Makna: resultan 5 m mengarah barat laut. Jika perlu sudut, arctan(3/4) ≈ 36,87° ke utara dari barat, setara 143,13° dari +x.",
                        "Cek: tanda Rx negatif dan Ry positif cocok dengan gambar; √(4² + 3²) = 5 m dan tidak ada panjang negatif.",
                    ],
                    "result": "R = (−4,3) m; besarnya 5 m menuju barat laut.",
                },
                "checks": [
                    _n("f-mek-1-pra-CP3-1", "vektor-tanda", "Dua perpindahan pada diagram adalah A = (−7,2) m dan B = (3,1) m. Berapa komponen x resultannya?", "Rx", -4, "m", explain="Jumlahkan komponen x dengan tanda: Rx = −7 + 3 = −4 m. Ry tidak masuk penjumlahan sumbu x.", diagram=_lab("vector", ax=-7, ay=2, bx=3, by=1)),
                    _c("f-mek-1-pra-CP3-2", "vektor-tanda", "Hasil perhitungan memberi Rx = −6 m dan Ry = −8 m. Deskripsi mana yang sesuai?", ["Besar 10 m ke barat daya.", "Besar −14 m ke timur laut.", "Besar 10 m ke timur laut karena kuadrat menghapus tanda."], 0, "Besar √(36 + 64) = 10 m; kedua tanda negatif menempatkan ujung panah di kiri bawah. Kuadrat menentukan besar, bukan mengubah arah.", seconds=180),
                ],
            },
            {
                "id": "vektor-bidang",
                "title": "Putar sumbu, pertahankan arah berat",
                "question": "Sumbu mana yang membuat pengaruh berat sepanjang papan miring paling mudah dibaca?",
                "explain": [
                    "Berat W adalah gaya gravitasi Bumi pada benda dan selalu mengarah vertikal ke bawah dalam model dekat permukaan Bumi. Memiringkan papan tidak memutar arah berat. Yang dapat kita putar adalah sumbu untuk mendeskripsikannya. Pilihan sumbu mendatar–tegak tetap sah, tetapi sumbu sejajar dan tegak lurus papan sering memudahkan karena arah gerak atau kendala kontak mengikuti papan.",
                    "Ambil sumbu positif sejajar bidang ke bawah lereng dan sumbu positif tegak lurus keluar dari bidang. Untuk papan membentuk sudut θ terhadap mendatar, komponen berat sepanjang bidang adalah +W sin θ. Komponen bertanda pada sumbu keluar bidang adalah −W cos θ, karena berat menekan ke dalam bidang. Bila yang diminta hanya besarnya, tulis W∥ = W sin θ dan W⊥ = W cos θ, keduanya positif pada 0° sampai 90°.",
                    "Mengapa θ muncul pada segitiga berat, padahal sudut diberikan di bawah papan? Garis normal bidang tegak lurus papan, sedangkan garis vertikal tegak lurus mendatar. Memutar dua garis acuan sama-sama 90° mempertahankan sudut lancipnya. Karena itu sudut antara berat dan arah masuk tegak lurus bidang sama dengan kemiringan papan. Sisi sejajar bidang berhadapan dengan θ dan memakai sinus; sisi normal menempel dan memakai kosinus.",
                    "Komponen berat bukan dua gaya tambahan, dan W⊥ bukan nama lain gaya normal dari papan. Gaya normal merupakan interaksi lain yang besarnya harus ditentukan dari kondisi gerak serta gaya-gaya lain. Di TP ini, tugas kita menguraikan berat. Uji batasnya: papan datar memberi W∥ = 0 dan W⊥ = W; papan makin tegak memberi W∥ mendekati W dan W⊥ mendekati nol. Arah panah berat pada lab tetap vertikal selama θ diubah.",
                ],
                "formula": "Besar: W∥ = W sin θ, W⊥ = W cos θ. Jika +∥ menurun dan +⊥ keluar bidang: W∥ bertanda positif, W⊥ bertanda negatif. W = mg.",
                "quantities": ["W: besar berat (N)", "W∥: besar komponen sejajar bidang (N)", "W⊥: besar komponen menuju bidang (N)", "θ: sudut bidang terhadap mendatar (°)", "m: massa (kg); g = 10 m/s²"],
                "assumptions": ["Bidang lurus dengan kemiringan 0°–90° terhadap mendatar.", "Gravitasi seragam, g = 10 m/s²; berat vertikal ke bawah.", "Lab hanya menguraikan berat; tidak mengasumsikan gaya normal sama dengan komponen berat untuk setiap situasi."],
                "lab": _lab("incline", W=100, theta=30),
                "explore": [
                    "Prediksi: berat tetap 100 N. Jika papan dibuat lebih curam, komponen mana yang membesar? Gunakan gambaran papan hampir tegak.",
                    "Ubah hanya θ dari 0° ke 30°, 60°, lalu 90°. Biarkan W tetap.",
                    "Amati arah berat yang tetap vertikal, arah kedua sumbu, dan perubahan panjang dua komponen. Pada setiap keadaan, periksa W∥² + W⊥² terhadap W².",
                    "Jelaskan dari segitiga mengapa komponen menuruni lereng memakai sinus sudut bidang, dan mengapa komponen menuju bidang tidak otomatis merupakan gaya dari papan.",
                ],
                "misconception": {
                    "claim": "Komponen berat sepanjang bidang selalu W cos θ karena letaknya mendatar pada gambar segitiga.",
                    "explain": "Sejajar bidang bukan berarti sejajar sumbu mendatar halaman. Sudut θ di segitiga berat terletak antara W dan arah masuk normal bidang; komponen sepanjang bidang berhadapan dengan sudut itu. Uji papan datar juga menolak W cos θ untuk komponen sejajar: pada θ = 0°, hasilnya seharusnya nol.",
                },
                "worked": {
                    "scenario": "Kotak sensor bermassa 12 kg berada pada papan 30° terhadap mendatar. Dengan g = 10 m/s², tentukan besar komponen berat yang menuruni papan.",
                    "steps": [
                        "Model: uraikan gaya gravitasi saja; belum menentukan normal atau percepatan kotak.",
                        "Data: m = 12 kg, g = 10 m/s², θ = 30°, sehingga W = mg = 120 N.",
                        "Diagram: gambar W vertikal ke bawah. Pilih sumbu sejajar papan ke bawah lereng dan sumbu normal keluar papan; bentuk segitiga dengan sisi miring W.",
                        "Persamaan: sudut antara W dan arah masuk normal adalah 30°. Komponen sejajar di depan sudut: W∥ = W sin 30°.",
                        "Hitung: W∥ = 120 × 0,5 = 60 N.",
                        "Makna: bagian pengaruh gravitasi sepanjang papan setara 60 N menuruni lereng. Ini belum merupakan gaya neto jika ada gaya lain sepanjang papan.",
                        "Cek: W⊥ ≈ 103,92 N dan √(60² + 103,92²) ≈ 120 N; pada papan datar komponen sejajar akan menjadi nol.",
                    ],
                    "result": "Besar komponen berat sejajar papan 60 N, menuruni lereng.",
                },
                "checks": [
                    _n("f-mek-1-pra-CP4-1", "vektor-bidang", "Berat peti 80 N pada bidang 30° terhadap mendatar. sin 30° = 0,5. Berapa besar komponen berat sejajar bidang?", "Besar W sejajar", 40, "N", explain="Komponen sepanjang bidang berada di depan θ pada segitiga berat: 80 sin 30° = 40 N menurun.", diagram=_lab("incline", W=80, theta=30)),
                    _c("f-mek-1-pra-CP4-2", "vektor-bidang", "Pada gambar bidang datar (θ = 0°), pernyataan manakah yang cocok dengan arah berat?", ["Komponen sejajar nol dan komponen menuju bidang sebesar W.", "Komponen sejajar W dan komponen menuju bidang nol.", "Kedua komponen masing-masing W."], 0, "Berat vertikal pada bidang datar seluruhnya tegak lurus bidang. Komponen sejajar harus W sin 0° = 0.", diagram=_lab("incline", W=100, theta=0)),
                ],
            },
        ],
        "prediction": [
            _c("f-mek-1-pra-P3-1", "vektor-sambung", "Dua robot menempuh dua ruas yang masing-masing 5 m. Robot A berbelok 90°, robot B berbalik 180°. Bandingkan besar perpindahan keduanya.", ["A lebih besar daripada B.", "Sama karena jarak kedua rute 10 m.", "B lebih besar karena sudut belok lebih besar."], 0, "Panah ujung–pangkal robot B kembali ke awal, sedangkan A berakhir di sudut diagonal. Jelaskan prediksimu sebelum mencoba lab.", seconds=180),
            _c("f-mek-1-pra-P3-2", "vektor-acuan", "Gaya yang sama tetap menunjuk kanan atas. Sudutnya dilabeli ulang dari terhadap mendatar menjadi terhadap tegak. Prediksikan komponen mendatarnya.", ["Tetap, karena vektor dan sumbu tidak berubah.", "Berubah menjadi komponen tegak sebelumnya.", "Selalu menjadi lebih kecil."], 0, "Acuan penyebutan sudut bukan perubahan gaya. Uji dengan mengganti pilihan acuan tanpa memutar panah.", seconds=180),
        ],
        "performance": {
            "scenario": "Siapkan kartu rute untuk robot pengantar alat. Rute A = (12,0) m dilanjutkan B = (−4,6) m. Di tujuan, sensor ditahan tali dengan gaya 50 N yang arahnya 36,87° dari +y (sin ≈ 0,60; cos ≈ 0,80). Kotak cadangan mempunyai berat 100 N pada jalur naik 30° terhadap mendatar. Tunjukkan cara memperoleh petunjuk arah, komponen gaya tali, dan komponen berat dengan gambar yang bisa dipakai temanmu.",
            "deliverables": [
                "Peta berskala dengan panah A, B disambung ujung–pangkal dan satu panah resultan dari awal ke akhir.",
                "Tabel komponen bertanda, besar resultan, dan arah yang cocok dengan tanda komponennya.",
                "Segitiga gaya tali berlabel acuan sudut, sisi depan/samping, hasil dua komponen, serta pemeriksaan Pythagoras.",
                "Diagram berat pada bidang miring dengan sumbu pilihan, dua komponen, dan pemeriksaan ketika bidang dibuat datar.",
                "Satu tangkapan atau catatan lab sebelum–sesudah mengubah satu variabel beserta penjelasan perubahan hasilnya.",
            ],
            "rubric": {
                "T1": "Menggambar sebagian panah, tetapi acuan sudut/sumbu belum jelas atau besar vektor masih dijumlah sebagai skalar; perlu bimbingan untuk memulai model.",
                "T2": "Menyambung rute dan memakai komponen, tetapi masih ada tanda, pilihan sinus/kosinus, arah hasil, atau satuan yang belum konsisten; pemeriksaan belum menjelaskan letak kesalahan.",
                "T3": "Secara mandiri menghasilkan peta, tabel komponen, penguraian tali dan berat yang benar; acuan sudut serta satuan jelas; arah konsisten dengan tanda, Pythagoras dan batas bidang datar diperiksa.",
                "T4": "Memenuhi T3, lalu memakai perubahan satu variabel di lab untuk menjelaskan mengapa hasil berubah; dapat menunjukkan dua acuan sudut yang ekuivalen dan memperbaiki gambar keliru dengan alasan geometri.",
            },
        },
    },
    "f-mek-2": {
        "hook": {
            "title": "Troli laboratorium masih ke kanan, tetapi gaya netonya ke mana?",
            "scene": "Troli sensor sedang melaju ke kanan pada rel laboratorium. Dua aktuator menariknya: kabel kanan 8 N dan kabel kiri 20 N. Seorang siswa menambahkan panah ‘gaya gerak’ ke kanan karena troli masih menuju ujung rel. Siswa lain ingin memeriksa siapa pemberi setiap gaya sebelum menebak gerak berikutnya.",
            "question": "Saat dua tarikan itu bekerja, mungkinkah troli tetap bergerak ke kanan untuk sementara? Ubah satu tarikan dan bandingkan panah gaya, percepatan, serta kecepatan.",
            "bridge": "Kita akan memisahkan gambar interaksi pada benda dari catatan geraknya. Gaya neto menentukan perubahan kecepatan; untuk mengetahui kecepatan berikutnya kita juga memerlukan keadaan awal dan lamanya gaya bekerja.",
            "lab": _lab("motion", right=8, left=20, m=4, v0=6, t=1),
        },
        "goals": [
            "memeriksa tiap panah gaya dengan satu pertanyaan — siapa pemberinya — dan membuang panah yang tidak punya pemberi;",
            "menjumlahkan gaya dengan tanda arah, lalu membaca arti gaya neto bagi keadaan geraknya;",
            "menghitung percepatan dari gaya neto dan massa, dan menyebut pasangan aksi–reaksi beserta benda tempatnya bekerja.",
        ],
        "concepts": [
            {
                "id": "gerak-pemberi",
                "title": "Mulai dari benda yang ditinjau dan siapa pemberi gayanya",
                "question": "Panah mana yang boleh masuk diagram gaya troli, dan mana yang hanya menggambarkan gerak?",
                "explain": [
                    "Gaya adalah interaksi antara dua benda, bukan sesuatu yang tersimpan karena benda sedang bergerak. Sebelum menggambar, lingkari satu benda yang ditinjau, misalnya troli. Lalu cari benda lain yang sedang berinteraksi dengannya. Tuliskan nama gaya sebagai ‘pemberi pada penerima’: tarikan kabel kanan pada troli, tarikan kabel kiri pada troli, gaya gravitasi Bumi pada troli, dan gaya normal rel pada troli.",
                    "Diagram benda bebas hanya memuat gaya yang bekerja pada benda yang dilingkari. Panah kecepatan boleh digambar terpisah untuk membantu membaca gerak, tetapi tidak dijumlahkan ke gaya. Gerak ke kanan bukan nama pemberi gaya. Ketika tangan sudah lepas, dorongan tangan pada troli sudah tidak ada; troli masih dapat melaju karena kecepatannya tidak berubah seketika hanya akibat hilangnya satu interaksi.",
                    "Pada rel mendatar tanpa gerak vertikal, normal rel ke atas menyeimbangkan berat ke bawah jika tidak ada gaya vertikal lain. Bagian lab motion menampilkan dua gaya horizontal secara khusus. right dan left adalah besar dua tarikan yang masing-masing berasal dari aktuator atau kabel; keduanya bilangan nonnegatif. Gaya ke kiri tidak otomatis berarti gesekan. Gesekan hanya dimasukkan bila kontak serta model geseknya dinyatakan dalam peristiwa.",
                    "Gunakan daftar interaksi untuk memeriksa kelengkapan diagram: siapa menarik atau mendorong, siapa menopang, dan adakah gravitasi? Sesudah diagram lengkap, barulah proyeksikan pada sumbu dan jumlahkan. Resultan merupakan ringkasan matematis dari gaya-gaya itu, bukan gaya tambahan yang harus digambar lalu dijumlah sekali lagi. Model titik di sini meninjau gerak translasi dan tidak membahas putaran roda atau lokasi titik kerja secara rinci.",
                ],
                "formula": "ΣFx = Fkanan − Fkiri; pada keadaan vertikal seimbang tanpa gaya vertikal lain: ΣFy = N − mg = 0. Kecepatan v tidak masuk ΣF.",
                "quantities": ["Fkanan, Fkiri: besar tarikan horizontal (N)", "N: gaya normal rel pada troli (N)", "W = mg: berat dari Bumi (N)", "v: kecepatan (m/s), bukan gaya", "m: massa (kg); g = 10 m/s²"],
                "assumptions": ["Troli dimodelkan sebagai titik; rel mendatar menahan gerak vertikal.", "Lab motion hanya menghitung komponen horizontal; normal dan berat saling menyeimbangkan.", "Dua gaya horizontal adalah tarikan eksternal konstan yang disebutkan, bukan otomatis gaya gesek.", "Hambatan udara dan gesekan diabaikan kecuali dinyatakan."],
                "lab": _lab("motion", right=12, left=4, m=4, v0=3, t=1),
                "explore": [
                    "Prediksi: jika dua kabel dilepas sekaligus, panah gaya horizontal manakah yang masih memiliki pemberi? Apakah kecepatan harus langsung nol?",
                    "Ubah tarikan kanan menjadi 0 N, amati, lalu ubah tarikan kiri menjadi 0 N. Pertahankan m = 4 kg, v0 = 3 m/s, dan t = 1 s.",
                    "Amati panah tarikan yang hilang ketika nilainya nol dan bandingkan keadaan v pada kedua tarikan nol. Pisahkan panah kecepatan dari panah gaya.",
                    "Jelaskan daftar gaya lengkap pada troli setelah kedua kabel lepas, termasuk berat dan normal yang tidak digambar di panel horizontal. Sebut pemberi setiap gaya.",
                ],
                "misconception": {
                    "claim": "Troli bergerak ke kanan, jadi harus ditambahkan gaya gerak ke kanan.",
                    "explain": "Panah itu tidak memiliki pemberi interaksi. Kecepatan menjelaskan keadaan gerak; gaya menjelaskan perubahan keadaan itu. Pada rel ideal, troli dapat tetap bergerak dengan dua tarikan nol. Jika troli nyata melambat, cari interaksi nyata seperti gesekan, bukan menambahkan atau menghilangkan gaya gerak rekaan.",
                },
                "worked": {
                    "scenario": "Troli 3 kg melaju ke kanan pada rel ideal. Kabel A menariknya 14 N ke kanan dan kabel B menarik 5 N ke kiri. Tentukan daftar gaya yang benar pada troli.",
                    "steps": [
                        "Model: lingkari troli saja sebagai sistem; rel mendatar dan tidak ada gerak vertikal.",
                        "Data: m = 3 kg, g = 10 m/s²; dua tarikan horizontal 14 N ke kanan dan 5 N ke kiri.",
                        "Daftar interaksi: kabel A, kabel B, Bumi, dan rel berinteraksi dengan troli. Gerak ke kanan bukan interaksi tambahan.",
                        "Diagram: pada satu titik troli gambar tarikan A ke kanan, tarikan B ke kiri, berat ke bawah, dan normal ke atas. Letakkan panah v di luar diagram gaya.",
                        "Persamaan vertikal: N − mg = 0, sehingga W = 30 N ke bawah dan N = 30 N ke atas; kedua tarikan horizontal tidak diubah oleh persamaan ini.",
                        "Makna: ada empat gaya nyata pada troli, meskipun lab horizontal hanya menampilkan dua tarikan. Resultan horizontal 9 N ke kanan adalah ringkasan, bukan gaya kelima.",
                        "Cek: setiap panah mempunyai pemberi dan penerima, satuan N, dan hanya gaya pada troli yang masuk diagram.",
                    ],
                    "result": "Tarikan A pada troli, tarikan B pada troli, berat dari Bumi, dan normal dari rel; tidak ada gaya gerak tambahan.",
                },
                "checks": [
                    _c("f-mek-2-CP1-1", "gerak-pemberi", "Troli sudah terlepas dari tangan dan melaju di rel mendatar ideal. Kedua kabel tidak menarik. Diagram gaya lengkap mana yang tepat?", ["Berat Bumi ke bawah dan normal rel ke atas.", "Berat, normal, dan gaya gerak ke depan.", "Hanya gaya dorong tangan yang tersisa."], 0, "Tangan tidak lagi berinteraksi, dan gerak bukan pemberi gaya. Berat dan normal tetap ada; resultan horizontalnya nol.", seconds=180, diagram=_lab("motion", right=0, left=0, m=3, v0=2, t=1)),
                    _c("f-mek-2-CP1-2", "gerak-pemberi", "Panel menunjukkan tarikan kiri 6 N dari kabel B pada troli. Nama gaya manakah yang boleh dipakai tanpa informasi tambahan?", ["Tarikan kabel B pada troli ke kiri.", "Gaya gesek pasti 6 N ke kiri.", "Gaya troli pada kabel B ke kiri."], 0, "Identitas pemberi ditentukan peristiwa. Arah kiri saja tidak membuktikan gesekan; gaya troli pada kabel bekerja pada kabel, sehingga tidak masuk diagram troli.", seconds=120),
                ],
            },
            {
                "id": "gerak-neto",
                "title": "Gaya neto menentukan perubahan kecepatan, bukan arah gerak sesaat",
                "question": "Bagaimana troli masih ke kanan ketika resultan gayanya ke kiri?",
                "explain": [
                    "Gaya neto adalah jumlah vektor semua gaya pada satu benda. Pada sumbu mendatar dengan kanan positif, tarikan kanan ditulis positif dan tarikan kiri negatif, sehingga ΣFx = Fkanan − Fkiri. Dua tarikan berlawanan tidak dijumlah besarnya. Jika keduanya sama, resultan nol meskipun tiap kabel tetap menarik. Pada arah vertikal kita mengasumsikan berat dan normal seimbang.",
                    "Hukum Newton menghubungkan gaya neto dengan percepatan. Percepatan adalah perubahan kecepatan tiap sekon; arah percepatan sama dengan arah gaya neto untuk massa positif. Kecepatan sesaat memerlukan informasi gerak sebelumnya. Jika troli sedang ke kanan dan gaya netonya ke kiri, kecepatan kanannya berkurang. Ia masih dapat ke kanan selama kecepatan belum mencapai nol.",
                    "Bila gaya ke kiri terus bekerja setelah troli berhenti sesaat, troli mulai bergerak ke kiri dan kelajuannya meningkat ke kiri. Dalam model gaya konstan, v = v0 + at dapat menelusuri perubahan itu. Jangan memakai rumus gaya konstan melewati keadaan ketika model gaya sebenarnya berubah; misalnya gaya gesek nyata yang berlawanan gerak perlu ditinjau ulang saat benda berhenti. Dua tarikan kabel lab tetap memiliki arah yang dinyatakan, sehingga tidak otomatis berubah saat v berganti tanda.",
                    "Gaya neto nol memberi a = 0, jadi kecepatan tetap. Nilai tetap itu bisa nol atau bisa bukan nol. Bedakan kecepatan bertanda dan kelajuan: ketika v = +4 berubah menjadi +2 m/s, kelajuan mengecil; ketika v = −2 berubah menjadi −4 m/s, kelajuan justru membesar, walaupun keduanya memiliki percepatan negatif. Amati tanda v dan tanda a bersama untuk menyatakan melambat atau makin cepat.",
                ],
                "formula": "ΣFx = Fkanan − Fkiri; arah a = arah ΣFx. Untuk a konstan: v(t) = v0 + at. ΣF = 0 ⇒ a = 0 ⇒ v tetap.",
                "quantities": ["ΣFx: gaya neto horizontal bertanda (N)", "a: percepatan bertanda (m/s²)", "v0, v: kecepatan awal dan kecepatan kemudian (m/s)", "t: lama dua tarikan tetap bekerja (s)"],
                "assumptions": ["Kanan dipilih positif; massa positif dan tetap.", "Dua kabel mempertahankan gaya konstan selama interval yang diamati.", "Rel cukup panjang; tidak ada tumbukan atau batas lintasan dalam interval itu."],
                "lab": _lab("motion", right=8, left=20, m=4, v0=6, t=1),
                "explore": [
                    "Prediksi: pada Fkanan = 8 N, Fkiri = 20 N, m = 4 kg, dan v0 = +6 m/s, ke mana troli bergerak setelah 1 s? Apakah arah itu sama dengan arah percepatan?",
                    "Ubah hanya t menjadi 1 s, 2 s, lalu 3 s; semua gaya, massa, dan kecepatan awal tetap.",
                    "Amati v = +3, 0, lalu −3 m/s sementara gaya neto tetap −12 N dan percepatan tetap −3 m/s². Temukan saat berhenti sesaat.",
                    "Jelaskan mengapa tanda gaya neto saja tidak cukup untuk menentukan arah kecepatan, dan mengapa kabel kiri tetap menarik ke kiri setelah troli berbalik.",
                ],
                "misconception": {
                    "claim": "Gaya neto ke kiri berarti benda langsung bergerak ke kiri; gaya neto nol berarti pasti diam.",
                    "explain": "Gaya neto memberi perubahan v, bukan mengganti v seketika. Troli yang memiliki v0 positif perlu waktu untuk mencapai nol ketika a negatif. Jika ΣF = 0, v mempertahankan nilai awalnya, termasuk nilai yang bukan nol.",
                },
                "worked": {
                    "scenario": "Troli 4 kg mula-mula berkecepatan +6 m/s. Dua kabel menarik konstan 8 N ke kanan dan 20 N ke kiri selama 1 s. Tentukan kecepatan setelah 1 s.",
                    "steps": [
                        "Model: gerak satu dimensi dengan dua tarikan konstan; kanan positif dan hambatan lain diabaikan.",
                        "Data: m = 4 kg, v0 = +6 m/s, Fkanan = 8 N, Fkiri = 20 N, t = 1 s.",
                        "Diagram: panah gaya kiri lebih panjang daripada kanan. Panah v0 digambar terpisah ke kanan.",
                        "Persamaan: ΣFx = 8 − 20 = −12 N; a = ΣFx/m = −3 m/s²; v = v0 + at.",
                        "Hitung: v = 6 + (−3)(1) = +3 m/s.",
                        "Makna: troli masih ke kanan tetapi melambat. Gaya neto dan percepatan ke kiri; keduanya tidak mengharuskan v saat ini ke kiri.",
                        "Cek: waktu berhenti jika gaya tetap adalah 6/3 = 2 s. Karena baru 1 s, tanda positif pada v masuk akal.",
                    ],
                    "result": "v = +3 m/s: masih ke kanan, dengan kelajuan berkurang.",
                },
                "checks": [
                    _c("f-mek-2-CP2-1", "gerak-neto", "Troli mula-mula +5 m/s. Pada diagram Fkanan = 6 N dan Fkiri = 14 N, m = 4 kg. Setelah 1 s tarikan konstan, pernyataan mana yang tepat?", ["Masih ke kanan, tetapi melambat.", "Langsung ke kiri karena gaya kiri lebih besar.", "Tetap +5 m/s karena troli sudah bergerak."], 0, "ΣFx = −8 N memberi a = −2 m/s². v setelah 1 s = 5 − 2 = +3 m/s; arahnya kanan, tetapi kelajuan berkurang.", level="C4", seconds=240, diagram=_lab("motion", right=6, left=14, m=4, v0=5, t=1)),
                    _c("f-mek-2-CP2-2", "gerak-neto", "Dua kabel masing-masing menarik 10 N ke arah berlawanan. Troli mula-mula bergerak +2 m/s di rel ideal. Apa yang terjadi selama gaya tetap?", ["Kecepatan tetap +2 m/s.", "Troli langsung berhenti.", "Kelajuan terus bertambah karena ada dua gaya."], 0, "Resultan horizontal nol sehingga a = 0. Dua gaya nyata ada, tetapi pengaruhnya pada perubahan kecepatan saling menyeimbangkan.", seconds=180, diagram=_lab("motion", right=10, left=10, m=4, v0=2, t=2)),
                ],
            },
            {
                "id": "gerak-massa",
                "title": "Gunakan resultan dan massa untuk menghitung percepatan",
                "question": "Mengapa dua troli dengan tarikan neto sama tidak selalu berubah kecepatannya sama cepat?",
                "explain": [
                    "Untuk benda bermassa tetap dalam kerangka laboratorium yang dapat dianggap tidak dipercepat, Hukum II Newton ditulis ΣF = ma. ΣF harus mencakup semua gaya pada benda yang dipilih. Satu gaya yang paling besar bukan pengganti resultan bila masih ada gaya lain. Sesudah resultan bertanda ditemukan, bagi dengan massa: a = ΣF/m. Tanda percepatan mengikuti tanda resultan.",
                    "Massa menyatakan ukuran kelembaman: makin besar massa, makin kecil perubahan kecepatan tiap sekon untuk resultan yang sama. Menambah massa dua kali dengan gaya neto tetap membuat percepatan separuhnya. Sebaliknya, menambah gaya neto dua kali pada massa tetap membuat percepatan dua kali. Pernyataan ini membandingkan percepatan, bukan otomatis membandingkan kelajuan sesaat karena keadaan awal juga berperan.",
                    "Satuan juga menjelaskan hubungan itu. Satu newton setara 1 kg·m/s², sehingga N/kg memberi m/s². Percepatan +2 m/s² berarti kecepatan bertambah secara aljabar 2 m/s setiap sekon selama model tetap. Jika v0 negatif, penambahan aljabar positif dapat mula-mula mengurangi kelajuan. Bedakan massa dalam kg dan berat dalam N; gunakan massa, bukan angka berat, sebagai penyebut dalam a = ΣF/m.",
                    "Lab memungkinkan perbandingan yang adil: tahan kedua tarikan tetap, ubah hanya massa, lalu amati a. Setelah itu pilih massa tetap dan ubah satu tarikan untuk mengubah resultan. Jika dua tarikan sama, memperkecil massa tidak menciptakan percepatan; nol dibagi massa positif tetap nol. Model tidak menerima massa nol, dan hasil berlaku selama gaya serta massa yang dinyatakan tidak berubah.",
                ],
                "formula": "a = ΣFx/m = (Fkanan − Fkiri)/m; Δv = at untuk a konstan; 1 N = 1 kg·m/s².",
                "quantities": ["m: massa, harus > 0 (kg)", "ΣFx: jumlah semua gaya horizontal bertanda (N)", "a: perubahan kecepatan tiap sekon (m/s²)", "Δv: perubahan kecepatan (m/s)", "t: selang waktu (s)"],
                "assumptions": ["Massa tetap dan positif.", "Kerangka pengamatan laboratorium mendekati kerangka inersial.", "Gaya horizontal konstan; gaya vertikal seimbang.", "Gesekan dan hambatan lain tidak dimasukkan kecuali dinyatakan."],
                "lab": _lab("motion", right=30, left=10, m=5, v0=0, t=2),
                "explore": [
                    "Prediksi: jika massa 5 kg diganti 10 kg sementara dua tarikan tetap 30 N dan 10 N, bagaimana percepatannya?",
                    "Ubah hanya m dari 5 kg menjadi 10 kg, lalu 20 kg. Pertahankan v0 dan t agar perbandingan tidak tercampur.",
                    "Amati bahwa ΣFx tetap +20 N, sedangkan a berubah dari 4 menjadi 2 lalu 1 m/s². Bandingkan perubahan kecepatannya pada waktu yang sama.",
                    "Jelaskan mengapa menggandakan massa tidak mengubah resultan dalam percobaan ini, tetapi mengubah akibatnya. Sebut apa yang harus dikendalikan agar perbandingan adil.",
                ],
                "misconception": {
                    "claim": "Percepatan cukup dihitung dari tarikan terbesar dibagi massa.",
                    "explain": "Tarikan lain tetap memberi pengaruh. Pada 30 N ke kanan dan 10 N ke kiri, penyebab perubahan gerak adalah resultan 20 N, bukan 30 N. Massa 5 kg memberi a = 4 m/s², bukan 6 m/s². Jika kedua gaya sama, cara tarikan-terbesar akan keliru memprediksi percepatan padahal resultannya nol.",
                },
                "worked": {
                    "scenario": "Troli bermassa 6 kg mendapat tarikan 42 N ke kanan dan 18 N ke kiri. Tentukan percepatannya dengan kanan positif.",
                    "steps": [
                        "Model: tinjau satu troli; gerak translasi satu dimensi dan massa tetap.",
                        "Data: Fkanan = 42 N, Fkiri = 18 N, m = 6 kg. Kanan positif.",
                        "Diagram: gambar dua gaya pada troli, kanan lebih panjang. Berat dan normal seimbang pada arah tegak.",
                        "Persamaan resultan: ΣFx = +42 + (−18) = +24 N; Hukum II: a = ΣFx/m.",
                        "Hitung: a = +24/6 = +4 m/s².",
                        "Makna: kecepatan berubah +4 m/s tiap sekon selama gaya tetap. Arah percepatan ke kanan; arah kecepatan awal belum diberikan.",
                        "Cek: satuan N/kg = m/s². Menghitung 42/6 = 7 m/s² akan mengabaikan tarikan kiri, sehingga bukan hasil model ini.",
                    ],
                    "result": "a = +4 m/s², ke kanan.",
                },
                "checks": [
                    _n("f-mek-2-CP3-1", "gerak-massa", "Troli 8 kg ditarik 10 N ke kanan dan 34 N ke kiri. Kanan positif. Berapa percepatannya?", "a", -3, "m/s²", explain="ΣFx = 10 − 34 = −24 N; a = −24/8 = −3 m/s². Tanda negatif menyatakan percepatan ke kiri.", seconds=180, diagram=_lab("motion", right=10, left=34, m=8, v0=4, t=1)),
                    _c("f-mek-2-CP3-2", "gerak-massa", "Troli A bermassa 4 kg dan B 8 kg. Keduanya mendapat resultan +16 N. Kesimpulan yang didukung data adalah…", ["Percepatan A dua kali percepatan B.", "Kelajuan A pasti dua kali kelajuan B setiap saat.", "Gaya pada B harus lebih besar karena massanya lebih besar."], 0, "aA = 16/4 = 4 dan aB = 16/8 = 2 m/s². Data hanya membandingkan percepatan; kelajuan sesaat masih bergantung pada v0 dan waktu.", level="C4", seconds=240),
                ],
            },
            {
                "id": "gerak-pasangan",
                "title": "Aksi–reaksi: tukar pemberi dan penerima, lalu pisahkan diagram",
                "question": "Jika gaya dua troli sama besar dan berlawanan arah, mengapa keduanya tetap dapat bergerak?",
                "explain": [
                    "Saat troli A dan B saling mendorong, A memberikan gaya pada B dan B memberikan gaya pada A secara bersamaan. Kedua gaya merupakan satu pasangan interaksi: sama besar, berlawanan arah, dan bekerja pada benda yang berbeda. Cara mencari pasangannya ialah menukar pemberi dan penerima pada kalimat nama gaya. Pasangan ‘A pada B’ adalah ‘B pada A’.",
                    "Karena penerimanya berbeda, kedua gaya tidak dijumlahkan pada satu diagram benda bebas. Diagram A hanya memuat gaya pada A, sedangkan diagram B hanya gaya pada B. Dua gaya itu baru saling meniadakan sebagai gaya internal bila kita meninjau gabungan A+B; itu tidak berarti tiap benda secara terpisah tidak mengalami percepatan. Tentukan sistem sebelum menjumlahkan gaya.",
                    "Besar gaya pasangan tetap sama untuk massa yang berbeda. Jika hanya gaya interaksi mendatar yang bekerja, besar percepatan masing-masing adalah F/mA dan F/mB, arahnya berlawanan. Troli ringan mengalami perubahan kecepatan lebih besar selama selang waktu yang sama. Respons yang berbeda bukan bukti bahwa gaya pasangan berbeda. Lab memakai kedua troli mula-mula diam dan gaya interaksi konstan selama waktu yang dipilih.",
                    "Berat dan normal sebuah troli bukan pasangan aksi–reaksi, walaupun sama besar pada rel mendatar tertentu: keduanya bekerja pada troli yang sama dan berasal dari interaksi berbeda. Pasangan berat ialah gaya gravitasi troli pada Bumi; pasangan normal rel pada troli ialah gaya troli pada rel. Kesamaan besar dan arah berlawanan saja belum cukup; selalu periksa dua benda dalam interaksi yang sama.",
                ],
                "formula": "F(A pada B) = −F(B pada A); jika hanya pasangan ini yang mendatar: aA = −F/mA, aB = +F/mB; v = at jika mula-mula diam.",
                "quantities": ["F: besar gaya interaksi (N)", "mA, mB: massa dua troli, masing-masing > 0 (kg)", "aA, aB: percepatan dua benda (m/s²)", "t: durasi interaksi konstan (s)"],
                "assumptions": ["A di kiri dan B di kanan; keduanya saling mendorong sehingga gaya pada A ke kiri dan pada B ke kanan.", "Troli mula-mula diam pada rel mendatar ideal.", "Gaya interaksi konstan selama t; tidak ada gaya horizontal luar lain.", "Dua troli digambar sebagai dua sistem terpisah sebelum membahas gabungannya."],
                "lab": _lab("reaction", F=12, m1=3, m2=6, t=1),
                "explore": [
                    "Prediksi: jika massa troli kanan digandakan, apakah gaya pada troli kiri dan kanan masih sama besar? Bagaimana percepatan troli kanan?",
                    "Ubah hanya m2 dari 6 kg menjadi 12 kg. Pertahankan F = 12 N, m1 = 3 kg, dan t = 1 s.",
                    "Amati dua panah gaya yang tetap sama panjang dan berlawanan arah, lalu bandingkan a pada kedua troli serta perubahan v masing-masing.",
                    "Jelaskan mengapa gaya pasangan tidak saling meniadakan pada satu troli. Tulis dua kalimat ‘pemberi pada penerima’ dan tunjuk diagram tempat masing-masing gaya berada.",
                ],
                "misconception": {
                    "claim": "Troli lebih berat memberi dorongan lebih besar, dan kedua gaya saling menghapus sehingga tidak ada percepatan.",
                    "explain": "Hukum III menyamakan besar gaya interaksi, bukan percepatannya. Setiap troli menerima satu gaya dari pasangannya dan dihitung dengan massanya sendiri. Gaya yang sama pada massa berbeda menghasilkan percepatan berbeda; gaya pada dua penerima tidak dapat saling menghapus di satu diagram troli.",
                },
                "worked": {
                    "scenario": "Troli A 2 kg di kiri dan B 5 kg di kanan saling mendorong pada rel ideal. Besar gaya interaksi 10 N. Tentukan percepatan B dan jelaskan kesamaan besar gaya pasangan.",
                    "steps": [
                        "Model: pisahkan sistem A dan sistem B; kanan positif. Hanya gaya interaksi mendatar yang bekerja.",
                        "Data: mA = 2 kg, mB = 5 kg, besar F = 10 N.",
                        "Diagram: B menerima gaya A pada B sebesar +10 N. A menerima gaya B pada A sebesar −10 N; kedua panah berada pada benda berbeda.",
                        "Persamaan: Hukum III memberi F(A pada B) = −F(B pada A); Hukum II pada B memberi aB = +10/5.",
                        "Hitung: aB = +2 m/s²; sebagai pembanding aA = −10/2 = −5 m/s².",
                        "Makna: B dipercepat ke kanan, A ke kiri. Besar gaya sama, tetapi A yang lebih ringan mengalami besar percepatan lebih tinggi.",
                        "Cek: mA|aA| = 2 × 5 = 10 N dan mB|aB| = 5 × 2 = 10 N; dua diagram memenuhi gaya pasangan sama besar.",
                    ],
                    "result": "aB = +2 m/s²; gaya pasangan 10 N pada setiap benda, berlawanan arah.",
                },
                "checks": [
                    _c("f-mek-2-CP4-1", "gerak-pasangan", "Troli A mendorong B 18 N ke kanan. Manakah pasangan reaksinya?", ["B mendorong A 18 N ke kiri.", "Bumi menarik B 18 N ke bawah.", "Rel mendorong B 18 N ke atas."], 0, "Tukar pemberi dan penerima pada interaksi yang sama: A pada B berpasangan dengan B pada A, bekerja pada benda berbeda.", seconds=120, diagram=_lab("reaction", F=18, m1=3, m2=6, t=1)),
                    _n("f-mek-2-CP4-2", "gerak-pasangan", "A bermassa 3 kg di kiri dan B 6 kg di kanan saling mendorong dengan gaya interaksi 18 N pada rel ideal. Kanan positif. Berapa percepatan A?", "aA", -6, "m/s²", explain="A menerima gaya B pada A sebesar −18 N. aA = −18/3 = −6 m/s²; gaya +18 N pada B tidak dijumlahkan pada A.", seconds=180, diagram=_lab("reaction", F=18, m1=3, m2=6, t=1)),
                ],
            },
        ],
        "prediction": [
            _c("f-mek-2-P3-1", "gerak-neto", "Troli sedang ke kanan. Tarikan kiri sedikit lebih besar daripada tarikan kanan. Prediksikan keadaan tepat setelah gaya bekerja selama selang waktu pendek.", ["Dapat tetap ke kanan sambil melambat.", "Pasti langsung ke kiri.", "Pasti diam karena gaya berlawanan."], 0, "Arah perubahan v mengikuti resultan, sedangkan v sesaat juga dipengaruhi v awal. Tuliskan alasan awalmu sebelum memeriksa lab.", seconds=180),
            _c("f-mek-2-P3-2", "gerak-pasangan", "Dua troli berbeda massa saling mendorong pada rel ideal. Troli ringan berubah kecepatannya lebih cepat. Prediksikan besar gaya pasangan selama mereka berinteraksi.", ["Sama besar, walaupun percepatannya berbeda.", "Gaya pada troli ringan selalu lebih kecil.", "Gaya pada troli berat nol karena lebih sulit bergerak."], 0, "Hukum III membandingkan gaya interaksi; Hukum II membandingkan akibat gaya pada massa masing-masing.", seconds=180),
        ],
        "performance": {
            "scenario": "Tim laboratorium menguji troli sensor 5 kg yang mula-mula bergerak +4 m/s. Kabel kanan menarik 10 N dan kabel kiri 20 N selama 1 s pada rel ideal. Seorang teman menggambar tambahan gaya gerak ke kanan dan mengatakan bahwa dua kabel merupakan pasangan aksi–reaksi. Buat laporan koreksi yang dapat dipakai tim untuk memprediksi gerak troli. Lanjutkan dengan model dua troli 5 kg dan 10 kg yang saling mendorong dengan gaya interaksi 20 N.",
            "deliverables": [
                "Diagram benda bebas troli dengan nama pemberi–penerima setiap gaya, serta panah kecepatan yang dipisahkan dari gaya.",
                "Perhitungan resultan bertanda, percepatan, dan satu kecepatan setelah 1 s; jelaskan arah gerak serta perubahan kelajuannya.",
                "Perbandingan dua keadaan lab yang mengubah satu variabel saja, disertai prediksi dan penjelasan dari model.",
                "Dua diagram terpisah untuk troli yang saling mendorong, nama pasangan aksi–reaksi, dan percepatan masing-masing.",
                "Koreksi klaim teman dengan alasan yang menyebut sistem, pemberi gaya, gaya neto, massa, dan dua penerima yang berbeda.",
            ],
            "rubric": {
                "T1": "Masih menganggap kecepatan sebagai gaya atau menggabungkan gaya pada dua benda; diagram dan prediksi memerlukan bantuan langsung.",
                "T2": "Mengenali sebagian pemberi gaya dan memakai ΣF/m, tetapi tanda, hubungan v dengan a, atau pasangan pada dua penerima belum konsisten; alasan belum mendukung hasil.",
                "T3": "Secara mandiri menyajikan diagram lengkap tanpa gaya rekaan, resultan dan percepatan bertanda benar, prediksi v sesuai v awal/waktu, serta pasangan interaksi dan percepatan kedua troli yang benar; asumsi dan satuan jelas.",
                "T4": "Memenuhi T3 lalu menggunakan perubahan satu variabel sebagai bukti, menjelaskan mengapa arah gaya neto tidak harus sama dengan v, dan membedakan penjumlahan pada tiap troli dari pembahasan sistem gabungan.",
            },
        },
    },
}


def _prerequisite(slug, form):
    """Bekal matematika/representasi; tidak mencampur bank materi TP baru."""
    p = f"{slug}-P2-f{form}"
    k = form
    if slug == "f-mek-1-pra":
        a, b, c = 3 * k, 4 * k, 5 * k
        angle = 25 + (form % 5) * 5
        return [
            _n(p + "-1", "bekal-pythagoras", f"Segitiga siku-siku memiliki sisi siku-siku {a} cm dan {b} cm. Berapa panjang sisi miringnya?", "Sisi miring", c, "cm", explain=f"Pythagoras: √({a}² + {b}²) = {c} cm. Sisi miring harus lebih panjang daripada kedua sisi siku-sikunya."),
            _n(p + "-2", "bekal-pythagoras", f"Sebuah segitiga siku-siku mempunyai sisi miring {13*k} cm dan satu sisi siku-siku {5*k} cm. Berapa sisi siku-siku lainnya?", "Sisi yang belum diketahui", 12*k, "cm", explain=f"Sisi lainnya = √(({13*k})² − ({5*k})²) = {12*k} cm. Gunakan pengurangan karena sisi miring sudah diketahui."),
            _c(p + "-3", "bekal-trigonometri", "Pada segitiga siku-siku, sudut α terletak di antara sisi samping dan sisi miring. Perbandingan manakah yang menyatakan cos α?", ["Sisi samping dibagi sisi miring.", "Sisi depan dibagi sisi miring.", "Sisi depan dibagi sisi samping.", "Sisi miring dibagi sisi samping."], 0, "Kosinus adalah samping/miring relatif terhadap sudut yang dipilih. Kata samping selalu memerlukan acuan sudut.", form=form),
            _c(p + "-4", "bekal-trigonometri", "Sisi depan terhadap sudut β panjangnya 6 cm dan sisi miringnya 10 cm. Pernyataan manakah yang benar?", ["sin β = 0,6.", "cos β pasti 0,6.", "sin β = 10/6.", "Sudut β pasti 6°."], 0, "Sinus membandingkan depan/miring, yaitu 6/10 = 0,6. Ini perbandingan panjang, bukan besar sudut dalam derajat.", seconds=180, form=form),
            _n(p + "-5", "bekal-acuan-sudut", f"Satu garis di kuadran kanan atas membuat sudut {angle}° terhadap garis tegak. Berapa sudut lancipnya terhadap garis mendatar?", "Sudut dari mendatar", 90-angle, "°", explain=f"Mendatar dan tegak saling siku-siku, jadi kedua sudut lancip berjumlah 90°: 90 − {angle} = {90-angle}°.", seconds=120),
            _c(p + "-6", "bekal-acuan-sudut", "Angka 40° tertera di dekat garis miring pada suatu gambar. Informasi apa yang perlu dilihat untuk memahami sudut itu?", ["Dua garis yang membatasi busur sudutnya.", "Hanya panjang garis miring.", "Warna garis yang paling terang.", "Angka 40 saja sudah menentukan acuan."], 0, "Sudut menghubungkan dua arah. Cari kedua kaki atau busur sudut, lalu sebut garis acuannya sebelum memakai besar sudut.", form=form),
            _n(p + "-7", "bekal-desimal", f"Hitung {70+10*k} × 0,6.", "Hasil perkalian", (70+10*k)*0.6, explain=f"0,6 berarti enam per sepuluh: ({70+10*k} × 6)/10 = {(70+10*k)*0.6:g}.", seconds=120),
            _n(p + "-8", "bekal-akar", f"Berapa akar kuadrat positif dari {(10+k)**2}?", "Akar kuadrat positif", 10+k, explain=f"{10+k} × {10+k} = {(10+k)**2}. Akar kuadrat positifnya {10+k}.", seconds=120),
        ]
    if slug == "f-mek-2":
        m, delta = 3+k, 2+k
        return [
            _n(p + "-1", "bekal-berat", f"Kotak alat bermassa {m} kg. Gunakan g = 10 m/s². Berapa berat kotak?", "Berat", 10*m, "N", explain=f"W = mg = {m} × 10 = {10*m} N. kg menyatakan massa; newton menyatakan gaya."),
            _n(p + "-2", "bekal-skala-panah", f"Pada diagram, skala 1 petak = {delta} N. Satu gaya besarnya {6*delta} N. Berapa petak panjang panahnya?", "Panjang panah", 6, "petak", explain=f"Panjang = besar gaya/skala = {6*delta}/{delta} = 6 petak.", seconds=120),
            _n(p + "-3", "bekal-jumlah-bertanda", f"Dua panah gaya segaris pada benda yang sama menunjukkan {20+5*k} N ke kanan dan {8+2*k} N ke kiri. Kanan positif. Berapa jumlah bertandanya?", "Jumlah gaya", 12+3*k, "N", explain=f"Jumlah bertanda = +{20+5*k} − {8+2*k} = +{12+3*k} N. Ini operasi penjumlahan vektor bekal."),
            _c(p + "-4", "bekal-satuan", "Manakah satuan SI untuk gaya?", ["newton (N)", "kilogram (kg)", "meter per sekon (m/s)", "meter per sekon kuadrat (m/s²)"], 0, "Gaya diukur dalam N; kg untuk massa, m/s untuk kecepatan, dan m/s² untuk percepatan.", form=form),
            _n(p + "-5", "bekal-perubahan-kecepatan", f"Kecepatan sebuah benda bertambah dari +{k} menjadi +{k+2*delta} m/s dalam 2 s. Berapa percepatan rata-ratanya?", "Percepatan rata-rata", delta, "m/s²", explain=f"a rata-rata = (v akhir − v awal)/Δt = ({k+2*delta} − {k})/2 = {delta} m/s². Ini definisi perubahan kecepatan, bukan perhitungan dari gaya."),
            _n(p + "-6", "bekal-jumlah-searah", f"Dua gaya masing-masing {9+k} N dan {13+k} N sama-sama ke kiri. Kiri dipilih positif. Berapa jumlah bertandanya?", "Jumlah gaya", 22+2*k, "N", explain=f"Kedua gaya searah positif yang dipilih: {9+k} + {13+k} = +{22+2*k} N."),
            _c(p + "-7", "bekal-arah-panah", "Komponen sebuah panah pada sumbu positif ke kanan bernilai negatif. Panah komponen itu menunjuk ke mana?", ["Ke kiri.", "Ke kanan.", "Selalu ke bawah.", "Tidak memiliki arah."], 0, "Tanda negatif menunjukkan arah yang berlawanan dengan sumbu positif. Di sini arah itu kiri.", form=form),
            _n(p + "-8", "bekal-massa", f"Berat sebuah wadah {10*(12+k)} N. Jika g = 10 m/s², berapa massanya?", "Massa", 12+k, "kg", explain=f"m = W/g = {10*(12+k)}/10 = {12+k} kg. Berat dan massa memakai besaran serta satuan berbeda."),
        ]
    raise KeyError(slug)


def _vector_questions(stage, form):
    """Setiap tahap punya naskah sendiri; P9 tidak mengambil potongan P7."""
    p, k = f"f-mek-1-pra-{stage}-f{form}", form
    q = []
    def N(i, indicator, prompt, label, answer, unit="m", **kw):
        q.append(_n(f"{p}-{i}", indicator, prompt, label, answer, unit, **kw))
    def C(i, indicator, prompt, options, answer, explain, **kw):
        q.append(_c(f"{p}-{i}", indicator, prompt, options, answer, explain, form=form, **kw))

    if stage == "P5":
        a, b = 6+k, 8+k
        N(1, "vektor-sambung", f"Robot pembawa kabel menempuh {a} m ke timur lalu {b} m ke utara. Berapa besar perpindahan langsung dari titik awal?", "Besar perpindahan", hypot(a,b), explain=f"Kedua ruas tegak lurus; R = √({a}² + {b}²) ≈ {hypot(a,b):.2f} m, bukan {a+b} m.", diagram=_lab("vector", ax=a, ay=0, bx=0, by=b))
        F = 30+10*k
        N(2, "vektor-acuan", f"Tali menarik ke kanan atas dengan gaya {F} N. Pada gambar, sudut terhadap +y adalah 30°. sin 30° = 0,5. Berapa Fx?", "Fx", F*0.5, "N", explain=f"Sisi x berada di depan sudut dari +y; Fx = {F} sin 30° = {F*0.5:g} N.", diagram=_lab("components", F=F, theta=60, ref="y"))
        N(3, "vektor-tanda", f"Diagram menunjukkan perpindahan A = ({4+k},2) m dan B = (−{7+k},2) m. Berapa besar resultannya?", "Besar R", 5, explain="Rx = −3 m dan Ry = +4 m. Besar resultan √(9 + 16) = 5 m; arahnya kiri atas.", diagram=_lab("vector", ax=4+k, ay=2, bx=-(7+k), by=2), seconds=240)
        W = 70+10*k
        N(4, "vektor-bidang", f"Papan membentuk 60° terhadap mendatar dan berat kotak {W} N. cos 60° = 0,5. Berapa besar komponen berat yang tegak lurus menuju bidang?", "Besar W tegak lurus", W*0.5, "N", explain=f"Komponen menuju bidang menempel sudut pada segitiga berat: W⊥ = {W} cos 60° = {W*0.5:g} N.", diagram=_lab("incline", W=W, theta=60))
        C(5, "vektor-acuan", "Pada vektor yang tetap menunjuk kanan atas, label sudut berubah dari 60° terhadap +x menjadi 30° terhadap +y. Alasan mana yang benar untuk komponen x?", ["F cos 60° = F sin 30°, sehingga Fx tetap.", "Angka sudut lebih kecil selalu membuat Fx lebih kecil.", "Fx menjadi Fy karena nama acuan berubah.", "Fx harus sama dengan besar F karena vektor tetap."], 0, "Dua label menyatakan vektor yang sama. Sisi mendatar menempel pada sudut dari x dan berhadapan dengan sudut dari y.", seconds=180)
    elif stage == "P7":
        a, b = 3*k, 4*k
        N(1, "vektor-sambung", f"Peta latihan robot menunjukkan A {a} m ke timur dan B {b} m ke utara. Berapa besar satu perpindahan penggantinya?", "Besar R", 5*k, explain=f"R = √({a}² + {b}²) = {5*k} m. Panah R menghubungkan awal A dengan akhir B.", diagram=_lab("vector", ax=a, ay=0, bx=0, by=b))
        C(2, "vektor-sambung", f"Robot menempuh {7+k} m ke utara, lalu {7+k} m ke selatan. Penjelasan mana yang sesuai dengan panah hasil?", ["Resultan nol karena ujung rute kembali ke titik awal.", "Resultan dua kali panjang satu ruas karena kedua ruas ditempuh.", "Resultan ke selatan karena arah terakhir selalu menentukan.", "Resultan ke utara karena arah awal selalu menentukan."], 0, "Kedua vektor sama besar dan berlawanan; jarak tempuh bukan besar perpindahan.", diagram=_lab("vector", ax=0, ay=7+k, bx=0, by=-(7+k)))
        F = 20+10*k
        N(3, "vektor-acuan", f"Penarik alat memberi gaya {F} N dengan arah 60° dari +x. cos 60° = 0,5. Berapa Fx?", "Fx", F/2, "N", explain=f"Sudut diukur dari +x; Fx = F cos 60° = {F/2:g} N.", diagram=_lab("components", F=F, theta=60, ref="x"))
        N(4, "vektor-acuan", f"Gaya {F} N yang sama diarahkan 30° terhadap +y di kuadran kanan atas. sin 30° = 0,5. Berapa Fx?", "Fx", F/2, "N", explain=f"Fx = F sin 30° = {F/2:g} N. Ini sama dengan sudut 60° dari +x; acuannya berbeda, vektornya sama.", diagram=_lab("components", F=F, theta=60, ref="y"))
        N(5, "vektor-tanda", f"Robot bergerak A = ({6+k},3) m lalu B = (−{10+k},0) m. Berapa komponen x resultan?", "Rx", -4, explain=f"Rx = ({6+k}) − ({10+k}) = −4 m. Pertahankan tanda arah barat sebelum menjumlah.", diagram=_lab("vector", ax=6+k, ay=3, bx=-(10+k), by=0))
        N(6, "vektor-tanda", f"Dua perpindahan ialah A = (−{5+k},−2) m dan B = ({2+k},−2) m. Berapa besar R?", "Besar R", 5, explain="Rx = −3 m, Ry = −4 m; √(9 + 16) = 5 m. Kedua tanda negatif menentukan arah barat daya.", diagram=_lab("vector", ax=-(5+k), ay=-2, bx=2+k, by=-2), seconds=240)
        C(7, "vektor-tanda", "Sebuah hasil mempunyai Rx negatif dan Ry positif. Penentuan arah manakah yang sesuai?", ["Kiri atas; sudut lancip hasil perbandingan komponen harus ditempatkan di kuadran itu.", "Kanan atas karena semua panjang positif.", "Kiri bawah karena ada satu tanda negatif.", "Arah tidak dapat diketahui sama sekali dari tanda komponen."], 0, "Rx < 0 berarti kiri dan Ry > 0 berarti atas. Menghitung besar dengan kuadrat tidak mengubah kuadran.", seconds=180)
        W=80+20*k
        N(8, "vektor-bidang", f"Kotak alat beratnya {W} N di papan 30° terhadap mendatar. sin 30° = 0,5. Berapa besar komponen berat menuruni papan?", "Besar W sejajar", W/2, "N", explain=f"W∥ = W sin θ = {W} × 0,5 = {W/2:g} N, menurun.", diagram=_lab("incline", W=W, theta=30))
        N(9, "vektor-bidang", f"Kotak yang beratnya {W} N diletakkan pada papan 60° terhadap mendatar. cos 60° = 0,5. Berapa besar komponen berat menuju papan?", "Besar W tegak lurus", W/2, "N", explain=f"Komponen menuju bidang adalah W cos θ = {W/2:g} N. Ini komponen berat; identitas gaya normal harus ditentukan terpisah.", diagram=_lab("incline", W=W, theta=60))
        C(10, "vektor-acuan", "Pada satu segitiga komponen, Fx = 12 N dan Fy = 16 N. Seorang siswa menyatakan F = 28 N. Koreksi mana yang tepat?", ["F = 20 N karena komponen saling tegak lurus dan harus diperiksa dengan Pythagoras.", "F = 28 N karena gaya selalu dijumlah panjangnya.", "F = 4 N karena semua komponen harus dikurangkan.", "F tidak dapat diperiksa dari kedua komponen."], 0, "√(12² + 16²) = √400 = 20 N. Komponen orthogonal tidak dijumlah sebagai besar skalar.", seconds=180)
    elif stage == "P9":
        # Konteks survei baru, nilai dan tuntutan berbeda dari latihan robot P7.
        a, b = 5*(k+1), 12*(k+1)
        N(1, "vektor-sambung", f"Perahu survei berpindah {a} m ke barat lalu {b} m ke selatan. Petugas mengukur garis lurus dari posisi berangkat ke posisi akhir. Berapa panjang garis itu?", "Besar perpindahan survei", 13*(k+1), explain=f"R = √({a}² + {b}²) = {13*(k+1)} m. R mengarah barat daya; panjang dua ruas tidak langsung menjadi panjang diagonal.", diagram=_lab("vector", ax=-a, ay=0, bx=0, by=-b), seconds=240)
        C(2, "vektor-sambung", f"Dua tahap pemetaan sepanjang {9+2*k} m dan {4+k} m sama-sama menuju barat. Mengapa besar resultannya boleh dijumlah langsung?", ["Karena kedua panah searah dan segaris.", "Karena penjumlahan vektor selalu sama dengan penjumlahan panjang.", "Karena arah barat selalu bernilai positif.", "Karena urutan tahap menentukan besar resultan."], 0, "Penjumlahan besar sah pada keadaan searah; untuk arah lain diperlukan geometri atau komponen.", diagram=_lab("vector", ax=-(9+2*k), ay=0, bx=-(4+k), by=0), seconds=180)
        F=55+10*k
        N(3, "vektor-acuan", f"Kabel alat ukur menarik {F} N ke kanan atas. Busur sudut pada diagram berangkat dari +y dan besarnya 60°. cos 60° = 0,5. Berapa komponen tegaknya?", "Fy", F/2, "N", explain=f"Komponen y menempel sudut yang beracuan +y, sehingga Fy = F cos 60° = {F/2:g} N. Komponen mendatar yang memakai sinus.", diagram=_lab("components", F=F, theta=30, ref="y"), seconds=180)
        C(4, "vektor-acuan", f"Panah tarikan {F} N diarahkan tepat ke atas. Seorang petugas memakai Fx = F cos 0° karena sudutnya 0° terhadap +y. Koreksi mana yang tepat?", ["Fx = 0; sudut 0° dari +y membuat komponen x berada di depan sudut.", "Fx = F; kosinus selalu untuk mendatar.", "Fx = −F; arah atas berarti x negatif.", "Fx dan Fy masing-masing F/2."], 0, "Vektor vertikal tidak memiliki proyeksi mendatar. Pada acuan y, Fx = F sin 0° = 0, sedangkan Fy = F.", diagram=_lab("components", F=F, theta=90, ref="y"), seconds=180)
        N(5, "vektor-tanda", f"Pergeseran pelampung dicatat A = ({8+k},−5) m dan B = (−{14+k},−3) m. Berapa besar perpindahan gabungan?", "Besar R", 10, explain="Rx = −6 m dan Ry = −8 m. Besar R = √(36 + 64) = 10 m; arah kiri bawah.", diagram=_lab("vector", ax=8+k, ay=-5, bx=-(14+k), by=-3), seconds=240)
        C(6, "vektor-tanda", f"Peta dua langkah A = (−{4+k},4) m dan B = ({4+k},−{7+k}) m terlihat pada diagram. Arah resultan mana yang benar?", ["Tepat ke selatan karena komponen x habis dan komponen y negatif.", "Tepat ke utara karena langkah A ke atas.", "Ke timur laut karena besar kedua x sama.", "Resultan nol karena kedua x saling menghapus."], 0, f"Rx = 0; Ry = 4 − {7+k} = −{3+k} m. Hilangnya komponen x tidak otomatis menghapus komponen y.", diagram=_lab("vector", ax=-(4+k), ay=4, bx=4+k, by=-(7+k)), seconds=240)
        W=130+20*k
        N(7, "vektor-bidang", f"Wadah sampel berbobot {W} N diletakkan pada jalur 60° terhadap mendatar. Diberikan sin 60° ≈ 0,866025. Berapa besar komponen berat sepanjang jalur?", "Besar W sejajar", W*sin(radians(60)), "N", explain=f"W∥ = W sin 60° ≈ {W*sin(radians(60)):.2f} N. Komponen ini mengarah turun sepanjang jalur.", diagram=_lab("incline", W=W, theta=60), seconds=240, tol=0.12)
        C(8, "vektor-bidang", "Dalam inspeksi ramp, petugas menambah sudut papan dari 30° menjadi 60° tanpa mengganti wadah. Pernyataan mana yang sesuai dengan proyeksi berat?", ["Komponen sejajar membesar, komponen menuju bidang mengecil, berat tetap vertikal.", "Kedua komponen membesar karena papan lebih curam.", "Berat berputar agar selalu tegak lurus papan.", "Komponen sejajar tetap karena massa tetap."], 0, "Pada 0°–90°, sin θ membesar dan cos θ mengecil ketika θ bertambah. W tetap; yang berubah ialah proyeksi terhadap sumbu yang diputar.", diagram=_lab("incline", W=W, theta=60), seconds=240)
    elif stage == "P10":
        a,b=8+2*k,15+2*k
        N(1, "vektor-sambung", f"Setelah jeda belajar, baca rute pemindai: {a} m ke utara, lalu {b} m ke timur. Berapa besar perpindahan langsung?", "Besar perpindahan", hypot(a,b), explain=f"Dua arah ortogonal: R = √({a}² + {b}²) ≈ {hypot(a,b):.2f} m.", diagram=_lab("vector", ax=0, ay=a, bx=b, by=0))
        F=24+12*k
        N(2, "vektor-acuan", f"Satu gaya {F} N menunjuk kanan atas dan membuat 60° terhadap +y. cos 60° = 0,5. Berapa komponen y?", "Fy", F/2, "N", explain=f"Sisi y menempel sudut dari +y: Fy = F cos 60° = {F/2:g} N.", diagram=_lab("components", F=F, theta=30, ref="y"))
        C(3, "vektor-tanda", f"A = ({5+k},−4) m dan B = (−{5+k},1) m. Arah mana yang sesuai dengan jumlah komponen?", ["Selatan, karena R = (0,−3) m.", "Utara, karena komponen B ke atas.", "Timur, karena A digambar lebih dulu.", "Tidak ada perpindahan, karena x habis."], 0, "Komponen x saling menghapus; y tetap −4 + 1 = −3 m. Periksa kedua sumbu, bukan satu saja.", diagram=_lab("vector", ax=5+k, ay=-4, bx=-(5+k), by=1), seconds=180)
        W=60+30*k
        N(4, "vektor-bidang", f"Kotak beratnya {W} N di ramp 30° terhadap mendatar. Dengan sin 30° = 0,5, berapa besar komponen berat menuruni ramp?", "Besar W sejajar", W/2, "N", explain=f"W∥ = W sin 30° = {W/2:g} N; uji ramp datar memberi komponen sejajar nol.", diagram=_lab("incline", W=W, theta=30))
    else:
        raise ValueError(f"Tahap tidak didukung: {stage}")
    return q


def _motion_questions(stage, form):
    p, k = f"f-mek-2-{stage}-f{form}", form
    q = []
    def N(i, indicator, prompt, label, answer, unit="", **kw):
        q.append(_n(f"{p}-{i}", indicator, prompt, label, answer, unit, **kw))
    def C(i, indicator, prompt, options, answer, explain, **kw):
        q.append(_c(f"{p}-{i}", indicator, prompt, options, answer, explain, form=form, **kw))

    if stage == "P5":
        C(1, "gerak-pemberi", "Setelah tangan lepas, troli bergerak pada rel mendatar dengan hambatan diabaikan. Diagram hanya memuat berat Bumi dan normal rel. Apakah perlu menambahkan panah gaya searah gerak?", ["Tidak; gerak bukan interaksi pemberi gaya.", "Ya; troli bergerak berarti pasti ada gaya gerak.", "Ya; dorongan tangan tersimpan di dalam troli.", "Tidak ada gaya sama sekali karena tangan lepas."], 0, "Berat dan normal tetap merupakan gaya pada troli. Tidak ada interaksi tangan sesudah lepas, dan v bukan gaya.", seconds=180, diagram=_lab("motion", right=0, left=0, m=4, v0=2+k, t=1))
        m=3+k; right=4+k; left=right+2*m; v0=5+k
        C(2, "gerak-neto", f"Troli {m} kg mula-mula +{v0} m/s. Kabel kanan {right} N dan kiri {left} N tetap bekerja selama 1 s. Bagaimana gerak setelah 1 s?", ["Masih ke kanan sambil melambat.", "Sudah pasti ke kiri karena gaya neto negatif.", "Diam karena ada dua gaya berlawanan.", "Makin cepat ke kanan karena v awal positif."], 0, f"ΣFx = −{2*m} N, a = −2 m/s², sehingga v = {v0} − 2 = +{v0-2} m/s. Gaya neto mengubah v, bukan menggantinya seketika.", level="C4", seconds=240, diagram=_lab("motion", right=right, left=left, m=m, v0=v0, t=1))
        N(3, "gerak-massa", f"Dua kabel memberi {12+4*k} N ke kanan dan {4+2*k} N ke kiri pada troli bermassa {4+k} kg. Kanan positif. Berapa percepatan troli?", "a", 2, "m/s²", explain=f"ΣFx = ({12+4*k}) − ({4+2*k}) = {8+2*k} N. a = ({8+2*k})/({4+k}) = +2 m/s².", diagram=_lab("motion", right=12+4*k, left=4+2*k, m=4+k, v0=0, t=1))
        C(4, "gerak-pasangan", "Troli A menarik kabel B. Manakah gaya pasangan reaksinya?", ["Kabel B menarik troli A.", "Bumi menarik troli A.", "Rel menopang troli A.", "Troli A menarik Bumi."], 0, "Nama interaksi yang sama dibalik pemberi–penerimanya. Pasangan bekerja pada dua benda berbeda.", seconds=120)
        C(5, "gerak-massa", "Dua troli mula-mula sama-sama diam. Resultan horizontal dan durasi gaya sama; massa troli kedua dua kali yang pertama. Kesimpulan mana yang didukung model?", ["Percepatan serta perubahan kecepatan troli kedua separuh troli pertama.", "Gaya pada troli kedua otomatis dua kali karena massanya lebih besar.", "Percepatan keduanya sama karena resultan sama.", "Troli kedua tidak mungkin bergerak."], 0, "a = ΣF/m dan Δv = at. Gaya neto serta t dikendalikan, maka menggandakan m membagi dua a dan Δv.", level="C4", seconds=240)
    elif stage == "P7":
        C(1, "gerak-pemberi", "Dalam latihan rel, troli ditarik dua kabel sambil bergerak ke kanan. Seorang siswa menambahkan gaya gerak ke kanan pada diagram. Alasan koreksi mana yang benar?", ["Setiap gaya perlu pemberi; keadaan bergerak tidak menambah interaksi baru.", "Panah gaya hanya boleh digambar jika benda diam.", "Gaya ke kanan tidak pernah ada saat benda bergerak.", "Semua gaya pada benda bergerak bernilai nol."], 0, "Tarikan kabel sah karena memiliki pemberi. Panah tambahan yang hanya berasal dari arah v tidak memiliki pemberi.", seconds=180)
        r=18+3*k; l=6+k
        N(2, "gerak-neto", f"Troli latihan menerima {r} N ke kanan dari kabel A dan {l} N ke kiri dari kabel B. Kanan positif. Berapa gaya netonya?", "ΣFx", r-l, "N", explain=f"ΣFx = +{r} − {l} = +{r-l} N; kedua gaya bekerja pada troli yang sama.", diagram=_lab("motion", right=r, left=l, m=4+k, v0=1, t=1))
        C(3, "gerak-neto", "Troli bergerak −3 m/s. Kedua kabel sekarang sama-sama menarik 12 N ke arah berlawanan. Apa yang terjadi pada kecepatan jika hambatan lain diabaikan?", ["Tetap −3 m/s selama resultan nol.", "Langsung nol karena kedua gaya saling menyeimbangkan.", "Bertambah ke kanan karena kanan positif.", "Berubah ke kiri makin cepat karena v negatif."], 0, "ΣFx = 0 memberi a = 0. Kecepatan negatif yang sudah dimiliki tetap, bukan otomatis menjadi nol.", diagram=_lab("motion", right=12, left=12, m=4+k, v0=-3, t=2), seconds=180)
        m=4+k; r=5+k; l=r+2*m
        N(4, "gerak-massa", f"Massa troli {m} kg; kabel kanan {r} N dan kiri {l} N. Kanan positif. Berapa a?", "a", -2, "m/s²", explain=f"ΣFx = {r} − {l} = −{2*m} N, sehingga a = −{2*m}/{m} = −2 m/s².", diagram=_lab("motion", right=r, left=l, m=m, v0=6, t=1))
        C(5, "gerak-neto", "Troli mula-mula +6 m/s dan memiliki a = −2 m/s² yang tetap selama 1 s. Pernyataan mana yang tepat?", ["Kecepatan menjadi +4 m/s; masih kanan tetapi lebih lambat.", "Kecepatan langsung −2 m/s karena a negatif.", "Kecepatan menjadi +8 m/s karena percepatan selalu menambah kelajuan.", "Kecepatan nol karena arah a melawan arah v."], 0, "v = 6 + (−2)(1) = +4 m/s. Tanda a negatif berarti perubahan v ke kiri, bukan otomatis v negatif.", level="C4", seconds=240)
        C(6, "gerak-massa", "Tarikan kanan dan kiri ditahan tetap. Massa troli dinaikkan dari 4 kg menjadi 12 kg. Jika resultan awal tidak nol, bagaimana percepatan barunya?", ["Sepertiga percepatan semula, dengan arah sama.", "Tiga kali percepatan semula.", "Tetap karena gaya tidak berubah.", "Arah berbalik karena massa bertambah."], 0, "Massa naik tiga kali sedangkan resultan sama: a baru = ΣF/(3m) = a lama/3. Massa positif tidak membalik tanda a.", level="C4", seconds=240)
        C(7, "gerak-pasangan", "Dua troli A dan B saling mendorong. Mengapa gaya A pada B dan B pada A tidak dijumlah untuk mendapatkan resultan pada A?", ["Karena gaya A pada B bekerja pada B, di luar diagram benda A.", "Karena gaya reaksi muncul sesudah aksi selesai.", "Karena gaya pada B selalu lebih kecil.", "Karena hukum Newton tidak berlaku untuk A."], 0, "Resultan pada A hanya menjumlah gaya yang penerimanya A. Kedua gaya pasangan muncul bersamaan pada dua penerima berbeda.", level="C4", seconds=240, diagram=_lab("reaction", F=12+2*k, m1=3+k, m2=6+k, t=1))
        F=12+6*k; m2=6+3*k
        N(8, "gerak-pasangan", f"Troli kiri dan kanan saling mendorong dengan gaya interaksi {F} N. Troli kanan bermassa {m2} kg, dan kanan positif. Berapa percepatan troli kanan bila tidak ada gaya horizontal lain?", "a kanan", 2, "m/s²", explain=f"Troli kanan menerima gaya +{F} N dari troli kiri, maka a = {F}/{m2} = +2 m/s². Gaya pada troli kiri berada di diagram lain.", diagram=_lab("reaction", F=F, m1=3+k, m2=m2, t=1))
        C(9, "gerak-pasangan", "Troli diam pada rel. Berat dari Bumi dan normal dari rel sama besar. Mengapa keduanya bukan pasangan aksi–reaksi?", ["Karena keduanya bekerja pada troli yang sama dan berasal dari dua interaksi berbeda.", "Karena gaya aksi–reaksi tidak boleh sama besar.", "Karena normal hanya muncul ketika troli bergerak.", "Karena gravitasi tidak memiliki pasangan reaksi."], 0, "Pasangan berat adalah tarikan troli pada Bumi; pasangan normal adalah gaya troli pada rel. Dua gaya pada satu troli dapat seimbang tanpa merupakan pasangan Hukum III.", level="C4", seconds=240)
        N(10, "gerak-massa", f"Troli {5+k} kg mula-mula diam. Kabel kanan {22+4*k} N dan kiri {2} N menarik tetap selama 2 s. Kanan positif. Berapa kecepatannya sesudah 2 s?", "v setelah 2 s", 8, "m/s", explain=f"Resultan = {20+4*k} N, a = ({20+4*k})/({5+k}) = 4 m/s²; v = 0 + 4 × 2 = +8 m/s.", seconds=240, diagram=_lab("motion", right=22+4*k, left=2, m=5+k, v0=0, t=2))
    elif stage == "P9":
        # P9 memakai robot servis, kapsul, dan bantalan udara; tidak menyalin P7.
        C(1, "gerak-pemberi", "Robot servis meluncur ke kiri setelah lengan pendorong terlepas pada lantai mendatar ideal. Seorang teknisi menggambar gaya sisa dari lengan ke kiri. Penilaian mana yang benar?", ["Hapus gaya sisa; setelah lepas tidak ada interaksi lengan pada robot.", "Pertahankan; setiap gerak menyimpan gaya dari pendorong.", "Ganti dengan gaya ke kanan agar robot dapat melambat.", "Hapus juga berat karena robot sedang meluncur."], 0, "Pemberi harus masih berinteraksi. Berat Bumi dan normal lantai tetap ada; tidak ada alasan menambahkan gaya horizontal tanpa pemberi.", level="C4", seconds=240, diagram=_lab("motion", right=0, left=0, m=6+k, v0=-4, t=1))
        m=6+k; r=8+k; l=r+3*m; v0=7+k
        N(2, "gerak-massa", f"Kapsul uji bermassa {m} kg mendapat tarikan aktuator kanan {r} N dan kiri {l} N. Kanan positif. Tentukan percepatannya.", "a kapsul", -3, "m/s²", explain=f"Resultan = {r} − {l} = −{3*m} N; a = −{3*m}/{m} = −3 m/s².", seconds=240, diagram=_lab("motion", right=r, left=l, m=m, v0=v0, t=1))
        C(3, "gerak-neto", f"Kapsul tadi mulai dengan v0 = +{v0} m/s. Dua tarikan pada diagram bertahan 1 s. Kesimpulan mana yang menghubungkan gaya dan geraknya dengan benar?", ["Resultan ke kiri, tetapi kapsul masih ke kanan dengan kelajuan berkurang.", "Resultan ke kiri membuat v langsung negatif.", "Kapsul pasti diam karena gaya kiri melawan geraknya.", "Kapsul makin cepat ke kanan karena massa positif."], 0, f"a = −3 m/s² dan v = {v0} − 3 = +{v0-3} m/s. Resultan menentukan perubahan v; v awal menentukan apakah tanda v sudah berbalik.", level="C4", seconds=300, diagram=_lab("motion", right=r, left=l, m=m, v0=v0, t=1))
        C(4, "gerak-neto", "Wahana mini di jalur lurus sudah bergerak ke kiri ketika dua aktuator diatur sama besar berlawanan. Apa kesimpulan yang benar jika gaya lain mendatar diabaikan?", ["Kecepatan ke kiri bertahan karena percepatan nol.", "Wahana seketika diam karena resultan nol.", "Wahana berbelok ke kanan karena gaya kanan masih ada.", "Massa menentukan apakah gaya kiri lebih besar."], 0, "Resultan horizontal nol. Hukum I mempertahankan keadaan gerak; massa positif apa pun tidak membuat resultan tak nol dari dua gaya sama besar.", seconds=180, diagram=_lab("motion", right=17+k, left=17+k, m=5+k, v0=-5, t=2))
        C(5, "gerak-massa", "Dua kapsul pada bantalan udara menerima resultan sama selama 2 s dan mula-mula diam. Kapsul P bermassa 3 kg, Q 9 kg. Klaim mana yang benar?", ["Perubahan kecepatan P tiga kali Q karena a = ΣF/m.", "Gaya pada Q tiga kali P karena massa Q lebih besar.", "Perubahan kecepatan sama karena waktu sama.", "Q berubah arah percepatan karena massanya lebih besar."], 0, "aP/aQ = mQ/mP = 3. Durasi sama memberi rasio Δv yang sama dengan rasio a. Resultan sama merupakan data yang harus dipertahankan.", level="C4", seconds=240)
        C(6, "gerak-pasangan", "Dalam uji magnet, kereta P menarik Q ke kiri dengan 16 N. Pasangan Hukum III yang benar adalah…", ["Q menarik P ke kanan 16 N, pada kereta P.", "Lantai menekan Q ke atas 16 N, pada kereta Q.", "Bumi menarik Q ke bawah 16 N, pada kereta Q.", "P menarik Q ke kiri dengan gaya tambahan 16 N."], 0, "Tukar pemberi dan penerima pada interaksi magnet yang sama. Arah berlawanan dan besar sama; pasangan berada pada P, bukan dua gaya pada Q.", seconds=180)
        F=20+10*k; ma=4+2*k; mb=10+5*k
        N(7, "gerak-pasangan", f"Dua kapsul mula-mula diam saling mendorong di bantalan udara. Kapsul kiri bermassa {ma} kg, kanan {mb} kg, gaya interaksi {F} N selama 2 s. Kanan positif. Berapa kecepatan kapsul kiri setelah 2 s?", "v kiri", -10, "m/s", explain=f"Gaya pada kapsul kiri = −{F} N. a kiri = −{F}/{ma} = −5 m/s²; v = 0 + (−5)(2) = −10 m/s. Gaya pada kapsul kanan tidak dijumlah pada kiri.", level="C4", seconds=300, diagram=_lab("reaction", F=F, m1=ma, m2=mb, t=2))
        C(8, "gerak-pasangan", "Sebuah kotak peralatan diam pada meja. Pasangan reaksi terhadap gaya gravitasi Bumi pada kotak adalah…", ["Gaya gravitasi kotak pada Bumi.", "Gaya normal meja pada kotak.", "Gaya kotak pada meja akibat kontak.", "Resultan berat dan normal pada kotak."], 0, "Interaksi gravitasi Bumi–kotak dipasangkan dengan menukar pemberi dan penerima. Normal berasal dari interaksi meja–kotak dan bekerja pada kotak yang sama seperti berat.", level="C4", seconds=240)
    elif stage == "P10":
        C(1, "gerak-pemberi", "Pada pemindai bergerak, diagram gaya memuat panah ‘kecepatan 4 m/s’ bersama dua tarikan kabel. Bagaimana memperbaikinya?", ["Pisahkan panah kecepatan dari diagram penjumlahan gaya; v bukan gaya.", "Ubah unit panah kecepatan menjadi N tanpa mengubah nilainya.", "Tambahkan berat pada arah kecepatan.", "Hapus semua tarikan karena pemindai sudah bergerak."], 0, "Kecepatan dan gaya adalah besaran berbeda. Diagram gaya memerlukan panah berunit N dengan pemberi yang jelas.", seconds=180)
        m=3+k; r=7+k; l=r+2*m
        C(2, "gerak-neto", f"Pemindai {m} kg mula-mula −3 m/s, menerima {r} N ke kanan dan {l} N ke kiri. Bagaimana kelajuannya pada 1 s berikutnya?", ["Membesar; v dan a sama-sama ke kiri.", "Mengecil karena semua percepatan negatif berarti melambat.", "Tetap karena sudah bergerak.", "Langsung nol karena kedua gaya berlawanan."], 0, "ΣFx negatif dan a = −2 m/s². v = −3 − 2 = −5 m/s; besar v bertambah dari 3 menjadi 5 m/s.", level="C4", seconds=240, diagram=_lab("motion", right=r, left=l, m=m, v0=-3, t=1))
        N(3, "gerak-massa", f"Massa sebuah kereta uji {7+k} kg. Gaya kanan {24+3*k} N dan kiri 3 N. Kanan positif. Berapa percepatannya?", "a", 3, "m/s²", explain=f"ΣFx = {24+3*k} − 3 = {21+3*k} N. a = ({21+3*k})/({7+k}) = +3 m/s².", diagram=_lab("motion", right=24+3*k, left=3, m=7+k, v0=0, t=1))
        C(4, "gerak-pasangan", "Dua kereta saling mendorong, tetapi massa kanan tiga kali massa kiri. Mana penjelasan yang tepat?", ["Gaya pasangan sama besar; percepatan kereta kanan sepertiga kereta kiri jika tidak ada gaya mendatar lain.", "Gaya pada kereta kanan tiga kali lebih besar sehingga percepatan sama.", "Gaya pasangan saling menghapus pada setiap kereta.", "Gaya dari kereta kiri hilang karena massanya lebih kecil."], 0, "Hukum III memberi kesamaan besar gaya. Hukum II pada tiap penerima memberi a berbanding terbalik dengan massa; gaya pasangan berada pada dua diagram berbeda.", level="C4", seconds=240, diagram=_lab("reaction", F=15+3*k, m1=2+k, m2=3*(2+k), t=1))
    else:
        raise ValueError(f"Tahap tidak didukung: {stage}")
    return q


def make_questions(slug, stage, form=1):
    """Kembalikan salinan bank baru: P2=8, P5=5, P7=10, P9=8, P10=4.

    `form` bilangan bulat positif; variasi numerik dan posisi opsi berubah.
    ID menyertakan slug, tahap, bentuk, dan nomor sehingga tidak bertabrakan.
    """
    if slug not in LESSONS:
        raise KeyError(slug)
    if not isinstance(form, int) or isinstance(form, bool) or form < 1:
        raise ValueError("form harus bilangan bulat positif")
    stage = str(stage).upper()
    if stage == "P2":
        result = _prerequisite(slug, form)
    elif slug == "f-mek-1-pra":
        result = _vector_questions(stage, form)
    else:
        result = _motion_questions(stage, form)
    return deepcopy(result)
