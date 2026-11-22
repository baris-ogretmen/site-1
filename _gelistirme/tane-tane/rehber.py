# -*- coding: utf-8 -*-
"""Rehber · Öğretmen ve Veli Rehberi — Tane Tane Matematik setini en iyi nasıl kullanırım?"""
from lib import *

k = Kitap('reh', 'Öğretmen ve Veli Rehberi', 'Seti en iyi nasıl kullanırım?', 'Rehber', 'Okul öncesi · 1. sınıf · Özel eğitim')
RENK, ACIK, KOYU = k.renk, k.acik, k.koyu
OY = {
    'parmak': ("Sihirli Parmaklar · 1'den 10'a", 'sihirlii parmaklar.html'),
    'matakis': ('MatAkış — Gör, Dokun, Oyna', 'matakis.html'),
    'minik': ('Minik Kâşifler', 'minik kasiflerr.html'),
    'kum': ('Kum Tüneli', 'kumm tuneliii.html'),
    'kup': ('Küp Yolu · Işık Hattı', 'kup yoluu.html'),
}
KITAP_RENK = {1: TEMA['k1'][0], 2: TEMA['k2'][0], 3: TEMA['k3'][0], 4: TEMA['k4'][0], 5: TEMA['kes'][0]}

P = lambda t: f'<p style="margin:8px 0">{t}</p>'


def metin(ic, fs=16):
    return f'<div style="font-size:{fs}px;line-height:1.58">{ic}</div>'


def kart(baslik, ic, renk=None, ikon=''):
    renk = renk or RENK
    return (f'<div style="border:3px solid {renk}33;border-left:8px solid {renk};border-radius:16px;padding:12px 16px;margin:10px 0;background:#fff">'
            f'<div style="font-size:19px;font-weight:900;color:{renk}">{ikon} {baslik}</div><div style="font-size:15px;line-height:1.55;margin-top:4px">{ic}</div></div>')


def bilgi(t):
    return f'<div class="not">{t}</div>'


# ---------------- 1. Kapak ----------------
kit_rozet = ''.join(f'<div style="width:62px;height:84px;border-radius:12px;background:{KITAP_RENK[i]};color:#fff;display:grid;place-items:center;font-size:40px;font-weight:900;box-shadow:0 4px 0 #0002">{i}</div>' for i in range(1, 6))
k.kapak('Beş çalışma kitabının amacı, yöntemi ve günlük kullanımı. Özel gereksinimli çocuklar için uyarlamalar, evde oynanacak matematik oyunları, '
        'ilerleme çizelgeleri ve gözlem formu.', f'<div style="display:flex;gap:8px;align-items:flex-end">{kit_rozet}</div>')

# ---------------- 2. Setin amacı ----------------
k.sayfa(metin(
    P('<b>Tane Tane Matematik</b>, okul öncesi ve 1. sınıf çağındaki çocuklar ile özel gereksinimli çocuklar için hazırlanmış, yazdırılarak kullanılan bir erken matematik setidir.') +
    P('Setin amacı, çocuğun sayıları <b>ezberlemesi</b> değil, sayıların ne anlama geldiğini <b>yaşayarak</b> kavramasıdır: “5” dediğinde beş tane nesneyi gözünde canlandırabilmesi, '
      '“bir fazlası” dendiğinde ne olacağını tahmin edebilmesi.') +
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0">' +
    ''.join(f'<div style="background:{ACIK};border-radius:16px;padding:12px 14px"><div style="font-size:30px">{i}</div><div style="font-weight:800;font-size:17px;color:{KOYU}">{b}</div><div style="font-size:14.5px">{t}</div></div>'
            for i, b, t in [('🐢', 'Tane tane', 'Her sayfada az görev. Acele yok; her çocuk kendi hızında.'),
                            ('🔁', 'Hep aynı düzen', 'Dersler aynı sırayla ilerler. Çocuk ne olacağını bilir, kaygısı azalır.'),
                            ('✋', 'Önce el, sonra kâğıt', 'Her kavram önce gerçek nesnelerle, sonra resimle, en son rakamla.'),
                            ('🧩', 'Herkese uygun', 'Özel gereksinimli çocuklar için uyarlama önerileri her kitapta var.')]) + '</div>' +
    P('<b>Kimler için?</b> 4–7 yaş arası çocuklar; sayı kavramını geç ya da zor edinen çocuklar; otizm spektrumu, dikkat güçlüğü, gelişim geriliği gibi '
      'farklı gereksinimleri olan çocuklarla çalışan öğretmenler ve aileler. Yaş yerine çocuğun <b>şu anki düzeyinden</b> başlayın.') +
    P('<b>Neler gerekir?</b> Yazıcı, kalem, boya, makas, yapıştırıcı ve sayaç olarak kullanılacak küçük nesneler (fasulye, düğme, lego). Hepsi bu kadar.') +
    bilgi('Bu rehber bir tedavi ya da terapi programı değildir. Özel eğitim desteği alan çocuklarda, çalışmaları çocuğun öğretmeni veya uzmanıyla birlikte planlamanız en doğrusudur.')),
    baslik='Setin amacı', no='1')

