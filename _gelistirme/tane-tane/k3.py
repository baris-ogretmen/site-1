# -*- coding: utf-8 -*-
"""Kitap 3 · Toplama ve Çıkarma Hikâyeleri (10'a ve 20'ye kadar) — 1. sınıf + özel gereksinim."""
import random
from lib import *

k = Kitap('k3', 'Toplama ve Çıkarma Hikâyeleri', "10'a ve 20'ye kadar", '3. Kitap', '1. sınıf · Özel eğitim')
R = random.Random(33)
OY_PARMAK = ("Sihirli Parmaklar · 1'den 10'a", 'sihirlii parmaklar.html')
OY_MATAKIS = ('MatAkış — Gör, Dokun, Oyna', 'matakis.html')
OY_KUM = ('Kum Tüneli', 'kumm tuneliii.html')
TR = '#ea580c'; KOYU = '#7c2d12'; KIR = '#ef4444'; MAV = '#3b82f6'
EKSI = '−'
EM = dict(NESNE)

# ---------- yardımcılar (lib'e dokunmadan) ----------
def grup(em, n, boy=44, cizik=0, sutun=5, renk=None, bg=None):
    """n nesne; son 'cizik' tanesinin üstü çizili (çıkarma). renk verilirse çerçeveli kutu."""
    assert 0 <= cizik <= n
    it = []
    for i in range(n):
        if i >= n - cizik:
            it.append(f'<span style="position:relative;display:inline-block;opacity:.55">{em}'
                      f'<svg viewBox="0 0 10 10" style="position:absolute;left:-4%;top:-4%;width:108%;height:108%">'
                      f'<line x1="1" y1="1" x2="9" y2="9" stroke="#dc2626" stroke-width="1.3" stroke-linecap="round"/>'
                      f'<line x1="9" y1="1" x2="1" y2="9" stroke="#dc2626" stroke-width="1.3" stroke-linecap="round"/></svg></span>')
        else:
            it.append(f'<span>{em}</span>')
    s = min(n, sutun) if n else 1
    g = (f'<div style="display:grid;grid-template-columns:repeat({s},{boy*1.22:.0f}px);font-size:{boy}px;line-height:1.2;justify-content:center">'
         + ''.join(it) + '</div>')
    if renk:
        g = f'<div style="border:3px solid {renk};background:{bg or "#fff"};border-radius:16px;padding:8px 10px">{g}</div>'
    return g

def bos(boy=52, renk=TR):
    return (f'<span style="display:inline-block;width:{boy*1.35:.0f}px;height:{boy*1.35:.0f}px;border:4px solid {renk};'
            f'border-radius:14px;background:#fff;vertical-align:middle"></span>')

def islem(*p, boy=52):
    """None → boş kutu, '○' → işaret yazılacak daire, diğerleri olduğu gibi."""
    h = []
    for x in p:
        if x is None: h.append(bos(boy))
        elif x == '○': h.append(f'<span style="display:inline-block;width:{boy*1.1:.0f}px;height:{boy*1.1:.0f}px;border:4px dashed #94a3b8;border-radius:50%;vertical-align:middle"></span>')
        elif x in ('+', EKSI, '='): h.append(f'<span style="color:{TR}">{x}</span>')
        else: h.append(f'<span>{x}</span>')
    return f'<div style="display:flex;align-items:center;justify-content:center;gap:14px;font-size:{boy}px;font-weight:900">' + ''.join(h) + '</div>'

def arti(boy=46):
    return f'<span style="font-size:{boy}px;font-weight:900;color:{TR}">+</span>'

def hikaye_metin(t):
    return f'<div style="font-size:21px;font-weight:700;line-height:1.4;text-align:left;width:100%">{t}</div>'

# ---------- 1. kapak + aileler ----------
k.kapak("Toplama ve çıkarmayı <b>kısa hikâyelerle</b> öğreten çalışma kitabı. Her işlem önce resimle görülür, sonra sayı doğrusu ve onluk çerçeveyle, en son rakamlarla yazılır.",
        f'<div style="font-size:78px;font-weight:900;color:{TR}">3 + 2 = 5</div>')

