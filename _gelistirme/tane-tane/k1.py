# -*- coding: utf-8 -*-
"""Kitap 1 · Sayılarla Tanışıyorum (1–5) — okul öncesi + özel gereksinim."""
import random
from lib import *

k = Kitap('k1', 'Sayılarla Tanışıyorum', "1'den 5'e kadar sayılar", '1. Kitap', 'Okul öncesi · 1. sınıf hazırlık · Özel eğitim')
R = random.Random(11)
OY_PARMAK = ("Sihirli Parmaklar · 1'den 10'a", 'sihirlii parmaklar.html')
OY_MATAKIS = ('MatAkış — Gör, Dokun, Oyna', 'matakis.html')
OY_MINIK = ('Minik Kâşifler', 'minik kasiflerr.html')

k.kapak("Saymayı, sayıları tanımayı ve yazmayı <b>adım adım</b> öğreten çalışma kitabı. Her sayı önce nesnelerle, sonra resimle, en son rakamla çalışılır.",
        '<div style="font-size:90px;font-weight:900;color:#16a34a;letter-spacing:10px">1 2 3 4 5</div>')

k.sayfa('''<div style="font-size:16px;line-height:1.6">
<p><b>Bu kitap nasıl çalışır?</b> Her sayı için aynı sırayı izleriz. Aynı düzen, özellikle özel gereksinimli çocuklarda ne yapacağını bilmeyi ve güveni kolaylaştırır.</p>
<table class="tbl"><tr><th>Sayfa</th><th>Ne yapıyoruz?</th><th>Sizin rolünüz</th></tr>
<tr><td>🌱 Tanışma</td><td>Sayıyı nesnelerle, nokta kartıyla ve çerçeveyle görür.</td><td>Önce gerçek nesnelerle (kalem, fasulye, lego) sayın. Sonra sayfaya geçin.</td></tr>
<tr><td>👆 Say ve seç</td><td>Nesneleri sayar, doğru sayıyı daire içine alır.</td><td>Parmakla dokunarak tek tek saymasını isteyin.</td></tr>
<tr><td>✏️ Rakam yaz</td><td>Rakamı izler, sonra kendisi yazar.</td><td>Kesikli çizgiyi baştan sona parmakla takip etmesini, sonra kalemle geçmesini isteyin.</td></tr>
<tr><td>🟥 Çerçeve</td><td>Beşlik çerçeveyi boyar, kaç tane olduğunu görür.</td><td>"Kaç kutu dolu, kaç kutu boş?" diye sorun.</td></tr>
<tr><td>🔗 Eşleştir</td><td>Nokta kartını rakamla eşleştirir.</td><td>Saymadan tanıyabiliyorsa övün.</td></tr></table>
<p style="margin-top:12px"><b>Somut → Resim → Sembol:</b> Çocuklar önce dokunarak, sonra resimle, en son rakamla öğrenir. Bu sıra, erken matematik öğretiminde araştırmalarla desteklenen bir yaklaşımdır. Bir sayfada zorlanırsa bir adım geri gidin (gerçek nesnelere dönün).</p>
<p><b>Özel gereksinimli çocuklar için:</b> Sayfayı ikiye katlayıp tek görev gösterebilirsiniz. Doğru cevabı önce siz gösterin, sonra birlikte, en son tek başına yapsın. Kısa ve sık çalışmak (günde 1–2 sayfa) uzun oturumlardan daha verimlidir.</p>
<p><b>Dijital destek:</b> Bazı sayfaların köşesindeki QR kod, sitedeki ilgili oyunu açar. Kitap ana çalışmadır; oyun pekiştirme içindir.</p></div>''',
        baslik='Aileler ve öğretmenler için', no='i')

