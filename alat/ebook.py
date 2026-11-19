#!/usr/bin/env python3
"""Menulis halaman topik KUMPULAN E-BOOK (jalur Olimpiade).

Setiap buku punya kunci "pdf": DAFTAR bagian berkas. Satu bagian = satu berkas PDF di aset-ebook/.
Buku di bawah 25 MiB cukup satu bagian; buku yang lebih besar dipotong dulu dengan alat/pecah-pdf.py
(batas Cloudflare Pages 25 MiB per berkas, batas unggah web GitHub 25 MB). Halaman menampilkan
panel PDF dengan pemilih bagian, tombol buka-tab-baru dan unduh, serta (bila "bab_hal" diisi)
daftar bab yang bisa diklik untuk melompat ke halamannya.
Bila berkas belum diunggah, panel menampilkan keterangan, bukan bingkai kosong.

Jalankan:  cd alat && python3 ebook.py   lalu   cd .. && node build.js
"""
import json, os, html

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR  = os.path.join(AKAR, "konten", "kumpulan-ebook", "paket")
E = html.escape

BUKU = [
  {
    "slug": "modul-praktis-master-fisika",
    "tahap": "karya",
    "judul": "Modul Praktis Master Fisika",
    "anak": "Konsep, Penurunan Rumus, dan Ilustrasi Visual",
    "penulis": "Komaruddin, S.Si., M.Si., Gr",
    "terbit": "Edisi Pertama, 2026 · diterbitkan mandiri",
    "bahasa": "Indonesia",
    "pdf": [{"berkas": "aset-ebook/modul-praktis-master-fisika.pdf", "label": "Buku utuh"}],
    "hak": "© 2026 Komaruddin. Boleh dipakai untuk pembelajaran non-komersial oleh guru dan siswa dengan mencantumkan sumber. Dilarang memperjualbelikan.",
    "ringkas": "Buku pegangan pembinaan olimpiade. Tiga puluh bab dari besaran hingga fisika inti, masing-masing dengan definisi tegas, konsep kunci, dan penurunan rumus langkah demi langkah. Sengaja tanpa contoh soal: dipakai untuk membangun pemahaman sebelum latihan.",
    "cara": [
      "Baca satu bab sebelum mengerjakan paket soal bidang yang sama.",
      "Tutup bukunya, lalu turunkan ulang rumus utama bab itu di kertas. Kalau macet, kembali ke langkah tempat kamu macet — bukan ke rumus akhirnya.",
      "Tandai penurunan yang belum kamu pahami dan bawa ke sesi pembinaan.",
    ],
    "bab": ["Besaran dan Vektor","Kinematika Gerak Lurus","Gerak Melingkar","Gaya","Gaya Gravitasi",
            "Momentum dan Impuls","Usaha dan Energi","Dinamika Rotasi","Kesetimbangan Benda Tegar",
            "Fluida Statis","Fluida Dinamis","Suhu dan Kalor","Teori Kinetik Gas","Termodinamika",
            "Elastisitas dan Getaran","Gelombang dan Bunyi","Optik","Alat-Alat Optik","Pembiasan Cahaya",
            "Optik Fisis","Listrik Statis","Listrik DC","Medan Magnet","Induksi Elektromagnetik",
            "Listrik AC","Gelombang Elektromagnetik","Teori Relativitas Khusus","Radiasi dan Teori Kuantum",
            "Fisika Atom","Fisika Inti dan Radioaktivitas"],
    "peta": [("Kinematika", "1–3"), ("Dinamika & gravitasi", "4–5"), ("Momentum & energi", "6–7"),
             ("Rotasi & benda tegar", "8–9"), ("Fluida", "10–11"), ("Termal", "12–14"),
             ("Getaran & gelombang", "15–16"), ("Optik", "17–20"), ("Listrik & magnet", "21–26"),
             ("Fisika modern", "27–30")],
  },
  {
    "slug": "introduction-to-classical-mechanics-morin",
    "tahap": "rujukan",
    "judul": "Introduction to Classical Mechanics",
    "anak": "With Problems and Solutions",
    "penulis": "David Morin",
    "terbit": "Cambridge University Press, 2008 · ISBN 978-0-521-87622-3",
    "bahasa": "Inggris",
    "pdf": [{"berkas": "aset-ebook/introduction-to-classical-mechanics-morin.pdf", "label": "Buku utuh"}],
    "hak": "Hak cipta pada David Morin dan Cambridge University Press. Dimuat di sini untuk pembinaan internal FIWA. Jangan disebarkan ulang; untuk koleksi sekolah, beli atau pinjam salinan resminya.",
    "ringkas": "Rujukan mekanika paling dihormati untuk pembinaan olimpiade tingkat lanjut. Kuat di strategi menyelesaikan soal, analisis limit dan dimensi, serta ratusan soal berpembahasan lengkap. Cocok untuk siswa yang sudah tuntas mekanika tingkat SMA dan bersiap ke OSN nasional atau seleksi internasional.",
    "cara": [
      "Mulai dari Bab 1 (Strategies for Solving Problems) — gratis di bawah, dan paling berguna dari seluruh buku.",
      "Untuk bab lain, pakai peta di bawah: kerjakan bidang OSN yang sedang dibina, bukan urut dari depan.",
      "Kerjakan soal bertanda satu atau dua bintang dulu; bintang tiga dan empat untuk persiapan seleksi internasional.",
    ],
    "gratis": [
      ("Daftar isi & prakata", "https://davidmorin.physics.fas.harvard.edu/sites/g/files/omnuum12331/files/2025-10/cmchap0.pdf"),
      ("Bab 1 · Strategies for Solving Problems", "https://davidmorin.physics.fas.harvard.edu/sites/g/files/omnuum12331/files/2025-10/cmchap1.pdf"),
      ("Bab 6 · The Lagrangian Method", "https://davidmorin.physics.fas.harvard.edu/sites/g/files/omnuum12331/files/2025-10/cmchap6.pdf"),
      ("Bab 11 · Relativity (Kinematics)", "https://davidmorin.physics.fas.harvard.edu/sites/g/files/omnuum12331/files/2025-10/cmchap11.pdf"),
      ("Bab tambahan · Hamiltonian Mechanics", "https://davidmorin.physics.fas.harvard.edu/sites/g/files/omnuum12331/files/2025-10/cmchap15.pdf"),
      ("Lampiran A–J", "https://davidmorin.physics.fas.harvard.edu/sites/g/files/omnuum12331/files/2025-10/cmappendices.pdf"),
      ("Ralat (errata)", "https://davidmorin.physics.fas.harvard.edu/sites/g/files/omnuum12331/files/2025-10/corrections.pdf"),
    ],
    "resmi": [
      ("Halaman buku di situs David Morin (Harvard)", "https://davidmorin.physics.fas.harvard.edu/books/classical-mechanics"),
      ("Halaman buku di Cambridge University Press", "https://www.cambridge.org/us/academic/subjects/physics/general-and-classical-physics/introduction-classical-mechanics-problems-and-solutions?format=HB"),
      ("Pratinjau halaman di Google Books", "https://books.google.com/books?id=Ni6CD7K2X4MC"),
    ],
    "bab": ["Strategies for Solving Problems","Statics","Using F = ma","Oscillations",
            "Conservation of Energy and Momentum","The Lagrangian Method","Central Forces",
            "Angular Momentum, Part I (Constant L̂)","Angular Momentum, Part II (General L̂)",
            "Accelerating Frames of Reference","Relativity (Kinematics)","Relativity (Dynamics)",
            "4-vectors","General Relativity"],
    "peta": [("Semua bidang · cara berpikir", "1"), ("Kesetimbangan", "2"), ("Dinamika", "3"),
             ("Getaran", "4"), ("Momentum & energi", "5"), ("Gravitasi & orbit", "7"),
             ("Rotasi & benda tegar", "8–9"), ("Kerangka dipercepat", "10"),
             ("Fisika modern · relativitas", "11–12"),
             ("Lanjutan, di atas OSN nasional", "6, 13–14")],
  },
  {
    "slug": "fundamentals-of-physics-halliday",
    "tahap": "rujukan",
    "judul": "Fundamentals of Physics",
    "anak": "Extended, 10th Edition",
    "penulis": "David Halliday, Robert Resnick, Jearl Walker",
    "terbit": "John Wiley & Sons, 2014 · ISBN 978-1-118-23072-5",
    "bahasa": "Inggris",
    # Berkas asli 1.450 halaman (±51 MiB) dipotong 4 dengan alat/pecah-pdf.py. Nomor halaman = halaman PDF asli.
    "pdf": [
      {"berkas": "aset-ebook/fundamentals-of-physics-halliday-1.pdf", "awal": 1,    "akhir": 282,  "label": "Bagian 1 · Prakata, Bab 1–9 · Mekanika"},
      {"berkas": "aset-ebook/fundamentals-of-physics-halliday-2.pdf", "awal": 283,  "akhir": 634,  "label": "Bagian 2 · Bab 10–20 · Rotasi sampai termodinamika"},
      {"berkas": "aset-ebook/fundamentals-of-physics-halliday-3.pdf", "awal": 635,  "akhir": 1035, "label": "Bagian 3 · Bab 21–33 · Listrik dan magnet"},
      {"berkas": "aset-ebook/fundamentals-of-physics-halliday-4.pdf", "awal": 1036, "akhir": 1450, "label": "Bagian 4 · Bab 34–44, lampiran, jawaban, indeks · Optik dan fisika modern"},
    ],
    "bab_hal": [27,39,66,88,120,150,175,203,240,283,321,353,380,412,439,470,505,540,575,609,635,656,685,711,
                743,771,797,829,862,890,929,967,998,1036,1073,1107,1142,1179,1212,1245,1278,1302,1335,1360],
    "lain_hal": [("Lampiran (konstanta, rumus, tabel)", 1395), ("Jawaban soal ganjil", 1411), ("Indeks", 1425)],
    "hak": "Hak cipta pada John Wiley & Sons. Dimuat di sini untuk pembinaan internal FIWA. Jangan disebarkan ulang; untuk koleksi sekolah, beli atau pinjam salinan resminya.",
    "ringkas": "Buku teks fisika dasar universitas yang menjadi rujukan baku pembinaan OSN. Keunggulannya: cakupan lengkap dari pengukuran hingga fisika partikel, penjelasan konsep yang runtut, dan bank soal sangat besar yang bertingkat dari mudah ke sulit di akhir tiap bab.",
    "cara": [
      "Pakai peta di bawah untuk memilih bab sesuai bidang OSN yang sedang dibina.",
      "Soal di akhir bab disusun dari mudah ke sulit. Untuk OSN, lewati yang paling awal dan mulai dari pertengahan.",
      "Jawaban soal bernomor ganjil ada di bagian belakang buku — pakai untuk memeriksa, bukan untuk mencontek langkah.",
    ],
    "pengganti": [
      ("OpenStax University Physics · Volume 1 — mekanika, getaran, gelombang", "https://openstax.org/books/university-physics-volume-1/pages/preface"),
      ("OpenStax University Physics · Volume 2 — termodinamika, listrik, magnet", "https://openstax.org/books/university-physics-volume-2/pages/preface"),
      ("OpenStax University Physics · Volume 3 — optik, fisika modern", "https://openstax.org/books/university-physics-volume-3/pages/preface"),
    ],
    "bab": ["Measurement","Motion Along a Straight Line","Vectors","Motion in Two and Three Dimensions",
            "Force and Motion—I","Force and Motion—II","Kinetic Energy and Work",
            "Potential Energy and Conservation of Energy","Center of Mass and Linear Momentum","Rotation",
            "Rolling, Torque, and Angular Momentum","Equilibrium and Elasticity","Gravitation","Fluids",
            "Oscillations","Waves—I","Waves—II","Temperature, Heat, and the First Law of Thermodynamics",
            "The Kinetic Theory of Gases","Entropy and the Second Law of Thermodynamics","Coulomb’s Law",
            "Electric Fields","Gauss’ Law","Electric Potential","Capacitance","Current and Resistance",
            "Circuits","Magnetic Fields","Magnetic Fields Due to Currents","Induction and Inductance",
            "Electromagnetic Oscillations and Alternating Current","Maxwell’s Equations; Magnetism of Matter",
            "Electromagnetic Waves","Images","Interference","Diffraction","Relativity",
            "Photons and Matter Waves","More About Matter Waves","All About Atoms",
            "Conduction of Electricity in Solids","Nuclear Physics","Energy from the Nucleus",
            "Quarks, Leptons, and the Big Bang"],
    "peta": [("Besaran & vektor", "1, 3"), ("Kinematika", "2, 4"), ("Dinamika", "5–6"),
             ("Momentum & energi", "7–9"), ("Rotasi & benda tegar", "10–12"), ("Gravitasi", "13"),
             ("Fluida", "14"), ("Getaran & gelombang", "15–17"), ("Termal", "18–20"),
             ("Listrik", "21–27"), ("Magnet & induksi", "28–33"), ("Optik", "34–36"),
             ("Fisika modern", "37–44")],
  },
]

