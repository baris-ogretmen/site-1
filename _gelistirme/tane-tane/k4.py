# -*- coding: utf-8 -*-
"""Kitap 4 · Şekiller, Örüntüler, Ölçme — okul öncesi + 1. sınıf + özel gereksinim.
Okul öncesi düzeyi: çoktan seçmeli sorularda HER ZAMAN 2 seçenek."""
import random
from lib import *

k = Kitap('k4', 'Şekiller, Örüntüler, Ölçme', 'Gör, karşılaştır, sırala', '4. Kitap', 'Okul öncesi · 1. sınıf · Özel eğitim')
R = random.Random(44)
MOR, ACIK, KOYU = TEMA['k4']
OY_KUP = ('Küp Yolu · Işık Hattı', 'kup yoluu.html')
OY_MINIK = ('Minik Kâşifler', 'minik kasiflerr.html')
OY_MATAKIS = ('MatAkış — Gör, Dokun, Oyna', 'matakis.html')
EMJ = "font-family:'Noto Color Emoji'"

# ================= yardımcılar (lib'e dokunmadan) =================
SEKILLER = ['daire', 'kare', 'üçgen', 'dikdörtgen']
KOSE = {'daire': 0, 'kare': 4, 'üçgen': 3, 'dikdörtgen': 4}
KENAR = {'daire': 0, 'kare': 4, 'üçgen': 3, 'dikdörtgen': 4}
SRENK = {'daire': '#ef4444', 'kare': '#3b82f6', 'üçgen': '#22c55e', 'dikdörtgen': '#f59e0b'}
KOSE_NOKTA = {'daire': [], 'kare': [(12, 12), (88, 12), (88, 88), (12, 88)], 'üçgen': [(50, 10), (90, 88), (10, 88)],
              'dikdörtgen': [(4, 26), (96, 26), (96, 74), (4, 74)]}
assert all(len(KOSE_NOKTA[s]) == KOSE[s] for s in SEKILLER)

def geo(ad, px=120, fill='#fff', stroke='#0f172a', kalin=5, dash=None, baslangic=False, kose_isaret=False):
    """Kendi şekil çizimimiz: kesikli (izleme) ve başlangıç noktası destekli."""
    d = f' stroke-dasharray="{dash}"' if dash else ''
    s = f'fill="{fill}" stroke="{stroke}" stroke-width="{kalin}" stroke-linejoin="round"{d}'
    g = {'daire': f'<circle cx="50" cy="50" r="42" {s}/>', 'kare': f'<rect x="12" y="12" width="76" height="76" {s}/>',
         'üçgen': f'<polygon points="50,10 90,88 10,88" {s}/>', 'dikdörtgen': f'<rect x="4" y="26" width="92" height="48" {s}/>'}[ad]
    if baslangic:
        bx, by = (50, 8) if ad == 'daire' else KOSE_NOKTA[ad][0]
        g += f'<circle cx="{bx}" cy="{by}" r="5" fill="#16a34a"/>'
    if kose_isaret:
        g += ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="#dc2626" stroke-width="3"/>' for x, y in KOSE_NOKTA[ad])
    return f'<svg viewBox="-4 -4 108 108" width="{px}" height="{px}" style="overflow:visible">{g}</svg>'

def emj(e, boy=60, ek=''):
    return f'<span style="font-size:{boy}px;line-height:1;{EMJ};{ek}">{e}</span>'

def yanlis_sayi(n, seed):
    """Doğrudan farklı, 0 altına düşmeyen yanlış seçenek."""
    y = n + 1 if (n == 0 or seed % 2 == 0) else n - 1
    assert y != n and y >= 0
    return y

def kelime_sec(liste, dogru, boy=28):
    assert dogru in liste and len(liste) == 2 and liste[0] != liste[1]
    return '<div class="sec">' + ''.join(f'<span style="display:inline-block;border:4px dashed #94a3b8;border-radius:999px;padding:8px 26px;font-size:{boy}px;font-weight:800">{E(x)}</span>' for x in liste) + '</div>'

def resim_sec(icerikler):
    """2 resimli seçenek (çocuk daire içine alır)."""
    assert len(icerikler) == 2
    return '<div class="sec">' + ''.join(f'<div style="border:4px dashed #94a3b8;border-radius:24px;padding:10px 14px;text-align:center;min-width:120px">{c}</div>' for c in icerikler) + '</div>'

def etiket(t, boy=16):
    return f'<div style="font-size:{boy}px;font-weight:700;color:#475569;margin-top:4px">{E(t)}</div>'

def kolon(*parcalar, gap=4):
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:{gap}px">' + ''.join(parcalar) + '</div>'

_gid = [0]
def kati(ad, px=110, renk='#9333ea'):
    """3B cisimler: küp, küre, silindir, koni (basit gölgeli çizim)."""
    _gid[0] += 1; gid = f'g{_gid[0]}'
    st = 'stroke="#0f172a" stroke-width="3" stroke-linejoin="round"'
    if ad == 'küp':
        g = (f'<polygon points="15,35 65,35 65,88 15,88" fill="{renk}" {st}/>'
             f'<polygon points="15,35 35,14 85,14 65,35" fill="{renk}" opacity=".75" {st}/>'
             f'<polygon points="65,35 85,14 85,67 65,88" fill="{renk}" opacity=".55" {st}/>')
    elif ad == 'küre':
        g = (f'<defs><radialGradient id="{gid}" cx="35%" cy="32%" r="70%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{renk}"/></radialGradient></defs>'
             f'<circle cx="50" cy="52" r="40" fill="url(#{gid})" {st}/>')
    elif ad == 'silindir':
        g = (f'<path d="M25 24 L25 80 A25 9 0 0 0 75 80 L75 24" fill="{renk}" opacity=".8" {st}/>'
             f'<ellipse cx="50" cy="24" rx="25" ry="9" fill="#fff" {st}/><ellipse cx="50" cy="24" rx="25" ry="9" fill="{renk}" opacity=".45" {st}/>')
    else:  # koni
        g = (f'<path d="M18 80 A32 10 0 0 0 82 80 L50 10 Z" fill="{renk}" opacity=".85" {st}/>'
             f'<path d="M18 80 A32 10 0 0 1 82 80" fill="none" stroke="#0f172a" stroke-width="2" stroke-dasharray="5 4"/>')
    return f'<svg viewBox="0 0 100 100" width="{px}" height="{px}">{g}</svg>'

def oge(x, boy=56):
    """Örüntü öğesi: ('c', renk) daire | ('s', şekil, renk) | emoji str | None (boş)."""
    if x is None:
        return f'<span style="display:inline-block;width:{boy}px;height:{boy}px;border:4px dashed #ea580c;border-radius:14px"></span>'
    if isinstance(x, tuple) and x[0] == 'c':
        return f'<svg viewBox="0 0 100 100" width="{boy}" height="{boy}"><circle cx="50" cy="50" r="42" fill="{x[1]}" stroke="#0f172a" stroke-width="5"/></svg>'
    if isinstance(x, tuple) and x[0] == 's':
        return geo(x[1], boy, x[2], kalin=6)
    if isinstance(x, tuple) and x[0] == 'bc':  # boyanacak boş daire
        return f'<svg viewBox="0 0 100 100" width="{boy}" height="{boy}"><circle cx="50" cy="50" r="42" fill="#fff" stroke="#94a3b8" stroke-width="5" stroke-dasharray="10 7"/></svg>'
    return emj(x, boy)

def oge_satir(seq, boy=56, gap=10):
    return f'<div style="display:flex;gap:{gap}px;align-items:center;justify-content:center;flex-wrap:nowrap">' + ''.join(oge(x, boy) for x in seq) + '</div>'

def oruntu(birim, uzunluk):
    return [birim[i % len(birim)] for i in range(uzunluk)]

