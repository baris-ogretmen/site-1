// Panelin "Sayfaları oluştur ve yükle" işini GitHub Actions'ta yapar.
// Üretici kodu her seferinde yonetici.html'den okunur (panel ile birebir aynı sonuç).
// Kullanım: node google_paketi.js  (depo kökünden; veri/icerik-yedek.json gerekir)
const fs = require('fs'), path = require('path'), vm = require('vm');
const SITE = 'https://baris-ogretmen.github.io/site-1/';
const panel = fs.readFileSync('yonetici.html', 'utf8');
const bas = panel.indexOf("const $k=s=>document.querySelector(s);", panel.indexOf('GOOGLE PAKETİ'));
const son = panel.indexOf('return {dosyalar,sayi:L.length}}', bas);
if (bas < 0 || son < 0) throw new Error('Panelde Google paketi üreticisi bulunamadı');
const kod = panel.slice(bas, son + 'return {dosyalar,sayi:L.length}}'.length) + '\n;globalThis.__uret=uret;';
const veri = JSON.parse(fs.readFileSync('veri/icerik-yedek.json', 'utf8'));
const ts = v => (typeof v === 'string' && /^\d{4}-\d\d-\d\dT/.test(v)) ? { seconds: Math.floor(Date.parse(v) / 1000) } : v;
const records = [];
for (const col of ['projeler', 'videolar', 'kitaplar', 'yazilar', 'kaynaklar']) {
  const d = veri[col] || {};
  if (d._hata) throw new Error(col + ' okunamadı: ' + d._hata);
  for (const [id, x] of Object.entries(d)) {
    const r = { ...x, id, col };
    for (const k of ['tarih', 'guncellendi']) if (r[k]) r[k] = ts(r[k]);
    records.push(r);
  }
}
const ctx = { records, SITE_HOME: SITE, base: SITE, URL, Date, JSON, Math, Map, Set, String, Array, Object, Promise, console,
  document: { querySelector: () => null, addEventListener: () => {} }, window: {}, globalThis: null };
ctx.globalThis = ctx; ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(kod, ctx);
const { dosyalar, sayi } = ctx.__uret();
if (sayi < 50) throw new Error('Çok az içerik üretildi (' + sayi + ') — veri eksik olabilir, yükleme yapılmadı');
// Değişiklik var mı? (yalnız tarih satırları farklıysa yazma)
const tarihsiz = s => s.replace(/<lastmod>[^<]*<\/lastmod>/g, '').replace(/© \d{4}/g, '');
let degisen = 0;
const yeniSayfalar = new Set();
for (const [p, icerik] of Object.entries(dosyalar)) {
  if (p.startsWith('sayfa/')) yeniSayfalar.add(path.basename(p));
  const eski = fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null;
  if (eski !== null && tarihsiz(eski) === tarihsiz(icerik)) continue;
  fs.mkdirSync(path.dirname(p) || '.', { recursive: true });
  fs.writeFileSync(p, icerik); degisen++;
}
// Panelle aynı: artık karşılığı olmayan eski üretilmiş sayfalar kaldırılır (yalnız sayfa/ klasörü)
let kalkan = [];
for (const f of fs.readdirSync('sayfa')) if (f.endsWith('.html') && !yeniSayfalar.has(f)) { fs.unlinkSync(path.join('sayfa', f)); kalkan.push(f); }
fs.writeFileSync('veri/google-paketi.json', JSON.stringify({ zaman: new Date().toISOString(), icerik: sayi, dosya: Object.keys(dosyalar).length, degisen, kalkan }, null, 1));
console.log('Google paketi:', sayi, 'içerik,', degisen, 'dosya değişti,', kalkan.length, 'eski sayfa kalktı');
