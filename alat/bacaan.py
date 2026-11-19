# -*- coding: utf-8 -*-
"""Halaman bacaan konsep milik sendiri — dijamin dapat ditanam di panel."""
import os, sys, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank'))
from data_tp import TP
AKAR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media-f-mek", "bacaan")
E = lambda s: html.escape(str(s))

ISI = {
"f-mek-1-pra": [
 ("Menyambung dua panah",
  "<p>Dua perpindahan yang disambung tidak menghasilkan jarak sejauh jumlah panjangnya, kecuali keduanya searah. Berjalan 3 ubin ke depan lalu 4 ubin ke kanan membuatmu berada <b>5 ubin</b> dari titik awal, bukan 7 — walaupun kakimu memang menempuh 7 ubin.</p>"
  "<p class=\"rumus\">R = √(a² + b²) &nbsp;&nbsp; bila a dan b saling tegak lurus</p>"
  "<p>Angka 7 itu <b>jarak tempuh</b>; angka 5 itu <b>besar perpindahan</b>. Keduanya pertanyaan yang berbeda, dan soal selalu menyebut yang mana.</p>",
  "Panjang hasil dua vektor adalah jumlah panjangnya.",
  "Jumlah panjang hanya berlaku bila kedua panah searah. Begitu arahnya berbeda, hasilnya selalu lebih pendek daripada jumlahnya."),
 ("Menguraikan satu panah",
  "<p>Satu gaya miring selalu bisa diganti dua gaya tegak lurus yang akibatnya sama persis. Yang menentukan sinus atau kosinus bukan kata &ldquo;mendatar&rdquo; atau &ldquo;tegak&rdquo;, melainkan <b>sisi mana yang menempel pada sudut</b>.</p>"
  "<p class=\"rumus\">sisi yang <b>menempel</b> pada sudut → kosinus<br>sisi yang <b>berhadapan</b> dengan sudut → sinus</p>"
  "<p>Karena itu langkah pertama bukan menghitung, melainkan menjawab satu pertanyaan: <b>sudut ini diukur dari sumbu mana?</b> Tulis jawabannya sebelum menyentuh kalkulator.</p>",
  "Mendatar selalu kosinus, tegak selalu sinus.",
  "Itu hanya benar bila sudutnya kebetulan diukur dari sumbu mendatar. Diukur dari garis tegak, keduanya bertukar."),
 ("Menjumlah lewat komponen",
  "<p>Untuk gaya yang arahnya sembarang, jangan menjumlahkan besarnya. Uraikan tiap gaya menjadi komponen, jumlahkan komponen yang searah, baru gabungkan kembali.</p>"
  "<p class=\"rumus\">ΣFx = F₁cos θ₁ + F₂cos θ₂ + …<br>ΣFy = F₁sin θ₁ + F₂sin θ₂ + …<br>R = √(ΣFx² + ΣFy²)</p>"
  "<p>Komponen yang berlawanan dengan arah positif ditulis <b>dengan tanda negatif</b>, bukan dibuang tandanya. Tanda itulah yang menyimpan informasi arah.</p>",
  "Semua komponen ditulis positif karena yang diambil besarnya.",
  "Begitu tandanya dibuang, arahnya hilang — dan hasil penjumlahanmu menjadi terlalu besar."),
 ("Memilih sumbu pada bidang miring",
  "<p>Pada bidang miring, sumbu mendatar–tegak justru menyulitkan. Pilih sumbu yang <b>sejajar</b> dan <b>tegak lurus</b> bidang: gaya normal dan arah gerak langsung jatuh di sumbu, sehingga tidak ada yang perlu diuraikan dua kali.</p>"
  "<p class=\"rumus\">W<sub>sejajar</sub> = W sin θ &nbsp;·&nbsp; W<sub>tegak lurus</sub> = W cos θ</p>"
  "<p>Makin curam bidangnya, makin besar komponen yang menuruni bidang, dan makin kecil yang menekan bidang. Beratnya sendiri tidak berubah sedikit pun.</p>",
  "Komponen sejajar bidang adalah berat dikali kosinus sudut bidang.",
  "Komponen sejajar berhadapan dengan sudut bidang, jadi ia memakai sinus. Periksa dengan bidang yang hampir datar: komponen yang menuruni bidang harus hampir nol."),
],
"f-mek-2": [
 ("Gaya nyata punya pemberi",
  "<p>Setiap panah pada diagram gaya harus bisa dijawab dengan satu pertanyaan: <b>siapa yang memberikannya?</b> Bumi, tali, lantai, udara, tangan. Panah yang tidak punya pemberi bukan gaya, dan harus dihapus.</p>"
  "<p>Kerikil yang sudah lepas dari ketapel hanya punya satu gaya: beratnya. Ketapelnya sudah tidak menyentuhnya lagi.</p>",
  "Benda yang bergerak ke kanan pasti punya gaya ke kanan.",
  "Gerak tidak memerlukan gaya untuk dipertahankan. Yang memerlukan gaya adalah <b>perubahan</b> gerak."),
 ("Gaya neto menentukan keadaan gerak",
  "<p>Gaya dijumlahkan dengan tanda arah, bukan dengan besarnya saja. Tetapkan dulu arah positif, lalu tulis setiap gaya dengan tandanya.</p>"
  "<p class=\"rumus\">ΣF = 0 → kecepatan <b>tetap</b> (boleh diam, boleh meluncur)<br>ΣF ≠ 0 → kecepatan <b>berubah</b></p>"
  "<p>Perhatikan baris pertama: gaya neto nol tidak berarti benda diam. Peti yang meluncur dengan kecepatan tetap juga memiliki ΣF = 0.</p>",
  "Gaya neto nol berarti benda pasti diam.",
  "Gaya neto nol hanya berarti kecepatannya tidak berubah. Berapa pun kecepatan itu — termasuk nol."),
 ("Percepatan: gaya neto dibagi massa",
  "<p>Gaya neto adalah sebabnya, percepatan adalah akibatnya, dan massa adalah yang menahan akibat itu.</p>"
  "<p class=\"rumus\">a = ΣF / m</p>"
  "<p>Melepas dorongan tidak membuat benda berhenti seketika. Yang hilang hanya dorongannya; gesekan masih ada, dan gesekan memerlukan waktu untuk menghabiskan kecepatan.</p>",
  "Dorongan dilepas, gerobak berhenti seketika.",
  "Sesudah dorongan hilang, ΣF = gesekan saja. Itu percepatan ke belakang yang terbatas, jadi kecepatannya turun bertahap."),
 ("Aksi dan reaksi: dua benda",
  "<p>Pasangan aksi dan reaksi selalu sama besar, berlawanan arah, dan — ini yang sering terlupa — <b>bekerja pada dua benda yang berbeda</b>. Karena itu keduanya tidak pernah dijumlahkan.</p>"
  "<p class=\"rumus\">Bumi menarik pot → pasangannya: pot menarik Bumi<br>rak menekan pot → pasangannya: pot menekan rak</p>"
  "<p>Cara memeriksanya: tukar posisi pemberi dan penerima. Kalau kalimatmu tetap masuk akal, itu pasangannya.</p>",
  "Berat dan normal adalah pasangan aksi dan reaksi.",
  "Keduanya bekerja pada benda yang sama, yaitu potnya. Itu gaya seimbang, bukan pasangan aksi–reaksi."),
],
"f-mek-1a": [
 ("Hukum I sebagai sebab dan akibat",
  "<p>Hukum I bukan sekadar bunyi kalimat. Ia menjelaskan <b>mengapa</b> keadaan gerak bertahan: karena tidak ada sebab yang mengubahnya.</p>"
  "<p>Penumpang yang terdorong ke depan saat bus direm bukan didorong apa pun. Tubuhnya hanya melanjutkan gerak yang sudah ia miliki, sementara busnya melambat.</p>",
  "Kelembaman adalah gaya yang mendorong atau menahan benda.",
  "Kelembaman bukan gaya; ia tidak punya pemberi. Ia nama bagi kecenderungan benda mempertahankan keadaan geraknya."),
 ("Hukum II: massa menahan akibat",
  "<p>Gaya neto yang sama tidak memberi percepatan yang sama. Benda yang lebih bermassa menahan perubahan kecepatan lebih kuat.</p>"
  "<p class=\"rumus\">a = ΣF / m &nbsp;→&nbsp; ΣF tetap, m naik dua kali, a turun separuh</p>"
  "<p>Percepatan searah dengan <b>gaya neto</b>, bukan dengan geraknya. Timba yang turun melambat punya percepatan ke atas, padahal geraknya ke bawah.</p>",
  "Percepatan selalu searah dengan gerak.",
  "Percepatan searah dengan gaya neto. Ketika keduanya berlawanan dengan gerak, bendanya melambat."),
 ("Hukum III: dua benda, dua percepatan",
  "<p>Gaya tidak pernah sendirian. Setiap kali satu benda memberi gaya, ia menerima gaya yang sama besar dan berlawanan dari benda yang dikenainya.</p>"
  "<p>Dua perahu yang saling mendorong menerima gaya yang sama besar, tetapi percepatannya berbeda bila massanya berbeda — karena a = F/m dihitung untuk tiap benda sendiri-sendiri.</p>",
  "Aksi dan reaksi saling meniadakan, jadi tidak ada yang bergerak.",
  "Meniadakan hanya berlaku untuk gaya pada <b>satu</b> benda yang sama. Di sini keduanya pada benda berbeda, jadi masing-masing tetap dipercepat."),
 ("Contoh yang cocok, bukan contoh yang mirip",
  "<p>Contoh dinilai dari <b>cara kerjanya</b>, bukan dari sekadar melibatkan gaya. Contoh kelembaman tidak bisa dipakai untuk Hukum III, sebanyak apa pun gaya yang disebut di dalamnya.</p>"
  "<p>Uji contohmu dengan tiga pertanyaan: ada berapa benda? siapa memberi gaya kepada siapa? apa yang dijelaskan — bertahannya gerak, berubahnya gerak, atau pasangan gaya?</p>",
  "Peristiwa yang sama dengan benda diganti adalah contoh baru.",
  "Mengganti jeruk dengan apel tidak mengubah mekanismenya. Contoh baru harus peristiwa yang berbeda."),
],
"f-mek-1b": [
 ("Memisahkan yang menentukan dari pengecoh",
  "<p>Sebuah keterangan relevan bila ia mengubah salah satu dari tiga hal: <b>gaya</b> yang bekerja, <b>lengan</b> gaya itu terhadap poros, atau <b>batas patah</b> bahannya. Selain itu, pengecoh.</p>"
  "<p>Warna cat, merek, dan nama toko tidak mengubah ketiganya. Menandainya relevan membuat analisismu penuh angka yang tidak pernah dipakai.</p>",
  "Warna, merek, atau berat udara ikut menentukan kuat tidaknya struktur.",
  "Uji tiap keterangan dengan tiga kata itu. Kalau tidak mengubah gaya, lengan, atau batas patah, ia pengecoh."),
 ("Dua syarat kesetimbangan",
  "<p>Benda tegar yang setimbang memenuhi <b>dua</b> syarat sekaligus, bukan satu.</p>"
  "<p class=\"rumus\">ΣF = 0 &nbsp;(tidak bergeser)<br>Στ = 0 &nbsp;(tidak berputar)</p>"
  "<p>Momen dihitung terhadap poros: τ = F × d, dengan d jarak tegak lurus dari poros ke garis kerja gaya. Beban yang sama di lengan yang lebih panjang memberi momen yang lebih besar.</p>",
  "Bila jumlah gaya nol, batang pasti setimbang.",
  "Dua gaya sama besar berlawanan arah di dua ujung batang menghasilkan ΣF = 0 tetapi Στ ≠ 0 — batangnya berputar."),
 ("Menguraikan tegangan miring",
  "<p>Kabel miring tidak menahan beban dengan seluruh tegangannya. Hanya <b>komponen tegaknya</b> yang menahan berat; komponen mendatarnya ditahan engsel.</p>"
  "<p class=\"rumus\">T sin θ = W &nbsp;→&nbsp; T = W / sin θ</p>"
  "<p>Karena sin θ selalu kurang dari 1, tegangan kabel <b>selalu lebih besar</b> daripada beban yang ditahannya. Makin landai kabelnya, makin besar tegangannya.</p>",
  "Seluruh tegangan tali miring menahan berat beban.",
  "Kalau benar begitu, tegangan akan sama dengan berat. Periksa dengan kabel yang hampir mendatar: tegangannya justru melonjak."),
 ("Peran penyangga diagonal",
  "<p>Jawaban &ldquo;supaya lebih kokoh&rdquo; tidak menjelaskan apa pun. Yang sebenarnya terjadi: komponen tegak penyangga memikul beban, sehingga engsel <b>tidak lagi menahan momen</b> — ia tinggal menahan gaya mendatar.</p>"
  "<p>Tanpa penyangga, engsel harus menahan momen sebesar berat dikali panjang menjulur. Itulah yang membuat batang berengsel saja melengkung.</p>",
  "Penyangga miring dipasang supaya struktur lebih kokoh.",
  "Sebutkan mekanismenya: komponen mana yang memikul beban, dan momen apa yang hilang dari engsel."),
],
}