ADLAR = ['', 'Bir', 'İki', 'Üç', 'Dört', 'Beş']
for n in range(1, 6):
    ad, em = NESNE[n * 3 % len(NESNE)]
    # 1) Tanışma
    g = f'''<div class="kutu" style="border-color:#bbf7d0;background:#f0fdf4"><div class="buyuk" style="color:#16a34a">{n}</div>
<div style="font-size:44px;font-weight:900;color:#14532d">{RAKAM_AD[n]}</div></div>
<div class="kutu">{nesneler(em, n, 70, duzen='zar')}<div style="font-size:26px;font-weight:800">{n} {ad}</div></div>
<div class="kutu">{nokta_karti(n, 150)}{cerceve(n, 5, 70, '#16a34a')}</div>
<div class="not">Birlikte sayın: her nesneye dokunarak "{', '.join(RAKAM_AD[1:n+1])}". Son söylenen sayı, kaç tane olduğunu gösterir.</div>'''
    k.sayfa(g, baslik=f'{ADLAR[n]} sayısıyla tanışalım', no=n, yonerge=f'Bu sayı <b style="color:#16a34a">{n}</b>. Nesneleri say, noktaları göster.', oyun=OY_PARMAK if n in (2, 4) else None)
    # 2) Say ve seç (iki seçenek)
    satirlar = []
    for j in range(3):
        m = n if j == 0 else R.randint(1, n)
        yanlis = m + 1 if m < 5 and (m == 1 or R.random() < .5) else m - 1
        ad2, em2 = NESNE[(n * 5 + j * 7) % len(NESNE)]
        satirlar.append(f'<div class="kutu">{nesneler(em2, m, 64, duzen="zar")}{secenek(iki_secenek(m, yanlis, j + n), m, 80)}</div>')
    k.sayfa(''.join(satirlar), baslik='Say ve daire içine al', no=n, yonerge='Kaç tane var? Doğru sayıyı <b>daire içine al</b>.', alt_yonerge='Parmağınla her birine dokunarak say.')
    # 3) Rakam yaz
    k.sayfa(rakam_izle(n, 330, '#16a34a', 6) + '<div class="yon" style="font-size:19px">Şimdi kendin yaz:</div>' + '<div class="cizgi"></div>' * 2 +
            f'<div style="margin-top:10px">{nesneler(em, n, 46)}</div>', baslik=f'{n} rakamını yazalım', no=n,
            yonerge=f'Kesikli çizginin üzerinden parmağınla, sonra kalemle geç.', alt_yonerge='Önce havada parmakla çiz, sonra kâğıda geç.')
    # 4) Çerçeve
    yan = n - 1 if n > 1 else 2
    g = f'''<div class="kutu" style="flex-direction:column"><div style="font-size:22px;font-weight:800">{n} tane yuvarlak boya</div>{cerceve(0, 5, 92, bos_isaret=True)}</div>
<div class="kutu"><div>{cerceve(n, 5, 72, '#16a34a')}</div>{secenek(iki_secenek(n, yan, n), n)}</div>
<div class="kutu"><div style="font-size:21px;font-weight:700">Kaç kutu boş kaldı?</div>{cerceve(n, 5, 60, '#16a34a', bos_isaret=False)}<div style="font-size:42px;font-weight:900;color:#94a3b8">{'⬜' if False else '___'}</div></div>'''
    k.sayfa(g, baslik='Beşlik çerçeve', no=n, yonerge='Çerçevede kaç tane var?', alt_yonerge='Beşlik çerçeve, sayıları 5 ile karşılaştırmayı kolaylaştırır.', oyun=OY_MATAKIS if n == 3 else None)
    # 5) Eşleştir (2'den itibaren)
    if n >= 2:
        sol = list(range(1, n + 1)) if n <= 4 else [1, 2, 3, 4, 5]
        sag = sol[:]; R.shuffle(sag)
        if sag == sol: sag = sag[::-1]
        satir = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;margin:10px 30px">{nokta_karti(a, 96, "#16a34a")}<span style="font-size:20px;color:#cbd5e1">● · · · · · ●</span><span style="font-size:72px;font-weight:900;width:110px;text-align:center">{b}</span></div>' for a, b in zip(sol, sag))
        k.sayfa(satir, baslik='Eşleştir', no=n, yonerge='Noktaları rakamla <b>çizgiyle</b> eşleştir.', alt_yonerge='Saymadan tanıyabiliyor musun? Sonra sayarak kontrol et.')

