"""Periksa kelengkapan berkas situs yang tersisa sebelum unggah per folder. Tidak menulis data."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for key in ('src','href','poster'):
   if a.get(key):self.urls.append(a[key])
checks=0;html_count=0
def exists(url,parent):
 global checks
 u=urlsplit(url)
 if u.scheme or u.netloc or not u.path or '${' in url or '{{' in url:return
 target=(ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else parent/unquote(u.path)).resolve()
 assert target.is_relative_to(ROOT),('Jalur keluar proyek',url)
 assert target.exists(),('Berkas lokal hilang',str(parent.relative_to(ROOT)),url)
 checks+=1
catalog=json.loads((ROOT/'katalog.json').read_text(encoding='utf8'))
def visit(obj):
 if isinstance(obj,dict):
  if obj.get('berkas'):exists(obj['berkas'],ROOT)
  for value in obj.values():visit(value)
 elif isinstance(obj,list):
  for value in obj:visit(value)
visit(catalog)
for path in ROOT.glob('media-*/media.json'):visit(json.loads(path.read_text(encoding='utf8')))
for p in ROOT.rglob('*.html'):
 if 'dokumentasi' in p.parts:continue
 parser=Links();parser.feed(p.read_text(encoding='utf8'));html_count+=1
 for url in parser.urls:exists(url,p.parent)
for p in ROOT.rglob('*.css'):
 for url in re.findall(r'url\(\s*[\'\"]?([^\)\'\"]+)',p.read_text(encoding='utf8')):
  if not url.startswith('var('):exists(url,p.parent)
for i in range(1,5):assert (ROOT/f'aset-ebook/fundamentals-of-physics-halliday-{i}.pdf').is_file()
assert (ROOT/'aset-f-use/GURU_RPP-F.USE.docx').is_file()
assert not (ROOT/'alat/sumber').exists()
assert (ROOT/'aset-f-mek/GURU_RPP-F.MEK.docx').is_file()
assert all(not p.name.startswith('S') for p in ROOT.glob('konten/*/*') if p.is_dir())
assert len(list((ROOT/'konten').rglob('*.html')))==153
assert len(list((ROOT/'konten').rglob('*.json')))==14
print(json.dumps({'result':'PASS','html_checked':html_count,'local_references_checked':checks,'content_html':153,'metadata':14,'halliday_parts':4},ensure_ascii=False))