HAL = """<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{judul}</title><link rel="stylesheet" href="bacaan.css"></head><body>
<article class="isi">
<p class="label">{kode}</p>
<h1>{judul}</h1>
<p class="lede">{lede}</p>
{bab}
<p class="kaki">CMS FIMS &middot; Fisika &middot; Fitrah Islamic World Academy</p>
</article></body></html>
"""
BAB = """<section class="lk">
<h2><span class="n">{n}</span>{nama}</h2>
{teks}
<div class="awas"><p class="salah">Yang sering dikira benar: &ldquo;{miskon}&rdquo;</p>
<p class="bahas">{bantah}</p></div>
</section>
"""

def jalankan():
    os.makedirs(AKAR, exist_ok=True)
    n = 0
    for t in TP:
        bab = "".join(BAB.format(n=i+1, nama=E(nama), teks=teks, miskon=E(mis), bantah=bantah)
                      for i, (nama, teks, mis, bantah) in enumerate(ISI[t["slug"]]))
        isi = HAL.format(judul=E(t["judul"]), kode=E(t["kode"]), bab=bab,
                         lede=E(t["teks"]))
        open(os.path.join(AKAR, f"bacaan-{t['slug']}.html"), "w", encoding="utf-8").write(isi)
        n += 1
    print(n, "halaman bacaan ditulis")

if __name__ == "__main__": jalankan()
