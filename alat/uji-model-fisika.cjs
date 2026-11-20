/* Uji nilai acuan dan keadaan batas yang dapat merusak makna diagram. */
const assert=require('node:assert/strict'),{calculate:calc,draw}=require('../assets/kelas-visual.js');
let checks=0;function near(a,b){assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);checks++}
near(calc('vector',{ax:3,ay:0,bx:0,by:4}).v.R,5);
near(calc('vector',{ax:4,ay:-2,bx:-4,by:2}).v.R,0);
near(calc('components',{F:50,theta:90}).v.x,0);
near(calc('incline',{W:100,theta:0}).v.normal,100);
near(calc('incline',{W:100,theta:90}).v.parallel,100);
near(calc('motion',{right:24,left:8,m:4,v0:2,t:2}).v.x,12);
near(calc('reaction',{F:80,m1:40,m2:20}).v.a1,-2);
near(calc('reaction',{F:80,m1:40,m2:20}).v.a2,4);
for(const a of [0,90,180,-90])near(calc('torque',{F:40,r:2,theta:a}).v.tau,80*Math.sin(a*Math.PI/180));
near(calc('couple',{F:30,d:.8}).v.tau,24);
near(calc('cable',{W:180,theta:30,fraction:.5,L:2}).v.T,180);
near(calc('cable',{W:200,theta:90,fraction:0}).v.Ry,200);
assert.equal(calc('cable',{theta:0,fraction:1}).v.cableCase,'impossible');checks++;
near(calc('work',{F:24,s:3,theta:90}).v.W,0);
near(calc('work',{F:24,s:3,theta:180}).v.W,-72);
near(calc('kinetic',{m:2,v:6}).v.K,36);
near(calc('potential',{m:2,h:3,ref:4}).v.U,-20);
near(calc('workenergy',{m:2,v0:6,F:-5,s:10}).v.actualS,7.2);
near(calc('workenergy',{m:2,v0:0,F:0,s:5}).v.actualS,0);
for(const m of [1,2,5])for(const h0 of [0,1,4,10])for(const h of [0,1,5,10])for(const mu of [0,.1,.4])for(const s of [0,1,10])for(const v0 of [0,3,8]){
 const v=calc('energy',{m,h0,h,mu,s,v0,mode:'friction'}).v;
 near(v.total,v.initial);assert.ok(v.thermal<=v.initial+1e-7&&v.actualS<=s&&v.K>=0);checks++;
}
const staticVector=draw('vector',{ax:-5,ay:4,bx:5,by:-8},{static:true});
assert.ok(!staticVector.includes('>R</text>'));checks++;
for(const k of ['components','incline','workenergy'])assert.ok(!draw(k,{}, {static:true}).includes('class="energy-ledger"'));
console.log(JSON.stringify({checks,result:'PASS'}));
