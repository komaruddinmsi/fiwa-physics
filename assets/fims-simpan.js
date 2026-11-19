/* ============================================================
   FIMS-SIMPAN — menyimpan isian dan skor SATU dokumen untuk SATU akun murid.

   Dipasang pada dokumen apa pun yang bisa diisi murid (lembar kerja, soal, simulasi PRI UIN, lapis L1–L4,
   dokumen baru). Dokumen tidak perlu ditulis ulang: berkas ini membaca semua kotak isian (<input>, <select>,
   <textarea>) lalu menyimpannya ke akun murid lewat /api/lembar. Saat dokumen dibuka lagi, di perangkat mana
   pun, isian dipulihkan. Bila guru membuka ulang dokumen itu, isian murid dihapus dan ia bisa mengerjakan
   dari awal.

   Cara memasang pada dokumen:
     <script src="../../../assets/fims-simpan.js"></script>       (di akhir <body>; sesuaikan jalurnya)
   Dokumen yang memuat fims-shim.js sudah otomatis. Dokumen yang tampil di dalam situs (bingkai) dipasangi
   otomatis oleh halaman induk, jadi dokumen baru pun tetap tersimpan walau lupa menambahkan tag di atas.

   Syarat satu-satunya: tiap kotak isian punya id atau name yang tetap. Kotak tanpa keduanya tetap disimpan
   berdasarkan urutannya, tetapi itu rapuh bila dokumen berubah.

   Kait opsional (semuanya boleh tidak ada), didefinisikan dokumen pada window:
     FIMS_RINGKAS()      -> { terisi, total, selesai, skor }   ringkasan untuk daftar guru
     FIMS_KEADAAN()      -> objek JSON                          keadaan di luar kotak isian (misalnya "terkunci")
     FIMS_PULIHKAN(info) -> dipanggil sesudah isian dipulihkan; info = { selesai, skor, x }. Di sinilah dokumen
                            yang punya pengatur waktu atau kunci menjalankan ulang kode pemulihannya.
   Dan dokumen boleh memanggil  FIMS_LEMBAR.lapor({ selesai: true, skor: 80 })  untuk menyimpan seketika.

   Penting: isian tidak pernah dikirim sebelum isian lama selesai dimuat, supaya lembar kosong tidak menimpa
   jawaban yang sudah tersimpan. Guru dan pemilik hanya melihat-lihat: tidak ada yang disimpan atas nama mereka.
   ============================================================ */