def siradaki(birim, uzunluk):
    """Gösterilen 'uzunluk' öğeden sonra gelecek doğru öğe + farklı bir yanlış öğe."""
    d = birim[uzunluk % len(birim)]
    y = next(b for b in birim if b != d)
    assert d != y
    return d, y

def oku(yon, px=140, renk='#9333ea'):
    p = '10,50 60,10 60,32 130,32 130,68 60,68 60,90' if yon == 'sol' else '130,50 80,10 80,32 10,32 10,68 80,68 80,90'
    return f'<svg viewBox="0 0 140 100" width="{px}" height="{px*100/140:.0f}"><polygon points="{p}" fill="{renk}" stroke="#0f172a" stroke-width="4" stroke-linejoin="round"/></svg>'

def terazi(sol, sag, agir, px=330):
    """agir: 'sol' | 'sag' — ağır taraf aşağı iner."""
    assert agir in ('sol', 'sag')
    dy = 22 if agir == 'sol' else -22
    ly, ry = 70 + dy, 70 - dy  # kol uçları
    def kefe(x, y, e):
        return (f'<line x1="{x}" y1="{y}" x2="{x-36}" y2="{y+52}" stroke="#64748b" stroke-width="2.5"/><line x1="{x}" y1="{y}" x2="{x+36}" y2="{y+52}" stroke="#64748b" stroke-width="2.5"/>'
                f'<path d="M{x-48} {y+52} Q{x} {y+84} {x+48} {y+52} Z" fill="#fde68a" stroke="#0f172a" stroke-width="3"/>'
                f'<text x="{x}" y="{y+48}" text-anchor="middle" font-size="46" style="{EMJ}">{e}</text>')
    return (f'<svg viewBox="0 0 300 220" width="{px}" height="{px*220/300:.0f}">'
            f'<polygon points="150,70 120,205 180,205" fill="#cbd5e1" stroke="#0f172a" stroke-width="3"/><rect x="95" y="203" width="110" height="12" rx="6" fill="#94a3b8"/>'
            f'<line x1="40" y1="{ly}" x2="260" y2="{ry}" stroke="#0f172a" stroke-width="7" stroke-linecap="round"/><circle cx="150" cy="70" r="8" fill="#9333ea"/>'
            + kefe(40, ly, sol) + kefe(260, ry, sag) + '</svg>')

def bardak(seviye, px=110):
    """seviye 0..1 su yüksekliği."""
    ust, alt_y = 10, 110
    wy = alt_y - seviye * 95
    xl = lambda y: 15 + (y - ust) / 100 * 10
    xr = lambda y: 85 - (y - ust) / 100 * 10
    su = (f'<polygon points="{xl(wy):.1f},{wy:.1f} {xr(wy):.1f},{wy:.1f} 75,110 25,110" fill="#60a5fa"/>' if seviye > 0 else '')
    return (f'<svg viewBox="0 0 100 120" width="{px}" height="{px*1.2:.0f}">{su}'
            f'<polygon points="15,10 85,10 75,110 25,110" fill="none" stroke="#0f172a" stroke-width="4" stroke-linejoin="round"/></svg>')

U = 56  # ölçme birimi (px)
def kalem(uz_px, renk='#f59e0b', kalin=26):
    gov = uz_px - 30
    return (f'<rect x="0" y="0" width="{gov}" height="{kalin}" rx="4" fill="{renk}" stroke="#0f172a" stroke-width="3"/>'
            f'<polygon points="{gov},0 {uz_px},{kalin/2} {gov},{kalin}" fill="#fde68a" stroke="#0f172a" stroke-width="3" stroke-linejoin="round"/>'
            f'<polygon points="{uz_px-9},{kalin/2-4} {uz_px},{kalin/2} {uz_px-9},{kalin/2+4}" fill="#0f172a"/>')

def olcum(n, birim='ataç', renk='#f59e0b'):
    """n birim uzunluğunda kalem + altında tam n birim (ataç ya da küp). Çizilen birim sayısı assert ile = n."""
    parcalar = []
    for i in range(n):
        x = i * U
        if birim == 'ataç':
            parcalar.append(f'<g transform="translate({x+3},48)"><rect width="{U-6}" height="20" rx="10" fill="none" stroke="#475569" stroke-width="3"/>'
                            f'<rect x="7" y="5" width="{U-20}" height="10" rx="5" fill="none" stroke="#475569" stroke-width="3"/></g>')
        else:
            c = ['#ef4444', '#3b82f6'][i % 2]
            parcalar.append(f'<rect x="{x+1}" y="44" width="{U-2}" height="{U-2}" rx="5" fill="{c}" stroke="#0f172a" stroke-width="3"/>')
    assert len(parcalar) == n
    h = 48 + U + 6
    return (f'<svg viewBox="-2 -2 {n*U+6} {h}" width="{n*U+6}" height="{h}"><g transform="translate(0,6)">{kalem(n*U, renk)}</g>'
            f'<line x1="0" y1="0" x2="0" y2="{h}" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 4"/>{"".join(parcalar)}</svg>')

# ================= kapak + aileler =================
kapak_sek = '<div style="display:flex;gap:14px;align-items:flex-end">' + ''.join(geo(s, 78, SRENK[s], kalin=6) for s in SEKILLER) + '</div>'
k.kapak("Şekilleri tanımayı, örüntü kurmayı, gruplamayı, karşılaştırmayı ve ölçmeyi <b>adım adım</b> öğreten çalışma kitabı. "
        "Her kavram önce nesneyle, sonra resimle, en son işaretle çalışılır.", kapak_sek)

k.sayfa('''<div style="font-size:15.5px;line-height:1.55">
<p><b>Bu kitapta ne var?</b> Rakamlardan önce gelen, matematiğin temel düşünme becerileri: şekilleri tanıma, örüntü (tekrar eden düzen), sınıflama, karşılaştırma, ölçme, konum ve zaman kavramları.</p>
<table class="tbl"><tr><th>Bölüm</th><th>Ne yapıyoruz?</th><th>Sizin rolünüz</th></tr>
<tr><td>1 · Şekiller</td><td>Daire, kare, üçgen, dikdörtgen; köşe sayma, şekil izleme, şekillerle resim, 3B cisimler.</td><td>Evde aynı şekilli nesneleri birlikte arayın (tabak, pencere, kapı…). Köşelere parmakla dokunarak sayın.</td></tr>
<tr><td>2 · Örüntüler</td><td>AB, AAB, ABB, ABC düzenleri; renk, şekil, nesne, ses-hareket.</td><td>Örüntüyü önce yüksek sesle okuyun: "kırmızı, mavi, kırmızı, mavi…" Alkış–ayak gibi bedenle yapın.</td></tr>
<tr><td>3 · Sınıflama</td><td>Renge, şekle, büyüklüğe göre gruplama; farklı olanı bulma, gölge eşleme.</td><td>"Neden bu gruba koydun?" diye sorun; açıklamasını dinleyin.</td></tr>
<tr><td>4 · Karşılaştırma ve ölçme</td><td>Büyük–küçük, uzun–kısa, kalın–ince, ağır–hafif, dolu–boş; ataç ve küple ölçme, sıralama.</td><td>Gerçek nesnelerle deneyin: iki kalemi yan yana koyun, ataçları uç uca dizin.</td></tr>
<tr><td>5 · Konum</td><td>Üstünde–altında, içinde–dışında, önünde–arkasında, sağında–solunda, yakın–uzak.</td><td>Bir oyuncakla komut oyunu oynayın: "Ayıcığı masanın altına koy."</td></tr>
<tr><td>6 · Zaman</td><td>Önce–sonra sıralama, sabah–öğle–akşam, dün–bugün–yarın.</td><td>Günlük rutinleri sırayla konuşun.</td></tr></table>
<p style="margin-top:10px"><b>Nasıl kullanılır?</b> Her bölüm aynı sırayla ilerler: <b>tanı → bul → yap</b>. Okul öncesi düzeyine uygun olarak her soruda <b>yalnız iki seçenek</b> vardır; çocuk doğru olanı daire içine alır. Somut → resim → sembol sırası, erken matematik öğretiminde araştırmalarla desteklenen bir yaklaşımdır. Zorlanırsa bir adım geri gidin (gerçek nesnelere dönün).</p>
<p><b>Özel gereksinimli çocuklar için:</b> Sayfanın yalnız bir kutusunu açık bırakıp diğerlerini kâğıtla kapatabilirsiniz. Önce siz gösterin, sonra birlikte yapın, en son kendisi yapsın. Kavram çiftlerini (büyük–küçük gibi) önce gerçek nesnelerle, tek tek çalışın. Kısa ve sık çalışmak (günde 1–2 sayfa) daha verimlidir.</p>
<p><b>Dijital destek:</b> Bazı sayfalardaki QR kod, sitedeki ilgili oyunu açar. Kitap ana çalışmadır; oyun pekiştirme içindir.</p></div>''',
        baslik='Aileler ve öğretmenler için', no='i')

