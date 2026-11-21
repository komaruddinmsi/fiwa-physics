/* Perayaan memakai perubahan kunci, bukan navigasi/penambahan skor palsu. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {tracker,mount,DURATION}=require('../assets/teman-belajar.js');
let checks=0;function ok(value,label){assert(value,label);checks++;}
const item=id=>({key:id,label:id});const t=tracker();
ok(t.observe('a',[item('P1'),item('P2')]).length===0,'First visit silent');
ok(t.observe('a',[item('P1'),item('P2')]).length===0,'Navigation silent');
ok(t.observe('a',[item('P1'),item('P2'),item('P3')])[0].key==='P3','Newly available stage');
ok(t.observe('a',[item('P1'),item('P2'),item('P3')]).length===0,'No replay from polling');
ok(t.observe('b',[item('P1')]).length===0,'Other account gets own baseline');
ok(t.observe(null,[item('P9')]).length===0,'Teacher/guest cannot celebrate');
ok(t.observe('a',[item('P1')]).length===0,'Reset is not a gain');
ok(t.observe('a',[item('P1'),item('P2')])[0].key==='P2','Re-earned stage works');
ok(tracker().observe('a',[item('P1'),item('P2')]).length===0,'Reload adopts existing access silently');

// Minimal DOM records real lifecycle effects and lets us advance the 15 s clock.
function fixture(){
 let persisted={},click,visibility,owl,now=0,next=0;const timers=new Map(),events={};
 const classes=new Set(),label={textContent:''},attrs={},button={querySelector:()=>label,setAttribute:(k,v)=>attrs[k]=v};
 const frame={draft:'jawaban belum dikirim',position:371};
 const rail={hidden:false,getBoundingClientRect:()=>({left:30,top:150,width:292,height:640})};
 const controls={...button,getBoundingClientRect:()=>({left:30,top:110,width:220,height:44})};
 const layout={classList:{toggle(k,b){b?classes.add(k):classes.delete(k)}}};
 const media={matches:false,addEventListener(){}};
 const doc={hidden:false,documentElement:{lang:'id'},currentScript:{src:'http://local.test/assets/teman-belajar.js'},
  querySelector(s){return s==='.study-layout'?layout:s==='.study-rail'?rail:s==='[data-study-panel]'?controls:s==='.bar'?{getBoundingClientRect:()=>({bottom:82})}:null},
  createElement(){const b={setAttribute(k,v){this[k]=v},addEventListener(k,fn){this[k]=fn}};const caption={};return {style:{setProperty(){}},classList:{toggle(){}},querySelector:s=>s==='button'?b:caption,remove(){owl=null},get b(){return b},get caption(){return caption}};},
  body:{appendChild(v){owl=v}},addEventListener(k,fn){if(k==='click')click=fn;if(k==='visibilitychange')visibility=fn}
 };
 const win={document:doc,location:{href:'http://local.test/',hash:'#tp-test-p3'},innerWidth:1280,innerHeight:900,
  localStorage:{getItem:k=>persisted[k]||null,setItem:(k,v)=>persisted[k]=v},matchMedia:()=>media,
  addEventListener:(k,fn)=>events[k]=fn,setTimeout(fn,ms){const id=++next;timers.set(id,{fn,time:now+ms});return id},clearTimeout:id=>timers.delete(id)};
 const api=mount(win),sync=(entries,account='a')=>api.sync({account,entries:entries.map(item)});
 return {api,sync,frame,rail,attrs,classes,controls,media,doc,get owl(){return owl},get timers(){return timers},
  toggle(){click({target:{closest:()=>controls}})},hideTab(){doc.hidden=true;visibility()},route(){win.location.hash='#tp-test-p4';events.hashchange()},
  tick(ms){now+=ms;for(const [id,x]of timers)if(x.time<=now){timers.delete(id);x.fn()}}
 };
}
let f=fixture();f.sync(['P1']);f.sync(['P1','P2']);ok(!!f.owl,'Owl appears for gain');
ok(f.owl.innerHTML.includes('http://local.test/assets/logo.png'),'Uses actual site logo');
ok(f.timers.size===1&&[...f.timers.values()][0].time===DURATION,'Exactly 15 second lifetime');
f.tick(8000);f.sync(['P1','P2','P3']);ok(f.timers.size===1,'Simultaneous gains do not stack timers');
f.tick(6999);ok(!!f.owl,'Still visible before 15 seconds');f.tick(1);ok(!f.owl,'Dismisses at 15 seconds without extending');
f.sync(['P1']);f.sync(['P1','P2']);f.owl.b.click();ok(!f.owl&&f.timers.size===0,'Click cancels owl and timer');
f.sync(['P1']);f.media.matches=true;f.sync(['P1','P2']);ok(f.owl.className.includes('reduced-motion'),'Reduced motion gets still owl');
f.toggle();ok(f.rail.hidden&&f.classes.has('is-rail-hidden')&&f.attrs['aria-expanded']==='false','Full panel collapses');
ok(f.frame.draft==='jawaban belum dikirim'&&f.frame.position===371,'Draft and iframe are untouched');
f.toggle();ok(!f.rail.hidden&&!f.classes.has('is-rail-hidden')&&f.attrs['aria-expanded']==='true','Full panel restores');
f.hideTab();ok(!f.owl&&f.timers.size===0,'Background dismisses owl');
f=fixture();f.sync(['P1']);f.sync(['P1','P2']);f.route();ok(!f.owl,'Navigation dismisses owl');
f.sync(['P1']);f.sync(['P1','P2']);f.sync([],null);ok(!f.owl,'Teacher/logout dismisses owl');
// Test actual app locks with the real curriculum, including teacher T3 and due dates.
const vm=require('node:vm'),root=path.resolve(__dirname,'..'),src=fs.readFileSync(path.join(root,'assets/app.js'),'utf8');
(async()=>{let state;const c={console,Date,URL,location:{hash:''},localStorage:{getItem:()=>null,setItem(){}},FIWA_SOUND:{},FIWA_STUDY:{sync:s=>state=s},setInterval(){},
 document:{currentScript:{src:'https://local.test/assets/app.js'},styleSheets:['alur-p.css','tema.css','teman-belajar.css'].map(x=>({href:'https://local.test/assets/'+x})),querySelector(){return null},querySelectorAll(){return []},addEventListener(){}},
 FIMS:{aku:{email:'siswa@test',peran:'siswa',guru:false},modeGuru:()=>false,dorong(){}},addEventListener(){},matchMedia:()=>({matches:true})};c.window=c;vm.createContext(c);
 for(const file of ['alur-p.js','alur-p-data.js'])vm.runInContext(fs.readFileSync(path.join(root,'assets',file),'utf8'),c);
 const tail='globalThis.test={setDB:v=>db=v,setK:v=>K=v,segarkanTemanBelajar};})();';
 vm.runInContext(src.slice(0,src.lastIndexOf("fetch('katalog.json').then"))+tail,c);await new Promise(setImmediate);
 c.test.setK(JSON.parse(fs.readFileSync(path.join(root,'katalog.json'),'utf8')));
 const tr=tracker();const d={ev:{},tier:null,s14:[],riwayat:[]};c.test.setDB({tp:{'f-mek-1-pra':d},opsi:{}});
 const run=()=>{c.test.segarkanTemanBelajar();return tr.observe(state.account,state.entries)};run();
 d.ev.S2={skor:40,waktu:1};ok(run().length===0,'Failed prerequisites do not celebrate remediation');
 d.ev.S2.skor=80;ok(run().some(x=>x.key==='f-mek-1-pra:S3'),'Passed prerequisites unlock P3');
 d.ev.S3={waktu:1};ok(run().some(x=>x.key==='f-mek-1-pra:S5'),'P4 discussion unlock');
 for(const id of ['S4','S5','S6','S7'])d.ev[id]={waktu:1};run();
 d.ev.S8={skor:80,waktu:1};let gains=run();ok(gains.some(x=>x.key==='f-mek-1-pra:S11')&&!gains.some(x=>x.key==='f-mek-1-pra:S9'),'Teacher pass unlocks P7 and skips P6');
 d.ev.S11={skor:80,versi:4,waktu:Date.now()-3*864e5};run();d.tier=2;ok(run().length===0,'T2 cannot open P9');
 d.tier=3;ok(run().some(x=>x.key==='f-mek-1-pra:S13'),'T3 opens due P9');
 c.FIMS.aku={email:'guru@test',peran:'guru',guru:true};c.test.segarkanTemanBelajar();ok(state.account===null&&state.entries.length===0,'Teacher preview has no celebration');
 console.log(JSON.stringify({checks,result:'PASS',production:false}));
})().catch(e=>{console.error(e);process.exitCode=1});
