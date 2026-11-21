/* Interaksi materi v4.1, penilaian per butir, waktu rekomendasi, dan pemulihan jawaban. */
(function () {
 'use strict';
 const config=window.FIWA_CLASS||{},stage=config.stage||'',version=Number(config.version||3);
 const cycle=new URL(location.href).searchParams.get('cycle')||'0',focus=Number(new URL(location.href).searchParams.get('fokus')||0);
 const focused=stage==='P6'&&(config.focusSets||[])[focus-1];
 if(focused){document.querySelector('.class-question-list').innerHTML=focused.html;document.getElementById('focus-note').textContent=focused.note;config.questions=focused.questions;}
 const questions=config.questions||[];
 let first=null,last=null,attempts=0,done=false,submitted=false,started=0,checked={},timer;
 const finish=document.getElementById('class-submit'),result=document.getElementById('class-result');
 const answerElement=q=>document.getElementById(q.id),numeric=s=>{const value=String(s).trim().replace(/−/g,'-').replace(',','.');return /^[-+]?\d*\.?\d+$/.test(value)?Number(value):null;};
 function sound(name){try{const api=parent.FIWA_SOUND||window.FIWA_SOUND;if(api)api.play(name);}catch(_){}}
 function message(text){if(result)result.textContent=text;}
 async function digest(value){if(!window.crypto||!crypto.subtle)throw Error('Peramban belum mendukung pemeriksaan ini.');const bytes=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(value));return Array.from(new Uint8Array(bytes),n=>n.toString(16).padStart(2,'0')).join('');}
 async function correct(q){const e=answerElement(q);if(!e||!e.value.trim())return false;
  if(q.hashes){const n=q.kind==='num'?numeric(e.value):e.value;if(n===null)return false;const token=q.kind==='num'?String(Math.round(n*(q.hashScale||config.hashScale))):String(n);return q.hashes.includes(await digest(config.salt+'|'+q.id+'|'+token));}
  if(q.kind==='choice')return String(q.answer)===e.value;
  const n=numeric(e.value);return n!==null&&Math.abs(n-Number(q.answer))<=Number(q.tol||.05);
 }
 function feedback(q,ok){const box=document.querySelector('[data-feedback="'+q.id+'"]');if(box){box.hidden=false;box.classList.toggle('wrong',!ok);box.querySelector('strong').textContent=ok?'Tepat. Periksa alasan dan satuannya.':'Bagian ini perlu ditinjau kembali.';const detail=box.querySelector('p');if(detail){detail.textContent=q.explain||'Periksa model, diagram, tanda dan satuan.';if(Array.isArray(q.steps)&&q.steps.length===7){detail.textContent='';const list=document.createElement('ol');list.className='solution-seven-list';q.steps.forEach(step=>{const li=document.createElement('li'),at=step.indexOf(':'),label=document.createElement('strong');label.textContent=at>=0?step.slice(0,at+1):'';li.append(label,document.createTextNode(' '+(at>=0?step.slice(at+1):step)));list.appendChild(li);});detail.appendChild(list);}}}const e=answerElement(q);if(e){e.setAttribute('aria-invalid',String(!ok));e.closest('.class-question').classList.toggle('needs-review',!ok);}}
 function focusQuestion(q){const e=answerElement(q),visible=e&&e.type==='hidden'?document.querySelector('[data-choice-for="'+q.id+'"]'):e;if(visible)visible.focus();}
 function lock(){if(!finish)return;finish.disabled=true;questions.forEach(q=>{const e=answerElement(q);if(e)e.disabled=true;document.querySelectorAll('[data-choice-for="'+q.id+'"]').forEach(r=>r.disabled=true);});}
 function readAnswers(){return Object.fromEntries(questions.map(q=>[q.id,answerElement(q).value]));}
 function report(score,extra={}){
  const payload={fims:score==null?'selesai':stage==='P5'?'usulan-cek':'skor',skor:score,versi:version,awal:first,stage,focus,branch:config.branch,session:config.session,form:config.form,elapsed:started?Math.round((Date.now()-started)/1000):0,...extra};
  if(window.FIMS_LEMBAR)window.FIMS_LEMBAR.lapor({selesai:done,skor:score});
  if(window.parent!==window)window.parent.postMessage(payload,location.origin);
 }
 async function grade(){
  if(submitted&&stage!=='P7'&&stage!=='P6'&&stage!=='P2'&&stage!=='L1'&&stage!=='L3-latihan')return;
  const empty=questions.find(q=>!answerElement(q)||!answerElement(q).value.trim());if(empty){message('Lengkapi semua jawaban sebelum mengirim.');focusQuestion(empty);return;}
  if(!started)started=Date.now();if(finish)finish.disabled=true;
  try{
   const flags=await Promise.all(questions.map(correct)),count=flags.filter(Boolean).length,score=Math.round(100*count/questions.length),wrong=questions.filter((_,i)=>!flags[i]);
   if(first===null)first=score;last=score;attempts++;submitted=true;done=['P5','P9','P10','L3'].includes(stage)||score>=Number(config.threshold||80);
   questions.forEach((q,i)=>feedback(q,flags[i]));sound(done?'complete':'wrong');
   const byIndicator={};wrong.forEach(q=>{byIndicator[q.indicator]=(byIndicator[q.indicator]||0)+1;});
   const main=Object.keys(byIndicator).sort((a,b)=>byIndicator[b]-byIndicator[a])[0];const proposedFocus=(config.indicators||[]).indexOf(main)+1;
   let text=count+' dari '+questions.length+' tepat ('+score+'%). Hasil percobaan mandiri pertama: '+first+'%. ';
   if(stage==='P5')text+='Hasil ini diajukan kepada guru. Skor P5 yang disahkan guru menentukan tindak lanjutmu.';
   else if(stage==='P9')text+='Jawaban uji ketuntasan sudah dikirim. Ikuti hasil dan langkah berikutnya pada panel P9.';
   else if(stage==='P10')text+='Sesi pengulangan selesai. Ikuti jadwal berikutnya pada P10.';
   else if(stage==='P6')text+=score===100?'Penguatan selesai. Lakukan cek ulang P5 bersama guru.':'Baca pembahasannya, lalu perbaiki bagian yang belum tepat.';
   else text+=done?'Persiapan memenuhi batas awal. Jelaskan kembali bagian yang sempat keliru.':'Pelajari umpan balik dan perbaiki jawabanmu.';
   message(text);
   if(['P5','P9','P10','L3'].includes(stage))lock();else if(finish)finish.disabled=false;
   report(score,{total:questions.length,benar:count,salah:questions.map((q,i)=>flags[i]?null:String(i+1)).filter(Boolean),diagnosis:byIndicator,fokus:Math.max(0,proposedFocus),answers:stage==='P10'?readAnswers():undefined});
  }catch(error){message(error.message||'Jawaban belum berhasil diperiksa. Coba lagi.');if(finish)finish.disabled=false;}
 }
 function updateClock(){const out=document.getElementById('class-clock-value');if(!out)return;const budget=Number(config.seconds||questions.reduce((n,q)=>n+Number(q.seconds||120),0)),elapsed=started?Math.floor((Date.now()-started)/1000):0,remaining=Math.max(0,budget-elapsed);out.textContent=Math.floor(remaining/60)+':'+String(remaining%60).padStart(2,'0');const box=out.closest('.class-clock');box.classList.toggle('late',elapsed>budget);if(elapsed>budget)document.getElementById('class-clock-label').textContent='Waktu rekomendasi sudah lewat; kamu tetap dapat menyelesaikan jawaban.';}
 function reveal(){const list=document.querySelector('.class-question-list');if(list)list.hidden=false;if(finish)finish.hidden=false;}
 const start=document.getElementById('class-start');if(start)start.addEventListener('click',()=>{if(!started)started=Date.now();start.disabled=true;start.textContent='Waktu pengerjaan berjalan';reveal();updateClock();if(window.FIMS_LEMBAR)window.FIMS_LEMBAR.lapor({selesai:false});});
 if(document.getElementById('class-clock-value')){updateClock();timer=setInterval(updateClock,1000);}
 document.addEventListener('input',event=>{if(event.target.closest('.class-question')&&!started)started=Date.now();});
 document.addEventListener('change',event=>{const id=event.target.dataset.choiceFor;if(id){document.getElementById(id).value=event.target.value;}});
 document.querySelectorAll('[data-check-one]').forEach(button=>button.addEventListener('click',async()=>{const id=button.dataset.checkOne,q=(config.checks||[]).find(q=>q.id===id),e=q&&answerElement(q);if(!q||!e||!e.value.trim()){message('Coba jawab checkpoint dahulu.');if(q)focusQuestion(q);return;}const ok=await correct(q);checked[id]=ok;feedback(q,ok);sound(ok?'correct':'wrong');const status=button.nextElementSibling;if(status)status.textContent=ok?'Checkpoint tepat. Hubungkan kembali dengan visual konsepnya.':'Tinjau kembali visual dan pembahasan, lalu coba kembali.';}));
 if(finish)finish.addEventListener('click',()=>{
  if(questions.length){grade();return;}
  if(stage==='P4'){
   const pending=(config.checks||[]).find(q=>!checked[q.id]);if(pending){message('Selesaikan seluruh checkpoint dengan tepat sebelum menyimpan penyelesaian konsep.');focusQuestion(pending);return;}
  }
  const required=Array.from(document.querySelectorAll('[data-required]')).find(e=>!e.value.trim());if(required){message('Lengkapi catatan atau bukti yang diminta sebelum mengirim.');required.focus();return;}
  done=true;submitted=true;sound('record');message(stage==='P8'?'Bukti penerapan terkirim. Guru akan menilai menggunakan rubrik.':'Penyelesaian tercatat. Lanjutkan kegiatan berikutnya pada panel kiri.');report(null);
 });
 window.FIMS_RINGKAS=()=>({selesai:done,skor:last,terisi:questions.length?questions.filter(q=>answerElement(q)&&answerElement(q).value.trim()).length:Array.from(document.querySelectorAll('[data-required]')).filter(e=>e.value.trim()).length,total:questions.length||document.querySelectorAll('[data-required]').length});
 window.FIMS_KEADAAN=()=>({version,first,last,attempts,done,submitted,started,checked,cycle,focus});
 window.FIMS_PULIHKAN=info=>{
  document.querySelectorAll('[data-physics-lab]').forEach(el=>{if(el.__fiwaRestore)el.__fiwaRestore();});
  [...questions,...(config.checks||[])].forEach(q=>{if(q.kind==='choice'){const e=answerElement(q);document.querySelectorAll('[data-choice-for="'+q.id+'"]').forEach(r=>r.checked=!!e&&r.value===e.value);}});
  const x=info&&info.x;if(!x||x.version!==version)return;
  if((['P5','P9','P10'].includes(stage)&&x.cycle!==cycle)||(stage==='P6'&&Number(x.focus||0)!==focus)){questions.forEach(q=>{const e=answerElement(q);if(e){e.value='';e.disabled=false;}document.querySelectorAll('[data-choice-for="'+q.id+'"]').forEach(r=>{r.checked=false;r.disabled=false;});});message('Kegiatan baru. Kerjakan tanpa membawa jawaban sesi sebelumnya.');return;}
  first=x.first;last=x.last;attempts=x.attempts||0;done=!!x.done;submitted=!!x.submitted;started=x.started||0;checked=x.checked||{};
  if(started){reveal();if(start){start.disabled=true;start.textContent='Waktu pengerjaan berjalan';}}
  if(submitted&&['P5','P9','P10','L3'].includes(stage))lock();
  if(last!=null)message('Hasil tersimpan: '+last+'%. Hasil mandiri pertama: '+first+'%.');
  updateClock();
 };
 document.querySelectorAll('[data-parent-route]').forEach(link=>{
  try{const bridge=window.parent.FIWA_COURSE,reason=bridge&&bridge.lockReason(link.dataset.tpSlug);if(reason){link.setAttribute('aria-disabled','true');link.removeAttribute('href');const note=document.createElement('small');note.textContent='Terkunci · '+reason;link.appendChild(note);}}
  catch(_){}
  link.addEventListener('click',event=>{if(link.getAttribute('aria-disabled')==='true'){event.preventDefault();return;}if(window.parent!==window){event.preventDefault();window.parent.location.hash=link.dataset.parentRoute;}});
 });
 window.addEventListener('pagehide',()=>{if(timer)clearInterval(timer);});
})();

document.querySelectorAll('.hook-option').forEach(button=>button.addEventListener('click',()=>{button.closest('.hook-try').querySelectorAll('.hook-option').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));}));
