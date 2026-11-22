# -*- coding: utf-8 -*-
"""Kitap 2 · On'a Kadar Sayıyorum (6–10 ve sayı hissi) — okul öncesi + özel gereksinim.
Okul öncesi düzeyi: çoktan seçmeli sorular HER ZAMAN 2 seçenek (sec2 ile zorlanır)."""
import random
from lib import *

k = Kitap('k2', "On'a Kadar Sayıyorum", "6'dan 10'a ve sayı hissi", '2. Kitap', 'Okul öncesi · 1. sınıf · Özel eğitim')
R = random.Random(22)
MAV, ACIK, KOYU = k.renk, k.acik, k.koyu
KIR = '#ef4444'
OY_PARMAK = ("Sihirli Parmaklar · 1'den 10'a", 'sihirlii parmaklar.html')
OY_MATAKIS = ('MatAkış — Gör, Dokun, Oyna', 'matakis.html')
OY_MINIK = ('Minik Kâşifler', 'minik kasiflerr.html')
OY_KUM = ('Kum Tüneli', 'kumm tuneliii.html')
QR_SAY = 0


# ---------- yardımcılar (lib'e dokunmadan) ----------
def ns(em, n, boy=54, sutun=None, duzen='izgara'):
    """nesneler() + görseldeki nesne sayısının doğrulanması."""
    h = nesneler(em, n, boy, sutun, duzen)
    if n == 0:
        assert 'bos' in h
    elif duzen == 'zar' and n <= 6:
        assert h.count(f'line-height:1">{em}</span>') == n, (em, n)
    else:
        assert h.count(f'<span>{em}</span>') == n, (em, n)
    return h


def sec2(dogru, yanlis, seed, boy=72):
    """Okul öncesi: yalnız 2 seçenek."""
    assert dogru != yanlis
    li = iki_secenek(dogru, yanlis, seed)
    assert len(li) == 2 and dogru in li
    return secenek(li, dogru, boy)


def yakin_yanlis(m, alt=0, ust=10):
    """Doğruya bir uzak (±1) ama aralık içinde, doğrudan farklı."""
    c = [v for v in (m - 1, m + 1) if alt <= v <= ust]
    y = R.choice(c)
    assert y != m
    return y


def nokta_bes(n, px=110, renk=KIR):
    """Nokta kartı: 6–10 her zaman '5 ve kalan' (iki kart). 0–5 tek kart."""
    assert 0 <= n <= 10
    if n <= 5:
        return nokta_karti(n, px, renk)
    def zar(kk, x0):
        return ''.join(f'<circle cx="{x0 + x * 100:.1f}" cy="{y * 100:.1f}" r="10" fill="{renk}"/>' for x, y in ZAR[kk])
    kalan = n - 5
    assert 1 <= kalan <= 5
    s = (f'<svg viewBox="0 0 204 100" width="{px*2.04:.0f}" height="{px}">'
         f'<rect x="2" y="2" width="96" height="96" rx="16" fill="#fff" stroke="#0f172a" stroke-width="3"/>'
         f'<rect x="106" y="2" width="96" height="96" rx="16" fill="#fff" stroke="#0f172a" stroke-width="3"/>{zar(5, 0)}{zar(kalan, 104)}</svg>')
    assert s.count('<circle') == n
    return s


def onluk(n, px=50, renk=KIR, ikinci=0, ikinci_renk=None, bos=False):
    h = cerceve(n, 10, px, renk, ikinci, ikinci_renk or MAV, bos)
    assert h.count('<circle') == (10 if bos else n + ikinci)
    return h


def tabak(em, n, boy=46):
    """Tabak/kase içinde n nesne (0 = boş tabak)."""
    ic = '' if n == 0 else ''.join(f'<span>{em}</span>' for _ in range(n))
    assert ic.count('<span>') == n
    return (f'<div style="width:300px;min-height:150px;border:5px solid #94a3b8;border-radius:50%/40%;background:#f8fafc;'
            f'display:flex;flex-wrap:wrap;justify-content:center;align-content:center;gap:2px 6px;padding:22px 40px;font-size:{boy}px;line-height:1.1">{ic}</div>')


def bes_ve(n):
    assert 6 <= n <= 10
    return f'<b style="color:{KIR}">5</b> ve <b style="color:{MAV}">{n-5}</b>'


