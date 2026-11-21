/* Model fisika dan gambar SVG. Besaran dihitung dari satu sumber yang juga diuji di Node. */
(function (global) {
  'use strict';
  const G=10, rad=x=>x*Math.PI/180, finite=(x,d=0)=>Number.isFinite(Number(x))?Number(x):d;
  const defaults={
    vector:{ax:3,ay:0,bx:0,by:4},components:{F:50,theta:37,ref:'x'},incline:{W:100,theta:30},
    motion:{right:24,left:8,m:4,v0:2,t:1},reaction:{F:80,m1:40,m2:20,t:1},
    torque:{F:40,r:1,theta:90},couple:{F:30,d:.8},cable:{W:120,theta:37,fraction:1,L:2},
    work:{F:40,s:4,theta:60},kinetic:{m:2,v:6},potential:{m:2,h:4,ref:0},
    workenergy:{F:-5,s:4,m:2,v0:6},energy:{m:2,h0:6,h:2,mu:0,s:3,v0:0,shape:'valley',mode:'ideal'}
  };
  function calculate(kind,input={}) {
    if(!defaults[kind])throw Error('Model visual belum terdaftar: '+kind);
    const p={...defaults[kind],...input};for(const key in defaults[kind])if(typeof defaults[kind][key]==='number')p[key]=finite(p[key],defaults[kind][key]);
    let v={};const m=Math.max(.01,p.m||1);
    if(kind==='vector'){const x=p.ax+p.bx,y=p.ay+p.by;v={x,y,R:Math.hypot(x,y),angle:Math.atan2(y,x)*180/Math.PI,path:Math.hypot(p.ax,p.ay)+Math.hypot(p.bx,p.by)};}
    if(kind==='components')v={x:p.F*Math.cos(rad(p.theta)),y:p.F*Math.sin(rad(p.theta)),shownAngle:p.ref==='y'?90-p.theta:p.theta};
    if(kind==='incline')v={parallel:p.W*Math.sin(rad(p.theta)),normal:p.W*Math.cos(rad(p.theta))};
    if(kind==='motion'){const F=p.right-p.left,a=F/m;v={F,a,velocity:p.v0+a*p.t,x:p.v0*p.t+.5*a*p.t*p.t,weight:m*G};}
    if(kind==='reaction')v={force1:-p.F,force2:p.F,a1:-p.F/Math.max(.01,p.m1),a2:p.F/Math.max(.01,p.m2)};
    if(kind==='torque')v={arm:p.r*Math.sin(rad(p.theta)),tau:p.F*p.r*Math.sin(rad(p.theta))};
    if(kind==='couple')v={Fnet:0,tau:p.F*p.d};
    if(kind==='cable'){const sine=Math.sin(rad(p.theta)),singular=Math.abs(sine)<1e-8,zeroMoment=Math.abs(p.W*p.fraction*p.L)<1e-8,T=singular?null:p.W*p.fraction/sine;v={T,Rx:T==null?null:T*Math.cos(rad(p.theta)),Ry:T==null?(zeroMoment?p.W:null):p.W-T*sine,loadMoment:p.W*p.fraction*p.L,cableCase:singular?(zeroMoment?'undetermined':'impossible'):'determined'};}
    if(kind==='work')v={Fx:p.F*Math.cos(rad(p.theta)),W:p.F*p.s*Math.cos(rad(p.theta))};
    if(kind==='kinetic')v={K:.5*m*p.v*p.v,doubleK:.5*m*(2*p.v)**2};
    if(kind==='potential')v={h:p.h-p.ref,U:m*G*(p.h-p.ref)};
    if(kind==='workenergy'){const K0=.5*m*p.v0**2,stationary=K0===0&&p.F===0,stop=stationary?0:p.F<0?K0/-p.F:Infinity,actualS=Math.min(p.s,stop),K=Math.max(0,K0+p.F*actualS);v={K0,actualS,W:p.F*actualS,K,v:Math.sqrt(2*K/m),reachable:p.s<=stop+1e-9,stop};}
    if(kind==='energy'){
      const initial=m*G*p.h0+.5*m*p.v0**2,U=m*G*p.h,friction=p.mode==='friction'?Math.max(0,p.mu*m*G):0,requiredThermal=friction*p.s;
      const actualS=initial<=1e-10?0:friction>0?Math.min(p.s,initial/friction):p.s,thermal=friction*actualS,left=Math.max(0,initial-thermal),available=left-U;
      const reachable=available>=-1e-9&&actualS>=p.s-1e-9&&(initial>1e-10||(p.s===0&&p.h===p.h0));
      const actualU=reachable?U:Math.min(U,left),K=reachable?Math.max(0,available):0;
      v={initial,U0:m*G*p.h0,K0:.5*m*p.v0**2,U,actualU,thermal,requiredThermal,actualS,K,v:reachable?Math.sqrt(2*K/m):null,reachable,deficit:Math.max(0,U+requiredThermal-initial),total:actualU+thermal+K};
    }
    for(const key in v)if(typeof v[key]==='number'&&Math.abs(v[key])<1e-10)v[key]=0;
    return {p,v};
  }
  const blue='#1969b3',orange='#a9581b',green='#16745d',ink='#203b5b',grid='#bfd0df',purple='#7250a0';
  const fmt=(x,d=2)=>x==null?'—':Number(x).toLocaleString('id-ID',{maximumFractionDigits:d});
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const line=(x1,y1,x2,y2,color=ink,width=3,dash='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}"${dash?` stroke-dasharray="${dash}"`:''}/>`;
  const text=(x,y,t,color=ink,size=26)=>`<text x="${x}" y="${y}" fill="${color}" font-size="${size}" font-family="Nunito,Segoe UI,sans-serif">${esc(t)}</text>`;
  const rect=(x,y,w,h,fill='#d4e7f7')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="${fill}" stroke="${ink}" stroke-width="2"/>`;
  const circle=(x,y,r,fill=blue)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${ink}" stroke-width="2"/>`;
  function arrow(x,y,dx,dy,color=blue,label='') {
    if(Math.hypot(dx,dy)<.1)return circle(x,y,3,color)+(label?text(x+12,y-12,label,color):'');
    const a=Math.atan2(dy,dx),xx=x+dx,yy=y+dy,head=10;
    return line(x,y,xx,yy,color,4)+`<path d="M${xx} ${yy}L${xx-head*Math.cos(a-.45)} ${yy-head*Math.sin(a-.45)}M${xx} ${yy}L${xx-head*Math.cos(a+.45)} ${yy-head*Math.sin(a+.45)}" stroke="${color}" stroke-width="4" fill="none"/>`+(label?text(Math.max(8,Math.min(520,xx+8)),Math.max(27,Math.min(320,yy-9)),label,color):'');
  }
  const poly=(points,color=blue,width=4)=>`<polyline points="${points.map(p=>p.join(',')).join(' ')}" stroke="${color}" stroke-width="${width}" fill="none"/>`;
  function arc(x,y,r,start,end,color=orange){const a=rad(start),b=rad(end),delta=end-start;return `<path d="M${x+r*Math.cos(a)} ${y+r*Math.sin(a)}A${r} ${r} 0 ${Math.abs(delta)>180?1:0} ${delta>=0?1:0} ${x+r*Math.cos(b)} ${y+r*Math.sin(b)}" fill="none" stroke="${color}" stroke-width="3"/>`;}
  function draw(kind,input,options={}) {
    const {p,v}=calculate(kind,input),isStatic=!!options.static;
    let s=rect(2,2,636,336,'#eaf1f7'),title='Diagram '+kind;
    if(kind==='vector'){
      const extent=Math.max(4,Math.abs(p.ax),Math.abs(p.ay),Math.abs(p.bx),Math.abs(p.by),Math.abs(v.x),Math.abs(v.y)),k=120/extent,ox=300,oy=175;
      for(let i=-4;i<=4;i++){s+=line(50,oy+i*30,600,oy+i*30,grid,1)+line(ox+i*30,40,ox+i*30,310,grid,1);}
      s+=arrow(50,oy,550,0,ink,'x')+arrow(ox,310,0,-275,ink,'y');
      s+=arrow(ox,oy,p.ax*k,-p.ay*k,blue,'A');
      if(isStatic)s+=arrow(ox,oy,p.bx*k,-p.by*k,orange,'B');
      else s+=arrow(ox+p.ax*k,oy-p.ay*k,p.bx*k,-p.by*k,orange)+text(ox+(p.ax+p.bx*.5)*k+10,oy-(p.ay+p.by*.5)*k-18,'B',orange)+arrow(ox,oy,v.x*k,-v.y*k,green)+text(ox+v.x*k*.5-24,oy-v.y*k*.5+26,'R',green);
      title=isStatic?'Dua vektor masukan; resultan belum digambar':'Penjumlahan ujung ke pangkal; resultan dari titik awal ke titik akhir';
    }else if(kind==='components'){
      const k=210/Math.max(100,p.F),x=310,y=275,dx=v.x*k,dy=-v.y*k;
      s+=arrow(40,y,530,0,ink,'x')+arrow(x,300,0,-270,ink,'y');
      if(!isStatic)s+=line(x+dx,y,x+dx,y+dy,grid,2,'6 5')+line(x,y+dy,x+dx,y+dy,grid,2,'6 5');
      s+=arrow(x,y,dx,dy,blue)+text(Math.max(12,x+dx+10),Math.max(28,y+dy-30),'F',blue)+arc(x,y,42,p.ref==='y'?-90:0,-p.theta);
      if(!isStatic&&Math.abs(v.x)>1e-8&&Math.abs(v.y)>1e-8)s+=arrow(x,y,dx,0,orange)+text(x+dx-40,y+30,'Fx',orange)+arrow(x,y,0,dy,green)+text(x+20,y+dy+25,'Fy',green);
      s+=text(35,42,p.ref==='y'?'Acuan sudut: sumbu y':'Acuan sudut: sumbu x',ink,23)+text(35,78,'Sudut = '+fmt(v.shownAngle)+'°',ink,23);
      title='Gaya dan dua komponen tegak lurus dengan acuan sudut yang dinyatakan';
    }else if(kind==='incline'){
      const a=rad(p.theta),cx=325,cy=170,c=Math.cos(a),sin=Math.sin(a),scale=80/Math.max(200,p.W),half=Math.min(240,100/Math.max(.01,Math.abs(sin))),lx=cx-half*c,ly=cy+half*sin;
      s+=line(lx,ly,cx+half*c,cy-half*sin,ink,5)+line(lx,ly,lx+115,ly,grid,2,'5 5')+arc(lx,ly,38,0,-p.theta);
      const travel=(options.inclineDistance||0)*25;
      s+=`<g transform="translate(${cx-travel*c},${cy-12+travel*sin}) rotate(${-p.theta})">${rect(-32,-27,64,36)}</g>`;
      s+=`<g transform="translate(${-travel*c},${travel*sin})">`;
      s+=arrow(cx,cy,0,p.W*scale,blue)+text(cx-40,cy+p.W*scale+27,!isStatic&&Math.abs(v.parallel)<1e-8?'W = W⊥':!isStatic&&Math.abs(v.normal)<1e-8?'W = W∥':'W',blue);
      if(!isStatic&&Math.abs(v.parallel)>1e-8&&Math.abs(v.normal)>1e-8)s+=arrow(cx,cy,-v.parallel*c*scale,v.parallel*sin*scale,orange)+text(cx-100,cy-24,'W∥',orange)+arrow(cx,cy,v.normal*sin*scale,v.normal*c*scale,green)+text(cx+v.normal*sin*scale+15,cy+v.normal*c*scale-10,'W⊥',green);
      s+='</g>';s+=text(32,42,'θ = '+fmt(p.theta)+'°',ink,24);title='Berat vertikal diuraikan pada sumbu sejajar dan tegak lurus bidang';
    }else if(kind==='motion'){
      const base=options.base||p,T=base.t||1,a=(base.right-base.left)/base.m,end=base.v0*T+.5*a*T*T,turn=a?(-base.v0/a):0,peak=turn>0&&turn<T?base.v0*turn+.5*a*turn*turn:0,span=Math.max(Math.abs(end),Math.abs(peak),1);const pos=isStatic?320:320+140*v.x/span,forceScale=90/Math.max(p.right,p.left,50);
      s+=line(35,265,605,265,ink,4)+rect(pos-42,195,84,54)+circle(pos-25,258,8,ink)+circle(pos+25,258,8,ink);
      s+=arrow(pos+45,215,p.right*forceScale,0,blue,'F kanan')+arrow(pos-45,232,-p.left*forceScale,0,orange)+text(Math.max(20,pos-170),195,'F kiri',orange,23);
      s+=arrow(pos,210,0,85,purple,'W')+arrow(pos,195,0,-85,purple,'N');
      if(!isStatic)s+=arrow(pos,75,Math.max(-130,Math.min(130,v.velocity*10)),0,green,'v');
      s+=text(30,42,'t = '+fmt(p.t)+' s',ink,24)+text(30,80,'m = '+fmt(p.m)+' kg',ink,24);
      title='Dua gaya horizontal pada satu benda; arah kecepatan dibedakan dari arah percepatan';
    }else if(kind==='reaction'){
      const d1=isStatic?0:.5*v.a1*p.t*p.t,d2=isStatic?0:.5*v.a2*p.t*p.t,k=160/Math.max(.5*Math.abs(v.a1)*(options.base?.t||p.t)**2,.5*Math.abs(v.a2)*(options.base?.t||p.t)**2,1),x1=245+d1*k,x2=395+d2*k;
      s+=line(30,265,610,265,blue,3);
      for(const [x,m,color] of [[x1,p.m1,blue],[x2,p.m2,orange]])s+=(p.object==='boat'?`<path d="M${x-45} 232h90l-15 24h-60z" fill="${color}"/>`:`<rect x="${x-45}" y="232" width="90" height="12" rx="4" fill="${color}"/>`+circle(x-28,251,7,ink)+circle(x+28,251,7,ink))+circle(x,199,16,'#d2b49b')+line(x,215,x,235,ink,8)+text(x-35,300,fmt(m)+' kg',ink,22);
      s+=arrow(x1,150,-Math.min(100,p.F*.8),0,blue,'F₁')+arrow(x2,150,Math.min(100,p.F*.8),0,orange,'F₂');
      s+=text(35,40,'Satu interaksi, dua benda',ink,25);title='Pasangan gaya sama besar dan berlawanan arah pada dua benda berbeda';
    }else if(kind==='torque'){
      const x=110+p.r*340/Math.max(2,p.r),y=220,a=rad(p.theta),len=Math.min(100,p.F*1.1);
      s+=line(110,y,520,y,ink,12)+`<path d="M90 256l20-36 20 36z" fill="${ink}"/>`+circle(110,y,7,orange);
      s+=arrow(x,y,len*Math.cos(a),-len*Math.sin(a),blue)+text(Math.min(560,x+42),y-42,'F',blue)+line(110,285,x,285,orange,3)+text(150,315,'r = '+fmt(p.r)+' m',ink,23)+text(28,42,'Sudut gaya = '+fmt(p.theta)+'°',ink,24);
      title='Gaya pada batang dengan poros, jarak, dan sudut yang jelas';
    }else if(kind==='couple'){
      const x1=320-p.d*180/Math.max(1.5,p.d),x2=320+p.d*180/Math.max(1.5,p.d),length=Math.min(125,p.F*1.8);
      s+=rect(100,145,440,45)+arrow(x1,168,0,length,blue,'F')+arrow(x2,168,0,-length,orange,'F');
      s+=line(x1,280,x2,280,green,3)+text(245,318,'d = '+fmt(p.d)+' m',ink,23)+text(25,42,'Garis kerja dapat dipisahkan',ink,24);
      title='Dua gaya berlawanan pada garis berbeda dapat menghasilkan pasangan momen';
    }else if(kind==='cable'){
      const a=rad(p.theta),vertical=Math.abs(Math.cos(a))<1e-6,length=vertical?320:Math.min(340,175/Math.max(.1,Math.tan(a))),x=120,y=230,end=x+length,load=x+length*p.fraction,top=vertical?55:y-length*Math.tan(a),max=Math.max(p.W,v.T||0,1),scale=60/max,anchorX=vertical?end:x;
      s+=line(105,25,105,290,ink,8)+line(x,y,end,y,ink,9)+line(anchorX,top,end,y,green,4)+circle(x,y,8,orange)+rect(load-16,y+10,32,26,'#e6bf81');
      s+=arrow(load,y+38,0,isStatic?48:p.W*scale,orange,'W');
      if(v.T!=null)s+=arrow(end,y,-(isStatic?65:v.T*scale)*Math.cos(a),-(isStatic?65:v.T*scale)*Math.sin(a),blue,'T');
      if(!isStatic&&v.T!=null){s+=arrow(x,y,Math.max(-75,Math.min(75,v.Rx*scale)),0,purple,'Rx')+arrow(x,y,0,-Math.max(-70,Math.min(70,v.Ry*scale)),purple,'Ry');s+=line(end,y,end-Math.cos(a)*v.T*scale,y,grid,2,'4 4')+line(end-Math.cos(a)*v.T*scale,y,end-Math.cos(a)*v.T*scale,y-Math.sin(a)*v.T*scale,grid,2,'4 4');}
      s+=text(30,42,'θ = '+fmt(p.theta)+'°',ink,24)+text(140,310,'L = '+fmt(p.L)+' m',ink,23);
      title='Batang berengsel dengan beban dan kabel miring; geometri dipertahankan saat gambar menyesuaikan ukuran';
    }else if(kind==='work'){
      const x=options.workX||175,y=190,a=rad(p.theta);
      s+=line(40,252,595,252,ink,3)+rect(x-35,y-25,70,54);
      s+=arrow(x,y,Math.min(135,p.F*1.4)*Math.cos(a),-Math.min(135,p.F*1.4)*Math.sin(a),blue,'F')+arrow(x,285,p.s*310/Math.max(10,p.s),0,orange,'s');
      s+=text(30,43,'θ = '+fmt(p.theta)+'°',ink,24)+text(30,80,'F = '+fmt(p.F)+' N',ink,24);title='Gaya dan perpindahan: sudut diukur antara dua arah tersebut';
    }else if(kind==='kinetic'){
      s+=line(25,265,260,265,ink,3)+circle(options.kineticX||105,215,15+Math.sqrt(p.m)*5,blue)+arrow(options.kineticX||105,165,p.v*8,0,orange,'v');
      s+=arrow(310,280,280,0,ink,'v')+arrow(310,280,0,-240,ink,'Ek');
      const vmax=Math.max(15,p.v),emax=Math.max(600,.5*p.m*vmax*vmax*1.1),points=[];for(let x=0;x<=vmax;x+=vmax/50)points.push([310+x/vmax*255,280-(.5*p.m*x*x)/emax*210]);
      if(!isStatic)s+=poly(points,green,4)+circle(310+p.v/vmax*255,280-v.K/emax*210,6,orange);
      s+=text(35,42,'m = '+fmt(p.m)+' kg',ink,24);title='Kecepatan benda dan grafik energi kinetik terhadap kelajuan';
    }else if(kind==='potential'){
      const lo=Math.min(0,p.h,p.ref),hi=Math.max(10,p.h,p.ref),yy=value=>295-(value-lo)/(hi-lo)*240,base=yy(0),hY=yy(p.h),rY=yy(p.ref);
      s+=line(45,base,585,base,ink,4)+line(45,rY,585,rY,green,3,'7 5')+circle(240,hY,18,blue)+line(275,rY,275,hY,orange,3);
      s+=text(300,hY,'h benda = '+fmt(p.h)+' m',ink,23)+text(45,Math.max(30,rY-12),'Acuan = '+fmt(p.ref)+' m',green,23);
      title='Benda dan garis acuan ketinggian; energi potensial dapat positif, nol atau negatif';
    }else if(kind==='workenergy'){
      const stop=Number.isFinite(v.stop)?v.stop:10,actual=isStatic?0:v.actualS,k=380/Math.max(10,p.s,Math.min(stop,100));
      s+=line(30,250,600,250,ink,3)+rect(70+actual*k,195,55,45)+arrow(95+actual*k,175,Math.sign(p.F)*Math.min(110,Math.abs(p.F)*2),0,blue,'F neto');
      s+=line(95+p.s*k,85,95+p.s*k,270,orange,2,'5 5');
      s+=text(30,42,'Jarak diminta = '+fmt(p.s)+' m',ink,24);
      if(!isStatic)s+=text(30,80,v.reachable?'Gerak pada posisi ini terjangkau':'Benda berhenti sebelum posisi itu',v.reachable?green:orange,23);
      title='Usaha neto mengubah energi kinetik; model memeriksa apakah posisi dapat dicapai';
    }else if(kind==='energy'){
      const base=options.base||p,hmax=Math.max(10,base.h0,base.h),floor=270,y0=floor-base.h0/hmax*200,y=floor-base.h/hmax*200;
      const points=typeof global.FIWA_ANIMATION!=='undefined'?global.FIWA_ANIMATION.energyPoints(base).points:[[60,y0],[200,floor],[400,floor],[575,y]];
      s+=poly(points,ink,5)+circle(60,y0-16,12,'#d4e7f7')+line(60,y0,60,floor,grid,2,'5 5')+circle(575,y-18,12,'#fff')+line(575,y,575,floor,grid,2,'5 5');
      if(options.body)s+=circle(options.body[0],options.body[1]-16,14,orange);
      else if(!isStatic)s+=circle(60,y0-16,14,orange);
      s+=text(25,40,'Awal '+fmt(base.h0)+' m',ink,24)+text(395,75,'Tujuan '+fmt(base.h)+' m',ink,23);
      if(base.mode==='friction'&&base.s>0)s+=rect(220,floor+2,160,9,'#d6a67d')+text(180,330,'segmen kasar '+fmt(base.s)+' m',ink,21);
      title='Lintasan turun, kasar mendatar, lalu naik. Gerak dihitung dari energi dan percepatan sepanjang setiap ruas.';

    }
    if(options.turn!=null){const tau=kind==='couple'?v.tau:v.tau,sign=Math.sign(tau),angle=-options.turn*180/Math.PI;
      s+=`<g transform="translate(490 130) rotate(${angle})">${line(-65,0,65,0,green,7)}${circle(65,0,9,orange)}</g>`+circle(490,130,6,ink)+text(390,35,sign===0?'Momen nol':'Arah putar',ink,23);
    }
    if(options.construct!=null){const progress=Math.max(.01,options.construct);s=s.replace(/<(line|path|polyline)\b/g,(_,tag)=>`<${tag} pathLength="100" style="stroke-dasharray:100;stroke-dashoffset:${100*(1-progress)}"`);}
    return `<svg class="physics-svg" viewBox="0 0 640 340" role="img" aria-label="${esc(title)}">${s}</svg>`;
  }
  const controlMap={
    vector:[['ax','Komponen x A','m',-10,10,1],['ay','Komponen y A','m',-10,10,1],['bx','Komponen x B','m',-10,10,1],['by','Komponen y B','m',-10,10,1]],
    components:[['F','Besar gaya','N',0,100,1],['theta','Sudut vektor dari +x','°',0,180,5],['ref','Acuan sudut tampilan','select',['x','y']]],
    incline:[['W','Berat','N',20,200,10],['theta','Sudut bidang','°',0,90,1]],
    motion:[['right','Gaya ke kanan','N',0,50,2],['left','Gaya ke kiri','N',0,50,2],['m','Massa','kg',1,40,1],['v0','Kecepatan awal','m/s',-5,5,1],['t','Waktu','s',0,3,.1]],
    reaction:[['F','Gaya interaksi','N',20,100,10],['m1','Massa benda kiri','kg',10,120,5],['m2','Massa benda kanan','kg',10,120,5],['t','Waktu sejak dorongan','s',0,3,.1]],
    torque:[['F','Besar gaya','N',0,100,1],['r','Jarak titik gaya dari poros','m',0,2,.1],['theta','Sudut gaya dari batang','°',-180,180,15]],
    couple:[['F','Besar setiap gaya','N',0,60,5],['d','Jarak antargaris kerja','m',0,1.5,.1]],
    cable:[['W','Berat beban','N',20,400,20],['theta','Sudut kabel terhadap batang','°',15,75,5],['fraction','Letak beban / panjang batang','',0,1,.1],['L','Panjang batang','m',1,4,.5]],
    work:[['F','Besar gaya','N',0,100,1],['s','Perpindahan','m',0,10,.5],['theta','Sudut gaya terhadap perpindahan','°',0,180,15]],
    kinetic:[['m','Massa','kg',.5,5,.5],['v','Kelajuan','m/s',0,15,.5]],
    potential:[['m','Massa','kg',1,5,.5],['h','Tinggi benda dari lantai','m',0,10,.5],['ref','Tinggi acuan nol dari lantai','m',-2,10,.5]],
    workenergy:[['F','Gaya neto sepanjang sumbu','N',-20,40,1],['s','Jarak yang ditinjau','m',0,10,.5],['m','Massa','kg',1,10,1],['v0','Kelajuan awal','m/s',0,10,.5]],
    energy:[['m','Massa','kg',1,5,.5],['h0','Tinggi awal','m',0,10,.05],['h','Tinggi posisi tujuan','m',0,10,.05],['v0','Kelajuan awal','m/s',0,10,.1],['mu','Koefisien gesek segmen mendatar','',0,.4,.01],['s','Panjang segmen kasar mendatar','m',0,10,.5],['mode','Model','select',['ideal','friction']],['shape','Bentuk lintasan','select',['ramp','valley','wave']]]
  };
  const statMap={vector:[['R','Besar resultan','m'],['x','Komponen x hasil','m'],['y','Komponen y hasil','m'],['path','Jumlah panjang lintasan','m']],components:[['x','Komponen x','N'],['y','Komponen y','N'],['shownAngle','Sudut terhadap acuan dipilih','°']],incline:[['parallel','Berat sejajar bidang','N'],['normal','Berat tegak lurus bidang','N']],motion:[['F','Resultan gaya','N'],['a','Percepatan','m/s²'],['velocity','Kecepatan saat ini','m/s'],['x','Perpindahan saat ini','m']],reaction:[['force1','Gaya pada kiri','N'],['force2','Gaya pada kanan','N'],['a1','Percepatan kiri','m/s²'],['a2','Percepatan kanan','m/s²']],torque:[['tau','Momen gaya bertanda','N·m'],['arm','Lengan tegak lurus bertanda','m']],couple:[['Fnet','Resultan gaya','N'],['tau','Momen pasangan gaya','N·m']],cable:[['T','Tegangan kabel','N'],['Rx','Reaksi engsel mendatar','N'],['Ry','Reaksi engsel tegak','N'],['loadMoment','Besar momen beban','N·m']],work:[['Fx','Komponen gaya searah perpindahan','N'],['W','Usaha gaya','J']],kinetic:[['K','Energi kinetik','J'],['doubleK','Energi bila kelajuan dua kali','J']],potential:[['h','Tinggi relatif acuan','m'],['U','Energi potensial','J']],workenergy:[['K0','Energi kinetik awal','J'],['W','Usaha neto pada jarak terjangkau','J'],['K','Energi kinetik akhir','J'],['v','Kelajuan akhir','m/s']],energy:[['initial','Energi awal','J'],['U','Energi potensial saat ini','J'],['thermal','Energi internal aktual','J'],['requiredThermal','Energi gesek sampai posisi ini','J'],['actualS','Jarak segmen yang terlewati','m'],['K','Energi kinetik tersedia','J'],['v','Kelajuan saat ini','m/s']]};
  function ledger(kind,v) {
    const colors={Ek:'#2277ad',Ep:'#467865',Internal:'#a16a2b',Usaha:'#7359a0'};
    const rows=kind==='energy'?[['Awal',[['Ep',v.U0],['Ek',v.K0]]],['Keadaan aktual',[['Ep',v.actualU],['Ek',v.K],['Internal',v.thermal]]]]:kind==='workenergy'?[['Awal',[['Ek',v.K0]]],['Usaha neto bertanda',[['Usaha',v.W]]],['Akhir',[['Ek',v.K]]]]:kind==='kinetic'?[['Energi gerak',[['Ek',v.K]]],['Jika kelajuan dua kali',[['Ek',v.doubleK]]]]:kind==='potential'?[['Terhadap acuan',[['Ep',v.U]]]]:kind==='work'?[['Usaha bertanda',[['Usaha',v.W]]]]:[];
    if(!rows.length)return '';
    const max=Math.max(1,...rows.map(r=>r[1].reduce((a,x)=>a+Math.abs(x[1]||0),0)));
    return '<div class="energy-ledger"><b>Bandingkan energi · J</b>'+rows.map(([name,parts])=>'<div>'+name+': '+parts.map(([key,value])=>key+' '+fmt(value)+' J').join(' + ')+'<div class="energy-bar" aria-hidden="true">'+parts.map(([key,value])=>'<span style="width:'+100*Math.abs(value||0)/max+'%;background:'+colors[key]+';'+(value<0?'background-image:repeating-linear-gradient(135deg,transparent 0 6px,#ffffff66 6px 9px)':'')+'"></span>').join('')+'</div></div>').join('')+'<small>Ek: gerak · Ep: potensial · Internal: akibat gesekan. Batang menunjukkan besar energi; tanda negatif tetap ditulis dan diberi arsiran.</small></div>';
  }
  let nextId=0;
  function zoom(host,cfg,state,id){
    const open=document.createElement('button');open.type='button';open.className='class-button secondary lab-zoom';open.textContent='Perbesar diagram';
    const modal=document.createElement('dialog');modal.className='lab-dialog';modal.setAttribute('aria-label','Diagram fisika diperbesar');modal.innerHTML='<button type="button" class="class-button secondary">Tutup diagram</button><div class="zoom-stage"></div>';
    modal.querySelector('button').addEventListener('click',()=>modal.close());
    open.addEventListener('click',()=>{modal.querySelector('.zoom-stage').innerHTML=draw(cfg.kind,host.__fiwaShown?.params||state,host.__fiwaShown?.options||{static:!!cfg.static})+(cfg.static?'':ledger(cfg.kind,calculate(cfg.kind,host.__fiwaShown?.params||state).v));modal.showModal();});
    host.appendChild(open);host.appendChild(modal);
  }
  function mount(host,config) {
    if(host.dataset.mounted)return;host.dataset.mounted='1';
    let cfg=config;try{if(!cfg)cfg=JSON.parse(host.dataset.physicsLab);}catch(_){host.textContent='Konfigurasi visual tidak dapat dibaca.';return;}
    if(!defaults[cfg.kind]){host.textContent='Model visual belum tersedia.';return;}
    const original={...defaults[cfg.kind],...(cfg.params||{})},state={...original},id='lab-'+(++nextId);
    if(cfg.static){host.innerHTML=draw(cfg.kind,state,{static:true})+`<figcaption>Diagram skematis. Arah, label dan data soal menjadi acuan; panjang panah tidak selalu berskala.</figcaption>`;zoom(host,cfg,state,id);return;}
    if(cfg.readonly){const {v}=calculate(cfg.kind,state);host.innerHTML=draw(cfg.kind,state)+ledger(cfg.kind,v)+'<figcaption>Ilustrasi kondisi pembanding; gerakkan model utama untuk menyelidiki.</figcaption>';return;}
    const controls=controlMap[cfg.kind].map(c=>{
      const [key,label,unit,min,max,step]=c,cid=id+'-'+key;
      if(unit==='select')return `<label for="${cid}">${esc(label)}<select id="${cid}" data-lab-input="${key}">${min.map(v=>`<option value="${v}"${state[key]===v?' selected':''}>${({x:'Sumbu x',y:'Sumbu y',ideal:'Tanpa gesekan',friction:'Dengan segmen kasar',ramp:'Lurus',valley:'Lembah',wave:'Bergelombang'})[v]||v}</option>`).join('')}</select></label>`;
      const actualMin=Math.min(min,finite(state[key])),actualMax=Math.max(max,finite(state[key]));
      return `<label for="${cid}"><span>${esc(label)} <output data-control-value="${key}">${fmt(state[key])} ${unit}</output></span><input type="range" id="${cid}" data-lab-input="${key}" min="${actualMin}" max="${actualMax}" step="any" value="${state[key]}"><input class="lab-number" type="number" min="${actualMin}" max="${actualMax}" step="any" value="${state[key]}" aria-label="Nilai ${esc(label)}" data-lab-number="${key}"></label>`;
    }).join('');
    host.innerHTML=`<div class="lab-stage"></div><div class="lab-controls">${controls}<button type="button" data-lab-reset>Kembalikan kondisi awal</button></div><div class="lab-readouts" aria-live="polite"></div><p class="lab-condition" role="status"></p>`;
    function update(frameParams=null,frameOptions={}){const shown=frameParams||state;host.__fiwaShown={params:{...shown},options:{...frameOptions}};const {v}=calculate(cfg.kind,shown);host.querySelector('.lab-stage').innerHTML=draw(cfg.kind,shown,frameOptions)+ledger(cfg.kind,v);host.querySelector('.lab-readouts').innerHTML=statMap[cfg.kind].map(([key,label,unit])=>`<div><span>${label}</span><output data-result="${key}">${fmt(v[key])} ${unit}</output></div>`).join('');
      const condition=host.querySelector('.lab-condition');condition.textContent=(cfg.kind==='energy'&&!v.reachable)?'Posisi tujuan belum dapat dicapai. Kekurangan energi '+fmt(v.deficit)+' J. Ubah kondisi awal atau kebutuhan lintasan.':(cfg.kind==='workenergy'&&!v.reachable)?'Benda berhenti pada '+fmt(v.stop)+' m. Posisi yang diminta tidak terjangkau dalam model gaya neto tetap ini.':cfg.kind==='cable'&&v.cableCase==='impossible'?'Sudut nol tidak dapat menopang momen beban melalui kabel dalam model ini.':cfg.kind==='components'?(state.ref==='y'?'Sudut dari +y bertanda positif ke arah +x dan negatif ke sisi kiri sumbu y. Perhatikan busur serta tanda komponen.':'Sudut diukur berlawanan arah jarum jam dari +x. Perhatikan busur dan tanda komponen.'):cfg.kind==='cable'&&v.cableCase==='undetermined'?'Momen beban nol. Persamaan momen tidak menentukan besar tegangan kabel mendatar secara tunggal.':'Model diperbarui. Bandingkan gambar, satuan, dan besaran hasil sebelum menyimpulkan.';
      for(const c of controlMap[cfg.kind]){const control=host.querySelector('[data-lab-input="'+c[0]+'"]');if(control)control.value=state[c[0]];const number=host.querySelector('[data-lab-number="'+c[0]+'"]');if(number&&document.activeElement!==number)number.value=state[c[0]];const out=host.querySelector('[data-control-value="'+c[0]+'"]');if(out)out.textContent=fmt(state[c[0]])+' '+c[2];}
    }
    host.addEventListener('input',e=>{const key=e.target.dataset.labInput||e.target.dataset.labNumber;if(key&&e.target.value!==''&&Number.isFinite(Number(e.target.value))){state[key]=Math.max(Number(e.target.min),Math.min(Number(e.target.max),Number(e.target.value)));update();}else if(key&&e.target.tagName==='SELECT'){state[key]=e.target.value;update();}});
    host.addEventListener('change',e=>{const key=e.target.dataset.labNumber;if(key&&e.target.value!==''&&Number.isFinite(Number(e.target.value))){state[key]=Math.max(Number(e.target.min),Math.min(Number(e.target.max),Number(e.target.value)));e.target.value=state[key];update();}});
    host.__fiwaRestore=()=>{host.querySelectorAll('[data-lab-input]').forEach(e=>{state[e.dataset.labInput]=e.tagName==='SELECT'?e.value:Number(e.value);});update();host.dispatchEvent(new CustomEvent('fiwa:lab-restored'));};
    host.querySelector('[data-lab-reset]').addEventListener('click',()=>{Object.assign(state,original);host.querySelectorAll('[data-lab-input]').forEach(e=>{e.value=state[e.dataset.labInput];});update();});
    host.__fiwaState=()=>({kind:cfg.kind,params:{...state}});host.__fiwaRender=(params,options)=>update(params,options);
    update();zoom(host,cfg,state,id);
  }
  const api={calculate,draw,mount,defaults};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  if(typeof document!=='undefined'){global.FIWA_VISUAL=api;const start=()=>{document.querySelectorAll('[data-physics-lab]').forEach(el=>mount(el));document.dispatchEvent(new CustomEvent('fiwa:visual-ready'));};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();}
})(typeof window!=='undefined'?window:globalThis);
