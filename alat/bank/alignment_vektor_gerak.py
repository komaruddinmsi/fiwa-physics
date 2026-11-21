# -*- coding: utf-8 -*-
"""Penyelarasan dua TP awal F.MEK dengan RPP, tanpa mengubah sumber asli.

G1–G8 berasal dari C1.6/C2.6; teks kartu G4/G8 dari D5.5.
RPP D6 berisi kisi pesanan 15 slot/TP, bukan naskah 60 soal yang sudah ada.
Bank di modul ini adalah naskah BARU, bukan kutipan butir gerbang atau HTML.
Kutipan gerbang mempertahankan ucapan 30 detik sebagai data sumber, sedangkan
seconds adalah alokasi digital minimum 120 detik sesuai standar proyek.
G4/G8 adalah bukti transfer pilihan, bukan tambahan syarat lulus T3.
"""

from copy import deepcopy
from math import hypot, sqrt, atan2, degrees, radians, sin, cos

try:
    from .lesson_vektor_gerak import make_questions as _previous_questions
except ImportError:
    try:
        from lesson_vektor_gerak import make_questions as _previous_questions
    except ImportError:
        from alat.bank.lesson_vektor_gerak import make_questions as _previous_questions


STEP_LABELS = ("Apa yang ditanyakan", "Formulasi", "Informasi distraktor",
               "Identifikasi data", "Substitusi", "Penyelesaian", "Kesimpulan")


def _steps(*items):
    if len(items) != 7:
        raise ValueError("Pembahasan memerlukan tujuh langkah konkret")
    return [f"{label}: {item}" for label, item in zip(STEP_LABELS, items)]


def _lab(kind, **params):
    return {"kind": kind, "params": params}


def _worked(scenario, *steps):
    return {"scenario": scenario, "steps": _steps(*steps), "result": steps[-1]}


EXECUTE = {
    "T1": "Belum bisa menguraikan vektor ke komponen atau belum bisa menjumlahkan dua vektor meski dibantu.",
    "T2": "Bisa bila diberi kerangka (\"gambar segitiga komponen dulu; sisi mana sejajar sumbu-x?\") atau contoh sejenis di sampingnya.",
    "T3": "Menguraikan vektor ke Fx = F cos θ, Fy = F sin θ dan menghitung resultan R = √(Rx²+Ry²) beserta arah, benar & tanpa dituntun pada bentuk baku.",
    "T4": "Menjalankan penguraian & penjumlahan vektor pada bentuk yang belum dilatih persis (sudut bukan 37°/53°, tiga vektor sekaligus, satuan campur) tanpa tersendat.",
}
IMPLEMENT = {
    "T1": "Belum menyadari penjumlahan vektor berbeda dari penjumlahan bilangan biasa.",
    "T2": "Perlu dipancing (\"ini vektornya tegak lurus atau bersudut? sumbu mana yang sejajar bidang?\") baru memilih metode tepat.",
    "T3": "Pada satu tugas baru (mis. menguraikan berat pada bidang miring), memilih sumbu & metode yang tepat sendiri lalu menjalankannya benar.",
    "T4": "Pada konfigurasi yang belum dicontohkan (mis. kesetimbangan tiga gaya, bidang miring bersudut baru), memilih & memadukan metode komponen sendiri disertai alasan pemilihan sumbu.",
}
DIFFERENTIATE = {
    "T1": "Belum bisa membedakan gaya dari kecepatan/energi meski dibantu.",
    "T2": "Bisa memilah bila diberi daftar kandidat gaya untuk dicoret/dipertahankan atau diagram gaya setengah jadi.",
    "T3": "Untuk peristiwa yang sudah dibahas, menyebut hanya gaya yang benar-benar bekerja (berat, normal, gesek, tegangan, dorong) dan menolak \"gaya gerak ke depan\", mandiri.",
    "T4": "Pada peristiwa yang belum dibahas (mis. satelit melingkar, penumpang di tikungan), memisahkan gaya nyata dari efek kelembaman/khayalan tanpa dituntun.",
}
ORGANIZE = {
    "T1": "Belum bisa menghubungkan gaya neto dengan keadaan gerak meski dibantu.",
    "T2": "Bisa memetakan bila diberi kerangka diagram gaya berlabel dan rumus ΣF = m·a untuk diisi.",
    "T3": "Menjumlah gaya dengan arah (resultan), menyimpulkan a = ΣF/m, dan mengaitkan keadaan gerak (diam/GLB bila ΣF=0; berubah bila ΣF≠0) pada peristiwa yang dibahas, mandiri.",
    "T4": "Menyusun diagram gaya & hubungan ΣF = m·a untuk sistem baru (mis. dua balok tersambung, lift dipercepat) tanpa dituntun.",
}