# ---------------- 3. 5 kitabın haritası ----------------
HARITA = [
    (1, 'Sayılarla Tanışıyorum', '1’den 5’e', 'Saymak, rakamı tanımak ve yazmak, beşlik çerçeve, çok–az', 'Okul öncesi'),
    (2, 'On’a Kadar Sayıyorum', '6–10 ve 0', 'Saymak, yazmak, onluk çerçeve, 5 ve …, sıfır, sayı doğrusu, sıralama, bir fazlası', 'Okul öncesi'),
    (3, 'Toplama ve Çıkarma Hikâyeleri', '20’ye kadar', 'Parça–bütün, sayı bağı, toplama, çıkarma, sayı doğrusunda ileri–geri', '1. sınıf'),
    (4, 'Şekiller, Örüntüler, Ölçme', 'Geometri ve ölçme', 'Şekiller, örüntü, büyük–küçük, uzun–kısa, sınıflama', 'Okul öncesi'),
    (5, 'Kes, Dokun, Say', 'Materyaller', 'Rakam, nokta, nesne kartları, çerçeveler, sayı doğrusu, rozetler', 'Hepsi'),
]
satir = ''.join(f'''<div style="display:flex;gap:14px;align-items:stretch;margin:10px 0">
<div style="width:72px;border-radius:16px;background:{KITAP_RENK[n]};color:#fff;display:grid;place-items:center;font-size:44px;font-weight:900">{n}</div>
<div style="flex:1;border:3px solid {KITAP_RENK[n]}40;border-radius:16px;padding:10px 14px;background:#fff">
<div style="display:flex;align-items:baseline;gap:10px"><span style="font-size:20px;font-weight:900;color:{KITAP_RENK[n]}">{ad}</span><span style="font-size:13px;font-weight:700;color:#64748b">{kap} · {sev}</span></div>
<div style="font-size:14.5px;margin-top:3px">{ic}</div></div></div>''' for n, ad, kap, ic, sev in HARITA)
yol = (f'<div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;font-size:16px;font-weight:800">'
       + '<span style="font-size:22px;color:#94a3b8">→</span>'.join(f'<span class="rozet" style="background:{KITAP_RENK[n]};font-size:16px">{n}</span>' for n in (1, 2, 3)) +
       '<span style="margin-left:18px;color:#64748b;font-size:14px">4. kitap her aşamada araya serpiştirilebilir · 5. kitap hepsinde kullanılır</span></div>')
k.sayfa(satir + yol + bilgi('<b>Önerilen sıra:</b> 1 → 2 → 3. Bir kitabı bitirmeden ötekine geçmek zorunda değilsiniz: çocuk 1–5’i rahat sayıyorsa Kitap 2’ye başlayıp '
                           'Kitap 1’in tekrar sayfalarını ısınma olarak kullanabilirsiniz. Kitap 4 (şekil, örüntü) sayı çalışmalarına mola veren keyifli bir değişikliktir.'),
        baslik='Beş kitabın haritası', no='2', yonerge='Her kitabın bir rengi var.')

# ---------------- 4. Somut → Resim → Sembol ----------------
basamak = [('✋', 'Somut', 'Gerçek nesneler', 'Fasulye, lego, kaşık… Çocuk dokunur, taşır, sayar.', nesneler('🫘', 3, 40)),
           ('🖼️', 'Resim', 'Çizim ve nokta', 'Sayfadaki elmalar, noktalar, çerçeve.', nokta_karti(3, 80, RENK)),
           ('3', 'Sembol', 'Rakam ve işaret', 'Rakamı okur, yazar; “+” ve “=” kullanır.', f'<div style="font-size:76px;font-weight:900;color:{RENK};line-height:1">3</div>')]
g = '<div style="display:flex;gap:10px;align-items:stretch;margin-top:12px">' + '<div style="align-self:center;font-size:34px;color:#94a3b8">➜</div>'.join(
    f'<div style="flex:1;border:3px solid {ACIK};border-radius:18px;padding:12px;text-align:center;background:#fff"><div style="font-size:22px;font-weight:900;color:{KOYU}">{i} {a}</div>'
    f'<div style="font-size:13px;font-weight:700;color:{RENK}">{b}</div><div style="height:96px;display:grid;place-items:center;margin:6px 0">{v}</div><div style="font-size:14px">{t}</div></div>'
    for i, a, b, t, v in basamak) + '</div>'
k.sayfa(g + metin(
    P('<b>Ne demek?</b> Yeni bir kavram önce gerçek nesnelerle, sonra resimle, en son rakam ve işaretle çalışılır. Matematik eğitiminde yaygın olarak kullanılan ve '
      '<b>araştırmalarla desteklenen</b> bir yaklaşımdır (somut–temsili–soyut sıralaması olarak da bilinir).') +
    P('<b>Nasıl uygularım?</b> Sayfaya geçmeden önce aynı görevi masada nesnelerle yapın. Örneğin “3 + 2” sayfasından önce 3 fasulye ile 2 fasulyeyi birleştirin. '
      'Çocuk sayfada zorlanırsa bir basamak geri dönün: rakamdan resme, resimden nesneye.') +
    P('<b>Ne zaman ilerlerim?</b> Çocuk bir basamakta birkaç gün üst üste rahatça başarılı oluyorsa bir sonrakine geçin. Basamaklar kesin çizgilerle ayrılmaz; '
      'rakamla çalışırken de nesne masada durabilir.'), 15.5),
        baslik='Yöntem 1 · Somut → Resim → Sembol', no='3')

