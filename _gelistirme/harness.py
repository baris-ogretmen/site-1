import asyncio,json,os,time,urllib.parse
from playwright.async_api import async_playwright
SITE='https://baris-ogretmen.github.io/site-1/'
REPO=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..')+'/'
MOCK=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'mockfb.js'),encoding='utf8').read()
CIKTI={}
def ts(gun): return {'seconds':int(time.time())-gun*86400,'nanoseconds':0}
def veri():
    P=lambda **k:k
    d={'projeler':{
        'p1':P(baslik='Fener Avı — Karanlıkta 12 Akıl Oyunu',aciklama='Karanlıkta fenerle 12 akıl oyunu',link='fener-avi.html',kategoriler=['Oyunlar','Akıl Zeka','3. Sınıf'],tarih=ts(1)),
        'p2':P(baslik='Robo Maket Stüdyosu',aciklama='Tabletten tahtaya robotik atölye',link='robo-maket-studyosu.html',kategoriler=['Oyunlar','Robotik','4. Sınıf'],tarih=ts(2)),
        'p3':P(baslik='Minik Kâşifler',aciklama='Okul öncesi oyun paketi',link='minik kasiflerr.html',kategoriler=['Oyunlar','Anaokulu'],tarih=ts(20)),
        'p4':P(baslik='Eski Gizli Oyun',aciklama='gizli',link='eski.html',kategoriler=['Oyunlar'],tarih=ts(40),arsivlendi=True)},
      'videolar':{'v1':P(baslik='Kodlamaya Giriş Videosu',aciklama='video',link='https://youtu.be/dQw4w9WgXcQ',kategoriler=['Kodlama'],tarih=ts(3))},
      'kitaplar':{'k1':P(baslik='Ben Ali',aciklama='kitap',link='ben-ali.html',kategoriler=['Anaokulu'],tarih=ts(30))},
      'yazilar':{'y1':P(baslik='Bir İnsan İnşa Etmek',aciklama='yazı',icerik='<p>Merhaba</p>',kategoriler=[],tarih=ts(5))},
      'kaynaklar':{},
      'site_ayarlari':{'genel':P(aciklama='Test'),'ozel_duyuru':P(aktif=True,daireMetni='EN YENİ',sekil='shape-leaf',renk='linear-gradient(135deg, #ef4444, #b91c1c)',link=SITE+'fener-avi.html',mesaj='Fener Avı — Karanlıkta 12 Akıl Oyunu',anim='anim-pulse')}}
    return d
def init(giris=False,ek=''):
    return "window.__DATA="+json.dumps(veri())+";window.__GIRIS="+('true' if giris else 'false')+";localStorage.setItem('ob_goruldu','1');try{localStorage.setItem('bo_yonetici',String(Date.now()))}catch(e){}"+ek
async def rota(r):
    u=r.request.url
    if 'gstatic.com/firebasejs' in u:
        return await r.fulfill(body=MOCK if 'firebase-app' in u else '',content_type='text/javascript')
    if u.startswith(SITE):
        p=urllib.parse.unquote(urllib.parse.urlparse(u).path[len('/site-1/'):]) or 'index.html'
        if p in CIKTI: return await r.fulfill(body=CIKTI[p],content_type='text/html; charset=utf-8')
        f=REPO+p
        if os.path.isfile(f):
            ct='text/html; charset=utf-8' if f.endswith('.html') else ('text/javascript' if f.endswith('.js') else ('image/png' if f.endswith('.png') else 'application/octet-stream'))
            return await r.fulfill(path=f,content_type=ct)
        return await r.fulfill(status=404,body='yok')
    return await r.abort()
async def sayfa(b,url,w=390,h=844,mob=True,giris=False,ek=''):
    ctx=await b.new_context(viewport={'width':w,'height':h},is_mobile=mob,has_touch=mob);pg=await ctx.new_page();es=[];pg.on('pageerror',lambda e:es.append(str(e)[:200]))
    await pg.add_init_script(init(giris,ek));await pg.route('**/*',rota);await pg.goto(SITE+url);await pg.wait_for_timeout(4000);return ctx,pg,es
def tarayici(p): return p.chromium.launch()