# ================= 1) ŞEKİLLER =================
ORNEK = {'daire': [('🍪', 'kurabiye'), ('🕒', 'saat'), ('🥏', 'frizbi')],
         'kare': [('🪟', 'pencere'), ('🧇', 'waffle'), ('🔲', 'düğme')],
         'üçgen': [('🍕', 'pizza dilimi'), ('⛺', 'çadır'), ('📐', 'gönye')],
         'dikdörtgen': [('🚪', 'kapı'), ('📱', 'telefon'), ('🍫', 'çikolata')]}
AD_BUYUK = {'daire': 'Daire', 'kare': 'Kare', 'üçgen': 'Üçgen', 'dikdörtgen': 'Dikdörtgen'}
KOSE_NOT = {'daire': 'Daire yuvarlaktır; köşesi ve düz kenarı yoktur.',
            'kare': 'Karenin 4 kenarı da birbirine eşittir.',
            'üçgen': 'Üçgenin 3 kenarı ve 3 köşesi vardır.',
            'dikdörtgen': 'Dikdörtgenin 2 uzun, 2 kısa kenarı vardır.'}

for si, sk in enumerate(SEKILLER):
    renk = SRENK[sk]
    # --- Tanış
    ornek = ''.join(kolon(emj(e, 72), etiket(a, 17)) for e, a in ORNEK[sk])
    if sk == 'daire':
        kose_soru = f'<div style="font-size:22px;font-weight:800">Dairenin köşesi var mı?</div>{kelime_sec(["Var", "Yok"] if si % 2 == 0 else ["Yok", "Var"], "Yok", 30)}'
    else:
        kc = KOSE[sk]
        kose_soru = f'<div style="font-size:22px;font-weight:800">Kaç köşesi var?</div>{secenek(iki_secenek(kc, yanlis_sayi(kc, si), si), kc, 60)}'
    g = f'''<div class="kutu" style="background:{ACIK};border-color:#e9d5ff">{geo(sk, 190, renk, kalin=6)}
<div style="text-align:center"><div style="font-size:54px;font-weight:900;color:{KOYU}">{AD_BUYUK[sk]}</div>
<div style="font-size:18px;color:#475569;margin-top:6px">{E(KOSE_NOT[sk])}</div></div></div>
<div class="kutu"><div style="font-size:19px;font-weight:700;width:120px">Hayatımızda:</div>{ornek}</div>
<div class="kutu">{geo(sk, 150, '#fff', kalin=6, kose_isaret=(sk != 'daire'))}{kolon(kose_soru, gap=12)}</div>
<div class="not">{'Kenarında parmağınızı gezdirin; köşe var mı, birlikte bakın.' if sk == 'daire' else 'Köşelere parmakla dokunarak birlikte sayın.'} Evde {E(sk)} şeklinde nesneler arayın ve kenarlarında parmağınızı gezdirin.</div>'''
    k.sayfa(g, baslik=f'{AD_BUYUK[sk]} ile tanışalım', no=1, yonerge=f'Bu şeklin adı <b style="color:{renk}">{sk}</b>. Göster, adını söyle.',
            oyun=OY_MATAKIS if sk == 'daire' else None)

    # --- Bul ve boya
    hedef = R.randint(4, 6)
    digerler = [s for s in SEKILLER if s != sk and not (sk == 'dikdörtgen' and s == 'kare')]  # kare de bir dikdörtgendir; karışmasın
    liste = [sk] * hedef + [R.choice(digerler) for _ in range(16 - hedef)]
    R.shuffle(liste)
    assert liste.count(sk) == hedef and len(liste) == 16
    izgara = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;justify-items:center;align-items:center;margin:8px 10px">' + \
        ''.join(geo(s, R.choice([84, 96, 108]), '#fff', kalin=5) for s in liste) + '</div>'
    g = f'''<div class="kutu" style="display:block;padding:10px">{izgara}</div>
<div class="kutu" style="min-height:150px"><div style="font-size:22px;font-weight:800">Kaç {E(sk)} boyadın?</div>{secenek(iki_secenek(hedef, yanlis_sayi(hedef, si + 1), si + 1), hedef, 64)}</div>'''
    k.sayfa(g, baslik=f'{AD_BUYUK[sk]} avı', no=1, yonerge=f'Bütün <b style="color:{renk}">{sk}leri</b> bul ve boya.' if sk != 'üçgen' else f'Bütün <b style="color:{renk}">üçgenleri</b> bul ve boya.',
            alt_yonerge='Önce parmakla göster, sonra boya. Boyadıklarını say.')

    # --- İzle ve çiz
    kucuk = ''.join(geo(sk, 112, '#fff', '#94a3b8', 4, '8 7', baslangic=True) for _ in range(4))
    g = f'''<div style="display:flex;justify-content:center;margin-top:4mm">{geo(sk, 300, '#fff', renk, 4, '12 9', baslangic=True)}</div>
<div class="kutu" style="min-height:150px">{kucuk}</div>
<div class="yon" style="font-size:19px">Şimdi kendin çiz:</div>
<div style="border:3px dashed #cbd5e1;border-radius:22px;height:200px"></div>'''
    k.sayfa(g, baslik=f'{AD_BUYUK[sk]} çizelim', no=1, yonerge='Yeşil noktadan başla, kesikli çizginin üzerinden geç.',
            alt_yonerge='Önce parmakla, sonra kalemle. Havada büyük çizmek de iyi bir ısınmadır.')

# --- Şekillerle resim (ev, robot)
def resim_sayfa(ad, parcalar, vb, px, baslik):
    """parcalar: (şekil_adı, svg) — sayım koddan."""
    sayim = {s: sum(1 for p in parcalar if p[0] == s) for s in SEKILLER}
    svg = f'<svg viewBox="{vb}" width="{px}" height="{px}">' + ''.join(p[1] for p in parcalar) + '</svg>'
    satir = ''.join(f'<div style="display:flex;align-items:center;gap:14px;margin:8px 0">{geo(s, 54, SRENK[s], kalin=6)}'
                    f'{secenek(iki_secenek(sayim[s], yanlis_sayi(sayim[s], i + len(ad)), i), sayim[s], 40)}</div>' for i, s in enumerate(SEKILLER))
    renkler = ' · '.join(f'<b style="color:{SRENK[s]}">{s}</b>' for s in SEKILLER)
    g = f'''<div class="kutu" style="align-items:center">{svg}<div>{satir}</div></div>
<div class="not">Boyama önerisi: {renkler}. Her şekli rengine boyayın, sonra sayın. Şekilleri kâğıttan kesip aynı resmi masada birlikte kurabilirsiniz.</div>'''
    k.sayfa(g, baslik=baslik, no=1, yonerge='Resmi şekillerin rengine boya. Her şekilden <b>kaç tane</b> var? Daire içine al.')
    return sayim