# ---------------- 5. Sayı hissi ve anında tanıma ----------------
ornek = ''.join(f'<div style="text-align:center">{nokta_karti(n, 92, RENK)}<div style="font-weight:800;margin-top:4px">{n}</div></div>' for n in (2, 3, 4, 5))
k.sayfa(metin(
    P('<b>Sayı hissi</b>, sayıların ne kadar büyük olduğunu sezmek, karşılaştırmak ve aralarındaki ilişkiyi görmektir: 4’ün 5’ten bir eksik olduğunu, 10’un 2’den çok olduğunu “hissetmek”. '
      'Erken yaşta gelişen sayı hissinin sonraki matematik öğrenimiyle ilişkili olduğu pek çok çalışmada gösterilmiştir.') +
    P('<b>Anında tanıma</b> (saymadan bir bakışta söyleme), küçük miktarlarda (genellikle 1–4, düzenli dizilince 5–6) mümkündür. Zar ve nokta kartı düzenleri bunu kolaylaştırır.')) +
    f'<div style="display:flex;justify-content:space-around;margin:14px 0;background:{ACIK};border-radius:18px;padding:14px">{ornek}</div>' +
    kart('Nasıl çalışılır?', '• Nokta kartını 2 saniye gösterip kapatın: “Kaç tane gördün?”<br>• Doğru söylerse: “Nasıl gördün?” diye sorun. “İki ve iki” gibi açıklamalar çok değerlidir.<br>'
         '• Yanlışsa düzeltmek yerine kartı tekrar açıp birlikte sayın.<br>• 6–10 kartlarında “5 ve …” düzenini vurgulayın: “Beş ve üç, sekiz.”', ikon='👀') +
    kart('Sayı hissini besleyen günlük sorular', '“Hangisinde daha çok var?” · “Bir tane daha koyarsak kaç olur?” · “Beşe ulaşmak için kaç tane lazım?” · “Tahmin et, sonra say.”', ikon='💬'),
    baslik='Yöntem 2 · Sayı hissi ve anında tanıma', no='4', oyun=None)

# ---------------- 6. Beşlik / onluk çerçeve ----------------
k.sayfa(metin(
    P('<b>Beşlik çerçeve</b> bir sırada 5 kutu, <b>onluk çerçeve</b> iki sırada 10 kutudur. Kutular soldan sağa, önce üst sıra doldurulur. Böylece sayılar 5 ve 10 ile '
      'ilişkilendirilerek görülür: 7, “5 ve 2” ya da “10’dan 3 eksik” olur. Erken matematikte sıkça kullanılan, <b>araştırmalarla desteklenen</b> bir görsel araçtır.')) +
    f'<div style="display:flex;justify-content:space-around;align-items:center;margin:12px 0"><div style="text-align:center">{cerceve(3, 5, 62, RENK)}<div style="font-weight:800;margin-top:6px">3: iki kutu boş</div></div>'
    f'<div style="text-align:center">{cerceve(7, 10, 50, RENK)}<div style="font-weight:800;margin-top:6px">7 = 5 ve 2</div></div></div>' +
    f'<div style="display:flex;justify-content:center;margin:6px 0 10px"><div style="text-align:center">{cerceve(4, 10, 58, "#ef4444", 3, "#3b82f6")}<div style="font-weight:800;margin-top:6px">4 kırmızı + 3 mavi = 7</div></div></div>' +
    kart('Sorulacak sorular', '“Kaç tane var?” · “Kaç kutu boş?” · “Dolması için kaç tane lazım?” · “5’ten çok mu, az mı?”', ikon='❓') +
    kart('İpucu', 'Kitap 5’teki boş çerçeveleri lamine edin; sayaçları koyup kaldırarak her gün birkaç sayı gösterin. Aynı sayıyı iki renk sayaçla farklı şekillerde gösterin (5 = 4 + 1 = 3 + 2).', ikon='💡'),
    baslik='Yöntem 3 · Beşlik ve onluk çerçeve', no='5', oyun=OY['matakis'])
assert 4 + 3 == 7 and 5 + 2 == 7