(function () {
  "use strict";
  if (window.FIMS_LEMBAR) return;

  var API = "/api/lembar";
  var JEDA_CEK = 3000;          // seberapa sering mencari perubahan untuk disimpan
  var JEDA_POLL = 45000;        // seberapa sering menanyakan apakah guru membuka ulang dokumen ini
  var TUNGGU_MUAT = 4000;       // paling lama menahan layar saat memuat isian lama

  /* ---------- bahasa ---------- */
  var BHS = "id";
  try { BHS = window.parent.FIMS.bahasa() === "en" ? "en" : "id"; }
  catch (e1) {
    try { var dd = JSON.parse(localStorage.getItem("va-fims-v1")) || {}; if (dd.opsi && dd.opsi.bahasa === "en") BHS = "en"; } catch (e2) {}
  }
  var TXT = {
    id: {
      memuat: "Memuat jawabanmu…", simpan: "Menyimpan…", ok: "Jawabanmu tersimpan di akunmu",
      gagal: "Belum tersimpan — mencoba lagi", offline: "Tidak terhubung ke penyimpanan akun. Jawaban baru tersimpan di halaman ini.",
      masuk: "Masuk dulu agar jawabanmu tersimpan di akun.", guru: "Mode guru: jawaban tidak disimpan.",
      usang: "Gurumu membuka ulang dokumen ini. Memuat ulang…", besar: "Isian terlalu besar untuk disimpan.",
      penuh: "Terlalu banyak dokumen tersimpan di akun ini.", lambat: "Jawaban tersimpan ditemukan, tetapi kamu sudah mengisi sebelum selesai dimuat. Muat ulang halaman untuk memulihkannya.",
      muatUlang: "Muat ulang", tutup: "Tutup", gagalPulih: "Jawaban tersimpan gagal dipulihkan, dan tidak ada yang disimpan dulu.",
      buka: "%s membuka ulang dokumen ini pada %s%s. Kerjakan lagi dari awal.", guruSaja: "Gurumu"
    },
    en: {
      memuat: "Loading your answers…", simpan: "Saving…", ok: "Your answers are saved to your account",
      gagal: "Not saved yet — retrying", offline: "Cannot reach account storage. Answers are only kept on this page for now.",
      masuk: "Sign in first so your answers are saved to your account.", guru: "Teacher mode: answers are not saved.",
      usang: "Your teacher reopened this document. Reloading…", besar: "Your answers are too large to save.",
      penuh: "Too many documents saved on this account.", lambat: "Saved answers were found, but you started typing before they finished loading. Reload the page to restore them.",
      muatUlang: "Reload", tutup: "Close", gagalPulih: "Saved answers could not be restored, so nothing is being saved for now.",
      buka: "%s reopened this document on %s%s. Start again from the beginning.", guruSaja: "Your teacher"
    }
  };
  function t(k) { return TXT[BHS][k] || TXT.id[k] || k; }

  /* ---------- kunci dokumen ----------
     Alamat berkas tanpa "/" depan, tanpa ".html", tanpa "index". Harus sama dengan fungsi
     FIMS.kunciLembar di assets/akun.js (dipakai panel guru untuk menunjuk dokumen yang sama). */
  function bentukKunci(jalur) {
    var p = String(jalur || "").replace(/[?#].*$/, "").replace(/^\/+/, "");
    try { p = decodeURIComponent(p); } catch (e) {}
    p = p.replace(/\/index\.html?$/i, "").replace(/\.html?$/i, "").replace(/\/+$/, "");
    p = p.replace(/[^A-Za-z0-9._\-\/]/g, "_").replace(/\/{2,}/g, "/").replace(/\.\.+/g, ".");
    return p.slice(0, 200);
  }
  var KUNCI = bentukKunci(location.pathname);
  if (!KUNCI || !/^[A-Za-z0-9]/.test(KUNCI)) return;

  /* ---------- membaca dan menulis isian ---------- */
  var ABAI = { button: 1, submit: 1, reset: 1, image: 1, file: 1, password: 1 };

  /* Memetakan semua kotak isian menjadi kelompok per kunci: { kunci: { bentuk, els } }.
     bentuk: str (teks, angka, pilihan, tersembunyi) | multi (select multiple) | bool (kotak centang tunggal)
             | radio (kelompok radio) | cek (kelompok kotak centang dengan name yang sama) */
  function petakan() {
    var daftar = document.querySelectorAll("input, select, textarea"), peta = {}, urut = [], hitung = {}, tanpa = {}, i;
    for (i = 0; i < daftar.length; i++) {
      var el = daftar[i];
      if (el.closest && el.closest("[data-fims-abaikan], #fims-simpan-bar")) continue;
      var tag = el.tagName.toLowerCase();
      var tipe = tag === "input" ? String(el.getAttribute("type") || "text").toLowerCase() : tag;
      if (ABAI[tipe]) continue;
      var kunci, bentuk;
      if (tipe === "radio" && el.name) { kunci = "@" + el.name; bentuk = "radio"; }
      else if (tipe === "checkbox" && !el.id && el.name) { kunci = "@" + el.name; bentuk = "cek"; }
      else {
        bentuk = (tipe === "checkbox" || tipe === "radio") ? "bool" : (tipe === "select" && el.multiple ? "multi" : "str");
        if (el.id) kunci = "#" + el.id;
        else if (el.name) kunci = "@" + el.name;
        else { tanpa[tipe] = (tanpa[tipe] || 0) + 1; kunci = "~" + tipe + tanpa[tipe]; }
        if (bentuk !== "radio" && bentuk !== "cek") {
          hitung[kunci] = (hitung[kunci] || 0) + 1;
          if (hitung[kunci] > 1) kunci += ":" + hitung[kunci];
        }
      }
      var g = peta[kunci];
      if (!g) { g = peta[kunci] = { bentuk: bentuk, els: [], tipe: tipe }; urut.push(kunci); }
      g.els.push(el);
    }
    return { peta: peta, urut: urut };
  }

  function nilaiGrup(g) {
    var i, o = [];
    switch (g.bentuk) {
      case "bool":  return !!g.els[0].checked;
      case "multi":
        for (i = 0; i < g.els[0].options.length; i++) if (g.els[0].options[i].selected) o.push(g.els[0].options[i].value);
        return o;
      case "radio":
        for (i = 0; i < g.els.length; i++) if (g.els[i].checked) return g.els[i].value;
        return null;
      case "cek":
        for (i = 0; i < g.els.length; i++) if (g.els[i].checked) o.push(g.els[i].value);
        return o;
      default: return g.els[0].value;
    }
  }
  function sama(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

  function peristiwa(el, nama) {
    try { el.dispatchEvent(new Event(nama, { bubbles: true })); }
    catch (e) {
      try { var ev = document.createEvent("Event"); ev.initEvent(nama, true, true); el.dispatchEvent(ev); } catch (e2) {}
    }
  }
  /* Menulis nilai ke kotak, lalu memberi tahu skrip dokumen lewat peristiwa input/change, supaya hitungan,
     penanda "terisi", dan sebagainya ikut diperbarui. */
  function tulisGrup(g, v) {
    var i, ada, el;
    memulihkan = true;
    try {
      switch (g.bentuk) {
        case "bool":  el = g.els[0]; el.checked = !!v; peristiwa(el, "input"); peristiwa(el, "change"); break;
        case "multi":
          el = g.els[0]; v = Array.isArray(v) ? v.map(String) : [];
          for (i = 0; i < el.options.length; i++) el.options[i].selected = v.indexOf(el.options[i].value) > -1;
          peristiwa(el, "input"); peristiwa(el, "change"); break;
        case "radio":
          for (i = 0; i < g.els.length; i++) {
            ada = v !== null && String(g.els[i].value) === String(v);
            g.els[i].checked = ada;
            if (ada) { peristiwa(g.els[i], "input"); peristiwa(g.els[i], "change"); }
          }
          break;
        case "cek":
          v = Array.isArray(v) ? v.map(String) : [];
          for (i = 0; i < g.els.length; i++) {
            ada = v.indexOf(String(g.els[i].value)) > -1;
            if (g.els[i].checked !== ada) { g.els[i].checked = ada; peristiwa(g.els[i], "input"); peristiwa(g.els[i], "change"); }
          }
          break;
        default:
          el = g.els[0];
          if (v === null || v === undefined) v = "";
          el.value = String(v);
          if (g.tipe === "hidden") el.setAttribute("value", el.value);
          else { peristiwa(el, "input"); peristiwa(el, "change"); }
      }
    } finally { memulihkan = false; }
  }

  var memulihkan = false;       // sedang menulis nilai pulihan: abaikan peristiwa yang ditimbulkannya
  var awal = {};                // nilai bawaan tiap kunci, direkam saat kotaknya pertama terlihat
  var tertunda = {};            // nilai tersimpan yang kotaknya belum ada (dokumen membangunnya belakangan)

  function rekamAwal(pt) {
    for (var i = 0; i < pt.urut.length; i++) {
      var k = pt.urut[i];
      if (!(k in awal)) {
        awal[k] = nilaiGrup(pt.peta[k]);
        if (k in tertunda) { tulisGrup(pt.peta[k], tertunda[k]); delete tertunda[k]; }
      }
    }
  }

  function ambilF() {
    var pt = petakan(), f = {}, i, k;
    rekamAwal(pt);
    for (i = 0; i < pt.urut.length; i++) {
      k = pt.urut[i];
      var v = nilaiGrup(pt.peta[k]);
      if (!sama(v, awal[k])) f[k] = v;
    }
    for (k in tertunda) if (Object.prototype.hasOwnProperty.call(tertunda, k) && !(k in f)) f[k] = tertunda[k];
    return f;
  }

  function terapkanF(f) {
    var pt = petakan(), k;
    rekamAwalSebelumTulis(pt);
    for (k in f) {
      if (!Object.prototype.hasOwnProperty.call(f, k)) continue;
      if (pt.peta[k]) tulisGrup(pt.peta[k], f[k]); else tertunda[k] = f[k];
    }
  }
  /* Nilai bawaan harus terekam SEBELUM nilai pulihan ditulis, kalau tidak isian pulihan dianggap bawaan. */
  function rekamAwalSebelumTulis(pt) {
    for (var i = 0; i < pt.urut.length; i++) if (!(pt.urut[i] in awal)) awal[pt.urut[i]] = nilaiGrup(pt.peta[pt.urut[i]]);
  }

  /* Hitungan kasar kotak yang terisi, dipakai bila dokumen tidak punya FIMS_RINGKAS. Kotak centang dan kotak
     tersembunyi tidak dihitung (biasanya penanda ragu-ragu, bukan jawaban). */
  function hitungOtomatis() {
    var pt = petakan(), terisi = 0, total = 0, i, k, g, v;
    for (i = 0; i < pt.urut.length; i++) {
      k = pt.urut[i]; g = pt.peta[k];
      if (g.tipe === "hidden" || g.tipe === "checkbox" || g.tipe === "range" || g.bentuk === "bool" || g.bentuk === "cek") continue;
      total++;
      v = nilaiGrup(g);
      if (Array.isArray(v) ? v.length : (v !== null && String(v).trim() !== "")) terisi++;
    }
    return { terisi: terisi, total: total };
  }

  /* ---------- keadaan dan ringkasan ---------- */
  var manual = {};              // yang dilaporkan dokumen lewat FIMS_LEMBAR.lapor
  function ringkas() {
    var r = hitungOtomatis(), h = null, el;
    for (var k in manual) if (Object.prototype.hasOwnProperty.call(manual, k)) r[k] = manual[k];
    try { if (typeof window.FIMS_RINGKAS === "function") h = window.FIMS_RINGKAS(); } catch (e) {}
    if (h) for (var k2 in h) if (Object.prototype.hasOwnProperty.call(h, k2) && h[k2] !== undefined && h[k2] !== null) r[k2] = h[k2];
    if (r.selesai === undefined) { el = document.getElementById("selesai"); r.selesai = !!(el && el.value === "1"); }
    r.selesai = !!r.selesai;
    if (!r.selesai) r.skor = null;
    else if (r.skor === undefined || r.skor === null) {
      try { if (typeof window.hitungNilai === "function") r.skor = Number(window.hitungNilai()); } catch (e2) {}
      if (r.skor === undefined || !isFinite(r.skor)) r.skor = null;
    }
    return r;
  }
  function ambilX() {
    try { if (typeof window.FIMS_KEADAAN === "function") { var x = window.FIMS_KEADAAN(); return (x === undefined) ? null : x; } } catch (e) {}
    return null;
  }

  /* ---------- tampilan: bilah status, catatan reset, tirai pemuatan ---------- */
  var bar = null, teksStatus = null, kotakReset = null, tirai = null;
  function pasangCss() {
    if (document.getElementById("fims-simpan-css")) return;
    var s = document.createElement("style"); s.id = "fims-simpan-css";
    s.textContent =
      "#fims-simpan-bar{box-sizing:border-box;font:12.5px/1.35 system-ui,-apple-system,'Segoe UI',sans-serif;color:#475569;" +
      "background:#f1f5f9;border-bottom:1px solid #e2e8f0;padding:5px 12px;display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center}" +
      "#fims-simpan-bar .fs-st:before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:#94a3b8;margin-right:7px;vertical-align:0}" +
      "#fims-simpan-bar.ok .fs-st:before{background:#16a34a}#fims-simpan-bar.kerja .fs-st:before{background:#d97706}" +
      "#fims-simpan-bar.err .fs-st:before{background:#dc2626}#fims-simpan-bar.err{color:#991b1b;background:#fef2f2;border-color:#fecaca}" +
      "#fims-simpan-bar button{font:inherit;cursor:pointer;border:1px solid currentColor;background:transparent;color:inherit;border-radius:6px;padding:1px 9px}" +
      "#fims-simpan-bar .fs-reset{flex:1 1 100%;background:#fffbeb;color:#78350f;border:1px solid #fcd34d;border-radius:8px;padding:6px 10px;display:flex;gap:10px;align-items:flex-start;justify-content:space-between}" +
      "#fims-simpan-muat{position:fixed;inset:0;z-index:2147483000;background:rgba(255,255,255,0);display:grid;place-items:center;" +
      "font:600 15px system-ui,sans-serif;color:#334155;transition:background .2s}" +
      "#fims-simpan-muat.lihat{background:rgba(255,255,255,.72)}#fims-simpan-muat span{opacity:0}#fims-simpan-muat.lihat span{opacity:1}" +
      "@media (prefers-color-scheme:dark){#fims-simpan-bar{background:#1e293b;color:#cbd5e1;border-color:#334155}" +
      "#fims-simpan-bar.err{background:#450a0a;color:#fecaca;border-color:#7f1d1d}" +
      "#fims-simpan-bar .fs-reset{background:#422006;color:#fde68a;border-color:#92400e}" +
      "#fims-simpan-muat.lihat{background:rgba(15,23,42,.72)}#fims-simpan-muat{color:#e2e8f0}}" +
      "@media print{#fims-simpan-bar,#fims-simpan-muat{display:none!important}}";
    (document.head || document.documentElement).appendChild(s);
  }
  function pasangBilah() {
    if (bar || !document.body) return;
    pasangCss();
    bar = document.createElement("div"); bar.id = "fims-simpan-bar"; bar.setAttribute("role", "status"); bar.setAttribute("aria-live", "polite");
    bar.hidden = true;
    teksStatus = document.createElement("span"); teksStatus.className = "fs-st";
    bar.appendChild(teksStatus);
    document.body.insertBefore(bar, document.body.firstChild);
  }
  function status(kelas, teks, tombol) {
    pasangBilah(); if (!bar) return;
    bar.hidden = false;
    bar.className = kelas || "";
    teksStatus.textContent = teks;
    var lama = bar.querySelector(".fs-aksi"); if (lama) lama.remove();
    if (tombol) {
      var b = document.createElement("button"); b.type = "button"; b.className = "fs-aksi"; b.textContent = tombol.teks;
      b.addEventListener("click", tombol.aksi); bar.insertBefore(b, kotakReset || null);
    }
  }
  function tampilkanReset(rs) {
    pasangBilah(); if (!bar || !rs) return;
    var tanda = "fims-simpan-tutup:" + KUNCI + ":" + rs.pada;
    try { if (sessionStorage.getItem(tanda)) return; } catch (e) {}
    var tgl = "";
    try { tgl = new Date(rs.pada).toLocaleString(BHS === "en" ? "en-GB" : "id-ID", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }); } catch (e2) {}
    var isiBuka = [rs.nama || t("guruSaja"), tgl, rs.alasan ? " — " + rs.alasan : ""], nb = 0;
    var kalimat = t("buka").replace(/%s/g, function () { return isiBuka[nb++]; });
    kotakReset = document.createElement("div"); kotakReset.className = "fs-reset";
    var p = document.createElement("span"); p.textContent = "↺ " + kalimat;
    var x = document.createElement("button"); x.type = "button"; x.textContent = t("tutup");
    x.addEventListener("click", function () { try { sessionStorage.setItem(tanda, "1"); } catch (e3) {} kotakReset.remove(); kotakReset = null; });
    kotakReset.appendChild(p); kotakReset.appendChild(x);
    bar.hidden = false; bar.appendChild(kotakReset);
  }
  function pasangTirai() {
    if (!document.body) return;
    pasangCss();
    tirai = document.createElement("div"); tirai.id = "fims-simpan-muat"; tirai.setAttribute("aria-busy", "true");
    var s = document.createElement("span"); s.textContent = t("memuat"); tirai.appendChild(s);
    document.body.appendChild(tirai);
    setTimeout(function () { if (tirai) tirai.className = "lihat"; }, 400);
  }
  function lepasTirai() { if (tirai) { tirai.remove(); tirai = null; } }

  /* ---------- hubungan dengan peladen ---------- */
  var aktifSimpan = false;      // boleh menyimpan (murid, sudah masuk, sudah selesai memuat)
  var siap = false;             // isian lama selesai dimuat
  var epoch = 0;
  var terakhir = "";            // kiriman terakhir yang BERHASIL, untuk membandingkan perubahan
  var sedangKirim = false, adaLagi = false, tundaSampai = 0, perluKirim = false, sedangMuatUlang = false;

  function bangunMuatan() {
    var r = ringkas(), data = { f: ambilF() }, x = ambilX();
    if (x !== null) data.x = x;
    return { kunci: KUNCI, epoch: epoch, data: data, skor: r.skor, selesai: r.selesai ? 1 : 0, terisi: r.terisi, total: r.total };
  }

  function kirim(sinkron) {
    if (!siap || !aktifSimpan) { if (!siap) perluKirim = true; return; }
    if (Date.now() < tundaSampai && !sinkron) return;
    var s = JSON.stringify(bangunMuatan());
    if (s === terakhir) return;
    if (sinkron) {                                         // tab ditutup / disembunyikan
      try {
        if (navigator.sendBeacon && navigator.sendBeacon(API, new Blob([s], { type: "application/json" }))) return;
      } catch (e) {}
      try { fetch(API, { method: "PUT", headers: { "content-type": "application/json" }, body: s, keepalive: true, credentials: "same-origin" }); } catch (e2) {}
      return;
    }
    if (sedangKirim) { adaLagi = true; return; }
    sedangKirim = true; status("kerja", t("simpan"));
    fetch(API, { method: "PUT", headers: { "content-type": "application/json" }, body: s, credentials: "same-origin", keepalive: true })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { st: r.status, d: d || {} }; }); })
      .then(function (res) {
        sedangKirim = false;
        if (res.d.usang) return usang();
        if (res.st === 401) { aktifSimpan = false; return status("err", t("masuk")); }
        if (res.st === 413) { tundaSampai = Date.now() + 60000; return status("err", t("besar")); }
        if (res.st === 429) { tundaSampai = Date.now() + 60000; return status("err", t("penuh")); }
        if (res.st >= 400 || !res.d.ok) { tundaSampai = Date.now() + 10000; return status("err", t("gagal")); }
        terakhir = s; tundaSampai = 0;
        var jam = ""; try { jam = " · " + new Date().toLocaleTimeString(BHS === "en" ? "en-GB" : "id-ID", { hour: "2-digit", minute: "2-digit" }); } catch (e3) {}
        status("ok", t("ok") + jam);
        if (adaLagi) { adaLagi = false; kirim(); }
      })
      .catch(function () { sedangKirim = false; tundaSampai = Date.now() + 10000; status("err", t("gagal")); });
  }

  function usang() {
    if (sedangMuatUlang) return;
    sedangMuatUlang = true; aktifSimpan = false;
    status("kerja", t("usang"));
    setTimeout(function () { try { location.reload(); } catch (e) {} }, 1600);
  }

  function cekEpoch() {
    if (!siap || !aktifSimpan || document.hidden || sedangMuatUlang) return;
    fetch(API + "?epoch=1&kunci=" + encodeURIComponent(KUNCI), { credentials: "same-origin", cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d && d.ada && Number(d.epoch) > epoch) usang(); })
      .catch(function () {});
  }

  /* ---------- memuat isian lama ---------- */
  var percobaan = 0, lewatBatas = false;

  function sesudahMuat(d) {
    var pernah = d && d.ada && d.data;
    epoch = d && d.epoch ? Number(d.epoch) : 0;
    if (pernah) {
      var f = d.data.f || {};
      if (lewatBatas) {
        // Peladen lambat dan murid sempat mengisi. Jangan menimpa; jangan menyimpan; minta muat ulang.
        var diubah = false, k;
        var sekarang = ambilF(); for (k in sekarang) { diubah = true; break; }
        if (diubah && Object.keys(f).length) {
          aktifSimpan = false;
          status("err", t("lambat"), { teks: t("muatUlang"), aksi: function () { location.reload(); } });
          return;
        }
      }
      terapkanF(f);
      if (d.selesai) manual.selesai = true;
      if (d.data.reset && !Object.keys(f).length && d.data.x === undefined) tampilkanReset(d.data.reset);
      var info = { selesai: !!d.selesai, skor: d.skor, terisi: d.terisi, total: d.total, x: d.data.x };
      var panggil = function () {
        try { if (typeof window.FIMS_PULIHKAN === "function") window.FIMS_PULIHKAN(info); } catch (e) {}
      };
      if (document.readyState === "complete") panggil(); else window.addEventListener("load", panggil);
    }
    // Sesudah pemulihan, keadaan sekarang menjadi pembanding: yang dikirim hanya perubahan sesudahnya.
    siap = true; aktifSimpan = true;
    terakhir = JSON.stringify(bangunMuatan());
    if (pernah) status("ok", t("ok")); else if (bar) bar.hidden = true;
    if (perluKirim) { perluKirim = false; kirim(); }
  }

  function muat() {
    fetch(API + "?kunci=" + encodeURIComponent(KUNCI), { credentials: "same-origin", cache: "no-store" })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { st: r.status, d: d || {} }; }); })
      .then(function (res) {
        lepasTirai();
        if (res.st === 401) return status("", t("masuk"));
        if (res.d.simpan === false) { aktifSimpan = false; return status("", t("guru")); }
        if (res.st !== 200) throw new Error("http " + res.st);
        try { sesudahMuat(res.d); }
        catch (e) {
          // Pemulihan gagal di tengah jalan: JANGAN menyimpan apa pun, supaya isian lama di peladen tidak tertimpa.
          siap = false; aktifSimpan = false;
          status("err", t("gagalPulih"), { teks: t("muatUlang"), aksi: function () { location.reload(); } });
        }
      })
      .catch(function () {
        lepasTirai();
        percobaan++;
        status("err", t("offline"));
        if (percobaan <= 6) setTimeout(muat, 8000 * percobaan);   // jangan menyimpan apa pun sebelum berhasil memuat
      });
  }

  /* ---------- API untuk dokumen ---------- */
  window.FIMS_LEMBAR = {
    kunci: KUNCI,
    lapor: function (o) {
      if (o && typeof o === "object") for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) manual[k] = o[k];
      kirim();
    },
    simpanSekarang: function () { kirim(); },
    aktif: function () { return aktifSimpan; }
  };

  /* ---------- pemasangan ---------- */
  function mulai() {
    pasangTirai();
    setTimeout(function () { if (!siap) { lewatBatas = true; lepasTirai(); } }, TUNGGU_MUAT);
    muat();
    setInterval(function () { kirim(); }, JEDA_CEK);
    setInterval(cekEpoch, JEDA_POLL);
    document.addEventListener("visibilitychange", function () { if (document.hidden) kirim(true); else cekEpoch(); });
    window.addEventListener("pagehide", function () { kirim(true); });
    if (window.MutationObserver) {
      var tunda = null;
      new MutationObserver(function () {
        if (tunda) return;
        tunda = setTimeout(function () { tunda = null; rekamAwal(petakan()); }, 120);
      }).observe(document.body, { childList: true, subtree: true });
    }
    rekamAwal(petakan());
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mulai);
  else mulai();
})();