GAYA = """
:root{--tosca0:#073B44;--tosca:#0B4F58;--tosca2:#17A2AF;--toscaB:#E3F5F6;--oranye:#C05621;--oranyeB:#FDEBDD;
--tinta:#12333A;--abu:#6A7F84;--abuB:#F1F5F6;--garis:#D7E6E8;--putih:#fff}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--abuB);color:var(--tinta);font:16px/1.6 'Segoe UI',system-ui,-apple-system,Roboto,Arial,sans-serif}
.bungkus{max-width:900px;margin:0 auto;padding:0 16px 56px}
header.kepala{background:linear-gradient(135deg,var(--tosca0),var(--tosca2));color:#fff;padding:28px 16px}
header.kepala .in{max-width:900px;margin:0 auto;display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:center}
.sampul{width:96px;height:132px;border-radius:6px;background:linear-gradient(160deg,rgba(255,255,255,.22),rgba(255,255,255,.04));
  border:1px solid rgba(255,255,255,.35);display:flex;flex-direction:column;justify-content:flex-end;padding:9px;font-size:.62rem;
  line-height:1.25;letter-spacing:.02em;box-shadow:0 8px 20px rgba(0,0,0,.18)}
.sampul b{display:block;font-size:.78rem;margin-bottom:4px;line-height:1.15}
.kode{display:inline-block;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;opacity:.85}
header h1{margin:.15rem 0 .1rem;font-size:1.55rem;line-height:1.2}
header .anak{margin:0;opacity:.9}
header .penulis{margin:.5rem 0 0;font-size:.9rem;opacity:.95}
.kartu{background:var(--putih);border:1px solid var(--garis);border-radius:10px;padding:18px 18px;margin-top:16px}
.kartu h2{margin:0 0 .6rem;font-size:1.08rem;color:var(--tosca)}
.meta{display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:0;font-size:.92rem}
.meta dt{color:var(--abu)}.meta dd{margin:0}
.hak{background:var(--oranyeB);border-left:3px solid var(--oranye);padding:10px 12px;border-radius:6px;font-size:.88rem;margin-top:12px}
ol.cara{margin:0;padding-left:1.25rem}ol.cara li{margin:.25rem 0}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th,td{padding:7px 9px;border-bottom:1px solid var(--garis);text-align:left;vertical-align:top}
th{color:var(--abu);font-weight:600;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em}
td.no{white-space:nowrap;font-variant-numeric:tabular-nums;color:var(--tosca);font-weight:600}
.gulir{overflow-x:auto}
ol.bab{columns:2;column-gap:28px;margin:0;padding-left:1.6rem;font-size:.9rem}
ol.bab li{break-inside:avoid;padding:2px 0}
@media (max-width:620px){ol.bab{columns:1}header.kepala .in{grid-template-columns:1fr}.sampul{display:none}}
.tombol{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:8px 13px;border-radius:7px;border:1px solid var(--tosca2);
  background:var(--tosca2);color:#fff;text-decoration:none;font-size:.88rem;font-weight:600;cursor:pointer;font-family:inherit}
.btn.tenang{background:transparent;color:var(--tosca)}
.btn[aria-pressed="true"]{background:var(--tosca);border-color:var(--tosca);color:#fff}
iframe.berkas{display:block;width:100%;height:78vh;min-height:520px;border:1px solid var(--garis);border-radius:8px;background:#fff;margin-top:12px}
.belum{background:var(--toscaB);border:1px dashed var(--tosca2);border-radius:8px;padding:16px;margin-top:12px;font-size:.92rem}
ul.taut{margin:0;padding:0;list-style:none}ul.taut li{padding:6px 0;border-bottom:1px solid var(--garis)}
ul.taut li:last-child{border-bottom:0}ul.taut a{color:var(--tosca);font-weight:600}
.kecil{font-size:.84rem;color:var(--abu);margin:.5rem 0 0}
details.kartu>summary{cursor:pointer;font-weight:600;color:var(--tosca)}
details.kartu[open]>summary{margin-bottom:.6rem}
ol.bab a.loncat{color:var(--tosca);text-decoration:none}ol.bab a.loncat:hover{text-decoration:underline}
ul.bab-lain{margin:.7rem 0 0;padding:.6rem 0 0;list-style:none;border-top:1px solid var(--garis);font-size:.9rem}
ul.bab-lain a{color:var(--tosca);font-weight:600;text-decoration:none}ul.bab-lain a:hover{text-decoration:underline}
.tombol button.btn{font-size:.82rem;text-align:left}
footer.kaki{text-align:center;color:var(--abu);font-size:.8rem;padding:24px 16px}
"""