k.sayfa(f'''<div style="font-size:15.5px;line-height:1.55">
<p><b>Bu kitapta ne var?</b> 1. sınıf matematik kazanımlarıyla uyumlu olarak: parça–bütün (sayı bağları), toplama ve çıkarma hikâyeleri, sayı doğrusunda ileri–geri sayma, toplama–çıkarma ilişkisi (işlem ailesi), 20'ye kadar sayılar (onluk + birlik) ve karışık problemler.</p>
<table class="tbl"><tr><th>Bölüm</th><th>Ne yapıyoruz?</th><th>Sizin rolünüz</th></tr>
<tr><td>1 · Sayı bağları</td><td>Bir sayının iki parçaya ayrılışını görür, eksik parçayı bulur. 10'u tamamlar.</td><td>Fasulye ya da legoyu iki tabağa ayırın: "Toplam kaç, burada kaç, orada kaç?"</td></tr>
<tr><td>2 · Toplama hikâyeleri</td><td>Hikâyeyi dinler, resmi sayar, işlemi yazar.</td><td>Hikâyeyi okuyun, nesnelerle canlandırın. Önce resim, sonra işlem.</td></tr>
<tr><td>3 · Sayı doğrusu</td><td>İleri sayarak toplar.</td><td>Yere bantla bir sayı doğrusu yapıp üzerinde zıplayabilirsiniz.</td></tr>
<tr><td>4 · Çıkarma hikâyeleri</td><td>Gidenlerin üstünü çizer, kalanı sayar; geri sayar.</td><td>"Kaç tane gitti, kaç tane kaldı?" diye sorun.</td></tr>
<tr><td>5 · İşlem ailesi</td><td>Aynı üç sayıyla 2 toplama, 2 çıkarma yazar.</td><td>Üç sayıyı kartlara yazıp yer değiştirerek oynayın.</td></tr>
<tr><td>6 · 20'ye kadar</td><td>Bir onluk ve birlikleri görür; 11–20'yi okur, yazar.</td><td>10 nesneyi bir bardağa koyup "bir onluk" deyin, kalanları tek tek sayın.</td></tr>
<tr><td>7 · Karışık</td><td>Toplama mı çıkarma mı karar verir, kendi hikâyesini anlatır.</td><td>Günlük hayattan hikâyeler kurun (sofra, oyuncaklar).</td></tr></table>
<p style="margin-top:10px"><b>Somut → Resim → Sembol:</b> Her yeni işlem önce nesneyle, sonra resimle, en son rakamla çalışılır. Bu sıra, erken matematik öğretiminde araştırmalarla desteklenen bir yaklaşımdır. Zorlanılan sayfada bir adım geri gidin: gerçek nesnelere dönün.</p>
<p><b>Özel gereksinimli çocuklar için:</b> Bir sayfada tek kutu gösterin, diğerlerini kâğıtla kapatın. Önce siz yapın, sonra birlikte, en son tek başına yapsın. Parmak, sayaç ve sayı doğrusu her zaman kullanılabilir; ezber beklemeyin. Kısa ve sık çalışmak (günde 1–2 sayfa) daha verimlidir.</p>
<p><b>Dijital destek:</b> Bazı sayfalardaki QR kod, sitedeki ilgili oyunu açar. Kitap ana çalışmadır; oyun pekiştirme içindir.</p></div>''',
        baslik='Aileler ve öğretmenler için', no='i')

# ---------- BÖLÜM 1 · Sayı bağları ----------
a, b = 3, 2; assert a + b == 5
k.sayfa(f'''<div class="kutu" style="flex-direction:column;gap:14px;background:{"#fff7ed"};border-color:#fed7aa">
<div style="display:flex;align-items:center;gap:18px">{grup('🍎', a, 54, renk=KIR, bg='#fef2f2')}{arti()}{grup('🍎', b, 54, renk=MAV, bg='#eff6ff')}</div>
<div style="font-size:24px;font-weight:800">Hepsi <b style="color:{TR}">{a+b}</b> elma: <span style="color:{KIR}">{a}</span> ve <span style="color:{MAV}">{b}</span></div></div>
<div class="kutu">{sayi_bagi(a+b, a, b, px=260)}<div style="font-size:21px;line-height:1.6;font-weight:600">Üstteki daire: <b>bütün</b> ({a+b})<br>Alttaki daireler: <b>parçalar</b> ({a} ve {b})<br>Parçalar birleşince bütün olur.</div></div>
<div class="not">Gerçek nesnelerle başlayın: 5 nesneyi iki tabağa farklı biçimlerde ayırın (4 ve 1, 3 ve 2…). Her seferinde "Bütün yine 5 mi?" diye sorun.</div>''',
        baslik='Parça ve bütün', no=1, yonerge='Bir sayı <b>iki parçaya</b> ayrılabilir.', alt_yonerge='Sayı bağı: üstte bütün, altta iki parça.', oyun=OY_MATAKIS)

bag_sayfalari = [[(2, 1, 1, None), (3, 2, 1, 'p2'), (4, 1, 3, 'p1')],
                 [(5, 4, 1, 'butun'), (5, 2, 3, 'p2'), (6, 3, 3, 'p1')],
                 [(6, 5, 1, 'butun'), (7, 4, 3, 'p2'), (7, 2, 5, 'p1')],
                 [(8, 6, 2, 'butun'), (8, 3, 5, 'p2'), (9, 4, 5, 'p1')]]
for si, sayfa_ in enumerate(bag_sayfalari):
    kutular = []
    for j, (n, p1, p2, gz) in enumerate(sayfa_):
        assert n == p1 + p2 and p1 >= 0 and p2 >= 0
        ad, em = NESNE[(si * 3 + j * 5 + 1) % len(NESNE)]
        kutular.append(f'<div class="kutu" style="margin:8px 0;padding:12px"><div style="display:flex;align-items:center;gap:10px">'
                       f'{grup(em, p1, 44, sutun=3, renk=KIR, bg="#fef2f2")}{grup(em, p2, 44, sutun=3, renk=MAV, bg="#eff6ff")}</div>{sayi_bagi(n, p1, p2, gizle=gz, px=240)}</div>')
    k.sayfa(''.join(kutular), baslik='Sayı bağları: resimle', no=1, yonerge='Nesneleri say. Boş daireye doğru sayıyı <b>yaz</b>.',
            alt_yonerge='Kırmızı kutu bir parça, mavi kutu öbür parça; ikisi birlikte bütün.')

