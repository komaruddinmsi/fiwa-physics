/* Menjalankan runtime siswa yang sesungguhnya dalam DOM kecil yang terkontrol. */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),{webcrypto}=require('node:crypto');
const source=fs.readFileSync(require('node:path').join(__dirname,'../assets/kelas-konten.js'),'utf8');
const tick=()=>new Promise(r=>setImmediate(r));let checks=0;
function fixture(stage,questions,extra={}){
 const els={},events={},messages=[],saved=[],intervals=[];let time=1000;
 const cls=()=>({add(){},toggle(){}});
 const element=id=>els[id]||(els[id]={id,value:'',textContent:'',hidden:false,disabled:false,dataset:{},classList:cls(),listeners:{},addEventListener(n,f){this.listeners[n]=f},setAttribute(k,v){this[k]=v},focus(){this.focused=true},closest(){return {classList:cls()}},querySelector(){return element(id+'-text')}});
 for(const q of [...questions,...(extra.checks||[])]){element(q.id);if(q.kind==='choice')for(let i=0;i<3;i++)element(q.id+'-opt-'+i);}
 const cfg={stage,questions,version:3,threshold:80,...extra};const finish=element('class-submit'),clock=element('class-clock-value'),start=element('class-start'),result=element('class-result');
 const doc={querySelector(s){if(s==='.class-question-list')return element('list');if(s==='[data-required]')return null;if(s.startsWith('[data-feedback=')){const id=s.match(/"(.*?)"/)[1];return element('feedback-'+id)}return null},getElementById:element,querySelectorAll(s){if(s.startsWith('[data-choice-for=')){const id=s.match(/"(.*?)"/)[1];return [0,1,2].map(i=>element(id+'-opt-'+i))}if(s==='[data-check-one]')return (extra.checks||[]).map(q=>{const b=element('check-'+q.id);b.dataset.checkOne=q.id;b.nextElementSibling=element('status-'+q.id);return b});return []},addEventListener(n,f){events[n]=f}};
 const c={console,URL,TextEncoder,crypto:webcrypto,location:{href:'http://localhost/lesson.html?cycle=1',origin:'http://localhost'},document:doc,setInterval(f){intervals.push(f);return 1},clearInterval(){},Date:{now:()=>time},FIWA_CLASS:cfg,FIMS_LEMBAR:{lapor:x=>saved.push(x)},parent:{postMessage:x=>messages.push(x)}};c.window=c;c.addEventListener=()=>{};vm.createContext(c);vm.runInContext(source,c);
 async function click(el){el.listeners.click();for(let i=0;i<20;i++){await tick();if(!finish.disabled||messages.length)break;}}
 return {c,els,messages,saved,finish,result,start,clock,events,click,intervals,setTime:t=>time=t,element};
}
(async()=>{
 const qs=[{id:'n',kind:'num',answer:2.5,tol:.01,indicator:'a',seconds:180,explain:'Penjelasan model.'},{id:'c',kind:'choice',answer:0,indicator:'b',seconds:120,explain:'Alasan konsep.'}];
 let f=fixture('P7',qs);await f.click(f.finish);assert.equal(f.messages.length,0);assert.ok(f.result.textContent.includes('Lengkapi'));checks++;
 f.els.n.value='2,5';f.els.c.value='0';await f.click(f.finish);assert.equal(f.messages[0].skor,100);assert.equal(f.messages[0].awal,100);checks++;
 f.els.n.value='−1';await f.click(f.finish);assert.equal(f.messages.at(-1).skor,50);assert.equal(f.messages.at(-1).awal,100);checks++;
 const state=f.c.FIMS_KEADAAN();const restored=fixture('P7',qs);restored.els.n.value='−1';restored.els.c.value='0';restored.c.FIMS_PULIHKAN({x:state});assert.equal(restored.c.FIMS_KEADAAN().last,50);assert.equal(restored.c.FIMS_KEADAAN().first,100);checks++;
 f=fixture('P5',qs,{indicators:['a','b'],seconds:300});f.els.n.value='0';f.els.c.value='0';await f.click(f.start);f.setTime(1000000);f.intervals.forEach(fn=>fn());assert.equal(f.clock.textContent,'0:00');await f.click(f.finish);assert.equal(f.messages[0].fims,'usulan-cek');assert.equal(f.messages[0].fokus,1);assert.equal(f.finish.disabled,true);assert.equal(f.els.n.disabled,true);checks++;
 f=fixture('P6',qs,{branch:'a',threshold:100});f.els.n.value='0';f.els.c.value='0';await f.click(f.finish);assert.equal(f.c.FIMS_KEADAAN().done,false);f.els.n.value='2.5';await f.click(f.finish);assert.equal(f.c.FIMS_KEADAAN().done,true);checks++;
 f=fixture('P4',[],{checks:qs});await f.click(f.finish);assert.equal(f.messages.length,0);for(const q of qs){f.element(q.id).value=String(q.answer);await f.click(f.element('check-'+q.id));}await f.click(f.finish);assert.equal(f.messages.at(-1).fims,'selesai');checks++;
 const salt='test',id='hash',hash=await webcrypto.subtle.digest('SHA-256',new TextEncoder().encode(salt+'|'+id+'|250'));
 f=fixture('P9',[{id,kind:'num',indicator:'a',hashScale:100,hashes:[Buffer.from(hash).toString('hex')],seconds:180}],{salt});f.els.hash.value='2,5';await f.click(f.finish);for(let i=0;i<30&&!f.messages.length;i++)await tick();assert.equal(f.messages[0].skor,100);assert.equal(f.finish.disabled,true);checks++;
 console.log(JSON.stringify({checks,result:'PASS'}));
})().catch(e=>{console.error(e);process.exitCode=1});