ST = 'fill="#fff" stroke="#0f172a" stroke-width="4" stroke-linejoin="round"'
ev = [('kare', f'<rect x="60" y="140" width="150" height="150" {ST}/>'),
      ('üçgen', f'<polygon points="45,140 135,55 225,140" {ST}/>'),
      ('dikdörtgen', f'<rect x="115" y="215" width="40" height="75" {ST}/>'),
      ('daire', f'<circle cx="92" cy="180" r="18" {ST}/>'), ('daire', f'<circle cx="178" cy="180" r="18" {ST}/>'),
      ('daire', f'<circle cx="262" cy="45" r="26" {ST}/>')]
s_ev = resim_sayfa('ev', ev, '0 0 300 300', 360, 'Şekillerle ev')
assert s_ev == {'daire': 3, 'kare': 1, 'üçgen': 1, 'dikdörtgen': 1}
robot = [('üçgen', f'<polygon points="138,30 150,6 162,30" {ST}/>'),
         ('kare', f'<rect x="110" y="30" width="80" height="80" {ST}/>'),
         ('daire', f'<circle cx="134" cy="64" r="11" {ST}/>'), ('daire', f'<circle cx="166" cy="64" r="11" {ST}/>'),
         ('dikdörtgen', f'<rect x="85" y="118" width="130" height="86" {ST}/>'),
         ('dikdörtgen', f'<rect x="30" y="130" width="50" height="22" {ST}/>'), ('dikdörtgen', f'<rect x="220" y="130" width="50" height="22" {ST}/>'),
         ('dikdörtgen', f'<rect x="108" y="210" width="28" height="68" {ST}/>'), ('dikdörtgen', f'<rect x="164" y="210" width="28" height="68" {ST}/>'),
         ('daire', f'<circle cx="150" cy="148" r="10" {ST}/>'), ('daire', f'<circle cx="150" cy="178" r="10" {ST}/>')]
s_rb = resim_sayfa('robot', robot, '0 0 300 300', 360, 'Şekillerle robot')
assert s_rb == {'daire': 4, 'kare': 1, 'üçgen': 1, 'dikdörtgen': 5}

# --- 3B cisimler
KATI = ['küp', 'küre', 'silindir', 'koni']
KRENK = {'küp': '#3b82f6', 'küre': '#ef4444', 'silindir': '#22c55e', 'koni': '#f59e0b'}
KORNEK = {'küp': [('🎲', 'zar'), ('🧊', 'buz')], 'küre': [('⚽', 'top'), ('🍊', 'portakal')],
          'silindir': [('🥫', 'konserve'), ('🥁', 'davul')], 'koni': [('🍦', 'dondurma külahı'), ('🥕', 'havuç')]}
kutular = ''.join(f'<div class="kutu" style="margin:0;flex-direction:column;gap:8px;min-height:250px">{kati(c, 120, KRENK[c])}'
                  f'<div style="font-size:30px;font-weight:900;color:{KOYU}">{c.capitalize()}</div>'
                  f'<div style="display:flex;gap:20px">' + ''.join(kolon(emj(e, 50), etiket(a, 14)) for e, a in KORNEK[c]) + '</div></div>' for c in KATI)
k.sayfa(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px">{kutular}</div>'
        '<div class="not">Düz şekiller (kare, daire…) kâğıda çizilir; cisimler ise elle tutulur, dolu bir hacmi vardır. Gerçek bir top, zar ve konserve kutusunu ellerine verin; "Yuvarlanır mı? Üst üste konur mu?" diye deneyin.</div>',
        baslik='Elle tutulan şekiller', no=1, yonerge='Bu cisimlerin adını söyle. Evde benzerlerini bul.')
sat = []
nes = [('🏀', 'küre', 'küp'), ('🎁', 'küp', 'silindir'), ('🕯️', 'silindir', 'koni'), ('🍦', 'koni', 'küre')]
for i, (e, d, y) in enumerate(nes):
    assert d != y and any(e == x for x, _ in KORNEK[d]) or e in ('🏀', '🎁', '🕯️')
    sec = iki_secenek(d, y, i)
    sat.append(f'<div class="kutu" style="min-height:170px;margin:8px 0">{emj(e, 90)}<span style="font-size:36px;color:#cbd5e1">→</span>'
               f'{resim_sec([kolon(kati(c, 86, KRENK[c]), etiket(c, 17)) for c in sec])}</div>')
k.sayfa(''.join(sat), baslik='Hangi cisme benziyor?', no=1, yonerge='Nesne hangi cisme benziyor? <b>Daire içine al.</b>', alt_yonerge='Önce nesneyi eline alıp çevirin: yuvarlanıyor mu, düz yüzü var mı?')

# ================= 2) ÖRÜNTÜLER =================
KIR, MAV, SAR, YES = '#ef4444', '#3b82f6', '#facc15', '#22c55e'
ORN = {
    'AB': dict(renk=[('c', KIR), ('c', MAV)], sekil=[('s', 'daire', '#a855f7'), ('s', 'kare', '#f59e0b')], nesne=['🍎', '🍌'], rbos=[KIR, MAV]),
    'AAB': dict(renk=[('c', SAR), ('c', SAR), ('c', YES)], sekil=[('s', 'üçgen', '#22c55e'), ('s', 'üçgen', '#22c55e'), ('s', 'daire', '#ef4444')], nesne=['⭐', '⭐', '🌙'], rbos=[SAR, SAR, YES]),
    'ABB': dict(renk=[('c', MAV), ('c', KIR), ('c', KIR)], sekil=[('s', 'kare', '#3b82f6'), ('s', 'üçgen', '#f59e0b'), ('s', 'üçgen', '#f59e0b')], nesne=['🐟', '🦆', '🦆'], rbos=[MAV, KIR, KIR]),
    'ABC': dict(renk=[('c', KIR), ('c', SAR), ('c', MAV)], sekil=[('s', 'daire', '#ef4444'), ('s', 'kare', '#3b82f6'), ('s', 'üçgen', '#22c55e')], nesne=['🍎', '🍐', '🍊'], rbos=[KIR, SAR, MAV]),
}
for oi, (tur, o) in enumerate(ORN.items()):
    L = len(o['renk'])
    # renk: 2 tam tekrar göster, sonraki 1 tekrar boyanacak boş daire
    goster = oruntu(o['renk'], 2 * L) + [('bc',)] * L
    # sekil: 2 tekrar + boş kutular (çiz)
    gs = oruntu(o['sekil'], 2 * L) + [None] * L
    # nesne: sırada ne var
    n_g = 2 * L + 1 if L == 2 else 2 * L + 1
    d, y = siradaki(o['nesne'], n_g)
    assert d == o['nesne'][n_g % L]
    gn = oruntu(o['nesne'], n_g)
    renk_adlari = {KIR: 'kırmızı', MAV: 'mavi', SAR: 'sarı', YES: 'yeşil'}
    okunus = ', '.join(renk_adlari[c] for c in o['rbos'])
    g = f'''<div class="kutu" style="flex-direction:column;gap:10px;min-height:190px"><div style="font-size:19px;font-weight:800">🖍️ Boyayarak devam et</div>{oge_satir(goster, 58 if L == 2 else 50)}</div>
<div class="kutu" style="flex-direction:column;gap:10px;min-height:190px"><div style="font-size:19px;font-weight:800">✏️ Şekli çizerek devam et</div>{oge_satir(gs, 58 if L == 2 else 50)}</div>
<div class="kutu" style="flex-direction:column;gap:12px;min-height:210px"><div style="font-size:19px;font-weight:800">❓ Sırada ne var? Daire içine al.</div>
<div style="display:flex;align-items:center;gap:14px">{oge_satir(gn + ['❔'], 50, 6)}</div>{secenek(iki_secenek(d, y, oi), d, 56)}</div>
<div class="not">Örüntüyü yüksek sesle okuyun: "{okunus}, {okunus}…" Tekrar eden parçayı (birimi) parmakla çevreleyin.</div>'''
    k.sayfa(g, baslik=f'{"-".join(tur)} örüntüsü', no=2, yonerge=f'<b>{"-".join(tur)}</b> düzeni tekrar ediyor. Devam ettir.',
            oyun=OY_KUP if tur == 'ABC' else None)

