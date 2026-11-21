"""Penyelarasan F.USE dengan RPP 21-11-2026; sumber dan adaptasi dinyatakan.

Isi gerbang dan tangga D4 bersumber pada RPP-Fisika-FUSE.docx. Pengantar
operasional papan mini/30 detik diganti waktu platform minimal 120 detik.
Contoh, ringkasan, hook dan soal P7/P9 di bawah adalah karya adaptasi baru,
bukan kutipan RPP. G4/G8 kartu transfer opsional, bukan gerbang kelulusan.
"""
from math import sqrt


RUBRICS = {
    "Classifying": {
        "T1": 'Menggolongkan berdasarkan intuisi "kerja keras = usaha besar" meski dibantu, tanpa mengecek arah gaya.',
        "T2": 'Bisa menggolongkan benar bila dipandu ("perhatikan arah gaya terhadap arah gerak").',
        "T3": 'Pada kasus baru dengan gaya jelas sejajar atau tegak lurus perpindahan, menggolongkan benar disertai alasan berbasis arah gaya, mandiri.',
        "T4": 'Pada situasi majemuk belum dicontohkan (gaya bersudut, atau beberapa gaya sekaligus dengan sebagian tegak lurus), menggolongkan tepat mana yang melakukan usaha, disertai perhitungan komponen bila perlu, tanpa dituntun.',
    },
    "Explaining": {
        "T1": 'Tak menghubungkan usaha dengan perubahan energi sama sekali, atau meyakini energi benar-benar lenyap.',
        "T2": 'Bisa menyebut W=ΔEk bila rumus diingatkan, tapi belum menjelaskan ke mana energi pergi tanpa dipandu.',
        "T3": 'Menjelaskan bahwa usaha total = perubahan energi kinetik, dan energi yang tampak hilang (mis. akibat gesekan) sesungguhnya berubah bentuk (kalor/bunyi) — bukan lenyap — pada situasi baru, mandiri.',
        "T4": 'Menjelaskan & memprediksi perubahan energi pada skenario "bagaimana kalau" belum pernah dibahas (mis. gaya bekerja pada arah miring, atau dua gaya berlawanan sekaligus), tetap menjalankan model usaha→ΔEk dengan benar tanpa dituntun.',
    },
    "Planning": {
        "T1": 'Tak membedakan segmen licin dari kasar dalam menyusun rencana, meski dibantu.',
        "T2": 'Bisa menyusun rencana benar bila segmen "mana licin/mana kasar" sudah ditandai eksplisit di soal.',
        "T3": 'Untuk lintasan tiga-segmen baru (licin-kasar-licin), menetapkan titik acuan Ep konsisten, menuliskan persamaan HKEM tepat per segmen (kekal penuh pada segmen licin; dikurangi usaha gesekan pada segmen kasar) sebelum menghitung, mandiri.',
        "T4": 'Merancang pendekatan pada lintasan majemuk belum dicontohkan (>2 segmen bergantian licin-kasar, atau target berada di tengah segmen kasar), tanpa dituntun, tetap menetapkan acuan & persamaan per segmen secara konsisten & benar.',
    },
    "Producing": {
        "T1": 'Salah konsep dasar (mis. mgh_awal = mgh_akhir langsung) meski dituntun langkah demi langkah.',
        "T2": 'Bisa menghitung tiap langkah bila dituntun urutan/kerangka tabelnya, tapi belum menyusun kesimpulan koheren tanpa diminta eksplisit.',
        "T3": 'Menghitung tuntas seluruh rangkaian (kecepatan/energi awal → energi hilang ke kalor pada segmen kasar → kecepatan/energi di titik target) dengan benar, dan menyusun kesimpulan koheren yang menjawab pertanyaan nyata disertai penjelasan energi berubah bentuk (bukan hilang), mandiri.',
        "T4": 'Menghasilkan solusi lengkap & koheren pada rancangan majemuk belum dicontohkan (multi-kendala sekaligus), termasuk mendiagnosis sendiri titik gagal & mengusulkan revisi kuantitatif tepat, tanpa dituntun.',
    },
}


def _rubric(*processes):
    if len(processes) == 1:
        return dict(RUBRICS[processes[0]])
    return {t: " | ".join(p + ": " + RUBRICS[p][t] for p in processes)
            for t in ("T1", "T2", "T3", "T4")}


def _gate(gid, title, processes, prompt, seconds, notes, optional=False):
    return dict(id=gid, title=title, process=" + ".join(processes),
                prompt=prompt, seconds=seconds, rubric=_rubric(*processes),
                teacher_notes=notes, optional=optional)


LABELS = ("Apa yang ditanyakan", "Formulasi yang digunakan", "Informasi distraktor",
          "Identifikasi data", "Substitusi nilai ke formula", "Penyelesaian",
          "Kesimpulan jawaban")


def _steps(*parts):
    if len(parts) != 7:
        raise ValueError("Pembahasan harus mempunyai tujuh langkah")
    return [label + ": " + part for label, part in zip(LABELS, parts)]


def _worked(scenario, result, *parts):
    return dict(scenario=scenario, steps=_steps(*parts), result=result)


def _lab(kind, **params):
    return dict(kind=kind, params=params)