eksik = [[(5, 2, 3, 'p2'), (6, 4, 2, 'p1'), (7, 6, 1, 'p2')],
         [(8, 5, 3, 'p1'), (9, 7, 2, 'p2'), (6, 2, 4, 'butun')],
         [(4, 3, 1, 'p1'), (9, 3, 6, 'p2'), (8, 7, 1, 'butun')]]
for si, sayfa_ in enumerate(eksik):
    kutular = []
    for (n, p1, p2, gz) in sayfa_:
        assert n == p1 + p2
        kutular.append(f'<div class="kutu" style="margin:8px 0;padding:12px">{sayi_bagi(n, p1, p2, gizle=gz, px=240)}'
                       f'<div style="text-align:center;font-size:15px;color:#64748b;font-weight:700">Çizerek bulabilirsin:<div style="margin-top:6px">{cerceve(0, 10, 50, bos_isaret=True)}</div></div></div>')
    k.sayfa(''.join(kutular), baslik='Eksik parçayı bul', no=1, yonerge='Sayı bağında hangi sayı eksik? <b>Yaz</b>.',
            alt_yonerge='Çerçeveye bütün kadar nokta çiz, parçayı ayır, kalanı say. Parmak da kullanılabilir.')

# 10'u tamamlama
sat = ''.join(f'<div style="display:flex;align-items:center;gap:14px;margin:6px 0">{cerceve(a, 10, 30, ikinci=10 - a)}'
              f'<span style="font-size:26px;font-weight:900"><span style="color:{KIR}">{a}</span> + <span style="color:{MAV}">{10-a}</span> = 10</span></div>'
              for a in range(1, 10))
assert all(a + (10 - a) == 10 for a in range(1, 10))
k.sayfa(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 24px;margin-top:10px">{sat}</div>'
        f'<div class="kutu" style="min-height:150px">{sayi_bagi(10, 6, 4, px=170)}<div style="font-size:19px;line-height:1.6;font-weight:600">10, iki parçaya pek çok yolla ayrılır.<br>Kırmızılar + maviler = her zaman <b>10</b>.</div></div>'
        '<div class="not">"10\'un kardeşleri" ileride 20\'ye kadar işlemlerde çok işe yarar. Onluk çerçevede boş kutular, 10\'a kaç tane eksik olduğunu gösterir.</div>',
        baslik="10'un sayı bağları", no=1, yonerge="Onluk çerçeve dolunca <b>10</b> olur.", alt_yonerge='Kırmızı ve mavileri birlikte sayın.')

ust = [7, 4, 8]
k.sayfa(''.join(f'<div class="kutu" style="flex-direction:column;gap:14px">{cerceve(a, 10, 64)}{islem(a, "+", None, "=", 10)}</div>' for a in ust),
        baslik="10'u tamamla", no=1, yonerge="Boş kutulara <b>mavi</b> boyayla nokta çiz. Kaç tane çizdin? <b>Yaz</b>.", alt_yonerge='Boş kutu sayısı = 10\'a eksik olan.')
cift = [(3, 7), (9, 1), (5, 5)]
for a, b in cift: assert a + b == 10
k.sayfa(''.join(f'<div class="kutu" style="flex-direction:column;gap:14px">{cerceve(a, 10, 64, ikinci=b)}{islem(None, "+", None, "=", 10)}</div>' for a, b in cift),
        baslik="10'u tamamla", no=1, yonerge='Kırmızıları ve mavileri say. İşlemi <b>yaz</b>.', alt_yonerge='Önce kırmızılar, sonra maviler.')

# ---------- BÖLÜM 2 · Toplama hikâyeleri ----------
a, b = 3, 2
k.sayfa(f'''<div class="kutu" style="flex-direction:column;gap:12px;background:#fff7ed;border-color:#fed7aa">{hikaye_metin(f"Ela'nın {a} balonu var. Ali {b} balon daha getirdi. Kaç balon oldu?")}
<div style="display:flex;align-items:center;gap:10px">{grup('🎈', a, 40, renk=KIR, bg='#fef2f2')}{arti(40)}{grup('🎈', b, 40, renk=MAV, bg='#eff6ff')}
<span style="font-size:40px;font-weight:900;color:{TR}">→</span>{grup('🎈', a+b, 40, renk=TR, bg='#fff')}</div></div>
<div class="kutu" style="flex-direction:column;gap:10px">{islem(a, '+', b, '=', a+b, boy=80)}
<div style="font-size:19px;font-weight:600;text-align:center;line-height:1.6"><b style="color:{TR}">+</b> "artı" okunur: birleştir, ekle.<br><b style="color:{TR}">=</b> "eşittir" okunur: iki yan aynı miktar.</div></div>
<div class="not">Önce hikâyeyi nesnelerle canlandırın, sonra resme bakın, en son işlemi okuyun: "{a} artı {b} eşittir {a+b}". Parmaklarla da gösterilebilir.</div>''',
        baslik='Toplama: birleştir, ekle', no=2, yonerge='İki grup birleşince <b>toplama</b> yaparız.', alt_yonerge='Resim → işlem.', oyun=OY_PARMAK)