# ses – hareket
SH = [(['👏', '🦶'], 'alkış, ayak'), (['👏', '👏', '🦶'], 'alkış, alkış, ayak'), (['🙌', '👏', '🦶'], 'eller yukarı, alkış, ayak')]
sat = []
for i, (b, ok_) in enumerate(SH):
    n_g = 2 * len(b) + (1 if i == 1 else 0)
    d, y = siradaki(b, n_g)
    sat.append(f'<div class="kutu" style="flex-direction:column;gap:10px;min-height:200px"><div style="font-size:17px;color:#475569;font-weight:700">Oku ve yap: {ok_}…</div>'
               f'{oge_satir(oruntu(b, n_g) + ["❔"], 52, 6)}{secenek(iki_secenek(d, y, i + 1), d, 54)}</div>')
k.sayfa(''.join(sat) + '<div class="not">Önce bedenle yapın: 👏 = el çırp, 🦶 = ayağını yere vur, 🙌 = ellerini kaldır. Ritmi birkaç kez tekrarlayın, sonra sıradakini seçsin.</div>',
        baslik='Ses ve hareket örüntüsü', no=2, yonerge='Örüntüyü <b>bedeninle</b> yap. Sırada ne var? Daire içine al.')

# sırada ne var (karışık)
SN = [['🚗', '🚗', '🚲'], [('s', 'kare', '#a855f7'), ('s', 'daire', '#facc15')], ['🌼', '🍁', '🍁'], [('c', YES), ('c', KIR), ('c', MAV)]]
sat = []
for i, b in enumerate(SN):
    n_g = 6 if len(b) == 3 else 5
    d, y = siradaki(b, n_g)
    sat.append(f'<div class="kutu" style="min-height:170px;margin:8px 0;justify-content:space-between">{oge_satir(oruntu(b, n_g) + ["❔"], 46, 5)}'
               f'<div style="display:flex;gap:16px">' + ''.join(f'<span class="secc" style="font-size:44px;display:inline-grid">{oge(x, 50)}</span>' for x in iki_secenek(d, y, i)) + '</div></div>')
k.sayfa(''.join(sat), baslik='Sırada ne var?', no=2, yonerge='Örüntüye bak. ❔ yerine ne gelir? <b>Daire içine al.</b>', alt_yonerge='Takılırsa örüntüyü baştan yüksek sesle okuyun.')

# kendi örüntün
bos_d = ''.join(oge(('bc',), 58) for _ in range(9))
bos_k = ''.join(f'<span style="display:inline-block;width:58px;height:58px;border:4px dashed #94a3b8;border-radius:10px"></span>' for _ in range(9))
g = f'''<div class="kutu" style="flex-direction:column;gap:10px;min-height:180px"><div style="font-size:19px;font-weight:800">2 renk seç: AB örüntüsü boya</div><div style="display:flex;gap:10px">{bos_d}</div></div>
<div class="kutu" style="flex-direction:column;gap:10px;min-height:180px"><div style="font-size:19px;font-weight:800">AAB ya da ABB örüntüsü boya</div><div style="display:flex;gap:10px">{bos_d}</div></div>
<div class="kutu" style="flex-direction:column;gap:10px;min-height:180px"><div style="font-size:19px;font-weight:800">Kutulara şekil çizerek kendi örüntünü yap</div><div style="display:flex;gap:10px">{bos_k}</div></div>
<div class="not">Çocuğun kurduğu örüntüyü ona okutun. Hatalıysa düzeltmek yerine "Hadi birlikte okuyalım" deyin; çoğu zaman hatayı kendisi fark eder.</div>'''
k.sayfa(g, baslik='Kendi örüntünü yap', no=2, yonerge='Sen bir örüntü kur ve boya!', alt_yonerge='Boncuk, lego ya da makarna ile önce masada kurabilirsiniz.')

# ================= 3) SINIFLAMA =================
# renge göre
renkler = [(KIR, 'kırmızı'), (MAV, 'mavi'), (SAR, 'sarı')]
adet = [4, 3, 5]
ogeler = [(c, R.choice(SEKILLER)) for (c, _), n in zip(renkler, adet) for _ in range(n)]
R.shuffle(ogeler)
assert len(ogeler) == sum(adet)
iz = '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;justify-items:center;align-items:center;padding:6px">' + ''.join(geo(s, 76, c, kalin=5) for c, s in ogeler) + '</div>'
sepet = ''.join(kolon(f'<div style="width:120px;height:84px;border:5px solid {c};border-top:none;border-radius:0 0 30px 30px;background:{c}22"></div>',
                      f'<div style="font-size:18px;font-weight:800;color:{c}">{a}</div>',
                      secenek(iki_secenek(sum(1 for cc, _ in ogeler if cc == c), yanlis_sayi(sum(1 for cc, _ in ogeler if cc == c), i), i), sum(1 for cc, _ in ogeler if cc == c), 38), gap=6)
                for i, (c, a) in enumerate(renkler))
for (c, _), n in zip(renkler, adet): assert sum(1 for cc, _ in ogeler if cc == c) == n
k.sayfa(f'<div class="kutu" style="display:block">{iz}</div><div class="kutu" style="min-height:260px">{sepet}</div>'
        '<div class="not">Her rengi kendi sepetine bir çizgiyle bağlayın ya da saydıkça işaretleyin. Gerçek oyuncakları renklerine göre kutulara ayırmak harika bir ön çalışmadır.</div>',
        baslik='Renge göre grupla', no=3, yonerge='Aynı renkleri grupla. Her sepette <b>kaç tane</b> olur? Daire içine al.', oyun=OY_MINIK)

# şekle göre
sk3 = ['daire', 'kare', 'üçgen']; adet = [3, 5, 4]
og2 = [(R.choice([KIR, MAV, SAR, YES]), s) for s, n in zip(sk3, adet) for _ in range(n)]
R.shuffle(og2)
iz = '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;justify-items:center;align-items:center;padding:6px">' + ''.join(geo(s, R.choice([64, 78]), c, kalin=5) for c, s in og2) + '</div>'
sepet = ''
for i, s in enumerate(sk3):
    n = sum(1 for _, ss in og2 if ss == s); assert n == adet[i]
    sepet += kolon(f'<div style="width:120px;height:84px;border:5px solid #475569;border-top:none;border-radius:0 0 30px 30px;display:grid;place-items:center">{geo(s, 46, "#fff", kalin=5)}</div>',
                   f'<div style="font-size:18px;font-weight:800">{s}</div>', secenek(iki_secenek(n, yanlis_sayi(n, i + 1), i + 1), n, 38), gap=6)
k.sayfa(f'<div class="kutu" style="display:block">{iz}</div><div class="kutu" style="min-height:260px">{sepet}</div>'
        '<div class="not">Renkler karışık ama biz yalnız <b>şekle</b> bakıyoruz. "Rengi farklı ama yine de üçgen mi?" diye sorun.</div>',
        baslik='Şekle göre grupla', no=3, yonerge='Renge değil, <b>şekle</b> bak. Her sepette kaç tane olur? Daire içine al.')

# büyüklüğe göre
sat = []
for i, (e, soru) in enumerate([('🐟', 'büyük'), ('🍓', 'küçük')]):
    boylar = [86, 44, 86, 44, 44, 86, 44] if i == 0 else [40, 80, 40, 80, 80, 40, 80]
    hedef_boy = max(boylar) if soru == 'büyük' else min(boylar)
    n = boylar.count(hedef_boy)
    sat.append(f'<div class="kutu" style="flex-direction:column;gap:14px;min-height:260px"><div style="display:flex;gap:16px;align-items:flex-end">' +
               ''.join(emj(e, b) for b in boylar) + f'</div><div style="display:flex;align-items:center;gap:24px"><div style="font-size:21px;font-weight:800">'
               f'<b style="color:#dc2626">{soru.capitalize()}</b> olanları daire içine al. Kaç tane?</div>{secenek(iki_secenek(n, yanlis_sayi(n, i), i), n, 44)}</div></div>')