ALIGNMENT = {
    "f-use-1-pra": {
        "gates": [
            _gate("G1", "Arah gaya, usaha, dan rasa lelah", ("Classifying",),
                  "Tas ransel 4 kg digendong sambil berjalan mendatar 20 m, kecepatan tetap, sangat lelah. Tulis: (a) usaha gaya penahan — angka + satuan. (b) satu kata: YA atau TIDAK, apakah lelah menunjukkan usaha secara fisika.", 120,
                  "Sumber C1.6, G1; isi soal dipertahankan, pengantar 'Papan mini, 30 detik' diadaptasi menjadi 120 detik. Kunci: (a) 0 J karena gaya penahan vertikal tegak lurus perpindahan; (b) TIDAK. Jangan menerima 0 J disertai YA. Rubrik dinilai dari alasan mandiri, bukan angka saja; rasa lelah tidak menentukan usaha pada tas."),
            _gate("G2", "Usaha total dan perubahan bentuk energi", ("Explaining",),
                  "Balok 2 kg diam didorong gaya mendatar tetap 3 m hingga v=4 m/s di lantai licin, lalu direm gesekan sampai berhenti. Tulis: (a) usaha total 3 m pertama — angka + satuan. (b) satu kata: sebut bentuk energi tujuan Ek yang hilang.", 180,
                  "Sumber C1.6, G2. Kunci: W_net = ½×2×4² = 16 J; energi berubah menjadi kalor dan sedikit bunyi. Frasa sumber 'gaya mendatar tetap 3 m' berarti gaya bekerja selama perpindahan 3 m, bukan gaya sebesar 3 m; satuan gaya tidak diberikan dan tidak perlu dikarang. Kata 'hilang' dalam pertanyaan mengacu pada berkurangnya Ek, bukan lenyapnya energi total. Waktu sumber 30 detik diadaptasi 180 detik."),
            _gate("G3", "Normal pada bidang miring dan segmen kasar", ("Classifying", "Explaining"),
                  "Kotak N didorong naik bidang miring licin oleh gaya sejajar bidang, lalu melintasi segmen datar kasar. Tulis: (a) usaha gaya normal sepanjang bidang miring — nol/tak-nol + satu kata alasan. (b) satu kata: sebut bentuk energi yang berkurang di segmen kasar.", 180,
                  "Sumber C1.6, G3 BARU. Kunci sumber: (a) nol — tegak lurus; (b) kalor. Redaksi (b) sumber tidak presisi: yang berkurang ialah energi mekanik, sedangkan bentuk TUJUAN perubahan ialah energi internal/kalor. Jelaskan kekaburan redaksi kepada penilai dan terima uraian fisika yang membedakan keduanya; jangan menilai 'kalor berkurang' sebagai pernyataan konsep yang benar. Dua proses dicatat terpisah, tidak dirata-ratakan. Waktu 30 detik sumber diadaptasi 180 detik."),
            _gate("G4", "Kartu transfer arah gaya dan usaha neto", ("Classifying", "Explaining"),
                  "T4-CLS — Peti 10kg ditarik sejauh 5m di lantai mendatar oleh tali bersudut 60° terhadap lantai dengan gaya 40N. Bekerja pula gaya berat, gaya normal, dan gaya gesek 12N. Golongkan tiap gaya (usaha positif/negatif/nol) dan hitung usaha gaya tali.\n\nT4-EXP — Balok 2kg mula-mula diam didorong gaya mendatar tetap 8N sejauh 3m di lantai kasar; gaya gesek 5N melawan. (a) Mengapa Ek akhir ≠ 8×3=24J? (b) Berapa Ek akhirnya, dan ke mana sisanya? (c) Bagaimana kalau gaya dorong hanya 5N?", 240,
                  "Sumber C1.6/G4 dan D5.3/D5.4. Artefak opsional T3→T4, dibaca per meja; yang belum memenuhi tetap T3, bukan gagal TP. 240 detik adalah sasaran per kartu, tidak ada penghentian otomatis untuk kedua kartu sekaligus. T4-CLS: W_tali=+100 J, W_gesek=−60 J, berat/normal=0, ΔEk=+40 J. T4-EXP: W_net=24−15=9 J, Ek akhir9 J, kenaikan internal15 J. Varian dorong5 N dari diam: dalam model gaya yang saling menyeimbangkan benda tidak mulai bergerak; jangan tetap memakai perpindahan3 m untuk mengklaim kalor15 J. Gesek kinetik pada benda yang tetap diam tidak boleh diperlakukan sebagai gaya aktual tanpa asumsi; RPP tidak memberi koefisien gesek statis. T4 membutuhkan transfer mandiri dan alasan yang bertahan saat ditanya mengapa, bukan hanya angka benar.", True),
        ],
        "worked": [
            _worked("Peti massa 1,2 kg ditarik 30 N pada sudut60° terhadap gerak mendatar tetap0,8 m/s selama2 s. Label peti bertuliskan rak4. cos60°=0,5. Tentukan usaha gaya tali saja.", "W_tali=+24 J.",
                    "Usaha satu gaya tali, bukan usaha neto dan bukan energi kinetik peti.",
                    "W_tali=Fs cosθ; karena kelajuan tetap, perpindahan s=vt. Sudut diukur antara gaya dan gerak.",
                    "Massa1,2 kg dan nomor rak4 tidak masuk usaha tali yang F,θ,s-nya diketahui. Kelajuan tetap tidak memaksa usaha tali nol: gaya lain dapat menyeimbangkannya.",
                    "F=30 N, θ=60°, v=0,8 m/s, t=2 s. Turunkan s=1,6 m sebelum menghitung usaha.",
                    "s=0,8×2=1,6 m; W_tali=30×1,6×0,5.",
                    "W_tali=24 J, positif karena komponen tali searah perpindahan. Maksimum Fs=48 J; sudut60° memberikan setengahnya.",
                    "Usaha tali +24 J. Pada gerak tetap, jumlah usaha semua gaya nol sehingga usaha gaya lain total−24 J."),
            _worked("Paket bermassa1200 g meluncur translasi dengan kelajuan tetap: menempuh10 m dalam2 s. Kemasan mempunyai4 lapisan karton. Tentukan Ek terhadap lantai.", "Ek=15 J.",
                    "Energi gerak translasi paket dalam joule terhadap pengamat di lantai.",
                    "Ek=½mv², dengan v=s/t untuk interval berkelajuan tetap; massa diubah ke kg.",
                    "Jumlah lapisan karton4 tidak digunakan. Tidak ada informasi energi rotasi sehingga model partikel dipakai.",
                    "m=1200/1000=1,2 kg, s=10 m, t=2 s; v=5 m/s bukan10 m/s.",
                    "Ek=½×1,2×(10/2)².",
                    "v²=25 m²/s² sehingga Ek=0,6×25=15 J. Jika kelajuan digandakan, Ek menjadi60 J.",
                    "Ek paket15 J. Faktor kuadrat kelajuan, bukan jumlah lapisan kemasan, menentukan perbandingan energi geraknya."),
            _worked("Wadah1,5 kg dinaikkan dari rak0,8 m ke rak2 m terhadap lantai melalui papan miring panjang4 m. g=10 m/s². Tentukan perubahan Ep.", "ΔEp=+18 J.",
                    "Selisih energi potensial akhir dikurangi awal, bukan salah satu nilai Ep saja.",
                    "ΔEp=mg(h_akhir−h_awal), dengan acuan sama pada kedua posisi.",
                    "Panjang papan4 m tidak sama dengan kenaikan vertikal. Bentuk jalur tidak mengubah ΔEp.",
                    "m=1,5 kg, h_awal=0,8 m, h_akhir=2 m; Δh=+1,2 m.",
                    "ΔEp=1,5×10×(2−0,8).",
                    "ΔEp=18 J. Dengan lantai acuan, Ep_awal12 J dan Ep_akhir30 J; selisihnya18 J.",
                    "Energi potensial bertambah18 J. Menggeser acuan yang sama untuk kedua posisi tetap memberikan selisih ini."),
            _worked("Kotak2 kg semula2 m/s ditarik10 N membentuk60° terhadap perpindahan mendatar4 m; gesekan tetap2 N melawan gerak. Berat dan normal vertikal. cos60°=0,5. Berapa kelajuan akhir?", "v_akhir=4 m/s; ΔEk=12 J.",
                    "Kelajuan akhir kotak setelah seluruh perpindahan4 m.",
                    "W_net=(F cosθ−f)s=ΔEk; Ek_akhir=½mv0²+W_net. Berat/normal tegak lurus gerak dan usahanya nol.",
                    "Gaya10 N bukan gaya neto. Menggunakan10×4 sebagai ΔEk akan mengabaikan sudut dan gesekan sekaligus.",
                    "m=2 kg, v0=2 m/s, F_sejajar=5 N, f=2 N, s=4 m; gaya neto3 N.",
                    "W_net=(10×0,5−2)×4=12 J; Ek_akhir=½×2×2²+12.",
                    "Ek_awal4 J dan Ek_akhir16 J; v=√(2×16/2)=4 m/s. Usaha tali20 J terbagi menjadi tambahanEk12 J dan kenaikan internal8 J.",
                    "Kelajuan akhir4 m/s. Energi yang masuk melalui tali tidak seluruhnya menjadi energi gerak; neraca20=12+8 J konsisten."),
        ],
        "summary": {
            "bigidea": "Tentukan benda dan prosesnya. Arah gaya menentukan usaha satu gaya; jumlah usaha menentukan perubahan Ek, sedangkan Ep memerlukan acuan.",
            "rows": [
                dict(title="Usaha satu gaya", formula="W=Fs cosθ", meaning="Komponen sejajar perpindahan memindahkan energi; tanda mengikuti arah komponen itu.", trap="Gaya besar atau rasa lelah tidak menjamin usaha positif."),
                dict(title="Energi kinetik", formula="Ek=½mv²", meaning="Energi keadaan gerak; massa linear, kelajuan kuadrat.", trap="Menggandakan v memberi empat kali Ek, bukan dua kali."),
                dict(title="Energi potensial", formula="Ep=mg(h−h_ref); ΔEp=mgΔh", meaning="Nilai Ep bergantung acuan; selisihnya tetap untuk acuan yang konsisten.", trap="Tinggi vertikal berbeda dari panjang lintasan; Ep dapat negatif."),
                dict(title="Usaha neto", formula="ΣW=Ek_akhir−Ek_awal", meaning="Gabungkan semua usaha dengan tandanya, lalu jelaskan perubahan bentuk energi.", trap="Usaha tarik saja tidak selalu sama dengan ΔEk; energi mekanik yang berkurang tidak lenyap."),
            ],
            "transfer": "Pada konveyor yang mempercepat kardus tanpa selip, gesekan statis pada kardus dapat searah perpindahan dan melakukan usaha positif. Periksa arah gaya pada benda yang dipilih; jangan menghafal semua gesekan selalu berusaha negatif.",
            "checklist": ["Benda dan dua posisi ditentukan.", "Sudut terhadap perpindahan digambar.", "Satuan SI dan kuadrat kelajuan diperiksa.", "Acuan Ep sama pada awal/akhir.", "Usaha tiap gaya dipisahkan sebelum dijumlahkan.", "Perubahan bentuk energi disebutkan, bukan hanya kata hilang."],
        },
        "hook": {
            "title": "Tarikan sama, akibat berbeda",
            "scene": "Kotak bergeser mendatar2 m. Pita penarik24 N dapat dipasang mendatar, miring60°, atau tegak lurus. Di lantai berikutnya ada karpet yang menyerap sebagian energi gerak. Pilih dugaan sebelum membuka penjelasan.",
            "question": "Jika gaya tetap24 N, apa yang berubah ketika sudut tarikan dinaikkan dari0° ke60°?",
            "options": ["Usaha tali menjadi setengah karena komponen sejajarnya berkurang.", "Usaha tetap karena besar gaya dan perpindahan sama.", "Usaha menjadi nol karena gaya tidak mendatar."],
            "bridge": "Dugaan ini akan diuji dengan arah gaya, lalu dibawa ke neraca usaha neto dan perubahan energi. Simpan alasan awalmu; jawaban otomatis lab hanya tersedia saat belajar.",
            "lab": _lab("work", F=24, s=2, theta=60),
        },
    },
    "f-use-1": {
        "gates": [
            _gate("G5", "Rencana sebelum hitungan", ("Planning",),
                  "Kelereng 0,2kg dilepas diam di puncak A (h_A=5m, licin), acuan Ep=0 di B; BC datar kasar 4m μ_k=0,25; CD licin ke D. Tulis: (a) acuan Ep yang dipakai. (b) segmen mana yang persamaannya BUKAN kekal penuh, dan mengapa.", 180,
                  "Sumber C2.6/G5 dan D5.2. Kunci: B sebagai acuan yang diberikan; BC memerlukan W_f=−μmgd karena sebagian Em berubah menjadi internal/kalor. Untuk diagnosis T3, minta persamaan per segmen SEBELUM menghitung; dua isian ringkas G5 saja belum membuktikan seluruh deskriptor Planning T3. Acuan lain yang dijelaskan konsisten secara fisika sah, meskipun soal ini sudah menetapkan B. Gunakan model partikel meluncur tanpa rotasi; RPP menyebut kelereng tetapi tidak mencantumkan energi rotasi. Waktu sumber30 detik diadaptasi180 detik."),
            _gate("G6", "Jangan tertipu angka yang tampak wajar", ("Producing",),
                  "Untuk lintasan G5 dengan h_D=4m: v_B=10 m/s (diberikan). Setelah BC (kalor 2J), berapa v_D di D, dan apakah syarat v_D≥2 m/s terpenuhi?", 240,
                  "Sumber C2.6/G6; sertakan data G5 saat menampilkan agar mandiri: m0,2 kg, BC4 m, μ0,25, Ep=0 di B, g10. Kunci: Ek_B10 J; BC mengubah2 J menjadi internal; Ek_C8 J; Ep_D8 J; Ek_D0 dan v_D0 m/s, GAGAL syarat≥2. Mengabaikan gesekan memberi√20≈4,47 m/s dan verdikt terbalik. D5.2 menyebut h_D maks3,8 m: ini batas untuk target v_D≥2, bukan tinggi sekadar terjangkau. Tinggi maksimum pada v=0 adalah4 m. Waktu sumber30 detik diadaptasi240 detik."),
            _gate("G7", "Integrasi rencana dan hasil", ("Planning", "Producing"),
                  "Bola 0,5kg dilepas h_A=3,2m licin, lorong kasar 2m μ_k=0,3, naik ke h_D=1m. Tulis: (a) satu kata: segmen mana yang membutuhkan persamaan berbeda. (b) angka: v_D (boleh menulis langkah singkat).", 240,
                  "Sumber C2.6/G7 BARU; gunakan g10 dan model translasi. Kunci: lorong kasar/tengah; Ek_B16 J, internal3 J, Ek_C13 J, Ep_D5 J, Ek_D8 J, v_D=√32≈5,66 m/s. D5.2 menambahkan syarat≥3 m/s sehingga lolos; syarat itu tidak tercetak pada stem G7 C2.6 dan tidak boleh dituntut diam-diam. Model tanpa gesekan memberi√44≈6,63 m/s; metode tetap salah walau dua angka sama-sama lolos≥3. Dua proses dinilai terpisah. Waktu sumber30 detik diadaptasi240 detik."),
            _gate("G8", "Kartu lintasan majemuk dan revisi kuantitatif", ("Planning", "Producing"),
                  "T4-PLN — Kelereng 0,2kg dilepas diam di puncak lintasan licin P (h_P=6m) turun ke Q; QR datar kasar 3m (μ₁=0,2); RS licin menanjak ke S (h_S=2m); ST datar kasar 5m (μ₂=0,3). Titik pemeriksaan M berada 2m setelah S, di dalam segmen ST. Tuliskan rencana: acuan, persamaan tiap segmen, dan cara menangani target di tengah segmen kasar.\n\nT4-PRD — Laksanakan rencana T4-PLN secara tuntas. Syarat wahana: kelereng harus tiba di T (5m dari S) dengan v_T≥7 m/s. Apakah terpenuhi? Bila tidak, tunjukkan di mana energi paling banyak berkurang dan berapa h_P minimum yang membuat syarat tepat terpenuhi.", 240,
                  "Sumber C2.6/G8 dan D5.3/D5.4, model translasi g10. Artefak T3→T4 opsional; bacaan per meja, tidak menurunkan T3. Sasaran240 detik per kartu, bukan batas gabungan dua artefak. Acuan QR; gunakan2 m untuk SM dan5 m untuk ST. Ek_Q12 J; disipasiQR1,2 J; Ek_R10,8 J; Ep_S4 J; Ek_S6,8 J. Di M: internalST1,2 J, Ek_M5,6 J; di T: internalST3 J, Ek_T3,8 J, v_T=√38≈6,16 m/s, gagal≥7. KebutuhanEk_T4,9 J, kekurangan1,1 J; h_P minimum6,55 m atau μ₂ maksimum0,19. Disipasi terbesarST3 J; kenaikanEp4 J bukan disipasi. RPP tidak memasukkan rotasi kelereng; jangan menafsirkan sebagai bola menggelinding fisik tanpa mengubah model.", True),
        ],
        "worked": [
            _worked("Paket1,5 kg bergerak4 m/s pada baki yang berada0,8 m di atas meja setinggi0,4 m dari lantai. Panjang baki3 m. Lantai menjadi acuan, g10. Tentukan Em saat itu.", "Em=30 J terhadap lantai.",
                    "Jumlah energi gerak dan energi potensial pada keadaan yang sama.",
                    "Em=½mv²+mgh; tinggi h harus diukur terhadap acuan lantai yang diberikan.",
                    "Panjang baki3 m tidak diperlukan. Tinggi0,8 m bukan tinggi terhadap lantai; jangan memasukkannya langsung sebagai h.",
                    "m=1,5 kg, v=4 m/s, h=0,4+0,8=1,2 m, g=10 m/s².",
                    "Em=½×1,5×4²+1,5×10×(0,4+0,8).",
                    "Ek=12 J, Ep=18 J, sehingga Em=30 J. Kedua suku bersatuan joule dan dihitung pada titik sama.",
                    "Energi mekanik30 J terhadap lantai. Mengganti acuan mengubah angka Ep/Em secara konsisten, tetapi tidak mengubah prediksi kelajuan dari selisih energi."),
            _worked("Dua jalur licin panjangnya3 m dan4 m menghubungkan pelepasan1,8 m ke ujung0,55 m terhadap lantai. Paket dilepas diam; semua puncak dapat dicapai. g10. Tentukan kelajuan akhir kedua jalur.", "Kedua kelajuan akhir5 m/s; waktu tiba belum ditentukan.",
                    "Kelajuan pada ujung kedua jalur, bukan waktu perjalanan.",
                    "½mv0²+mgh0=½mv²+mgh; massa tercoret dan v²=v0²+2g(h0−h).",
                    "Panjang3 m dan4 m tidak masuk neraca dua titik ideal; panjang itu belum cukup untuk menentukan waktu tempuh.",
                    "v0=0, h0=1,8 m, h=0,55 m; Δh turun1,25 m dan semua penghalang sudah dinyatakan terjangkau.",
                    "v²=0+2×10×(1,8−0,55).",
                    "v²=25 sehingga v=5 m/s untuk kedua jalur. PenurunanEp per kilogram12,5 J/kg sama dengan pertambahanEk per kilogram.",
                    "Kelajuan akhir sama5 m/s, meskipun bentuk jalur dapat membuat waktu tempuh berbeda."),
            _worked("Paket2 kg dilepas diam pada1,6 m, turun licin ke lantai, melewati bantalan dari posisi2 m sampai5 m, lalu naik licin ke0,4 m. Pada bantalan mendatar, gaya gesek4 N. g10. Tentukan kelajuan tiba.", "v_tiba=√12≈3,46 m/s.",
                    "Kelajuan setelah segmen turun, kasar, dan naik diselesaikan berurutan.",
                    "Acuan lantai; AB:Ek_B=mgh0, BC:Ek_C=Ek_B−f d, CD:Ek_D=Ek_C−mgh_D; v_D=√(2Ek_D/m).",
                    "Angka posisi akhir5 m bukan panjang bantalan. Panjang aktual adalah5−2=3 m. Gaya gesek sudah diberikan, jadi μ tidak perlu ditebak.",
                    "m2 kg, h0=1,6 m, h_D0,4 m, f4 N, d3 m. N=mg karena bantalan mendatar tanpa gaya vertikal lain.",
                    "Ek_B=2×10×1,6; Ek_C=Ek_B−4×(5−2); Ek_D=Ek_C−2×10×0,4.",
                    "Ek_B32 J, internal12 J, Ek_C20 J, Ep_D8 J, Ek_D12 J, v_D=√(24/2)=√12. Semua energi antara yang dibutuhkan positif.",
                    "Paket mencapai tujuan dengan3,46 m/s. Ek12+Ep8+kenaikan internal12=32 J; energi total tetap, Em turun12 J."),
            _worked("Model jalur kirim dilepas dari diam menuju baki0,4 m. Bantalan mendatar3 m mempunyaiμ0,15; bagian lain licin. Target tiba2 m/s, g10. Rancangan lama h0=0,95 m. Berapa tinggi pelepasan nominal yang tepat?", "h0=1,05 m, naik0,10 m dari rancangan lama.",
                    "Tinggi awal nominal yang menghasilkan kelajuan target, disertai pemeriksaan rancangan lama.",
                    "Rencanakan turun→kasar→naik: gh0=μg d+gh_D+½v_D². Jadi h0=h_D+μd+v_D²/(2g).",
                    "Massa tidak diberikan dan tidak diperlukan karena membagi semua suku; bukan alasan untuk mengabaikan gesekan.",
                    "h_D0,4 m, μ0,15, d3 m, v_D2 m/s, v0=0; h0 lama0,95 m hanya dipakai untuk membandingkan revisi.",
                    "h0=0,4+0,15×3+2²/(2×10).",
                    "h0=0,4+0,45+0,20=1,05 m. Per kilogram:10,5 J tersedia,4,5 J menjadi internal,4 J menjadiEp,2 J menjadiEk. Rancangan lama hanya menyisakanEk1 J/kg, jadi v=√2<2.",
                    "Pelepasan nominal1,05 m memenuhi target; revisi+0,10 m. Uji variasiμ dan keterjangkauan sebelum menganggap model mewakili alat nyata."),
        ],
        "summary": {
            "bigidea": "Tulis rencana sebelum angka: acuan tunggal, keadaan tiap titik, lalu neraca berbeda untuk segmen licin dan kasar. Solusi harus berakhir pada verdikt terhadap syarat nyata.",
            "rows": [
                dict(title="Energi mekanik", formula="Em=½mv²+mgh", meaning="Jumlah dua bentuk pada titik yang sama dan acuan yang sama.", trap="Ek bertambah tidak berarti Em bertambah pada lintasan ideal."),
                dict(title="Segmen ideal", formula="v²=v0²+2g(h0−h)", meaning="Selisih tinggi menentukan kelajuan; setiap puncak perantara harus terjangkau.", trap="Kelajuan akhir sama tidak berarti waktu tempuh sama."),
                dict(title="Segmen mendatar kasar", formula="Ek_keluar=Ek_masuk−μmgd", meaning="Jarak yang benar-benar ditempuh menentukan kenaikan internal; N=mg hanya dengan asumsi vertikal yang tepat.", trap="Ek negatif berarti target tidak tercapai; jangan mengakarkan bilangan negatif sebagai kelajuan."),
                dict(title="Rancangan dan verdikt", formula="h0=h_D+(v_D²−v0²)/(2g)+μd", meaning="Susun dari syarat hasil, lalu cek tiap segmen dan kebutuhan energi.", trap="h maksimum untuk tiba dengan v_min>0 lebih rendah daripada h maksimum saat v=0; massa sering tercoret."),
            ],
            "transfer": "Untuk target di tengah bantalan, gunakan jarak parsial dari awal bantalan ke target. Untuk beberapa bantalan, jumlahkan μ_i m g d_i; jangan menyamakan kenaikanEp di tanjakan dengan disipasi menjadi internal.",
            "checklist": ["Acuan dan model translasi ditulis.", "Ruas licin/kasar diidentifikasi dari situasi.", "Persamaan per segmen muncul sebelum substitusi.", "Data antara diturunkan, misalnya d=x_akhir−x_awal atau μ=f/N.", "Energi tersisa cukup pada setiap ruas.", "Verdikt dibandingkan dengan batas yang diminta.", "Internal/kalor dibedakan dari Ep dan energi yang lenyap."],
        },
        "hook": {
            "title": "Sampai di baki belum tentu memenuhi syarat",
            "scene": "Paket dilepas dari meja, menurun, melewati bantalan mendatar, kemudian naik ke baki. Syarat kirim: tiba dengan kelajuan sedikitnya2 m/s. Satu perhitungan mengabaikan bantalan dan menyatakan lolos; perhitungan lain memasukkannya dan meragukan rancangan.",
            "question": "Bukti mana yang harus disiapkan sebelum menerima verdikt lolos?",
            "options": ["Rencana beracuan konsisten dan neraca tiap segmen, termasuk energi internal di bantalan.", "Kelajuan akhir yang angkanya positif dan tampak masuk akal.", "Energi awal besar, sehingga rincian bantalan tidak diperlukan."],
            "bridge": "Prediksi bukan bukti akhir. Susun dahulu rencana, jalankan perhitungan, lalu gunakan syarat kedatangan untuk menilai rancangan; saat gerbang mandiri, neraca otomatis disembunyikan.",
            "lab": _lab("energy", m=1, h0=1.1, h=.4, mu=.2, s=3, v0=0, shape="valley", mode="friction"),
        },
    },
}