TOPLA = [("Ela'nın {a} balonu var. Ali {b} balon daha getirdi. Kaç balon oldu?", '🎈', 3, 2),
         ("Çiçeklerin üstünde {a} kelebek var. {b} kelebek daha geldi. Şimdi kaç kelebek var?", '🦋', 4, 3),
         ("Zeynep sepete {a} elma koydu. Kerem de {b} elma koydu. Sepette kaç elma var?", '🍎', 5, 2),
         ("Havuzda {a} ördek yüzüyor. {b} ördek daha suya girdi. Havuzda kaç ördek var?", '🦆', 2, 6),
         ("Defne'nin {a} kalemi var. Annesi {b} kalem daha aldı. Defne'nin kaç kalemi oldu?", '✏️', 6, 1),
         ("Emir {a} kek yaptı. Nehir de {b} kek yaptı. Toplam kaç kek var?", '🧁', 4, 4),
         ("Bahçede {a} tavşan var. {b} tavşan daha geldi. Bahçede kaç tavşan oldu?", '🐰', 7, 2),
         ("Can'ın kutusunda {a} araba var. {b} araba daha aldı. Kutuda kaç araba oldu?", '🚗', 5, 5),
         ("Yaprakta {a} uğur böceği var. {b} uğur böceği daha kondu. Kaç uğur böceği oldu?", '🐞', 3, 5),
         ("Ali {a} çilek topladı. Ela {b} çilek topladı. İkisi toplam kaç çilek topladı?", '🍓', 6, 3)]
for i in range(0, 10, 2):
    kutular = []
    for t, em, a, b in TOPLA[i:i + 2]:
        c = a + b; assert 0 <= c <= 10
        eq = islem(a, '+', b, '=', None) if i < 4 else islem(None, '+', None, '=', None)
        kutular.append(f'<div class="kutu" style="flex-direction:column;gap:12px;margin:10px 0">{hikaye_metin(t.format(a=a, b=b))}'
                       f'<div style="display:flex;align-items:center;gap:16px">{grup(em, a, 40 if a + b >= 9 else 52, renk=KIR, bg="#fef2f2")}{arti()}{grup(em, b, 40 if a + b >= 9 else 52, renk=MAV, bg="#eff6ff")}</div>{eq}</div>')
    k.sayfa(''.join(kutular), baslik='Toplama hikâyeleri', no=2,
            yonerge='Hikâyeyi dinle, resmi say. Boş kutulara <b>yaz</b>.' if i < 4 else 'Hikâyeyi dinle, resmi say. İşlemi kendin <b>yaz</b>.',
            alt_yonerge='Hikâyeyi yetişkin okur; çocuk resimdeki nesneleri parmakla sayar.')

cift = [(4, 2), (6, 3), (5, 4)]
for a, b in cift: assert a + b <= 10
k.sayfa(''.join(f'<div class="kutu" style="flex-direction:column;gap:14px">{cerceve(a, 10, 60, ikinci=b)}{islem(a, "+", b, "=", None)}</div>' for a, b in cift),
        baslik='Çerçevede toplama', no=2, yonerge='Kırmızılar ve maviler birlikte kaç tane? <b>Yaz</b>.', alt_yonerge='Beşi bir bakışta gör: üst sıra dolu ise 5\'ten saymaya devam et.')

# ---------- BÖLÜM 3 · Sayı doğrusunda ileri sayma ----------
a, b = 3, 4; assert a + b == 7
k.sayfa(f'''<div class="kutu" style="flex-direction:column;gap:6px;background:#fff7ed;border-color:#fed7aa">
<div style="font-size:21px;font-weight:700">{a} + {b} işlemini sayı doğrusunda yapalım:</div>{sayi_dogrusu(0, 10, isaret={a, a+b}, atla=(a, b), w=660)}</div>
<div class="kutu" style="flex-direction:column;gap:10px;font-size:20px;font-weight:600;line-height:1.6;align-items:flex-start">
<div>1. <b style="color:#dc2626">{a}</b> üzerinde dur.</div><div>2. {b} kez ileri zıpla: {", ".join(str(a + i) for i in range(1, b + 1))}.</div><div>3. Durduğun yer cevaptır: <b style="color:#dc2626">{a+b}</b>.</div>
<div style="align-self:center;margin-top:6px">{islem(a, "+", b, "=", a+b, boy=60)}</div></div>
<div class="not">İleride büyük sayıdan başlayıp küçüğü ileri saymayı deneyin; bu, saymayı kısaltır. Yerde bantla yapılmış bir sayı doğrusunda zıplamak bu adımı somutlaştırır.</div>''',
        baslik='Sayı doğrusunda toplama', no=3, yonerge='Toplamada sayı doğrusunda <b>ileri</b> zıplarız.', oyun=OY_KUM)

