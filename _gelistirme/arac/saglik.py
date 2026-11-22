# Sitenin günlük sağlık kontrolü → veri/saglik.json. "acil" varsa sitede/panelde kırmızı uyarı çıkar.
import json, os, re, urllib.parse, datetime, subprocess
S = []  # (seviye, baslik, ayrinti)
def ekle(sev, bas, ayr=""): S.append({"seviye": sev, "baslik": bas, "ayrinti": ayr})
try:
    v = json.load(open("veri/icerik-yedek.json", encoding="utf-8"))
except Exception as e:
    v = {}; ekle("acil", "İçerik veritabanı okunamadı", str(e)[:200])
for k in ["projeler", "videolar", "kitaplar", "yazilar", "kaynaklar"]:
    if "_hata" in v.get(k, {}): ekle("acil", f"'{k}' içerikleri okunamadı", v[k]["_hata"][:200])
def surum(f):
    try: return re.search(r'<meta name="surum" content="([^"]+)"', open(f, encoding="utf-8").read()).group(1)
    except Exception: return None
si, pa = surum("index.html"), surum("yonetici.html")
if not si or not pa: ekle("acil", "index.html ya da yonetici.html bozuk/eksik")
elif si != pa: ekle("acil", f"Site (v{si}) ile panel (v{pa}) sürümü farklı")
if not os.path.exists("google2d4ad73791266272.html"): ekle("acil", "Google doğrulama dosyası silinmiş", "google2d4ad73791266272.html geri yüklenmeli")
if not os.path.exists("sitemap.xml") or "<url>" not in open("sitemap.xml", encoding="utf-8").read(): ekle("acil", "Site haritası (sitemap.xml) bozuk")
for f in ["index.html", "yonetici.html", "kpss-merkezi.html", "ozel-ders.html"]:
    if os.path.exists(f) and os.path.getsize(f) < 2000: ekle("acil", f"{f} neredeyse boş", "yanlışlıkla üzerine yazılmış olabilir")
# Kırık bağlantı / kapak (yalnız yayındaki içerik, yalnız depo içi dosyalar)
kirik, kapaksiz = [], []
def yerel(u):
    if not u or not isinstance(u, str): return None
    if u.startswith("https://baris-ogretmen.github.io/site-1/"): u = u[len("https://baris-ogretmen.github.io/site-1/"):]
    if re.match(r"^[a-z]+:", u, re.I) or u.startswith("//"): return None
    return urllib.parse.unquote(u.split("?")[0].split("#")[0]).lstrip("./") or None
for k in ["projeler", "videolar", "kitaplar", "yazilar", "kaynaklar"]:
    for i, x in v.get(k, {}).items():
        if i.startswith("_") or not isinstance(x, dict) or x.get("arsivlendi") or x.get("silindi") or x.get("yayinDurumu") == "taslak": continue
        p = yerel(x.get("link"))
        if p and not os.path.exists(p): kirik.append(f"{x.get('baslik','?')} → {p}")
        c = yerel(x.get("kapak"))
        if c and not os.path.exists(c): kapaksiz.append(f"{x.get('baslik','?')} → {c}")
if kirik: ekle("uyari", f"{len(kirik)} içeriğin dosyası bulunamadı (açılmaz)", "\n".join(kirik[:30]))
if kapaksiz: ekle("uyari", f"{len(kapaksiz)} içeriğin kapak görseli bulunamadı", "\n".join(kapaksiz[:30]))
try:
    g = json.load(open("veri/google-paketi.json", encoding="utf-8"))
except Exception:
    g = None
if os.environ.get("GOOGLE_HATA"): ekle("acil", "Google sayfaları üretilemedi", os.environ["GOOGLE_HATA"][:300])
durum = "acil" if any(s["seviye"] == "acil" for s in S) else ("uyari" if S else "iyi")
json.dump({"zaman": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "durum": durum, "surum": si,
           "icerik": sum(len([1 for i in v.get(k, {}) if not i.startswith('_')]) for k in ["projeler","videolar","kitaplar","yazilar","kaynaklar"]),
           "google": g, "sorunlar": S}, open("veri/saglik.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(durum, [s["baslik"] for s in S])
