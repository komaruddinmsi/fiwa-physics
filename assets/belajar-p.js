(function () {
 'use strict';
 const config=window.FIWA_LESSON||{},mode=document.body.dataset.lessonMode;
 const focus=Number(new URL(location.href).searchParams.get('fokus')||0),selected=mode==='followup'&&(config.focusSets||[])[focus-1];
 if(selected){document.getElementById('lesson-questions').innerHTML=selected.html;document.getElementById('focus-note').textContent=selected.note;config.questions=selected.questions;}
 const questions=config.questions||[];
 let first=null,last=null,attempts=0,done=false,checked=[],reviewSent=false;
 const result=document.getElementById('lesson-result'),cycle=new URL(location.href).searchParams.get('cycle')||'0';
 function match(q) { const el=document.getElementById(q.id);if(!el||!el.value.trim())return false;
  if(q.t==='pil')return el.value===String(q.nilai);
  const value=Number(el.value.trim().replace(/−/g,'-').replace(',','.'));
  return Number.isFinite(value)&&Math.abs(value-q.nilai)<=q.tol;
 }
 function report(score,complete) {
  const data={fims:score==null?'selesai':'skor',skor:score,total:questions.length,benar:questions.filter(match).length,salah:questions.map((q,i)=>match(q)?null:String(i+1)).filter(Boolean),branch:config.branch,focus,session:config.session,awal:first,versi:2};
  if(mode==='review')data.answers=Object.fromEntries(questions.map(q=>[q.id,document.getElementById(q.id).value]));
  if(window.FIMS_LEMBAR)window.FIMS_LEMBAR.lapor({selesai:complete,skor:score});
  if(window.parent!==window)window.parent.postMessage(data,location.origin);
 }
 function show(q) { const ok=match(q),p=document.querySelector('[data-feedback="'+q.id+'"]');if(p){p.hidden=false;p.classList.toggle('wrong',!ok);}const el=document.getElementById(q.id);if(el)el.setAttribute('aria-invalid',String(!ok));return ok; }
 function grade() {
  if(mode==='review'&&reviewSent)return;
  const empty=questions.find(q=>!document.getElementById(q.id).value.trim());
  if(empty){result.textContent='Lengkapi jawaban sebelum memeriksa.';document.getElementById(empty.id).focus();return;}
  const correct=questions.filter(show).length,score=Math.round(correct/questions.length*100);
  if(first===null)first=score;last=score;attempts++;done=mode==='review'||score>=config.threshold;
  result.textContent=correct+' dari '+questions.length+' tepat ('+score+'%). '+(mode==='review'?(score>=config.threshold?'Sesi lulus. ':'Sesi memerlukan penguatan. '):done?'Persiapan selesai. ':'Periksa pembahasan dan perbaiki bagian yang belum tepat. ')+(mode==='followup'&&done?'Lanjutkan cek ulang P5 bersama guru.':'')+' Hasil mandiri pertama: '+first+'%.';
  if(mode==='review'){reviewSent=true;document.getElementById('lesson-finish').disabled=true;questions.forEach(q=>document.getElementById(q.id).disabled=true);result.textContent+=' Sesi sudah dikirim. Ikuti jadwal berikutnya di panel P10.';}
  report(score,done);
 }
 document.querySelectorAll('[data-checkpoint]').forEach(button=>button.addEventListener('click',()=>{
  const i=Number(button.dataset.checkpoint),q=questions[i-1],el=document.getElementById(q.id),status=document.querySelector('[data-cp-status="'+i+'"]');
  if(!el.value.trim()){status.textContent='Coba jawab terlebih dahulu.';el.focus();return;}
  const ok=show(q);checked[i-1]=ok;status.textContent=ok?'Tepat. Hubungkan alasan ini dengan konsep di atas.':'Baca penjelasannya, lalu coba kembali.';
 }));
 document.getElementById('lesson-finish').addEventListener('click',()=>{
  if(mode==='reading'){done=true;result.textContent='Tujuan belajar tercatat. Lanjutkan Cek Prasyarat pada P2.';report(null,true);}
  else if(mode==='concept'){
   if(!questions.every((_,i)=>checked[i])){result.textContent='Jawab dan periksa seluruh checkpoint dengan tepat terlebih dahulu.';return;}
   done=true;result.textContent='Konsep dan checkpoint selesai. Lanjutkan diskusi dan praktik kelas pada subbagian P4.';report(null,true);
  }else grade();
 });
 window.FIMS_RINGKAS=()=>({selesai:done,skor:last,terisi:questions.filter(q=>document.getElementById(q.id).value.trim()).length,total:questions.length});
 window.FIMS_KEADAAN=()=>({first,last,attempts,done,checked,reviewSent,cycle,focus,version:2});
 window.FIMS_PULIHKAN=info=>{const x=info&&info.x;if(!x||x.version!==2)return;if(mode==='followup'&&Number(x.focus||0)!==focus)return;if(mode==='review'&&x.cycle!==cycle){questions.forEach(q=>{const e=document.getElementById(q.id);e.value='';e.disabled=false;});result.textContent='Sesi pengulangan baru. Kerjakan tanpa melihat jawaban sebelumnya.';return;}first=x.first;last=x.last;attempts=x.attempts||0;done=!!x.done;checked=x.checked||[];reviewSent=!!x.reviewSent;if(mode==='review'&&reviewSent){document.getElementById('lesson-finish').disabled=true;questions.forEach(q=>document.getElementById(q.id).disabled=true);}if(last!=null){questions.forEach(show);result.textContent='Hasil tersimpan: '+last+'%. Hasil mandiri pertama: '+first+'%.';}};
})();
