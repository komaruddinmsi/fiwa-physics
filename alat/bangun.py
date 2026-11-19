# -*- coding: utf-8 -*-
import json, os, sys, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank'))
from data_tp import TOPIK, TP
from bank_s2 import S2
from bank_s11 import S11
from bank_s13 import S13

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # akar repositori
ROOT = "../../../../"          # dari konten/f-mek/<tp>/<S>/
ROOTL = "../../../"            # dari konten/f-mek/<L>/
E = lambda s: html.escape(str(s), quote=True)

import hashlib
GARAM  = "F.MEK-2026-kunci-tidak-pernah-dicetak-pada-berkas-murid"
FAKTOR = 20

def _h(x): return hashlib.sha256(x.encode("utf-8")).hexdigest()

def sandikan(kunci):
    """Mengubah kunci terbuka menjadi hash bergaram, supaya tidak terbaca dari kode sumber."""
    out = {"garam": GARAM, "faktor": FAKTOR, "num": {}, "pil": {}}
    for i, (nilai, tol) in kunci.get("num", {}).items():
        lo = int(round((nilai - tol) * FAKTOR)); hi = int(round((nilai + tol) * FAKTOR))
        out["num"][i] = [[_h(f"{GARAM}|{i}|{n}") for n in range(lo, hi + 1)], tol]
    for i, v in kunci.get("pil", {}).items():
        out["pil"][i] = _h(f"{GARAM}|{i}|{str(v).strip()}")
    return out

def halaman(judul, kode, sub, isi, root=ROOT, kunci=None, bar=False, tombol="Sudah saya kerjakan", sandi=False):
    sk = ""
    if kunci:
        if sandi: kunci = sandikan(kunci)
        sk = "<script>window.FIMS_KUNCI = %s;</script>\n" % json.dumps(kunci, ensure_ascii=False)
    bilah = ""
    if bar:
        bilah = ("""<div class="bilah-bawah"><div class="bilah-dalam">
  <div class="jalur"><div class="isi-jalur" id="isi-jalur"></div></div>
  <div class="bilah-baris"><span class="hitung" id="hitung-teks">0 dari 0 isian dijawab</span>
    <span><button type="button" class="periksa" id="btn_periksa">Periksa kelengkapan</button>
    <button type="button" class="selesai" id="btn_selesai">%s</button></span></div>
  <div class="pesan" id="pesan" role="status" aria-live="polite"></div>
</div></div>\n""" % E(tombol))
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(judul)}</title>
<link rel="stylesheet" href="{root}assets/tahapan.css">
</head>
<body>
<header class="kepala"><div class="in">
<span class="kode">{E(kode)}</span>
<h1>{E(judul)}</h1>
<p>{sub}</p>
</div></header>
<main class="bungkus">
{isi}
</main>
<footer class="kaki">CMS FIMS &middot; Fisika<br>Fitrah Islamic World Academy</footer>
{bilah}{sk}<script src="{root}assets/fims-shim.js"></script>
</body>
</html>
"""

def render_soal(daftar):
    """Satu blok .soal per butir, dengan kunci terkumpul."""
    out, num, pil = [], {}, {}
    for s in daftar:
        isi = [f'<div class="naskah">{s["naskah"]}</div>']
        if s.get("arah"):    isi.append(f'<div class="arah"><b>{s["arah"]}</b></div>')
        if s.get("catatan"): isi.append(f'<p class="catatan">{s["catatan"]}</p>')
        kotak = []
        for it in s["isian"]:
            i = it["id"]
            if it["t"] == "num":
                num[i] = [it["nilai"], it["tol"]]
                sat = f' <span class="sat">{E(it["sat"])}</span>' if it.get("sat") else ""
                bantu = f'<span class="bantu">{E(it["bantu"])}</span>' if it.get("bantu") else ""
                kotak.append(f'<div class="isian"><label for="{i}">{it["lab"]}{sat}</label>'
                             f'<input type="text" inputmode="decimal" autocomplete="off" id="{i}" name="{i}" data-isian="1">{bantu}</div>')
            elif it["t"] == "pil":
                pil[i] = it["nilai"]
                op = '<option value="">— pilih —</option>' + "".join(
                    f'<option value="{E(v)}">{t}</option>' for v, t in it["opsi"])
                kotak.append(f'<div class="isian lebar"><label for="{i}">{it["lab"]}</label>'
                             f'<select id="{i}" name="{i}" data-isian="1">{op}</select></div>')
            else:  # teks bebas, dibaca guru
                kotak.append(f'<div class="isian lebar"><label for="{i}">{it["lab"]} '
                             f'<span class="sat">dibaca guru</span></label>'
                             f'<textarea id="{i}" name="{i}" rows="{it.get("baris",3)}" data-isian="1"></textarea>'
                             f'<span class="bantu">Tidak dinilai otomatis, tetapi tetap diisi.</span></div>')
        isi.append('<div class="isian-grid">' + "".join(kotak) + "</div>")
        out.append(f'<article class="soal"><h3 class="soal-judul"><span>{E(s["judul"])}</span></h3>'
                   f'<div class="dalam-soal">{"".join(isi)}</div></article>')
    return "\n".join(out), {"num": num, "pil": pil}

def identitas():
    return ('<section class="kartu"><h2>Identitas</h2><div class="isian-grid">'
            '<div class="isian"><label for="nama">Nama lengkap</label><input type="text" id="nama" autocomplete="name"></div>'
            '<div class="isian"><label for="kelas">Kelas</label><input type="text" id="kelas"></div>'
            '<div class="isian"><label for="tanggal">Tanggal</label><input type="text" id="tanggal"></div>'
            "</div></section>")

def aturan(poin):
    li = "".join(f"<li>{p}</li>" for p in poin)
    return f'<section class="kelas"><b>Cara mengisi</b><ol>{li}</ol></section>'

ATURAN_UMUM = [
  "Bilangan boleh memakai koma atau titik; keduanya diterima.",
  "Tulis angkanya saja, tanpa satuan — satuannya sudah tercetak di sebelah kotak.",
  "Kalau jawabannya negatif, jangan lupa tanda minus. Pada besaran berarah, tanda adalah setengah dari jawaban.",
  "Tekan <b>Periksa kelengkapan</b> untuk menandai kotak yang masih kosong; tekan <b>Selesai</b> untuk mengirimkan dan melihat nomor mana yang masih salah.",
]

# ===================== tiap tahapan =====================
def tulis(path, isi):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(isi)

def bekal_li(t):
    return "".join(f"<li><b>{E(a)}</b>{E(b)}</li>" for a, b in t["bekal"])

def subbab_tabel(t):
    return "".join(
        f'<h3>{E(k)} · {E(n)}</h3><div class="miskon"><b>Miskonsepsi yang diincar:</b> '
        + " &middot; ".join(f"&ldquo;{E(m)}&rdquo;" for m in ms) + "</div>"
        for k, n, ms in t["subbab"])

def S01(t):
    isi = f"""<div class="kartu"><h2>Yang akan kamu pelajari</h2>
