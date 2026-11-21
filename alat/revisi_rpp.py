"""Penerapan standar RPP/visual/gating versi 4. Referensi dibaca sebagai data."""
from pathlib import Path
import sys,copy,json,importlib.util,re,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'alat/bank'))
LABELS=['Apa yang ditanyakan','Formulasi yang digunakan','Informasi distraktor (tidak diperlukan)','Identifikasi data','Substitusi nilai ke formula','Penyelesaian','Kesimpulan jawaban']
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'alat/bank'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def prose(s):
 s=str(s);s=re.sub(r'(?<=[a-z])(?=\d)',' ',s);s=re.sub(r'(?<=\d)(?=[A-Za-zμ])',' ',s);return s
def clean_prompt(s):
 s=re.sub(r'(Papan (?:siap|mini)[,.]?\s*)|(?:[Tt]iga puluh detik[.!]?)|(?:30 detik[.!]?)|(?:Angkat[.!]?)','',str(s))
 return re.sub(r'\s+',' ',s).strip(' »“”".,…')
def seven(q,formula='Gunakan model dan arah yang dinyatakan pada soal.'):
 if len(q.get('steps',[]))==7:
  return [label+': '+re.sub(r'^[^:]{1,65}:\s*','',str(text)) for label,text in zip(LABELS,q['steps'])]
 explanation=q.get('explain','');parts=re.split(r'(?<=[.!])\s+',explanation);data=', '.join(re.findall(r'[-−]?\d+(?:[.,]\d+)?\s*(?:kg|kN|N|m/s²|m/s|m|s|J|°)?',q['prompt']))
 answer=(q.get('options')or[])[q['answer']] if q['kind']=='choice' else str(round(float(q['answer']),5))+' '+q.get('unit','')
 return [LABELS[0]+': '+q.get('label','Jawaban')+' pada kasus yang ditanyakan.',LABELS[1]+': '+formula,LABELS[2]+': Tidak ada informasi tambahan yang perlu dibuang pada butir ini. Semua acuan arah tetap harus diperiksa.',LABELS[3]+': '+(data or q['prompt']),LABELS[4]+': '+parts[0],LABELS[5]+': '+explanation,LABELS[6]+': '+answer]
def rpp_newton(slug,lesson,provider):
 path=ROOT/'alat/bank/gating_rpp.json';source=json.loads(path.read_text(encoding='utf8'));gates=source[slug]
 qs=provider(slug,'P7',1);worked=[]
 for c in lesson['concepts']:
  q=next(q for q in qs if q['indicator']==c['id']);worked.append({'scenario':q['prompt']+(' Pilihan: '+' | '.join(q['options']) if q['kind']=='choice' else ''),'steps':seven(q,c['formula']),'result':q['explain']})
 return {'gates':gates,'worked':worked,'hook':{**lesson['hook'],'options':['Prediksi pertama: keadaan tetap seperti semula.','Prediksi kedua: perubahan bergantung pada resultan dan letak gaya.','Saya perlu mengamati model sebelum memutuskan.']},'summary':{'bigidea':lesson['goals'][0],'rows':[{'title':c['title'],'formula':c['formula'],'meaning':c['explain'][0],'trap':c['misconception']['claim']}for c in lesson['concepts']],'transfer':'Pilih sistem dan acuan terlebih dahulu, lalu hubungkan data, persamaan dan alasan.','checklist':lesson['goals']}}
