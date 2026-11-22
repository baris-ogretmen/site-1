#!/usr/bin/env python3
"""setler.html (Barış Öğretmen Setleri) ve hece-hece-okuma-yazma.html sayfalarını üretir."""
from urllib.parse import quote
S = '/home/claude/site-1/'
DON = open('/tmp/don.txt', encoding='utf-8').read()
EPOSTA = 'barilkay466@gmail.com'
CSS = """:root{--bg:#fff8ef;--kart:#fff;--yazi:#1d3557;--soluk:#55657a;--cizgi:#f0e3d2}
*{box-sizing:border-box}body{margin:0;font-family:"Didact Gothic",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--yazi)}
a{color:inherit}header{position:relative;overflow:hidden;padding:24px 16px 30px;color:#fff;text-align:center;background:linear-gradient(135deg,#ea580c,#db2777 55%,#7c3aed)}
header.hh{background:linear-gradient(135deg,#2a9d8f,#3a86c8 60%,#8e6fc9)}
header:before{content:"";position:absolute;width:260px;height:260px;border-radius:50%;background:#ffffff22;left:-80px;top:-120px}
.geri{position:relative;color:#fff;text-decoration:none;font-weight:800;font-size:.95rem}
header h1{position:relative;margin:10px 0 6px;font-size:clamp(1.9rem,7vw,2.9rem)}header p{position:relative;max-width:680px;margin:0 auto;line-height:1.55;font-size:1.05rem}
.hap{display:inline-block;background:#ffffff26;border:1.5px solid #ffffff55;border-radius:999px;padding:5px 12px;font-weight:800;font-size:.86rem;margin:10px 3px 0}
main{max-width:1020px;margin:0 auto;padding:16px 16px 50px}h2{font-size:1.35rem;margin:28px 0 12px}
.izgara{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}
.kart{display:flex;flex-direction:column;background:var(--kart);border-radius:22px;overflow:hidden;border:1.5px solid var(--cizgi);box-shadow:0 14px 30px -24px #1d3557;text-decoration:none}
.kart img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#f1f5f9}
.kart .ic{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}.kart h3{margin:0;font-size:1.15rem}.kart p{margin:0;color:var(--soluk);line-height:1.5}
.yakin{display:grid;place-items:center;aspect-ratio:16/9;font-size:4rem;background:linear-gradient(135deg,#fde68a,#fbcfe8)}
.etik{display:flex;flex-wrap:wrap;gap:6px}.etik span{font-size:.76rem;font-weight:800;border-radius:999px;padding:3px 9px;background:#f1f5f9;color:#334155}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;border:0;border-radius:14px;padding:12px 16px;font-weight:800;font-size:1rem;text-decoration:none;color:#fff;background:#ea580c;margin-top:auto;cursor:pointer}
.btn.mavi{background:#2563eb}.btn.yesil{background:#16a34a}.btn.gri{background:#e2e8f0;color:#1d3557}
.iletisim{background:linear-gradient(135deg,#1d3557,#3a86c8);color:#fff;border-radius:22px;padding:20px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between}
.iletisim p{margin:4px 0 0;opacity:.9;line-height:1.5}.iletisim .btn{background:#ffd166;color:#1d3557;margin:0}
.liste{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.liste a{display:flex;gap:10px;align-items:center;background:var(--kart);border:1.5px solid var(--cizgi);border-radius:16px;padding:12px;text-decoration:none;font-weight:800}
.liste span{font-size:1.6rem}.liste small{display:block;font-weight:600;color:var(--soluk)}
.adim{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}.adim div{background:var(--kart);border-radius:18px;padding:14px;border:1.5px solid var(--cizgi);line-height:1.5}.adim b{display:block;margin-bottom:4px}
.harfler{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:12px}.harfler i{font-style:normal;width:40px;height:40px;border-radius:10px;display:grid;place-items:center;font-weight:800;font-size:1.4rem;background:#fff;color:#1d3557}
.not{background:#fff;border:1.5px dashed #f59e0b;border-radius:16px;padding:12px 14px;line-height:1.55;color:#7c2d12}
footer{text-align:center;color:var(--soluk);font-size:.9rem;padding:16px}"""
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Didact+Gothic&display=swap" rel="stylesheet">'


def sayfa(dosya, baslik, aciklama, gorsel, govde):
    html = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{baslik} — Barış Öğretmen</title><meta name="description" content="{aciklama}">
