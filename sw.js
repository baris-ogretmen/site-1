/* Barış Öğretmen · Dijital Eğitim Üssü — Servis Çalışanı (v2)
   Strateji: HER ZAMAN ÖNCE İNTERNET. İçerik/fotoğraf güncellemeleri anında görünür.
   İnternet yoksa en son görülen hâli devreye girer (çevrimdışı yedek).
   Firebase ve yapay zekâ (googleapis) istekleri hiç dokunulmadan geçer. */

const CACHE = 'bo-uss-v2';
const KABUK = ['./', './index.html', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(KABUK).catch(() => {})));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // Firebase/CDN/Gemini'ye karışma

  // ÖNCE İNTERNET: taze içerik her zaman kazanır; internet yoksa önbellek yedeği
  e.respondWith(
    fetch(req).then((res) => {
      const kopya = res.clone();
      caches.open(CACHE).then((c) => c.put(req, kopya)).catch(() => {});
      return res;
    }).catch(() => caches.match(req).then((r) => r || (req.mode === 'navigate' ? caches.match('./index.html') : undefined)))
  );
});