# ---------------- 7. Parça–bütün ve sayı doğrusu ----------------
k.sayfa(f'<div style="display:flex;gap:16px;align-items:center">{sayi_bagi(5, 3, 2, px=200)}' + metin(
    P('<b>Parça–bütün</b>: Bir miktar iki parçaya ayrılabilir ve parçalar yeniden birleşince bütünü verir. 5, “3 ve 2” ya da “4 ve 1” olabilir. '
      'Toplama ve çıkarmayı aynı ilişkinin iki yüzü olarak görmeyi sağlar; sayı bağı bu ilişkiyi çizer.') +
    P('<b>Önce somut:</b> 5 fasulyeyi iki avuca ayırın. “Bu elde kaç, öbür elde kaç, hepsi kaç?”'), 15) + '</div>' +
    f'<div style="margin-top:12px;display:flex;justify-content:center">{sayi_dogrusu(0, 10, isaret=[3, 5], atla=(3, 2), w=640)}</div>' +
    metin(P('<b>Sayı doğrusu</b> sayıları sırayla ve eşit aralıklarla gösterir. “Bir fazlası” bir adım sağa, “bir eksiği” bir adım sola gitmektir. Yukarıda 3’ten 2 adım ileri: 5. '
            'Sayı doğrusu, sayıların büyüklük ilişkisini görmede <b>araştırmalarla desteklenen</b> bir araçtır.') +
           P('<b>Önce bedenle:</b> Yere bantla bir sayı doğrusu yapın; çocuk üzerinde zıplayarak ileri–geri saysın. Sonra Kitap 5’teki şeritle masada oyuncak yürütün.'), 15) +
    bilgi('Dört araç (nokta kartı, çerçeve, sayı bağı, sayı doğrusu) aynı sayıya farklı pencerelerden bakmaktır. Bir çocuk birinde zorlanırsa diğeriyle deneyin.'),
    baslik='Yöntem 4 · Parça–bütün ve sayı doğrusu', no='6', oyun=OY['kum'])
assert 3 + 2 == 5

# ---------------- 8. Günlük plan ----------------
PLAN = [('1–2 dk', '👋 Açılış', 'Aynı şarkı ya da sayma tekerlemesi. “Bugün kaç?” sayacına bir sayaç ekleyin.'),
        ('2–3 dk', '✋ Somut ısınma', 'Gerçek nesnelerle o günün sayısı / işlemi. Ör. 6 fasulyeyi onluk çerçeveye koyma.'),
        ('4–6 dk', '📄 Kitap sayfası', '1 sayfa (gerekirse yarım sayfa). Yetişkin yanında, kısa yönerge.'),
        ('2–3 dk', '🎲 Oyun', 'Kartlarla kısa oyun ya da QR’daki dijital oyun.'),
        ('1 dk', '🏅 Kapanış', 'Ne yaptığını birlikte söyleyin; takip çizelgesine ✔ koyun. Gerekirse bir rozet verin.')]
tbl = '<table class="tbl" style="font-size:15px"><tr><th style="width:80px">Süre</th><th style="width:150px">Bölüm</th><th>Ne yapılır?</th></tr>' + ''.join(
    f'<tr><td><b>{s}</b></td><td><b>{b}</b></td><td>{t}</td></tr>' for s, b, t in PLAN) + '</table>'
HAFTA = [('Pzt', 'Yeni sayfa / yeni sayı'), ('Sal', 'Aynı konu, ikinci sayfa'), ('Çar', 'Kartlarla oyun günü'), ('Per', 'Yeni sayfa'), ('Cum', 'Tekrar + evde oyun')]
hafta = '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:10px">' + ''.join(
    f'<div style="background:{ACIK};border-radius:14px;padding:10px;text-align:center"><div style="font-weight:900;color:{KOYU};font-size:18px">{g}</div><div style="font-size:13.5px">{t}</div></div>' for g, t in HAFTA) + '</div>'
k.sayfa(tbl + '<div style="font-size:19px;font-weight:800;margin:16px 2px 4px">Örnek hafta</div>' + hafta +
        kart('Neden kısa?', 'Küçük çocuklarda ve dikkat güçlüğü olan çocuklarda kısa, sık ve düzenli çalışma genellikle uzun ve seyrek oturumlardan daha verimlidir. '
             'Çocuk yorulmadan, keyifliyken bitirmek bir sonraki güne isteği taşır.', ikon='⏱️') +
        kart('Esneklik', 'Bu bir örnektir. Kötü bir günde yalnızca somut ısınma ve oyun yeterlidir. Süre çocuğun dikkat süresine göre kısaltılabilir.', ikon='🌤️'),
        baslik='Günde 10–15 dakika: örnek plan', no='7', yonerge='Her gün aynı sıra, kısa ve keyifli.')

# ---------------- 9. Özel gereksinim 1: hatasız öğretim + ipucu basamakları ----------------
IPUCU = [('Tam fiziksel', 'Elini elinizle tutup birlikte dokunarak sayarsınız.', '🤲'),
         ('Kısmi fiziksel', 'Bileğine ya da dirseğine hafifçe dokunup yönlendirirsiniz.', '👉'),
         ('İşaret / model', 'Doğru yeri parmakla gösterir ya da bir kez siz yaparsınız.', '☝️'),
         ('Bağımsız', 'Çocuk kendi başına yapar. Siz yalnızca izler ve översiniz.', '⭐')]
merdiven = '<div style="display:flex;align-items:flex-end;gap:8px;margin:12px 0">' + ''.join(
    f'<div style="flex:1;background:{RENK};opacity:{.55 + i*.15:.2f};border-radius:14px 14px 4px 4px;padding:10px;color:#fff;height:{120 + i*36}px;display:flex;flex-direction:column;justify-content:flex-end">'
    f'<div style="font-size:30px">{ik}</div><div style="font-weight:900;font-size:16px">{i+1}. {a}</div><div style="font-size:12.5px;line-height:1.35">{t}</div></div>' for i, (a, t, ik) in enumerate(IPUCU)) + '</div>'
