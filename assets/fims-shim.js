/* ============================================================
   FIMS-SHIM v2 — mesin lembar tahapan, satu berkas untuk semua.

   Halaman tahapan cukup menulis markah soalnya. Berkas ini yang
   mengurus: membaca bilangan, menilai, bilah bawah yang dapat
   dilipat, daftar nomor yang masih salah, dan pelaporan ke
   mesin alur di halaman induk.

   Cara memakainya pada satu halaman:
     <script>window.FIMS_KUNCI = {
        num: { "a1": [45, 0.2] },      // jawaban berupa bilangan [nilai, toleransi]
        pil: { "a2": "B" }             // jawaban berupa pilihan
     };</script>
     <script src="..../assets/fims-shim.js"></script>

   Tanpa FIMS_KUNCI, halaman hanya melapor "selesai" lewat
   tombol #fims-kirim.
   ============================================================ */
/* Penyimpan isian per akun (fims-simpan.js) dimuat otomatis dari folder yang sama dengan berkas ini. */
(function () {
  try {
    if (window.FIMS_LEMBAR || document.getElementById("fims-simpan-js")) return;
    var me = document.currentScript, src = me && me.src ? me.src.replace(/fims-shim\.js(\?.*)?$/, "fims-simpan.js") : "/assets/fims-simpan.js";
    var e = document.createElement("script"); e.id = "fims-simpan-js"; e.src = src;
    (document.head || document.documentElement).appendChild(e);
  } catch (x) {}
})();