def make_questions(slug, stage, form=1):
    """P7 sepuluh dan P9 delapan butir baru; P2/P10 memakai sumber sebelumnya."""
    if slug not in ALIGNMENT:
        raise ValueError(slug)
    if not isinstance(form, int) or isinstance(form, bool) or form < 1:
        raise ValueError("form harus bilangan bulat positif")
    stage = str(stage).upper()
    if stage in ("P2", "P10"):
        try:
            from .lesson_energi import make_questions as old_questions
        except ImportError:
            from lesson_energi import make_questions as old_questions
        return old_questions(slug, stage, form)
    if stage not in ("P7", "P9"):
        raise ValueError("Provider penyelarasan hanya menyediakan P7/P9 dan delegasi P2/P10")
    qs = []
    prefix = f"align-{slug}-{stage}-f{form}"

    def add(indicator, prompt, answer, parts, *, options=None, unit="J", label="Jawaban", diagram=None, level="C4", seconds=240, tol=.02):
        q = dict(id=f"{prefix}-{len(qs)+1:02d}", indicator=indicator, prompt=prompt,
                 kind="choice" if options else "num", label=label, unit="" if options else unit,
                 answer=answer, tol=0 if options else tol, level=level, seconds=seconds,
                 steps=_steps(*parts), explain=parts[5]+" "+parts[6])
        if options:
            shift=(form-1)%len(options)
            q["options"]=options[shift:]+options[:shift]
            q["answer"]=(answer-shift)%len(options)
        if diagram:
            q["diagram"]=diagram
        qs.append(q)

    k=(form-1)%5
    if slug == "f-use-1-pra":
        _pra_questions(stage, k, add)
    else:
        _use_questions(stage, k, add)
    return qs