# ---------- kapak + aileler ----------
k.kapak("6'dan 10'a kadar sayıları <b>beşlik yapıyla</b> öğreten çalışma kitabı: \"6, 5 ve 1'dir.\" Sıfır, sayı doğrusu, 1 fazla–1 eksik, karşılaştırma ve sıralama ile sayı hissi gelişir.",
        f'<div style="font-size:84px;font-weight:900;color:{MAV};letter-spacing:8px">6 7 8 9 10</div>')

k.sayfa(f'''<div style="font-size:15.5px;line-height:1.55">
<p><b>Bu kitap nasıl çalışır?</b> 1. Kitaptaki düzen aynen sürer. Her sayı (6, 7, 8, 9, 10) için aynı beş sayfa vardır. Bildik düzen, özellikle özel gereksinimli çocuklarda güveni ve bağımsızlığı kolaylaştırır.</p>
<table class="tbl"><tr><th>Sayfa</th><th>Ne yapıyoruz?</th><th>Sizin rolünüz</th></tr>
<tr><td>🌱 Tanışma</td><td>Sayıyı nesnelerle, nokta kartıyla ve onluk çerçeveyle görür.</td><td>Önce gerçek nesnelerle (fasulye, lego, düğme) sayın.</td></tr>
<tr><td>👆 Say ve seç</td><td>Sayar, iki sayıdan doğru olanı daire içine alır.</td><td>Her nesneye dokunarak saymasını isteyin.</td></tr>
<tr><td>✏️ Rakam yaz</td><td>Rakamı izler, sonra kendisi yazar.</td><td>10'da iki rakam olduğunu gösterin: 1 ve 0.</td></tr>
<tr><td>🟥 Onluk çerçeve</td><td>Çerçeveyi boyar, "5 ve kaç?" sorusunu yanıtlar.</td><td>"Üst sıra dolu, alt sırada kaç var?" diye sorun.</td></tr>
<tr><td>🔗 Eşleştir</td><td>Nokta kartlarını rakamlarla eşleştirir.</td><td>Saymadan tanırsa övün, sonra sayarak kontrol etsin.</td></tr></table>
<p style="margin-top:10px"><b>"5 ve biraz" fikri:</b> 6'dan 10'a kadar her sayıyı <b style="color:{KIR}">5</b> ve <b style="color:{MAV}">kalan</b> olarak görürüz (7 = 5 ve 2). Nokta kartlarında ve onluk çerçevede ilk 5 hep aynı yerde durur. Böylece çocuk her seferinde 1'den saymak yerine "5'i biliyorum, 2 daha" diye düşünmeye başlar. Beşlik ve onluk yapıyla çalışmak, erken matematikte araştırmalarla desteklenen bir yaklaşımdır.</p>
<p><b>Sonraki bölümler:</b> Sıfır (hiç yok), sayı doğrusu, 1 fazla–1 eksik, çok–az karşılaştırma, sıralama ve bir bakışta tanıma.</p>
<p><b>Özel gereksinimli çocuklar için:</b> Sorularda hep iki seçenek vardır. Sayfayı katlayıp tek görev gösterebilirsiniz. Önce siz yapın, sonra birlikte, en son kendisi. Günde 1–2 sayfa, kısa ve sık çalışma uzun oturumlardan daha verimlidir. Zorlanırsa bir adım geri gidin: gerçek nesnelere dönün.</p>
<p><b>Dijital destek:</b> Bazı sayfaların köşesindeki QR kod, sitedeki ilgili oyunu açar. Kitap ana çalışmadır; oyun pekiştirme içindir.</p></div>''',
        baslik='Aileler ve öğretmenler için', no='i')

