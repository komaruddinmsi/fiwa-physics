/* Skenario regresi progres lama, percabangan, dan kesiapan alur P. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),source=fs.readFileSync(path.join(root,'assets/app.js'),'utf8');
const listeners={},c={console,Date,URL,location:{hash:''},localStorage:{getItem:()=>null,setItem(){}},document:{addEventListener(e,fn){listeners[e]=fn},querySelector(){return null},querySelectorAll(){return []}},matchMedia:()=>({matches:true}),addEventListener(){},FIMS:{aku:{guru:false},modeGuru:()=>false,dorong(){}}};c.window=c;
vm.createContext(c);for(const f of ['alur-p.js','alur-p-data.js'])vm.runInContext(fs.readFileSync(path.join(root,'assets',f),'utf8'),c);
const tail=`globalThis.testP={setCatalog:v=>K=v,setDB:v=>db=v,cariTP,hitung,hitungP,kunci,langkah,catat,cabangS9,tahapSelesai,latihanSiap,T,navigasiTahapan};})();`;
vm.runInContext(source.slice(0,source.lastIndexOf("fetch('katalog.json').then"))+tail,c);
const p=c.testP;p.setCatalog(JSON.parse(fs.readFileSync(path.join(root,'katalog.json'),'utf8')));const tp=p.cariTP('f-use-1-pra');
let count=0;function check(name,fn){fn();count++;console.log('PASS '+name)}
function seed(score){const t=Date.now()-5*864e5;const v={ev:{S1:{waktu:t},S2:{skor:80,waktu:t},S3:{waktu:t},S4:{waktu:t},S5:{waktu:t},S6:{waktu:t},S7:{waktu:t}},tier:null,s14:[],riwayat:[]};if(score!==null)v.ev.S8={skor:score,waktu:t};p.setDB({tp:{[tp.slug]:v},opsi:{}});return v;}
for(const [score,branch] of [[null,null],[0,'b'],[59,'b'],[60,'a'],[79,'a'],[80,'skip'],[100,'skip']])check('P5 '+score+' routes to '+branch,()=>{seed(score);assert.equal(p.cabangS9(p.hitung(tp)),branch)});
check('No-score P6 cannot open for students',()=>{seed(null);assert.ok(p.kunci(tp,'S9',p.hitung(tp)))});
check('Failed P5 cannot open P7',()=>{seed(79);assert.ok(p.kunci(tp,'S11',p.hitung(tp)))});
check('P5 pass opens P7 and skips P6',()=>{seed(80);const h=p.hitung(tp);assert.equal(p.kunci(tp,'S11',h),null);assert.equal(p.tahapSelesai(tp,p.T('S9'),h),true);assert.equal(p.langkah(tp),'S11')});
check('P6 does not forge a P5 pass; queues a recheck',()=>{const d=seed(59);p.catat(tp,'S9',{skor:100,branch:'b',versi:2});assert.equal(d.ev.S8.skor,59);assert.equal(d.ev.S8.cekUlang,true);assert.equal(p.langkah(tp),'S8')});
check('Wrong completed branch is not reused after score changes',()=>{const d=seed(60);d.ev.S9={skor:100,cabang:'b'};assert.equal(p.tahapSelesai(tp,p.T('S9'),p.hitung(tp)),false)});
check('Changing the diagnosed concept requires the corresponding followup',()=>{const d=seed(60);d.ev.S8.fokus=2;d.ev.S9={skor:100,cabang:'a',fokus:1};assert.equal(p.tahapSelesai(tp,p.T('S9'),p.hitung(tp)),false)});
check('Teacher regrade clears pending flag',()=>{const d=seed(60);d.ev.S8.cekUlang=true;p.catat(tp,'S8',{skor:80});assert.equal(d.ev.S8.cekUlang,undefined);assert.equal(p.langkah(tp),'S11')});
check('Seven of ten new questions does not qualify',()=>{const d=seed(80);d.ev.S11={skor:70,versi:2,waktu:1};assert.equal(p.latihanSiap(d.ev),false);assert.ok(p.kunci(tp,'S12',p.hitung(tp)))});
check('Eight of ten new questions qualifies',()=>{const d=seed(80);d.ev.S11={skor:80,versi:2,waktu:1};assert.equal(p.latihanSiap(d.ev),true);assert.equal(p.kunci(tp,'S12',p.hitung(tp)),null)});
check('Legacy 75-percent result remains valid',()=>{const d=seed(80);d.ev.S11={skor:75,waktu:1};assert.equal(p.latihanSiap(d.ev),true)});
check('P8 T2 blocks P9 despite perfect practice',()=>{const d=seed(80);d.ev.S11={skor:100,versi:2,waktu:1};d.tier=2;assert.ok(p.kunci(tp,'S13',p.hitung(tp)))});
check('P9 waits two days',()=>{const d=seed(80);d.ev.S11={skor:80,versi:2,waktu:Date.now()};d.tier=3;assert.ok(p.kunci(tp,'S13',p.hitung(tp)))});
check('New mastery requires P7, P8 and P9',()=>{const d=seed(80);d.ev.S11={skor:80,versi:2,waktu:1};d.ev.S13={skor:80,waktu:3};d.tier=3;assert.equal(p.hitungP(d,tp).s,5)});
check('Old mastery is preserved',()=>{const d=seed(80);d.ev.S11={skor:75,waktu:1};d.ev.S13={skor:75,waktu:3};d.tier=3;assert.equal(p.hitungP(d,tp).s,5)});
check('Past review passes before a restart do not imply stable mastery',()=>{const d=seed(80);d.ev.S11={skor:80,versi:2,waktu:1};d.ev.S13={skor:80,waktu:3};d.tier=3;d.s14Mulai=10;d.s14=[{hasil:'lulus',waktu:4},{hasil:'lulus',waktu:5},{hasil:'lulus',waktu:6},{hasil:'lulus',waktu:11}];assert.equal(p.hitungP(d,tp).stabil,false)});
check('Ten public groups with P10 separate and no S10',()=>{seed(80);const h=p.hitung(tp),html=p.navigasiTahapan(tp,'S4',h);assert.equal((html.match(/class="step-number"/g)||[]).length,10);assert.ok(html.includes('study-review'));assert.ok(!html.includes('S10'));assert.equal(p.T('S10'),undefined);assert.equal(c.FIWA_ALUR.groups.length,10)});
check('Public labels preserve data keys in attributes',()=>{const s=c.FIWA_ALUR.html('<a href="#tp-f-use-1-pra-s11" data-stage="S11">S11</a>');assert.ok(s.includes('href="#tp-f-use-1-pra-p7"'));assert.ok(s.includes('data-stage="S11"'));assert.ok(s.includes('>P7</a>'))});
check('Canonical new route mapping',()=>{assert.equal(c.FIWA_ALUR.toOld['p10'],'S14');assert.equal(c.FIWA_ALUR.toOld['p4-praktik'],'S7');assert.equal(c.FIWA_ALUR.toOld['p2a'],'S2b')});
check('Manual grade of a new practice also uses the 80-percent criterion',()=>{const d=seed(80);p.catat(tp,'S11',{skor:75});assert.equal(d.ev.S11.versi,tp.tahapan.S11.versi);assert.equal(p.latihanSiap(d.ev),false)});
check('Failed spaced review restarts with the first interval',()=>{const d=seed(80);d.ev.S11={skor:80,versi:2,waktu:1};d.ev.S13={skor:80,waktu:3};d.tier=3;p.catat(tp,'S14',{skor:50});assert.ok(d.s14Mulai>d.s14[0].waktu);assert.equal(p.hitungP(d,tp).stabil,false)});
console.log(JSON.stringify({passed:count}));