<p style="background:var(--abuB);border-radius:10px;padding:14px 16px;margin:0 0 6px;">&ldquo;{E(t['teks'])}&rdquo;</p>
<p style="color:var(--abu);font-size:14px;margin:0;">Kalimat di atas adalah tujuan bagian ini, apa adanya.</p></div>

<div class="kartu"><h2>Setelah ini kamu dapat&hellip;</h2>
<ul>{''.join(f'<li>{j}</li>' for j in t['tujuan'])}</ul></div>

<div class="kartu"><h2>Kapan kamu boleh bilang &ldquo;selesai&rdquo;</h2><p>{t['selesai']}</p></div>

<div class="kartu"><h2>Empat sub-bab bagian ini</h2>{subbab_tabel(t)}</div>

<div class="kartu"><h2>Bekal yang kamu bawa dari sebelumnya</h2>
<ul class="bekal">{bekal_li(t)}</ul>
<p style="margin:12px 0 0;font-size:15px;color:var(--abu);">Kalau salah satu terasa goyah, tenang — bagian berikutnya memang memeriksanya dulu.</p></div>

<div class="kartu"><h2>Lembar bekalnya</h2>
<p>Baca satu kartu, kerjakan contohnya di kertas, lalu tandai bekal mana yang masih goyah. Kira-kira lima belas menit; tidak ada nilai.</p>
<iframe class="berkas" src="{ROOT}aset-f-mek/S01-S02b_Lembar-Bekal-{E(t['kode'])}.pdf" title="Lembar Bekal {E(t['kode'])}" loading="lazy"></iframe>
<p class="catatan">Bila kotak di atas kosong, perambanmu belum bisa menampilkan PDF di dalam halaman — pakai tombol di bawah.</p>
<a class="unduh tenang" href="{ROOT}aset-f-mek/S01-S02b_Lembar-Bekal-{E(t['kode'])}.pdf" target="_blank" rel="noopener">Buka penuh di tab baru ↗</a>
<a class="unduh" href="{ROOT}aset-f-mek/S01-S02b_Lembar-Bekal-{E(t['kode'])}.pdf" download>Unduh (PDF)</a></div>

<div class="kartu"><h2>Perkiraan waktu belajar</h2><p class="waktu">{E(t['waktu'])}</p></div>
<button type="button" id="fims-kirim">Saya siap mulai</button>"""
    return halaman("Peta & Tujuan Pembelajaran", t["kode"], E(t["judul"]), isi)

def S02(t):
    soal, kunci = render_soal(S2[t["slug"]])
    isi = f"""<div class="lead">Gerbang ini memeriksa <b>bekalmu</b>, bukan materi baru. Delapan butir, tidak ada yang menjebak.
Hasilnya menentukan jalurmu: <b>80 ke atas</b> langsung lanjut, <b>60–79</b> lewat Penguatan, <b>di bawah 60</b> lewat Remediasi.</div>
{identitas()}
{aturan(ATURAN_UMUM)}
{soal}"""
    return halaman("Gerbang Prasyarat", t["kode"], E(t["judul"]), isi,
                   kunci=kunci, bar=True, tombol="Selesai", sandi=True)

def S02b(t, remedi=False):
    nama = "Remediasi Prasyarat" if remedi else "Penguatan Prasyarat"
    ajak = ("Skormu di bawah 60. Itu bukan soal bakat — ada bekal yang memang belum pernah dipasang kuat. "
            "Kerjakan ulang <b>seluruh</b> kartu bekal, pelan-pelan, bersama gurumu bila bisa."
            if remedi else
            "Skormu 60–79. Satu atau dua bekal masih goyah. Kerjakan ulang kartu yang kamu tandai goyah saja — tidak perlu semuanya.")
    lanjut = ("Sesudah ini, kerjakan ulang <b>Gerbang Prasyarat</b>. Status belajarmu baru naik setelah kamu lulus gerbang itu, bukan setelah halaman ini."
              if remedi else
              "Sesudah ini, kerjakan ulang <b>Gerbang Prasyarat</b> satu kali.")
    isi = f"""<div class="{'awas' if remedi else 'kelas'}">{ajak}</div>

<div class="kartu"><h2>Kartu bekal bagian ini</h2>
<ul class="bekal">{bekal_li(t)}</ul></div>