k.sayfa(kart('Hatasız öğretim', 'Yeni bir beceri öğretilirken çocuğun hata yapmasına fırsat vermeden, doğru cevabı baştan yeterli yardımla göstermek ve yardımı yavaş yavaş azaltmaktır. '
             'Özel eğitimde yaygın kullanılan, <b>araştırmalarla desteklenen</b> bir yaklaşımdır. Tekrarlanan hatalar yanlış cevabın da öğrenilmesine ve hayal kırıklığına yol açabilir.', ikon='🎯') +
        '<div style="font-size:19px;font-weight:800;margin:14px 2px 0">İpucu basamakları: çoktan aza</div>' + merdiven +
        metin(P('<b>Nasıl kullanılır?</b> Çocuğun başarılı olacağı en az yardımla başlayın; yeni beceride bu çoğu zaman tam fiziksel yardımdır. Birkaç doğru denemeden sonra bir basamak '
                'yukarı çıkın (daha az yardım). Zorlanırsa bir basamak geri inin. Amaç, yardımın zamanla tamamen çekilmesidir.') +
              P('<b>Bekleme süresi:</b> Yönergeden sonra 3–5 saniye sessizce bekleyin; hemen yardım etmeyin. Bazı çocukların cevabı düzenlemek için zamana ihtiyacı vardır.'), 15),
        baslik='Özel gereksinim · Hatasız öğretim', no='8', yonerge='Yardım ederek başla, yardımı azaltarak bitir.')

# ---------------- 10. Özel gereksinim 2 ----------------
GORSEL = [('👋', 'Merhaba'), ('🫘', 'Say'), ('📄', 'Sayfa'), ('🎲', 'Oyun'), ('⭐', 'Bitti')]
gp = '<div style="display:flex;gap:8px;justify-content:center;margin:6px 0">' + '<span style="align-self:center;color:#94a3b8;font-size:22px">→</span>'.join(
    f'<div style="width:86px;border:3px solid {RENK};border-radius:12px;text-align:center;padding:6px;background:#fff"><div style="font-size:36px">{e}</div><div style="font-weight:800;font-size:14px">{t}</div></div>' for e, t in GORSEL) + '</div>'
k.sayfa('<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 14px">' +
        '<div>' + kart('Görsel program', 'Çalışmanın adımlarını resimli kartlarla sırayla gösterin. Biten adımın kartını “bitti” kutusuna koyun. Ne olacağını bilmek geçişleri kolaylaştırır.', ikon='🗓️') + '</div>' +
        '<div>' + kart('Tek görev', 'Sayfanın yalnızca bir kutusu görünsün: sayfayı katlayın ya da bir kâğıtla diğer kutuları örtün. Bir kutu bitince sonrakini açın.', ikon='1️⃣') + '</div>' +
        '</div>' + gp +
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 14px">' +
        '<div>' + kart('Pekiştirme', 'Doğru davranışın hemen ardından ve ne için olduğunu söyleyerek övün: “Her birine dokunarak saydın!” Çocuğun sevdiği küçük bir etkinlik (bir şarkı, bir dakika oyuncak) de ödül olabilir. '
                       'Beceri yerleştikçe ödülü seyrekleştirin.', ikon='🏅') + '</div>' +
        '<div>' + kart('Dikkat süresi', 'Oturumu çocuğun dikkat süresine göre planlayın; 3–5 dakikalık bölümler + kısa hareket molası. Çalışmayı, çocuk henüz istekliyken bitirin. '
                       'Masada yalnızca o görevin malzemesi olsun.', ikon='⏳') + '</div>' +
        '<div>' + kart('İnce motor zorluğu', 'Yazmak zorsa amaç matematiktir, kalem değil: rakam kartını <b>yapıştırabilir</b>, doğru cevabı <b>gösterebilir</b>, söyleyebilir ya da kartı seçip verebilir. '
                       'Kalın kalem, kalem tutacağı, büyük kutular yardımcı olur.', ikon='✋') + '</div>' +
        '<div>' + kart('Dil ve iletişim', 'Kısa, aynı kalıp yönergeler kullanın: “Say.” “Göster.” “Hangisi 4?” Konuşmayan çocuklar gösterme, kart verme ya da iletişim araçlarıyla cevaplayabilir.', ikon='💬') + '</div>' +
        '</div>' + bilgi('Uyarlamalar çocuğa göre seçilir; hepsini birden uygulamak gerekmez. Çocuğun öğretmeni ya da uzmanıyla aynı yöntemi kullanmak, çocuğun işini kolaylaştırır.'),
        baslik='Özel gereksinim · Uyarlamalar', no='9')

# ---------------- 11. Evde matematik oyunları ----------------
EV = [('🍽️', 'Sofrayı kur', 'Kaç kişiyiz? O kadar tabak, o kadar kaşık. Her tabağa bir kaşık (birebir eşleme).'),
      ('🪜', 'Merdiven sayma', 'Her basamakta bir sayı. İnerken geri sayın: “5, 4, 3…”'),
      ('🧺', 'Çorap eşleri', 'Çorapları eşleyin, ikişer sayın. “Kaç çift oldu? Teki kalan var mı?”'),
      ('🛒', 'Market', 'Sepete “3 elma koyalım” deyin. Kasada ürünleri birlikte sayın. Hangi poşet daha ağır?'),
      ('🍳', 'Mutfakta sayma', 'Tarifte 2 yumurta, 3 kaşık… Ölçerken sayın. “Kaç kaşık kaldı?”'),
      ('🚗', 'Yol oyunu', 'Yolda kırmızı arabaları sayın. 5 olunca el çırpın.'),
      ('🧸', 'Oyuncak toplama', 'Oyuncakları kutuya toplarken sayın. “Kaç tane kaldı?”'),
      ('🎲', 'Zar oyunu', 'Zar atın, o kadar zıplayın ya da o kadar alkış.')]
