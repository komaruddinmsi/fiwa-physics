"""Sumber penerbitan konten interaktif. Baca STANDAR-KONTEN-FISIKA.md.
Memuat aset lesson_*.py, memvalidasi seluruh TP, baru menulis HTML versi 4.
"""
from pathlib import Path
import copy,hashlib,html,importlib.util,json,math,os,re
ROOT=Path(__file__).resolve().parents[1]
E=lambda value:html.escape(str(value),quote=True)
STAGES={'P2':8,'P7':10,'P9':8,'P10':4}
SOURCES={
 'f-use':['https://openstax.org/books/university-physics-volume-1/pages/7-1-work','https://openstax.org/books/university-physics-volume-1/pages/8-3-conservation-of-energy'],
 'f-mek':['https://openstax.org/books/university-physics-volume-1/pages/2-3-algebra-of-vectors','https://openstax.org/books/university-physics-volume-1/pages/5-3-newtons-second-law','https://openstax.org/books/university-physics-volume-1/pages/12-1-conditions-for-static-equilibrium']}
TOPICS={
 'f-use':{'title':'Misi paket: bergerak, berhenti, sampai tujuan','scene':'Sebuah paket meluncur dari meja pengiriman menuju tempat penampungan. Bagian lintasannya licin, bagian lain dilapisi bahan kasar. Di mana paket bertambah cepat, dan ke mana energi geraknya berpindah ketika melambat?','question':'Bisakah kamu mengatur lintasan agar paket sampai, tetapi tidak menabrak terlalu cepat?','bridge':'Mulai dengan mengenali usaha dan bentuk energi, lalu gunakan neraca energi untuk menilai sebuah rancangan.','lab':{'kind':'energy','params':{'m':2,'h0':4,'h':1,'mu':.15,'s':3,'mode':'friction','shape':'valley'}}},
 'f-mek':{'title':'Misi laboratorium: satu troli, banyak keputusan','scene':'Alat praktikum dibawa dengan troli lalu ditempatkan pada rak berpenyangga. Mengubah arah tarikan, jumlah muatan, atau posisi beban bisa menghasilkan akibat yang berbeda. Kita ingin dapat memprediksinya dari gambar, bukan menebak dari rasa berat.','question':'Bagaimana panah dan model sederhana membantu memilih cara menarik troli serta menempatkan beban?','bridge':'Bangun bekal vektor, hubungkan gaya dengan perubahan gerak, lalu analisis momen dan komponen pada struktur.','lab':{'kind':'motion','params':{'right':24,'left':12,'m':4,'v0':1,'t':2}}}}