_CARD_EXE = "Tiga gaya bekerja pada satu titik (sumbu-x ke timur, sumbu-y ke utara): F₁ = 10 N ke timur; F₂ = 10 N pada sudut 60° di atas sumbu-x (cos 60° = 0,50; sin 60° = 0,87); F₃ = 0,0080 kN ke selatan. Tulis komponen x dan y tiap gaya dalam newton, lalu Rx, Ry, besar R, dan arah R dari sumbu-x. Tulis satu kalimat mengapa Ry hampir nol padahal F₂ cukup besar."
_CARD_IMP = "Sebuah balok berat 80 N diam di atas bidang miring licin bersudut 25° (cos 25° = 0,91; sin 25° = 0,42). Balok ditahan tali yang sejajar bidang. Tentukan tegangan tali dan gaya tekan bidang pada balok (diam → resultan nol). Tulis sumbu yang kamu pilih beserta alasannya, lalu satu kalimat mengapa sumbu mendatar–tegak membuat soal ini lebih panjang."
_CARD_DIF = "Seorang penumpang duduk di mobil yang menikung ke kiri dengan laju tetap; ia terdorong ke kanan sampai menekan pintu. Seorang murid berkata: “Ada gaya sentrifugal ke kanan yang mendorong penumpang.” Gambar diagram gaya mendatar pada penumpang dari sudut pandang jalan (kerangka tanah), sebut gaya nyata beserta pemberinya, tulis arah gaya neto, lalu satu kalimat mengapa “terdorong ke kanan” dapat dijelaskan tanpa gaya ke kanan."
_CARD_ORG = "Dua balok A (3 kg) dan B (2 kg) terhubung tali ringan di lantai licin; tali tidak melar. Balok B ditarik gaya 25 N ke kanan, balok A berada di sisi kiri dan hanya ditarik tali. Tulis diagram gaya mendatar tiap balok, percepatan sistem, dan tegangan tali; lalu satu kalimat mengapa tegangan tali bukan 25 N."


