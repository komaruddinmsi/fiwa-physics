"""Pemeriksaan sumber, halaman aktif, jumlah soal, waktu dan tautan lokal; tanpa menulis konten."""
from pathlib import Path
import importlib.util,json,re,sys,hashlib,math
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from konten_interaktif import load_sources,validate,ROOT
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.labs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ('src','href'):
   if key in a:self.links.append(a[key])
  if 'data-physics-lab' in a:self.labs.append(json.loads(a['data-physics-lab']))
catalog=json.loads((ROOT/'katalog.json').read_text(encoding='utf8'))
lessons,providers=load_sources();summary=validate(lessons,providers,catalog)
manifest=json.loads((ROOT/'dokumentasi/05-validasi/2026/11/konten-interaktif/struktur-konten.json').read_text(encoding='utf8'))
questions=0;labs=0;protected=0
for file in manifest['files']:
 p=ROOT/file;text=p.read_text(encoding='utf8');doc=Page();doc.feed(text)
 assert len(doc.ids)==len(set(doc.ids)),file+' ID ganda'
 for link in doc.links:
  u=urlsplit(link)
  if u.scheme or u.netloc or not u.path:continue
  assert (p.parent/unquote(u.path)).resolve().exists(),(file,link)
 for lab in doc.labs:assert lab['kind'] in {'vector','components','incline','motion','reaction','torque','couple','cable','work','kinetic','potential','workenergy','energy'}
 labs+=len(doc.labs)
 cfg=json.loads(re.search(r'window.FIWA_CLASS=(.*?);</script>',text).group(1))
 for q in cfg.get('questions',[])+cfg.get('checks',[]):
  questions+=1;assert q['seconds']>=120
  if q.get('hashes'):
   protected+=1;assert 'answer' not in q and 'steps' not in q
   assert len(q['hashes'])>0 and len(set(q['hashes']))==len(q['hashes'])
   if cfg['stage']=='P9':
    # Kunci sumber benar harus diterima hash yang dipakai peramban.
    slug=next(s for s in lessons if '/'+s+'/' in file)
    source=providers[slug](slug,'P9',cfg['form'])
    orig=next(x for x in source if q['id'].endswith('-'+x['id']))
    token=str(round(orig['answer']*q['hashScale'])) if q['kind']=='num' else str(orig['answer'])
    assert hashlib.sha256(f'{cfg["salt"]}|{q["id"]}|{token}'.encode()).hexdigest() in q['hashes']
 if cfg.get('stage')=='P7':assert len(cfg['questions'])==10
 if cfg.get('stage')=='P6':
  n=2 if cfg['branch']=='a' else 3
  assert len(cfg['questions'])==n and all(len(x['questions'])==n for x in cfg['focusSets'])
 if cfg.get('stage')=='P10':assert len(cfg['questions'])==4
 if cfg.get('stage')=='P1':assert text.index('class-hook')<text.index('id="tujuan"')
for t in catalog['topik']:
 for tp in t.get('tp',[]):
  assert 'S10' not in tp['tahapan']
  assert all(x.get('versi')==3 for x in tp['tahapan'].values()),tp['slug']
  p7={q['indicator'] for q in providers[tp['slug']](tp['slug'],'P7',1)}
  p9={q['indicator'] for q in providers[tp['slug']](tp['slug'],'P9',1)}
  assert p9<=p7,(tp['slug'],'Indikator belum dilatih',p9-p7)
print(json.dumps({'tp':len(summary),'concepts':sum(x['concepts'] for x in summary),'pages':len(manifest['files']),'visuals':labs,'question_occurrences':questions,'protected_questions':protected,'result':'PASS'},ensure_ascii=False))