k.sayfa(''.join(sat) + '<div class="not">Önce gerçek nesnelerle: büyük ve küçük kaşık, büyük ve küçük top… "Bu büyük, bu küçük" diyerek ayırın.</div>',
        baslik='Büyüklüğe göre grupla', no=3, yonerge='Büyükleri ve küçükleri ayır.')

# farklı olanı bul
def farkli_satir(ayni, farkli, i):
    ogs = [ayni] * 3; poz = (i * 3 + 1) % 4; ogs.insert(poz, farkli)
    assert sum(1 for x in ogs if x == farkli) == 1
    return f'<div class="kutu" style="min-height:150px;margin:8px 0">' + ''.join(f'<div style="padding:8px">{x}</div>' for x in ogs) + '</div>'
k.sayfa(farkli_satir(geo('daire', 96, KIR), geo('daire', 96, MAV), 0) + farkli_satir(geo('kare', 96, YES), geo('üçgen', 96, YES), 1) +
        farkli_satir(emj('🍎', 84), emj('🚗', 84), 2) + farkli_satir(emj('⭐', 90), emj('⭐', 46), 3),
        baslik='Farklı olanı bul', no=3, yonerge='Her satırda biri farklı. Onu <b>daire içine al.</b>', alt_yonerge='Sonra sorun: "Neden farklı?" (renk, şekil, tür, büyüklük)')

# gölge eşleme
es = ['🐰', '🍐', '🦋', '🚲']
sag = es[:]; R.shuffle(sag)
if sag == es: sag = sag[::-1]
assert sorted(sag) == sorted(es) and sag != es
rows = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;margin:16px 50px">{emj(a, 92)}'
               f'<span style="font-size:20px;color:#cbd5e1">● · · · · · · · ●</span>{emj(b, 92, "filter:brightness(0);opacity:.75")}</div>' for a, b in zip(es, sag))
k.sayfa(rows, baslik='Gölgesini bul', no=3, yonerge='Her resmi kendi <b>gölgesiyle</b> çizgiyle eşleştir.', alt_yonerge='Biçimine bak: kulaklar, kanatlar, tekerlekler…')

# ================= 4) KARŞILAŞTIRMA VE ÖLÇME =================
sat = []
for i, (e, soru) in enumerate([('🐘', 'büyük'), ('🌳', 'küçük'), ('🎈', 'büyük')]):
    boy = [120, 60] if i % 2 == 0 else [60, 120]
    assert boy[0] != boy[1]
    sat.append(f'<div class="kutu" style="min-height:220px;margin:10px 0"><div style="font-size:22px;font-weight:800;width:170px">Daha <b style="color:#dc2626">{soru}</b> olanı daire içine al.</div>'
               + ''.join(f'<div style="width:190px;display:grid;place-items:center">{emj(e, b)}</div>' for b in boy) + '</div>')
k.sayfa(''.join(sat), baslik='Büyük – küçük', no=4, yonerge='İki resmi karşılaştır.', alt_yonerge='"Büyük" ve "küçük" sözcüklerini elle de gösterin (kollar açık / avuç kapalı).')

# uzun-kısa + kalın-ince
def cubuk(uz, kal, renk, px_w=520):
    return f'<svg viewBox="0 0 {px_w} {kal+8}" width="{px_w}" height="{kal+8}"><rect x="4" y="4" width="{uz}" height="{kal}" rx="{min(kal, 30)/2}" fill="{renk}" stroke="#0f172a" stroke-width="3"/></svg>'
kutu = []
for i, (soru, a, b) in enumerate([('uzun', 470, 250), ('kısa', 300, 480)]):
    assert a != b
    kutu.append(f'<div class="kutu" style="flex-direction:column;gap:12px;min-height:180px;align-items:flex-start;padding-left:40px"><div style="font-size:21px;font-weight:800">Daha <b style="color:#dc2626">{soru}</b> kalemi daire içine al.</div>'
                f'<svg viewBox="0 0 {max(a, b)+8} 36" width="{max(a, b)+8}" height="36">{kalem(a, "#3b82f6")}</svg><svg viewBox="0 0 {max(a, b)+8} 36" width="{max(a, b)+8}" height="36">{kalem(b, "#22c55e")}</svg></div>')
for i, (soru, a, b) in enumerate([('kalın', 46, 14), ('ince', 12, 40)]):
    kutu.append(f'<div class="kutu" style="flex-direction:column;gap:14px;min-height:180px;align-items:flex-start;padding-left:40px"><div style="font-size:21px;font-weight:800">Daha <b style="color:#dc2626">{soru}</b> ipi daire içine al.</div>'
                f'{cubuk(420, a, "#f472b6" if i else "#a855f7")}{cubuk(420, b, "#f59e0b" if i else "#14b8a6")}</div>')
k.sayfa(''.join(kutu), baslik='Uzun – kısa · Kalın – ince', no=4, yonerge='Karşılaştır ve daire içine al.',
        alt_yonerge='Uzunluk karşılaştırırken uçları aynı çizgiden başlatın (sol kenar hizalı).')

# ağır-hafif
sat = []
for i, (sol, sag, agir, soru) in enumerate([('🍉', '🍓', 'sol', 'ağır'), ('🎈', '🧸', 'sag', 'hafif'), ('🐭', '🐘', 'sag', 'ağır')]):
    dogru = (sol if agir == 'sol' else sag) if soru == 'ağır' else (sag if agir == 'sol' else sol)
    yanlis = sag if dogru == sol else sol
    assert dogru != yanlis
    sat.append(f'<div class="kutu" style="min-height:240px;margin:8px 0">{terazi(sol, sag, agir, 300)}<div style="text-align:center">'
               f'<div style="font-size:21px;font-weight:800;margin-bottom:10px">Hangisi daha <b style="color:#dc2626">{soru}</b>?</div>{secenek(iki_secenek(dogru, yanlis, i), dogru, 54)}</div></div>')
k.sayfa(''.join(sat), baslik='Ağır – hafif', no=4, yonerge='Teraziye bak. Aşağı inen taraf <b>daha ağırdır</b>.',
        alt_yonerge='Ellerinizi terazi yapın: bir elde kitap, diğerinde kalem. Hangi el aşağı iniyor?')

# dolu-boş
g = f'''<div class="kutu" style="min-height:220px"><div style="font-size:21px;font-weight:800;width:200px"><b style="color:#dc2626">Dolu</b> bardağı daire içine al.</div>{bardak(0, 110)}{bardak(1, 110)}</div>
<div class="kutu" style="min-height:220px"><div style="font-size:21px;font-weight:800;width:200px"><b style="color:#dc2626">Boş</b> bardağı daire içine al.</div>{bardak(1, 110)}{bardak(0, 110)}</div>
<div class="kutu" style="min-height:220px"><div style="font-size:21px;font-weight:800;width:200px">Hangisinde <b style="color:#dc2626">daha çok</b> su var?</div>{bardak(.3, 110)}{bardak(.75, 110)}</div>
<div class="not">Mutfakta şeffaf iki bardakla deneyin: birini doldurun, birini boş bırakın. Sonra ikisine farklı miktarda su koyup karşılaştırın.</div>'''
k.sayfa(g, baslik='Dolu – boş', no=4, yonerge='Bardaklara bak ve daire içine al.')

# ölçme (standart olmayan birim)
sat = []
for i, (n, birim, renk) in enumerate([(5, 'ataç', '#3b82f6'), (3, 'ataç', '#ef4444'), (7, 'küp', '#22c55e')]):
    sat.append(f'<div class="kutu" style="flex-direction:column;gap:10px;min-height:205px;align-items:flex-start;padding-left:30px">{olcum(n, birim, renk)}'
               f'<div style="display:flex;align-items:center;gap:20px"><div style="font-size:20px;font-weight:800">Kalem kaç {birim} uzunluğunda?</div>{secenek(iki_secenek(n, yanlis_sayi(n, i), i), n, 42)}</div></div>')
