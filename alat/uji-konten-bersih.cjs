/* Memastikan penghapusan HTML lama tidak merusak katalog, rute, atau penjagaan akun. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),source=fs.readFileSync(path.join(root,'functions/_middleware.js'),'utf8');
const c={URL,Request,Response,TextEncoder,TextDecoder,btoa,atob,crypto:require('node:crypto').webcrypto};vm.createContext(c);
vm.runInContext(source.replace(/\bexport\s+(?=(?:async\s+)?function)/g,'')+'\nglobalThis.test={ruteKontenLama,onRequest};',c);
let checks=0;const catalog=JSON.parse(fs.readFileSync(path.join(root,'katalog.json'),'utf8'));
function paths(obj){if(!obj||typeof obj!=='object')return;if(obj.berkas){assert.ok(fs.existsSync(path.join(root,obj.berkas)),obj.berkas);checks++;}Object.values(obj).forEach(paths)}paths(catalog);
const tps=catalog.topik.flatMap(t=>t.tp.map(tp=>({topic:t.slug,slug:tp.slug})));
const map={S1:'p1',S2:'p2',S2b:'p2a',S2c:'p2b',S3:'p3',S4:'p4',S5:'p4-diskusi',S6:'p4-contoh',S7:'p4-praktik',S8:'p5',S9:'p6',S10:'p1',S11:'p7',S12:'p8',S13:'p9',S14:'p10'};
async function redirects(route,expected){const res=await c.test.onRequest({request:new Request('https://fiwa.test'+route),env:{},next:()=>{throw Error('Rute lama tidak dialihkan: '+route)}});assert.equal(res.status,302);assert.equal(res.headers.get('location'),'https://fiwa.test/#'+expected);assert.equal(res.headers.get('cache-control'),'no-store');checks++;}
(async()=>{
 for(const t of tps)for(const [old,now] of Object.entries(map)){
  const base='/konten/'+t.topic+'/'+t.slug+'/'+old;
  assert.ok(!fs.existsSync(path.join(root,base.slice(1))),base+' masih ada');
  for(const suffix of ['', '/', '/index.html'])await redirects(base+suffix,'tp-'+t.slug+'-'+now);
 }
 for(const t of tps)for(const form of [2,3,4])await redirects('/konten/'+t.topic+'/'+t.slug+'/P5/form-'+form+'.html','tp-'+t.slug+'-p5');
 for(const topic of ['f-mek','f-use'])for(const id of ['L1','L2','L3','L4']){
  const base='/konten/'+topic+'/'+id;for(const suffix of ['', '/', '/index.html'])await redirects(base+suffix,'topik-'+topic+'-'+id.toLowerCase());
  if(id==='L3')await redirects(base+'/latihan.html','topik-'+topic+'-l3-latihan');
 }
 for(const route of ['/konten/f-mek/L1/interaktif.html','/konten/f-use/L3/latihan-interaktif.html','/konten/f-use/f-use-1-pra/P4/index.html','/konten/asing/tp/S1/index.html','/konten/f-use/f-use-1-pra/S99/index.html','/media-f-use/media.json','/']){
  assert.equal(c.test.ruteKontenLama(route),null);const res=await c.test.onRequest({request:new Request('https://fiwa.test'+route),env:{},next:()=>new Response('aktif')});assert.equal(res.status,200);checks++;
 }
 const denied=await c.test.onRequest({request:new Request('https://fiwa.test/konten/f-use/f-use-1-pra/P4/index.html'),env:{DB:{},RAHASIA:'test'},next:()=>{throw Error('Materi aktif tanpa sesi tidak boleh terbuka')}});assert.equal(denied.status,401);checks++;
 console.log(JSON.stringify({checks,result:'PASS'}));
})().catch(e=>{console.error(e);process.exitCode=1});