ileri = [(2, 3), (5, 4), (1, 6), (4, 4), (6, 3), (3, 5)]
for p in range(3):
    kutular = []
    for a, b in ileri[p * 2:p * 2 + 2]:
        assert a + b <= 10
        kutular.append(f'<div class="kutu" style="flex-direction:column;gap:8px;margin:14px 0;min-height:330px"><div style="font-size:20px;font-weight:700"><b style="color:#dc2626">{a}</b> üzerinden başla, {b} kez ileri zıpla.</div>'
                       f'{sayi_dogrusu(0, 10, isaret={a}, atla=(a, b) if p == 0 else None, w=660)}{islem(a, "+", b, "=", None)}</div>')
    k.sayfa(''.join(kutular), baslik='İleri say, topla', no=3,
            yonerge='Zıplamaları say. Nerede durdun? <b>Yaz</b>.' if p == 0 else 'Zıplama yaylarını sen <b>çiz</b>. Nerede durdun? <b>Yaz</b>.',
            alt_yonerge='Her yay bir adım. Parmağını sayı doğrusunda yürüt.')

# ---------- BÖLÜM 4 · Çıkarma ----------
a, b = 5, 2; assert a - b == 3
k.sayfa(f'''<div class="kutu" style="flex-direction:column;gap:12px;background:#fff7ed;border-color:#fed7aa">{hikaye_metin(f"Ağaçta {a} elma var. {b} elma yere düştü. Ağaçta kaç elma kaldı?")}
{grup('🍎', a, 60, cizik=b)}<div style="font-size:20px;font-weight:700">Giden {b} elmanın üstünü çizdik. Çizilmeyenleri sayarız: <b style="color:{TR}">{a-b}</b></div></div>
<div class="kutu" style="flex-direction:column;gap:10px">{islem(a, EKSI, b, '=', a-b, boy=80)}
<div style="font-size:19px;font-weight:600;text-align:center;line-height:1.6"><b style="color:{TR}">{EKSI}</b> "eksi" okunur: ayır, çıkar, eksilt.<br>Çıkarmada kalan, baştakinden fazla olamaz.</div></div>
<div class="not">Gerçek nesnelerle canlandırın: 5 nesne koyun, 2 tanesini alın. "Kaç tane kaldı?" Sonra resme bakın, en son işlemi okuyun.</div>''',
        baslik='Çıkarma: ayır, eksilt', no=4, yonerge='Bir gruptan bazıları <b>gidince</b> çıkarma yaparız.', alt_yonerge='Resim → işlem.', oyun=OY_MATAKIS)

CIKAR = [("Ağaçta {a} elma var. {b} elma yere düştü. Ağaçta kaç elma kaldı?", '🍎', 5, 2),
         ("Ela'nın {a} balonu var. {b} balonu uçup gitti. Kaç balonu kaldı?", '🎈', 6, 1),
         ("Tabakta {a} kek var. Kerem {b} kek yedi. Tabakta kaç kek kaldı?", '🧁', 7, 3),
         ("Gölde {a} kurbağa var. {b} kurbağa zıplayıp gitti. Kaç kurbağa kaldı?", '🐸', 8, 4),
         ("Zeynep'in {a} kalemi var. {b} kalemini Can'a verdi. Zeynep'in kaç kalemi kaldı?", '✏️', 9, 5),
         ("Çiçekte {a} arı var. {b} arı uçup gitti. Çiçekte kaç arı kaldı?", '🐝', 6, 4),
         ("Sepette {a} portakal var. Defne {b} portakal aldı. Sepette kaç portakal kaldı?", '🍊', 10, 3),
         ("Bahçede {a} civciv var. {b} civciv kümese girdi. Bahçede kaç civciv kaldı?", '🐥', 8, 6)]
for i in range(0, 8, 2):
    kutular = []
    for t, em, a, b in CIKAR[i:i + 2]:
        c = a - b; assert 0 <= c <= 10 and b <= a
        eq = islem(a, EKSI, b, '=', None) if i < 4 else islem(None, EKSI, None, '=', None)
        kutular.append(f'<div class="kutu" style="flex-direction:column;gap:14px;margin:12px 0;min-height:330px">{hikaye_metin(t.format(a=a, b=b))}{grup(em, a, 56, cizik=b)}{eq}</div>')
    k.sayfa(''.join(kutular), baslik='Çıkarma hikâyeleri', no=4,
            yonerge='Gidenlerin üstü çizildi. Kalanları say, <b>yaz</b>.' if i < 4 else 'Gidenlerin üstü çizildi. İşlemi kendin <b>yaz</b>.',
            alt_yonerge='Önce baştaki hepsini, sonra gidenleri, en son kalanları say.')

ciz = [('⭐', 6, 2), ('🍐', 9, 4), ('🌼', 7, 5)]
k.sayfa(''.join(f'<div class="kutu" style="flex-direction:column;gap:12px"><div style="font-size:21px;font-weight:700">{b} tanesinin üstünü <b style="color:#dc2626">çiz</b>.</div>{grup(em, a, 42)}{islem(a, EKSI, b, "=", None)}</div>'
                for em, a, b in ciz if a - b >= 0),
        baslik='Çiz ve çıkar', no=4, yonerge='Söylenen kadar nesnenin üstünü <b>çiz</b>. Kalanları say, <b>yaz</b>.', alt_yonerge='Sondan başlayarak çizmek saymayı kolaylaştırır.')

