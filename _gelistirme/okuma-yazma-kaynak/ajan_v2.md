GÖREV: Barış Öğretmen'in "Adım Adım Okuma–Yazma Seti"nin YENİ sürümü için içerik yazmak. Hedef: ilk okuma-yazma öğrenen çocuklar, ÖZELLİKLE özel gereksinimli çocuklar. İçerik somut, sıcak, tekrarlı ve günlük hayattan olmalı.

YÖNTEM (Barış'ın yöntemi): önce 8 ünlü, sonra her derste tek ünsüz. Harf sırası ve sesler /home/claude/aa/sira.json dosyasında:
- Ders 1–8: a e i o u ı ö ü
- Ders 9–29: l n k m t r y s d z b ç g ş p c h v f ğ j

Ders n'de YALNIZCA 1..n harfleri kullanılabilir. Büyük harf de yalnızca öğrenilmiş harflerden olabilir. Rakam kullanılmaz.
Denetim aracı: `python3 /home/claude/aa/dogrula.py <dosyan>`. Çıktıda HATA: 0 görene kadar düzelt; bu araç geçmeden teslim etme.

TELİF (ÇOK ÖNEMLİ):
- Her şey tamamen ÖZGÜN olacak. Hiçbir yayınlanmış okuma-yazma kitabından (Basara, Anetil yayınları vb.) kelime listesi, cümle ya da hikâye kopyalama; onları arama, açma.
- Tek tek yaygın Türkçe kelimeler ve heceler herkesindir; cümleler ve hikâyeler senin yazdığın olsun.

GENEL KURALLAR:
- Gerçek, doğal Türkçe kelimeler kullan (TDK'de olan ya da çok yaygın olan); emin olmadığın kelimeyi kullanma.
- Anlamlı cümleler yaz, doğru yazım ve noktalama kullan. Anlamsız hece dizisi cümle sayılmaz.
- Şiddet, korku ve üzücü içerik yok. "savaş", "öl", "öldü" gibi kelimeler yok. Dinî ya da siyasi içerik yok.
- Temalar: sevgi, aile, oyun, doğa, hayvanlar, okul, yardımlaşma, mizah.
- Gerçek kişi adı yok. Şu adları ASLA kullanma: Mete, Enes, Beyazıt, Poyraz, Sarp, Mustafa, Aras, Metehan, Resul, Nur.
- Ortak kahramanlar (öğrenilmiş harflerle yazılabildiği andan itibaren):
  - Ela (kız)
  - Kaan (erkek)
  - Nine (büyükanne; "nine" kelimesi)
  - Lokum (yavru kedi, ders 12'den sonra)
  - Başka uydurma ad da kullanabilirsin, öğrenilmiş harflerle yazılabiliyorsa.
- Emojiler gerçekten anlatılan şeyi göstermeli.

DERS İÇERİĞİ ŞEMASI (ders dosyaları):
{"ders":n,"harf":"x",
 "resimli_kelime":{"kelime":"…","emoji":"🍎"},
 "dinle":[{"kelime":"arı","emoji":"🐝"}, … 4-6 öğe],
 "heceler":[…],
 "kelimeler":[…8-14],
 "cumleler":[…],
 "ipucu_veli":"…tek cümle, veliye/öğretmene öneri…"}

- "dinle": yeni sesle BAŞLAYAN, emojiyle gösterilebilen somut kelimeler. Öğretmen okur, çocuk ilk sesi duyar. Bu alan DENETLENMEZ, her harf kullanılabilir.
- resimli_kelime.kelime denetlenir (öğrenilmiş harflerle olmalı). Ünlü derslerinde kelime harfin kendisi olsun, emoji de ağız ya da sesi göstersin (ör. a → 😮).

Ünlü dersleri (1–8):
- heceler: okunabilir ünlü dizileri, öğrenilmiş ünlülerle 6–10 öğe. Örnek: "a", "aa", "a e", "e a e".
- kelimeler: o ünlüyü içeren okunabilir öğeler; ünlem ve kısa diziler olabilir: "a", "aa", "Aa!", "ee", "Ee!", "oo", "Oo!", "ay" yok (y öğrenilmedi).
- cumleler: BOŞ dizi [] olsun. Ünlülerle cümle kurulamaz; cümle sayfası basılmaz.

Ünsüz dersleri (9–29):
- heceler: yeni ünsüzle 8 ünlünün HEPSİ hem açık hem kapalı hecede. Örnek: la le li lo lu lı lö lü / al el il ol ul ıl öl ül. Ders ilerledikçe 3 harfli heceler de olsun (lal, kol, nem).
- kelimeler: 8–14 öğe, çoğu YENİ harfi içersin, kısa ve uzun karışık.
- cumleler: 4–7 kısa cümle, 2–6 kelime. Ders 9'da bile en az 3 cümle olsun ("Ela, al." "Lale al." "Ali, Ela'ya el ele." gibi).

HİKÂYE ŞEMASI (hikâye dosyaları):
{"ders":n,"baslik":"…","kapak_emoji":"🐱🏠🍎","sahneler":[{"emoji":"🏠👵","cumleler":["…","…"]}, …],"sorular":[{"soru":"…","cevap":"…"}, … 3-4 soru]}

Ders n'nin hikâyesi yalnızca 1..n harfleriyle yazılır; soru metni denetlenmez, cevap denetlenir.

HİKÂYE KALİTESİ (Barış'ın açık isteği):
- İki-üç cümlelik "hikâye" KABUL EDİLMEZ. Gerçek bir hikâye olsun:
  - Bir giriş (kim, nerede).
  - Bir sorun ya da merak (kayıp eşya, yardım isteyen hayvan, sürpriz hazırlığı, yarışma, yağmur…).
  - Çözüm için bir çaba, bir mizah ya da duygu anı.
  - Sıcak bir son.
- Diyalog kullan (tırnak içinde). Ses taklitleri ekle (öğrenilmiş harflerle).
- Uzunluk (toplam cümle):
  - ders 11–13: 12–16
  - 14–17: 16–22
  - 18–20: 20–26
  - 21–25: 24–32
  - 26–29: 28–38
- Sahne başına 2–4 cümle; her sahnenin emojisi o sahneyi göstersin (2–4 emoji).
- Hikâyeler birbirinden farklı konularda olsun ve tekrar etmesin.

RESİMLİ HİKÂYE KİTABI ZANAATİ (Barış önceki hikâyeleri "berbat" buldu; bu bölüm en önemlisi):
- Her hikâye gerçek bir resimli çocuk kitabı gibi olsun: her sahne = bir sayfa resim + 2–4 cümle.
- Merak uyandıran başlık ve ilk cümle. Örnek: "Kaan'ın kalemi kayboldu!" gibi bir kanca.
- Üçler kuralı: kahraman sorunu çözmek için üç kez dener. İlk ikisi komik ya da beklenmedik biçimde olmaz, üçüncüsü olur.
- Nakarat: her hikâyede çocukların hep bir ağızdan söyleyeceği, 2–3 kez tekrar eden kısa bir cümle olsun. Örnek: "Nerede, nerede, Lokum nerede?"
- Bir sürpriz ya da gülümseten an mutlaka olsun.
- Sıcak son olsun. Hikâyede küçük bir değer bulunsun (paylaşmak, sabır, yardımlaşma, özür dilemek, sevgi), ama ders verir gibi değil, hissettirerek.
- Karakterlerin kişiliği:
  - Ela meraklı ve soru sorar.
  - Kaan aceleci ve şakacıdır.
  - Nine bilge, sakin ve espriseverdir.
  - Lokum yaramaz, meraklı bir yavru kedidir ("Miyav!").
- Duyguları göster: sevindi, şaştı, güldü, telaşlandı. Ses taklitleri kullan: Pıt pıt! Tık tık! Hav! Şıp şıp!
- "dedi" tekrarından kaçın; diyaloğu tırnakla ve canlı yaz.
- Harf kısıtı yüzünden anlamsız, yapay ya da bozuk Türkçe cümle KURMA. Kelime izinli değilse cümleyi baştan kur. Doğal, akıcı Türkçe şart.
- Konular birbirinden farklı olsun. Çocuğun günlük hayatından seç: kayıp eşya, yeni arkadaş, pazar alışverişi, yağmurda şemsiye, kek yapımı, bahçeye fide dikmek, hasta kuşa yardım, doğum günü sürprizi, karda kardan adam, deniz kenarı, okulda gösteri.
- Sorular: 3–4 soru olsun. Biri olay, biri duygu ("Sen olsan ne yapardın?"), biri tahmin sorusu.