ALIGNMENT = {
    "f-mek-1-pra": {
        "gates": [
            {
                "id": "G1", "title": "Acuan sudut menentukan komponen",
                "process": "Menjalankan (executing)", "seconds": 180,
                "prompt": "» “Papan siap. Sebuah gaya F = 20 N bekerja membentuk sudut 53° di atas mendatar (cos 53° = 0,6; sin 53° = 0,8). Tulis Fx dan Fy dengan satuan, plus satu kalimat: mengapa Fx memakai cos. Tiga puluh detik.” … » “Angkat.”",
                "rubric": deepcopy(EXECUTE),
                "teacher_notes": "Sumber C1.6, paragraf 0943–0948. Harapan: Fx=12 N, Fy=16 N, sisi mendatar menempel sudut dari mendatar; cek √(12²+16²)=20 N. Alasan kosong/tanpa acuan belum memenuhi bukti. Jangan menyamakan angka benar dengan kemandirian. Ucapan 30 detik dipertahankan verbatim; alokasi digital 180 detik. Catat proses, bantuan yang diberikan, dan mode gagal secara terpisah; jangan agregasikan profil proses menjadi satu angka.",
            },
            {
                "id": "G2", "title": "Resultan mempunyai besar dan arah",
                "process": "Menjalankan (executing)", "seconds": 240,
                "prompt": "» “Papan siap. Seorang murid berjalan 6 m ke timur lalu 8 m ke utara. Temannya berkata: ‘Perpindahannya 14 m.’ Tulis besar dan arah perpindahan (tan 53° ≈ 1,33; arah dari timur), plus satu kalimat tanggapan untuk temannya. Tiga puluh detik.” … » “Angkat.”",
                "rubric": deepcopy(EXECUTE),
                "teacher_notes": "Sumber C1.6, paragraf 0950–0955. Harapan 10 m, sekitar 53° dari timur menuju utara; 14 m adalah jarak rute, bukan besar perpindahan rute ini. Jangan menerima 10 m tanpa arah atau tanpa tanggapan. Nilai kemandirian menjalankan prosedur dan letak salahnya; 240 detik digital menggantikan alokasi ucapan 30 detik tanpa mengubah teks kutipan.",
            },
            {
                "id": "G3", "title": "Pilih sumbu menurut bidang",
                "process": "Mengimplementasikan (implementing)", "seconds": 240,
                "prompt": "» “Papan siap. Balok berat W = 100 N diam pada bidang miring 37° (cos 37° = 0,8; sin 37° = 0,6). Tulis komponen sejajar bidang dan komponen tegak lurus bidang dengan satuan, plus satu kalimat: komponen mana yang menarik balok meluncur. Tiga puluh detik.” … » “Angkat.”",
                "rubric": deepcopy(IMPLEMENT),
                "teacher_notes": "Sumber C1.6, paragraf 0957–0962. Harapan besar komponen 60 N menuruni bidang dan 80 N menuju bidang, sumbu sejajar/normal dipilih dengan alasan. Komponen 60 N menyatakan kecenderungan gravitasi; karena balok dinyatakan diam, jangan menyebutnya gaya neto atau memastikan balok benar-benar meluncur. Gaya penahan/gesek tidak diberikan, sehingga nilai normal tidak digeneralisasi pada setiap konfigurasi. Alokasi digital 240 detik; ucapan sumber tetap verbatim.",
            },
            {
                "id": "G4", "title": "Artefak transfer vektor pilihan", "optional": True,
                "process": "Menjalankan (executing) / Mengimplementasikan (implementing)", "seconds": 240,
                "prompt": "2 kartu tingkat 4 tertelungkup di kotak depan: T4-EXE.1 (menjalankan), T4-IMP.1 (mengimplementasikan). Teks kartu pada D5.5; kuncinya pada D5.6. » “Kartu boleh diambil siapa saja yang selesai varian. Tidak ada yang mencatat siapa yang tidak mengambil.”\n\nT4-EXE.1\n" + _CARD_EXE + "\n\nT4-IMP.1\n" + _CARD_IMP,
                "rubric": {key: "Menjalankan: " + EXECUTE[key] + " Mengimplementasikan: " + IMPLEMENT[key] for key in EXECUTE},
                "teacher_notes": "Sumber C1.6 0964–0967 dan D5.5 3543/3546; artefak lengkap, bukan kisi. Pilihan T4, tidak menjadi syarat lulus T3 dan tidak menurunkan T3 bila tidak diambil/belum transfer. 240 detik awal per kartu pilihan, dapat diberi waktu tambahan. Catat hasil per proses yang ditunjukkan kartu. Baca tiga bukti: tanpa dituntun; alasan memakai pembeda yang benar; bertahan saat ditanya kenapa sekali. Kunci EXE memakai trig yang DIBERIKAN: (10,0),(5,8,7),(0,−8) N → (15;0,7) N, R≈15,02 N, arah≈2,67°. Kunci IMP: T=33,6 N, normal=72,8 N dari pembulatan sin/cos sumber, karena licin dan setimbang. Jangan menukar data trig sumber dengan nilai kalkulator lalu menyalahkan perbedaan pembulatan.",
            },
        ],
        "worked": [
            _worked("Robot pemindah alat menempuh 6 m ke timur lalu 8 m ke utara di ruang panjang 20 m. Tentukan besar perpindahannya.",
                    "Cari besar perpindahan dari titik awal ke titik akhir, dalam meter, bukan panjang kedua ruas.",
                    "A dan B tegak lurus. Sambung ujung–pangkal lalu gunakan R=√(A²+B²).",
                    "Panjang ruang 20 m tidak menentukan selisih posisi awal–akhir yang sudah diberikan.",
                    "A=6 m ke timur; B=8 m ke utara; sudut antarruas 90° dan satuan sudah sama.",
                    "R=√(6²+8²)=√(36+64).",
                    "R=√100=10 m; untuk memeriksa arah, tan α=8/6 sehingga α≈53° dari timur menuju utara. Panjang rute 14 m.",
                    "Besar perpindahan 10 m menuju timur laut; 14 m merupakan jarak lintasan. Hasil 10 m berada di antara selisih dan jumlah panjang ruas."),
            _worked("Tali penarik kotak memberi gaya 20 N pada 53° di atas mendatar. Panjang tali 2 m; sin 53°=0,8 dan cos 53°=0,6. Tentukan Fx.",
                    "Cari komponen mendatar gaya tali, Fx, dalam N.",
                    "Sudut beracuan mendatar, sehingga sisi x menempel sudut: Fx=F cos θ. Gambarkan segitiga dengan F sebagai sisi miring.",
                    "Panjang tali 2 m tidak mengubah proyeksi gaya untuk F dan θ yang sudah diketahui.",
                    "F=20 N, θ=53° dari +x, cos θ=0,6; arah gaya kanan atas sehingga Fx positif.",
                    "Fx=20×0,6.",
                    "Fx=12 N. Fy=20×0,8=16 N; √(12²+16²)=20 N, jadi penguraian konsisten.",
                    "Fx=+12 N ke kanan. Kosinus dipilih karena acuan sudut, bukan karena setiap komponen mendatar selalu memakai kosinus."),
            _worked("Gaya A=(16,12) N dan B=(−10,−4) N bekerja pada satu titik sebuah cincin bermassa 3 kg. Tentukan besar resultan kedua gaya.",
                    "Cari besar resultan gaya pada cincin, dalam N.",
                    "Jumlahkan komponen sejenis lengkap dengan tanda: Rx=Ax+Bx, Ry=Ay+By; kemudian R=√(Rx²+Ry²).",
                    "Massa 3 kg baru diperlukan bila mencari percepatan; bukan untuk menjumlah gaya yang telah diketahui.",
                    "Ax=16, Ay=12, Bx=−10, By=−4 N; kanan +x dan atas +y.",
                    "Rx=16−10=6 N; Ry=12−4=8 N; R=√(6²+8²).",
                    "R=√100=10 N; arah kanan atas karena kedua komponen total positif, dengan tan α=8/6.",
                    "Resultan 10 N sekitar 53° di atas +x. Mempositifkan komponen negatif sebelum menjumlah akan mengubah arah gaya B."),
            _worked("Wadah massa 10 kg berada pada papan 37° terhadap mendatar. Panjang papan 3 m; g=10 m/s², sin37°=0,6 dan cos37°=0,8. Tentukan besar komponen berat sejajar papan.",
                    "Cari besar komponen berat menuruni papan, dalam N; bukan gaya neto atau gaya gesek.",
                    "Pilih sumbu sejajar bidang dan normalnya. Berat tetap vertikal; W∥=mg sin θ dan W⊥=mg cos θ.",
                    "Panjang papan 3 m tidak diperlukan karena sudutnya telah diberikan; gaya penahan juga tidak diberikan sehingga gerak aktual belum dapat ditentukan.",
                    "m=10 kg, g=10 m/s², W=100 N, θ=37° dari mendatar, sin θ=0,6.",
                    "W∥=(10×10)×0,6.",
                    "W∥=60 N; W⊥=80 N. Pythagoras memberi √(60²+80²)=100 N, dan batas θ=0° memberi komponen sejajar nol.",
                    "Besar komponen sejajar 60 N menurun. Pada sumbu normal positif keluar bidang, komponen berat normal bertanda −80 N; besarnya tetap 80 N."),
        ],
        "summary": {
            "bigidea": "Satu vektor yang sama harus tetap sama ketika gambar dipindah sejajar atau acuan sudut diganti; hasil berubah bila arah fisik atau sumbu proyeksinya berubah.",
            "rows": [
                {"title": "Ujung–pangkal", "formula": "R=A+B; jika tegak lurus, R²=A²+B²", "meaning": "Resultan menghubungkan awal panah pertama dengan akhir panah kedua; jarak rute menjumlah panjang ruas.", "trap": "Menganggap 6+8=14 sebagai besar perpindahan untuk dua ruas tegak lurus."},
                {"title": "Acuan sudut", "formula": "θ dari +x: Fx=F cosθ, Fy=F sinθ", "meaning": "Samping memakai cos, depan memakai sin. Pada kuadran I, sudut φ dari +y memberi Fx=F sinφ dan Fy=F cosφ.", "trap": "Memakai fungsi tanpa melihat dua garis pembentuk sudut."},
                {"title": "Komponen bertanda", "formula": "Rx=ΣFx; Ry=ΣFy; R=√(Rx²+Ry²)", "meaning": "Jumlahkan sejajar sumbu; tanda komponen menentukan kuadran sebelum sudut arah ditempatkan.", "trap": "Membuat semua komponen positif atau menganggap hasil arctan otomatis menentukan kuadran."},
                {"title": "Bidang miring", "formula": "Besar W∥=W sinθ; besar W⊥=W cosθ", "meaning": "θ adalah sudut bidang terhadap mendatar. Berat tetap vertikal; sumbu dipilih sejajar/normal bidang.", "trap": "Menganggap komponen normal berat selalu sama dengan gaya normal, atau komponen sejajar sudah merupakan gaya neto."},
            ],
            "transfer": "Pada gambar baru, tandai dahulu acuan sudut dan sumbu, samakan satuan, tentukan tanda, lalu pilih penguraian atau segitiga yang sah. Periksa arah, Pythagoras, dan keadaan batas sebelum mempercayai angka.",
            "checklist": ["Saya dapat menunjuk garis acuan sudut tanpa petunjuk.", "Saya menyambung panah tanpa memutar salinannya.", "Saya membedakan jarak lintasan dan besar perpindahan.", "Saya menjumlah komponen dengan tanda serta menempatkan arah pada kuadran benar.", "Saya memilih sumbu bidang dan memeriksa batas datar secara mandiri."],
        },
        "hook": {"title": "Robot dan tali penghubung tujuan", "scene": "Robot sensor menempuh tiga ubin ke timur, lalu empat ubin ke utara. Setiap ubin 1 m. Tali dari tempat berangkat ke posisi akhir dibentangkan, sementara meter rute robot menunjukkan 7 m.", "question": "Sebelum tali diukur, berapa dugaan panjang garis langsung itu dan apa alasanmu?", "options": ["7 m, karena panjang kedua ruas dijumlah.", "5 m, karena garis penghubung menjadi sisi miring segitiga.", "1 m, karena dua panjang ruas harus dikurangkan."], "bridge": "Bedakan perjalanan dari perubahan posisi. Sesudah mencoba dugaan dengan panah, kita akan membaca acuan sudut, memberi tanda komponen, dan memilih sumbu agar hasil perhitungan cocok dengan titik akhir.", "lab": _lab("vector", ax=3, ay=0, bx=0, by=4)},
    },
    "f-mek-2": {
        "gates": [
            {"id": "G5", "title": "Tolak panah yang tidak mempunyai pemberi", "process": "Membedakan (differentiating)", "seconds": 180,
             "prompt": "» “Papan siap. Sebuah bola kasti dilempar lurus ke atas. Di titik tertinggi bola sesaat diam (abaikan hambatan udara). Tulis gaya apa saja yang bekerja pada bola saat naik, plus satu kalimat tanggapan untuk temanmu yang berkata: ‘Bola naik karena masih ada gaya ke atas dari lemparan.’ Tiga puluh detik.” … » “Angkat.”",
             "rubric": deepcopy(DIFFERENTIATE), "teacher_notes": "Sumber C2.6 1574–1579. Hanya berat dari Bumi, ke bawah setelah tangan lepas, termasuk saat v sesaat nol. a tetap g ke bawah. Pertanyaan sumber menyebut puncak tetapi meminta gaya saat naik; periksa konsistensi kedua fase tanpa menambah gaya rekaan. Alasan harus menyebut interaksi tangan sudah berakhir dan kecepatan bukan gaya. Alokasi digital 180 detik; jangan membaca 30 detik pada kutipan sebagai batas otomatis aplikasi."},
            {"id": "G6", "title": "Kesetimbangan dan pasangan dua benda", "process": "Mengorganisasi (organizing)", "seconds": 240,
             "prompt": "» “Papan siap. Sebuah lampu bermassa 2 kg tergantung diam pada seutas tali (g = 10 m/s²). (a) Tulis gaya-gaya pada lampu beserta besarnya. (b) Seorang murid berkata: ‘Berat lampu dan tegangan tali adalah pasangan aksi–reaksi.’ Benarkah? Tulis satu kalimat alasan. Tiga puluh detik.” … » “Angkat.”",
             "rubric": deepcopy(ORGANIZE), "teacher_notes": "Sumber C2.6 1581–1586. Berat Bumi pada lampu 20 N ke bawah dan tegangan tali pada lampu 20 N ke atas. Keduanya seimbang pada penerima sama, bukan pasangan Hukum III. Pasangan berat: lampu pada Bumi; pasangan tegangan: lampu pada tali. Baca alasan dua penerima sebagai bukti, bukan sekadar angka 20. Catat bantuan terpisah. Alokasi digital 240 detik."},
            {"id": "G7", "title": "Dorongan hilang, gesekan masih ada", "process": "Mengorganisasi (organizing)", "seconds": 240,
             "prompt": "» “Papan siap. Sebuah peti 5 kg didorong mendatar dengan gaya 40 N ke kanan; gesekan 15 N ke kiri. (a) Tulis ΣF dan percepatan peti. (b) Dorongan dilepas, gesekan tetap 15 N; seorang murid berkata: ‘Peti langsung berhenti.’ Nilai pernyataan itu dan tulis percepatan sesudah dilepas. Tiga puluh detik.” … » “Angkat.”",
             "rubric": deepcopy(ORGANIZE), "teacher_notes": "Sumber C2.6 1588–1593. Dengan kanan positif: sebelum lepas ΣF=+25 N, a=+5 m/s²; sesudah lepas ΣF=−15 N, a=−3 m/s² selama peti masih meluncur ke kanan. Peti melambat bertahap. Jangan memperpanjang model gesekan kiri sampai memaksa gerak balik setelah berhenti: model kontak harus diperiksa lagi saat v=0. Alokasi digital 240 detik menggantikan alokasi ucapan sumber 30 detik."},
            {"id": "G8", "title": "Artefak transfer Newton pilihan", "process": "Membedakan (differentiating) / Mengorganisasi (organizing)", "seconds": 240, "optional": True,
             "prompt": "2 kartu tingkat 4 tertelungkup di kotak depan: T4-DIF.2 (membedakan), T4-ORG.2 (mengorganisasi). Teks kartu pada D5.5; kuncinya pada D5.6. » “Kartu boleh diambil siapa saja yang selesai varian. Tidak ada yang mencatat siapa yang tidak mengambil.”\n\nT4-DIF.2\n" + _CARD_DIF + "\n\nT4-ORG.2\n" + _CARD_ORG,
             "rubric": {key: "Membedakan: " + DIFFERENTIATE[key] + " Mengorganisasi: " + ORGANIZE[key] for key in DIFFERENTIATE},
             "teacher_notes": "Sumber C2.6 1595–1598 dan D5.5 3549/3552. Dua kartu lengkap dan opsional; bukan tambahan syarat T3. 240 detik awal per kartu pilihan, boleh ditambah. DIF: gunakan kerangka tanah; gaya kontak mendatar dari pintu/jok yang benar-benar berinteraksi membelokkan penumpang ke kiri, tidak ada interaksi nyata pemberi sentrifugal kanan. Sensasi kanan adalah gerak relatif saat mobil berbelok. ORG: sistem A+B memberi a=25/(3+2)=5 m/s²; pada A, T=3×5=15 N; pada B, 25−15=2×5. Pisahkan diagram penerima dan catatan kedua proses. Jangan memakai model reaction (dua benda saling menolak) untuk menggambar dua balok terhubung yang bergerak bersama."},
        ],
        "worked": [
            _worked("Bola sensor 0,2 kg dilempar ke atas dan sudah lepas dari tangan. Ketinggiannya saat diamati 2 m. Abaikan hambatan udara; g=10 m/s². Tentukan gaya nyata pada bola saat masih naik.",
                    "Cari gaya pada bola beserta pemberinya; arah v tidak diminta sebagai gaya.",
                    "Pilih bola sebagai sistem dan daftar interaksi yang masih berlangsung. Setelah kontak tangan berakhir, hanya gravitasi Bumi pada bola.",
                    "Ketinggian 2 m tidak mengubah daftar interaksi atau besar berat pada model g konstan ini.",
                    "m=0,2 kg, g=10 m/s², tangan telah lepas dan hambatan udara diabaikan.",
                    "W=mg=0,2×10 N; tidak ada suku gaya tangan yang masih bekerja.",
                    "Berat 2 N ke bawah. Bola dapat naik dengan v ke atas sambil dipercepat ke bawah; di puncak v=0 tidak menghapus berat.",
                    "Hanya gaya Bumi pada bola, 2 N ke bawah. Tidak ada gaya lempar yang tersimpan atau dibawa bola."),
            _worked("Troli 4 kg mula-mula +6 m/s ditarik kabel kanan 8 N dan kabel kiri 20 N selama 1 s di rel ideal sepanjang 30 m. Tentukan keadaan geraknya sesudah 1 s.",
                    "Tentukan apakah troli masih kanan atau sudah kiri dan apakah kelajuannya bertambah atau berkurang.",
                    "Kanan positif: ΣFx=Fkanan−Fkiri; a=ΣFx/m; untuk gaya konstan, v=v0+at.",
                    "Panjang rel 30 m tidak menentukan a atau v pada interval ini; diasumsikan tidak ada tumbukan ujung rel.",
                    "m=4 kg, Fkanan=8 N, Fkiri=20 N, v0=+6 m/s dan t=1 s. Berat dan normal seimbang.",
                    "ΣFx=8−20=−12 N; a=−12/4; v=6+(−12/4)×1.",
                    "a=−3 m/s² dan v=+3 m/s. Waktu berhenti jika tarikan tetap adalah 2 s, lebih lama daripada waktu pengamatan.",
                    "Troli masih ke kanan sambil melambat, meskipun gaya neto dan percepatan ke kiri."),
            _worked("Peti 5 kg sedang bergeser ke kanan. Dorongan 40 N ke kanan melawan gesekan 15 N ke kiri. Lebar peti 0,6 m. Tentukan percepatannya sebelum dorongan dilepas.",
                    "Cari percepatan mendatar peti, lengkap dengan arah.",
                    "Tinjau satu peti: ΣFx=F−f=ma. Kanan dipilih positif; bukan menjumlah besar dua gaya yang berlawanan.",
                    "Lebar 0,6 m tidak masuk model translasi titik; gaya gesek sudah dinyatakan langsung.",
                    "F=40 N, f=15 N ke kiri, m=5 kg. Arah vertikal seimbang dan peti masih meluncur ke kanan.",
                    "a=(40−15)/5.",
                    "ΣFx=25 N dan a=+5 m/s². Pemeriksaan satuan N/kg=m/s². Sesudah dorongan lepas, persamaan harus ditulis ulang, bukan memakai resultan lama.",
                    "Percepatan sebelum lepas 5 m/s² ke kanan. Dorongan 40 N sendiri bukan gaya neto."),
            _worked("Lampu 2 kg tergantung diam pada tali sepanjang 1,5 m; g=10 m/s². Seorang siswa menyebut berat dan tegangan sebagai aksi–reaksi. Nilai klaim itu.",
                    "Putuskan apakah dua gaya pada lampu merupakan satu pasangan Hukum III dan sebutkan alasan fisiknya.",
                    "Diagram lampu menjumlah gaya pada lampu: T−mg=0. Untuk pasangan Hukum III, tukar pemberi dan penerima dalam interaksi yang sama.",
                    "Panjang tali 1,5 m tidak memengaruhi nilai tegangan pada keadaan diam yang diberikan.",
                    "m=2 kg, g=10 m/s², lampu diam; Bumi memberi berat pada lampu dan tali memberi tegangan pada lampu.",
                    "W=2×10=20 N; T=W=20 N. Nama gaya: Bumi pada lampu dan tali pada lampu.",
                    "Kedua gaya memiliki penerima sama. Pasangan berat ialah lampu pada Bumi; pasangan tegangan ialah lampu pada tali, masing-masing pada benda berbeda dari lampu.",
                    "Klaim siswa salah. Berat dan tegangan seimbang pada lampu, tetapi bukan pasangan aksi–reaksi."),
        ],
        "summary": {
            "bigidea": "Tentukan penerima dan pemberi gaya, jumlahkan hanya gaya pada sistem yang sama, lalu hubungkan resultan dengan perubahan kecepatan dan massa.",
            "rows": [
                {"title": "Pemberi gaya", "formula": "Gaya = interaksi pemberi pada penerima", "meaning": "Kecepatan tidak menjadi panah gaya; kontak yang berakhir tidak meninggalkan gaya tersimpan.", "trap": "Menambahkan gaya gerak karena benda masih bergerak."},
                {"title": "Gaya neto dan v", "formula": "ΣF=0 ⇒ a=0 ⇒ v tetap", "meaning": "Tetap dapat berarti diam atau bergerak lurus beraturan. Jika ΣF≠0, yang ditentukan langsung adalah arah perubahan v.", "trap": "Gaya neto kiri pasti berarti v kiri; atau resultan nol pasti berarti diam."},
                {"title": "Massa dan percepatan", "formula": "a=ΣF/m; jika a konstan, v=v0+at", "meaning": "Massa positif lebih besar memberi percepatan lebih kecil pada resultan sama. Ketika satu gaya hilang, hitung ulang gaya yang tersisa.", "trap": "Membagi gaya terbesar dengan massa, atau menghapus gesekan ketika dorongan lepas."},
                {"title": "Pasangan dua benda", "formula": "F(A pada B)=−F(B pada A)", "meaning": "Besar sama pada dua penerima berbeda; percepatan dapat berbeda karena massa berbeda.", "trap": "Mengira berat dan normal adalah pasangan karena seimbang, atau menghapus pasangan pada satu diagram benda."},
            ],
            "transfer": "Pada peristiwa baru, tulis dulu sistem, kerangka pengamatan, dan daftar interaksi. Pisahkan fase sebelum/sesudah perubahan gaya. Jika memakai gesekan kinetik, periksa kembali model pada saat benda berhenti.",
            "checklist": ["Setiap panah mempunyai pemberi dan penerima.", "Panah v saya pisahkan dari diagram gaya.", "Saya menjumlah gaya dengan arah pada satu benda.", "Saya menyebut pengaruh gaya neto pada perubahan v dengan memperhatikan v awal.", "Saya menemukan pasangan dengan menukar pemberi–penerima, tanpa menggabungkannya pada satu diagram."],
        },
        "hook": {"title": "Kabel dilepas, troli masih melaju", "scene": "Troli sensor sudah bergerak ke kanan di rel ideal. Dua kabel dilepas sekaligus, lalu kamera tetap merekam troli. Seorang pengamat ingin menggambar panah dorongan yang masih tersimpan di dalam troli.", "question": "Apa dugaanmu tentang kecepatan troli setelah kedua tarikan nol dan mengapa?", "options": ["Troli segera diam karena tidak ada tarikan mendatar.", "Troli tetap ke kanan dengan kecepatan tetap karena resultan mendatar nol.", "Troli makin cepat karena dorongan lama tersimpan."], "bridge": "Keadaan bergerak perlu dibedakan dari penyebab perubahan gerak. Kita akan memeriksa pemberi setiap panah, lalu membaca resultan, massa, serta pasangan gaya pada dua benda; penalaran yang sama akan dipakai pada bola yang sudah lepas dari tangan di G5.", "lab": _lab("motion", right=0, left=0, m=4, v0=3, t=1)},
    },
}