# ---------- 6–10 dersleri ----------
ADLAR = {6: 'Altı', 7: 'Yedi', 8: 'Sekiz', 9: 'Dokuz', 10: 'On'}
NES_SIRA = [0, 3, 7, 9, 19]  # elma, balon, kelebek, çiçek, civciv → tanışma nesneleri
for idx, n in enumerate(range(6, 11)):
    ad, em = NESNE[NES_SIRA[idx]]
    # 1) Tanışma
    g = f'''<div class="kutu" style="border-color:#bfdbfe;background:#eff6ff"><div class="buyuk" style="color:{MAV}">{n}</div>
<div style="text-align:center"><div style="font-size:44px;font-weight:900;color:{KOYU}">{RAKAM_AD[n]}</div>
<div style="font-size:28px;font-weight:700;margin-top:8px">{n} = {bes_ve(n)}</div></div></div>
<div class="kutu">{ns(em, n, 58, 5)}<div style="font-size:26px;font-weight:800">{n} {ad}</div></div>
<div class="kutu">{nokta_bes(n, 108)}{onluk(5, 50, KIR, n - 5, MAV)}</div>
<div class="not">Birlikte sayın: "{', '.join(RAKAM_AD[1:n+1])}". Sonra kırmızı 5'i gösterip "Burada 5 var, {RAKAM_AD[n-5]} tane daha: {RAKAM_AD[n]}" deyin.</div>'''
    k.sayfa(g, baslik=f'{ADLAR[n]} sayısıyla tanışalım', no=n, yonerge=f'Bu sayı <b style="color:{MAV}">{n}</b>. Nesneleri say, noktaları göster.',
            oyun=OY_PARMAK if n in (6, 9) else None)

    # 2) Say ve seç (iki seçenek)
    satirlar = []
    for j in range(3):
        m = n if j == 0 else R.randint(max(5, n - 3), n)
        yanlis = yakin_yanlis(m, 1, 10)
        ad2, em2 = NESNE[(n * 5 + j * 7) % len(NESNE)]
        satirlar.append(f'<div class="kutu">{ns(em2, m, 50, 5)}{sec2(m, yanlis, j + n, 72)}</div>')
    k.sayfa(''.join(satirlar), baslik='Say ve daire içine al', no=n, yonerge='Kaç tane var? Doğru sayıyı <b>daire içine al</b>.',
            alt_yonerge='İpucu: Üst sırada hep 5 tane var. "5… sonra 6, 7…" diye devam et.')

    # 3) Rakam yaz
    tek = len(str(n)) == 1
    k.sayfa(rakam_izle(n, 320 if tek else 290, MAV, 6 if tek else 4) + '<div class="yon" style="font-size:19px">Şimdi kendin yaz:</div>' + '<div class="cizgi"></div>' * 2 +
            f'<div style="margin-top:10px">{ns(em, n, 42, 10 if n == 10 else 5)}</div>',
            baslik=f'{n} rakamını yazalım' if tek else '10 sayısını yazalım', no=n,
            yonerge='Kesikli çizginin üzerinden parmağınla, sonra kalemle geç.' if tek else '10 (on) sayısı iki rakamla yazılır: önce <b>1</b>, sonra <b>0</b>.',
            alt_yonerge='Önce havada parmakla çiz, sonra kâğıda geç.' if tek else '1 ile 0 arasında küçük bir boşluk bırakın; iki rakam yan yana durur.')

    # 4) Onluk çerçeve
    yan = yakin_yanlis(n, 6, 10)
    g = f'''<div class="kutu" style="flex-direction:column"><div style="font-size:22px;font-weight:800">{n} tane yuvarlak boya</div>{onluk(0, 64, bos=True)}</div>
<div class="kutu"><div>{onluk(n, 50, MAV)}</div>{sec2(n, yan, n, 64)}</div>
<div class="kutu"><div style="font-size:21px;font-weight:700;line-height:1.5">Üst sırada <b style="color:{KIR}">5</b> var.<br>Alt sırada kaç var?</div>{onluk(5, 46, KIR, n - 5, MAV)}<div style="font-size:30px;font-weight:900">5 ve <span style="color:#94a3b8">___</span></div></div>'''
    k.sayfa(g, baslik='Onluk çerçeve', no=n, yonerge='Çerçevede kaç tane var?', alt_yonerge='Onluk çerçevede üst sıra dolunca 5 olur. 10 olması için kaç kutu boş, birlikte bakın.',
            oyun=OY_MATAKIS if n in (7, 10) else None)

    # 5) Eşleştir
    sol = list(range(n - 3, n + 1))
    sag = sol[:]
    R.shuffle(sag)
    while any(a == b for a, b in zip(sol, sag)):
        R.shuffle(sag)
    R.shuffle(sol)
    assert sorted(sol) == sorted(sag)
    satir = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;margin:16px 10px"><div style="width:240px">{nokta_bes(a, 88, MAV)}</div>'
                    f'<span style="font-size:20px;color:#cbd5e1">● · · · · ●</span><span style="font-size:72px;font-weight:900;width:120px;text-align:center">{b}</span></div>' for a, b in zip(sol, sag))
    k.sayfa(satir, baslik='Eşleştir', no=n, yonerge='Noktaları rakamla <b>çizgiyle</b> eşleştir.',
            alt_yonerge='İki kart varsa ilk kart hep 5. "5 ve kaç?" diye düşün.')