def load_sources():
 lessons={};providers={}
 for path in sorted((ROOT/'alat/bank').glob('lesson_*.py')):
  spec=importlib.util.spec_from_file_location('fiwa_'+path.stem,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  for slug,data in module.LESSONS.items():
   if slug in lessons:raise ValueError('Sumber TP ganda: '+slug)
   lessons[slug]=data;providers[slug]=module.make_questions
 from revisi_rpp import align_sources
 return align_sources(lessons,providers)

def validate(lessons,providers,catalog):
 kinds={'vector','components','incline','motion','reaction','torque','couple','cable','work','kinetic','potential','workenergy','energy'}
 report=[]
 for topic in catalog['topik']:
  for tp in topic.get('tp',[]):
   slug=tp['slug']
   if slug not in lessons:raise ValueError(f'{slug}: lengkapi lesson_*.py menurut STANDAR-KONTEN-FISIKA.md sebelum membangun topik baru.')
   lesson=lessons[slug];ids=[c['id'] for c in lesson['concepts']]
   assert len(ids)>=2 and len(set(ids))==len(ids)
   assert all(lesson['hook'].get(k) for k in ('title','scene','question','bridge','lab'))
   for c in lesson['concepts']:
    assert len(c['explain'])>=3 and c['lab']['kind'] in kinds,(slug,c['id'])
    assert len(c['worked']['steps'])>=5 and len(c['checks'])>=1
    assert c['formula'] and c['quantities'] and c['assumptions'] and len(c['explore'])>=3
    for q in c['checks']:validate_question(q,slug,True)
   prompts={}
   for stage,count in STAGES.items():
    for form in range(1,5):
     qs=providers[slug](slug,stage,form);assert len(qs)==count,(slug,stage,form,len(qs))
     assert len({q['id'] for q in qs})==count
     for q in qs:validate_question(q,slug,stage=='P5')
     prompts[stage,form]={re.sub(r'\s+',' ',q['prompt'].strip()) for q in qs}
   assert not prompts['P7',1]&prompts['P9',1],(slug,'Butir P9 menduplikasi P7')
   report.append({'tp':tp['kode'],'concepts':len(ids),'checks':sum(len(c['checks']) for c in lesson['concepts']),'min_check_seconds':min(q['seconds'] for c in lesson['concepts'] for q in c['checks'])})
 return report

def validate_question(q,slug,timed=False):
 assert q['kind'] in ('num','choice') and q.get('prompt') and q.get('indicator'),(slug,q)
 assert isinstance(q['seconds'],(int,float)) and q['seconds']>=(30 if q.get('prerequisite') else 120),(slug,q['id'])
 if q['kind']=='choice':assert isinstance(q['answer'],int) and 0<=q['answer']<len(q['options'])
 else:assert math.isfinite(float(q['answer'])) and float(q.get('tol',.05))>0
 if timed:
  level=str(q.get('level','C2'));floor={'C1':120,'C2':120,'C3':180,'C4':240,'C5':300,'C6':300}.get(level,120)
  assert q['seconds']>=floor,(slug,q['id'],'Waktu tidak sesuai tuntutan soal')

def lab(config,static=False):
 config=copy.deepcopy(config);config['static']=static
 return '<figure class="class-stimulus" data-physics-lab="'+E(json.dumps(config,ensure_ascii=False))+'"></figure>'
def paras(lines):return ''.join('<p>'+E(x)+'</p>' for x in lines)
def items(lines):return '<ul>'+''.join('<li>'+E(x)+'</li>' for x in lines)+'</ul>'
def minutes(seconds):return f'{seconds//60:g} menit'+(f' {seconds%60:g} detik' if seconds%60 else '')

def question(raw,prefix,protected=False):
 q=copy.deepcopy(raw);q['id']='v4-'+prefix+'-'+str(q['id']);qid=q['id'];level=q.get('level','C2');unit=q.get('unit','')
 stimulus=lab(q['diagram'],True) if q.get('diagram') else ''
 if q['kind']=='choice':
  field='<fieldset class="class-choice"><legend>'+E(q.get('label','Pilih satu jawaban'))+'</legend><input type="hidden" id="'+E(qid)+'" name="'+E(qid)+'" value="">'+''.join(f'<label for="{E(qid)}-opt-{i}"><input id="{E(qid)}-opt-{i}" type="radio" name="{E(qid)}-option" value="{i}" data-choice-for="{E(qid)}"><span>{E(option)}</span></label>' for i,option in enumerate(q['options']))+'</fieldset>'
 else:field=f'<label class="q-label" for="{E(qid)}">{E(q.get("label","Jawaban"))}{" ("+E(unit)+")" if unit else ""}</label><input type="text" inputmode="decimal" autocomplete="off" id="{E(qid)}" name="{E(qid)}" placeholder="Tuliskan angka tanpa satuan">'
 block=f'<article class="class-question" data-question-id="{E(qid)}"><span class="class-time">{E(level)} · Alokasi {minutes(q["seconds"])}</span><p class="q-prompt">{E(q["prompt"])}</p>{stimulus}{field}<div class="class-feedback" data-feedback="{E(qid)}" hidden><strong></strong><p></p></div></article>'
 if protected:
  salt='FIWA-2026-v4-'+prefix;scale=max(100,10**math.ceil(-math.log10(float(q.get('tol',.05))))) if q['kind']=='num' else 1; q['hashScale']=scale
  if q['kind']=='num':
   answer=float(q['answer']);tol=float(q.get('tol',.05));tokens=range(math.ceil((answer-tol)*scale-1e-8),math.floor((answer+tol)*scale+1e-8)+1)
  else:tokens=[str(q['answer'])]
  q['hashes']=[hashlib.sha256(f'{salt}|{qid}|{token}'.encode()).hexdigest() for token in tokens]
  q.pop('answer',None);q.pop('steps',None);q['explain']='Tinjau kembali konsep '+q['indicator']+'. Periksa gambar, model, tanda, satuan, serta alasan yang kamu gunakan.'
 return block,q

def worked(data):
 return '<section class="class-worked"><h3>Contoh terkerjakan · bangun alasan langkah demi langkah</h3><p>'+E(data['scenario'])+'</p>'+''.join(f'<details><summary>Langkah {i+1}</summary><p>{E(step)}</p></details>' for i,step in enumerate(data['steps']))+'<details><summary>Makna hasil dan pemeriksaan</summary><p class="worked-result">'+E(data['result'])+'</p></details></section>'

def page(path,title,code,subtitle,body,config=None,topic=None):
 root=Path(os.path.relpath(ROOT,path.parent)).as_posix()+'/'
 cfg=json.dumps(config or {},ensure_ascii=False).replace('</','<\\/')
 runtime='gating.js' if (config or {}).get('stage')=='P5-gating' else 'unit-test.js' if (config or {}).get('stage')=='unit' else 'kelas-konten.js'
 src='' if (config or {}).get('stage') in ('P2','P5','P9') else '<aside class="class-sources"><b>Rujukan konsep</b> '+''.join('<a href="'+E(url)+'" target="_blank" rel="noopener">OpenStax · '+E(url.rsplit('/',1)[-1].replace('-',' '))+'</a>' for url in SOURCES.get(topic,[]))+'</aside>'
 text=f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · {E(code)}</title><link rel="stylesheet" href="{root}assets/kelas-konten.css"></head><body class="class-page"><header class="class-header"><div class="class-eyebrow">Fisika · {E(code)}</div><h1>{E(title)}</h1><p>{E(subtitle)}</p></header><main class="class-main">{body}{src}</main><footer class="class-footer">Physics FIWA · Model ideal dan asumsi dinyatakan pada tiap kegiatan. Materi interaktif v4.</footer><script>window.FIWA_CLASS={cfg};</script><script src="{root}assets/kelas-visual.js"></script><script src="{root}assets/kelas-animasi.js"></script><script src="{root}assets/{runtime}"></script><script src="{root}assets/fims-simpan.js"></script></body></html>'''
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');return path.relative_to(ROOT).as_posix()

def actions(label='Simpan penyelesaian',hidden=False):
 return '<div class="class-actions"><button type="button" class="class-button" id="class-submit"'+(' hidden' if hidden else '')+'>'+E(label)+'</button></div><p id="class-result" class="class-result" role="status" aria-live="polite"></p>'
def field(label,name,rows=4):return '<label for="'+E(name)+'">'+E(label)+'</label><textarea data-required="1" id="'+E(name)+'" name="'+E(name)+'" rows="'+str(rows)+'"></textarea>'

def concept_body(lesson,prefix):
 body='<p class="class-lead">Pelajari satu konsep melalui gambar, ubah variabel untuk menguji dugaan, lalu jawab checkpoint. Contoh dapat dibuka bertahap agar kamu sempat berpikir sebelum melihat langkah selanjutnya.</p><nav class="class-toc" aria-label="Konsep dan checkpoint">'+''.join(f'<a href="#konsep-{i}">Konsep {i}</a><a href="#checkpoint-{i}">Checkpoint {i}</a>' for i,_ in enumerate(lesson['concepts'],1))+'</nav>';checks=[]
 for i,c in enumerate(lesson['concepts'],1):
  body+=f'<section class="class-concept" id="konsep-{i}"><header><span class="class-pill">Konsep {i}</span><h2>{E(c["title"])}</h2><p>{E(c["question"])}</p></header>{paras(c["explain"])}<div class="class-formula">{E(c["formula"])}</div><ul class="class-quantities">'+''.join('<li>'+E(x)+'</li>' for x in c['quantities'])+'</ul><div class="class-assumption"><b>Model dan batasnya</b>'+items(c['assumptions'])+'</div>'
  body+='<section class="class-lab"><h3>Lab visual · prediksi, ubah, amati</h3>'+lab(c['lab'])+'<ol class="class-explore">'+''.join('<li>'+E(x)+'</li>' for x in c['explore'])+'</ol></section>'
  m=c['misconception'];body+='<aside class="class-misconception"><strong>Uji dugaan ini: '+E(m['claim'])+'</strong><p>'+E(m['explain'])+'</p></aside>'+worked(c['worked'])
  body+=f'<section class="class-checkpoint" id="checkpoint-{i}"><h3>Checkpoint {i} · jelaskan sebelum melanjutkan</h3>'
  for j,q in enumerate(c['checks'],1):
   block,data=question(q,prefix+f'-cp{i}-{j}');checks.append(data);body+=block+'<button class="class-button" type="button" data-check-one="'+E(data['id'])+'">Periksa alasanmu</button><p role="status"></p>'
  body+='</section></section>'
 return body,checks

def build():
 catalog=json.loads((ROOT/'katalog.json').read_text(encoding='utf-8'));lessons,providers=load_sources();summary=validate(lessons,providers,catalog);written=[];hooks={}
 for topic in catalog['topik']:
  for meta in topic.get('tp',[]):
   slug=meta['slug'];lesson=lessons[slug];base=ROOT/'konten'/topic['slug']/slug;code=meta['kode'];sub=meta['judul'];provider=providers[slug];ids=[c['id'] for c in lesson['concepts']]
   def save(name,title,body,cfg):written.append(page(base/name,title,code,sub,body,{'version':4,**cfg},topic['slug']))
   h=lesson['hook'];hooks[slug]={'head':h['title'],'hook':h['scene']+' '+h['question'],'bridge':h['bridge'],'concepts':[c['title'] for c in lesson['concepts']]}
   body='<section class="class-hook"><div class="class-eyebrow">Mulai dengan sebuah fenomena</div><h2>'+E(h['title'])+'</h2><p class="class-lead">'+E(h['scene'])+'</p><p class="hook-question">'+E(h['question'])+'</p>'+lab(h['lab'])+'<p>'+E(h['bridge'])+'</p><a class="class-button" href="#tujuan">Temukan tujuan belajarmu</a></section>'
   goals=[g for g in lesson['goals'] if g.strip()!=meta.get('teks','').strip()]
   body+='<section class="class-card class-goals" id="tujuan"><h2>Tujuan Pembelajaran</h2><p><strong>'+E(meta.get('teks',''))+'</strong></p><h3>Setelah bagian ini kamu dapat</h3>'+items(goals)+'<p>Keberhasilan ditunjukkan melalui jawaban mandiri, penjelasan yang tepat, dan bukti penerapan. Prediksi yang perlu dicatat guru akan ditulis pada P3.</p></section>'+actions('Saya memahami tujuan belajar')
   save('P1/index.html','Pembuka dan Tujuan',body,{'stage':'P1'})
   body='<section class="class-card"><h2>Prediksimu penting</h2><p>Tuliskan jawaban awal dan alasanmu. Bagian ini belum mengoreksi benar atau salah; kita akan kembali pada alasan ini setelah menguji model.</p></section><section class="class-card class-task">'
   for i,pred in enumerate(lesson['prediction'],1):
    if isinstance(pred,dict):
     if pred.get('diagram'):body+=lab(pred['diagram'],True)
     if pred.get('options'):body+=items(pred['options'])
    body+=field(pred.get('prompt','') if isinstance(pred,dict) else pred,f'v3-prediksi-{i}')
   body+='</section>'+actions('Kirim prediksi dan alasan');save('P3/index.html','Prediksi Awal',body,{'stage':'P3'})
   save('P5/index.html','Cek Pemahaman · Gating TP','<div id="gating-host"><p>Memuat gerbang dan respon guru…</p></div>',{'stage':'P5-gating','tp':slug})
   core,checks=concept_body(lesson,slug);save('P4/index.html','Konsep dan Praktik',core+actions('Simpan penyelesaian konsep'),{'stage':'P4','checks':checks})
   for filename,title,stage,text in [('diskusi.html','Diskusi Prediksi','P4-diskusi','Bandingkan alasan awal dengan model yang sudah diamati. Pilih satu dugaan yang berubah, lalu jelaskan bukti visual yang membuatmu mengubahnya.'),('contoh.html','Contoh Terbimbing','P4-contoh','Kerjakan setiap langkah dalam pikiran atau buku sebelum membukanya. Sebutkan model, arah positif, dan alasan memilih persamaan.'),('praktik.html','Praktik dan Penyelidikan','P4-praktik','Pilih satu variabel untuk diubah. Tetapkan variabel lain, prediksi hasil, ambil sedikitnya tiga kondisi, lalu jelaskan pola yang ditemukan.')]:
    b='<section class="class-card"><h2>'+E(title)+'</h2><p>'+E(text)+'</p></section>'
    if filename=='contoh.html':b+=''.join(worked(c['worked']) for c in lesson['concepts'])
    else:
     selected=[lesson['concepts'][0],lesson['concepts'][-1]]
     for c in selected:b+='<section class="class-lab"><h3>'+E(c['title'])+'</h3>'+lab(c['lab'])+items(c['explore'])+'</section>'
    b+='<section class="class-card class-task">'+field('Catatan model, data atau perbandingan yang kamu gunakan','v3-'+stage+'-data')+field('Kesimpulan dan alasan berdasarkan bukti yang diamati','v3-'+stage+'-alasan')+'</section>'+actions('Simpan catatan kegiatan');save('P4/'+filename,title,b,{'stage':stage})
   for stage,form in [('P2',1),('P7',1)]:
    qs=provider(slug,stage,form);body='<section class="class-card"><h2>'+({'P2':'Periksa bekal sebelum melangkah','P5':'Tunjukkan pemahamanmu','P7':'Sepuluh soal untuk menyiapkan diri'})[stage]+'</h2><p>'+({'P2':'Gunakan bekal yang sudah kamu pelajari. Hasilnya menentukan apakah kamu perlu penguatan prasyarat.','P5':'Kerjakan secara mandiri. Hasil awal membantu diagnosis; guru mengesahkan skor dan fokus tindak lanjut.','P7':'Kerjakan sepuluh soal secara mandiri dahulu. Sesudah mencoba, pelajari umpan balik dan perbaiki bagian yang masih keliru. Hasil percobaan pertama tetap dibedakan dari hasil perbaikan.'})[stage]+'</p></section>'
    if stage in ('P2','P5'):body+='<div class="class-clock"><span id="class-clock-label">Waktu rekomendasi; alokasi per soal mengikuti tingkat kesulitan.</span><output id="class-clock-value"></output></div><button type="button" class="class-button" id="class-start">Mulai pengerjaan</button>'
    body+='<div class="class-question-list"'+(' hidden' if stage in ('P2','P5') else '')+'>';data=[]
    for i,q in enumerate(qs,1):block,d=question(q,slug+'-'+stage+'-f'+str(form));body+='<h3>Soal '+str(i)+'</h3>'+block;data.append(d)
    body+='</div>'+actions('Kirim hasil' if stage!='P7' else 'Periksa 10 jawaban',stage in ('P2','P5'))
    save(stage+('/index.html' if form==1 else '/form-'+str(form)+'.html'),{'P2':'Cek Prasyarat','P5':'Cek Pemahaman','P7':'Latihan Persiapan · 10 soal'}[stage],body,{'stage':stage,'questions':data,'indicators':ids,'form':form,'threshold':80,'seconds':sum(q['seconds'] for q in qs)})
   for branch,title in [('a','Penguatan Prasyarat'),('b','Belajar Terbimbing Prasyarat')]:
    qbase=provider(slug,'P2',1);body='<section class="class-card"><h2>'+title+'</h2><p>Tinjau bekal yang belum tepat sebelum mencoba kembali P2. Kerjakan contoh berikut dengan alasanmu sendiri.</p></section>'
    for q in qbase[:3 if branch=='a' else 4]:body+='<section class="class-worked"><h3>'+E(q['prompt'])+'</h3><details><summary>Lihat penjelasan sesudah mencoba</summary><p>'+E(q['explain'])+'</p></details></section>'
    body+=actions('Saya siap mencoba kembali P2');save('P2'+branch+'/index.html',title,body,{'stage':'P2'+branch})
   for branch,n in [('a',2),('b',3)]:
    default=provider(slug,'P5',2)[:n];blocks=[];data=[]
    for q in default:block,d=question(q,slug+'-P6'+branch);blocks.append(block);data.append(d)
    focus_sets=[]
    for c in lesson['concepts']:
     pool=[q for q in provider(slug,'P7',2) if q['indicator']==c['id']]
     pool+=copy.deepcopy(c['checks']);selected=pool[:n]
     while len(selected)<n:selected+=copy.deepcopy(c['checks'][:1])
     fb=[];fd=[]
     for k,q in enumerate(selected[:n]):q=copy.deepcopy(q);q['id']+='-focus-'+str(k);block,d=question(q,slug+'-P6'+branch+'-'+c['id']);fb.append(block);fd.append(d)
     focus_sets.append({'html':''.join(fb),'questions':fd,'note':c['misconception']['explain']})
    body='<section class="class-card"><h2>'+('Penguatan' if branch=='a' else 'Belajar Terbimbing')+'</h2><p>Bagian ini terbuka sesuai hasil P5. Fokus pada satu kesulitan yang perlu diperbaiki.</p><p id="focus-note">Baca pertanyaannya, gambar modelnya, dan periksa alasan yang digunakan.</p></section><div class="class-question-list">'+''.join(blocks)+'</div>'+actions('Periksa tindak lanjut')+'<p>Sesudah semua tepat, lakukan cek ulang P5 bersama guru. Penguatan tidak otomatis mengubah skor P5 menjadi lulus.</p>'
    save('P6'+branch+'/index.html','Tindak Lanjut',body,{'stage':'P6','branch':branch,'questions':data,'focusSets':focus_sets,'threshold':100})
   task=lesson['performance'];body='<section class="class-card"><h2>Masalah penerapan</h2><p class="class-lead">'+E(task['scenario'])+'</p>'+items(task['deliverables'])+'</section><section class="class-card"><h2>Rubrik yang digunakan guru</h2><table class="class-rubric"><thead><tr><th>Tingkat</th><th>Bukti yang ditunjukkan</th></tr></thead><tbody>'+''.join('<tr><th>'+E(k)+'</th><td>'+E(v)+'</td></tr>' for k,v in task['rubric'].items())+'</tbody></table></section><section class="class-card class-task">'+field('Model, data, sketsa atau uraian rancanganmu','v3-p8-model',6)+field('Penyelesaian dan pemeriksaan hasil','v3-p8-proses',6)+field('Keputusan, alasan, batas model dan kesimpulan','v3-p8-keputusan',5)+'</section>'+actions('Kirim bukti penerapan')
   save('P8/index.html','Tugas Penerapan',body,{'stage':'P8'})
   for stage,forms in [('P9',range(1,5)),('P10',range(1,4))]:
    for form in forms:
     qs=provider(slug,stage,form);body='<section class="class-card"><h2>'+('Buktikan penguasaan pada masalah baru' if stage=='P9' else 'Panggil kembali konsep setelah jeda')+'</h2><p>Kerjakan mandiri. Gambar adalah stimulus soal, bukan kalkulator jawaban. Setelah dikirim, jawaban sesi ini dikunci.</p></section><div class="class-clock"><span id="class-clock-label">Alokasi waktu sesuai tuntutan setiap soal; tidak ada kegagalan otomatis karena waktu rekomendasi terlewati.</span><output id="class-clock-value"></output></div><button type="button" class="class-button" id="class-start">Mulai pengerjaan</button><div class="class-question-list" hidden>';data=[];prefix=slug+'-'+stage+'-f'+str(form)
     for i,q in enumerate(qs,1):block,d=question(q,prefix,stage=='P9');body+='<h3>Soal '+str(i)+'</h3>'+block;data.append(d)
     body+='</div>'+actions('Kirim uji ketuntasan' if stage=='P9' else 'Kirim sesi pengulangan',True)
     cfg={'stage':stage,'questions':data,'indicators':ids,'threshold':meta.get('ambang',75),'form':form,'session':form if stage=='P10' else None,'seconds':sum(q['seconds'] for q in qs)}
     if stage=='P9':cfg.update(salt='FIWA-2026-v4-'+prefix,hashScale=100)
     save(f'{stage}/'+(f'form-{form}.html' if stage=='P9' else f'sesi-{form}.html'),'Uji Ketuntasan TP' if stage=='P9' else 'Ulangi Materi',body,cfg)
   # Bacaan utama lama diganti edisi interaktif yang sama, tetap dapat dibuka terpisah.
   reading=ROOT/f'media-{topic["slug"]}/bacaan'/('bacaan-tp1.html' if slug=='f-use-1-pra' else 'bacaan-tp2.html' if slug=='f-use-1' else 'bacaan-'+slug+'.html')
   written.append(page(reading,'Bacaan Konsep Interaktif',code,sub,core+actions('Simpan penyelesaian bacaan'),{'version':4,'stage':'bacaan','checks':checks},topic['slug']))
  if topic.get('tp'):
   intro=TOPICS.get(topic['slug'])
   if not intro:raise ValueError('Lengkapi pembuka fenomena topik: '+topic['slug'])
   body='<section class="opening-frame"><div class="opening-grid"><div><span class="class-eyebrow">Opening · fenomena dunia nyata</span><h2>'+E(intro['title'])+'</h2><p class="class-lead">'+E(intro['scene'])+'</p><aside class="hook-q"><h3>Pertanyaan penggerak</h3><p>'+E(intro['question'])+'</p></aside><section class="hook-memory"><h3>Ingat kembali</h3><p>'+('Gaya adalah interaksi berarah. Perubahan gerak dan kecenderungan putar memerlukan model yang sesuai.' if topic['slug']=='f-mek' else 'Energi dapat berpindah bentuk. Berkurangnya energi mekanik tidak berarti energi total hilang.')+'</p></section><section class="hook-try"><h3>Coba sekarang</h3><p>'+('Ubah besar dorongan dan massa secara terpisah. Prediksi arah percepatan, tekan Play, lalu bandingkan geraknya.' if topic['slug']=='f-mek' else 'Ubah tinggi awal dan koefisien gesek secara terpisah. Prediksi apakah paket sampai, lalu tekan Play dan amati neraca energinya.')+'</p></section></div><div class="opening-visual">'+lab(intro['lab'])+'</div></div><p class="opening-bridge">'+E(intro['bridge'])+'</p></section><section class="class-card"><h2>Pilih perjalanan belajarmu</h2><p>Amati fenomenanya, lalu mulai dari TP yang sudah terbuka. Keterampilan sebelumnya menjadi bekal bagian berikutnya.</p>'+''.join('<a class="topic-destination" data-parent-route="tp-'+E(tp['slug'])+'-p1" data-tp-slug="'+E(tp['slug'])+'" href="../../../index.html#tp-'+E(tp['slug'])+'-p1" target="_top"><strong>'+E(tp['kode'])+' · '+E(tp['judul'])+'</strong><span>'+E(lessons[tp['slug']]['hook']['title'])+'</span></a>' for tp in topic['tp'])+'</section>'
   written.append(page(ROOT/'konten'/topic['slug']/'pembuka/index.html','Fenomena Dunia Nyata',topic['kode'],topic['nama'],body,{'version':4,'stage':'topic'},topic['slug']))
 # Lapis topik: bank lintas-TP dan penyelidikan dengan bukti model.
 for topic in catalog['topik']:
  tps=topic.get('tp',[])
  if not tps:continue
  for stage,bank,form in [('L1','P7',3)]:
   body='<section class="class-card"><h2>Hubungkan model antar-TP</h2><p>Gunakan diagram, satuan dan alasan untuk memilih model. '+('Kerjakan mandiri; jawaban dikunci sesudah dikirim.' if stage=='L3' else 'Coba dahulu, lalu gunakan umpan balik untuk memperbaiki alasan.')+'</p></section><div class="class-question-list">';data=[]
   for tp in tps:
    for q in providers[tp['slug']](tp['slug'],bank,form)[:3]:
     block,d=question(q,topic['slug']+'-'+stage,stage=='L3');body+=block;data.append(d)
   body+='</div>'+actions('Kirim jawaban lintas-TP')
   cfg={'version':4,'stage':stage,'questions':data,'threshold':75,'seconds':sum(q['seconds'] for q in data)}
   if stage=='L3':cfg.update(salt='FIWA-2026-v4-'+topic['slug']+'-'+stage,hashScale=100)
   name='L3/latihan-interaktif.html' if stage=='L3-latihan' else stage+'/interaktif.html'
   written.append(page(ROOT/'konten'/topic['slug']/name,'Latihan Unit Test' if stage=='L3-latihan' else 'Penilaian Lintas-TP',topic['kode'],topic['nama'],body,cfg,topic['slug']))
  for mode,filename in [('practice','latihan-interaktif.html'),('real','interaktif.html')]:
   written.append(page(ROOT/'konten'/topic['slug']/'L3'/filename,'Latihan Unit Test' if mode=='practice' else 'Unit Test',topic['kode'],topic['nama'],'<div id="unit-host"><p>Memuat Unit Test…</p></div>',{'version':4,'stage':'unit','topic':topic['slug'],'unitMode':mode,'root':'../../../'},topic['slug']))
  for stage in ('L2','L4'):
   body='<section class="class-card"><h2>Penyelidikan terpadu · '+E(TOPICS[topic['slug']]['title'])+'</h2><p>'+E(TOPICS[topic['slug']]['scene'])+'</p><p>Hubungkan sedikitnya dua model dari TP dalam topik ini. Ubah satu variabel, rekam tiga kondisi, dan nyatakan batas kesimpulanmu.</p></section>'
   for tp in tps:
    c=lessons[tp['slug']]['concepts'][-1];body+='<section class="class-lab"><h2>'+E(tp['judul'])+'</h2>'+lab(c['lab'])+items(c['explore'])+'</section>'
   body+='<section class="class-card class-task">'+field('Pertanyaan penyelidikan dan prediksi','v3-'+stage+'-prediksi')+field('Model, variabel, data tiga kondisi dan perbandingannya','v3-'+stage+'-data',7)+field('Kesimpulan lintas-TP, alasan, batas model dan rancangan perbaikan','v3-'+stage+'-alasan',6)+'</section><section class="class-card"><h2>Kriteria bukti</h2><p>T1: mengumpulkan data tanpa model yang tepat. T2: model sebagian tepat tetapi hubungan antar-TP belum dijelaskan. T3: model, satuan, perbandingan data dan alasan lintas-TP tepat. T4: semua bukti T3 disertai pemeriksaan alternatif serta batas model yang jelas. Guru menilai bukti; tombol kirim tidak memberi tier secara otomatis.</p></section>'+actions('Kirim bukti penyelidikan')
   written.append(page(ROOT/'konten'/topic['slug']/stage/'interaktif.html','Penyelidikan Lintas-TP',topic['kode'],topic['nama'],body,{'version':4,'stage':stage},topic['slug']))
 (ROOT/'assets/alur-p-data.js').write_text('window.FIWA_TP_HOOKS='+json.dumps(hooks,ensure_ascii=False)+';\nwindow.FIWA_TOPIC_HOOKS='+json.dumps(TOPICS,ensure_ascii=False)+';\n',encoding='utf-8')
 out=ROOT/'dokumentasi/05-validasi/2026/11/konten-interaktif';out.mkdir(parents=True,exist_ok=True)
 (out/'struktur-konten.json').write_text(json.dumps({'version':4,'lessons':summary,'files':written},ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'{len(summary)} TP, {sum(x["concepts"] for x in summary)} konsep interaktif, {len(written)} halaman edisi 4 ditulis.')
 return summary
if __name__=='__main__':
 from revisi_rpp import build as build_rpp
 build_rpp()
