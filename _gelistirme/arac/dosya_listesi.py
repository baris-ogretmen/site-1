# Depodaki kullanıcıya dönük dosyaların ilk yüklenme ve son güncellenme zamanları → veri/dosya-listesi.json
# (GitHub Actions'ta tam geçmişle çalışır; panelde "📁 Yüklenen Dosyalar" bu listeyi okur.)
import subprocess, json, os
UZ = ('.html', '.pdf', '.mp4', '.mp3', '.png', '.jpg', '.jpeg', '.webp')
HARIC = ('sayfa/', 'veri/', '_gelistirme/', '.github/', 'gorseller/', 'node_modules/')
out = subprocess.run(['git', 'log', '--format=@%ct', '--name-only', '--diff-filter=AM', '--no-renames'], capture_output=True, text=True).stdout
ilk, son = {}, {}
t = None
for line in out.splitlines():
    if line.startswith('@'): t = int(line[1:]); continue
    p = line.strip()
    if not p: continue
    if p not in son: son[p] = t           # log yeniden eskiye: ilk görülen = son değişiklik
    ilk[p] = t                              # en son atanan = en eski ekleme
liste = []
for p in sorted(son):
    if not os.path.exists(p) or not p.lower().endswith(UZ) or p.startswith(HARIC): continue
    if p.startswith('google') and p.endswith('.html') and os.path.getsize(p) < 200: continue
    liste.append({'yol': p, 'ilk': ilk[p], 'son': son[p], 'kb': round(os.path.getsize(p) / 1024)})
json.dump({'olusturma': max([x['son'] for x in liste] or [0]), 'dosyalar': liste}, open('veri/dosya-listesi.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(liste), 'dosya')