<link rel="canonical" href="https://baris-ogretmen.github.io/site-1/{dosya}">
<meta property="og:title" content="{baslik} — Barış Öğretmen"><meta property="og:description" content="{aciklama}">
<meta property="og:image" content="https://baris-ogretmen.github.io/site-1/{gorsel}"><meta name="theme-color" content="#ea580c">
{FONT}<style>{CSS}</style></head><body>
{govde}
<footer>© Barış Öğretmen · <a href="index.html">baris-ogretmen.github.io/site-1</a></footer>
{DON}
</body></html>'''
    open(S + dosya, 'w', encoding='utf-8').write(html)


ILETISIM = f'''<h2>✉️ Setin tamamı ve okullar için</h2>
<div class="iletisim"><div><b style="font-size:1.15rem">Setlerin tamamını isteyin</b><p>Sitede setlerin yalnızca örnek sayfaları var. Setin tamamı, okul ve kurum fiyatı için yazın.</p></div>
<a class="btn" href="mailto:{EPOSTA}?subject={quote('Barış Öğretmen Setleri hakkında')}">✉️ {EPOSTA}</a></div>'''

setler = f'''<header><a class="geri" href="index.html">← Barış Öğretmen ana sayfa</a>
<h1>📚 Barış Öğretmen Setleri</h1>
<p>Sınıfta ve evde kullanılan, yazdırılabilir, renkli çalışma setleri. Her set bir yöntemle, adım adım ilerler; sayfalardaki kare kodlar sitedeki dijital oyunlara götürür.</p>
<span class="hap">✏️ Yazdır, kalemle çalış</span><span class="hap">📱 Kare kodla tablette oyna</span><span class="hap">🏫 Okullar için</span></header>
<main>
<h2>Setler</h2>
<div class="izgara">
<a class="kart" href="hece-hece-okuma-yazma.html"><img src="gorseller/hece-hece-kapak-set.png" alt="Hece Hece Okuma–Yazma kapak" loading="lazy"><div class="ic"><h3>🔤 Hece Hece Okuma–Yazma</h3><p>Önce 8 ünlü, sonra hece hece okuma. 2 çalışma kitabı ve 19 resimli, nakaratlı hikâye.</p><div class="etik"><span>Okul öncesi sonu</span><span>1. sınıf</span><span>Özel eğitim</span></div><span class="btn">Örnek sayfaları gör</span></div></a>
<a class="kart" href="tane-tane-matematik.html"><img src="gorseller/tane-tane-kapak-set.png" alt="Tane Tane Matematik kapak" loading="lazy"><div class="ic"><h3>🧮 Tane Tane Matematik</h3><p>Sayılar, toplama-çıkarma, şekiller, örüntüler ve ölçme; önce nesne, sonra resim, en son rakam.</p><div class="etik"><span>Okul öncesi</span><span>1. sınıf</span><span>Özel eğitim</span></div><span class="btn yesil">Seti incele</span></div></a>
<div class="kart" id="bip-kart"><div class="yakin">🤖</div><div class="ic"><h3>🤖 Bip Bip Robotik</h3><p>Okul öncesinden 2. sınıfa kâğıt üstünde kodlama: yön, sıra, döngü, koşul, hata ayıklama ve kodla boyama.</p><div class="etik"><span>Okul öncesi</span><span>1. sınıf</span><span>2. sınıf</span></div><span class="btn gri">Çok yakında</span></div></div>
<div class="kart"><div class="yakin">♟️</div><div class="ic"><h3>♟️ Hamle Hamle Satranç</h3><p>Taşları tanıyarak başlayan, oyunla ilerleyen satranç çalışma seti.</p><div class="etik"><span>Okul öncesi</span><span>İlkokul</span></div><span class="btn gri">Hazırlanıyor</span></div></div>
</div>
{ILETISIM}
</main>'''
sayfa('setler.html', 'Barış Öğretmen Setleri', 'Okuma-yazma, matematik ve robotik-kodlama çalışma setleri: yazdırılabilir, renkli, kare kodla dijital oyunlara bağlı. Örnek sayfalar.', 'gorseller/hece-hece-kapak-set.png', setler)

CAL = [('🗺️', 'Harf Yolculuğu (ANETİL)', 'Harfleri tanı, yaz', 'anetill okuma yazma.html'), ('🕰️', 'Okuma Saati', 'Ses temelli okuma', 'anetil okuma saati.html'),
       ('✍️', 'Sihirli Parmaklar', 'Yazı atölyesi', 'sihirli-parmaklar.html'), ('⚽', 'Harf Topu', '7 oyunlu harf dünyası', 'harf topu.html'),
       ('🧩', 'Sihirli Heceler', 'Heceden kelime kur', 'hece-birlestirme.html'), ('🚂', 'Okuma Yazma Treni', 'Hece vagonları', 'okuma-yazma-v2.html'),
       ('📝', 'Mega Dikte Seti', '5 kelime oyunu', 'mega-dikte-seti.html'), ('🍂', 'Sonbahar Dikte', 'Dikte oyunu', 'sonbahar_dikte.html'),
       ('🦉', 'Akıllı Okuma Asistanı', 'Akıcı okuma', 'akilli-okuma.html'), ('🕵️', '5N1K Dedektifleri', 'Okuduğunu anlama', '5n1k-okuma.html'),
       ('🗣️', 'Konuşma Atölyesi', 'Ses, nefes, dil oyunları', 'konusma-atolyesi.html')]
liste = ''.join(f'<a href="{quote(y)}"><span>{e}</span><div>{a}<small>{k}</small></div></a>' for e, a, k, y in CAL)
harf = ''.join(f'<i>{h}</i>' for h in 'aeiouıöü')
hh = f'''<header class="hh"><a class="geri" href="setler.html">← Barış Öğretmen Setleri</a>
<h1>🔤 Hece Hece Okuma–Yazma</h1>
<p>Önce 8 ünlü, sonra her derste tek ünsüz: <b>la le li lo lu lı lö lü</b>. Her derste harf tanıtımı, Dinle ve bul, hece, kelime, cümle ve yazma; kahramanları Ela, Kaan, Nine ve kedi Lokum olan resimli hikâyeler.</p>
<div class="harfler">{harf}</div>
<span class="hap">📘 1. Kitap · 76 sayfa</span><span class="hap">📗 2. Kitap · 86 sayfa</span><span class="hap">📚 19 hikâye · 193 sayfa</span><span class="hap">📱 Her derste kare kod</span></header>
<main>
<h2>👀 Örnek sayfalar</h2>
<div class="izgara">
<a class="kart" href="okuma-yazma/Hece_Hece_Okuma_Yazma_ORNEK.pdf"><img src="gorseller/hece-hece-kapak-set.png" alt="Örnek sayfalar" loading="lazy"><div class="ic"><h3>Örnek sayfaları aç (PDF)</h3><p>Üç kitaptan seçilmiş 15 sayfa: ünlü dersi, ünsüz dersi, cümleler ve bir hikâyeden sahneler.</p><span class="btn mavi">📄 Örneği aç</span></div></a>
<div class="kart"><img src="gorseller/hece-hece-kapak-1_kitap.png" alt="1. Kitap" loading="lazy"><div class="ic"><h3>📘 1. Kitap · Ders 1–15</h3><p>8 ünlü (a e i o u ı ö ü), sonra l n k m t r y.</p></div></div>
<div class="kart"><img src="gorseller/hece-hece-kapak-2_kitap.png" alt="2. Kitap" loading="lazy"><div class="ic"><h3>📗 2. Kitap · Ders 16–29</h3><p>s d z b ç g ş p c h v f ğ j; her ders yalnızca öğrenilmiş harflerle.</p></div></div>
<div class="kart"><img src="gorseller/hece-hece-kapak-hikayeler.png" alt="Okuma Hikâyeleri" loading="lazy"><div class="ic"><h3>📚 Okuma Hikâyeleri</h3><p>19 resimli, nakaratlı hikâye; her biri o derse kadar öğrenilen harflerle. Sonda "Hadi konuşalım" soruları.</p></div></div>
</div>
<h2>🧭 Yöntem</h2>
<div class="adim">
<div><b>1. Önce 8 ünlü</b>Çocuk sesleri tanır, ağız şeklini görür, harfi yazar. Ünlüler her hecenin kalbidir.</div>
<div><b>2. Her derste tek ünsüz</b>Yeni ünsüz 8 ünlünün hepsiyle hece olur; çocuk heceyi kurmayı hemen öğrenir.</div>
<div><b>3. Benzerler arayla</b>i–ı, o–ö, u–ü, m–n, b–d–p, s–ş, c–ç, g–ğ art arda gelmez.</div>
<div><b>4. Okul yazısı</b>Kuyruksuz "a", dik temel harfe yakın, büyük ve yeşil noktalı yazma satırları.</div>
</div>
<h2>📱 Kare kodla açılan çalışmalar</h2>
<p style="color:var(--soluk);margin-top:-4px">Kitaptaki kare kodlar bu çalışmalara götürür; tablette ya da akıllı tahtada oynanır.</p>
<div class="liste">{liste}</div>
{ILETISIM}
</main>'''
sayfa('hece-hece-okuma-yazma.html', 'Hece Hece Okuma–Yazma', 'Önce 8 ünlü, sonra hece hece okuma: 2 çalışma kitabı ve 19 resimli hikâye. Okul öncesi sonu, 1. sınıf ve özel eğitim için. Örnek sayfalar.', 'gorseller/hece-hece-kapak-set.png', hh)
print('ok')
