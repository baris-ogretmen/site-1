# Firestore'daki herkese açık içerikleri okuyup veri/icerik-yedek.json'a yazar (GitHub Actions'ta çalışır).
import json, urllib.request, urllib.parse, os
P = "shaped-totem-481514-c5"
KEY = "AIzaSyAqeO-yQyQPnLsOqKmSNvVH23WPvneIjaU"
BASE = f"https://firestore.googleapis.com/v1/projects/{P}/databases/(default)/documents"
KOL = ["projeler", "videolar", "kitaplar", "yazilar", "kaynaklar", "site_ayarlari", "duyurular", "tavsiyeler"]

def coz(v):
    if "stringValue" in v: return v["stringValue"]
    if "integerValue" in v: return int(v["integerValue"])
    if "doubleValue" in v: return v["doubleValue"]
    if "booleanValue" in v: return v["booleanValue"]
    if "timestampValue" in v: return v["timestampValue"]
    if "nullValue" in v: return None
    if "arrayValue" in v: return [coz(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v: return {k: coz(x) for k, x in v["mapValue"].get("fields", {}).items()}
    return str(v)

out = {}
for k in KOL:
    out[k] = {}
    tok = ""
    while True:
        q = {"key": KEY, "pageSize": 300}
        if tok: q["pageToken"] = tok
        try:
            with urllib.request.urlopen(f"{BASE}/{k}?" + urllib.parse.urlencode(q), timeout=60) as r:
                d = json.load(r)
        except Exception as e:
            out[k]["_hata"] = str(e); break
        for doc in d.get("documents", []):
            out[k][doc["name"].split("/")[-1]] = {f: coz(v) for f, v in doc.get("fields", {}).items()}
        tok = d.get("nextPageToken")
        if not tok: break
os.makedirs("veri", exist_ok=True)
with open("veri/icerik-yedek.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
print({k: len(v) for k, v in out.items()})