k.sayfa('<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px">' + ''.join(
    f'<div style="border:3px solid {ACIK};border-radius:18px;padding:12px 14px;display:flex;gap:12px;align-items:flex-start;background:#fff"><span style="font-size:42px;line-height:1">{e}</span>'
    f'<div><div style="font-size:18px;font-weight:900;color:{KOYU}">{b}</div><div style="font-size:14.5px;line-height:1.45">{t}</div></div></div>' for e, b, t in EV) + '</div>' +
    bilgi('Evde matematik, “ders” gibi değil, günlük işin içinde geçen sohbet gibi olsun. Çocuk saymayı yanlış yaparsa düzeltmek yerine “Birlikte sayalım mı?” deyin. '
          'Küçük nesnelerle oynarken ağza alma riskine karşı gözetim gerekir.'),
    baslik='Evde yapılacak matematik oyunları', no='10', yonerge='Ev, en iyi matematik sınıfıdır.')

# ---------------- 12–13. İlerleme takip çizelgeleri ----------------
DERS = {
    1: ['1 ile tanışma', '2 ile tanışma', '3 ile tanışma', '4 ile tanışma', '5 ile tanışma', 'Rakam yazma 1–5', 'Beşlik çerçeve', 'Bir bakışta söyle', 'Çok mu, az mı?', 'Sayı treni (sıralama)'],
    2: ['6 ile tanışma', '7 ile tanışma', '8 ile tanışma', '9 ile tanışma', '10 ile tanışma', 'Rakam yazma 6–10', 'Onluk çerçeve', '5 ve … (6–10)', 'Sıfır ve sayı doğrusu', 'Bir fazlası / bir eksiği', 'Sıralama 1–10'],
    3: ['Parça–bütün (somut)', 'Sayı bağı', 'Toplama: birleştirme', 'Toplama: sayı doğrusu', 'Çıkarma: ayırma', 'Çıkarma: sayı doğrusu', '10’a tamamlama', '20’ye kadar sayılar', 'Hikâyeli problemler', 'Karışık tekrar'],
    4: ['Daire, kare, üçgen', 'Dikdörtgen ve diğer şekiller', 'Şekilleri sınıflama', 'Örüntü (AB)', 'Örüntü (ABB, ABC)', 'Büyük–küçük', 'Uzun–kısa', 'Ağır–hafif', 'Sıralama (boy)', 'Karışık tekrar'],
    5: ['Rakam kartları hazırlandı', 'Nokta / nesne kartları', 'Çerçeveler ve sayaçlar', 'Sayı doğrusu birleştirildi', 'Sayı bağı ve işlem kartları', 'Hafıza oyunu', 'Eşini Bul', 'Sıraya Diz', 'Bir Fazlası', '“Bugün kaç?” rutini'],
}
for n in DERS: assert 10 <= len(DERS[n]) <= 11


def cizelge(n, fs=13):
    r = KITAP_RENK[n]
    bas = (f'<tr><th style="background:{r};color:#fff;width:44%">Kitap {n} · {HARITA[n-1][1]}</th><th style="background:{r};color:#fff;text-align:center">Yardımla</th>'
           f'<th style="background:{r};color:#fff;text-align:center">Bağımsız</th><th style="background:{r};color:#fff;width:22%">Tarih</th></tr>')
    kutu = '<td style="text-align:center"><span style="display:inline-block;width:20px;height:20px;border:2.5px solid #94a3b8;border-radius:5px"></span></td>'
    return (f'<table class="tbl" style="font-size:{fs}px;margin:8px 0">' + bas + ''.join(f'<tr><td>{d}</td>{kutu}{kutu}<td></td></tr>' for d in DERS[n]) + '</table>')


k.sayfa('<div style="font-size:14px;color:#475569;margin:10px 2px 2px">Çocuğun adı: ........................................................ &nbsp; Başlama tarihi: ......................</div>' +
        cizelge(1) + cizelge(2) + bilgi('“Yardımla” sütununu ipucu ile yaptığı, “Bağımsız” sütununu tek başına yaptığı gün işaretleyin (✔). İki ✔ arasındaki fark, yardımın nasıl azaldığını gösterir.'),
        baslik='İlerleme çizelgesi · Kitap 1 ve 2', no='11', yonerge='Her dersten sonra ✔ koyun ve tarih yazın.')
k.sayfa(cizelge(3, 13) + cizelge(4, 13),
        baslik='İlerleme çizelgesi · Kitap 3 ve 4', no='12')
k.sayfa(cizelge(5, 13) + bilgi('Kes-kullan materyallerini hazırladıkça ve kart oyunlarını oynadıkça işaretleyin.'),
        baslik='İlerleme çizelgesi · Kitap 5', no='12')