# ---------- Sıfır ----------
g = f'''<div class="kutu" style="border-color:#bfdbfe;background:#eff6ff"><div class="buyuk" style="color:{MAV}">0</div>
<div style="font-size:44px;font-weight:900;color:{KOYU}">sıfır</div><div style="font-size:26px;font-weight:700">hiç yok</div></div>
<div class="kutu" style="flex-direction:column;gap:8px">{tabak('🍎', 0)}<div style="font-size:22px;font-weight:800">Tabakta hiç elma yok: <span style="color:{MAV}">0 elma</span></div></div>
<div class="kutu">{nokta_karti(0, 120)}{cerceve(0, 5, 60)}</div>
<div class="not">Gerçek bir kapla oynayın: içine 3 nesne koyun, tek tek çıkarın. "3, 2, 1… hiç kalmadı: sıfır." Boş kap = 0.</div>'''
k.sayfa(g, baslik='Sıfır: hiç yok', no=0, yonerge='Hiç yoksa <b>0</b> deriz.')

satirlar = []
for j, (m, ems) in enumerate([(0, '🍓'), (2, '🍊'), (0, '🧁')]):
    yanlis = 1 if m == 0 else (0 if j == 1 else m + 1)
    satirlar.append(f'<div class="kutu" style="min-height:200px">{tabak(ems, m, 44)}{sec2(m, yanlis, j, 72)}</div>')
k.sayfa(''.join(satirlar), baslik='Tabakta kaç tane?', no=0, yonerge='Tabakta kaç tane var? Doğru sayıyı <b>daire içine al</b>.',
        alt_yonerge='Boş tabak için "hiç yok, sıfır" demesini bekleyin.')

# ---------- Sayı doğrusu 0–10 ----------
W = 680
bos1 = sorted(R.sample(range(1, 10), 3))
bos2 = sorted(R.sample([v for v in range(0, 11) if v not in bos1], 4))
g = f'''<div class="kutu" style="flex-direction:column;gap:4px;min-height:0"><div style="font-size:19px;font-weight:700">Parmağınla 0'dan 10'a yürü:</div>{sayi_dogrusu(0, 10, isaret=[0, 5, 10], w=W)}</div>
<div class="kutu" style="flex-direction:column;gap:4px;min-height:0">{sayi_dogrusu(0, 10, bos=bos1, w=W)}</div>
<div class="kutu" style="flex-direction:column;gap:4px;min-height:0">{sayi_dogrusu(0, 10, bos=bos2, w=W)}</div>
<div class="not">Sayı doğrusunda sağa gittikçe sayılar büyür. 5'in tam ortada durduğunu gösterin. Yerde ip ya da bantla bir sayı doğrusu yapıp üzerinde yürümek çok işe yarar.</div>'''
k.sayfa(g, baslik='Sayı doğrusu', no='★', yonerge='Boş kutulara eksik sayıları yaz.', alt_yonerge='Soldan başlayıp sayarak ilerle.', oyun=OY_KUM)