def kepala(b):
    return f"""<header class="kepala"><div class="in">
<div class="sampul" aria-hidden="true"><b>{E(b['judul'])}</b>{E(b['penulis'].split(',')[0])}</div>
<div><span class="kode">{'Karya pembina FIWA' if b['tahap']=='karya' else 'Buku rujukan'} · {E(b['bahasa'])}</span>
<h1>{E(b['judul'])}</h1><p class="anak">{E(b['anak'])}</p>
<p class="penulis">{E(b['penulis'])}</p></div></div></header>"""

def info_berkas(b):
    n = len(b['pdf'])
    ada = [os.path.join(AKAR, x['berkas']) for x in b['pdf']]
    mib = sum(os.path.getsize(f) for f in ada if os.path.exists(f)) / 1048576
    ukur = f' · ±{mib:.0f} MiB' if mib else ''
    return f"<dt>Berkas</dt><dd>{'PDF' if n == 1 else str(n) + ' bagian PDF'}{ukur}</dd>"

def kartu_data(b):
    return f"""<div class="kartu"><h2>Tentang buku ini</h2>
<p style="margin-top:0">{E(b['ringkas'])}</p>
<dl class="meta"><dt>Penulis</dt><dd>{E(b['penulis'])}</dd><dt>Terbitan</dt><dd>{E(b['terbit'])}</dd>
<dt>Bahasa</dt><dd>{E(b['bahasa'])}</dd><dt>Isi</dt><dd>{len(b['bab'])} bab</dd>{info_berkas(b)}</dl>
<div class="hak">{E(b['hak'])}</div></div>"""

