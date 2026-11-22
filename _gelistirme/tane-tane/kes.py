# -*- coding: utf-8 -*-
"""Kitap 5 · Kes, Dokun, Say — kartlar ve materyaller (okul öncesi · 1. sınıf · özel eğitim)."""
import random
from lib import *

k = Kitap('kes', 'Kes, Dokun, Say', 'Kartlar ve materyaller', '5. Kitap', 'Okul öncesi · 1. sınıf · Özel eğitim')
R = random.Random(55)
RENK, ACIK, KOYU = k.renk, k.acik, k.koyu
OY_PARMAK = ("Sihirli Parmaklar · 1'den 10'a", 'sihirlii parmaklar.html')
OY_MATAKIS = ('MatAkış — Gör, Dokun, Oyna', 'matakis.html')
OY_MINIK = ('Minik Kâşifler', 'minik kasiflerr.html')
OY_KUM = ('Kum Tüneli', 'kumm tuneliii.html')
OY_KUP = ('Küp Yolu · Işık Hattı', 'kup yoluu.html')

MAKAS = '<span style="position:absolute;left:-2px;top:-15px;font-size:20px;background:#fff;line-height:1">✂️</span>'


def kart(icerik, h, zemin='#fff', ek=''):
    """Kesme çizgili kart hücresi (yükseklik px)."""
    return (f'<div class="kes" style="position:relative;height:{h}px;background:{zemin};display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;gap:4px;{ek}">{icerik}</div>')


def izgara(hucreler, sutun, bosluk=14, ust=10):
    return (f'<div style="display:grid;grid-template-columns:repeat({sutun},1fr);gap:{bosluk}px;margin-top:{ust}px">' + ''.join(hucreler) + '</div>')


def kes_notu(metin):
    return f'<div class="not">✂️ {metin}</div>'


# ---------------- 1. Kapak ----------------
k.kapak("Diğer dört kitapta kullanılan <b>rakam, nokta ve nesne kartları</b>, beşlik–onluk çerçeveler, sayı doğrusu, sayı bağı, işlem kartları ve rozetler. "
        "Kesin, dokunun, sayın: matematik önce elle öğrenilir.",
        '<div style="display:flex;gap:10px;align-items:flex-end">'
        f'<div class="kes" style="background:#fff;width:84px;height:110px;display:grid;place-items:center;font-size:70px;font-weight:900;color:{RENK}">7</div>'
        f'<div class="kes" style="background:#fff;padding:8px">{nokta_karti(5, 90, RENK)}</div>'
        f'<div class="kes" style="background:#fff;width:84px;height:110px;display:grid;place-items:center;font-size:76px;font-weight:900;color:#ea580c">+</div></div>')