<div class="kartu"><h2>Lembarnya</h2>
<iframe class="berkas" src="{ROOT}aset-f-mek/S01-S02b_Lembar-Bekal-{E(t['kode'])}.pdf" title="Lembar Bekal {E(t['kode'])}" loading="lazy"></iframe>
<p class="catatan">Bila kotak di atas kosong, perambanmu belum bisa menampilkan PDF di dalam halaman — pakai tombol di bawah.</p>
<a class="unduh" href="{ROOT}aset-f-mek/S01-S02b_Lembar-Bekal-{E(t['kode'])}.pdf" download>Unduh (PDF)</a>
<a class="unduh tenang" href="{ROOT}aset-f-mek/S01-S02b_Lembar-Bekal-{E(t['kode'])}.pdf" target="_blank" rel="noopener">Buka penuh di tab baru ↗</a></div>

<div class="baik"><b>Langkah berikutnya.</b> {lanjut}</div>
<button type="button" id="fims-kirim">Sudah saya kerjakan</button>"""
    return halaman(nama, t["kode"], E(t["judul"]), isi)

def S03(t):
    kartu = "".join(
        f'<article class="soal"><h3 class="soal-judul"><span>Pemantik {i+1} · {E(nama)}</span></h3>'
        f'<div class="dalam-soal"><div class="naskah">{tantang}</div>'
        f'<div class="isian lebar"><label for="p{i+1}">Tulis tebakanmu dan alasannya, dalam dua sampai tiga kalimat</label>'
        f'<textarea id="p{i+1}" name="p{i+1}" rows="4" data-isian="1"></textarea></div></div></article>'
        for i, (nama, _ket, tantang) in enumerate(t["miskon_utama"]))
    isi = f"""<div class="lead">Tidak ada nilai di sini, dan tidak ada jawaban yang memalukan.
Yang gurumu cari justru tebakan apa adanya — supaya pembahasan di kelas berangkat dari kepala kelasmu sendiri,
bukan dari kepala penulis buku. Tulis dugaanmu sebelum membaca modul.</div>
{identitas()}
{kartu}
<button type="button" id="fims-kirim">Kirim prakonsepsi saya</button>"""
    return halaman("Pemantik & Prakonsepsi", t["kode"], E(t["judul"]), isi)

def S04(t):
    isi = f"""<div class="lead">Ini bacaan inti bagian ini. Baca sampai habis, kerjakan dua soal latihan di tiap sub-bab,
dan jawab kotak <b>&ldquo;Coba ini&rdquo;</b> sebelum pindah ke sub-bab berikutnya.</div>

<div class="kartu"><h2>Yang dibangun modul ini</h2>{subbab_tabel(t)}</div>

<div class="kartu"><h2>Lembarnya</h2>
<iframe class="berkas" src="{ROOT}aset-f-mek/S04_Modul-Konsep-{E(t['kode'])}.pdf" title="Modul Konsep {E(t['kode'])}" loading="lazy"></iframe>
<p class="catatan">Bila kotak di atas kosong, perambanmu belum bisa menampilkan PDF di dalam halaman — pakai tombol di bawah.</p>
<a class="unduh" href="{ROOT}aset-f-mek/S04_Modul-Konsep-{E(t['kode'])}.pdf" download>Unduh (PDF)</a>
<a class="unduh tenang" href="{ROOT}aset-f-mek/S04_Modul-Konsep-{E(t['kode'])}.pdf" target="_blank" rel="noopener">Buka penuh di tab baru ↗</a></div>
<button type="button" id="fims-kirim">Sudah saya pelajari</button>"""
    return halaman("Penyajian Konsep Awal", t["kode"], E(t["judul"]), isi)

GERBANG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank", "gerbang.json"), encoding="utf-8"))
PETA_G = {"f-mek-1-pra": ["G1","G2","G3"], "f-mek-2": ["G5","G6","G7"],
          "f-mek-1a": ["G9","G10","G11"], "f-mek-1b": ["G13","G14","G15"]}

def naskah_gerbang(g):
    """Naskah untuk murid saja: kutipan pertama, tanpa kunci dan tanpa aturan cabang."""
    k = GERBANG[g]["naskah"]
    t = k[0] if k else ""
    t = t.replace("Papan siap.", "").replace("Tiga puluh detik.", "").strip()
    return t

def papan_mini(t):
    """Dokumen terpisah berisi SOAL GERBANG SAJA — tanpa pembahasan, tanpa kunci."""
    blok = ""
    for n, g in enumerate(PETA_G[t["slug"]], 1):
        blok += (f'<article class="soal"><h3 class="soal-judul"><span>Butir {n} · {g}</span></h3>'
                 f'<div class="dalam-soal"><div class="naskah">{naskah_gerbang(g)}</div>'
                 f'<p class="catatan">Tulis jawabanmu di papan mini, lalu angkat ketika diminta.</p></div></article>')
    isi = f"""<div class="kelas"><b>Papan Mini — Gerbang Formatif Kelas.</b> Tiga butir, dikerjakan serentak di kelas pada papan mini.
Tiga puluh detik tiap butir. Tidak ada pembahasan di lembar ini: pembahasannya dipimpin gurumu sesudah papan diangkat.</div>
{blok}
<div class="kartu"><h2>Catatan</h2><p>Lembar ini sengaja hanya berisi soal. Kunci jawaban dan aturan cabangnya ada pada
RPP guru, dan tidak pernah dicetak di lembar murid mana pun.</p></div>"""
    return halaman("Papan Mini · Gerbang Formatif", t["kode"], E(t["judul"]), isi, root="../")

def S05(t):
    kartu = "".join(
        f'<div class="kartu"><h3>{i+1}. {E(nama)}</h3><p class="miskon"><b>Yang sering terjadi:</b> {E(ket)}</p>'
        f'<p><b>Penantangnya di kelas:</b> {tantang}</p></div>'
        for i, (nama, ket, tantang) in enumerate(t["miskon_utama"]))
    isi = f"""<div class="kelas"><b>Tahapan ini dipimpin gurumu di kelas.</b> Halaman ini bukan lembar kerja —