def _pra_questions(stage, k, q):
    if stage == "P7":
        q("usaha", "Kotak meluncur naik bidang miring tetap30° tanpa terangkat dari permukaan. Besar normal18 N. Manakah penjelasan usaha normal yang tepat?", 1,
          ("Klasifikasi usaha normal, bukan usaha gravitasi atau gaya pendorong.", "W_N=Ns cosθ; θ ialah sudut normal terhadap perpindahan sepanjang bidang.", "Sudut bidang30° bukan sudut antara normal dan gerak; normal18 N tidak langsung dikalikan jarak.", "Normal tegak lurus permukaan dan gerak berada sepanjang permukaan:θ90°.", "W_N=18×s×cos90° untuk berapa pun s sepanjang bidang.", "cos90°=0 sehingga W_N0 J. Kemiringan bidang tidak mengubah sifat tegak lurus itu.", "Usaha normal nol karena tegak lurus perpindahan, walau normal tidak nol."),
          options=["Positif karena normal menopang kotak.", "Nol karena normal tegak lurus perpindahan.", "Bergantung pada besar sudut bidang, sehingga belum dapat ditentukan."], level="C2", seconds=120)
        F=32+2*k; ans=F*.5*1.2*4
        q("usaha", f"Peti ditarik {F} N bersudut60° terhadap gerak mendatar tetap1,2 m/s selama4 s. cos60°=0,5. Kode rak peti adalah7. Berapa usaha gaya tarik saja?", ans,
          ("Usaha tarikan dalam interval4 s.", "Turunkan s=vt lalu W=Fs cos60°.", "Kode rak7 tidak relevan. Kelajuan tetap memberi usaha NETO nol, bukan usaha tarikan nol.", f"F={F} N; v1,2 m/s; t4 s; s4,8 m; θ60°.", f"W={F}×(1,2×4)×0,5.", f"Komponen sejajar{F/2:g} N dan s4,8 m menghasilkan W={ans:g} J.", f"Usaha tarikan+{ans:g} J; usaha gaya lain menyeimbangkannya bila kelajuan tetap."), label="Usaha tarikan", diagram=_lab("work",F=F,s=4.8,theta=60))
        q("usaha", "Kardus tidak selip di atas konveyor yang sedang mempercepat ke kanan. Satu-satunya gaya mendatar pada kardus ialah gesekan statis ke kanan. Bagaimana tanda usaha gesekan pada kardus terhadap lantai?", 2,
          ("Tanda usaha gesekan statis pada kardus yang berpindah ke kanan.", "Gunakan arah gaya pada benda yang dipilih:W=f_s s cosθ.", "Kata gesekan tidak otomatis berarti usaha negatif; jenis statis berarti tidak ada selip relatif di kontak.", "Gaya gesek pada kardus ke kanan; perpindahan kardus terhadap lantai juga ke kanan;θ0°.", "W=f_s s cos0°=+f_s s untuk s>0.", "Usahanya positif dan menambahEk kardus. Gaya reaksi pada sabuk adalah pada benda lain, bukan untuk menjumlah gaya pada kardus.", "Gesekan statis melakukan usaha positif pada kardus dalam acuan lantai."), options=["Negatif karena semua gesekan melawan gerak.", "Nol karena tidak ada selip.", "Positif karena gaya pada kardus searah perpindahannya."], seconds=240)
        mass=900+100*k; s=12+2*k; v=s/3; K=.5*(mass/1000)*v*v
        q("kinetik", f"Sampel bermassa{mass} g bergerak translasi dengan kelajuan tetap, menempuh{s} m dalam3 s. Penanda jalurnya bernomor8. Berapa Ek sampel terhadap lantai?", K,
          ("Ek translasi sampel, bukan momentumnya.", "v=s/t dan Ek=½mv², dengan m dalamkg.", "Nomor jalur8 tidak dipakai; jarak bukan kelajuan sampai dibagi waktu.", f"m={mass/1000:g} kg; v={s}/3={v:g} m/s.", f"Ek=½×{mass/1000:g}×({s}/3)².", f"Kuadrat kelajuan{v*v:g} memberi Ek={K:g} J; satuan kg·m²/s² adalahJ.", f"Energi gerak sampel{K:g} J."), label="Energi kinetik", diagram=_lab("kinetic",m=mass/1000,v=v))
        q("kinetik", "Wadah baru bermassa dua kali wadah awal tetapi bergerak dengan setengah kelajuan awal. Pengamat sama. Bagaimana Ek barunya?", 0,
          ("PerbandinganEk baru terhadapEk awal.", "RasioEk=(m_b/m_a)(v_b/v_a)².", "Nilai absolut massa dan kelajuan tidak perlu diketahui karena yang dicari rasio.", "Faktor massa2 dan faktor kelajuan½; keduanya harus digunakan bersama.", "Ek_b/Ek_a=2×(½)².", "Rasionya2×¼=½. Membaca hanya faktor massa akan memberi dua kali, sedangkan melupakan kuadrat v memberi satu kali.", "Ek baru setengah semula."), options=["Setengah semula.", "Sama dengan semula.", "Dua kali semula."], seconds=180, level="C3")
        gap=.8+.1*k; mass=1.5; U=mass*10*gap
        q("potensial", f"Meja berada0,6 m di atas lantai. Benda1,5 kg berada{gap:g} m di atas meja. Garis meja dipilih sebagaiEp0. g10 m/s². Berapa Ep benda?", U,
          ("Ep relatif terhadap meja, bukan terhadap lantai.", "Ep=mg(h_benda−h_ref).",
           "Tinggi meja0,6 m tidak perlu ditambahkan lagi jika tinggi relatif terhadap meja sudah diberikan; tetap berguna untuk memeriksa acuan.", f"m1,5 kg; tinggi relatif{gap:g} m; g10.", f"Ep=1,5×10×{gap:g}.", f"Ep={U:g} J. Jika memakai lantai, kedua posisi tinggi harus diubah dan nilaiEp memang berbeda.", f"Ep benda terhadap meja+{U:g} J."), label="Energi potensial",diagram=_lab("potential",m=mass,h=.6+gap,ref=.6))
        q("potensial", "Sebuah beban dipindah dari rakA ke rakB. Penilai mengganti acuanEp dari lantai ke rakA, tetapi tetap memakai acuan baru itu untuk kedua posisi. Besaran mana yang pasti tetap?", 1,
          ("Besaran energi yang tidak berubah akibat penggeseran acuan yang konsisten.", "ΔEp=mg[(h_B−h_ref)−(h_A−h_ref)]=mg(h_B−h_A).", "Acuan baru bukan perubahan posisi beban; jangan menganggap beban benar-benar diturunkan.", "Kedua nilaiEp mendapat tambahan konstanta sama; m,g,h_A,h_B tetap.", "Kurangkan Ep_B−Ep_A; suku−mg h_ref saling menghilangkan.", "NilaiEp_A danEp_B dapat bergeser, tetapi selisihnya tetap. Kerja gravitasi−ΔEp juga tetap.", "PerubahanEp dariA keB tetap sama."), options=["Ep pada setiap posisi pasti tetap.", "PerubahanEp antaraA danB tetap.", "Ep pada semua posisi menjadi nol."], level="C3",seconds=180)
        v0=2+.5*k; F=8; f=3; s=2; vf=sqrt(v0*v0+10)
        q("usaha-neto", f"Wadah2 kg semula{v0:g} m/s didorong8 N mendatar sejauh2 m. Gaya gesek3 N melawan gerak; berat/normal vertikal. Berapa kelajuan akhir?", vf,
          ("Kelajuan setelah semua usaha pada perpindahan2 m dijumlahkan.", "Ek_f=½mv0²+(F−f)s; v_f=√(2Ek_f/m).", "8 N ialah dorongan, bukan resultan; berat dan normal tidak memberi usaha mendatar.", f"m2 kg; v0{v0:g} m/s; F_net5 N; s2 m.", f"Ek_f=½×2×{v0:g}²+(8−3)×2.", f"Ek_awal{v0*v0:g} J, W_net10 J, Ek_f{v0*v0+10:g} J; v_f={vf:.3f} m/s.", f"Kelajuan akhir≈{vf:.3f} m/s; 6 J dari usaha dorongan beralih menjadi internal."),label="Kelajuan akhir",unit="m/s",diagram=_lab("workenergy",F=5,s=2,m=2,v0=v0))
        e0=14+2*k;e1=38+4*k;s=3;force=(e1-e0)/s
        q("usaha-neto",f"Sensor pada luncuran mendatar mencatatEk naik dari{e0} J ke{e1} J sepanjang3 m. Massa sensor tercetak0,4 kg. Gaya neto tetap. Berapa besar gaya neto searah perpindahan?",force,
          ("Gaya neto tetap, bukan salah satu gaya individual.", "W_net=ΔEk=F_net s, sehinggaF_net=(Ek_f−Ek_i)/s.", "Massa0,4 kg tidak diperlukan karena kedua energi sudah diberikan dalamJ.",f"Ek_i{e0} J; Ek_f{e1} J; s3 m; perubahanEk positif.",f"F_net=({e1}−{e0})/3.",f"ΔEk={e1-e0} J dan F_net={force:g} N; N·m=J sehingga satuannya tepat.",f"Gaya neto{force:g} N searah perpindahan."),unit="N",label="Gaya neto")
        K=18+2*k
        q("usaha-neto",f"Kapsul denganEk{K} J direm sampai diam pada lantai mendatar. Hambatan udara dan bunyi diabaikan; sistem mencakup kapsul dan bantalan. Klaim yang tepat adalah…",0,
          ("Menilai usaha pengereman dan bentuk energi setelah berhenti.","W_net=Ek_f−Ek_i; untuk sistem kapsul–bantalan, penurunanEk menjadi kenaikan internal.","Jarak dan gaya pengerem tidak perlu diketahui untuk selisih energi yang sudah diberikan.",f"Ek_i{K} J; Ek_f0; tidak ada perubahanEp atau transfer lain.",f"W_net=0−{K}; ΔE_internal={K}−0.",f"Usaha pada gerak−{K} J dan kenaikan internal+{K} J. Energi total tetap meskipun energi mekanik turun.",f"Ek berkurang{K} J dan internal bertambah{K} J; tidak ada energi yang lenyap."),options=[f"Usaha neto−{K} J; energi internal bertambah{K} J.",f"Usaha neto+{K} J; energi total bertambah{K} J.",f"Usaha nol karena kelajuan akhir nol; energi{K} J hilang."],seconds=180,level="C3")
    else:
        q("usaha","Di ruang arsip, penopang vertikal menyangga kotak yang berpindah mendatar dengan tinggi tetap. Kemudian kotak dinaikkan oleh tangan. Ditinjau HANYA selama tahap mendatar, usaha penopang adalah…",2,
          ("Usaha penopang selama tahap mendatar saja.","W=Fs cosθ, ditentukan dari perpindahan pada interval yang ditanya.","Tahap pengangkatan berikutnya tidak masuk interval ini; mencampurnya akan mengubah arah perpindahan yang dinilai.","Gaya penopang vertikal, gerak mendatar,θ90°.","W=F s cos90°.","F dan s boleh tidak nol tetapi cos90°=0. Penopang melakukan nol usaha pada interval mendatar.","Jawab0 J karena tegak lurus, bukan karena benda tidak bergerak."),options=["Positif karena nanti kotak diangkat.","Negatif karena melawan berat.","Nol karena tegak lurus perpindahan tahap yang ditanya."],level="C2",seconds=120)
        F=36+2*k;s=1.5;W=F*s*.5
        q("usaha",f"Pintu geser laboratorium ditarik{F} N pada sudut120° terhadap perpindahan1,5 m. cos120°=−0,5. Massa pintu8 kg. Berapa usaha gaya tarik pada interval tersebut?",-W,
          ("Usaha bertanda dari satu gaya yang arah proyeksinya melawan perpindahan.","W=Fs cosθ; nilai kosinus negatif harus dipertahankan.","Massa8 kg tidak digunakan untuk usaha satu gaya yang telah diketahui.",f"F{F} N,s1,5 m,θ120°,cosθ−0,5.",f"W={F}×1,5×(−0,5).",f"W=−{W:g} J. Besar gaya positif; tanda usaha negatif berasal dari arah, bukan massa.",f"Gaya tersebut melakukan usaha−{W:g} J."),label="Usaha gaya",diagram=_lab("work",F=F,s=s,theta=120))
        mass=1600+100*k;distance=9+1.5*k;v=distance/3;K=.5*mass/1000*v*v
        q("kinetik",f"Pembawa film bermassa{mass} g bergerak tetap sejauh{distance:g} m dalam3 s terhadap lantai. Kotak penyimpannya diberi nomor11. Berapa energi kinetiknya?",K,
          ("Ek pembawa film terhadap lantai.","Ubah g kekg, hitungv=s/t, laluEk=½mv².","Nomor11 adalah identitas penyimpanan, tidak memberi energi. Jarak tidak boleh langsung dikuadratkan sebagai kelajuan.",f"m{mass/1000:g} kg; s{distance:g} m; t3 s; v{v:g} m/s.",f"Ek=½×{mass/1000:g}×({distance:g}/3)².",f"Ek={K:g} J setelah kelajuan dikuadratkan; arah gerak tidak memberi tanda negatif padaEk.",f"Energi kinetik{K:g} J."),label="Energi kinetik",diagram=_lab("kinetic",m=mass/1000,v=v))
        initial=12+2*k
        q("kinetik",f"Satu sachet yang sama mula-mula mempunyaiEk{initial} J. Kelajuannya menjadi3/2 kelajuan semula, tanpa perubahan massa atau pengamat. Berapa Ek barunya?",initial*2.25,
          ("Energi gerak setelah perubahan kelajuan, bukan pertambahannya.","Ek_b/Ek_a=(v_b/v_a)² untuk massa tetap.","Massa tidak perlu dicari karena sudah tercoret pada rasio; jangan memakai faktor3/2 secara linear.",f"Ek_a{initial} J; faktorv=3/2 sehingga faktorEk=9/4.",f"Ek_b={initial}×(3/2)².",f"Ek_b={initial*2.25:g} J; pertambahannya{initial*1.25:g} J adalah besaran berbeda.",f"Energi kinetik akhir{initial*2.25:g} J."),label="Energi kinetik akhir",level="C3",seconds=180)
        m=1.2+.1*k;hi=2.3;hf=.7;change=m*10*(hf-hi)
        q("potensial",f"Botol bermassa{m:g} kg diturunkan darih2,3 m keh0,7 m terhadap lantai. Panjang tali yang digunakan4 m. g10 m/s². Berapa perubahanEp botol–Bumi?",change,
          ("ΔEp akhir dikurangi awal, lengkap dengan tandanya.","ΔEp=mg(h_f−h_i).","Panjang tali4 m tidak sama dengan selisih tinggi dan tidak dipakai; semua posisi memakai lantai yang sama.",f"m{m:g} kg; h_i2,3 m; h_f0,7 m; Δh−1,6 m.",f"ΔEp={m:g}×10×(0,7−2,3).",f"ΔEp={change:g} J. Gravitasi justru melakukan usaha+{-change:g} J pada penurunan ini.",f"Energi potensial berkurang{-change:g} J, jadiΔEp={change:g} J."),label="Perubahan energi potensial")
        h=1.1+.1*k;ref=2;U=20*(h-ref)
        q("potensial",f"Wadah2 kg berada padah{h:g} m, sedangkan acuanEp0 padah2 m. Tinggi diukur dari lantai yang sama, g10 m/s². Berapa Ep wadah?",U,
          ("Ep relatif terhadap garis yang lebih tinggi dari benda.","Ep=mg(h−h_ref); Ep boleh negatif.","NolEp tidak harus di lantai. Menganggap semuaEp tak negatif akan bertentangan dengan acuan yang dipilih.",f"m2 kg; h{h:g} m; h_ref2 m; tinggi relatif{h-ref:g} m.",f"Ep=2×10×({h:g}−2).",f"Ep={U:g} J; massa dan gravitasi tetap positif. Tidak ada perubahan posisi akibat pilihan acuan.",f"Ep wadah{U:g} J terhadap garis2 m."),label="Energi potensial",diagram=_lab("potential",m=2,h=h,ref=ref))
        v0=1.5+.25*k;F=14;f=3;s=2;K=.5*2*v0*v0+(7-3)*s;vf=sqrt(K)
        q("usaha-neto",f"Sebuah kereta inspeksi2 kg mula-mula{v0:g} m/s. Gaya14 N membentuk60° terhadap gerak mendatar2 m; gesekan3 N melawan. cos60°0,5. Berapa kelajuan akhirnya?",vf,
          ("Kelajuan akhir setelah usaha tarikan dan gesekan dijumlahkan.","W_net=(F cos60°−f)s; v_f²=v0²+2W_net/m.","Besar14 N bukan komponen mendatar; gunakan7 N sebelum mengurangi gesekan.",f"m2 kg; v0{v0:g} m/s; F_net4 N; s2 m; W_net8 J.",f"v_f²={v0:g}²+2×(14×0,5−3)×2/2.",f"v_f²={K:g}; v_f≈{vf:.3f} m/s. Gesekan mengubah6 J menjadi internal, bukan menghilangkannya.",f"Kelajuan akhir≈{vf:.3f} m/s."),unit="m/s",label="Kelajuan akhir",diagram=_lab("workenergy",F=4,s=2,m=2,v0=v0))
        q("usaha-neto","Alat pendingin sampel diam setelah direm. Seorang siswa menulis 'karenaEk akhir0, seluruh usaha selama pengereman0'. Koreksi yang tepat adalah…",1,
          ("Menilai kesimpulan usaha neto dari energi akhir saja.","W_net=Ek_f−Ek_i, bukanW_net=Ek_f.","Keadaan akhir diam tidak memberi tahu bahwa keadaan awal juga diam; awal pengereman justru bergerak.","Ek_i positif; Ek_f0; tinggi tetap dan tidak ada penggerak tambahan.","W_net=0−Ek_i<0.","Usaha neto negatif sebesarEk awal; energi gerak berpindah terutama menjadi internal benda dan rem.","Usaha neto negatif; nolnyaEk akhir tidak menghapus energi awal dalam selisih."),options=["Benar karena benda akhirnya tidak berpindah lagi.","Keliru: usaha neto negatif sebesarEk awal, dengan perubahan bentuk energi.","Keliru: usaha neto positif sebesarEk awal."],level="C3",seconds=180)