def kartu_cara(b):
    return '<div class="kartu"><h2>Cara memakainya untuk pembinaan</h2><ol class="cara">' + \
        ''.join(f'<li>{E(x)}</li>' for x in b['cara']) + '</ol></div>'

def kartu_peta(b):
    baris = ''.join(f'<tr><td>{E(a)}</td><td class="no">Bab {E(n)}</td></tr>' for a, n in b['peta'])
    return f"""<div class="kartu"><h2>Peta bab ke bidang OSN</h2>
<div class="gulir"><table><tr><th>Bidang</th><th>Baca</th></tr>{baris}</table></div></div>"""

def lokasi(b, hal):
    """Nomor halaman PDF asli -> (indeks bagian, halaman di dalam bagian itu)."""
    for i, x in enumerate(b['pdf']):
        if x.get('awal') and x['awal'] <= hal <= x['akhir']:
            return i, hal - x['awal'] + 1
    return None

def kartu_bab(b):
    hal = b.get('bab_hal')
    if not hal:
        return '<div class="kartu"><h2>Daftar bab</h2><ol class="bab">' + \
            ''.join(f'<li>{E(x)}</li>' for x in b['bab']) + '</ol></div>'
    def tautan(judul, h):
        i, p = lokasi(b, h)
        return f'<a href="#baca" class="loncat" data-bagian="{i}" data-hal="{p}">{E(judul)}</a>'
    isi = ''.join(f'<li>{tautan(j, h)}</li>' for j, h in zip(b['bab'], hal))
    lain = ''.join(f'<li class="lain">{tautan(j, h)}</li>' for j, h in b.get('lain_hal', []))
    return f"""<div class="kartu"><h2>Daftar bab</h2>
<p class="kecil" style="margin-top:0">Klik satu bab: panel baca di atas langsung pindah ke halamannya.</p>
<ol class="bab">{isi}</ol>
<ul class="bab-lain">{lain}</ul></div>"""