# Anında tanı
for t in range(2):
    sayilar = [R.randint(1, 5) for _ in range(6)]
    g = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:14px">' + ''.join(
        f'<div class="kutu" style="flex-direction:column;margin:0">{nokta_karti(v, 130, "#ef4444" if i % 2 else "#16a34a")}<div class="cizgi" style="width:90px;height:50px"></div></div>' for i, v in enumerate(sayilar)) + '</div>'
    k.sayfa(g + '<div class="not">Kartı 2 saniye gösterip kapatın, "Kaç tane gördün?" diye sorun. Saymadan küçük miktarları tanımak (anında tanıma) sayı hissini güçlendirir.</div>',
            baslik='Bir bakışta söyle!', no='★', yonerge='Noktalara bir bak, kaç tane? Altına yaz.', oyun=OY_MINIK)

# Çok mu az mı (iki grup)
for t in range(3):
    a = R.randint(1, 5); b = R.randint(1, 5)
    while b == a: b = R.randint(1, 5)
    ad1, em1 = NESNE[(t * 4 + 2) % len(NESNE)]; ad2, em2 = NESNE[(t * 4 + 9) % len(NESNE)]
    soru = 'çok' if t % 2 == 0 else 'az'
    g = f'''<div class="kutu" style="min-height:200px"><div style="text-align:center">{nesneler(em1, a, 52, duzen='zar')}<div class="secc" style="font-size:28px;margin-top:8px">A</div></div>
<div style="font-size:40px;color:#cbd5e1">|</div><div style="text-align:center">{nesneler(em2, b, 52, duzen='zar')}<div class="secc" style="font-size:28px;margin-top:8px">B</div></div></div>
<div class="kutu" style="flex-direction:column;gap:6px"><div style="font-size:20px;font-weight:700">Hangisi daha <b style="color:#dc2626">{soru}</b>? Harfini daire içine al.</div>
<div style="font-size:16px;color:#64748b">İpucu: Her {ad1} ile bir {ad2} arasında çizgi çek. Eşi olmayan hangi tarafta kaldı?</div></div>'''
    k.sayfa(g, baslik=f'Hangisi daha {soru}?', no='★', yonerge='İki grubu karşılaştır.')

# Sırayı tamamla
for t in range(2):
    bos = R.sample(range(1, 6), 2)
    kutular = ''.join(f'<span class="secc" style="font-size:64px;border-style:{"solid" if v not in bos else "dashed"};border-color:{"#16a34a" if v not in bos else "#ea580c"}">{v if v not in bos else "&nbsp;"}</span>' for v in range(1, 6))
    tren = ''.join(f'<span style="font-size:62px">{"🚂" if i == 0 else "🚃"}</span>' for i in range(6))
    k.sayfa(f'<div style="text-align:center;margin-top:16mm">{tren}</div><div class="sec" style="margin-top:8mm">{kutular}</div>'
            f'<div style="margin-top:14mm">{sayi_dogrusu(0, 5, bos=bos, w=640)}</div><div class="not">Sayıları sırayla yüksek sesle söyleyin. Boş vagona hangi sayı gelir?</div>',
            baslik='Sayı treni', no='★', yonerge='Eksik sayıları yaz.')

# Karışık tekrar
for t in range(3):
    satir = []
    for j in range(3):
        m = R.randint(1, 5); ad2, em2 = NESNE[R.randrange(len(NESNE))]
        satir.append(f'<div class="kutu">{nesneler(em2, m, 60)}<div class="cizgi" style="width:120px"></div>{nokta_karti(0, 1) if False else ""}</div>')
    k.sayfa(''.join(satir), baslik='Tekrar zamanı', no='★', yonerge='Say ve kaç tane olduğunu <b>yaz</b>.', alt_yonerge='Zorlanırsa rakamı birlikte söyleyin, o izlesin.')

k.basardim("1'den 5'e kadar sayıları tanıyorum, sayıyorum ve yazıyorum.")
print('Kitap 1 sayfa:', k.pdf('/home/claude/mat/cikti/Tane_Tane_Matematik_1_Sayilarla_Tanisiyorum.pdf'))
