/* Kode publik P; kunci lama tetap dibaca agar progres dan penilaian akun tidak hilang. */
(function () {
  'use strict';
  const groups = [
    ['P1','Pembuka dan Tujuan',['S1'],'star'], ['P2','Cek Prasyarat',['S2','S2b','S2c'],'clipboard'],
    ['P3','Prediksi Awal',['S3'],'bulb'], ['P4','Konsep dan Praktik',['S4','S5','S6','S7'],'book'],
    ['P5','Cek Pemahaman',['S8'],'trophy'], ['P6','Tindak Lanjut',['S9'],'vector'],
    ['P7','Latihan Persiapan',['S11'],'clipboard'], ['P8','Tugas Penerapan',['S12'],'flag'],
    ['P9','Uji Ketuntasan TP',['S13'],'trophy'], ['P10','Ulangi Materi',['S14'],'repeat']
  ];
  const toPublic = { S1:'P1',S2:'P2',S2b:'P2a',S2c:'P2b',S3:'P3',S4:'P4',S5:'P4-diskusi',S6:'P4-contoh',S7:'P4-praktik',S8:'P5',S9:'P6',S11:'P7',S12:'P8',S13:'P9',S14:'P10' };
  const toOld = Object.fromEntries(Object.entries(toPublic).map(([a,b]) => [b.toLowerCase(),a]));
  toOld.p6a = 'S9'; toOld.p6b = 'S9';
  function label(text) { return String(text).replace(/\bS(?:1[0-4]|[1-9])(?:[bc])?\b/g, code => toPublic[code] || 'tahap arsip'); }
  function html(text) {
    return String(text).split(/(<[^>]+>)/g).map(part => {
      if (!part.startsWith('<')) return label(part);
      return part.replace(/((?:title|aria-label)="[^"]*)"/g, (_, a) => label(a) + '"')
        .replace(/(href="#tp-[^"]+)-(s\d+[bc]?)"/gi, (_, a, b) => a + '-' + (toPublic[b.toUpperCase().replace(/[BC]$/,x=>x.toLowerCase())] || 'p1').toLowerCase() + '"');
    }).join('');
  }
  function decorate(doc) {
    if (!doc || !doc.body || doc.__fiwaPLabels) return; doc.__fiwaPLabels = true;
    function run() {
      const walker = doc.createTreeWalker(doc.body, 4), nodes = []; let n;
      while ((n=walker.nextNode())) if (!n.parentElement.closest('script,style,textarea,input,pre,code,svg,math,[contenteditable]') && /\bS\d/.test(n.nodeValue)) nodes.push(n);
      nodes.forEach(n => { const value=label(n.nodeValue); if(value!==n.nodeValue) n.nodeValue=value; });
    }
    run(); let queued=false;
    new MutationObserver(() => { if (!queued) { queued=true; queueMicrotask(() => {queued=false; run();}); } }).observe(doc.body,{childList:true,subtree:true});
  }
  window.FIWA_ALUR = { groups,toPublic,toOld,label,html,decorate };
  document.addEventListener('DOMContentLoaded', () => decorate(document));
})();