bos3 = sorted(R.sample(range(0, 11), 5))
g = f'''<div class="kutu" style="flex-direction:column;gap:4px;min-height:0">{sayi_dogrusu(0, 10, bos=bos3, w=W)}</div>
<div class="kutu" style="flex-direction:column;gap:6px;min-height:0"><div style="font-size:20px;font-weight:700">Tavşan 4'ten başladı, 3 zıpladı. Nereye geldi? Daire içine al.</div>{sayi_dogrusu(0, 10, isaret=[4], atla=(4, 3), w=W)}{sec2(7, 6, 1, 60)}</div>
<div class="kutu" style="flex-direction:column;gap:6px;min-height:0"><div style="font-size:20px;font-weight:700">Kurbağa 6'dan başladı, 2 zıpladı. Nereye geldi?</div>{sayi_dogrusu(0, 10, isaret=[6], atla=(6, 2), w=W)}{sec2(8, 9, 0, 60)}</div>'''
assert 4 + 3 == 7 and 6 + 2 == 8
k.sayfa(g, baslik='Sayı doğrusunda zıpla', no='★', yonerge='Eksikleri yaz, sonra zıplamaları say.', alt_yonerge='Her mavi yay bir zıplama. Yayları parmakla tek tek say.')

# ---------- 1 fazla / 1 eksik ----------
def fazla_kutu(n, em, seed):
    assert 0 <= n <= 9
    yeni = n + 1
    gorsel = ns(em, n, 46, 5) + f'<div style="font-size:40px;font-weight:900;color:{MAV}">+</div>' + ns(em, 1, 46)
    return f'<div class="kutu" style="min-height:190px"><div style="display:flex;align-items:center;gap:10px">{gorsel}</div>{sec2(yeni, n, seed, 64)}</div>'

def eksik_kutu(n, em, seed):
    assert 1 <= n <= 10
    kalan = n - 1
    items = ''.join(f'<span>{em}</span>' for _ in range(kalan)) + f'<span style="position:relative;opacity:.35">{em}<b style="position:absolute;inset:0;color:#dc2626;font-size:.9em;text-align:center">✕</b></span>'
    assert items.count(em) == n
    gorsel = f'<div class="nes" style="display:grid;grid-template-columns:repeat(5,58px);font-size:46px;line-height:1.2">{items}</div>'
    return f'<div class="kutu" style="min-height:190px">{gorsel}{sec2(kalan, n, seed, 64)}</div>'

fz = [(5, '🎈'), (7, '🦆'), (9, '⭐')]
k.sayfa(''.join(fazla_kutu(n, e, i) for i, (n, e) in enumerate(fz)), baslik='1 fazla', no='★',
        yonerge='Bir tane daha geldi. Şimdi kaç tane oldu? <b>Daire içine al.</b>', alt_yonerge='1 fazlası, sayı doğrusunda bir sonraki sayıdır.')
ek = [(6, '🍪' if False else '🍐'), (8, '🐟'), (10, '🍓')]
k.sayfa(''.join(eksik_kutu(n, e, i + 1) for i, (n, e) in enumerate(ek)), baslik='1 eksik', no='★',
        yonerge='Çarpı olan gitti. Kaç tane <b>kaldı</b>? Daire içine al.', alt_yonerge='1 eksiği, sayı doğrusunda bir önceki sayıdır. Çarpılı olanı saymayın.')

EK = {6: "'nın", 8: "'in", 9: "'un"}
satir = []
for i, (n, tur) in enumerate([(6, 'fazla'), (9, 'eksik'), (8, 'fazla')]):
    cevap = n + 1 if tur == 'fazla' else n - 1
    yanlis = n - 1 if tur == 'fazla' else n + 1
    assert 0 <= cevap <= 10 and 0 <= yanlis <= 10
    satir.append(f'''<div class="kutu" style="min-height:190px"><div style="text-align:center">{onluk(n, 40, MAV)}<div style="font-size:24px;font-weight:800;margin-top:8px">{n}{EK[n]} 1 <b style="color:{"#16a34a" if tur == "fazla" else "#dc2626"}">{"fazlası" if tur == "fazla" else "eksiği"}</b>?</div></div>{sec2(cevap, yanlis, i, 64)}</div>''')
k.sayfa(''.join(satir), baslik='1 fazla mı, 1 eksik mi?', no='★', yonerge='Çerçeveye bak. Doğru sayıyı daire içine al.',
        alt_yonerge='1 fazla: bir yuvarlak daha çiz. 1 eksik: bir yuvarlağın üstünü çiz. Sonra say.', oyun=OY_MATAKIS)