geri = [(7, 3), (9, 4), (8, 5), (10, 6)]
for p in range(2):
    kutular = []
    for a, b in geri[p * 2:p * 2 + 2]:
        assert 0 <= a - b
        kutular.append(f'<div class="kutu" style="flex-direction:column;gap:8px;margin:14px 0;min-height:330px"><div style="font-size:20px;font-weight:700"><b style="color:#dc2626">{a}</b> üzerinden başla, {b} kez <b>geri</b> zıpla.</div>'
                       f'{sayi_dogrusu(0, 10, isaret={a}, atla=(a, -b) if p == 0 else None, w=660)}{islem(a, EKSI, b, "=", None)}</div>')
    k.sayfa(''.join(kutular), baslik='Geri say, çıkar', no=4,
            yonerge='Çıkarmada sayı doğrusunda <b>geri</b> zıplarız. Nerede durdun? <b>Yaz</b>.' if p == 0 else 'Geri zıplama yaylarını sen <b>çiz</b>. Nerede durdun? <b>Yaz</b>.',
            alt_yonerge='Her yay bir adım geri. Parmağını sola doğru yürüt.')

# ---------- BÖLÜM 5 · İşlem ailesi ----------
n, a, b = 8, 3, 5; assert a + b == n and b + a == n and n - a == b and n - b == a
k.sayfa(f'''<div class="kutu" style="gap:20px;background:#fff7ed;border-color:#fed7aa"><div style="display:flex;align-items:center;gap:10px">{grup('🐟', a, 44, sutun=3, renk=KIR, bg='#fef2f2')}{grup('🐟', b, 44, sutun=3, renk=MAV, bg='#eff6ff')}</div>{sayi_bagi(n, a, b, px=210)}</div>
<div class="kutu" style="display:grid;grid-template-columns:1fr 1fr;gap:18px">{islem(a, '+', b, '=', n, boy=46)}{islem(b, '+', a, '=', n, boy=46)}{islem(n, EKSI, a, '=', b, boy=46)}{islem(n, EKSI, b, '=', a, boy=46)}</div>
<div class="not">Aynı üç sayı ({a}, {b}, {n}) dört işlem kurar: iki toplama, iki çıkarma. Toplamada parçalar birleşir, çıkarmada bütünden bir parça ayrılır. Bu ilişkiyi görmek, çıkarmayı toplamayla kontrol etmeyi sağlar.</div>''',
        baslik='İşlem ailesi', no=5, yonerge='Üç sayı, <b>dört işlem</b>: bir aile!', alt_yonerge='Bütün = en büyük sayı. Çıkarma her zaman bütünden başlar.')

AILE = [(7, 4, 3), (9, 6, 3), (10, 8, 2), (6, 5, 1), (10, 4, 6), (9, 2, 7)]
for p in range(3):
    kutular = []
    for j, (n, a, b) in enumerate(AILE[p * 2:p * 2 + 2]):
        assert a + b == n and a != b and n <= 10
        if p == 0:
            eqs = [islem(a, '+', b, '=', None, boy=40), islem(b, '+', a, '=', None, boy=40), islem(n, EKSI, a, '=', None, boy=40), islem(n, EKSI, b, '=', None, boy=40)]
        elif p == 1:
            eqs = [islem(a, '+', None, '=', n, boy=40), islem(None, '+', a, '=', n, boy=40), islem(n, EKSI, None, '=', b, boy=40), islem(None, EKSI, b, '=', a, boy=40)]
        else:
            eqs = [islem(None, '+', None, '=', None, boy=40)] * 2 + [islem(None, EKSI, None, '=', None, boy=40)] * 2
        kutular.append(f'<div class="kutu" style="gap:14px;margin:14px 0;min-height:360px">{sayi_bagi(n, a, b, px=240)}<div style="display:grid;grid-template-columns:1fr;gap:16px">{"".join(eqs)}</div></div>')
    k.sayfa(''.join(kutular), baslik='İşlem ailesi', no=5,
            yonerge=['Sayı bağına bak. Boş kutuları <b>doldur</b>.', 'Eksik sayıları bul, <b>yaz</b>.', 'Ailenin dört işlemini kendin <b>yaz</b>.'][p],
            alt_yonerge='İki toplama, iki çıkarma. Çıkarma bütünden başlar.')

# ---------- BÖLÜM 6 · 20'ye kadar ----------
n = 13; assert 10 + 3 == n
k.sayfa(f'''<div class="kutu" style="flex-direction:column;gap:14px;background:#fff7ed;border-color:#fed7aa">
<div style="display:flex;gap:18px;align-items:center">{cerceve(10, 10, 46)}{cerceve(3, 10, 46, renk=MAV)}</div>
<div style="display:flex;gap:40px;font-size:22px;font-weight:800"><span style="color:{KIR}">1 onluk = 10</span><span style="color:{MAV}">3 birlik = 3</span></div></div>
<div class="kutu" style="flex-direction:column;gap:6px">{islem(10, '+', 3, '=', 13, boy=70)}<div style="font-size:40px;font-weight:900;color:{KOYU}">on üç</div></div>
<div class="not">10 nesneyi bir bardağa (ya da lastikle demete) koyup "bir onluk" deyin, kalanları tek tek sayın: "on… on bir, on iki, on üç". 11–19 arası sayılar hep "on" ile başlar.</div>''',
        baslik='Onluk ve birlik', no=6, yonerge="10'dan büyük sayılar: <b>bir onluk</b> ve birlikler.", alt_yonerge='Dolu çerçeve = 10. Yanındaki çerçevede birlikler.', oyun=OY_KUM)