ALIGN={}
def align_sources(lessons,providers):
 global ALIGN
 energy=load('alignment_energi');vg=load('alignment_vektor_gerak');newton=load('alignment_newton_statika');vectorq=load('alignment_vector_questions')
 ALIGN={**energy.ALIGNMENT,**vg.ALIGNMENT}
 for slug in ['f-mek-1a','f-mek-1b']:ALIGN[slug]=rpp_newton(slug,lessons[slug],newton.make_questions)
 old_providers=dict(providers)
 for slug,lesson in lessons.items():
  data=ALIGN[slug];lesson['hook']=copy.deepcopy(data['hook']);lesson['summary']=data['summary'];lesson['rpp_gates']=data['gates']
  for ci,(c,w) in enumerate(zip(lesson['concepts'],data['worked'])):
   c['worked']=copy.deepcopy(w)
   if slug in ('f-mek-1a','f-mek-1b'):
    from kegiatan_unik import make as unique_case
    q=unique_case(slug,c,ci,'concept');c['worked']={'scenario':q['prompt'],'steps':q['steps'],'result':q['explain']}

  base=old_providers[slug];fresh=energy.make_questions if slug.startswith('f-use') else newton.make_questions if slug in ('f-mek-1a','f-mek-1b') else vectorq.make_questions
  def make(slug,stage,form=1,base=base,fresh=fresh,lesson=lesson):
   qs=copy.deepcopy(fresh(slug,stage,form) if stage in ('P7','P9') else base(slug,stage,form))
   for q in qs:
    q['indicator']={'vektor-resultan':'vektor-sambung','gerak-sumber':'gerak-pemberi'}.get(q['indicator'],q['indicator'])
    if stage=='P2':q['prerequisite']=True;q['seconds']=30 if q.get('level')=='C1' else 60 if len(q['prompt'])<220 and q.get('level') in ('C2','C3') else 90 if q.get('level')=='C3' else 120
    c=next((c for c in lesson['concepts'] if c['id']==q['indicator']),lesson['concepts'][0]);q['steps']=seven(q,c['formula'])
    for key in ['prompt','explain','label']:q[key]=prose(q.get(key,''))
    q['steps']=[prose(x)for x in q['steps']]
   return qs
  providers[slug]=make
  for c in lesson['concepts']:
   for q in c['checks']:q['steps']=seven(q,c['formula'])
 return lessons,providers

def prepare_contracts(core):
 catalog=json.loads((ROOT/'katalog.json').read_text(encoding='utf8'));lessons,providers=core.load_sources();contracts={}
 focus={'G1':2,'G2':1,'G3':4,'G5':1,'G6':2,'G7':3}
 for slug,l in lessons.items():
  gates=[]
  for i,g in enumerate(l['rpp_gates']):
   if g.get('optional'):continue
   g=copy.deepcopy(g);g['source_prompt']=g['prompt'];g['prompt']=clean_prompt(g['prompt']);g['seconds']=({'G1':120,'G2':120,'G3':120,'G5':120,'G6':120,'G7':120}.get(g['id'],180) if slug.startswith('f-mek') else ({'G1':60,'G2':120,'G3':120}.get(g['id'],180) if slug=='f-use-1-pra' else {'G5':180,'G6':120,'G7':180}.get(g['id'],180)));g['teacher_notes']=re.sub(r'(?:minimal|minimum)\s*120\s*detik','sesuai tingkat kesulitan',g['teacher_notes']);g['focus']=focus.get(g['id'],i+1) if slug.startswith('f-mek') else (4 if i==1 and slug=='f-use-1-pra' else i+1);gates.append(g)
  assert len(gates)==3,(slug,len(gates));contracts[slug]={'gates':gates}
 practice=json.loads((ROOT/'alat/bank/unit_practice.json').read_text(encoding='utf8'));unit={}
 from unit_real_redaksi import REAL
 for topic,qs in practice.items():
  real=[]
  for q in qs:
   q['seconds']={'L1':120,'L2':180,'L3':240}.get(q['level'],180)
   assert q['pembahasan'].count('<li>')==7,(topic,q['no'])
   r=copy.deepcopy(q)
   visual=re.search(r'(<div[^>]*>\s*<svg[\s\S]*?</svg>\s*</div>)',q['stimulus'])
   r['stimulus']=REAL[topic][q['no']-1]+(visual.group(1) if visual else '')
   if q['bentuk']=='PGK':r['stem']='Pilih semua kesimpulan yang sesuai dengan data kasus ini. Lebih dari satu jawaban dapat benar.'
   elif q['bentuk']=='BS':r['stem']='Nilailah setiap pernyataan: pilih Benar atau Salah berdasarkan model pada stimulus.'
   else:r['stem']='Dari data pengujian ini, '+q['stem'][0].lower()+q['stem'][1:]
   paraphrases={'besar resultan (jumlah vektor)':'nilai gabungan kedua vektor','Untuk dua gaya yang saling tegak lurus':'Jika kedua arah gaya membentuk sudut siku-siku','disebut langsung pada stimulus':'diperoleh dari deskripsi kasus','Angka itu terasa relevan karena':'Data tersebut berkaitan dengan','tidak masuk ke rumus':'tidak diperlukan dalam persamaan yang dipilih','yakni':'yaitu','karena':'sebab','diperlukan':'dibutuhkan','memakai':'menggunakan','terlebih dahulu':'lebih dulu','diberikan':'tersedia','diperoleh':'didapat','Hitung':'Tentukan','Kuadratkan':'Hitung kuadrat tiap besaran','Jumlahkan':'Gabungkan hasil penjumlahan','Tarik akar':'Ambil akar kuadratnya','Bandingkan dengan opsi':'Periksa juga pilihan','Jadi':'Dengan demikian'}
   for field in ['pembahasan','review']:
    for old,new in paraphrases.items():r[field]=re.sub(r'\b'+re.escape(old)+r'\b',lambda m:new,r[field])
   assert r['pembahasan']!=q['pembahasan'],(topic,q['no'],'Pembahasan real masih identik')
   assert r['stimulus']!=q['stimulus'] and r['correct']==q['correct'],(topic,q['no'],q['stimulus'])
   real.append(r)
  unit[topic]={'practice':qs,'real':real}
 p=ROOT/'functions/api/[[rute]].js';s=p.read_text(encoding='utf8');a=s.index('/* FIWA_CONTRACT_BEGIN */');b=s.index('/* FIWA_CONTRACT_END */')+len('/* FIWA_CONTRACT_END */')
 s=s[:a]+'/* FIWA_CONTRACT_BEGIN */\nconst GATING_CONTRACT = '+json.dumps(contracts,ensure_ascii=False)+';\nconst UNIT_CONTRACT = '+json.dumps(unit,ensure_ascii=False)+';\n/* FIWA_CONTRACT_END */'+s[b:];p.write_text(s,encoding='utf8')
 (ROOT/'alat/bank/gating_contract.json').write_text(json.dumps(contracts,ensure_ascii=False,indent=2),encoding='utf8')
 (ROOT/'alat/bank/unit_contract.json').write_text(json.dumps(unit,ensure_ascii=False,indent=2),encoding='utf8')