# ---------- Karşılaştırma ----------
for t, soru in enumerate(['çok', 'az']):
    a = R.randint(4, 10); b = R.randint(4, 10)
    while abs(a - b) < 2: b = R.randint(4, 10)
    dogru = ('A' if a > b else 'B') if soru == 'çok' else ('A' if a < b else 'B')
    ad1, em1 = NESNE[(t * 4 + 2) % len(NESNE)]; ad2, em2 = NESNE[(t * 4 + 11) % len(NESNE)]
    g = f'''<div class="kutu" style="min-height:260px"><div style="text-align:center">{ns(em1, a, 44, 5)}<div class="secc" style="font-size:30px;margin-top:10px">A</div></div>
<div style="font-size:40px;color:#cbd5e1">|</div><div style="text-align:center">{ns(em2, b, 44, 5)}<div class="secc" style="font-size:30px;margin-top:10px">B</div></div></div>
<div class="kutu" style="flex-direction:column;gap:8px;min-height:150px"><div style="font-size:21px;font-weight:700">Hangisi daha <b style="color:#dc2626">{soru}</b>? Harfini daire içine al.</div>
<div style="font-size:16px;color:#64748b">İpucu: Her {ad1} ile bir {ad2} arasında çizgi çek. Eşi olmayanlar hangi tarafta kaldı?</div></div>
<div class="kutu" style="min-height:150px"><div style="font-size:21px;font-weight:700">Şimdi say ve yaz:</div><div style="font-size:28px;font-weight:800">A: ____</div><div style="font-size:28px;font-weight:800">B: ____</div></div>'''
    assert dogru in ('A', 'B') and a != b
    k.sayfa(g, baslik=f'Hangisi daha {soru}?', no='★', yonerge='İki grubu karşılaştır.', alt_yonerge='Önce tahmin et, sonra eşleştirerek kontrol et.')

satir = []
for i, kim in enumerate(['büyük', 'küçük', 'büyük']):
    a = R.randint(3, 10); b = R.randint(3, 10)
    while a == b: b = R.randint(3, 10)
    cevap = max(a, b) if kim == 'büyük' else min(a, b)
    satir.append(f'''<div class="kutu" style="min-height:200px;flex-direction:column;gap:10px"><div style="font-size:20px;font-weight:700">Hangisi daha <b style="color:{MAV}">{kim}</b>?</div>
<div style="display:flex;gap:40px;align-items:center"><div style="text-align:center">{onluk(a, 30, KIR)}<div class="secc" style="font-size:52px;margin-top:6px">{a}</div></div>
<div style="text-align:center">{onluk(b, 30, MAV)}<div class="secc" style="font-size:52px;margin-top:6px">{b}</div></div></div></div>''')
    assert cevap in (a, b)
k.sayfa(''.join(satir), baslik='Büyük mü, küçük mü?', no='★', yonerge='Doğru sayıyı <b>daire içine al</b>.',
        alt_yonerge='Çerçevede daha çok yuvarlak olan sayı daha büyüktür. Sayı doğrusunda daha sağdadır.', oyun=OY_KUM)

# ---------- Sıralama ----------
def vagonlar(seq, bos):
    out = []
    for v in seq:
        b = v in bos
        out.append(f'<div style="text-align:center"><div style="font-size:52px;line-height:1">🚃</div><span class="secc" style="font-size:46px;margin-top:4px;'
                   f'border-style:{"dashed" if b else "solid"};border-color:{"#ea580c" if b else MAV}">{"&nbsp;" if b else v}</span></div>')
    return '<div style="display:flex;justify-content:center;gap:14px;align-items:flex-end"><div style="font-size:58px">🚂</div>' + ''.join(out) + '</div>'

b1 = R.sample(range(1, 6), 2); b2 = R.sample(range(6, 11), 2)
g = (f'<div class="kutu" style="flex-direction:column">{vagonlar(range(1, 6), b1)}</div>'
     f'<div class="kutu" style="flex-direction:column">{vagonlar(range(6, 11), b2)}</div>'
     '<div class="not">Sayıları sırayla yüksek sesle söyleyin. Boş vagona hangi sayı gelir? Her vagon bir öncekinden 1 fazladır.</div>')
k.sayfa(g, baslik='Sayı treni', no='★', yonerge='Eksik vagonlara sayıları yaz.', alt_yonerge='Küçükten büyüğe: 1, 2, 3 … 10.')