k.sayfa(''.join(sat), baslik='Ataç ve küple ölç', no=4, yonerge='Kalemin altındaki ataçları / küpleri say.',
        alt_yonerge='Birimler arasında boşluk bırakmadan, kırmızı çizgiden başlayarak dizilir. Gerçek ataçlarla da ölçün.', oyun=OY_MATAKIS)

# sıralama
uz = R.sample([3, 4, 6, 8], 4)
renk4 = ['#ef4444', '#3b82f6', '#22c55e', '#f59e0b']
sirasi = sorted(range(4), key=lambda j: -uz[j])  # uzundan kısaya
assert len(set(uz)) == 4
kal = ''.join(f'<div style="display:flex;align-items:center;gap:16px;margin:12px 0"><svg viewBox="0 0 {8*U+8} 32" width="{8*U*0.9:.0f}" height="30">{kalem(u * U, renk4[j])}</svg>'
              f'<span style="margin-left:auto;display:inline-block;width:56px;height:56px;border:4px dashed #ea580c;border-radius:12px"></span></div>' for j, u in enumerate(uz))
kule_h = R.sample([2, 4, 6], 3)
kule = ''.join(kolon(f'<svg viewBox="0 0 60 {6*44+4}" width="60" height="{6*44+4}">' + ''.join(f'<rect x="4" y="{6*44 - (b+1)*44 + 4}" width="52" height="40" rx="5" fill="{renk4[(j+b)%4]}" stroke="#0f172a" stroke-width="3"/>' for b in range(h)) + '</svg>',
                     '<span style="display:inline-block;width:56px;height:56px;border:4px dashed #ea580c;border-radius:12px;margin-top:6px"></span>') for j, h in enumerate(kule_h))
for h in kule_h: assert h in (2, 4, 6)
k.sayfa(f'<div class="kutu" style="display:block;padding:14px 22px">{kal}</div><div class="kutu" style="min-height:360px;align-items:flex-end;justify-content:space-evenly">'
        f'<div style="font-size:20px;font-weight:800;align-self:center;width:180px">Kuleleri en uzundan en kısaya 1, 2, 3 diye numarala.</div>{kule}</div>',
        baslik='Uzundan kısaya sırala', no=4, yonerge='En uzun kaleme <b>1</b>, sonrakine <b>2</b>… yaz.', alt_yonerge='Takılırsa önce en uzunu, sonra en kısayı bulsun; ortadakileri sonra karşılaştırsın.')

# ================= 5) KONUM =================
def masa(kedi_ust):
    y = 52 if kedi_ust else 172
    return (f'<svg viewBox="0 0 240 200" width="230" height="192"><rect x="20" y="70" width="200" height="16" rx="4" fill="#a16207" stroke="#0f172a" stroke-width="3"/>'
            f'<rect x="36" y="86" width="14" height="108" fill="#a16207" stroke="#0f172a" stroke-width="3"/><rect x="190" y="86" width="14" height="108" fill="#a16207" stroke="#0f172a" stroke-width="3"/>'
            f'<text x="120" y="{y}" text-anchor="middle" font-size="54" style="{EMJ}">🐱</text></svg>')
def kutu_top(ic):
    tx = 95 if ic else 205
    return (f'<svg viewBox="0 0 240 200" width="230" height="192"><text x="{tx}" y="{150 if ic else 180}" text-anchor="middle" font-size="52" style="{EMJ}">⚽</text>'
            f'<path d="M30 70 L30 190 L160 190 L160 70" fill="#fde68a" fill-opacity=".55" stroke="#0f172a" stroke-width="4" stroke-linejoin="round"/>'
            f'<line x1="30" y1="70" x2="10" y2="50" stroke="#0f172a" stroke-width="4"/><line x1="160" y1="70" x2="180" y2="50" stroke="#0f172a" stroke-width="4"/></svg>')
kut = []
for i, ust in enumerate([True, False]):
    d = 'üstünde' if ust else 'altında'; sec = iki_secenek('üstünde', 'altında', i)
    kut.append(f'<div class="kutu" style="flex-direction:column;margin:0;gap:6px;min-height:340px">{masa(ust)}<div style="font-size:18px;font-weight:700">Kedi masanın…</div>{kelime_sec(sec, d, 22)}</div>')
for i, ic in enumerate([False, True]):
    d = 'içinde' if ic else 'dışında'; sec = iki_secenek('içinde', 'dışında', i + 1)
    kut.append(f'<div class="kutu" style="flex-direction:column;margin:0;gap:6px;min-height:340px">{kutu_top(ic)}<div style="font-size:18px;font-weight:700">Top kutunun…</div>{kelime_sec(sec, d, 22)}</div>')
k.sayfa(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px">{"".join(kut)}</div>',
        baslik='Üstünde – altında · İçinde – dışında', no=5, yonerge='Resme bak. Doğru sözcüğü <b>daire içine al.</b>',
        alt_yonerge='Okuyamayan çocuğa iki seçeneği siz okuyun; o göstersin.', oyun=OY_MINIK)

def agac_tavsan(onde):
    z = 3 if onde else 1
    return (f'<div style="position:relative;width:230px;height:190px"><span style="position:absolute;left:40px;top:0;font-size:150px;line-height:1;z-index:2;{EMJ}">🌳</span>'
            f'<span style="position:absolute;left:{120 if onde else 105}px;top:{100 if onde else 70}px;font-size:{72 if onde else 60}px;line-height:1;z-index:{z};{EMJ}">🐰</span></div>')
kut = []
for i, onde in enumerate([True, False]):
    d = 'önünde' if onde else 'arkasında'
    kut.append(f'<div class="kutu" style="min-height:230px;margin:10px 0">{agac_tavsan(onde)}<div style="text-align:center"><div style="font-size:20px;font-weight:700;margin-bottom:12px">Tavşan ağacın…</div>'
               f'{kelime_sec(iki_secenek("önünde", "arkasında", i), d, 24)}</div></div>')
yakin = (f'<div class="kutu" style="min-height:220px;margin:10px 0;flex-direction:column"><div style="font-size:20px;font-weight:800">Eve <b style="color:#dc2626">yakın</b> olan çocuğu daire içine al.</div>'
         f'<div style="display:flex;align-items:flex-end;width:100%;padding:0 20px">{emj("🏠", 110)}<span style="margin-left:30px">{emj("👧", 74)}</span><span style="margin-left:auto">{emj("👦", 74)}</span></div></div>')
k.sayfa(''.join(kut) + yakin, baslik='Önünde – arkasında · Yakın – uzak', no=5, yonerge='Resme bak ve doğru olanı <b>daire içine al.</b>',
        alt_yonerge='Önünde olan nesne, arkadakinin bir kısmını kapatır.')

# sağ-sol
sat = [f'<div class="kutu" style="min-height:190px;margin:8px 0"><div style="font-size:21px;font-weight:800;width:190px"><b style="color:#dc2626">Sağa</b> bakan oku daire içine al.</div>{oku("sol")}{oku("sag")}</div>']
for i, (dizi, merkez, yon) in enumerate([(['🐱', '⚽', '🐶'], '⚽', 'sağında'), (['🍎', '🧸', '🍌'], '🧸', 'solunda')]):
    m = dizi.index(merkez)
    d = dizi[m + 1] if yon == 'sağında' else dizi[m - 1]
    y = dizi[m - 1] if yon == 'sağında' else dizi[m + 1]
    assert d != y
    ad_m = {'⚽': 'Topun', '🧸': 'Ayıcığın'}[merkez]
    sat.append(f'<div class="kutu" style="flex-direction:column;gap:12px;min-height:220px;margin:8px 0"><div style="display:flex;gap:40px">' + ''.join(emj(x, 80) for x in dizi) +
               f'</div><div style="display:flex;align-items:center;gap:26px"><div style="font-size:21px;font-weight:800">{ad_m} <b style="color:#dc2626">{yon}</b> ne var?</div>{secenek(iki_secenek(d, y, i), d, 50)}</div></div>')
