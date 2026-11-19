#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pemeriksa kelengkapan bahan pendukung satu topik.

Aturan wajib (lihat PANDUAN-TOPIK-BARU.md bagian 5):
  Tiap TP harus punya keempat jenis bahan, dan simulasi serta bacaannya
  harus ada yang MILIK SENDIRI — bukan hanya tautan ke situs luar, sebab
  situs luar bisa menolak ditampilkan di dalam halaman.

Pakai:  python3 alat/periksa-media.py f-mek
"""
import json, os, sys

WAJIB = ("audio", "video", "simulasi", "bacaan")

def jalankan(slug):
    akar = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    berkas = os.path.join(akar, f"media-{slug}", "media.json")
    if not os.path.exists(berkas):
        print(f"✗ {berkas} tidak ada"); return 1
    m = json.load(open(berkas, encoding="utf-8"))
    salah = []
    for tp, tahapan in m.get("tp", {}).items():
        punya = {t: 0 for t in WAJIB}
        sendiri = {"simulasi": 0, "bacaan": 0}
        for daftar in tahapan.values():
            for x in daftar:
                t = x.get("tipe")
                if t in punya: punya[t] += 1
                if t in sendiri and x.get("berkas"):
                    sendiri[t] += 1
                # berkas milik sendiri harus benar-benar ada, dan jalurnya
                # dihitung dari AKAR SITUS — sebab itulah cara app.js memuatnya
                b = x.get("berkas")
                if b and not os.path.exists(os.path.join(akar, b)):
                    salah.append(f"{tp}: berkas tidak ditemukan dari akar situs — {b}")
        for t in WAJIB:
            if not punya[t]: salah.append(f"{tp}: tidak ada bahan jenis '{t}'")
        for t in sendiri:
            if not sendiri[t]:
                salah.append(f"{tp}: '{t}' hanya dari situs luar — harus ada yang milik sendiri")
        print(f"  {tp:14} " + "  ".join(f"{t} {punya[t]}" for t in WAJIB)
              + f"   (sendiri: simulasi {sendiri['simulasi']}, bacaan {sendiri['bacaan']})")
    # Halaman pembuka topik wajib ada, dengan bahan pendukungnya sendiri.
    hal = os.path.join(akar, "konten", slug, "pembuka", "index.html")
    if not os.path.exists(hal):
        salah.append(f"topik: halaman pembuka tidak ada — konten/{slug}/pembuka/index.html")
    pem = (m.get("topik", {}) or {}).get("PEMBUKA") or []
    jenis = {x.get("tipe") for x in pem}
    for t in WAJIB:
        if t not in jenis:
            salah.append(f"PEMBUKA: tidak ada bahan jenis '{t}' pada media.json -> topik.PEMBUKA")
    if not any(x.get("berkas") for x in pem if x.get("tipe") == "simulasi"):
        salah.append("PEMBUKA: simulasi harus ada yang milik sendiri (berkas, bukan url)")
    for x in pem:
        b = x.get("berkas")
        if b and not os.path.exists(os.path.join(akar, b)):
            salah.append(f"PEMBUKA: berkas tidak ditemukan dari akar situs — {b}")
    print(f"  {'PEMBUKA':14} " + "  ".join(f"{t} {sum(1 for x in pem if x.get('tipe')==t)}" for t in WAJIB)
          + f"   (halaman: {'ada' if os.path.exists(hal) else 'TIDAK ADA'})")

    for g in ("S2", "S8", "S13"):
        for tp, tahapan in m.get("tp", {}).items():
            if tahapan.get(g):
                salah.append(f"{tp}: gerbang {g} tidak boleh punya bahan pendukung")
    print()
    if salah:
        print(f"✗ {len(salah)} pelanggaran:")
        for s in salah: print("   -", s)
        return 1
    print("✓ lengkap: halaman pembuka ada dengan bahannya; tiap TP punya audio, video,"
          " simulasi, dan bacaan; simulasi dan bacaan ada yang milik sendiri; gerbang tetap bersih")
    return 0

if __name__ == "__main__":
    sys.exit(jalankan(sys.argv[1] if len(sys.argv) > 1 else "f-mek"))