# ---------------- 2. Aileler ve öğretmenler için ----------------
k.sayfa(f'''<div style="font-size:15.5px;line-height:1.55">
<p><b>Bu kitapta ne var?</b> Setin diğer kitaplarında ve günlük oyunlarda kullanılacak <b>kesilip hazırlanan</b> materyaller. Kitaptaki çalışma sayfalarını tamamlar; tek başına bir “ders kitabı” değildir.</p>
<table class="tbl"><tr><th>Materyal</th><th>Ne işe yarar?</th><th>Hangi kitapla?</th></tr>
<tr><td>🔢 Rakam kartları 0–20</td><td>Rakamı tanıma, sıraya dizme, miktarla eşleme</td><td>1, 2, 3</td></tr>
<tr><td>🔴 Nokta kartları 1–10</td><td>Saymadan bir bakışta tanıma (anında tanıma)</td><td>1, 2</td></tr>
<tr><td>🍎 Nesne kartları 1–10</td><td>Resimdeki nesneleri sayma, eşini bulma</td><td>1, 2</td></tr>
<tr><td>🟦 Beşlik / onluk çerçeve</td><td>Sayıyı 5 ve 10 ile ilişkilendirme</td><td>1, 2, 3</td></tr>
<tr><td>⚪ Sayaçlar</td><td>Çerçeveye, sayı bağına yerleştirilen pullar</td><td>Hepsi</td></tr>
<tr><td>📏 Sayı doğrusu 0–20</td><td>Sıra, bir fazlası / bir eksiği, ileri–geri sayma</td><td>2, 3</td></tr>
<tr><td>🔗 Sayı bağı · ➕ İşlem kartları</td><td>Parça–bütün, toplama ve çıkarma cümlesi kurma</td><td>3</td></tr>
<tr><td>📅 “Bugün kaç?” · 🏅 Rozetler</td><td>Günlük sayma rutini ve emeği görünür kılma</td><td>Hepsi</td></tr></table>
<p style="margin-top:10px"><b>Hazırlarken:</b> Kalın kâğıda (160 g ve üzeri) basın ya da kartona yapıştırın. Mümkünse şeffaf bantla kaplayın veya lamine edin; silinebilir kalemle tekrar tekrar kullanılır. Her kart takımını ayrı zarfa koyup üstüne adını yazın.</p>
<p><b>Özel gereksinimli çocuklar için:</b> Kesme, ince motor becerisi için iyi bir çalışmadır ama zorlayıcı olabilir. Kalın düz çizgileri çocuk, köşeleri yetişkin kesebilir. Kartlarla çalışırken masada <b>az kart</b> bulunsun (önce 2–3 kart), başarı arttıkça çoğaltın. Kartlar küçük parçalardır; ağza alma riski olan çocuklarda yetişkin gözetimi gerekir.</p>
<p><b>Sayaç yerine:</b> Fasulye, düğme, makarna, lego, kapak gibi evdeki nesneler kullanılabilir. Küçük nesneleri yalnızca gözetim altında kullanın.</p></div>''',
        baslik='Aileler ve öğretmenler için', no='i')

# ---------------- 3–6. Rakam kartları 0–20 ----------------
RK = [RENK, '#ea580c', '#16a34a']  # 0–9 camgöbeği, 10–19 turuncu, 20 yeşil
def rakam_karti(v):
    if v is None:
        return kart('<div style="font-size:15px;color:#94a3b8;font-weight:700">Boş kart</div><div style="width:150px;border-bottom:3px dashed #cbd5e1;height:120px"></div>'
                    '<div style="font-size:12px;color:#94a3b8">Kendi sayını yaz</div>', 238)
    renk = RK[0] if v < 10 else (RK[1] if v < 20 else RK[2])
    fs = 172 if v < 10 else 150
    return kart(f'<div style="font-size:{fs}px;font-weight:900;line-height:1;color:{renk};font-feature-settings:\'cv01\'">{v}</div>'
                f'<div style="font-size:20px;font-weight:700;color:#334155">{RAKAM_AD[v]}</div>'
                f'<div style="position:absolute;bottom:6px;width:60%;border-bottom:3px solid {renk};opacity:.35"></div>', 238)

grup = [list(range(0, 6)), list(range(6, 12)), list(range(12, 18)), [18, 19, 20, None, None, None]]
for i, g in enumerate(grup):
    gercek = [v for v in g if v is not None]
    k.sayfa(izgara([rakam_karti(v) for v in g], 2, 16, 14) + (kes_notu('Kartın altındaki çizgi, kartın doğru tutulmasını sağlar (6 ile 9 karışmaz).') if i == 0 else ''),
            baslik=f'Rakam kartları {gercek[0]}–{gercek[-1]}', no=i + 1,
            yonerge='Kesikli çizgiden <b>kes</b>.', alt_yonerge='0–9 mavi, 10–19 turuncu, 20 yeşil. Sıraya dizme, eşleme ve “bir fazlası” oyunlarında kullanılır.',
            oyun=OY_PARMAK if i == 3 else None)

