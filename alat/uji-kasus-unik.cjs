/* Cocokkan kunci kasus susunan Python dengan mesin fisika JavaScript yang independen. */
const {spawnSync}=require('node:child_process'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),V=require('../assets/kelas-visual.js');
const script="import sys,json;sys.path.insert(0,'alat');from konten_interaktif import load_sources;from kegiatan_unik import make;l,_=load_sources();print(json.dumps([make(s,c,i,stage,v) for s,a in l.items() for i,c in enumerate(a['concepts']) for stage in ['concept','guided','transfer','followup'] for v in ([0,1,5,6,7]if stage=='followup'else[0])]))";
const result=spawnSync(process.env.FIWA_PYTHON||'python',['-B','-X','utf8','-c',script],{cwd:root,encoding:'utf8',maxBuffer:5e6});if(result.status!==0)throw Error(result.stderr||String(result.error));
const cases=JSON.parse(result.stdout),keys={vector:'R',components:'x',incline:'parallel',motion:'a',reaction:'a2',torque:'tau',couple:'tau',cable:'T',work:'W',kinetic:'K',potential:'U',workenergy:'K',energy:'v'};
for(const q of cases){const {kind,params}=q.diagram,{v}=V.calculate(kind,params);assert(Number.isFinite(q.answer)&&Math.abs(q.answer-v[keys[kind]])<1e-5,q.id);assert(q.steps.length===7&&q.seconds===120,q.id);}
console.log(JSON.stringify({cases:cases.length,result:'PASS'}));
