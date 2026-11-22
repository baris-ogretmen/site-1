/* test için sahte Firebase 8 compat (firestore + auth) */
(function(){
if(window.firebase&&window.firebase.__mock)return;
const data=window.__DATA||{};window.__DATA=data;
const subs=new Set();
class TS{constructor(s,n=0){this.seconds=s;this.nanoseconds=n}toMillis(){return this.seconds*1000}toDate(){return new Date(this.toMillis())}static now(){return new TS(Math.floor(Date.now()/1000))}static fromDate(d){return new TS(Math.floor(d.getTime()/1000))}static fromMillis(m){return new TS(Math.floor(m/1000))}}
window.__TS=s=>new TS(s);
const INC=Symbol('inc'),DEL=Symbol('del'),SRV=Symbol('srv');
function val(v,old){if(v&&v[INC]!==undefined)return (Number(old)||0)+v[INC];if(v===SRV)return TS.now();return v}
function apply(t,v){t=t&&typeof t==='object'?JSON.parse(JSON.stringify(t),rev):{};for(const [k,x] of Object.entries(v)){if(x===DEL){delete t[k];continue}if(k.includes('.')){const ps=k.split('.');let o=t;for(let i=0;i<ps.length-1;i++){o[ps[i]]=o[ps[i]]&&typeof o[ps[i]]==='object'?o[ps[i]]:{};o=o[ps[i]]}o[ps.at(-1)]=val(x,o[ps.at(-1)]);continue}
  if(x&&typeof x==='object'&&!(x instanceof TS)&&!Array.isArray(x)&&x[INC]===undefined&&t[k]&&typeof t[k]==='object'&&!(t[k] instanceof TS))t[k]=apply(t[k],x);else t[k]=val(x,t[k])}return t}
function rev(k,v){return v&&typeof v==='object'&&'seconds' in v&&'nanoseconds' in v?new TS(v.seconds,v.nanoseconds):v}
const clone=o=>o==null?o:JSON.parse(JSON.stringify(o),rev);
function notify(){setTimeout(()=>subs.forEach(f=>{try{f()}catch(e){console.error(e)}}),0)}
const col=p=>(data[p]=data[p]||{});
function snapDoc(c,id){const d=col(c)[id];return {id,exists:d!==undefined,data:()=>clone(d),get:k=>clone(d)?.[k],ref:new Doc(c,id)}}
class Doc{constructor(c,id){this.col=c;this.id=id||Math.random().toString(36).slice(2,12);this.path=c+'/'+this.id}
 collection(n){return new Col(this.col+'/'+this.id+'/'+n)}
 async get(){return snapDoc(this.col,this.id)}
 async set(v,o){const C=col(this.col);C[this.id]=o&&o.merge?apply(C[this.id],v):apply(undefined,v);notify()}
 async update(v){const C=col(this.col);if(C[this.id]===undefined)throw new Error('no doc');C[this.id]=apply(C[this.id],v);notify()}
 async delete(){delete col(this.col)[this.id];notify()}
 onSnapshot(cb,err){const f=()=>cb(snapDoc(this.col,this.id));subs.add(f);setTimeout(f,0);return ()=>subs.delete(f)}}
class Col{constructor(p,q=[]){this.path=p;this.q=q}
 doc(id){return new Doc(this.path,id)}
 async add(v){const d=new Doc(this.path);await d.set(v);return d}
 where(f,op,v){return new Col(this.path,[...this.q,['w',f,op,v]])}
 orderBy(f,dir){return new Col(this.path,[...this.q,['o',f,dir]])}
 limit(n){return new Col(this.path,[...this.q,['l',n]])}
 startAfter(){return this}
 _docs(){let L=Object.keys(col(this.path)).map(id=>snapDoc(this.path,id));for(const q of this.q){if(q[0]==='w'){const [,f,op,v]=q;L=L.filter(d=>{const x=d.data()[f];return op==='=='?x===v:op==='!='?x!==v:op==='in'?v.includes(x):op==='array-contains'?Array.isArray(x)&&x.includes(v):op==='>'?x>v:op==='>='?x>=v:op==='<'?x<v:op==='<='?x<=v:true})}else if(q[0]==='o'){const [,f,dir]=q;const g=d=>{const x=d.data()[f];return x&&x.seconds!==undefined?x.seconds:x};L.sort((a,b)=>(g(a)>g(b)?1:g(a)<g(b)?-1:0)*(dir==='desc'?-1:1))}else if(q[0]==='l')L=L.slice(0,q[1])}return L}
 async get(){const docs=this._docs();return {docs,size:docs.length,empty:!docs.length,forEach:f=>docs.forEach(f)}}
 onSnapshot(cb,err){const f=()=>{const docs=this._docs();cb({docs,size:docs.length,empty:!docs.length,forEach:g=>docs.forEach(g),docChanges:()=>[]})};subs.add(f);setTimeout(f,0);return ()=>subs.delete(f)}}
const db={collection:p=>new Col(p),doc:p=>{const a=p.split('/');return new Doc(a.slice(0,-1).join('/'),a.at(-1))},batch(){const ops=[];return {set:(r,v,o)=>ops.push(()=>r.set(v,o)),update:(r,v)=>ops.push(()=>r.update(v)),delete:r=>ops.push(()=>r.delete()),commit:async()=>{for(const o of ops)await o()}}},runTransaction:async fn=>fn({get:r=>r.get(),set:(r,v,o)=>r.set(v,o),update:(r,v)=>r.update(v),delete:r=>r.delete()}),enablePersistence:async()=>{},settings(){}};
const fs=()=>db;fs.FieldValue={increment:n=>({[INC]:n}),serverTimestamp:()=>SRV,delete:()=>DEL,arrayUnion:(...a)=>a,arrayRemove:()=>[]};fs.Timestamp=TS;
const user={uid:'test-uid',email:'baris@test'};let cbs=[];
const auth={currentUser:window.__GIRIS?user:null,onAuthStateChanged(cb){cbs.push(cb);setTimeout(()=>cb(this.currentUser),0);return ()=>{}},async signInWithEmailAndPassword(){this.currentUser=user;cbs.forEach(c=>c(user));return {user}},async signOut(){this.currentUser=null;cbs.forEach(c=>c(null))},async setPersistence(){},async signInAnonymously(){return {user}}};
const au=()=>auth;au.Auth={Persistence:{LOCAL:'local',SESSION:'session'}};au.GoogleAuthProvider=function(){};
window.firebase={__mock:true,apps:[],initializeApp(c){const a={options:c,name:'[DEFAULT]'};this.apps.push(a);return a},app(){return this.apps[0]||{options:{projectId:'test'}}},firestore:fs,auth:au};
})();