ia catatan supaya kamu tahu apa yang akan dibahas, dan bisa membukanya lagi sesudah kelas.</div>

<div class="lead">Prakonsepsi yang kamu dan teman-temanmu kirim pada tahapan sebelumnya dibuka di sini.
Yang dibahas bukan siapa yang benar, melainkan <b>mengapa</b> dugaan tertentu terasa benar padahal tidak.</div>

{kartu}

<div class="baik"><b>Yang kamu bawa pulang dari tahapan ini:</b> satu kalimat untuk tiap miskonsepsi di atas —
mengapa ia terasa benar, dan apa yang membantahnya. Tulis di bukumu.</div>
<button type="button" id="fims-kirim">Saya sudah mengikuti pembahasannya</button>"""
    return halaman("Pembahasan Prakonsepsi", t["kode"], E(t["judul"]), isi)

def S06(t):
    langkah = "".join(f'<li><b>{E(k)} · {E(n)}</b><br><span style="color:var(--abu)">Pola empat langkah: '
                      '① Jelaskan &middot; ② Kerjakan &middot; ③ Jelaskan ulang berpasangan &middot; ④ Periksa ekspektasi</span></li>'
                      for k, n, _ in t["subbab"])
    isi = f"""<div class="kelas"><b>Tahapan ini dipimpin gurumu di kelas.</b> Tiga tahap, masing-masing ditutup satu gerbang serentak.</div>

<div class="kartu"><h2>Urutan yang dikerjakan di kelas</h2><ol>{langkah}</ol></div>

<div class="lead">Satu hal yang diminta sepanjang tahapan ini: <b>putuskan dulu, baru hitung.</b>
Sebelum memilih rumus, tulis keputusanmu — sudutnya diukur dari mana, siapa pemberi gaya itu, di mana porosnya.
Keputusan itulah yang dinilai, bukan angka yang kebetulan cocok.</div>

<div class="kartu"><h2>Modulnya, bila kamu perlu membuka lagi</h2>
<iframe class="berkas" src="{ROOT}aset-f-mek/S04_Modul-Konsep-{E(t['kode'])}.pdf" title="Modul Konsep {E(t['kode'])}" loading="lazy"></iframe>
<p class="catatan">Bila kotak di atas kosong, perambanmu belum bisa menampilkan PDF di dalam halaman — pakai tombol di bawah.</p>
<a class="unduh tenang" href="{ROOT}aset-f-mek/S04_Modul-Konsep-{E(t['kode'])}.pdf" target="_blank" rel="noopener">Buka penuh di tab baru ↗</a>
<a class="unduh" href="{ROOT}aset-f-mek/S04_Modul-Konsep-{E(t['kode'])}.pdf" download>Unduh (PDF)</a></div>
<button type="button" id="fims-kirim">Saya sudah mengikuti</button>"""
    return halaman("Inti Terbimbing", t["kode"], E(t["judul"]), isi)

def S08(t):
    isi = f"""<div class="kelas"><b>Gerbang ini dikerjakan serentak di kelas, bukan di rumah.</b>
Tiga butir di papan mini, tiga puluh detik tiap butir. Skormu diisi gurumu sesudah papan diangkat.</div>

<div class="kartu"><h2>Lembar soalnya</h2>
<p>Lembar ini hanya berisi soal gerbang — tanpa pembahasan dan tanpa kunci, supaya gerbangnya tetap berfungsi sebagai gerbang.</p>
<iframe class="berkas" src="{ROOT}aset-f-mek/S08_Papan-Mini-{E(t['kode'])}.html" title="Papan Mini {E(t['kode'])}" loading="lazy"></iframe>
<a class="unduh tenang" href="{ROOT}aset-f-mek/S08_Papan-Mini-{E(t['kode'])}.html" target="_blank" rel="noopener">Buka penuh di tab baru ↗</a></div>

<div class="kartu"><h2>Sesudah papan diangkat</h2>
<p>Kelas terbagi dua: yang tertangkap pergi ke meja tuntun bersama guru, yang lolos melanjutkan ke varian mandiri.
Keduanya bukan hukuman dan bukan hadiah — hanya jalur yang berbeda menuju tahapan berikutnya.</p></div>

<div class="baik"><b>Catatan untuk murid.</b> Kamu tidak bisa mengisi skormu sendiri di sini. Tekan tombol di bawah
untuk menandai bahwa kamu mengikuti gerbangnya; nilainya menyusul dari gurumu.</div>
<button type="button" id="fims-kirim">Saya mengikuti gerbang ini</button>"""
    return halaman("Gerbang Formatif Kelas", t["kode"], E(t["judul"]), isi)

TIER = [("T1","Belum tertangkap polanya",
         "Kerjakan ulang satu contoh terkerjakan dari modul bersama guru di meja tuntun, lalu satu varian yang angkanya diganti. Satu soal dulu, sampai langkahnya mengalir."),
        ("T2","Langkahnya benar, hasilnya belum stabil",
         "Kerjakan tiga varian berturut-turut tanpa membuka contoh. Tulis keputusanmu dulu di tiap soal — sudut diukur dari mana, siapa pemberi gaya, di mana porosnya."),
        ("T3","Mandiri pada soal baru",
         "Kerjakan dua soal yang konteksnya belum pernah dibahas. Tidak boleh membuka lembar contoh. Ini tingkat yang dituju bagian ini."),
        ("T4","Siap ditantang",
         "Ambil kartu tantangan di kotak depan: satu sistem yang belum pernah dibahas di kelas. Selesaikan, lalu jelaskan ulang kepada satu teman yang masih di T2.")]

def S09(t):
    kartu = "".join(f'<div class="kartu"><h3>{k} · {E(n)}</h3><p>{E(d)}</p></div>' for k, n, d in TIER)
    isi = f"""<div class="lead">Jalurmu di sini ditentukan hasil gerbang kelas tadi, bukan oleh siapa kamu.