def kartu_berkas(b):
    bag = [{"src": '../../../' + x['berkas'], "path": x['berkas'], "label": x['label']} for x in b['pdf']]
    pilih = ''
    if len(bag) > 1:
        pilih = '<div class="tombol" id="pilih-bagian" role="group" aria-label="Pilih bagian">' + ''.join(
            f'<button type="button" class="btn tenang" data-i="{i}" aria-pressed="false">{E(x["label"])}</button>'
            for i, x in enumerate(bag)) + '</div>'
    return f"""<div class="kartu" id="baca"><h2>Baca e-book</h2>
{pilih}
<div class="tombol" id="alat-baca"><a class="btn tenang" id="tab-baru" href="{bag[0]['src']}" target="_blank" rel="noopener">Buka penuh di tab baru ↗</a>
<a class="btn tenang" id="unduh" href="{bag[0]['src']}" download>Unduh bagian ini (PDF)</a></div>
<div id="wadah"></div>
<p class="kecil">Di HP, penampil PDF dalam halaman sering hanya menampilkan halaman pertama. Bila begitu, pakai <b>Buka penuh di tab baru</b>.
Panel bookmark di penampil (ikon daftar di kiri atas) memuat bab dan subbab.</p>
<script>
(function(){{
  var BAG = {json.dumps(bag, ensure_ascii=False)};
  var ada = [];          // true / false / undefined (belum diketahui)
  var wadah = document.getElementById('wadah');
  var tabBaru = document.getElementById('tab-baru'), unduh = document.getElementById('unduh');
  var pilih = document.getElementById('pilih-bagian');
  function tampil(i, hal){{
    var x = BAG[i];
    if (pilih) pilih.querySelectorAll('button').forEach(function(t){{ t.setAttribute('aria-pressed', String(t.getAttribute('data-i') === String(i))); }});
    var u = x.src + (hal ? '#page=' + hal + '&view=FitH' : '');
    tabBaru.href = u; unduh.href = x.src;
    if (ada[i] === false) {{
      wadah.innerHTML = '<div class="belum"><b>Berkas PDF belum diunggah.</b><br>Taruh berkasnya di <code>' + x.path +
        '</code> pada repositori, lalu terbitkan ulang. Halaman ini akan langsung menampilkannya.</div>';
      tabBaru.style.display = unduh.style.display = 'none';
      return;
    }}
    tabBaru.style.display = unduh.style.display = '';
    // bingkai dibuat baru tiap kali: pindah halaman lewat #page= tidak andal di bingkai yang sudah terbuka
    wadah.innerHTML = '';
    var f = document.createElement('iframe');
    f.className = 'berkas'; f.title = x.label; f.src = u;
    wadah.appendChild(f);
  }}
  function periksa(i){{
    return fetch(BAG[i].src, {{ method: 'HEAD', credentials: 'same-origin' }})
      .then(function(r){{ ada[i] = r.ok; }}).catch(function(){{ /* tak diketahui: coba tampilkan saja */ }});
  }}
  var cek = BAG.map(function(_, i){{ return periksa(i); }});
  Promise.all(cek).then(function(){{ tampil(0); }});
  if (pilih) pilih.addEventListener('click', function(e){{
    var t = e.target.closest('button[data-i]'); if (t) tampil(Number(t.getAttribute('data-i')));
  }});
  document.addEventListener('click', function(e){{
    var a = e.target.closest('a.loncat'); if (!a) return;
    e.preventDefault();
    tampil(Number(a.getAttribute('data-bagian')), Number(a.getAttribute('data-hal')));
    document.getElementById('baca').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }});
}})();
</script></div>"""