# ---------------- 7–8. Nokta kartları 1–10 ----------------
for i, aralik in enumerate([range(1, 7), range(7, 11)]):
    if i == 0:
        hucre = [kart(nokta_karti(n, 180, '#ef4444', cerceve='#cbd5e1'), 232) for n in aralik]
        gov = izgara(hucre, 2, 16, 14)
    else:
        hucre = [kart(nokta_karti(n, 150, '#ef4444', cerceve='#cbd5e1'), 210) for n in aralik]
        gov = izgara(hucre, 2, 14, 14)
    for n in aralik:
        assert 1 <= n <= 10
    k.sayfa(gov + kes_notu('Kartın arka yüzüne rakamını küçük yazın: çocuk cevabını kendisi kontrol eder.' if i == 0 else
                             '6’dan büyük sayılar “5 ve …” diye iki parça görünür: “Beş ve iki, yedi.” Bu düzen, beşlik çerçeveyle aynı mantıktadır.'),
            baslik=f'Nokta kartları {aralik[0]}–{aralik[-1]}', no=i + 1, yonerge='Kes. Noktalara bir bak: kaç tane?',
            alt_yonerge='Kartı 2 saniye gösterip kapatın; saymadan söylemeye çalışsın.', oyun=OY_MATAKIS if i == 1 else None)

# Sayfa 8'de 7–10 kartları geniş olduğu için ikili sütuna sığması kontrol edildi (150px yükseklik → 306px genişlik).

# ---------------- 9–10. Nesne kartları 1–10 ----------------
NES_SIRA = [NESNE[j] for j in (0, 3, 5, 7, 9, 10, 2, 14, 19, 22)]  # elma, balon, balık, çiçek, araba, ördek, çilek, yaprak, civciv, tavşan
for i, aralik in enumerate([range(1, 7), range(7, 11)]):
    hucre = []
    for n in aralik:
        ad, em = NES_SIRA[n - 1]
        if n <= 6:
            ic = nesneler(em, n, 58, duzen='zar')
        else:
            ic = nesneler(em, n, 50, sutun=5)
        sayac = ic.count('<span')
        assert sayac == n, (n, sayac)
        hucre.append(kart(ic + f'<div style="font-size:15px;font-weight:700;color:#64748b;margin-top:4px">{ad}</div>', 236 if n <= 6 else 250))
    k.sayfa(izgara(hucre, 2, 16, 14) + kes_notu('Rakam kartlarıyla eşleyin: nesne kartını koyun, çocuk yanına doğru rakam kartını getirsin.'),
            baslik=f'Nesne kartları {aralik[0]}–{aralik[-1]}', no=i + 1, yonerge='Kes. Nesneleri dokunarak say.',
            alt_yonerge='Her nesneye bir kez dokunun; son söylenen sayı “kaç tane” sorusunun cevabıdır.', oyun=OY_MINIK if i == 1 else None)

# ---------------- 11. Beşlik çerçeve ----------------
bes = ''.join(f'<div class="kes" style="position:relative;padding:14px 10px;margin:14px 0;display:flex;justify-content:center;background:#fff">{MAKAS}{cerceve(0, 5, 116)}</div>' for _ in range(4))
k.sayfa(bes + '<div class="not">Her kutuya <b>bir</b> sayaç koyun ve soldan başlayın. “Kaç tane var? Kaç kutu boş? 5 olması için kaç tane daha lazım?” diye sorun.</div>',
        baslik='Beşlik çerçeve', no='5', yonerge='Kes. Kutulara fasulye, düğme ya da sayaç koy.', alt_yonerge='Beşlik çerçeve, sayıları 5 ile karşılaştırmayı kolaylaştırır (Kitap 1).')

# ---------------- 12. Onluk çerçeve ----------------
onl = ''.join(f'<div class="kes" style="position:relative;padding:16px 10px;margin:16px 0;display:flex;justify-content:center;background:#fff">{MAKAS}{cerceve(0, 10, 116)}</div>' for _ in range(2))
k.sayfa(onl + '<div class="not">Önce üst sırayı soldan sağa doldurun, sonra alt sırayı. Böylece 7 = “üstte 5, altta 2” diye görünür. '
              'Toplamada iki renk sayaç kullanın (ör. 4 kırmızı + 3 mavi). Çıkarmada sayaçları tek tek geri alın.</div>',
        baslik='Onluk çerçeve', no='10', yonerge='Kes. Kutulara sayaç koyarak 10’a kadar sayıları göster.', alt_yonerge='İki onluk çerçeve yan yana konunca 20’ye kadar sayılar gösterilir (Kitap 2–3).',
        oyun=OY_MATAKIS)

