/* Barış Öğretmen · Dijital Eğitim Üssü – güvenli önbellek (v6 · sayfalar her açılışta GitHub’dan tazelenir)
   Video/ses ve parça (Range) isteklerine hiç dokunmaz; sayfalar önce internetten gelir,
   internet yoksa son kaydedilen hâli gösterilir. Eski önbellekler otomatik silinir. */
const CACHE='bi-v6-2026-09-30';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>Promise.allSettled(['./','./index.html'].map(u=>c.add(u)))))});
self.addEventListener('activate',e=>e.waitUntil((async()=>{for(const k of await caches.keys())if(k!==CACHE)await caches.delete(k);await self.clients.claim()})()));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);if(u.origin!==location.origin)return;
 if(r.headers.has('range')||r.destination==='video'||r.destination==='audio'||/\.(mp4|webm|m4v|mov|mp3|wav|ogg|m4a)$/i.test(u.pathname))return;
 if(r.mode==='navigate'||r.destination==='document'){e.respondWith(fetch(r.url,{cache:'no-cache',credentials:'same-origin'}).then(res=>{if(res.ok){const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c)).catch(()=>{})}return res}).catch(async()=>(await caches.match(r))||(await caches.match('index.html'))||Response.error()));return}
 e.respondWith(caches.open(CACHE).then(async c=>{const hit=await c.match(r);const net=fetch(r).then(res=>{if(res.status===200)c.put(r,res.clone()).catch(()=>{});return res}).catch(()=>hit||Response.error());return hit||net}));
});
