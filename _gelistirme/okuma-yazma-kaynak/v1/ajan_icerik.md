GÖREV: "Adım Adım Okuma–Yazma Seti" (Barış Öğretmen) için ders içeriği yazmak. Hedef kitle: ilk okuma-yazma öğrenen çocuklar, ÖZELLİKLE özel gereksinimli çocuklar (somut, kısa, sıcak, tekrarlı, günlük hayattan).

Harf sırası ve sesler: /home/claude/aa/sira.json (ders n = sıradaki n. harf; o derste yalnızca 1..n harfleri kullanılabilir). Denetim aracı: `python3 /home/claude/aa/dogrula.py <dosya>` — HATA: 0 olana kadar düzelt. Bu araç geçmeden teslim etme.

TELİF (ÇOK ÖNEMLİ): Bu içerik tamamen ÖZGÜN olmalı. Hiçbir yayınlanmış okuma-yazma kitabından (Basara dahil) kelime listesi, cümle, hikâye kopyalama; onları açma/okuma. Hece ve tek tek yaygın Türkçe kelimeler herkesindir ama cümleler ve hikâyeler senin kendi yazdığın olsun. "Basara" kelimesini hiçbir yerde kullanma.

İÇERİK KURALLARI:
- Doğal, gerçek Türkçe kelimeler ve anlamlı cümleler (anlamsız hece dizileri cümle sayılmaz). Türkçe yazım ve noktalama kurallarına uy. Cümle başı büyük harf; büyük harf de yalnızca öğrenilmiş harflerden olur (araç bunu denetler).
- Çocuğa ve veliye uygun, şiddetsiz, korkutucu değil; "savaş" kelimesi asla. Sevgi, aile, oyun, doğa, hayvanlar, okul, yardımlaşma temaları. Dinî/siyasi içerik yok. Gerçek kişi adı yok (masal kişisi adları öğrenilmiş harflerle uydurulabilir: Ela, Ali, Mete değil — Mete gerçek öğrenci adı, KULLANMA; ayrıca Enes, Beyazıt da kullanma).
- Her ders JSON nesnesi:
  {"ders":n,"harf":"x","resimli_kelime":{"kelime":"...","emoji":"🍎"},
   "heceler":[...6-12 hece, yeni harfle oluşturulan açık/kapalı heceler],
   "kelimeler":[...8-12 kelime, çoğu YENİ harfi içersin, kısa-uzun karışık],
   "cumleler":[...4-6 kısa cümle, 2-5 kelime],
   "hikaye":{"baslik":"...","cumleler":[...5-8 cümle, küçük bir olay örgüsü],"sorular":[{"soru":"(öğretmen okur, serbest)","cevap":"(yalnız öğrenilmiş harflerle, kısa)"}, ... 2-3 soru]}}
  Resimli kelime: yeni harfi içeren, emojiyle gösterilebilen somut bir kelime (emoji gerçekten o şeyi göstermeli; yoksa en yakın somut kelimeyi seç).
- İlk derslerde (1–3) harf az olduğu için içerik doğal olarak kısa olabilir: ders 1 (yalnız "a") için hece/kelime: "a", "aa"; ders 2: "al", "la", "ala", "lala"; ders 3: "mama", "ama", "lama", "alam" gibi. Ders 1–3'te hikaye alanı null olabilir; ders 4'ten itibaren hikâye zorunlu. Cümle yazılamıyorsa "cumleler" 1–2 öğeyle olabilir.
- Kelimeler gerçekten Türkçe olsun (TDK sözlüğünde olan ya da çok yaygın kullanım). Emin olmadığın kelimeyi kullanma.
ÇIKTI: Bir JSON dizi (ders sırasıyla) → /home/claude/aa/{DOSYA}. UTF-8, ensure_ascii=False, indent=1. Sonunda dogrula.py çıktısını ve 2 örnek dersi kısaca raporla (Türkçe). Başka dosyaya dokunma, git çalıştırma.