def configure(core):
 core.STAGES={'P2':8,'P7':10,'P9':8,'P10':4}
 def validate_question(q,slug,timed=False):
  assert q['kind']in('num','choice') and q['prompt'] and q['indicator']
  assert q['seconds']>= (30 if q.get('prerequisite') else 120),(slug,q['id'])
  if q['kind']=='choice':assert isinstance(q['answer'],int)and 0<=q['answer']<len(q['options'])
  else:assert isinstance(q['answer'],(float,int)) and q.get('tol',.05)>0
 core.validate_question=validate_question
 E=core.E;lab=core.lab;items=core.items;paras=core.paras
 def worked(w):
  assert len(w['steps'])==7, w['scenario']
  return '<section class="class-worked"><h3>Contoh terkerjakan</h3><p>'+E(prose(w['scenario']))+'</p><div class="solution-seven"><h4>Pembahasan</h4><ol>'+''.join('<li><strong>'+E(LABELS[i])+':</strong> '+E(prose(re.sub(r'^[^:]{1,65}:\s*','',x)))+'</li>'for i,x in enumerate(w['steps']))+'</ol></div></section>'
 core.worked=worked
 original_question=core.question
 def question(q,prefix,protected=False):
  q=copy.deepcopy(q);q['steps']=seven(q);return original_question(q,prefix,protected)
 core.question=question
 def summary(lesson):
  d=lesson['summary'];rows=d.get('rows',[])
  return '<section class="class-summary" id="rangkuman"><header><span class="class-eyebrow">Rangkuman · hubungkan seluruh gagasan</span><h2>Model yang perlu kamu bawa</h2><p>'+E(prose(d.get('bigidea','')) )+'</p></header><div class="summary-grid">'+''.join('<article><span class="class-pill">'+str(i+1)+'</span><h3>'+E(r['title'])+'</h3><div class="class-formula">'+E(r['formula'])+'</div><p>'+E(prose(r['meaning']))+'</p><aside><b>Jebakan:</b> '+E(prose(r['trap']))+'</aside></article>'for i,r in enumerate(rows))+'</div><section class="summary-transfer"><h3>Dari model ke masalah baru</h3><p>'+E(prose(d.get('transfer','')))+'</p><h3>Cek kesiapan mandiri</h3>'+items(d.get('checklist',[]))+'</section></section>'
 def pair(c):
  a=copy.deepcopy(c['lab']);b=copy.deepcopy(a);k=b['kind'];p=b['params']
  changes={'vector':{'bx':-abs(p.get('bx',3)),'by':0},'components':{'ref':'y'},'incline':{'theta':60},'motion':{'left':p.get('right',24)},'reaction':{'m2':p.get('m1',40)},'torque':{'theta':0},'couple':{'d':0},'cable':{'theta':60},'work':{'theta':90},'kinetic':{'v':2*p.get('v',3)},'potential':{'ref':p.get('h',3)},'workenergy':{'F':-abs(p.get('F',4))},'energy':{'mode':'friction','mu':.2}}
  p.update(changes[k]);a['readonly']=True;b['readonly']=True
  return '<details class="compare-models"><summary>Bandingkan dua keadaan · jelaskan perubahan</summary><div class="comparison-grid"><section><h4>Keadaan A</h4>'+lab(a)+'</section><section><h4>Keadaan B</h4>'+lab(b)+'</section></div><p>Temukan variabel yang berubah. Jelaskan bagian gambar, angka dan hubungan fisika yang ikut berubah; nyatakan pula apa yang tetap.</p></details>'
 def concept_body(lesson,prefix):
  body='<p class="class-lead">Prediksi dahulu, gerakkan model, hubungkan gambar dengan rumus, lalu buktikan lewat checkpoint.</p><nav class="class-toc">'+''.join('<a href="#konsep-'+str(i)+'">Konsep '+str(i)+'</a><a href="#checkpoint-'+str(i)+'">Checkpoint '+str(i)+'</a>'for i in range(1,len(lesson['concepts'])+1))+'<a href="#rangkuman">Rangkuman</a></nav>';checks=[]
  for i,c in enumerate(lesson['concepts'],1):
   body+='<section class="class-concept" id="konsep-'+str(i)+'"><header><span class="class-eyebrow">Main Concept · '+str(i)+'</span><h2>'+E(c['title'])+'</h2><p>'+E(c['question'])+'</p></header><div class="concept-visual-grid"><div>'+paras(c['explain'][:2])+'<div class="class-formula">'+E(c['formula'])+'</div></div><section class="class-lab"><h3>Ilustrasi konsep dan lab gerak</h3>'+lab(c['lab'])+'</section></div><h3>Bangun model dengan tepat</h3>'+paras(c['explain'][2:])+'<ul class="class-quantities">'+''.join('<li>'+E(x)+'</li>'for x in c['quantities'])+'</ul><aside class="class-assumption"><b>Asumsi dan batas model</b>'+items(c['assumptions'])+'</aside><section class="class-protocol"><h3>Prediksi · Ubah · Amati · Jelaskan</h3>'+items(c['explore'])+'</section>'+pair(c)+'<details class="class-misconception"><summary>Uji dugaan: '+E(c['misconception']['claim'])+'</summary><p>'+E(c['misconception']['explain'])+'</p></details>'+worked(c['worked'])+'<section class="class-checkpoint" id="checkpoint-'+str(i)+'"><h3>Checkpoint '+str(i)+'</h3>'
   for j,q in enumerate(c['checks'],1):block,data=question(q,prefix+f'-cp{i}-{j}');checks.append(data);body+=block+'<button class="class-button" type="button" data-check-one="'+E(data['id'])+'">Periksa langkah dan alasan</button><p role="status"></p>'
   body+='</section></section>'
  return body+summary(lesson),checks
 core.concept_body=concept_body
 original_page=core.page
 def page(path,title,code,subtitle,body,config=None,topic=None):
  cfg={**(config or {}),'version':4};slug=next((s for s in ALIGN if '/'+s+'/' in str(path).replace('\\','/')),None)
  if cfg.get('stage')=='P1' and slug:
   lesson=lesson_cache[slug];h=lesson['hook'];body='<section class="opening-frame"><span class="class-eyebrow">Opening · Coba pikirkan dulu</span><div class="opening-grid"><div><h2>'+E(h['title'])+'</h2><p class="class-lead">'+E(prose(h['scene']))+'</p><div class="hook-q"><b>Pertanyaan penggerak</b><p>'+E(prose(h['question']))+'</p></div><aside class="hook-memory"><h3>Ingat kembali</h3><p>'+E({'f-mek-1-pra':'Arah membedakan perpindahan dari jarak perjalanan.','f-mek-2':'Sebuah gaya memerlukan dua benda yang berinteraksi.','f-mek-1a':'Perubahan kecepatan ditentukan oleh resultan gaya pada benda yang dipilih.','f-mek-1b':'Letak garis kerja gaya memengaruhi kecenderungan putar.','f-use-1-pra':'Energi dapat berpindah melalui gaya sepanjang perpindahan.','f-use-1':'Acuan tinggi yang sama diperlukan ketika membandingkan dua keadaan.'}[slug])+'</p></aside><section class="hook-try"><h3>Coba sekarang</h3><p>Amati model. Simpan satu dugaan sebelum menekan Play; ubah satu parameter lalu bandingkan hasilnya.</p>'+''.join('<button class="hook-option" type="button">'+E(x)+'</button>'for x in h.get('options',[]))+'</section></div><div class="opening-visual">'+lab(h['lab'])+'</div></div><p class="opening-bridge">'+E(prose(h['bridge']))+'</p><a class="class-button" href="#tujuan">Lihat tujuan dan peta belajar</a></section><section class="class-card" id="tujuan"><span class="class-eyebrow">Tujuan pembelajaran</span><h2>Kemampuan yang akan kamu bangun</h2><p><b>'+E(meta_cache[slug].get('teks',''))+'</b></p>'+items([g for g in lesson['goals'] if g!=meta_cache[slug].get('teks','')])+'<nav class="roadmap">'+''.join('<a data-parent-route="tp-'+slug+'-p4-konsep-'+str(i)+'" data-tp-slug="'+slug+'" href="#tujuan"><b>'+str(i)+'</b><span>'+E(c['title'])+'</span><small>Konsep dan checkpoint</small></a>'for i,c in enumerate(lesson['concepts'],1))+'</nav></section>'+core.actions('Saya memahami tujuan belajar')
  if cfg.get('stage')=='P8' and slug:
   cards=[g for g in ALIGN[slug]['gates'] if g.get('optional')]
   body+='<section class="class-card"><h2>Tantangan T4 opsional</h2><p>Bagian ini menguji transfer mandiri dan tidak menurunkan bukti T3 yang sudah dicapai.</p>'+''.join('<details><summary>'+E(g['id']+' · '+g['title'])+'</summary><p>'+E(clean_prompt(g['prompt']))+'</p><p>'+E(g['rubric']['T4'])+'</p></details>'for g in cards)+'</section>'
  return original_page(path,title,code,subtitle,body,cfg,topic)
 core.page=page
 lesson_cache={};meta_cache={}
 origload=core.load_sources
 def cached_load():
  lessons,providers=origload();lesson_cache.update(lessons);catalog=json.loads((ROOT/'katalog.json').read_text(encoding='utf8'));meta_cache.update({t['slug']:t for topic in catalog['topik'] for t in topic.get('tp',[])});return lessons,providers
 core.load_sources=cached_load
 return lesson_cache

def build():
 import konten_interaktif as core
 configure(core);prepare_contracts(core);core.build()
 # Materi pendukung hanya pada tahap yang mempunyai kebutuhan tersendiri.
 for topic in ['f-mek','f-use']:
  p=ROOT/f'media-{topic}/media.json';data=json.loads(p.read_text(encoding='utf8'));seen=set()
  for tp,stages in data.get('tp',{}).items():
   old=copy.deepcopy(stages);stages.clear();video=next((x for xs in old.values() for x in xs if x.get('tipe')=='video'),None);audio=next((x for xs in old.values()for x in xs if x.get('tipe')=='audio'),None)
   keep=[]
   for x in [video,audio]:
    if not x:continue
    key=(x['tipe'],x.get('yt')or x.get('berkas')or x.get('naskah'))
    if key in seen:continue
    seen.add(key);x['catatan']='Pilihan pendukung saat mempelajari P4; gunakan untuk mengamati atau mendengar konsep yang sedang dibahas.';keep.append(x)
   stages['S4']=keep
  data['topik']={};p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
 print('Penyelarasan RPP, gating tiga gerbang inti per TP dan Unit Test berpasangan tersimpan.')
if __name__=='__main__':build()