def _question(slug, stage, form, number, indicator, prompt, *, answer,
              label="Pilih satu jawaban", unit="", options=None, steps,
              diagram=None, seconds=240, level="C3", tol=0.08):
    if len(steps) != 7 or any(not step.startswith(prefix + ":") for step, prefix in zip(steps, STEP_LABELS)):
        raise ValueError("Urutan tujuh langkah tidak lengkap")
    q = dict(id=f"{slug}-{stage}-rpp-f{form}-{number}", indicator=indicator,
             prompt=prompt, kind="choice" if options is not None else "num",
             label=label, unit=unit, answer=answer, tol=0 if options is not None else tol,
             explain=steps[-1], steps=steps, level=level, seconds=seconds)
    if options is not None:
        shift=(form-1)%len(options)
        q["options"]=list(options[shift:])+list(options[:shift])
        q["answer"]=(int(answer)-shift)%len(options)
    else:
        q["answer"]=round(float(answer),6)
    if diagram is not None:
        q["diagram"]=diagram
    return q


# Rujukan adalah data: array JSON dibaca tanpa menjalankan skrip HTML.
REFERENCE_AUDIT = {
    "practice": "LESSON PLAN/Latihan-TKA-Fisika-F.MEK.html",
    "assessment": "LESSON PLAN/Worksheet-CBT-Fisika-F.MEK-Paket2.html",
    "practice_count": 25, "assessment_count": 25,
    "groups": {"ST1": [1,5], "ST2": [6,17], "ST3": [18,25]},
    "rpp_training": "D6: 4 TP × 15 slot = 60; merupakan kisi/pesanan, naskah belum diproduksi. Tidak sama dengan kedua paket HTML 25 nomor atau bank baru P7 sepuluh nomor per TP.",
    "first_ten": [
        {"no":1,"skill":"Resultan dua gaya tegak lurus","practice_key":"50 kN","assessment_key":"13 kN","mapping":"G2; vektor-sambung"},
        {"no":2,"skill":"Komponen mendatar; sudut dari vertikal","practice_key":"60 N","assessment_key":"120 N","mapping":"G1; vektor-acuan"},
        {"no":3,"skill":"Turunkan berat dan sin sudut dari tinggi/panjang ramp","practice_key":"300 N","assessment_key":"480 N","mapping":"G3; vektor-bidang"},
        {"no":4,"skill":"Tiga gaya dengan komponen bertanda; PGK","practice_key":"A dan D","assessment_key":"B, C, E","mapping":"G2/G4; vektor-tanda; perlu keputusan tunggal baru bila memakai skema num/choice"},
        {"no":5,"skill":"Berat dan angin ortogonal, acuan sudut, massa berubah; BS","practice_key":"B–S–S","assessment_key":"S–B–B","mapping":"G1/G2; vektor-acuan dan vektor-tanda; pecah menjadi keputusan tunggal baru, bukan menyamakan pola kunci"},
        {"no":6,"skill":"Percepatan dari resultan yang sudah diberikan","practice_key":"1,5 m/s²","assessment_key":"2,5 m/s²","mapping":"G7; gerak-massa; tuntutan hitungnya lebih sederhana daripada G7 lengkap"},
        {"no":7,"skill":"GLB, turunkan gesek dan normal lalu μk","practice_key":"0,4","assessment_key":"0,2","mapping":"G7 sebagian; gerak-neto. μk bukan naskah inti G5–G7, perlukan penguatan tersendiri."},
        {"no":8,"skill":"Resultan dorong dikurangi gesek, lalu percepatan","practice_key":"1,5 m/s²","assessment_key":"2,0 m/s²","mapping":"G7; gerak-massa"},
        {"no":9,"skill":"Dua benda bersentuhan, gaya kontak dari satu diagram","practice_key":"60 N","assessment_key":"50 N","mapping":"G8 transfer pilihan; gerak-pasangan/gerak-massa. Lebih luas daripada soal satu benda G7."},
        {"no":10,"skill":"Atwood, dua persamaan Newton, tegangan dinamis","practice_key":"45 N","assessment_key":"42 N","mapping":"Perluasan transfer sesudah G8, bukan syarat G5–G7; jangan menyatakan tercakup hanya karena sudah membahas lampu diam."},
    ],
    "notes": ["Nomor1–10 sejajar keterampilan dan bentuk, tetapi konteks, data, opsi benar, serta hasil berbeda; pembahasan harus dihitung untuk data tiap paket.", "L1–L3 pada HTML adalah level internal paket; bukan padanan otomatis Bloom C1–C3.", "PB pada CBT tidak dipakai sebagai bukti kesepadanan pembahasan; audit ini membandingkan stimulus, tuntutan dan perhitungan baru.", "Keterampilan G5 sumber gaya dan menolak gaya gerak memerlukan butir khusus; nomor6–10 HTML dominan perhitungan dan tidak menggantikan seluruh bukti G5/G6.", "P7 modul ini tetap 10 keputusan tunggal per TP, P9 delapan butir baru. Penguasaan proses RPP tetap dibaca dari artefak dan kemandirian pada gerbang; skor bank tidak otomatis menyatakan T3/T4."],
}