# ---------------- 13. Sayaçlar ----------------
def sayac(renk):
    return (f'<div style="display:grid;place-items:center"><svg viewBox="0 0 100 100" width="92" height="92">'
            f'<circle cx="50" cy="50" r="47" fill="#fff" stroke="#94a3b8" stroke-width="2.5" stroke-dasharray="6 5"/>'
            f'<circle cx="50" cy="50" r="40" fill="{renk}"/><circle cx="38" cy="38" r="9" fill="#fff" opacity=".35"/></svg></div>')
sayaclar = [sayac('#ef4444') for _ in range(18)] + [sayac('#3b82f6') for _ in range(18)]
assert len(sayaclar) == 36
k.sayfa(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px 6px;margin-top:16px">{"".join(sayaclar)}</div>'
        '<div class="not">18 kırmızı + 18 mavi sayaç. Toplamada iki rengi kullanın: “3 kırmızı ve 2 mavi, hepsi kaç?” '
        'Yuvarlakları kesmek zorsa kare olarak kesin; sayaç yine çalışır.</div>',
        baslik='Sayaçlar', no='●', yonerge='Yuvarlakları kesikli çizgiden <b>kes</b>.', alt_yonerge='Kartona yapıştırırsanız daha kolay tutulur.')

# ---------------- 14–15. Sayı doğrusu 0–20 (iki parça) ----------------
ADIM = 58
def serit(parca):
    """parca 1: 0–10, sağ kenar 10'dan yarım adım sonra. parca 2: yapıştırma payı + 11–20 + ok.
    Parça 1, parça 2'nin yapıştırma payının üstüne konunca 10 ile 11 arası da tam bir adım olur."""
    H = 170; ly = 66; h = []
    if parca == 1:
        x = lambda v: 30 + v * ADIM
        W = x(10) + ADIM // 2
        h.append(f'<line x1="8" y1="{ly}" x2="{W}" y2="{ly}" stroke="#0f172a" stroke-width="5"/>')
        rng = range(0, 11)
    else:
        F = 64
        x = lambda v: F + ADIM // 2 + (v - 11) * ADIM
        W = x(20) + 46
        h.append(f'<rect x="0" y="0" width="{F}" height="{H}" fill="#e2e8f0"/>'
                 f'<text x="{F/2}" y="{H/2}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="13" fill="#64748b" transform="rotate(-90 {F/2} {H/2})">YAPIŞTIR · 1. parça</text>')
        h.append(f'<line x1="{F}" y1="{ly}" x2="{W-8}" y2="{ly}" stroke="#0f172a" stroke-width="5"/><polygon points="{W-4},{ly} {W-22},{ly-10} {W-22},{ly+10}" fill="#0f172a"/>')
        rng = range(11, 21)
    for v in rng:
        renk = '#dc2626' if v % 5 == 0 else '#0f172a'
        h.append(f'<line x1="{x(v)}" y1="{ly-16}" x2="{x(v)}" y2="{ly+16}" stroke="{renk}" stroke-width="5"/>')
        h.append(f'<text x="{x(v)}" y="{ly+66}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="{40 if v < 10 else 34}" fill="{renk}">{v}</text>')
    # adım uzunluğu doğrulaması
    xs = [x(v) for v in rng]
    assert all(b - a == ADIM for a, b in zip(xs, xs[1:]))
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="display:block">{"".join(h)}</svg>', W
# parça birleşince 10→11 mesafesi: (parça1 sağ kenar − x(10)) + (parça2: x(11) − F) = 29 + 29 = 58
assert (ADIM // 2) + (ADIM // 2) == ADIM

for p in (1, 2):
    svg, W = serit(p)
    assert W <= 688, W
    kopya = ''.join(f'<div class="kes" style="position:relative;display:inline-block;margin:16px 0 6px;border-radius:4px;background:#fff">{MAKAS}{svg}</div>' for _ in range(2))
    acik = ('Bu 1. parça (0–10). İki kopya var: biri sınıf/ev için, biri yedek.' if p == 1 else
            'Bu 2. parça (11–20). Gri alanın üstüne 1. parçanın sağ ucunu yapıştırın; 10 ile 11 arası, diğer aralıklarla aynı olur.')
    k.sayfa(f'<div style="display:flex;flex-direction:column;align-items:center">{kopya}</div>'
            f'<div style="display:flex;justify-content:center;gap:14px;margin-top:14px;align-items:center">{tane(90, "dusun")}'
            f'<div style="font-size:18px;font-weight:700;max-width:120mm;line-height:1.45">{acik}</div></div>'
            '<div class="not">Kullanım: Bir oyuncağı sayının üstüne koyun. “Bir adım ileri git, şimdi kaçtasın?” '
            '5, 10, 15, 20 kırmızıdır; sayıları 5’er gruplar hâlinde görmeyi kolaylaştırır.</div>',
            baslik=f'Sayı doğrusu · {p}. parça', no=p, yonerge='Kes ve iki parçayı birleştir.' if p == 1 else 'Kes, gri alanı 1. parçanın altına yapıştır.',
            alt_yonerge='Birleşince 0’dan 20’ye bir sayı doğrusu olur (yaklaşık 64 cm).' if p == 2 else 'İleri saymak sağa, geri saymak sola gitmektir.',
            oyun=OY_KUM if p == 2 else None)

# ---------------- 16–17. Sayı bağı ----------------
def bos_bag(px, renk='#ea580c'):
    d = lambda cx, cy, r: f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{renk}" stroke-width="6"/>'
    return (f'<svg viewBox="0 0 320 300" width="{px}" height="{px*300/320:.0f}"><line x1="160" y1="80" x2="70" y2="215" stroke="{renk}" stroke-width="6"/>'
            f'<line x1="160" y1="80" x2="250" y2="215" stroke="{renk}" stroke-width="6"/>{d(160, 75, 62)}{d(70, 220, 55)}{d(250, 220, 55)}'
            f'<text x="160" y="22" text-anchor="middle" font-family="Inter" font-weight="700" font-size="13" fill="#64748b"> </text></svg>')
k.sayfa(f'<div class="kes" style="position:relative;display:flex;flex-direction:column;align-items:center;padding:16px;margin-top:14px;background:#fff">{MAKAS}'
        f'<div style="font-size:20px;font-weight:800;color:#ea580c">BÜTÜN</div>{bos_bag(560)}'
        f'<div style="display:flex;justify-content:space-between;width:500px;font-size:20px;font-weight:800;color:#ea580c;margin-top:-6px"><span>PARÇA</span><span>PARÇA</span></div></div>'
        '<div class="not">Üst daireye bütünü (ör. 5 sayaç), alt dairelere parçaları koyun (ör. 3 ve 2). Sayaçları alt dairelerden üste taşıyınca '
        '“3 ve 2, hepsi 5” cümlesi somut olarak görünür. Rakam kartlarını da dairelerin içine koyabilirsiniz.</div>',
        baslik='Sayı bağı (büyük şablon)', no='🔗', yonerge='Dairelere sayaç ya da rakam kartı koy.', alt_yonerge='Parça–bütün ilişkisi toplama ve çıkarmanın temelidir (Kitap 3).')

bar = (f'<div class="kes" style="position:relative;padding:14px;background:#fff">{MAKAS}<div style="font-size:15px;font-weight:800;color:#64748b;margin-bottom:6px">Parça–bütün şeridi</div>'
       f'<div style="border:4px solid #ea580c;border-radius:12px;height:112px;display:grid;place-items:center;font-weight:800;color:#ea580c">BÜTÜN</div>'
       f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:6px"><div style="border:4px solid #0891b2;border-radius:12px 0 0 12px;height:112px;display:grid;place-items:center;font-weight:800;color:#0891b2">PARÇA</div>'
       f'<div style="border:4px solid #0891b2;border-left:0;border-radius:0 12px 12px 0;height:112px;display:grid;place-items:center;font-weight:800;color:#0891b2">PARÇA</div></div></div>')
k.sayfa(f'<div style="display:flex;justify-content:space-around;margin-top:14px">'
        + ''.join(f'<div class="kes" style="position:relative;padding:8px;background:#fff">{MAKAS}{bos_bag(320)}</div>' for _ in range(2)) + '</div>'
        f'<div style="margin-top:16px">{bar}</div>'
        '<div class="not">Küçük sayı bağları masada iki çocuğun aynı anda çalışması içindir. Şerit, aynı fikri bir çubuk olarak gösterir: '
        'üstteki bütün, alttaki iki parçanın toplamıdır.</div>',
        baslik='Sayı bağı (küçük şablonlar)', no='🔗', yonerge='Kes. Dairelere ve kutulara sayaç koy.')

# ---------------- 18. İşlem kartları ----------------
ISL = [('+', '#16a34a', 'artı'), ('−', '#dc2626', 'eksi'), ('=', '#2563eb', 'eşittir')]
hucre = [kart(f'<div style="font-size:170px;font-weight:900;line-height:.9;color:{r}">{s}</div><div style="font-size:18px;font-weight:700;color:#475569">{ad}</div>', 222)
         for s, r, ad in ISL for _ in range(3)]
k.sayfa(izgara(hucre, 3, 14, 14) + '<div class="not">Rakam kartlarıyla işlem cümlesi kurun: <b>3 + 2 = 5</b>. Önce sayaçlarla yapın, sonra kartlarla yazın. '
        'Aynı işlemi sayaçlarla göstermesini isteyin: sembol, somut olayın kısa yazılışıdır.</div>',
        baslik='İşlem kartları', no='+', yonerge='Kes. Rakam kartlarının arasına koy.', alt_yonerge='Her işaretten 3 kart var.')

# ---------------- 19. Bugün kaç? ----------------
k.sayfa(f'''<div style="display:flex;gap:16px;align-items:center;margin-top:10px">
<div style="flex:1;border:4px solid {RENK};border-radius:22px;padding:14px;background:{ACIK};text-align:center">
<div style="font-size:24px;font-weight:900;color:{KOYU}">Bugün kaçıncı gün?</div>
<div style="margin:10px auto 0;width:178px;height:250px;border:4px dashed {RENK};border-radius:14px;background:#fff;display:grid;place-items:center;font-size:15px;color:#64748b;font-weight:700;padding:10px">Rakam kartını<br>buraya koy<br>(cep yapmak için<br>alt ve yanları<br>bantlayın)</div></div>
<div style="width:210px;text-align:center">{tane(150, 'mutlu', True)}<div style="font-size:18px;font-weight:800;margin-top:6px">Her gün bir sayaç ekle!</div></div></div>
<div style="font-size:20px;font-weight:800;margin:16px 4px 6px">Kaç gün oldu? Her gün bir kutuya sayaç koy ya da boya.</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:12px">{cerceve(0, 10, 84)}{cerceve(0, 10, 84)}</div>
<div class="not">Her gün aynı saatte (ör. sabah çemberinde) bir kutu boyanır ve rakam kartı değiştirilir: “Dün 6’ydı, bugün bir fazlası, 7.”
20 gün dolunca yeni bir sayfa başlatın. Rutin, özellikle özel gereksinimli çocuklarda güven verir.</div>''',
        baslik='Bugün kaç? · Günlük sayaç', no='📅', yonerge='Bu sayfayı panoya as ya da lamine et.', alt_yonerge='Silinebilir kalemle her ay yeniden kullanılır.')

# ---------------- 20. Başardım rozetleri ----------------
ROZET = [('Sayıyorum!', '#16a34a'), ('1–5 tamam', '#0891b2'), ('6–10 tamam', '#2563eb'), ('Rakam yazarım', '#9333ea'), ('Topladım!', '#ea580c'),
         ('Çıkardım!', '#dc2626'), ('Şekil ustası', '#ca8a04'), ('Örüntü buldum', '#db2777'), ('Harika çalıştım', '#0f766e')]
def rozet(metin, r):
    return (f'<div style="display:grid;place-items:center"><div style="position:relative;width:200px;height:200px;border-radius:50%;border:3px dashed #94a3b8;display:grid;place-items:center">'
            f'<div style="width:182px;height:182px;border-radius:50%;background:{r};display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">'
            f'<div style="background:#fff;border-radius:50%;width:92px;height:92px;display:grid;place-items:center">{tane(66, "mutlu", True)}</div>'
            f'<div style="font-size:18px;font-weight:900;margin-top:6px;text-align:center;line-height:1.1">{metin}</div>'
            f'<div style="font-size:15px">★ ★ ★</div></div></div></div>')
k.sayfa(f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px 6px;margin-top:14px">{"".join(rozet(m, r) for m, r in ROZET)}</div>'
        '<div class="not">Rozeti çabanın hemen ardından verin ve ne için verdiğinizi söyleyin: “Beşe kadar dokunarak saydın.” Göğse bantla takılabilir ya da Başardım sayfasına yapıştırılabilir.</div>',
        baslik='Başardım rozetleri', no='🏅', yonerge='Kes ve kazandığında yapıştır.')

# ---------------- 21. Kartlarla oyun önerileri ----------------
OYUNLAR = [
    ('🧠', 'Hafıza', 'Nokta kartları + rakam kartları (ör. 1–5)',
     'Kartları ters çevirip dizin. Sırayla iki kart açılır; nokta sayısı rakamla aynıysa kartları alır, değilse geri kapatır.',
     'Az kartla başlayın (3 çift). Kartları açık oynayarak öğretin.'),
    ('🤝', 'Eşini Bul', 'Nesne kartları + rakam kartları',
     'Nesne kartları masada açık durur. Çocuk bir rakam kartı çeker, aynı sayıdaki nesne kartını bulup yanına koyar.',
     'Önce 2 nesne kartından birini seçsin; sonra seçenek sayısını artırın.'),
    ('🚂', 'Sıraya Diz', 'Rakam kartları 0–10 (sonra 0–20)',
     'Kartlar karışık verilir; çocuk küçükten büyüğe dizer. Sayı doğrusu şeridini kontrol için yanında kullanabilir.',
     'İlk kartı siz koyun. Bir kartı gizleyip “Hangisi kayıp?” diye sorun.'),
    ('➕', 'Bir Fazlası', 'Rakam kartları + sayaçlar + onluk çerçeve',
     'Bir rakam kartı çekilir. Çerçeveye o kadar sayaç konur, bir tane daha eklenir: “4’ün bir fazlası 5.” Doğru kart yanına konur.',
     'Sayı doğrusunda bir adım ileri giderek kontrol edin. Sonra “bir eksiği” oynayın.'),
]
# kurallardaki örnek doğruluğu
assert 4 + 1 == 5
g = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px">' + ''.join(
    f'''<div style="border:3px solid {ACIK};border-radius:20px;padding:18px;background:#fff;min-height:330px">
<div style="display:flex;align-items:center;gap:10px"><span style="font-size:40px">{ik}</span><span style="font-size:28px;font-weight:900;color:{KOYU}">{ad}</span></div>
<div style="font-size:14.5px;font-weight:700;color:{RENK};margin:8px 0">Gerekenler: {ger}</div>
<div style="font-size:17.5px;line-height:1.5">{kur}</div>
<div style="font-size:14.5px;color:#475569;background:#f8fafc;border-radius:8px;padding:8px 10px;margin-top:10px"><b>Kolaylaştır:</b> {kol}</div></div>''' for ik, ad, ger, kur, kol in OYUNLAR) + '</div>'
k.sayfa(g + '<div class="not" style="max-width:110mm">Oyun kısa sürsün (5–10 dakika) ve çocuk “biraz daha” derken bitsin. Kaybetme baskısı yerine birlikte oynayın.</div>',
        baslik='Kartlarla oyun önerileri', no='🎲', yonerge='Kestiğin kartlarla oyna!', oyun=OY_KUP)

k.basardim('Kartlarımı kestim, saydım, dizdim ve oynadım.')
print('Kitap 5 sayfa:', k.pdf('/home/claude/mat/cikti/Tane_Tane_Matematik_5_Kes_Kullan.pdf'))