(function () {
  "use strict";

  var K        = window.FIMS_KUNCI || null;
  var ADA_NILAI = !!(K && ((K.num && Object.keys(K.num).length) || (K.pil && Object.keys(K.pil).length)));
  var TERPASANG = (window.parent !== window);
  var sudahKirim = false;

  var IDS_NUM = (K && K.num) ? Object.keys(K.num) : [];
  var IDS_PIL = (K && K.pil) ? Object.keys(K.pil) : [];
  var TOTAL   = IDS_NUM.length + IDS_PIL.length;

  /* ---------- membaca bilangan yang ditulis murid ----------
     Koma dan titik sama-sama diterima, termasuk pemisah ribuan,
     supaya "1.250", "1,250", "1250" dibaca sama.               */
  function bacaAngka(teks) {
    if (teks === null || teks === undefined) return null;
    var s = String(teks).replace(/−/g, "-").replace(/\s+/g, "");
    if (s === "") return null;
    if (/^-?\d{1,3}([.,]\d{3})+$/.test(s)) {
      s = s.replace(/[.,]/g, "");
    } else if (s.indexOf(".") >= 0 && s.indexOf(",") >= 0) {
      var t = Math.max(s.lastIndexOf("."), s.lastIndexOf(","));
      s = s.slice(0, t).replace(/[.,]/g, "") + "." + s.slice(t + 1);
    } else {
      s = s.replace(",", ".");
    }
    if (!/^-?\d*\.?\d+$/.test(s)) return null;
    var v = parseFloat(s);
    return isFinite(v) ? v : null;
  }

  /* ---------- menyalin isian ke atribut ----------
     Supaya halaman yang disimpan atau dicetak tetap membawa
     jawabannya, bukan kotak kosong.                            */
  function cermin(el) {
    if (!el || !el.tagName) return;
    var tag = el.tagName.toLowerCase();
    if (tag === "input") {
      var t = (el.getAttribute("type") || "text").toLowerCase();
      if (t === "checkbox" || t === "radio") {
        if (el.checked) el.setAttribute("checked", "checked");
        else el.removeAttribute("checked");
      } else { el.setAttribute("value", el.value); }
    } else if (tag === "textarea") {
      el.textContent = el.value;
    } else if (tag === "select") {
      for (var i = 0; i < el.options.length; i++) {
        if (el.options[i].selected) el.options[i].setAttribute("selected", "selected");
        else el.options[i].removeAttribute("selected");
      }
    }
  }
  function cerminSemua() {
    var d = document.querySelectorAll("input, select, textarea");
    for (var i = 0; i < d.length; i++) cermin(d[i]);
  }

  /* ---------- kunci tersandi ----------
     Pada gerbang, kunci tidak ditulis apa adanya di halaman, melainkan sebagai
     hash SHA-256 bergaram. Murid yang membuka kode sumber tidak menemukan
     jawabannya. Ini penghalang, bukan rahasia kriptografis: garamnya ikut
     dikirim ke peramban karena penilaian memang dikerjakan di sisi murid. */
function sha256(ascii){
  function rr(n,x){return (n>>>x)|(n<<(32-x));}
  var mx=Math.pow,h=[],k=[],p=2,i=0,j,res="";
  while(i<64){
    var isP=true;
    for(j=2;j*j<=p;j++){ if(p%j===0){isP=false;break;} }
    if(isP){ if(i<8) h[i]=(mx(p,.5)%1*4294967296)|0; k[i]=(mx(p,1/3)%1*4294967296)|0; i++; }
    p++;
  }
  var bytes=[];
  for(i=0;i<ascii.length;i++){
    var c=ascii.charCodeAt(i);
    if(c<128) bytes.push(c);
    else if(c<2048){ bytes.push(192|(c>>6),128|(c&63)); }
    else { bytes.push(224|(c>>12),128|((c>>6)&63),128|(c&63)); }
  }
  var bitLen=bytes.length*8;
  bytes.push(128);
  while(bytes.length%64!==56) bytes.push(0);
  for(i=7;i>=0;i--) bytes.push((bitLen/mx(2,i*8))&255);
  var w=[],a,b,cc,d,e,f,g,hh,ta,tb;
  for(var blk=0;blk<bytes.length;blk+=64){
    for(i=0;i<16;i++){
      w[i]=(bytes[blk+i*4]<<24)|(bytes[blk+i*4+1]<<16)|(bytes[blk+i*4+2]<<8)|(bytes[blk+i*4+3]);
    }
    for(i=16;i<64;i++){
      var s0=rr(w[i-15],7)^rr(w[i-15],18)^(w[i-15]>>>3);
      var s1=rr(w[i-2],17)^rr(w[i-2],19)^(w[i-2]>>>10);
      w[i]=(w[i-16]+s0+w[i-7]+s1)|0;
    }
    a=h[0];b=h[1];cc=h[2];d=h[3];e=h[4];f=h[5];g=h[6];hh=h[7];
    for(i=0;i<64;i++){
      var S1=rr(e,6)^rr(e,11)^rr(e,25);
      var ch=(e&f)^((~e)&g);
      ta=(hh+S1+ch+k[i]+w[i])|0;
      var S0=rr(a,2)^rr(a,13)^rr(a,22);
      var maj=(a&b)^(a&cc)^(b&cc);
      tb=(S0+maj)|0;
      hh=g;g=f;f=e;e=(d+ta)|0;d=cc;cc=b;b=a;a=(ta+tb)|0;
    }
    h[0]=(h[0]+a)|0;h[1]=(h[1]+b)|0;h[2]=(h[2]+cc)|0;h[3]=(h[3]+d)|0;
    h[4]=(h[4]+e)|0;h[5]=(h[5]+f)|0;h[6]=(h[6]+g)|0;h[7]=(h[7]+hh)|0;
  }
  for(i=0;i<8;i++){
    var v=h[i]>>>0, s=v.toString(16);
    while(s.length<8) s="0"+s;
    res+=s;
  }
  return res;
}

  var TERSANDI = !!(K && K.garam);
  var FAKTOR   = (K && K.faktor) || 20;
  function sidikNum(id, n) { return sha256(K.garam + "|" + id + "|" + n); }
  function sidikPil(id, j) { return sha256(K.garam + "|" + id + "|" + String(j).trim()); }

  /* ---------- menilai ---------- */
  function benarkah(id) {
    var el = document.getElementById(id);
    if (!el) return false;
    if (K.num && Object.prototype.hasOwnProperty.call(K.num, id)) {
      var v = bacaAngka(el.value), k = K.num[id];
      if (v === null) return false;
      if (TERSANDI) {
        var c = sidikNum(id, Math.round(v * FAKTOR));
        for (var i = 0; i < k[0].length; i++) if (k[0][i] === c) return true;
        return false;
      }
      return Math.abs(v - k[0]) <= (k.length > 1 ? k[1] : 0.01) + 1e-9;
    }
    if (K.pil && Object.prototype.hasOwnProperty.call(K.pil, id)) {
      var j = String(el.value).trim();
      if (j === "") return false;
      return TERSANDI ? sidikPil(id, j) === K.pil[id] : j === String(K.pil[id]).trim();
    }
    return false;
  }

  function hitungNilai() {
    if (!ADA_NILAI) return 0;
    cerminSemua();
    var benar = 0;
    for (var i = 0; i < IDS_NUM.length; i++) if (benarkah(IDS_NUM[i])) benar++;
    for (var j = 0; j < IDS_PIL.length; j++) if (benarkah(IDS_PIL[j])) benar++;
    return TOTAL ? Math.round((benar / TOTAL) * 100) : 0;
  }
  window.hitungNilai = hitungNilai;

  /* ---------- nomor soal mana yang masih salah ----------
     Diurutkan mengikuti urutan soal di lembar, bukan urutan kunci. */
  function butirSalah() {
    cerminSemua();
    var tandai = {}, salah = [], semua = IDS_NUM.concat(IDS_PIL), i;
    for (i = 0; i < semua.length; i++) if (!benarkah(semua[i])) tandai[semua[i]] = true;

    var urut = [], peta = {}, sudah = {}, blok = document.querySelectorAll(".soal, .kartu-soal");
    for (i = 0; i < blok.length; i++) {
      var medan = blok[i].querySelectorAll("[id]"), kena = false, m;
      for (m = 0; m < medan.length; m++) if (tandai[medan[m].id]) { kena = true; break; }
      if (!kena) continue;
      for (m = 0; m < medan.length; m++) if (tandai[medan[m].id]) sudah[medan[m].id] = true;
      var jud = blok[i].querySelector(".soal-judul") || blok[i].querySelector(":scope > h3");
      var sp  = jud ? jud.querySelector("span") : null;
      var teks = ((sp || jud) ? String((sp || jud).textContent || "") : "").replace(/\s+/g, " ").trim();
      if (!teks) teks = "Soal " + (i + 1);
      if (!Object.prototype.hasOwnProperty.call(peta, teks)) { peta[teks] = blok[i]; urut.push(teks); }
    }
    for (i = 0; i < semua.length; i++) {
      if (!tandai[semua[i]] || sudah[semua[i]]) continue;
      var el = document.getElementById(semua[i]);
      var lab = el ? document.querySelector('label[for="' + semua[i] + '"]') : null;
      var t2 = lab ? lab.textContent.replace(/\s+/g, " ").trim() : semua[i];
      if (!Object.prototype.hasOwnProperty.call(peta, t2)) { peta[t2] = el; urut.push(t2); }
    }
    for (i = 0; i < semua.length; i++) if (tandai[semua[i]]) salah.push(semua[i]);
    return { nama: urut, peta: peta, salah: salah, total: TOTAL, benar: TOTAL - salah.length };
  }
  window.fimsButirSalah = butirSalah;

  /* ---------- kotak ringkasan di dalam lembar ---------- */
  function gambarRingkas(d) {
    var induk = document.querySelector(".bilah-dalam") || document.body;
    var kotak = document.getElementById("fims-salah");
    if (!kotak) {
      kotak = document.createElement("div");
      kotak.id = "fims-salah";
      kotak.setAttribute("role", "status");
      induk.appendChild(kotak);
    }
    if (!d.nama.length) {
      kotak.innerHTML = "<b>Semua butir sudah benar.</b> Benar " + d.benar + " dari " + d.total + " butir.";
      return;
    }
    var h = "<b>Masih ada " + d.nama.length + " nomor yang salah.</b> Benar " + d.benar +
            " dari " + d.total + " butir.<div>";
    for (var i = 0; i < d.nama.length; i++) {
      h += '<span class="nomor" data-ke="' + i + '">' + d.nama[i].replace(/[<>&]/g, "") + "</span>";
    }
    h += '</div><p style="margin:8px 0 0">Klik nomornya untuk melompat ke soal itu. ' +
         "Kerjakan ulang langkahnya, lalu periksa lagi. Kunci jawaban sengaja tidak ditampilkan.</p>";
    kotak.innerHTML = h;
    var chip = kotak.querySelectorAll("[data-ke]");
    for (var j = 0; j < chip.length; j++) {
      (function (c) {
        c.addEventListener("click", function () {
          var sasaran = d.peta[d.nama[+c.dataset.ke]];
          if (!sasaran) return;
          try { sasaran.scrollIntoView({ behavior: "smooth", block: "center" }); }
          catch (e) { sasaran.scrollIntoView(); }
          sasaran.classList.add("disorot");
          setTimeout(function () { sasaran.classList.remove("disorot"); }, 2600);
        });
      })(chip[j]);
    }
  }

  /* ---------- bilah bawah ---------- */
  function daftarIsian() { return document.querySelectorAll("[data-isian]"); }
  function terisi(el) { return String(el.value).trim() !== ""; }

  function perbarui() {
    var d = daftarIsian(), n = d.length, x = 0, i;
    for (i = 0; i < n; i++) {
      if (terisi(d[i])) { x++; d[i].classList.add("terisi"); d[i].classList.remove("kosong"); }
      else d[i].classList.remove("terisi");
    }
    var jalur = document.getElementById("isi-jalur"), teks = document.getElementById("hitung-teks");
    if (jalur) jalur.style.width = (n ? Math.round(100 * x / n) : 0) + "%";
    if (teks) teks.textContent = x + " dari " + n + " isian dijawab";
  }

  function periksaKelengkapan() {
    cerminSemua();
    var d = daftarIsian(), kosong = [], i;
    for (i = 0; i < d.length; i++) {
      if (!terisi(d[i])) { d[i].classList.add("kosong"); kosong.push(d[i]); }
      else d[i].classList.remove("kosong");
    }
    var pesan = document.getElementById("pesan");
    if (kosong.length) {
      if (pesan) pesan.textContent = "Masih ada " + kosong.length +
        " isian yang kosong — kotak itu ditandai oranye.";
      try { kosong[0].scrollIntoView({ behavior: "smooth", block: "center" }); }
      catch (e) { kosong[0].scrollIntoView(); }
      try { kosong[0].focus({ preventScroll: true }); } catch (e2) {}
    } else if (pesan) {
      pesan.textContent = "Semua isian sudah terisi. Tekan Selesai untuk mengirimkan.";
    }
    perbarui();
  }

  /* ---------- melapor ke mesin alur ---------- */
  var selesaiLembar = false;       // murid sudah menekan Selesai (juga bila lembar dibuka sendiri, bukan lewat situs)
  function lapor() {
    selesaiLembar = true;
    try { if (window.FIMS_LEMBAR) window.FIMS_LEMBAR.lapor({ selesai: true }); } catch (e0) {}
    if (!TERPASANG) return false;
    try {
      if (ADA_NILAI) {
        var d = butirSalah();
        parent.postMessage({ fims: "skor", skor: hitungNilai(),
          salah: d.salah, benar: d.benar, total: d.total }, "*");
      } else {
        parent.postMessage({ fims: "selesai" }, "*");
      }
      sudahKirim = true;
      return true;
    } catch (e) { return false; }
  }

  /* ---------- kait untuk penyimpan isian per akun ---------- */
  window.FIMS_RINGKAS = function () {
    var r = { selesai: selesaiLembar };
    if (ADA_NILAI) {
      var semua = IDS_NUM.concat(IDS_PIL), n = 0, i, el;
      for (i = 0; i < semua.length; i++) { el = document.getElementById(semua[i]); if (el && terisi(el)) n++; }
      r.terisi = n; r.total = TOTAL;
      if (selesaiLembar) r.skor = hitungNilai();
    }
    return r;
  };
  window.FIMS_PULIHKAN = function (info) {
    if (!info || !info.selesai) return;
    selesaiLembar = true; sudahKirim = true;       // hasilnya sudah tercatat sebelumnya: tampilkan lagi, jangan kirim ulang
    try { if (ADA_NILAI) { cerminSemua(); gambarRingkas(butirSalah()); perbarui(); } } catch (e) {}
    try { kabar(document.getElementById("btn_selesai") || document.getElementById("fims-kirim")); } catch (e2) {}
  };

  function kabar(dekat) {
    var k = document.getElementById("fims-kabar");
    if (!k) {
      k = document.createElement("p");
      k.id = "fims-kabar";
      k.setAttribute("role", "status");
      (dekat && dekat.parentNode ? dekat.parentNode : document.body).appendChild(k);
    }
    k.textContent = sudahKirim ? "Hasilmu sudah terkirim." : "Tercatat di halaman ini.";
  }

  /* ---------- bilah yang dapat dilipat ---------- */
  function pasangLipat() {
    var bar = document.querySelector(".bilah-bawah");
    if (!bar || document.querySelector(".lipat-tombol")) return;
    var KUNCI = "fims-lipat:" + location.pathname;
    var tb = document.createElement("button");
    tb.type = "button"; tb.className = "lipat-tombol";
    bar.appendChild(tb);

    var aksi = document.getElementById("btn_selesai") || document.getElementById("fims-kirim-bar");
    if (aksi) { aksi.classList.add("fims-aksi"); document.body.classList.add("ada-kirim"); }

    function ukur() { document.body.style.paddingBottom = (bar.offsetHeight + 16) + "px"; }
    function pasang(lipat, ingat) {
      document.body.classList.toggle("bilah-lipat", !!lipat);
      tb.textContent = lipat ? "▲ Tampilkan panel" : "▼ Sembunyikan panel";
      tb.setAttribute("aria-expanded", lipat ? "false" : "true");
      if (ingat) { try { localStorage.setItem(KUNCI, lipat ? "1" : "0"); } catch (e) {} }
      ukur();
    }
    tb.addEventListener("click", function () {
      pasang(!document.body.classList.contains("bilah-lipat"), true);
    });
    var awal = false;
    try { awal = localStorage.getItem(KUNCI) === "1"; } catch (e) {}
    pasang(awal, false);
    if (window.ResizeObserver) new ResizeObserver(ukur).observe(bar);
    window.addEventListener("resize", ukur);
    if (window.MutationObserver) {
      var terakhir = null;
      new MutationObserver(function () {
        var k = document.getElementById("fims-salah");
        var kini = k ? k.innerHTML : null;
        if (kini !== null && kini !== terakhir) {
          terakhir = kini;
          if (document.body.classList.contains("bilah-lipat")) { pasang(false, false); return; }
        }
        ukur();
      }).observe(bar, { childList: true, subtree: true, characterData: true });
    }
  }

  /* ---------- pemasangan ---------- */
  function pasang() {
    if (ADA_NILAI) {
      var pr = document.getElementById("btn_periksa");
      if (pr) pr.addEventListener("click", periksaKelengkapan);
      var sl = document.getElementById("btn_selesai");
      if (sl) sl.addEventListener("click", function () {
        setTimeout(function () { gambarRingkas(butirSalah()); lapor(); kabar(sl); }, 0);
      });
      document.addEventListener("input",  function (e) { cermin(e.target); perbarui(); });
      document.addEventListener("change", function (e) { cermin(e.target); perbarui(); });
      document.addEventListener("blur",   function (e) { cermin(e.target); }, true);
      window.addEventListener("pagehide", cerminSemua);
      document.addEventListener("visibilitychange", cerminSemua);
      cerminSemua(); perbarui(); pasangLipat();
    } else {
      var el = document.getElementById("fims-kirim");
      if (!el) {
        if (!TERPASANG) return;
        el = document.createElement("button");
        el.type = "button"; el.id = "fims-kirim"; el.textContent = "Kirim hasil";
        document.body.appendChild(el);
      }
      el.addEventListener("click", function () {
        setTimeout(function () { lapor(); kabar(el); }, 0);
      });
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", pasang);
  else pasang();
})();