Tingkat ini berubah tiap tahapan — murid yang hari ini di T1 bisa berada di T3 pekan depan.</div>
{kartu}
<div class="baik"><b>Yang dituju bagian ini adalah T3:</b> mandiri pada soal yang konteksnya baru.
T4 adalah pengayaan, bukan syarat tuntas.</div>
<button type="button" id="fims-kirim">Saya sudah mengerjakan jalur saya</button>"""
    return halaman("Diferensiasi T1–T4", t["kode"], E(t["judul"]), isi)

def S10(t):
    isi = f"""<div class="lead">Satu tahapan tidak selesai pada saat kamu bisa menghitung. Ia selesai ketika kamu bisa
<b>menceritakan ulang</b> apa yang kamu kerjakan, dengan kata-katamu sendiri, kepada orang yang belum tahu.</div>
{identitas()}
<article class="soal"><h3 class="soal-judul"><span>Jangkar 1 · Satu kalimat inti</span></h3><div class="dalam-soal">
<div class="naskah">Tulis satu kalimat yang merangkum seluruh bagian ini. Kalimat itu harus bisa dipahami teman yang belum belajar bagian ini.</div>
<div class="isian lebar"><label for="j1">Satu kalimat intinya</label><textarea id="j1" name="j1" rows="3" data-isian="1"></textarea></div></div></article>

<article class="soal"><h3 class="soal-judul"><span>Jangkar 2 · Jebakan yang hampir menipumu</span></h3><div class="dalam-soal">
<div class="naskah">Dari empat miskonsepsi yang dibahas, pilih satu yang paling hampir kamu percayai. Tulis mengapa ia terasa benar, lalu apa yang membantahnya.</div>
<div class="isian lebar"><label for="j2">Miskonsepsi yang kamu pilih, dan bantahannya</label><textarea id="j2" name="j2" rows="4" data-isian="1"></textarea></div></div></article>

<article class="soal"><h3 class="soal-judul"><span>Jangkar 3 · Contohmu sendiri</span></h3><div class="dalam-soal">
<div class="naskah">Tulis satu contoh dari hidupmu sendiri — rumah, jalan, dapur, lapangan — yang bisa dijelaskan dengan isi bagian ini. Contoh dari buku tidak dihitung.</div>
<div class="isian lebar"><label for="j3">Contohmu, dan penjelasannya</label><textarea id="j3" name="j3" rows="4" data-isian="1"></textarea></div></div></article>

<div class="baik">Jangkar ini dibaca gurumu dan tersimpan di akunmu. Ia tidak diberi angka — tetapi inilah yang paling sering
dipakai gurumu untuk memutuskan apakah kamu benar-benar sudah tuntas.</div>
<button type="button" id="fims-kirim">Kirim jangkar saya</button>"""
    return halaman("Konsolidasi & Jangkar", t["kode"], E(t["judul"]), isi)

# ---------- S7: worksheet lampiran, mesinnya diganti mesin bersama ----------
import re
LAMPIRAN = os.path.join(AKAR, "alat", "sumber")   # taruh worksheet asli di sini
WS = {"f-mek-1-pra": "c06af0d4-Worksheet-Fisika-F.MEK.1-pra-Dua-Soal-Latihan.html",
      "f-mek-2":     "482df6d0-Worksheet-Fisika-F.MEK.2-Dua-Soal-Latihan.html",
      "f-mek-1a":    "19a77db1-Worksheet-Fisika-F.MEK.1a-Dua-Soal-Latihan.html",
      "f-mek-1b":    "db4199ff-Worksheet-Fisika-F.MEK.1b-Dua-Soal-Latihan.html"}

CSS_TAMBAHAN = """
.lipat-tombol{position:absolute;top:-16px;right:16px;z-index:2;background:#fff;color:#0B4F58;
 border:1px solid #D7E6E8;border-bottom:none;border-radius:9px 9px 0 0;padding:4px 13px;cursor:pointer;
 font:600 12px 'Segoe UI',Arial,sans-serif;box-shadow:0 -3px 10px rgba(0,0,0,.07)}