satir = []
for i in range(3):
    s = sorted(R.sample(range(1, 11), 3 if i < 2 else 4))
    karisik = s[:]
    while karisik == s: R.shuffle(karisik)
    kut = ''.join(f'<span class="secc" style="font-size:52px;border-style:solid;border-color:{MAV};border-radius:16px">{v}</span>' for v in karisik)
    bosk = ''.join('<span style="display:inline-block;width:76px;height:76px;border:4px dashed #ea580c;border-radius:16px"></span>' for _ in s)
    satir.append(f'<div class="kutu" style="flex-direction:column;gap:14px;min-height:210px"><div class="sec">{kut}</div><div style="font-size:30px">⬇</div><div style="display:flex;gap:18px">{bosk}</div></div>')
    assert sorted(karisik) == s
k.sayfa(''.join(satir), baslik='Küçükten büyüğe sırala', no='★', yonerge='Sayıları küçükten büyüğe aşağıya yaz.',
        alt_yonerge='Zorlanırsa sayı doğrusuna bakın: soldaki küçüktür.')

# ---------- Anında tanı ----------
for t in range(2):
    sayilar = [R.randint(6, 10) for _ in range(6)]
    if t == 0:
        hucre = [nokta_bes(v, 82, KIR if i % 2 else MAV) for i, v in enumerate(sayilar)]
    else:
        hucre = [onluk(v, 34, KIR if i % 2 else MAV) for i, v in enumerate(sayilar)]
    g = '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:12px">' + ''.join(
        f'<div class="kutu" style="flex-direction:column;margin:0;min-height:200px">{h}<div class="cizgi" style="width:90px;height:50px"></div></div>' for h in hucre) + '</div>'
    k.sayfa(g + '<div class="not">Kartı 2 saniye gösterip kapatın, "Kaç tane gördün?" diye sorun. "5 ve 3, sekiz" gibi düşünmesi beklenen yoldur; saymadan tanımak sayı hissini güçlendirir.</div>',
            baslik='Bir bakışta söyle!', no='★', yonerge='Bir bak, kaç tane? Altına yaz.', oyun=OY_MINIK if t == 0 else OY_PARMAK)

# ---------- Karışık tekrar ----------
satir = []
for j in range(3):
    m = R.randint(6, 10); ad2, em2 = NESNE[(j * 9 + 4) % len(NESNE)]
    satir.append(f'<div class="kutu">{ns(em2, m, 50, 5)}<div class="cizgi" style="width:120px"></div></div>')
k.sayfa(''.join(satir), baslik='Tekrar zamanı', no='★', yonerge='Say ve kaç tane olduğunu <b>yaz</b>.', alt_yonerge='Zorlanırsa rakamı birlikte söyleyin, o izlesin.')

satir = []
for j in range(3):
    m = R.randint(6, 10)
    satir.append(f'<div class="kutu" style="flex-direction:column;gap:8px"><div style="font-size:21px;font-weight:700">{m} tane boya</div>{onluk(0, 56, bos=True)}</div>')
k.sayfa(''.join(satir), baslik='Tekrar zamanı', no='★', yonerge='Söylenen sayı kadar yuvarlak <b>boya</b>.', alt_yonerge='Üst sırayı doldurunca "5" deyin, alta devam edin.')

satir = []
for j in range(3):
    m = R.choice([0, 6, 7, 8, 9, 10]) if j else R.randint(6, 10)
    yanlis = yakin_yanlis(m, 0, 10)
    ad2, em2 = NESNE[(j * 5 + 13) % len(NESNE)]
    gor = tabak(em2, m, 38) if m == 0 else ns(em2, m, 48, 5)
    satir.append(f'<div class="kutu">{gor}{sec2(m, yanlis, j, 70)}</div>')
k.sayfa(''.join(satir), baslik='Tekrar zamanı', no='★', yonerge='Kaç tane var? Doğru sayıyı <b>daire içine al</b>.')

k.basardim("0'dan 10'a kadar sayıları tanıyorum, sayıyorum ve yazıyorum.<br>6'nın 5 ve 1 olduğunu biliyorum!")
print('Kitap 2 sayfa:', k.pdf('/home/claude/mat/cikti/Tane_Tane_Matematik_2_Ona_Kadar.pdf'))