# ---------------- 14. Gözlem formu ----------------
GOZ = ['Sayıları sırayla söyler (1’den …’e kadar)', 'Her nesneye bir kez dokunarak sayar (birebir eşler)', 'Son söylediği sayının “kaç tane” olduğunu bilir',
       'Nesnelerin yeri değişince sayının değişmediğini bilir', 'Küçük miktarları saymadan tanır (1–4)', 'İstenen sayıda nesne verir (“Bana 4 tane ver”)',
       'Rakamı tanır ve adını söyler', 'Rakamı miktarla eşleştirir', 'İki gruptan hangisinin çok / az olduğunu söyler', 'Bir fazlasını / bir eksiğini söyler',
       'Bir sayıyı iki parçaya ayırır (5 = 3 ve 2)', 'Rakamı yazar ya da kartla gösterir']
kutu3 = ''.join('<td style="text-align:center"><span style="display:inline-block;width:18px;height:18px;border:2.5px solid #94a3b8;border-radius:50%"></span></td>' for _ in range(3))
gtbl = ('<table class="tbl" style="font-size:13.5px;margin-top:10px"><tr><th>Davranış</th><th style="text-align:center;width:66px">Henüz değil</th><th style="text-align:center;width:66px">Yardımla</th>'
        '<th style="text-align:center;width:66px">Bağımsız</th><th style="width:20%">Not (hangi sayıya kadar?)</th></tr>' +
        ''.join(f'<tr><td>{i}. {d}</td>{kutu3}<td></td></tr>' for i, d in enumerate(GOZ, 1)) + '</table>')
k.sayfa('<div style="display:flex;gap:16px;font-size:14px;color:#475569;margin:10px 2px 0"><span>Çocuğun adı: ..................................</span><span>Tarih: ................</span><span>Gözlemleyen: ..........................</span></div>' +
        gtbl + bilgi('Gözlemi oyun içinde, doğal ortamda yapın; çocuğu sınav havasına sokmayın. 4–6 haftada bir tekrarlayıp karşılaştırın. '
                     'Bu form bir tanı ya da değerlendirme aracı değildir; çocuğun öğretmeni veya uzmanıyla paylaşmak için bir gözlem notudur.'),
        baslik='Gözlem formu', no='13', yonerge='Çocuk ne yapabiliyor? Gözlediğinizi işaretleyin.')

# ---------------- 15. Dijital oyunlar ----------------
DIJ = [('parmak', 'Kitap 1, 2', 'Parmaklarla 1–10 gösterme; sayı–miktar eşleme'),
       ('matakis', 'Kitap 1, 2, 3', 'Gör, dokun, say; çerçeve ve sayı oyunları'),
       ('minik', 'Kitap 1, 4', 'Okul öncesi kavram ve sayma oyunları'),
       ('kum', 'Kitap 2, 3', 'Doğru sayıya / sonuca topu yuvarlama'),
       ('kup', 'Kitap 4', 'Yol bulma, sıra ve örüntü (mantık)')]
satirlar = ''.join(f'''<div style="display:flex;gap:14px;align-items:center;border:3px solid {ACIK};border-radius:18px;padding:10px 14px;margin:9px 0;background:#fff">
{qr_svg(qr_kodu("reh", OY[a][1], OY[a][0]), 92)}<div style="flex:1"><div style="font-size:19px;font-weight:900;color:{KOYU}">{OY[a][0]}</div>
<div style="font-size:14.5px;margin-top:2px">{t}</div></div><span class="rozet" style="background:{RENK}">{kit}</span></div>''' for a, kit, t in DIJ)
k.sayfa(satirlar + bilgi('<b>Kâğıt önce, ekran sonra.</b> Dijital oyunlar, kitapta çalışılan konuyu pekiştirmek içindir; somut ve kâğıt çalışmasının yerini tutmaz. '
                         'Ekran süresini kısa tutun (5–10 dk) ve mümkünse çocukla birlikte oynayın. QR’ı telefon kamerasıyla okutun ya da ' + ADRES + ' adresine girin.'),
        baslik='Dijital oyunlarla birlikte kullanım', no='14', yonerge='Telefon kamerasıyla QR kodu okutun.')

