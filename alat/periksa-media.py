"""Validasi media pendukung sesuai kebutuhan tahap, tanpa kewajiban lampiran yang berulang."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
def jalankan(slug):
 data=json.loads((ROOT/f'media-{slug}/media.json').read_text(encoding='utf8'));seen=set();count=0
 for tp,stages in data.get('tp',{}).items():
  for stage,entries in stages.items():
   assert stage not in ('S2','S8','S13') or not entries,(tp,stage,'Bahan pada gerbang')
   for item in entries:
    assert item['tipe'] in ('video','audio','bacaan','simulasi','tautan') and item.get('catatan'),(tp,stage)
    key=(item['tipe'],item.get('yt')or item.get('berkas')or item.get('url')or item.get('naskah'));assert key not in seen,('Media berulang',key);seen.add(key)
    if item.get('berkas'):assert (ROOT/item['berkas']).exists(),item['berkas']
    count+=1
 assert (ROOT/'konten'/slug/'pembuka/index.html').exists()
 print(json.dumps({'topic':slug,'supporting_items':count,'result':'PASS'},ensure_ascii=False));return 0
if __name__=='__main__':sys.exit(jalankan(sys.argv[1] if len(sys.argv)>1 else 'f-mek'))
