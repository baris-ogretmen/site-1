# Tane Tane Matematik — kitap yazarı ajan talimatı

Barış Öğretmen (okul öncesi öğretmeni, özel eğitim deneyimli) için özgün, renkli, yazdırılabilir bir matematik çalışma seti üretiyoruz.
Hedef: okul öncesi + 1. sınıf + özel gereksinimli çocuklar. Dil: Türkçe. Set adı "Tane Tane Matematik", maskot "Tane" (lib.tane()).

## Altyapı (DEĞİŞTİRME)
- /home/claude/mat/lib.py: Kitap sınıfı ve hazır bileşenler. Mutlaka oku. lib.py'yi DÜZENLEME; ek yardımcı gerekiyorsa kendi dosyanda tanımla.
- Örnek: /home/claude/mat/k1.py (1. Kitap, 1–5). Aynı üslup, düzen, sayfa yoğunluğu ve kalite çizgisini koru.
- Çalıştır: `cd /home/claude/mat && python3 kX.py` → cikti/ içine PDF (+ aynı adlı .html).
- Önizleme: `pdftoppm -r 40 -jpeg -f N -l N dosya.pdf /tmp/x` ile sayfaları görüntüleyip Read aracıyla BAK. En az 8 farklı sayfaya bak; taşan, üst üste binen, boş kalan, okunmayan şey varsa düzelt.

## Pedagojik kurallar (KESİN)
1. Somut → Resim → Sembol sırası. Her yeni kavram önce nesne/resimle, sonra rakam/işaretle.
2. Okul öncesi düzeyindeki (Kitap 2 ve 4) çoktan seçmeli sorularda HER ZAMAN YALNIZ 2 SEÇENEK (lib.iki_secenek). Kitap 3 (1. sınıf) yazarak cevaplama ağırlıklı olabilir.
3. Sayfa başına az öğe (özel gereksinim): genelde 1 ana görev ya da en fazla 3–4 kutu. Büyük yazı, büyük nesneler.
4. Her ders aynı düzende ilerlesin (öngörülebilirlik). Yönerge kısa; altında küçük yazıyla yetişkin için ipucu (alt_yonerge) ya da .not kutusu.
5. MATEMATİK %100 DOĞRU: her sayıyı, toplamı, farkı, sayılan nesne adedini kodda üret ve assert ile doğrula. Görselde gösterilen nesne sayısı = sorunun cevabı. Yanlış seçenek doğruya eşit olamaz.
6. Abartılı iddia yok ("garanti", "kesin öğrenir" yok). Yöntem açıklamalarında "araştırmalarla desteklenen yaklaşım" gibi ölçülü dil.
7. Özgün içerik: başka kitaptan metin/karakter yok; bilinen çizgi film karakteri yok. Emojiler ve lib içindeki SVG'ler kullanılabilir.
8. Kültürel olarak nötr, şiddetsiz, çocuğa uygun nesneler (lib.NESNE listesi). Hikâye problemlerinde Türkçe isimler (Ela, Ali, Zeynep, Kerem, Defne, Emir, Nehir, Can...). Gerçek öğrenci adı yok.
9. Sitedeki dijital oyunlara QR: k.sayfa(..., oyun=(baslik, dosya)). Kullanılabilir dosyalar:
   - ("Sihirli Parmaklar · 1'den 10'a", 'sihirlii parmaklar.html')
   - ('MatAkış — Gör, Dokun, Oyna', 'matakis.html')
   - ('Minik Kâşifler', 'minik kasiflerr.html')
   - ('Kum Tüneli', 'kumm tuneliii.html')
   - ('Küp Yolu · Işık Hattı', 'kup yoluu.html')
   - ('Zekâ Mega Paket', 'kup yoluu.html') değil — yalnız yukarıdakileri kullan.
   Her kitapta 4–6 sayfada, konuya uyan oyun.
10. Her kitap: k.kapak(...) ile başla, 2. sayfa "Aileler ve öğretmenler için" (bu kitapta ne var, nasıl kullanılır, özel gereksinim uyarlaması), sonda k.basardim(...).
11. Sayfa sayısı hedefi kitabın talimatında. Tekrara düşmeden çeşit yap (farklı nesneler, farklı düzenler), ama aynı ders yapısını koru.

## Bitince
Kısa rapor: dosya yolu, sayfa sayısı, bölüm listesi, bildiğin eksikler. Uzun açıklama yazma.