# ---------------- 16–17. SSS ----------------
SSS = [('Parmakla sayması doğru mu?', 'Evet, destekleyin. Parmaklar her zaman yanında olan doğal bir sayma aracıdır ve parmak kullanımı erken sayı becerileriyle ilişkilidir. '
        'Zamanla, sayılar zihinde yerleştikçe çocuk parmağa daha az ihtiyaç duyar. Yasaklamak yerine “5 ve 2, parmaklarında göster” gibi düzenli kullanımı teşvik edin.'),
       ('Rakamı ters yazıyor, sorun mu?', 'Bu yaşta yaygındır ve çoğu çocukta zamanla kendiliğinden azalır. Düzeltip üzerinde durmak yerine model olun: rakamı yanına doğru yazın, '
        'başlangıç noktasını gösterin, havada ve kumda birlikte çizin. 1. sınıfın sonrasında da sık ve sürekli devam ediyorsa öğretmeniyle konuşun.'),
       ('1’den 10’a sayıyor ama 5 tane nesne veremiyor. Neden?', 'Sayıları sırayla söylemek (ezbere sayma) ile miktarı anlamak farklı becerilerdir. Birebir dokunarak saymaya '
        've “son sayı kaç tane olduğunu söyler” fikrine dönün. Kitap 1’in nesne sayfaları ve beşlik çerçeve bunun içindir.'),
       ('Her gün çalışmak istemiyor. Ne yapayım?', 'Süreyi kısaltın, oyunla başlayın, sayfayı ikiye bölün. Bir gün yalnızca kartlarla oynamak da çalışmadır. '
        'Zorlamak isteksizliği artırabilir; kısa ve keyifli bir başarıyla bitirmek ertesi gün için isteği taşır.'),
       ('Kitapları sırayla mı bitirmeliyiz?', 'Kitap 1 → 2 → 3 sırası önerilir, ama katı değildir. Kitap 4 her aşamada araya girebilir. Çocuk bildiği konuları hızlı geçebilir; '
        'zorlandığı yerde daha uzun kalmak normaldir.'),
       ('Hata yapınca düzeltmeli miyim?', 'Hatayı “yanlış” diye işaretlemek yerine birlikte tekrar yapın: “Birlikte sayalım.” Yeni bir beceride hatasız öğretimi deneyin: '
        'önce doğruyu gösterin, sonra yardımı azaltın.'),
       ('Çocuğum özel eğitim alıyor. Bu seti kullanabilir miyim?', 'Evet; set, uyarlamaya uygun hazırlandı. Yine de çocuğun öğretmeni veya uzmanıyla konuşup '
        'hedeflerini ve yöntemini birlikte belirlemeniz en doğrusudur. Aynı dili ve ipuçlarını kullanmak çocuğun işini kolaylaştırır.'),
       ('Ne kadar sürede öğrenir?', 'Her çocuğun hızı farklıdır ve bir süre vermek doğru olmaz. İlerlemeyi takip çizelgesinden izleyin: “Yardımla”dan “Bağımsız”a geçen her ders bir adımdır.'),
       ('Tablet / telefon oyunları yeterli mi?', 'Tek başına önerilmez. Somut nesnelerle ve kâğıtla çalışma temeldir; dijital oyunlar kısa pekiştirme içindir.'),
       ('Sıfırı ne zaman öğretelim?', '“Hiç yok” fikri, ör. “tabakta hiç elma kalmadı”, günlük konuşmada erkenden geçebilir. Rakam olarak 0, 2. Kitap’ta (s. 28–29) “hiç yok” sayfalarıyla tanıtılır; sayı doğrusu ve çıkarma ile birlikte (3. Kitap) daha da anlam kazanır.')]
for parca, no in ((SSS[:5], '15'), (SSS[5:], '16')):
    k.sayfa(''.join(f'''<div style="border:3px solid {ACIK};border-radius:18px;padding:12px 16px;margin:10px 0;background:#fff">
<div style="font-size:18px;font-weight:900;color:{KOYU}">❓ {s}</div><div style="font-size:14.5px;line-height:1.55;margin-top:4px">{c}</div></div>''' for s, c in parca) +
            (f'<div style="display:flex;gap:12px;align-items:center;margin-top:8px">{tane(80, "mutlu")}<div style="font-size:15px;font-weight:700;color:#475569">Sorunuz burada yoksa: çocuğu izleyin, bir adım geri gidin, kısa tutun ve keyifli bitirin.</div></div>' if no == '16' else ''),
            baslik='Sık sorulan sorular' + (' (devam)' if no == '16' else ''), no=no)

# ---------------- 18. Kapanış ----------------
k.sayfa(f'''<div style="position:absolute;inset:0;background:linear-gradient(170deg,{ACIK},#fff 60%)"></div>
<div style="position:relative;text-align:center;padding-top:22mm">{tane(190, 'mutlu', True)}
<div style="font-size:50px;font-weight:900;color:{KOYU};margin-top:8mm;line-height:1.1">Tane tane,<br>adım adım.</div>
<div style="font-size:20px;line-height:1.6;max-width:150mm;margin:8mm auto 0;color:#334155">Her çocuk kendi hızında öğrenir. Bugün bir sayıyı dokunarak saymak,
yarın onu rakamla yazmanın ilk adımıdır. Kısa, düzenli ve keyifli çalışmalar; sabırlı ve güler yüzlü bir yetişkin… Gereken çoğu şey bu kadar.</div>
<div style="display:flex;justify-content:center;gap:8px;margin-top:10mm">{kit_rozet}</div>
<div style="margin-top:10mm;display:flex;flex-direction:column;align-items:center;gap:6px;font-size:14px;color:#475569">{qr_svg(SET_SAYFA, 110)}<b>Setin tamamı ve dijital oyunlar</b>{ADRES}</div>
<div style="margin-top:8mm;font-size:13px;color:#64748b">Barış Öğretmen · Tane Tane Matematik · Yazdırılabilir eğitim seti</div></div>''', ham=True)

print('Rehber sayfa:', k.pdf('/home/claude/mat/cikti/Tane_Tane_Matematik_0_Ogretmen_Veli_Rehberi.pdf'))