def _use_questions(stage, k, q):
    if stage == "P7":
        q("mekanik","Paket dilepas dariA, turun pada rel polos keB, bergeser di karpet mendatarBC, lalu naik pada rel polosCD. Ep0 dipilih diB. Rencana mana yang sah sebelum menghitung?",0,
          ("Memilih rencana energi untuk tiga karakter permukaan, bukan memilih angka akhir.","Segmen polos tanpa hambatan memakaiEm tetap; karpet memakaiEm_f=Em_i−μmgd.","Kata polos tidak menghapus gravitasi; kata karpet tidak berarti energi total lenyap.","AB danCD ideal, BC mendatar kasar; acuanB konsisten untuk semua titik.","AB:mgh_A=Ek_B; BC:Ek_C=Ek_B−μmgd; CD:Ek_C=Ek_D+mgh_D.","Ketiga ruas tersambung melaluiEk_B danEk_C. Menggunakanmgh_A=mgh_D mengabaikan gerak akhir dan disipasi.","Pilih rencana yang memuat acuanB serta suku gesekan hanya padaBC."),options=["AB:mgh_A=Ek_B; BC:Ek_C=Ek_B−μmgd; CD:Ek_C=Ek_D+mgh_D.","AB,BC,CD semuanyaEm kekal karena energi total kekal.","Langsungmgh_A=mgh_D; kelajuan diperiksa setelahnya."],level="C3",seconds=180)
        m=1.2+.2*k;h=.5+.9;v=3;Em=m*(14+4.5)
        q("mekanik",f"Paket{m:g} kg bergerak3 m/s pada rak0,9 m di atas meja. Meja0,5 m di atas lantai yang menjadiEp0. Rak diberi nomor6. g10. Berapa Em paket?",Em,
          ("Em pada rak dengan acuan lantai.","Em=½mv²+mgh; h harus diturunkan dari dua kenaikan vertikal.","Nomor rak6 tidak relevan; memakai0,9 m sebagaih mengabaikan tinggi meja.",f"m{m:g} kg; v3 m/s; h=0,5+0,9=1,4 m.",f"Em=½×{m:g}×3²+{m:g}×10×1,4.",f"Ek={4.5*m:g} J; Ep={14*m:g} J; Em={Em:g} J.",f"Energi mekanik{Em:g} J terhadap lantai."),label="Energi mekanik",diagram=_lab("energy",m=m,h0=h,h=h,v0=v,mu=0,s=0,mode="ideal",shape="ramp"))
        q("lintasan-ideal","Dua paket berbeda massa melalui jalur licin berbeda bentuk dari tinggi awal danv0 yang sama ke tinggi akhir yang sama; semua puncak terjangkau. Apa simpulan energi yang tepat?",2,
          ("Hubungan kelajuan akhir, energi dalamJ, dan waktu tempuh.","Bagi½mv0²+mgh0=½mv²+mgh denganm; diperolehv²=v0²+2gΔh.","Bentuk dan panjang lintasan tidak masuk persamaan kelajuan dua titik; waktu memerlukan riwayat gerak tambahan.","h0,h,v0 sama; massa berbeda; semua gaya hambat diabaikan.","v_1²=v0²+2gΔh=v_2²; Ek_1/Ek_2=m_1/m_2 pada kelajuan sama.","Kelajuan akhir sama, energi dalamJ tidak harus sama, dan waktu tiba belum tentu sama.","Samakan kelajuan akhir saja; jangan menyamakan energi atau waktu tanpa alasan tambahan."),options=["Kelajuan dan waktu sama, energi juga sama.","Paket berat selalu tiba dengan kelajuan lebih besar.","Kelajuan akhir sama; energi dan waktu belum tentu sama."],seconds=240)
        length=1.6+.2*k;drop=length*.5;v=sqrt(20*drop)
        q("lintasan-ideal",f"Manik meluncur tanpa rotasi dari diam pada bidang licin panjang{length:g} m dengan kemiringan30°. sin30°0,5, g10. Tidak ada hambatan lain. Berapa kelajuan di dasar?",v,
          ("Kelajuan dasar dari penurunan vertikal, bukan panjang bidang langsung.","Δh=L sin30°; mgh=½mv² sehinggav=√(2gΔh).", "Panjang miring bukanh; massa tidak diperlukan setelah semua suku dibagi.",f"L{length:g} m; Δh={length:g}×0,5={drop:g} m; v0=0.",f"v=√(2×10×{length:g}×0,5).",f"v²={20*drop:g}; v≈{v:.3f} m/s. Normal tidak bekerja karena tegak lurus gerak.",f"Kelajuan dasar≈{v:.3f} m/s dalam model translasi ideal."),unit="m/s",label="Kelajuan dasar")
        weight=20;f=4;distance=2+.25*k;vin=5;v2=25-4*distance;vf=sqrt(v2)
        q("gesekan",f"Pembawa suku cadang masuk bantalan mendatar dengan5 m/s. Gaya gesek terukur4 N saat beratnya20 N. Panjang bantalan{distance:g} m, g10 danN=mg. Berapa kelajuan keluar?",vf,
          ("Kelajuan sesudah seluruh bantalan, setelahμ diturunkan dari data gaya.","μ=f/N=f/(mg); v_keluar²=v_masuk²−2μgd.","Berat20 N ialah data antara untukμ, bukan massa20 kg; jangan mengurangi4 N langsung dari kuadrat kelajuan.",f"μ=4/20=0,2; v_masuk5 m/s; d{distance:g} m.",f"v_keluar²=5²−2×(4/20)×10×{distance:g}.",f"v²={v2:g}>0 sehingga bantalan terlewati; v≈{vf:.3f} m/s. Disipasi perkg={2*distance:g} J/kg.",f"Kelajuan keluar≈{vf:.3f} m/s; sebagianEk menjadi internal."),unit="m/s",label="Kelajuan keluar",diagram=_lab("energy",m=2,h0=0,h=0,v0=5,mu=.2,s=distance,mode="friction",shape="ramp"))
        x0=1.5;x1=4.5+.5*k;d=x1-x0;v0=6;v2=v0*v0-3*d;vf=sqrt(v2)
        q("gesekan",f"Modul masuk lantai kasar pada posisi{x0:g} m dan keluar pada{x1:g} m, keduanya pada sumbu mendatar sama. Kelajuan masuk6 m/s, μ0,15, g10, N=mg. Berapa kelajuan keluar?",vf,
          ("Kelajuan di ujung dengan jarak kontak kasar yang benar.","d=x_keluar−x_masuk; v_f²=v_i²−2μgd.","Koordinat akhir bukan jarak; awal lintasan kasar tidak berada padax0=0.",f"d={x1:g}−1,5={d:g} m; v_i6 m/s; μ0,15.",f"v_f²=36−2×0,15×10×({x1:g}−1,5).",f"v_f²={v2:g}>0; v_f≈{vf:.3f} m/s. Usaha gesekan dibatasi ruas yang benar-benar dilalui.",f"Kelajuan keluar≈{vf:.3f} m/s."),unit="m/s",label="Kelajuan keluar",diagram=_lab("energy",m=1,h0=0,h=0,v0=6,mu=.15,s=d,mode="friction",shape="ramp"))
        q("rancang","Paket dilepas darih0=1,2 m, turun licin, melewati bantalan mendatar3 m denganμ0,2, lalu harus naik licin ke1 m. v0=0 dang10. Seorang siswa mengabaikan bantalan dan memperoleh2 m/s. Penilaian yang tepat adalah…",1,
          ("Verdikt keterjangkauan tujuan, bukan mengoreksi sekadar pembulatan kelajuan.","Energi perkg sesudah bantalan=g(h0−μd); target memerlukangh_D.","Kelajuan2 m/s positif dari model tanpa gesekan tidak membuktikan metode sah.","h0=1,2; μd=0,6; h_D1 m; energi perkg sesudah bantalan6 J/kg.","Ek_D/m=10×1,2−0,2×10×3−10×1.","Hasil kebutuhan bersisa−4 J/kg; D tidak tercapai. Batas tinggi saatv0=0 di tanjakan0,6 m, bukan1 m.","Tujuan tidak tercapai;Ek negatif adalah penanda keadaan yang tidak terjadi."),options=["Lolos karena2 m/s adalah bilangan nyata.","Tidak sampaiD; tinggi maksimum setelah bantalan0,6 m.","SampaiD dengan kelajuan−2 m/s."],seconds=240)
        target=2+.25*k;H=.5+.2*2.5+target*target/20
        q("rancang",f"Desain pengantar kartu harus tiba pada baki0,5 m dengan kelajuan sedikitnya{target:g} m/s. Pelepasan dari diam; bantalan mendatar2,5 m mempunyaiμ0,2; bagian lain licin tanpa puncak penghalang. g10. Berapa tinggi awal minimum?",H,
          ("Batas bawah tinggi awal untuk memenuhi kelajuan minimum, bukan tinggi sekadar dapat mencapai baki.","gh0≥gh_D+μgd+½v_min²; batas minimum memakai kesamaan.","Massa tidak diberikan karena semua suku proporsionalm; kata minimum tidak berartiv_D0.",f"h_D0,5 m; μd0,5 m; v_min{target:g} m/s; v0=0.",f"h0_min=0,5+0,2×2,5+{target:g}²/(2×10).",f"h0_min={H:g} m. Jika hanya1 m, semua energi tersisa menjadiEp dan kelajuan tiba0, belum memenuhi syarat.",f"Tinggi minimum{H:g} m untuk target≥{target:g} m/s."),unit="m",label="Tinggi awal minimum",seconds=300,tol=.01)
        H=1.6+.1*k;hmax=H-.15*4-1.5**2/20
        q("rancang",f"Pembawa barang dilepas diam pada{H:g} m dan melintasi bantalan mendatar4 m denganμ0,15. Bagian lain licin. g10. Berapa tinggi tujuan maksimum agar kelajuan tiba masih sedikitnya1,5 m/s?",hmax,
          ("Tinggi maksimum yang masih menyisakan energi gerak untukv_min1,5 m/s.","h_D≤h0−μd−v_min²/(2g), setelah persamaan per segmen disatukan.","Tinggi saat berhenti berbeda dari tinggi yang masih memenuhi kelajuan minimum; jangan menghilangkan sukuEk target.",f"h0{H:g} m; μd0,6 m; v_min²/(2g)=2,25/20=0,1125 m.",f"h_Dmaks={H:g}−0,15×4−1,5²/20.",f"h_Dmaks={hmax:g} m. Batas sekadar terjangkau{H-.6:g} m lebih tinggi0,1125 m.",f"Tujuan paling tinggi{hmax:g} m untuk syarat kelajuan ini."),unit="m",label="Tinggi tujuan maksimum",seconds=300,tol=.01)
        H=1.3+.1*k;target=2;dmax=(H-.5-.2)/.2
        q("rancang",f"Paket dilepas dari diam pada{H:g} m menuju baki0,5 m dengan syaratv_tiba≥2 m/s. Bantalan mendatarμ0,2; bagian lain licin tanpa puncak lain. g10. Berapa panjang bantalan maksimum yang masih memenuhi syarat?",dmax,
          ("Batas atas panjang bantalan; melebihinya mengurangi kelajuan di bawahtarget.","μd≤h0−h_D−v_min²/(2g), maka d_maks=[h0−h_D−v_min²/(2g)]/μ.","Memperbesar massa tidak menyelesaikan kendala karena massa tercoret; nilaiμ bukan energi dalamJ.",f"h0{H:g} m; h_D0,5 m; v_min²/(2g)0,2 m; μ0,2.",f"d_maks=({H:g}−0,5−0,2)/0,2.",f"d_maks={dmax:g} m. Substitusi kembali memberikanv_D²4 sehingga tepat2 m/s; jarak lebih pendek menghasilkan kelajuan lebih besar.",f"Panjang bantalan harus≤{dmax:g} m untuk batas bawah kelajuan yang diminta."),unit="m",label="Panjang maksimum",seconds=300,tol=.01)
    else:
        q("mekanik","Pada jalur pengembalian alat medis, pengamatA memilih dasar sebagaiEp0, pengamatB memilih meja atas. Keduanya memakai acuannya secara konsisten dan menulis neraca per segmen. Pernyataan yang tepat adalah…",1,
          ("Menilai kesetaraan dua rencana dengan pilihan nolEp berbeda.","Pergeseran acuan menambah konstanta padaEp awal danakhir; selisihnya sama.","Dasar sering nyaman tetapi tidak wajib; rumus energi tidak mensyaratkan nolEp di tanah sesungguhnya.","Kedua pengamat menilai benda, gaya gesek, dan posisi fisik sama; hanya nolEp berbeda.","(Ep_f+C)−(Ep_i+C)=Ep_f−Ep_i; usaha gesek tidak berubah.","Kelajuan dan verdikt fisika harus sama. NilaiEm numerik dapat berbeda dengan konstanta yang sama pada semua titik.","Kedua acuan sah bila konsisten, dan prediksi kelajuan sama."),options=["Hanya acuan dasar yang benar.","Kedua acuan sah dan memprediksi kelajuan sama.","PengamatB boleh mengabaikan gesekan karenaEp awal0."],level="C3",seconds=180)
        initial=48+4*k;heat=13+k;mech=initial-heat
        q("mekanik",f"Sistem kapsul–Bumi mula-mula mempunyaiEm{initial} J. Dalam lintasan berlapis, bantalan bertambah energi internal{heat} J; tidak ada motor atau transfer lain. Di tujuan tinggi tetap0,8 m. Berapa Em kapsul–Bumi di tujuan?",mech,
          ("Em akhir, bukanEk akhir atau energi total termasukbantalan.","Em_f+ΔE_internal=Em_i untuk sistem gabungan yang terisolasi dalammodel.","Tinggi0,8 m baru diperlukan bila Em harus dipecah menjadiEk danEp; pertanyaan hanya meminta jumlahnya.",f"Em_i{initial} J; ΔE_internal{heat} J; transfer lain0.",f"Em_f={initial}−{heat}.",f"Em_f={mech} J. Penjumlahannya kembali denganinternal{heat} J memberi{initial} J.",f"Em akhir{mech} J, sedangkan energi total gabungan tetap{initial} J."),label="Energi mekanik akhir",level="C3",seconds=180)
        top=1.7+.1*k;ref=.45;final=.6;drop=top-ref-final;vf=sqrt(20*drop)
        q("lintasan-ideal",f"Peluncur kamera dilepas diam pada posisi vertikal{top:g} m dari lantai. Jalurnya licin menuju titik0,6 m di atas dasar yang berada0,45 m dari lantai. Jalur panjang3 m. g10 dan semua puncak terjangkau. Berapa kelajuan tiba?",vf,
          ("Kelajuan pada posisi akhir yang tingginya harus diturunkan terhadap acuan sama.","h_f=h_dasar+0,6; v²=2g(h_i−h_f).", "Panjang3 m bukan penurunan tinggi;0,6 m bukan tinggi akhir terhadap lantai.",f"h_i{top:g} m; h_f0,45+0,6=1,05 m; turun{drop:g} m.",f"v²=2×10×({top:g}−0,45−0,6).",f"v²={20*drop:g}; v≈{vf:.3f} m/s. Massa tercoret dan jalur terjangkau sesuai data.",f"Kelajuan tiba≈{vf:.3f} m/s."),unit="m/s",label="Kelajuan tiba",diagram=_lab("energy",m=1,h0=top,h=1.05,v0=0,mu=0,s=0,mode="ideal",shape="wave"))
        q("lintasan-ideal","Kapsul perpustakaan dilepas diam dari1,4 m. Tujuan berada0,3 m, tetapi jalur licin melewati puncak1,6 m sebelum tujuan. Tidak ada penggerak. Seorang siswa menghitung√22 m/s dari dua ujung. Bagaimana penilaiannya?",2,
          ("Kesahihan prediksi kelajuan pada tujuan melalui jalur yang diberikan.","Tinggi maksimum ideal dari diamh_maks=h0; setiap penghalang harus dicek sebelum memakai keadaan akhir.","Tujuan lebih rendah bukan jaminan seluruh jalur terjangkau; angka√22 berasal dari mengabaikan puncak perantara.","h0=1,4 m; puncak1,6 m; v0=0. Energi awal perkg14 J/kg, kebutuhan puncak16 J/kg.","Ek_puncak/m=10×1,4−10×1,6=−2 J/kg.","Puncak tidak tercapai; keadaan akhir yang dipakai siswa tidak terjadi. Tidak ada kelajuan nyata di tujuan melalui jalur ini.","Perhitungan dua ujung tidak sah untuk lintasan yang puncaknya tak terjangkau."),options=["Benar karena√22 positif.","Kelajuan tujuan harus diberi tanda negatif.","Tujuan tidak dicapai karena puncak1,6 m tidak terjangkau."],seconds=240)
        end=2.4+.2*k;start=.4;d=end-start;v0=7;v2=49-5*d;vf=sqrt(v2)
        q("gesekan",f"Kapsul uji masuk bantalan datar pada koordinat0,4 m dengan7 m/s. Titik pemeriksaanM berada padakoordinat{end:g} m, masih di bantalan yang berakhir5 m. μ0,25, g10, N=mg. Berapa kelajuan diM?",vf,
          ("Kelajuan pada target di tengah, bukan setelah seluruh bantalan.","d_SM=x_M−x_awal; v_M²=v_masuk²−2μg d_SM.","Ujung bantalan5 m belum dilalui; memasukkan jarak sampaiujung akan menghitung disipasi yang belum terjadi.",f"d_SM={end:g}−0,4={d:g} m; v_masuk7 m/s; μ0,25.",f"v_M²=49−2×0,25×10×({end:g}−0,4).",f"v_M²={v2:g}>0 sehinggaM terjangkau; v_M≈{vf:.3f} m/s. Kenaikan internal perkg{2.5*d:g} J/kg.",f"Kelajuan padaM≈{vf:.3f} m/s, memakai jarak parsial{d:g} m."),unit="m/s",label="Kelajuan pada M",diagram=_lab("energy",m=1,h0=0,h=0,v0=7,mu=.25,s=d,mode="friction",shape="ramp"))
        H=2.1+.1*k;h=.5;mu=.2;d=4;v2=20*(H-h-mu*d);vf=sqrt(v2)
        q("gesekan",f"Di jalur sortir lensa, wadah dilepas diam dari{H:g} m, turun licin keB, menempuh karpet mendatarBC4 m denganμ0,2, lalu naik licin keD0,5 m. g10; normalmg diBC. Berapa kelajuan diD?",vf,
          ("Kelajuan tujuan setelah rangkaian AB,BC,CD, bukan kelajuan sebelum tanjakan.","AcuanB:Ek_B/m=gh_A; Ek_C/m=gh_A−μgd; Ek_D/m=Ek_C/m−gh_D.","Massa tidak dibutuhkan, tetapi sukuμgd tetap harus ada setelah massa tercoret.",f"h_A{H:g} m; d4 m; μ0,2; h_D0,5 m; v0=0.",f"v_D²=2[10×{H:g}−0,2×10×4−10×0,5].",f"Energi perkg:B{10*H:g}, C{10*(H-.8):g}, D{v2/2:g} J/kg; v_D≈{vf:.3f} m/s. Semua keadaan antara terjangkau.",f"KelajuanD≈{vf:.3f} m/s; internal bertambah8 J/kg sehingga Em berkurang, bukan energi total."),unit="m/s",label="Kelajuan di D",diagram=_lab("energy",m=1.3,h0=H,h=h,v0=0,mu=mu,s=d,mode="friction",shape="valley"))
        target=3+.2*k;minimum=.7+.18*3+target*target/20
        q("rancang",f"Rancangan pengantar botol dilepas dari diam menuju peron0,7 m. Alas kasar mendatar3 m memilikiμ0,18; lainnya licin tanpa puncak penghalang. Targetv_tiba≥{target:g} m/s, g10. Berapa tinggi pelepasan minimum yang harus disediakan?",minimum,
          ("Tinggi awal minimum yang menyediakanEk target,Ep peron, dan energi internal.","TulisAB,BC,CD dahulu lalu h0_min=h_D+μd+v_min²/(2g).", "Menghitung hanya selisih tinggi akan mengabaikan energi yang wajib berubah menjadi internal; massa tidak memperbaiki kekurangan perkg.",f"h_D0,7 m; μd0,54 m; v_min{target:g} m/s; v0=0.",f"h0_min=0,7+0,18×3+{target:g}²/20.",f"h0_min={minimum:g} m. Perkg kebutuhan7 J untukEp,5,4 J untukinternal, dan{target*target/2:g} J untukEk.",f"Pelepasan harus setidaknya{minimum:g} m pada modelnominal ini."),unit="m",label="Tinggi minimum",seconds=300,tol=.01)
        H=1.9+.1*k;goal=.8;target=2.5;mu=.22;dmax=(H-goal-target*target/20)/mu
        q("rancang",f"Kapsul dokumen dilepas diam pada{H:g} m menuju baki0,8 m. Hanya satu bantalan mendatar yang kasar, μ0,22. Batas kedatanganv≥2,5 m/s; g10, jalur lain licin. Berapa panjang bantalan maksimum?",dmax,
          ("Panjang maksimum yang mempertahankan kelajuan minimum, bukan jarak sampai berhenti.","Dari rencana per segmen:μgd≤g(h0−h_D)−½v_min².","Jarak henti memakai targetEk0 dan akan memberi bantalan terlalu panjang untuk syarat2,5 m/s.",f"h0{H:g}; h_D0,8; v_min2,5; μ0,22; sisa tinggi untukEk0,3125 m.",f"d_maks=({H:g}−0,8−2,5²/20)/0,22.",f"d_maks≈{dmax:.4f} m. Substitusinya memberiEk_D/m3,125 J/kg dan v_D2,5 m/s; lebihpanjang membuat syarat gagal meskipun baki mungkin masih dicapai.",f"Panjang bantalan harus≤{dmax:.4f} m."),unit="m",label="Panjang maksimum",seconds=300,tol=.01)