.lipat-tombol:hover{background:#E3F5F6}
body.bilah-lipat .bilah-bawah #fims-salah,body.bilah-lipat .bilah-bawah .pesan{display:none}
body.bilah-lipat.ada-kirim .bilah-bawah .hitung,
body.bilah-lipat.ada-kirim .bilah-bawah button:not(.fims-aksi){display:none}
body.bilah-lipat.ada-kirim .bilah-bawah .bilah-baris{justify-content:flex-end}
body.bilah-lipat .bilah-bawah{padding-top:8px;padding-bottom:10px}
body.bilah-lipat .bilah-bawah .jalur{height:7px}
body.bilah-lipat .bilah-bawah button.fims-aksi{padding:6px 17px;font-size:12.5px}
button.selesai{font:inherit;font-weight:700;background:#0B4F58;color:#fff;border:0;border-radius:9px;padding:8px 16px;cursor:pointer}
button.selesai:hover{background:#073B44}
#fims-salah{background:#FDEBDD;border:1px solid #E27A2E;border-left:6px solid #C05621;border-radius:10px;
 padding:11px 14px;margin:12px 0 0;max-height:30vh;overflow:auto;font-size:14.6px}
#fims-salah b{color:#C05621}
#fims-salah .nomor{display:inline-block;background:#fff;border:1px solid #E27A2E;color:#C05621;border-radius:999px;
 padding:3px 12px;margin:5px 6px 0 0;font-weight:700;font-size:13.4px;cursor:pointer}
#fims-salah .nomor:hover{background:#C05621;color:#fff}
.disorot,.kartu-soal.disorot{outline:3px solid #E27A2E;outline-offset:3px;border-radius:12px}
#fims-kabar{margin:12px 0 0;padding:10px 14px;border-radius:10px;background:#E6F4EC;color:#1F7A4D;
 border:1px solid #1F7A4D;font:600 15px 'Segoe UI',Arial,sans-serif}
@media print{.lipat-tombol{display:none!important}}
"""

def S07(t):
    src = open(os.path.join(LAMPIRAN, WS[t["slug"]]), encoding="utf-8").read()
    m_num = re.search(r'var KUNCI_NUM = (\{.*?\});', src, re.S)
    m_pil = re.search(r'var KUNCI_PIL = (\{.*?\});', src, re.S)
    kunci = {"num": json.loads(m_num.group(1)), "pil": json.loads(m_pil.group(1))}
    # buang mesin lama seluruhnya
    src = re.sub(r'<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', '', src, flags=re.S)
    # tombol Selesai di samping Periksa kelengkapan
    src = src.replace('<button type="button" class="periksa" id="tombol-periksa">Periksa kelengkapan</button>',
        '<button type="button" class="periksa" id="btn_periksa">Periksa kelengkapan</button>'
        ' <button type="button" class="selesai" id="btn_selesai">Selesai</button>')
    src = src.replace('</style>', CSS_TAMBAHAN + '</style>', 1)
    pasang = ('<script>window.FIMS_KUNCI = %s;</script>\n<script src="%sassets/fims-shim.js"></script>\n</body>'
              % (json.dumps(kunci, ensure_ascii=False), ROOT))
    src = src.replace('</body>', pasang, 1)
    return src, kunci

def S11h(t):
    soal, kunci = render_soal(S11[t["slug"]])
    isi = f"""<div class="lead">Latihan ini dikerjakan <b>di rumah</b>, H+0 sampai H+2 setelah kelas.
Ambangnya {t['ambang']}. Boleh diulang; yang dicatat skor terbaikmu.</div>
{identitas()}
{aturan(ATURAN_UMUM)}
{soal}"""
    return halaman("Latihan Bertingkat", t["kode"], E(t["judul"]), isi,
                   kunci=kunci, bar=True, tombol="Selesai")

def S12h(t):
    isi = f"""<div class="lead">Tugas kinerja dinilai gurumu dengan rubrik, bukan dinilai otomatis.
Yang dinilai adalah <b>caramu memutuskan</b>, bukan angka akhirnya. Dikerjakan H+1 sampai H+5.</div>

<div class="kartu"><h2>Yang kamu kerjakan</h2>
<p>Pilih satu benda atau struktur nyata di sekitarmu — di rumah, sekolah, pasar, atau jalan — yang belum pernah dibahas di kelas.
Analisis dengan seluruh isi bagian ini, lalu tulis laporan satu halaman.</p>
<ol><li>Foto atau sketsa bendanya, dengan ukuran kasarnya.</li>
<li>Gambar diagram gayanya. Tiap panah wajib menyebut pemberinya.</li>
<li>Tulis keputusanmu sebelum menghitung: arah positif, sudut diukur dari mana, di mana porosnya.</li>
<li>Hitung, lalu periksa hasilmu dengan cara kedua.</li>
<li>Tutup dengan satu paragraf: apa yang akan berubah bila satu ukurannya diubah.</li></ol></div>

<div class="kartu"><h2>Tingkat yang dinilai gurumu</h2>
<ul class="bekal">
<li><b>T1</b>Menyalin contoh kelas dengan benda diganti namanya</li>
<li><b>T2</b>Benda baru, tetapi langkahnya masih mengikuti contoh baris demi baris</li>
<li><b>T3</b>Benda baru, keputusan diambil sendiri dan ditulis sebelum menghitung — <b>ini ambang tuntas</b></li>
<li><b>T4</b>Benda baru, ditambah pemeriksaan kedua dan telaah pengaruh perubahan ukuran</li></ul></div>

<div class="kelas"><b>Minimal T3 untuk tuntas.</b> Bagian ini dan Gerbang Ketuntasan harus lulus dua-duanya —
lulus gerbang saja dengan tugas kinerja di T2 belum membuatmu Tuntas.</div>
<button type="button" id="fims-kirim">Tugas saya sudah dikumpulkan</button>"""
    return halaman("Tugas Kinerja", t["kode"], E(t["judul"]), isi)

def S13h(t):
    soal, kunci = render_soal(S13[t["slug"]])
    isi = f"""<div class="awas"><b>Sekali jalan.</b> Butir di gerbang ini belum pernah kamu lihat di tahapan mana pun,
dan kuncinya tidak ditampilkan. Dikerjakan H+2 sampai H+7, tanpa membuka modul. Ambang {t['ambang']}.</div>
{identitas()}
{aturan(ATURAN_UMUM[:3] + ["Kerjakan sendiri, sekali jalan. Tekan <b>Selesai</b> hanya ketika kamu benar-benar sudah selesai."])}
{soal}"""
    return halaman("Gerbang Ketuntasan TP", t["kode"], E(t["judul"]), isi,
                   kunci=kunci, bar=True, tombol="Selesai", sandi=True)

def S14h(t):
    isi = f"""<div class="lead">Tuntas sekali bukan tuntas selamanya. Bagian ini muncul lagi pada <b>H+14, H+30, dan H+60</b>
untuk memeriksa apakah yang kamu kuasai masih bertahan. Tidak ada yang perlu dipelajari ulang sebelumnya — justru itu gunanya.</div>

<div class="kartu"><h2>Cara kerjanya</h2>
<ol><li>Pada hari yang dijadwalkan, bagian ini terbuka sendiri dengan beberapa butir dari bank yang sama.</li>
<li>Kerjakan tanpa membuka modul. Lima sampai sepuluh menit.</li>
<li>Lulus: statusmu menjadi <b>Tuntas stabil</b>. Gagal: statusmu turun satu tingkat dan tahapan latihan terbuka lagi.</li></ol></div>

<div class="kartu"><h2>Mengapa diulang berjarak</h2>
<p>Yang baru dipelajari akan memudar bila tidak pernah dipanggil kembali. Memanggilnya kembali justru ketika
sudah mulai memudar — bukan ketika masih segar — adalah yang membuatnya bertahan lama. Karena itu jaraknya
makin jauh: dua pekan, sebulan, dua bulan.</p></div>

<div class="baik"><b>Turun tingkat bukan hukuman.</b> Ia hanya kabar bahwa bagian ini perlu dipanggil sekali lagi.</div>
<button type="button" id="fims-kirim">Saya sudah mengerjakan pengulangan hari ini</button>"""
    return halaman("Pengulangan Berjarak", t["kode"], E(t["judul"]), isi)

# ---------- lapis topik ----------
from bank_s2 import N as _N, P as _P
L1_SOAL = [
 {"judul":"Soal 1 · Vektor","naskah":"Seorang petugas berjalan 12 m ke timur, lalu 16 m ke utara.",
  "isian":[_N("l1","Jarak lurusnya dari titik awal","(m)",20,0.2)]},
 {"judul":"Soal 2 · Menguraikan gaya","naskah":"Gaya 250 N membentuk sudut θ terhadap sumbu mendatar, dengan cos θ = 0,80 dan sin θ = 0,60.",
  "isian":[_N("l2","Komponen mendatarnya","(N)",200,0.5),_N("l3","Komponen tegaknya","(N)",150,0.5)]},
 {"judul":"Soal 3 · Bidang miring","naskah":"Sebuah drum berat 300 N berada pada bidang miring dengan sin θ = 0,60 dan cos θ = 0,80.",
  "isian":[_N("l4","Komponen berat yang sejajar bidang","(N)",180,0.5)]},
 {"judul":"Soal 4 · Gaya neto","naskah":"Sebuah peti ditarik 70 N ke kanan dan digesek lantai 22 N ke kiri.",
  "arah":"Arah positif untuk soal ini sudah ditetapkan: ke kanan.",
  "isian":[_N("l5","Gaya neto peti","(N)",48,0.2)]},
 {"judul":"Soal 5 · Percepatan","naskah":"Peti pada soal sebelumnya bermassa 16 kg.",
  "isian":[_N("l6","Percepatan peti","(m/s²)",3,0.05)]},
 {"judul":"Soal 6 · Berat","naskah":"Sebuah tabung bermassa 11 kg. Gunakan g = 10 m/s².",
  "isian":[_N("l7","Beratnya","(N)",110,0.5)]},
 {"judul":"Soal 7 · Kecepatan tetap","naskah":"Sebuah lemari didorong 29 N dan bergerak lurus dengan kecepatan tetap.",
  "isian":[_N("l8","Besar gesekan lantai","(N)",29,0.2)]},
 {"judul":"Soal 8 · Gaya yang punya pemberi","naskah":"Sebuah batu lepas dari ketapel dan melayang mendatar. Hambatan udara diabaikan.",
  "isian":[_P("l9","Panah gaya pada batu itu:",[("berat","satu panah ke bawah, yaitu beratnya"),
    ("dua","satu panah ke bawah dan satu ke depan"),("nol","tidak ada panah")],"berat")]},
 {"judul":"Soal 9 · Aksi dan reaksi","naskah":"Sebuah buku diam di atas meja.",
  "isian":[_P("l10","Pasangan dari gaya normal meja pada buku:",[("berat","berat buku, bekerja pada buku"),
    ("meja","tekanan buku pada meja, bekerja pada meja"),("bumi","tarikan buku pada Bumi")],"meja")]},
 {"judul":"Soal 10 · Memeriksa sendiri","naskah":"Sebuah gaya diuraikan menjadi komponen 15 N dan 20 N yang saling tegak lurus.",
  "isian":[_N("l11","Besar gaya semula","(N)",25,0.2)]},
]

def L1h():
    soal, kunci = render_soal(L1_SOAL)
    isi = f"""<div class="lead">Kuis blok ini mencakup <b>dua TP pertama</b> topik ini: operasi vektor, dan gaya &amp; gerak
pada peristiwa sehari-hari. Sepuluh soal, boleh diulang.</div>
{identitas()}
{aturan(ATURAN_UMUM)}
{soal}"""
    return halaman("Kuis Blok", "F.MEK", "Mekanika: Gaya &amp; Gerak", isi,
                   root=ROOTL, kunci=kunci, bar=True, tombol="Selesai")

def L2h():
    isi = f"""<div class="lead">Muara topik bukan ujian. Ia tempat kamu menyambungkan keempat bagian menjadi satu cerita
yang utuh — dan itulah yang membedakan orang yang hafal rumus dari orang yang paham.</div>
{identitas()}
<article class="soal"><h3 class="soal-judul"><span>Muara 1 · Satu benang merah</span></h3><div class="dalam-soal">
<div class="naskah">Keempat bagian topik ini — vektor, gaya sehari-hari, hukum Newton, dan struktur — sebenarnya satu rangkaian.
Tulis satu paragraf yang menyambungkan keempatnya: mengapa vektor harus datang lebih dulu, dan mengapa struktur datang terakhir.</div>
<div class="isian lebar"><label for="m1">Benang merahnya</label><textarea id="m1" rows="5" data-isian="1"></textarea></div></div></article>

<article class="soal"><h3 class="soal-judul"><span>Muara 2 · Satu benda, empat bagian</span></h3><div class="dalam-soal">
<div class="naskah">Pilih satu benda di sekitarmu. Jelaskan benda itu memakai <b>keempat</b> bagian topik ini sekaligus:
uraikan gayanya ke komponen, sebut pemberi tiap gaya, terapkan hukum Newton, lalu bahas kesetimbangan atau momennya.</div>
<div class="isian lebar"><label for="m2">Bendamu dan analisisnya</label><textarea id="m2" rows="7" data-isian="1"></textarea></div></div></article>

<article class="soal"><h3 class="soal-judul"><span>Muara 3 · Miskonsepsi yang paling keras kepala</span></h3><div class="dalam-soal">
<div class="naskah">Dari seluruh topik ini, miskonsepsi mana yang paling sulit kamu lepaskan? Tulis jujur, lalu jelaskan
apa yang akhirnya meyakinkanmu — atau apa yang masih membuatmu ragu sampai sekarang.</div>
<div class="isian lebar"><label for="m3">Jawabanmu</label><textarea id="m3" rows="5" data-isian="1"></textarea></div></div></article>

<div class="baik">Tidak ada angka di sini. Gurumu membacanya, dan jawabanmu ikut menentukan tingkat tugas kinerjamu.</div>
<button type="button" id="fims-kirim">Kirim muara topik saya</button>"""
    return halaman("Muara Topik", "F.MEK", "Mekanika: Gaya &amp; Gerak", isi, root=ROOTL)

def L4h():
    isi = f"""<div class="lead">Tantangan ini melintasi topik: ia memakai Mekanika bersama topik lain yang sudah kamu tuntaskan.
Berkala, tidak dijadwalkan ketat, dan <b>tidak memengaruhi status tuntasmu</b>.</div>

<div class="kartu"><h2>Tantangan 1 · Satu struktur, dua topik</h2>
<p>Pilih satu struktur nyata — jembatan kecil, derek mainan, rak dinding, ayunan. Analisis gayanya dengan Mekanika,
lalu hitung usaha dan energinya dengan topik Usaha &amp; Energi. Tulis apa yang hanya terlihat ketika kedua topik dipakai bersama.</p></div>

<div class="kartu"><h2>Tantangan 2 · Membantah dengan hitungan</h2>
<p>Cari satu klaim di internet atau iklan yang melanggar fisika — alat yang mengaku menghemat energi,
struktur yang mengaku tidak bisa roboh. Bantah dengan hitungan, bukan dengan pendapat.</p></div>

<div class="kartu"><h2>Tantangan 3 · Bank soal TKA</h2>
<p>Bank latihan TKA topik ini terbuka kapan saja, 25 butir bergaya TKA lengkap dengan pembahasan tujuh langkah.</p>
<iframe class="berkas" src="../L3/latihan.html" title="Latihan TKA F.MEK" loading="lazy"></iframe>
<a class="unduh tenang" href="../L3/latihan.html" target="_blank" rel="noopener">Buka penuh di tab baru ↗</a></div>

<div class="baik">Kerjakan yang kamu mau, kapan kamu mau. Bagian ini memang dibuat untuk dikerjakan karena penasaran,
bukan karena dinilai.</div>
<button type="button" id="fims-kirim">Saya sudah mengerjakan satu tantangan</button>"""
    return halaman("Tantangan Mata Pelajaran", "F.MEK", "Mekanika: Gaya &amp; Gerak", isi, root=ROOTL)

# ---------- penulis ----------
def jalankan():
    base = os.path.join(AKAR, "konten", "f-mek")
    tulis(os.path.join(base, "topik.json"), json.dumps(TOPIK, ensure_ascii=False, indent=2))
    n = 0
    for t in TP:
        d = os.path.join(base, t["slug"])
        tulis(os.path.join(d, "tp.json"), json.dumps({
            "kode": t["kode"], "judul": t["judul"], "teks": t["teks"], "bloom": t["bloom"],
            "urutan_ajar": t["urutan"], "prasyarat": t["prasyarat"], "ambang": t["ambang"],
        }, ensure_ascii=False, indent=2))
        hal = {"S1": S01(t), "S2": S02(t), "S2b": S02b(t, False), "S2c": S02b(t, True),
               "S3": S03(t), "S4": S04(t), "S5": S05(t), "S6": S06(t),
               "S8": S08(t), "S9": S09(t), "S10": S10(t),
               "S11": S11h(t), "S12": S12h(t), "S13": S13h(t), "S14": S14h(t)}
        hal["S7"] = S07(t)[0]
        for sid, isi in hal.items():
            tulis(os.path.join(d, sid, "index.html"), isi); n += 1
        tulis(os.path.join(AKAR, "aset-f-mek", f"S08_Papan-Mini-{t['kode']}.html"), papan_mini(t))
    tulis(os.path.join(base, "L1", "index.html"), L1h()); n += 1
    tulis(os.path.join(base, "L2", "index.html"), L2h()); n += 1
    tulis(os.path.join(base, "L4", "index.html"), L4h()); n += 1
    print(f"{n} halaman tahapan + 4 papan mini ditulis")

if __name__ == "__main__":
    jalankan()
