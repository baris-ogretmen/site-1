# Barış Öğretmen Sitesi — Devir Notu (Claude için)

Bu notu okuyan Claude: Barış Öğretmen'in eğitim sitesi ve yönetici paneli üzerinde aylardır birlikte çalışıldı. Aşağıdakiler sistemi bozmadan devam etmen için gereken her şey. **Önce bunu baştan sona oku.**

## 1. Kim, ne istiyor
- **Barış İlkan (Barış Öğretmen):** okul öncesi öğretmeni. Ayrıca anaokulu–8. sınıfta robotik-kodlama, yapay zekâ, satranç ve akıl-zekâ oyunları dersleri veriyor; özel eğitim deneyimi var.
- Telefondan ve dizüstünden çalışıyor; kod bilmiyor ama çok net geri bildirim veriyor. **Türkçe** yaz, sade anlat.
- **Teslim kuralları (ZİRVE):**
  1. Güncellenen/eklenen her şeyin **ekran görüntüsü, koddan ÖNCE** gönderilir.
  2. Her teslimin sonunda sürüm satırı yazılır:
     `📦 Sürüm: vX (önceki vY) · Site N satır/KB → N satır/KB · Panel N satır/KB → N satır/KB`
  3. Dosya adları birebir aynı kalır: `index.html`, `yonetici.html`.
  4. Abartı yok, kanıtsız fayda vaadi yok; sınırlamalar dürüstçe söylenir.
  5. **Hiçbir içerik silinmez** (gizlemek = `arsivlendi`). Mevcut özellikler birebir korunur.
  6. Bağlantı ve adresler tıklanabilir ve kopyalama kutusunda verilir.
  7. Her çalışmaya (oyun, uygulama) ayrı bir **PNG kapak görseli** ve başlık + kısa açıklama verilir.

## 2. Sistem
- **Depo:** `github.com/baris-ogretmen/site-1` (GitHub Pages). Site: `https://baris-ogretmen.github.io/site-1/`
- `index.html` = site; `yonetici.html` = yönetici paneli. Tek dosya HTML'ler, ~600 KB.
- **Firebase (8 compat):** proje `shaped-totem-481514-c5`.
  - Koleksiyonlar: `projeler` (oyunlar), `videolar`, `kitaplar`, `yazilar`, `kaynaklar` (PDF).
  - Alanlar: `site_ayarlari/genel` ve `site_ayarlari/ozel_duyuru` (Acil Buton).
  - Kayıt alanları: `baslik, aciklama, link, kapak, kategoriler[], tarih, arsivlendi`.
- **GitHub bağlantısı:** panel, GitHub token'ı tarayıcıda `localStorage bi_ghToken` olarak tutar; token asla paylaşılmaz.
  - Claude oturumunda GitHub bağlıysa doğrudan `main`'e commit/push yapılır. Barış buna izin verdi ("her şeyi sen yükle").
  - Push öncesi her zaman `git fetch` + `reset --hard origin/main`. Barış başka oturumlardan da yükleme yapıyor.