for grup_ in [(11, 12, 13), (14, 15, 16), (17, 18, 19, 20)]:
    sat = []
    for v in grup_:
        bir = v - 10; assert 0 <= bir <= 10 and 10 + bir == v
        sat.append(f'<div class="kutu" style="min-height:{200 if len(grup_) == 3 else 160}px;margin:10px 0;padding:12px;gap:14px;flex-wrap:wrap"><div style="display:flex;gap:8px">{cerceve(10, 10, 32)}{cerceve(bir, 10, 32, renk=MAV)}</div>'
                   f'<div style="text-align:center;width:130px"><div style="font-size:66px;font-weight:900;line-height:1">{v}</div><div style="font-size:19px;font-weight:800;color:{KOYU}">{RAKAM_AD[v]}</div></div>'
                   f'<div class="cizgi" style="width:120px;height:60px"></div></div>')
    k.sayfa(''.join(sat), baslik=f"Sayılar {grup_[0]}–{grup_[-1]}", no=6,
            yonerge='Sayıyı oku. Çizginin üstüne <b>yaz</b>.', alt_yonerge='Önce çerçeveleri say: on, on bir, on iki…')

kac = [16, 12, 19]
k.sayfa(''.join(f'<div class="kutu" style="flex-direction:column;gap:12px"><div style="display:flex;gap:14px">{cerceve(10, 10, 46)}{cerceve(v-10, 10, 46, renk=MAV)}</div>{islem(10, "+", None, "=", None, boy=52)}</div>' for v in kac),
        baslik='Kaç tane?', no=6, yonerge='Onluğu ve birlikleri say. Boş kutulara <b>yaz</b>.', alt_yonerge='Dolu çerçeveyi tek tek saymaya gerek yok: o 10.')

on_n = [(10, 4, None), (10, 7, None), (10, 2, None), (10, None, 15), (10, None, 18), (None, 1, 11)]
kut = []
for x, y, z in on_n:
    vals = [x, y, z]; bilinmeyen = vals.count(None); assert bilinmeyen == 1
    if z is None: assert 10 + y <= 20
    if y is None: assert z - 10 >= 0
    if x is None: assert z - y == 10
    kut.append(f'<div class="kutu" style="min-height:190px;margin:0">{islem(x, "+", y, "=", z, boy=50)}</div>')
k.sayfa(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px">{"".join(kut)}</div>'
        '<div class="not">10 + birlik: sonuç "on…" diye okunur. 10 + 4 = 14 (on dört). Zorlanırsa bir önceki sayfadaki çerçevelere dönün.</div>',
        baslik='10 + birlik', no=6, yonerge='Boş kutuya doğru sayıyı <b>yaz</b>.', alt_yonerge='İpucu: on dört = 10 + 4.')

ek20 = [(12, 3), (14, 5), (11, 6)]
k.sayfa(''.join(f'<div class="kutu" style="flex-direction:column;gap:12px"><div style="display:flex;gap:14px">{cerceve(10, 10, 46)}{cerceve(a-10, 10, 46, ikinci=b)}</div>{islem(a, "+", b, "=", None, boy=52)}</div>'
                for a, b in ek20 if a + b <= 20 and a - 10 + b <= 10),
        baslik="20 içinde toplama", no=6, yonerge='Kırmızılar ve maviler birlikte kaç? <b>Yaz</b>.', alt_yonerge='Onluk yerinde kalır; birlikleri topla.')

cik20 = [(17, 3), (19, 5)]
for a, b in cik20: assert a - b >= 10
k.sayfa(''.join(f'<div class="kutu" style="flex-direction:column;gap:8px;margin:14px 0;min-height:330px"><div style="font-size:20px;font-weight:700"><b style="color:#dc2626">{a}</b> üzerinden {b} kez <b>geri</b> zıpla.</div>'
                f'{sayi_dogrusu(10, 20, isaret={a}, atla=(a, -b) if i == 0 else None, w=660)}{islem(a, EKSI, b, "=", None)}</div>' for i, (a, b) in enumerate(cik20)),
        baslik='20 içinde çıkarma', no=6, yonerge='Sayı doğrusunda geri say. Nerede durdun? <b>Yaz</b>.', alt_yonerge='İkinci soruda yayları kendin çiz.')

