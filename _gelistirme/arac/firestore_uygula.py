# veri/claude-istekleri.json içindeki henüz uygulanmamış istekleri Firestore'a işler.
# Kural: ASLA silme yok. Yalnız alan güncelleme ("guncelle") ve yeni kayıt ("ekle").
# Her güncellemeden önce eski değerler veri/claude-istekleri-uygulanan.json'a yazılır (geri alınabilir).
import json, os, urllib.request, urllib.parse, datetime
P = "shaped-totem-481514-c5"; KEY = "AIzaSyAqeO-yQyQPnLsOqKmSNvVH23WPvneIjaU"
BASE = f"https://firestore.googleapis.com/v1/projects/{P}/databases/(default)/documents"
IZINLI = {"projeler", "videolar", "kitaplar", "yazilar", "kaynaklar", "site_ayarlari"}
SIMDI = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def kodla(v):
    if isinstance(v, dict) and "__zaman__" in v:  # "simdi" ya da ISO zaman (ör. 2026-11-22T14:30:03Z)
        return {"timestampValue": SIMDI if v["__zaman__"] == "simdi" else v["__zaman__"]}
    if v is None: return {"nullValue": None}
    if isinstance(v, bool): return {"booleanValue": v}
    if isinstance(v, int): return {"integerValue": str(v)}
    if isinstance(v, float): return {"doubleValue": v}
    if isinstance(v, list): return {"arrayValue": {"values": [kodla(x) for x in v]}}
    if isinstance(v, dict): return {"mapValue": {"fields": {k: kodla(x) for k, x in v.items()}}}
    return {"stringValue": str(v)}

def coz(v):
    for t in ("stringValue", "booleanValue", "doubleValue", "timestampValue"):
        if t in v: return v[t]
    if "integerValue" in v: return int(v["integerValue"])
    if "nullValue" in v: return None
    if "arrayValue" in v: return [coz(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v: return {k: coz(x) for k, x in v["mapValue"].get("fields", {}).items()}
    return None

def istek(url, yontem="GET", govde=None):
    req = urllib.request.Request(url, method=yontem, data=json.dumps(govde).encode() if govde is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)

IST = "veri/claude-istekleri.json"; UYG = "veri/claude-istekleri-uygulanan.json"
if not os.path.exists(IST): print("istek yok"); raise SystemExit
istekler = json.load(open(IST, encoding="utf-8")).get("istekler", [])
uyg = json.load(open(UYG, encoding="utf-8")) if os.path.exists(UYG) else {}
for s in istekler:
    sid = s["id"]
    if sid in uyg and uyg[sid].get("durum") == "tamam": continue
    kol, belge, alanlar, tur = s["koleksiyon"], s.get("belge"), s.get("alanlar", {}), s.get("tur", "guncelle")
    kayit = {"zaman": SIMDI, "not": s.get("not", "")}
    try:
        if kol not in IZINLI: raise ValueError("izinsiz koleksiyon")
        if tur == "guncelle":
            eski = istek(f"{BASE}/{kol}/{belge}?key={KEY}")
            ef = eski.get("fields", {})
            kayit["eski"] = {k: (coz(ef[k]) if k in ef else "__yoktu__") for k in alanlar}
            q = [("key", KEY), ("currentDocument.exists", "true")] + [("updateMask.fieldPaths", k) for k in alanlar]
            istek(f"{BASE}/{kol}/{belge}?" + urllib.parse.urlencode(q), "PATCH", {"fields": {k: kodla(v) for k, v in alanlar.items()}})
        elif tur == "ekle":
            q = [("key", KEY)] + ([("documentId", belge)] if belge else [])
            r = istek(f"{BASE}/{kol}?" + urllib.parse.urlencode(q), "POST", {"fields": {k: kodla(v) for k, v in alanlar.items()}})
            kayit["belge"] = r["name"].split("/")[-1]
        else: raise ValueError("bilinmeyen tür (silme yapılmaz)")
        kayit["durum"] = "tamam"
    except Exception as e:
        kayit["durum"] = "hata"; kayit["hata"] = str(e)[:300]
    uyg[sid] = kayit; print(sid, kayit["durum"], kayit.get("hata", ""))
json.dump(uyg, open(UYG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
