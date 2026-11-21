/* Animasi dipicu siswa. Model gerak memakai waktu fisika; konstruksi vektor diberi label. */
(function(global){'use strict';
 const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),G=10;
 function energyPoints(p){const hm=Math.max(10,p.h0,p.h),floor=270,y0=floor-p.h0/hm*200,y=floor-p.h/hm*200;
  const down=p.shape==='ramp'?[[60,y0],[200,floor]]:p.shape==='wave'?[[60,y0],[90,y0+(floor-y0)*.12],[130,y0+(floor-y0)*.6],[165,y0+(floor-y0)*.76],[200,floor]]:[[60,y0],[115,y0+(floor-y0)*.2],[155,y0+(floor-y0)*.7],[200,floor]];
  const up=p.shape==='ramp'?[[400,floor],[575,y]]:[[400,floor],[475,floor+(y-floor)*.12],[530,floor+(y-floor)*.55],[575,y]];
  return {points:[...down,...up],hm};
 }
 function energySegments(p){const {points,hm}=energyPoints(p),segments=[];let velocity=Number(p.v0||0),time=0,rough=0;
  for(let i=1;i<points.length;i++){const A=points[i-1],B=points[i],flat=A[0]===200&&B[0]===400,dy=(B[1]-A[1])*hm/200,length=flat?p.s:Math.hypot(B[0]-A[0],B[1]-A[1])*hm/200;
   if(length<1e-9){segments.push({A,B,start:time,duration:0,length:0,rough,flat,v0:velocity,a:0});continue;}
   const a=G*dy/length-(flat&&p.mode==='friction'?p.mu*G:0),target=velocity*velocity+2*a*length;
   let reach=length;
   if(a<0&&target<0)reach=velocity*velocity/(-2*a);
   const endV=Math.sqrt(Math.max(0,velocity*velocity+2*a*reach));
   const duration=Math.abs(a)>1e-10?(endV-velocity)/a:velocity>1e-10?reach/velocity:0;
   if(duration===0&&reach>0&&velocity===0){segments.push({A,B:A,start:time,duration:0,length:0,rough,flat,v0:0,a:0});break;}
   const end=[A[0]+(B[0]-A[0])*reach/length,A[1]+(B[1]-A[1])*reach/length];
   segments.push({A,B:end,start:time,duration,length:reach,rough,flat,v0:velocity,a});time+=duration;if(flat)rough+=reach;velocity=endV;
   if(reach<length-1e-8)break;
  }return {segments,total:time,hm};
 }
 function duration(kind,p){if(kind==='energy')return energySegments(p).total||3;
  if(kind==='motion'||kind==='reaction')return Math.max(.1,p.t||3);
  if(kind==='incline')return Math.sin(p.theta*Math.PI/180)>1e-5?Math.sqrt(4/(G*Math.sin(p.theta*Math.PI/180))):4;
  if(kind==='workenergy'){const a=p.F/p.m,stop=a<0?p.v0*p.v0/(-2*a):Infinity,s=Math.min(p.s,stop),v=Math.sqrt(Math.max(0,p.v0*p.v0+2*a*s));return Math.abs(a)>1e-8?Math.max(.1,(v-p.v0)/a):p.v0>0?Math.max(.1,s/p.v0):3;}
  return 4;
 }
 function frame(kind,input,time){const p={...input},end=duration(kind,p),t=clamp(time,0,end),phase=clamp(t/end,0,1),options={phase,time:t,base:{...p}},params={...p};let note='';
  if(kind==='motion'||kind==='reaction'){params.t=t;note='Waktu fisika: '+t.toFixed(2)+' s.';}
  else if(kind==='work'){params.s=p.s*phase;options.workX=90+350*phase;note='Perpindahan diperagakan bertahap; usaha kumulatif mengikuti F s cos θ. Laju gambar bukan hasil gaya neto.';}
  else if(kind==='workenergy'){const a=p.F/p.m;params.s=Math.max(0,p.v0*t+.5*a*t*t);note='Waktu fisika: '+t.toFixed(2)+' s; gerak berhenti ketika energi kinetik habis.';}
  else if(kind==='kinetic'){options.kineticX=55+p.v*t*(180/(Math.max(15,p.v)*4));note='Gerak lurus dengan kelajuan tetap. Jarak sejak mulai: '+(p.v*t).toFixed(2)+' m; energi kinetik tetap.';}
  else if(kind==='potential'){params.h=p.ref+(p.h-p.ref)*(3*phase*phase-2*phase*phase*phase);note='Ilustrasi pemindahan perlahan dari acuan ke tinggi pilihan; bukan gerak jatuh bebas. Bandingkan perubahan Ep.';}
  else if(kind==='incline'){const acc=G*Math.sin(p.theta*Math.PI/180);options.inclineDistance=.5*acc*t*t;note='Benda dilepas dari diam pada bidang licin: a = g sin θ. Jarak turun '+options.inclineDistance.toFixed(2)+' m.';}
  else if(kind==='energy'){const model=energySegments(p);let seg=model.segments.find(s=>t<=s.start+s.duration+1e-9)||model.segments.at(-1);
   if(seg){const dt=clamp(t-seg.start,0,seg.duration),distance=clamp(seg.v0*dt+.5*seg.a*dt*dt,0,seg.length),f=seg.length>0?distance/seg.length:1;options.body=[seg.A[0]+(seg.B[0]-seg.A[0])*f,seg.A[1]+(seg.B[1]-seg.A[1])*f];params.h=(270-options.body[1])*model.hm/200;params.s=seg.rough+(seg.flat?distance:0);}
   note='Gerak mengikuti neraca energi di lintasan licin dan segmen kasar mendatar. Waktu fisika '+t.toFixed(2)+' s.';if(time>=end){const last=model.segments.at(-1),target=energyPoints(p).points.at(-1);note+=last&&Math.hypot(last.B[0]-target[0],last.B[1]-target[1])>1e-5?' Benda berhenti sebelum tujuan.':' Cuplikan berakhir di tujuan; kelajuan akhir ditampilkan, bukan otomatis nol.';}
  }else if(kind==='torque'||kind==='couple'){const tau=kind==='couple'?p.F*p.d:p.F*p.r*Math.sin(p.theta*Math.PI/180);options.turn=Math.abs(tau)<1e-8?0:phase*Math.sign(tau)*Math.PI*.65;note='Peragaan arah kecenderungan putar akibat momen. Laju putaran kualitatif; momen inersia tidak dimodelkan.';}
  else{options.construct=phase;note=kind==='cable'?'Konstruksi diagram gaya bertahap pada keadaan setimbang: benda tetap diam.':'Konstruksi vektor/proyeksi bertahap; animasi ini bukan gerak benda.';}
  return {params,options,note,done:time>=end,duration:end,time:t};
 }
 function mount(host){if(!host.__fiwaRender||host.dataset.animationMounted)return;host.dataset.animationMounted='1';
  const box=document.createElement('div');box.className='lab-playback';box.dataset.fimsAbaikan='';box.innerHTML='<div class="playback-buttons"><button type="button" data-play>▶ Play</button><button type="button" data-pause disabled>Ⅱ Pause</button><button type="button" data-stop>■ Stop</button><button type="button" data-reset>↺ Reset</button></div><label>Kecepatan tayang <select data-speed aria-label="Kecepatan tayang"><option value=".5">0,5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><output data-time>0,00 s</output><p data-motion-note role="status">Tekan Play untuk mengamati perubahan.</p>';
  host.querySelector('.lab-stage').before(box);const play=box.querySelector('[data-play]'),pause=box.querySelector('[data-pause]'),out=box.querySelector('[data-time]'),note=box.querySelector('[data-motion-note]');let elapsed=0,playing=false,last=0,raf=0;
  function render(){const cfg=host.__fiwaState(),view=frame(cfg.kind,cfg.params,elapsed);host.__fiwaRender(view.params,view.options);out.textContent=view.time.toFixed(2).replace('.',',')+' s';note.textContent=view.note+(view.done?' Animasi selesai.':'');return view;}
  function halt(){box.dataset.state='paused';playing=false;last=0;cancelAnimationFrame(raf);play.disabled=false;pause.disabled=true;}
  function tick(now){if(!host.isConnected){halt();return;}if(last)elapsed+=Math.min(.1,(now-last)/1000)*Number(box.querySelector('[data-speed]').value);last=now;const view=render();if(view.done){halt();return;}raf=requestAnimationFrame(tick);}
  play.addEventListener('click',()=>{const cfg=host.__fiwaState();if(elapsed>=duration(cfg.kind,cfg.params))elapsed=0;playing=true;box.dataset.state='playing';last=0;play.disabled=true;pause.disabled=false;raf=requestAnimationFrame(tick);});
  pause.addEventListener('click',()=>{halt();note.textContent='Animasi dijeda. Tekan Play untuk melanjutkan.';});
  box.querySelector('[data-stop]').addEventListener('click',()=>{halt();elapsed=0;render();note.textContent+=' Stop mengembalikan waktu ke awal, parameter pilihan tetap.';});
  box.querySelector('[data-reset]').addEventListener('click',()=>{halt();elapsed=0;host.querySelector('[data-lab-reset]').click();render();});
  host.addEventListener('input',e=>{if(e.target.closest('.lab-controls')){halt();elapsed=0;render();note.textContent='Parameter berubah. Tekan Play untuk menguji kondisi ini.';}});
  host.querySelector('[data-lab-reset]').addEventListener('click',()=>{halt();elapsed=0;render();out.textContent='0,00 s';});
  host.addEventListener('fiwa:lab-restored',()=>{halt();elapsed=0;render();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&playing)halt();});window.addEventListener('pagehide',halt);render();box.dataset.state='ready';
 }
 const api={frame,duration,energyPoints,energySegments,mount};if(typeof module!=='undefined'&&module.exports)module.exports=api;
 if(typeof document!=='undefined'){global.FIWA_ANIMATION=api;const start=()=>document.querySelectorAll('[data-physics-lab]').forEach(mount);document.addEventListener('fiwa:visual-ready',start);if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();}
})(typeof window!=='undefined'?window:globalThis);
