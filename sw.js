/* Barış Öğretmen · Dijital Eğitim Üssü — Servis Çalışanı
   Strateji: içerik HER ZAMAN taze kalsın diye "önce internet" (network-first).
   İnternet yoksa son görülen sayfa/dosya devreye girer. Firebase ve yapay zekâ
   istekleri (googleapis) HİÇ dokunulmadan geçer — canlı içerik ve robot aynen çalışır. */

const CACHE = 'bo-uss-v1';
const KABUK = [
  './',
  './index.html',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png'
];

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

  // Sadece GET ve sadece kendi sitemiz; Firebase/Gemini/CDN'e karışma
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Sayfa gezinmeleri: önce internet, olmazsa önbellek (içerik taze kalır)
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then((res) => {
        const kopya = res.clone();
        caches.open(CACHE).then((c) => c.put(req, kopya)).catch(() => {});
        return res;
      }).catch(() => caches.match(req).then((r) => r || caches.match('./index.html')))
    );
    return;
  }

  // Statik dosyalar (resim/ikon vb.): önbellekten göster, arkada güncelle
  e.respondWith(
    caches.match(req).then((cached) => {
      const agdan = fetch(req).then((res) => {
        const kopya = res.clone();
        caches.open(CACHE).then((c) => c.put(req, kopya)).catch(() => {});
        return res;
      }).catch(() => cached);
      return cached || agdan;
    })
  );
});
