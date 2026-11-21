/* Basis data SQLite sementara di memori; tidak menghubungi Cloudflare. Node 24+. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {DatabaseSync}=require('node:sqlite');
const ROOT=path.resolve(__dirname,'..');
async function setup(){
 const sql=new DatabaseSync(':memory:');sql.exec(fs.readFileSync(path.join(ROOT,'skema.sql'),'utf8'));sql.exec('ALTER TABLE progres ADD COLUMN oleh TEXT');
 const DB={prepare(text){let values=[];return {bind(...v){values=v;return this;},async first(){return sql.prepare(text).get(...values)||null;},async all(){return {results:sql.prepare(text).all(...values)};},async run(){const r=sql.prepare(text).run(...values);return {meta:{changes:Number(r.changes)}};}};},async batch(items){sql.exec('BEGIN');try{const r=[];for(const x of items)r.push(await x.run());sql.exec('COMMIT');return r;}catch(e){sql.exec('ROLLBACK');throw e;}}};
 for(const [email,peran,nama] of [['siswa@example.test','siswa','Siswa Uji'],['guru@example.test','guru','Guru Uji'],['asing@example.test','guru','Guru Lain']])sql.prepare('INSERT INTO anggota(email,peran,nama,status,dibuat)VALUES(?,?,?,\'aktif\',0)').run(email,peran,nama);
 sql.prepare('INSERT INTO bimbing(guru,murid,dibuat)VALUES(?,?,0)').run('guru@example.test','siswa@example.test');
 const module=await import('data:text/javascript;base64,'+Buffer.from(fs.readFileSync(path.join(ROOT,'functions/api/[[rute]].js'),'utf8')).toString('base64'));
 const env={DB,RAHASIA:'lokal-fiktif-tidak-untuk-produksi'};const cookies={};for(const who of ['siswa','guru','asing'])cookies[who]='fims_sesi='+encodeURIComponent(await module.buatSesi(who+'@example.test',who==='siswa'?'siswa':'guru',env.RAHASIA));
 // Cookie name follows the real module (avoid assuming an older application name).
 const cookieName=fs.readFileSync(path.join(ROOT,'functions/api/[[rute]].js'),'utf8').match(/const NAMA_KUKI\s*=\s*'([^']+)'/)[1];for(const who in cookies)cookies[who]=cookies[who].replace('fims_sesi=',cookieName+'=');
 function seed(slug,patch={}){const d={ev:Object.fromEntries(['S1','S2','S3','S4','S5','S6','S7'].map(x=>[x,{skor:100,waktu:Date.now(),versi:4}])),tier:null,s14:[],riwayat:[],...patch};sql.prepare('INSERT OR REPLACE INTO progres(email,tp,data,diubah)VALUES(?,?,?,0)').run('siswa@example.test',slug,JSON.stringify(d));return d;}
 async function call(route,body,who='siswa',method=body?'POST':'GET'){const request=new Request('http://localhost/api/'+route,{method,headers:{cookie:cookies[who]||'','content-type':'application/json'},...(body?{body:JSON.stringify(body)}:{})});const response=await module.onRequest({request,env,params:{rute:route.split('?')[0].split('/')}});return {status:response.status,data:await response.json()};}
 return {sql,DB,module,env,cookies,seed,call};
}
async function test(){const h=await setup(),{call,seed,sql}=h;let checks=0;const ok=(condition,label)=>{assert(condition,label);checks++;};
 const gates=JSON.parse(fs.readFileSync(path.join(ROOT,'alat/bank/gating_contract.json'),'utf8')),units=JSON.parse(fs.readFileSync(path.join(ROOT,'alat/bank/unit_contract.json'),'utf8'));
 for(const [slug,c] of Object.entries(gates)){
  seed(slug);let r=await call('gating?tp='+slug);ok(r.status===200&&r.data.state.current.id===c.gates[0].id,'First gate');ok(!JSON.stringify(r.data).includes(c.gates[1].prompt),'Future prompt hidden');
  let skip=await call('gating/jawab',{tp:slug,gate:c.gates[1].id,revision:0,answer:'Bukti mencoba melompat'});ok(skip.status===409,'Cannot skip gate');
  for(const [i,g] of c.gates.entries()){
   r=await call('gating?tp='+slug);let rev=r.data.state.revision;
   r=await call('gating/jawab',{tp:slug,gate:g.id,revision:rev,answer:'Jawaban, persamaan, substitusi dan alasan siswa.'});ok(r.status===200&&r.data.state.current.pending,'Pending teacher');rev=r.data.state.revision;
   ok((await call('guru/gating',{murid:'siswa@example.test',tp:slug,gate:g.id,revision:rev,tier:3,feedback:'Alasan sudah sesuai.'},'asing')).status===403,'Unassigned teacher');
   const queue=await call('guru/antrean',null,'guru');ok(queue.data.antrean.some(x=>x.tp===slug&&x.gate===g.id&&x.answer),'Evidence in queue');
   if(i===0){
    r=await call('guru/gating',{murid:'siswa@example.test',tp:slug,gate:g.id,revision:rev,tier:2,feedback:'Perbaiki model dan alasan.'},'guru');ok(r.status===200,'T2 feedback');
    r=await call('gating?tp='+slug);ok(r.data.state.current.id===g.id&&!r.data.state.current.pending,'T2 keeps same gate');
    r=await call('gating/jawab',{tp:slug,gate:g.id,revision:r.data.state.revision,answer:'Perbaikan model dan bukti baru sesuai umpan balik.'});rev=r.data.state.revision;
   }
   ok((await call('guru/gating',{murid:'siswa@example.test',tp:slug,gate:g.id,revision:rev-1,tier:3,feedback:'Versi usang harus ditolak.'},'guru')).status===409,'Stale revision');
   r=await call('guru/gating',{murid:'siswa@example.test',tp:slug,gate:g.id,revision:rev,tier:i===2?4:3,feedback:'Model, data dan kesimpulan sudah tepat.'},'guru');ok(r.status===200,'Teacher T3/T4');
  }
  r=await call('gating?tp='+slug);ok(r.data.state.complete&&r.data.data.ev.S8.skor===80,'All three gate pass');
  const before=r.data.data;
  await call('progres',{tp:{[slug]:{...before,gating4:{revision:999,items:{}},ev:{...before.ev,S8:{skor:100,versi:4}}}}},'siswa','PUT');
  r=await call('gating?tp='+slug);ok(r.data.data.ev.S8.skor===80&&r.data.state.complete,'Student cannot forge server gate');
  r=await call('guru/reset',{murid:'siswa@example.test',tp:slug,tahapan:'S8',alasan:'Uji ulang lokal'},'guru');ok(r.status===200,'Teacher reset');
  r=await call('gating?tp='+slug);ok(!r.data.state.complete&&r.data.state.current.id===c.gates[0].id,'Reset restarts first gate');
 }
 for(const [topik,c] of Object.entries(units)){
  ok((await call('unit?topik='+topik+'&mode=real')).status===403,'Real locked at API');
  let r=await call('unit?topik='+topik+'&mode=practice');ok(r.data.questions.length===25&&!('correct'in r.data.questions[0]),'Practice 25 without keys');
  ok((await call('unit/kirim',{topik,mode:'practice',answers:{}})).status===400,'Incomplete rejected');
  await call('progres',{tp:{['unit-'+topik]:{unit4:{practice:{done:true}}}}},'siswa','PUT');ok((await call('unit?topik='+topik+'&mode=real')).status===403,'Forged practice rejected');
  for(const q of c.practice){const r=await call('unit/periksa',{topik,mode:'practice',no:q.no,answer:q.correct});ok(r.status===200&&r.data.point===1&&r.data.pembahasan.match(/<li>/g).length===7,'Practice key and seven steps');}
  const answers=Object.fromEntries(c.practice.map(q=>[q.no,q.correct]));r=await call('unit/kirim',{topik,mode:'practice',answers});ok(r.status===200&&r.data.practiceComplete&&r.data.result.score===100,'Practice complete opens real');
  r=await call('unit?topik='+topik+'&mode=real');ok(r.status===200&&r.data.questions.length===25&&!r.data.review.length,'Real opens without review');
  ok((await call('unit/periksa',{topik,mode:'real',no:1,answer:c.real[0].correct})).status===403,'Real cannot check answer');
  for(let i=0;i<25;i++)ok(c.practice[i].stimulus!==c.real[i].stimulus&&c.practice[i].stem!==c.real[i].stem,'Different wording paired method');
  r=await call('unit/kirim',{topik,mode:'real',answers:Object.fromEntries(c.real.map(q=>[q.no,q.correct]))});ok(r.status===200&&r.data.result.score===100&&r.data.review.length===25,'Real server grade');
  r=await call('unit?topik='+topik+'&mode=real');ok(r.data.review.length===25,'Review persists on reload');
 }
 seed('f-mek-1-pra',{ev:{}});ok((await call('gating?tp=f-mek-1-pra')).status===403,'Prerequisites enforced');ok((await call('unit?topik=f-mek','',null)).status===401,'Anonymous cannot get question');
 console.log(JSON.stringify({checks,result:'PASS',storage:'SQLite in memory',production:false}));sql.close();
}
module.exports={setup};if(require.main===module)test().catch(e=>{console.error(e);process.exitCode=1;});
