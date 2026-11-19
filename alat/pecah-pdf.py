#!/usr/bin/env python3
"""Memotong PDF besar jadi beberapa bagian di bawah batas 25 MiB Cloudflare Pages.

Pakai:
  python3 pecah-pdf.py SUMBER.pdf  KELUAR/awalan  1-282 283-634 635-1035 1036-1450

Hasil: KELUAR/awalan-1.pdf, awalan-2.pdf, ...
Tiap bagian:
  - dioptimalkan untuk web (linearized): halaman pertama tampil sebelum berkas selesai diunduh;
  - punya daftar isi (bookmark) sendiri yang hanya memuat bab dalam bagian itu, dengan nomor halaman
    yang sudah disesuaikan; panel bookmark terbuka otomatis di penampil PDF.

Butuh: qpdf, pypdf.  Rentang halaman memakai nomor halaman PDF (bukan nomor cetak buku).
"""
import os, subprocess, sys, tempfile
import pypdf


def baca_outline(r):
    hasil = []
    def jalan(o, d=0):
        for x in o:
            if isinstance(x, list):
                jalan(x, d + 1)
            else:
                try:
                    hasil.append((d, x.title.strip(), r.get_destination_page_number(x)))  # 0-based
                except Exception:
                    pass
    jalan(r.outline)
    return hasil


def main():
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    sumber, awalan, rentang = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(os.path.dirname(os.path.abspath(awalan)) or '.', exist_ok=True)
    asli = pypdf.PdfReader(sumber)
    outline = baca_outline(asli)
    print(f'{len(asli.pages)} halaman, {len(outline)} entri bookmark')

    for i, rg in enumerate(rentang, 1):
        a, b = [int(x) for x in rg.split('-')]
        akhir = f'{awalan}-{i}.pdf'
        with tempfile.TemporaryDirectory() as tmp:
            t1 = os.path.join(tmp, 'potong.pdf')
            # qpdf: kode 3 = peringatan saja (berkas sumber yang agak rusak tetap terbaca)
            subprocess.run(['qpdf', '--warning-exit-0', sumber, '--pages', sumber, f'{a}-{b}', '--', t1],
                           check=True, stderr=subprocess.DEVNULL)
            w = pypdf.PdfWriter(clone_from=t1)
            # buang bookmark lama (menunjuk halaman yang tidak ada di bagian ini), tulis ulang yang relevan
            if '/Outlines' in w._root_object:
                del w._root_object['/Outlines']
            tumpukan = []  # (kedalaman, item)
            n = 0
            for d, judul, p0 in outline:
                p = p0 + 1
                if not (a <= p <= b):
                    continue
                while tumpukan and tumpukan[-1][0] >= d:
                    tumpukan.pop()
                induk = tumpukan[-1][1] if tumpukan else None
                item = w.add_outline_item(judul, p - a, parent=induk)
                tumpukan.append((d, item))
                n += 1
            w.page_mode = '/UseOutlines'
            t2 = os.path.join(tmp, 'bookmark.pdf')
            with open(t2, 'wb') as f:
                w.write(f)
            subprocess.run(['qpdf', '--warning-exit-0', '--linearize', '--object-streams=generate', t2, akhir],
                           check=True, stderr=subprocess.DEVNULL)
        mib = os.path.getsize(akhir) / 1048576
        print(f'{akhir}: halaman {a}-{b} ({b - a + 1}), {n} bookmark, {mib:.1f} MiB' + ('  <-- LEBIH DARI 25 MiB' if mib > 25 else ''))


if __name__ == '__main__':
    main()
