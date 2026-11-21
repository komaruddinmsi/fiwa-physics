"""Latihan beralasan untuk gerbang F.MEK.1-pra dan F.MEK.2; bukan kutipan RPP."""
from math import hypot,atan2,pi
from copy import deepcopy
LABELS=['Apa yang ditanyakan','Formulasi yang digunakan','Informasi distraktor (tidak diperlukan)','Identifikasi data','Substitusi nilai ke formula','Penyelesaian','Kesimpulan jawaban']
def make_questions(slug,stage,form=1):
 from lesson_vektor_gerak import make_questions as old
 if stage not in ('P7','P9'):return old(slug,stage,form)
 k=form-1+(0 if stage=='P7' else 4);items=[];place='bengkel alat' if stage=='P7' else 'pangkalan pengamatan'
 def add(ind,prompt,answer,formula,data,sub,solve,conclusion,unit='',diagram=None,level='C4',distractor='Tidak ada data tambahan yang perlu dibuang; arah dan acuan tetap harus dipilih dengan tepat.'):
  goal=prompt.split('?')[0]+('?' if '?' in prompt else '')
  steps=[goal,formula,distractor,data,sub,solve,conclusion]
  items.append(dict(id=f'rpp-{slug}-{stage}-f{form}-{len(items)+1}',indicator=ind,prompt=prompt,kind='num' if not isinstance(answer,tuple) else 'choice',answer=answer[0] if isinstance(answer,tuple) else answer,options=answer[1] if isinstance(answer,tuple) else None,label='Jawaban',unit=unit,tol=.08,level=level,seconds=240,explain=solve+' '+conclusion,steps=[a+': '+b for a,b in zip(LABELS,steps)],**({'diagram':diagram} if diagram else {})))
 if slug=='f-mek-1-pra':
  F=50+10*k
  add('vektor-acuan',f'Di {place}, tali menegang {F} N pada sudut37° terhadap vertikal (sin37°0,6;cos37°0,8). Gulungan sisa tali2 m. Tentukan komponen mendatar dan jelaskan pemilihan sinus.',.6*F,'Fx=F sinθ karena sudut dari vertikal; Fy=F cosθ.',f'F={F} N,θ=37° dari+y; x positifke kanan.',f'Fx={F}×0,6.',f'Fx={.6*F:g} N;√(Fx²+Fy²)=F sebagai cek.',f'Komponen mendatar{.6*F:g} N; bukan0,8F karena acuan bukan+x.','N',distractor='Sisa tali2 m tidak menentukan penguraian satu gaya.')
  a=6+k;b=8+k;R=hypot(a,b)
  add('vektor-sambung',f'Robot {place} berpindah{a} m timur lalu{b} m utara. Operator menjumlahkannya sebagai perpindahan{a+b} m. Berapa besar perpindahan yang benar?',R,'R=√(Rx²+Ry²), sedangkan jarak rute=|A|+|B|.',f'Rx={a},Ry={b}; kedua arah tegak lurus.',f'R=√({a}²+{b}²).',f'R≈{R:.5f} m, lebih kecil daripada{a+b} m.',f'Perpindahan≈{R:.5f} m; klaim operator mencampurkan jarak dan perpindahan.','m',{'kind':'vector','params':dict(ax=a,ay=0,bx=0,by=b)})
  angle=atan2(b,a)*180/pi
  add('vektor-sambung',f'Rute sensor pada {place}: {a} m timur dan{b} m utara. tanθ={b}/{a}; sudut diukur dari timur. Tentukan arah resultan dalam derajat (boleh memakai arctan).',angle,'θ=atan2(Ry,Rx); kuadran ditentukan tanda komponen.',f'Rx={a},Ry={b}; semua komponen positif.',f'θ=arctan({b}/{a}).',f'θ≈{angle:.4f}° di kuadran I.',f'Arah{angle:.4f}° dari timur menuju utara.','°')
  W=100+20*k
  add('vektor-bidang',f'Beban berat{W} N berada di papan37° terhadap mendatar (sin0,6;cos0,8). Teman memilih0,8W sebagai komponen sejajar. Tentukan komponen sejajar bidang.',.6*W,'W∥=W sinα dan W⊥=W cosα; berat tetap vertikal.',f'W={W} N,α=37°; arah sejajar positif menurun.',f'W∥={W}×0,6.',f'W∥={.6*W:g} N; W⊥={.8*W:g} N, kedua komponen merekonstruksiW.',f'Komponen sejajar{.6*W:g} N;0,8W adalah komponen tegak lurus.','N',{'kind':'incline','params':dict(W=W,theta=37)})
  add('vektor-tanda',f'Gaya pada kait {place}: {F} N timur, {F-12} N barat dan16 N utara. Cari besar gaya gabungan.',20,'ΣFx=Ftimur−Fbarat;ΣFy=Futara;R=√(ΣFx²+ΣFy²).',f'Ftimur={F},Fbarat={F-12},Futara16 N.',f'Rx={F}−{F-12}=12;Ry=16;R=√(12²+16²).','R=20 N, bukan penjumlahan besar semua gaya.','Resultan20 N ke timur-laut.','N')
  add('vektor-acuan','Satu vektor sama dinyatakan53° dari+x atau37° dari+y. Bila besarnya50 N, berapa komponen+y? sin53°0,8;cos37°0,8.',40,'Fy=F sin53°=F cos37°; acuan berbeda tidak mengubah vektor.','F50 N; kedua sudut saling berkomplemen.','Fy=50×0,8.','Fy40 N pada kedua cara.','Ganti acuan sudut, bukan menukar arti arah komponen.','N',level='C3')
  add('vektor-tanda',f'Rute alat: vektorA=({a},−{b}) m danB=(−{a-3},{b+4}) m. Berapa besarA+B?',5,'Penjumlahan dilakukan per komponen dengan tanda.',f'Ax{a},Ay−{b},Bx−{a-3},By{b+4}.',f'Rx={a}−{a-3}=3;Ry=−{b}+{b+4}=4.','R=√(3²+4²)=5 m.','Resultan5 m, bukan jumlah semua besar komponen.','m')
  add('vektor-bidang',f'Papan untuk beban{W} N diubah dari30° menjadi60°. Berapa perubahan komponen sejajar, nilai akhir dikurangi awal? sin30°0,5;sin60°≈0,866.',.366*W,'ΔW∥=W(sin60°−sin30°).',f'Berat tetap{W} N; yang berubah hanya sudut bidang.',f'ΔW∥={W}(0,866−0,5).',f'ΔW∥={.366*W:g} N positif.',f'Komponen menurun bertambah{.366*W:g} N; berat total tetap.','N')
  add('vektor-sambung','Dua perpindahan masing-masing5 m: A timur, B barat. Besar resultan dan jarak rute berbeda. Berapa jarak rutenya?',10,'Jarak rute=jumlah panjang ruas; resultan=jumlah vektor.','A(+5,0),B(−5,0).','s=5+5;R=|5−5|.','s10 m danR0 m.','Jarak10 m tidak berarti perpindahan10 m.','m',level='C3')
  add('vektor-acuan','Vektor gaya50 N membentuk127° dari+x; cos127°=−0,6 dan sin127°=0,8. Tentukan komponen mendatar bertandanya.',-30,'Fx=F cosθ; tanda mengikuti kuadran.','θ127° berada dikuadranII.','Fx=50(−0,6).','Fx=−30 N, Fy=+40 N.','Komponen mendatar30 N ke kiri.','N')
 else:
  m=4+k;F=40+2*k;a=2
  add('gerak-massa',f'Troli{place} bermassa{m} kg bertambah kecepatan dari1 menjadi5 m/s dalam2 s. Tarikan mendatar{F} N. Berapa gaya hambatan, jika kanan positif?',F-m*a,'a=Δv/Δt;F−f=ma sehingga f=F−ma.',f'm{m} kg;v01;v5;t2;F{F} N.',f'a=(5−1)/2=2;f={F}−{m}×2.',f'f={F-m*a} N ke kiri.',f'Hambatan{F-m*a} N; kecepatan tidak ditambahkan sebagai gaya.','N')
  m=10+k;pull=20+2*k;N=10*m-.5*pull
  add('gerak-neto',f'Peti{m} kg ditarik{pull} N,30° ke atas dari mendatar (sin0,5), tetap menyentuh lantai dan tanpa percepatan vertikal. Tentukan normal lantai.',N,'ΣFy=N+Fsinθ−mg=0.',f'm{m},F{pull},g10,θ30°;ay0.',f'N={m}×10−{pull}×0,5.',f'N={N:g} N; komponen tarik atas mengurangi normal.',f'Normal{N:g} N, bukan otomatismg.','N')
  a=(.8*pull-4)/m
  add('gerak-massa',f'Peti{m} kg menerima tarikan miring{pull} N (cosθ0,8) dan gesek4 N ke kiri. Berapa percepatan mendatarnya?',a,'ΣFx=Fcosθ−f=ma.',f'F{pull},cosθ0,8,f4,m{m}.',f'a=({pull}×0,8−4)/{m}.',f'a≈{a:.5f} m/s² ke kanan.',f'Percepatan mengikuti resultan, bukan F/m sebelum komponen dipilih.','m/s²')
  add('gerak-neto',f'Peti{m} kg ditarik mendatar30 N dengan kecepatan tetap. Berapa koefisien gesek kinetik? g10.',30/(m*10),'ax0: f=30;ay0:N=mg;μk=f/N.',f'm{m},F30,v tetap,g10.',f'μk=30/({m}×10).',f'μk={30/(m*10):.5f}, tanpa satuan.',f'Normal dan gesek berasal dari dua persamaan arah berbeda.','')
  F=60+6*k
  add('gerak-pasangan',f'Dua papan beroda bermassa30 dan60 kg saling mendorong. Papan30 kg dipercepat{F/30:g} m/s². Berapa besar percepatan papan60 kg akibat interaksi itu?',F/60,'Fpasangan sama besar;F=m1a1=m2|a2|.','m130,m260;abaikanhambatan.',f'F=30×{F/30:g}={F};|a2|={F}/60.',f'|a2|={F/60:g} m/s² dengan arah berlawanan.',f'Gaya sama besar tidak berarti percepatan sama.','m/s²')
  add('gerak-pasangan',f'Dua kereta3 dan2 kg bersentuhan di rel licin. Kereta3 kg didorong{F} N dan menekan kereta2 kg. Tentukan gaya kontak pada kereta2 kg.',2*F/5,'asistem=F/(m1+m2);Fkontak=m2a.',f'm13,m22,F{F};hanyakereta3 didorongdari luar.',f'a={F}/5;Fkontak=2×{F}/5.',f'Fkontak={2*F/5:g} N; bukan seluruh F.',f'Pilih sistem gabungan untuk a lalu sistem kereta2 untuk kontak.','N')
  m=50+5*k
  add('gerak-neto',f'Beban{m} kg dalam lift berubah dari diam menjadi4 m/s ke atas dalam2 s. Tentukan gaya normal. g10.',12*m,'a=Δv/Δt;N−mg=ma.',f'm{m},a=(4−0)/2=2,g10.',f'N={m}(10+2).',f'N={12*m} N, lebih besar darimg.',f'Kecepatan dan percepatan sama arah di sini; bukan menambah gaya gerak baru.','N')
  add('gerak-pemberi','Sebuah kereta bergerak ke kanan tetapi melambat di rel mendatar. Gaya normal dan berat seimbang. Gaya mendatar neto6 N bekerja. Pilih pernyataan yang dapat dipertanggungjawabkan.',(1,['Ada gaya gerak ke kanan yang selalu lebih besar.','Resultan6 N ke kiri; sumber interaksi seperti gesekan harus diidentifikasi.','Resultan nol karena kereta masih bergerak.']),'Percepatan mengikuti perubahan kecepatan; setiap gaya perlu sumber interaksi.','v kanan menurun; a berarah kiri.','ΣFx=ma<0 pada arah kanan positif.','Gaya neto kiri memperkecil v kanan; gerak bukan sumber gaya.','Pilihan kedua tepat.','',level='C4')
  add('gerak-pemberi','Pada diagram satu lampu yang diam tergantung satu tali vertikal, pilih kumpulan gaya yang tepat.',(0,['Tarikan Bumi pada lampu dan tarikan tali pada lampu.','Berat lampu dan tarikan lampu pada Bumi.','Tarikan tali pada lampu dan tarikan lampu pada tali.']),'Diagram satu benda hanya berisi gaya yang diterima benda itu.','Sistem lampu; sumberBumi dan tali.','ΣFy=T−mg=0.','Dua gaya pada lampu saling menyeimbangkan; pasangan reaksinya bekerja pada benda lain.','Pilihan pertama memuat semua dan hanya gaya pada lampu.','',level='C4')
  add('gerak-massa','Sebuah benda meluncur turun bidang37° (sin0,6;cos0,8), koefisien gesek kinetik0,25; g10. Tentukan percepatan sepanjang bidang, turun positif.',4,'ΣF∥=mg sinθ−μmg cosθ=ma.','Gesek ke atas; normalmgcosθ pada model tanpa gaya tambahan.','a=10(0,6−0,25×0,8).','a=4 m/s²; massa saling menghilangkan.','Percepatan menurun4 m/s² dalam model yang dinyatakan.','m/s²')
 if stage=='P9':
  # Konteks, angka dan urutan representasi berbeda dari latihan; cakupan tetap.
  items=items[:8]
  for q in items:q['prompt']='Pada evaluasi rancangan baru, '+q['prompt'].replace('bengkel alat','pangkalan pengamatan')
 return deepcopy(items)