def kartu_gratis(b):
    if not b.get('gratis'): return ''
    tombol = ''.join(f'<button type="button" class="btn tenang" data-src="{E(u)}" aria-pressed="false">{E(j)}</button>'
                     for j, u in b['gratis'])
    buka = '<details class="kartu"><summary>Cadangan: bab yang dibagikan gratis oleh penulis</summary>'
    return f"""{buka}
<p style="margin-top:0">David Morin membagikan bagian-bagian ini sendiri di situs resminya. Dipakai bila berkas utuh di atas tidak tampil. Pilih satu untuk dibaca di sini.</p>
<div class="tombol" id="pilih-bab">{tombol}</div>
<div id="wadah-bab" class="belum">Pilih salah satu bab di atas.</div>
<p class="kecil">Berkasnya dimuat dari server Harvard. Bila kotaknya tetap kosong, server itu menolak ditampilkan di dalam halaman lain —
pakai tautan <b>Buka penuh di tab baru</b> yang muncul di atas kotak.</p>
<script>
(function(){{
  var w = document.getElementById('wadah-bab');
  document.getElementById('pilih-bab').addEventListener('click', function(e){{
    var b = e.target.closest('button[data-src]'); if (!b) return;
    document.querySelectorAll('#pilih-bab button').forEach(function(x){{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
    var u = b.getAttribute('data-src');
    w.className = '';
    w.innerHTML = '<div class="tombol"><a class="btn tenang" target="_blank" rel="noopener" href="' + u + '">Buka penuh di tab baru ↗</a></div>' +
                  '<iframe class="berkas" title="' + b.textContent.replace(/"/g, '') + '" src="' + u + '"></iframe>';
  }});
}})();
</script></details>"""

