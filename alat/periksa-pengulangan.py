"""Audit kasus, pertanyaan, pembahasan utuh dan paragraf panjang antartahap. Rumus/label UI dikecualikan."""
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
import json,re,sys,html
ROOT=Path(__file__).resolve().parents[1]
class Read(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.items=[];self.capture=[]
 def handle_starttag(self,tag,attrs):
  if tag in ('br','hr','img','input','meta','link','source','wbr'):return
  a=dict(attrs);classes=set(a.get('class','').split());self.stack.append((tag,classes))
  if tag=='p' or 'solution-seven'in classes:self.capture.append([len(self.stack),[],'solution'if'solution-seven'in classes else'paragraph',classes,any('class-worked'in c for t,c in self.stack)])
 def handle_data(self,s):
  for c in self.capture:c[1].append(s)
 def handle_endtag(self,tag):
  end=next((i for i in range(len(self.stack)-1,-1,-1)if self.stack[i][0]==tag),len(self.stack))
  for c in self.capture[:]:
   if c[0]>end:
    text=re.sub(r'\s+',' ',''.join(c[1])).strip();self.items.append((c[2],text,c[3],c[4]));self.capture.remove(c)
  self.stack=self.stack[:end]
 def handle_startendtag(self,tag,attrs):pass
def stage(path):
 parts=path.parts
 if'P4'in parts:return 'P4-'+path.stem if path.stem!='index' else'P4'
 return next((p for p in parts if re.fullmatch(r'P\d+[ab]?|L\d|pembuka|bacaan',p)),'other')
def audit(root):
 groups=defaultdict(list);blocks=0
 for base in [root/'konten/f-mek',root/'konten/f-use',root/'media-f-mek/bacaan',root/'media-f-use/bacaan']:
  for p in base.rglob('*.html'):
   parser=Read();parser.feed(p.read_text(encoding='utf8'));relative=p.relative_to(root)
   match=re.search(r'window.FIWA_CLASS=(.*?);</script>',p.read_text(encoding='utf8'))
   if match:
    cfg=json.loads(match[1])
    for focus in cfg.get('focusSets',[]):
     for q in focus['questions']:parser.items.append(('question',q['prompt'],set(),False))
   for kind,text,classes,worked in parser.items:
    if len(text)<100 and kind!='question' and 'q-prompt'not in classes:continue
    # Operational messages are shared interface text, not separate learning cases.
    if any(text.startswith(x)for x in ['Kerjakan mandiri.','Alokasi waktu','Penjelasan, ilustrasi, rangkuman','Latihan singkat ini','Kembali ke soal gerbang','Susun jawaban sendiri','Bagian ini terbuka','Tinjau bekal','Prediksi dahulu, gerakkan model','Amati model. Simpan','Satu gerbang','Amati fenomenanya, lalu','Selesaikan seluruh','Tunjukkan','Sesudah semua tepat']):continue
    key=re.sub(r'\s+',' ',html.unescape(text)).strip().casefold();groups[(kind,key)].append({'file':relative.as_posix(),'stage':stage(relative)});blocks+=1
 duplicates=[{'kind':k[0],'text':k[1],'places':v}for k,v in groups.items()if len(set(x['stage']for x in v))>1]
 unit=json.loads((root/'alat/bank/unit_contract.json').read_text(encoding='utf8'))
 unit_dups=[]
 for topic,c in unit.items():
  for a,b in zip(c['practice'],c['real']):
   if a['stimulus']==b['stimulus']or a['pembahasan']==b['pembahasan']:unit_dups.append({'topic':topic,'no':a['no']})
 return {'blocks_checked':blocks,'cross_stage_duplicates':duplicates,'unit_pair_duplicates':unit_dups}
if __name__=='__main__':
 root=Path(sys.argv[1])if len(sys.argv)>1 else ROOT;result=audit(root)
 output=Path(sys.argv[2])if len(sys.argv)>2 else None
 if output:output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'blocks':result['blocks_checked'],'cross_stage_duplicates':len(result['cross_stage_duplicates']),'unit_pair_duplicates':len(result['unit_pair_duplicates']),'samples':result['cross_stage_duplicates'][:10]},ensure_ascii=False))
 sys.exit(bool(result['cross_stage_duplicates']or result['unit_pair_duplicates']))