k.sayfa(''.join(sat), baslik='Sağında – solunda', no=5, yonerge='Sayfaya bakarken <b>sağ elin</b> hangi taraftaysa orası sağdır.',
        alt_yonerge='Sağ eline küçük bir çıkartma yapıştırın; her soruda o eli kaldırsın.', oyun=OY_KUP)

# ================= 6) ZAMAN =================
SIRA = [([('🥚', 'yumurta'), ('🐣', 'çatlıyor'), ('🐥', 'civciv')]), ([('🌱', 'filiz'), ('🌿', 'büyüyor'), ('🌻', 'çiçek')]),
        ([('🛏️', 'uyanıyor'), ('🪥', 'diş fırçalıyor'), ('🎒', 'okula gidiyor')])]
sat = []
for i, s in enumerate(SIRA):
    karisik = s[:]
    while karisik == s: R.shuffle(karisik)
    assert sorted(karisik) == sorted(s)
    sat.append('<div class="kutu" style="min-height:220px;margin:10px 0">' + ''.join(kolon(emj(e, 84), etiket(a, 15), '<span style="display:inline-block;width:56px;height:56px;border:4px dashed #ea580c;border-radius:12px;margin-top:6px"></span>') for e, a in karisik) + '</div>')
k.sayfa(''.join(sat), baslik='Önce – sonra', no=6, yonerge='Ne <b>önce</b> oldu? Kutulara 1, 2, 3 yaz.', alt_yonerge='"Önce… sonra… en son…" diye birlikte anlatın.')

zaman = [('🌅', 'Sabah', '🥣', 'kahvaltı'), ('☀️', 'Öğle', '🍲', 'öğle yemeği'), ('🌙', 'Akşam', '🛌', 'uyku')]
sag = zaman[:]
while sag == zaman: R.shuffle(sag)
rows = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;margin:10px 40px">{kolon(emj(a[0], 78), etiket(a[1], 18))}'
               f'<span style="font-size:20px;color:#cbd5e1">● · · · · · · ●</span>{kolon(emj(b[2], 78), etiket(b[3], 16))}</div>' for a, b in zip(zaman, sag))
g = f'''<div class="kutu" style="display:block;padding:8px">{rows}</div>
<div class="kutu" style="min-height:180px"><div style="font-size:21px;font-weight:800">Gece hangisi gökyüzünde görünür?</div>{secenek(iki_secenek('🌙', '☀️', 1), '🌙', 64)}</div>'''
k.sayfa(g, baslik='Sabah – öğle – akşam', no=6, yonerge='Her zamanı yapılan işle <b>çizgiyle</b> eşleştir.')

g = f'''<div class="kutu" style="min-height:260px;gap:10px">''' + ''.join(
    kolon(f'<div style="font-size:24px;font-weight:900;color:{c}">{t}</div>', f'<div style="width:170px;height:170px;border:4px {"solid" if t == "Bugün" else "dashed"} {c};border-radius:20px"></div>')
    + ('<span style="font-size:40px;color:#94a3b8">→</span>' if t != 'Yarın' else '') for t, c in [('Dün', '#64748b'), ('Bugün', MOR), ('Yarın', '#0891b2')]) + '</div>'
g += f'''<div class="kutu" style="min-height:160px"><div style="font-size:21px;font-weight:800"><b>Dün</b>, bugünden önce mi, sonra mı?</div>{kelime_sec(iki_secenek('önce', 'sonra', 0), 'önce', 28)}</div>
<div class="kutu" style="min-height:160px"><div style="font-size:21px;font-weight:800"><b>Yarın</b>, bugünden önce mi, sonra mı?</div>{kelime_sec(iki_secenek('sonra', 'önce', 0), 'sonra', 28)}</div>
<div class="not">Kutulara çizim yapabilir: dün ne yaptı, bugün ne yaptı, yarın ne yapacak? Takvimde günü işaretleyerek konuşun.</div>'''
k.sayfa(g, baslik='Dün – bugün – yarın', no=6, yonerge='<b>Bugün</b> yaptığın bir şeyi ortadaki kutuya çiz.')

# ================= 7) KARIŞIK TEKRAR =================
# tekrar 1
liste = ['üçgen', 'daire', 'üçgen', 'kare', 'üçgen', 'dikdörtgen', 'daire']
n_uc = liste.count('üçgen'); assert n_uc == 3
d, y = siradaki([('s', 'daire', KIR), ('s', 'daire', KIR), ('s', 'kare', MAV)], 5)
g = (f'<div class="kutu" style="flex-direction:column;gap:12px;min-height:210px"><div style="display:flex;gap:10px">' + ''.join(geo(s, 70, SRENK[s], kalin=5) for s in liste) +
     f'</div><div style="display:flex;align-items:center;gap:24px"><div style="font-size:20px;font-weight:800">Kaç üçgen var?</div>{secenek(iki_secenek(n_uc, 2, 0), n_uc, 44)}</div></div>'
     f'<div class="kutu" style="min-height:190px;justify-content:space-between">{oge_satir(oruntu([("s", "daire", KIR), ("s", "daire", KIR), ("s", "kare", MAV)], 5) + ["❔"], 50, 6)}'
     f'<div style="display:flex;gap:16px">' + ''.join(f'<span class="secc" style="font-size:44px;display:inline-grid">{oge(x, 50)}</span>' for x in iki_secenek(d, y, 1)) + '</div></div>'
     f'<div class="kutu" style="min-height:240px">{terazi("📚", "🪶", "sol", 280)}<div style="text-align:center"><div style="font-size:20px;font-weight:800;margin-bottom:10px">Hangisi daha <b style="color:#dc2626">hafif</b>?</div>{secenek(iki_secenek("🪶", "📚", 0), "🪶", 54)}</div></div>')
k.sayfa(g, baslik='Tekrar zamanı', no='★', yonerge='Her kutudaki soruyu çöz.', alt_yonerge='Bir kutu bitince mola verin; acele yok.')

# tekrar 2
d3 = 4
g = (f'<div class="kutu" style="flex-direction:column;gap:10px;min-height:200px;align-items:flex-start;padding-left:30px">{olcum(d3, "küp", "#a855f7")}'
     f'<div style="display:flex;align-items:center;gap:20px"><div style="font-size:20px;font-weight:800">Kalem kaç küp uzunluğunda?</div>{secenek(iki_secenek(d3, 5, 1), d3, 42)}</div></div>'
     f'<div class="kutu" style="min-height:200px">{kati("küre", 100, "#ef4444")}<span style="font-size:36px;color:#cbd5e1">→</span>{resim_sec([emj("🎲", 70), emj("🍊", 70)])}'
     f'<div style="font-size:16px;color:#475569;width:150px">Küreye benzeyeni daire içine al.</div></div>'
     f'<div class="kutu" style="min-height:220px">{masa(False)}<div style="text-align:center"><div style="font-size:20px;font-weight:700;margin-bottom:10px">Kedi masanın…</div>{kelime_sec(["üstünde", "altında"], "altında", 24)}</div></div>')
k.sayfa(g, baslik='Tekrar zamanı', no='★', yonerge='Her kutudaki soruyu çöz.', alt_yonerge='Doğru yaptığı her kutuya birlikte bir yıldız çizin.')

k.basardim('Şekilleri tanıyorum, örüntü kuruyorum,<br>karşılaştırıyor ve ölçüyorum!')
print('Kitap 4 sayfa:', k.pdf('/home/claude/mat/cikti/Tane_Tane_Matematik_4_Sekiller_Oruntuler.pdf'))