# ---------- BÖLÜM 7 · Karışık ----------
KARISIK = [("Nehir {a} çiçek topladı. {b} çiçeğini annesine verdi. Nehir'in kaç çiçeği kaldı?", '🌼', 8, 3, '-'),
           ("Sınıfta {a} kalem var. Öğretmen {b} kalem daha getirdi. Sınıfta kaç kalem oldu?", '✏️', 10, 4, '+'),
           ("Tabakta {a} çilek var. Emir {b} çilek yedi. Tabakta kaç çilek kaldı?", '🍓', 12, 2, '-'),
           ("Ali {a} yıldız çizdi. Ela {b} yıldız çizdi. İkisi toplam kaç yıldız çizdi?", '⭐', 6, 3, '+'),
           ("Bahçede {a} yaprak var. Rüzgâr {b} yaprağı uçurdu. Bahçede kaç yaprak kaldı?", '🍁', 15, 4, '-'),
           ("Defne {a} kek yaptı. Sonra {b} kek daha yaptı. Kaç kek oldu?", '🧁', 13, 5, '+')]
for i in range(0, 6, 2):
    kutular = []
    for t, em, a, b, op in KARISIK[i:i + 2]:
        c = a + b if op == '+' else a - b; assert 0 <= c <= 20
        res = (f'<div style="display:flex;align-items:center;gap:16px">{grup(em, a, 38, renk=KIR, bg="#fef2f2")}{arti(40)}{grup(em, b, 38, renk=MAV, bg="#eff6ff")}</div>'
               if op == '+' else grup(em, a, 44, cizik=b))
        kutular.append(f'<div class="kutu" style="flex-direction:column;gap:12px;margin:12px 0;min-height:330px">{hikaye_metin(t.format(a=a, b=b))}{res}{islem(a, "○", b, "=", None)}</div>')
    k.sayfa(''.join(kutular), baslik='Toplama mı, çıkarma mı?', no=7, yonerge='Daireye <b>+</b> ya da <b>−</b> yaz. Sonucu bul, <b>yaz</b>.',
            alt_yonerge='"Daha geldi, daha yaptı" → toplama. "Gitti, yedi, verdi" → çıkarma.')

k.sayfa(f'''<div class="kutu" style="min-height:330px;align-items:flex-start;justify-content:flex-start;flex-direction:column;border-style:dashed">
<div style="font-size:16px;color:#94a3b8;font-weight:700">Resmini buraya çiz:</div></div>
<div style="font-size:19px;font-weight:700;line-height:1.7;margin:6px 4px">Kimler var? Ne var? Kaç tane? · Sonra ne oldu? Geldi mi, gitti mi? · Şimdi kaç tane?</div>
<div class="kutu" style="min-height:120px">{islem(None, '○', None, '=', None, boy=56)}</div>
<div class="not">Çocuk hikâyesini sözlü anlatsın, siz yazabilirsiniz. Sayıları 10 ya da 20 ile sınırlayın. Kendi hikâyesini kurmak, problemi anlamayı destekler.</div>''',
        baslik='Kendi hikâyeni anlat', no=7, yonerge='Bir toplama ya da çıkarma hikâyesi <b>uydur</b>. Resmini çiz, işlemini yaz.', alt_yonerge='Örnek: "Masada 4 elma vardı, 2 elma daha koydum…"')

TEKRAR = [(4, '+', 3), (9, EKSI, 2), (5, '+', 5), (7, EKSI, 4), (10, '+', 6), (18, EKSI, 3), (2, '+', 6), (14, EKSI, 4)]
kut = []
for a, op, b in TEKRAR:
    c = a + b if op == '+' else a - b; assert 0 <= c <= 20
    kut.append(f'<div class="kutu" style="min-height:150px;margin:0">{islem(a, op, b, "=", None, boy=48)}</div>')
k.sayfa(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px">{"".join(kut)}</div>',
        baslik='Karışık tekrar', no=7, yonerge='İşlemleri yap, <b>yaz</b>.', alt_yonerge='Parmak, sayı doğrusu ya da çerçeve kullanılabilir. İşarete dikkat: + mı, − mi?', oyun=OY_KUM)

a, b = 9, 4; assert a - b == 5
k.sayfa(f'''<div class="kutu" style="gap:16px">{sayi_bagi(10, 7, 3, gizle='p2', px=180)}<div style="font-size:20px;font-weight:700">Eksik parçayı yaz.</div></div>
<div class="kutu" style="flex-direction:column;gap:12px">{cerceve(6, 10, 52, ikinci=3)}{islem(None, '+', None, '=', None, boy=44)}</div>
<div class="kutu" style="flex-direction:column;gap:6px">{sayi_dogrusu(0, 10, isaret={a}, w=640)}{islem(a, EKSI, b, '=', None, boy=44)}</div>''',
        baslik='Karışık tekrar', no=7, yonerge='Üç görev: sayı bağı, çerçeve, sayı doğrusu.', alt_yonerge='Her kutu ayrı bir görev; birini bitirince ötekine geçin.')
assert 6 + 3 == 9 and 7 + 3 == 10

k.basardim("10'a kadar toplama ve çıkarma yapıyorum, 20'ye kadar sayıları tanıyorum.<br>Hikâyeleri işleme dönüştürüyorum.")
print('Kitap 3 sayfa:', k.pdf('/home/claude/mat/cikti/Tane_Tane_Matematik_3_Toplama_Cikarma.pdf'))