- **Sürüm:** üç yerde birlikte güncellenir:
  - `<meta name="surum" content="X">` (iki dosyada)
  - site alt bilgisindeki `· vX</span>`
  - panelde `const PANEL_SURUM='X'` ve `SITE_GEREKEN='X'`

  **Sürüm artık TAM SAYI (Barış'ın isteği, 22 Kasım 2026):** 12, 13, 14… Ondalık (11.8 gibi) kullanma; teslim satırında da "v12 (önceki v11)" yaz. Site ve panel her zaman aynı sürümde yüklensin.
- **Son durum (22 Kasım 2026): v12.**
- 22 Kasım eklemeleri: KVKK aydınlatma metni; 🧭 **Öğrenme Yolları** (index.html sonunda `YOL_VARSAYILAN`: rob/sat/akl/yz, 9 basamak = okul öncesi…8. sınıf, `?yol=rob`); **Robi'yi Eğit** (`robiyi-egit.html`, YZ yolunun 9 basamağı, `?kademe=0..8`); ⚡ **hafif mod** (`html.bo-hafif`, telefon/tablet/tahtada otomatik, `localStorage bo_hiz`); kaydırma/izleyici işleri requestAnimationFrame ile birleştirildi.
- Boş basamaklar: Satranç 8–9 ("Oyun Sonu Laboratuvarı", "Maçını İncele"), Akıl-Zekâ 9 ("Kural Dedektifi").
- Barış'a söylenecek riskler kuralı: bulunan her sorunu "Barış, şu sıkıntılı" diye bildir. Firebase kurallarına DOKUNMA (Barış istemedi).

## 3. Çalışma yöntemi (yama)
- Dosyalar elle baştan yazılmaz. Canlı dosya okunur, küçük ve **tam bir kez eşleşen** metin değişiklikleri yapılır. Yeni özellikler `</body>`'den hemen önce ayrı `<script>` / `<style>` bloğu olarak eklenir.
- Mevcut fonksiyonlar "sarmalanarak" genişletilir (ör. `applySettings`, `renderOriginalCollections`, `freshEditor`, `fillEditor`, `previewSpecial`).
- Her `<script>` bloğu `node --check` ile denetlenir.
- **Test:** `_gelistirme/` klasöründeki `mockfb.js` (sahte Firebase) ve `harness.py` (Playwright). Gerçek depo dosyaları sahte verilerle açılır, ekran görüntüleri buradan alınır. GitHub API için testlerde sahte yanıt kullanılır.
- Sitede global olanlar: `allItems, getItem, itemKey, openItem, openModal, closeModal, esc, safeURL, base, settings, applySettings, showArea, areaDefinitions, kapakSrc, thumbOf, videoSource`.
- Panelde global olanlar: `records, keyOf, db, showView, openModal, closeModal, toast, busy, local, SITE_HOME, freshEditor, fillEditor, window.boGH (gh(), repo(), tok())`.
  - **Dikkat:** `loadRepoTree` ve `PANEL_SURUM` panelde global DEĞİL (IIFE içinde).

## 4. v10.6 → v11.4 arasında eklenenler (bunları koru)
- **Acil Buton** (sitede sağ alttaki "EN YENİ" baloncuğu):
  - Görünüm: ikon, alt yazı, 10 şekil, hareketler, boyut, tarih aralığı. Dokununca kapaklı tanıtım penceresi açılır ya da içerik doğrudan açılır.
  - **Otomatik mod** en son içeriği gösterir; bağlantı elle değişince kendiliğinden kapanır, açıkken sarı uyarı çıkar.
  - **Bölüme göre akıllı mod:** Robotik, Akıl Zekâ, Satranç, BİLSEM… ikon, renk ve alt yazı bölümden gelir.
  - 34 hazır şablon üç sekmede: İçerik / Duyuru & sınıf / Özel günler. Özel günlerde tarih otomatik, sarı öneri de çıkar.
  - v11.3'te **sade düzen:** önizleme + "👁 Sitede:" özeti + en fazla 3 öneri + temel alanlar; gerisi kapalı bölümlerde.
  - Video bağlantısında (.mp4) site içinde oynatılır.
- **Panel düzenleyici:**
  - Bağlantı yazılınca başlık, açıklama, etiketler ve kapak **dosyanın içinden otomatik** dolar; dosya yayında değilse GitHub API'den okunur.
  - Sarı **kategori önerileri**, oyun dosyasının içinden de çıkar.
  - **Son yüklenen dosyalar** en üstte; `sayfa/` ve `gorseller/` hariç.
  - Aynı dosya iki kez eklenirse uyarı; kapak çakışması uyarısı.
- **Kapak adları benzersiz** (`-kapak-xxxxx`). Eskiden aynı ad kullanılınca kapaklar birbirinin üzerine yazılıyordu: `gorseller/kapak-kapak.jpg` şu an "Atmaya Devam" kapağı. "hikayem devamı…" videosundan bu kapak kaldırılmalı; Barış'a söylendi.
- **Sitede video kartları:** kendi kapağını gösterir; kapak başka içerikle ortaksa videonun kendi karesi gösterilir.
- **Google paketi (panel):**
  - Her içeriğe ayrı sayfa üretir (`sayfa/*.html`), ayrıca `sitemap.xml` ve bölüm sayfaları (`sayfa/kademe-*.html`).
  - v11.4'te Satranç, Akıl Zekâ ve Özel Eğitim bölüm sayfaları eklendi. Barış'ın panelde "Sayfaları oluştur ve yükle"ye bir kez basması gerekiyor.
  - Eskiden doğrulama dosyası yüklenirken bütün `sayfa/` dosyaları siliniyordu; düzeltildi, artık yalnızca `sitemap.xml` içeren tam pakette eski sayfalar temizlenir.
- **📊 Site Karnesi (panel ana ekranı):** 10 üzerinden puan verir. İçerik bilgileri (açıklama, kapak, kademe, branş), kırık bağlantılar, kapak çakışması, Google doğrulaması, sayfaların güncelliği ve sürüm uyumunu ölçer; tek dokunuşla düzenlemeye götürür.
- **Sitede Google için:** başlık ve açıklama robotik kodlama, yapay zekâ, satranç, akıl zekâ, okul öncesi ve özel eğitim odaklı; alt bilgide JavaScript'siz içerik dizini.

## 5. Google Search Console (22 Kasım 2026)
- Mülk: **URL ön eki** `https://baris-ogretmen.github.io/site-1/`. Doğrulandı (HTML dosyası yöntemi).
- Doğrulama dosyası: `google2d4ad73791266272.html`. **ASLA SİLİNMEZ.**
- `sitemap.xml` gönderildi: 327 adres, XML geçerli, hepsinin dosyası var. İlk durum "Getirilemedi" idi; yeni sitelerde normal.
- Ana sayfa ve `sayfa/index.html` için "Dizine eklenmesini iste" yapıldı.
- Not: `robots.txt` alt klasörde olduğu için Google onu okumaz; zararı yok. "sitemap (1).xml" fazladan bir dosya, zararsız.

## 6. Bekleyen / fikir
- KVKK aydınlatma metnini güçlendirmek: öğrenci adı ve sınıfı toplanıyor.
- Ana sayfayı hızlandırmak: 580 KB tek dosya.
- Öğrencilere yapay zekâyı öğreten bir oyun (anaokulu–8. sınıf kademeli). Sitede şu an böyle bir içerik yok.
- Özel Kasa için Firestore kuralları bekleniyor; alan adı (barisogretmen.com) taşıma daha sonra; Charon sesi baris-kasa üzerinden.

## 7. Uyarılar
- Firestore'a bu ortamdan erişilemiyor (ağ izin listesi). İçerik verisini yalnızca panel okur.
- `baris-ogretmen.github.io` adresine bu ortamın kabuğundan ulaşılamıyor. Testler yerel harness ile yapılır; GitHub API'nin `pages/builds` yolu da kapalı.
- Panelde birden fazla eski yama katmanı var (v10.x). Bir şeyi değiştirmeden önce `grep` ile aynı işi yapan eski kod var mı bak; çift iş olmasın.