def kartu_taut(judul, daftar, catatan=''):
    if not daftar: return ''
    isi = ''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(j)} ↗</a></li>' for j, u in daftar)
    return f'<div class="kartu"><h2>{E(judul)}</h2>{catatan}<ul class="taut">{isi}</ul></div>'

def halaman(b):
    badan = [kepala(b), '<main class="bungkus">', kartu_data(b)]
    badan.append(kartu_berkas(b))
    badan += [kartu_gratis(b)]
    badan.append(kartu_taut('Bahan pendamping gratis berlisensi terbuka', b.get('pengganti'),
        '<p style="margin-top:0">OpenStax University Physics memakai lisensi CC BY 4.0: boleh dibaca, diunduh, dan dibagikan '
        'bebas. Cakupan dan tingkatnya setara dengan buku ini.</p>'))
    badan += [kartu_cara(b), kartu_peta(b), kartu_bab(b)]
    badan.append(kartu_taut('Halaman resmi', b.get('resmi')))
    badan.append('</main><footer class="kaki">CMS FIMS · Physics Olympiad<br>Fitrah Islamic World Academy</footer>')
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(b['judul'])} — Kumpulan E-Book</title><style>{GAYA}</style></head>
<body>
{''.join(badan)}
</body></html>
"""

def main():
    os.makedirs(DIR, exist_ok=True)
    ket = {}
    for b in BUKU:
        p = os.path.join(DIR, b['slug'] + '.html')
        open(p, 'w', encoding='utf-8').write(halaman(b))
        ket[b['slug'] + '.html'] = {
            "judul": b['judul'] + (' — ' + b['anak'] if b['anak'] else ''),
            "tahap": b['tahap'],
            "bentuk": 'E-book PDF · ' + b['bahasa'],
            "ringkas": b['penulis'] + '. ' + b['ringkas'].split('. ')[0] + '.',
            "catatan": f"{len(b['bab'])} bab",
        }
        print('ditulis', os.path.relpath(p, AKAR))
    json.dump({
        "tahap": [
            {"kode": "karya", "nama": "Karya Pembina FIWA", "urutan": 1},
            {"kode": "rujukan", "nama": "Buku Rujukan", "urutan": 2},
        ],
        "berkas": ket,
    }, open(os.path.join(DIR, 'paket.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('ditulis konten/kumpulan-ebook/paket/paket.json')

if __name__ == '__main__':
    main()
