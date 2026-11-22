# -*- coding: utf-8 -*-
"""Tane Tane Matematik — ortak sayfa kütüphanesi (HTML → PDF, A4 dikey).
Her kitap: Kitap(...) oluştur, k.sayfa(...) ile sayfa ekle, k.pdf(yol) ile çıkar.
Kurallar: okul öncesi çoktan seçmeli = HER ZAMAN 2 seçenek; sayfa başına az öğe; büyük yazı;
sayılar her zaman doğru (assert'ler); özgün içerik; telifli karakter yok."""
import html, math, random, os, asyncio
from reportlab.graphics.barcode import qrencoder as _q

SITE = 'https://baris-ogretmen.github.io/site-1/'
SET_SAYFA = SITE + 'tane-tane-matematik.html'
ADRES = 'baris-ogretmen.github.io/site-1'
E = html.escape

# ---------- renkler / temalar ----------
TEMA = {
    'k1': ('#16a34a', '#dcfce7', '#14532d'),   # yeşil
    'k2': ('#2563eb', '#dbeafe', '#1e3a8a'),   # mavi
    'k3': ('#ea580c', '#ffedd5', '#7c2d12'),   # turuncu
    'k4': ('#9333ea', '#f3e8ff', '#581c87'),   # mor
    'kes': ('#0891b2', '#cffafe', '#164e63'),  # camgöbeği
    'reh': ('#db2777', '#fce7f3', '#831843'),  # pembe
}
RAKAM_AD = ['sıfır', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz', 'on',
            'on bir', 'on iki', 'on üç', 'on dört', 'on beş', 'on altı', 'on yedi', 'on sekiz', 'on dokuz', 'yirmi']
# sayılabilir, kültüre uygun, net emojiler (ad, emoji)
NESNE = [('elma', '🍎'), ('armut', '🍐'), ('çilek', '🍓'), ('balon', '🎈'), ('yıldız', '⭐'), ('balık', '🐟'), ('kelebek', '🦋'),
         ('çiçek', '🌼'), ('top', '⚽'), ('araba', '🚗'), ('ördek', '🦆'), ('mantar', '🍄'), ('havuç', '🥕'), ('kalp', '❤️'),
         ('yaprak', '🍁'), ('salyangoz', '🐌'), ('ayıcık', '🧸'), ('kalem', '✏️'), ('portakal', '🍊'), ('civciv', '🐥'),
         ('arı', '🐝'), ('uğur böceği', '🐞'), ('kurbağa', '🐸'), ('tavşan', '🐰'), ('kek', '🧁'), ('muz', '🍌')]

# ---------- QR (SVG) ----------
def qr_svg(url, px=110, renk='#0f172a'):
    for v in range(2, 15):
        try:
            c = _q.QRCode(v, _q.QRErrorCorrectLevel.M); c.addData(url); c.make(); break
        except Exception:
            continue
    n = c.getModuleCount(); q = 2; tot = n + 2 * q
    rects = ''.join(f'<rect x="{x+q}" y="{y+q}" width="1.02" height="1.02"/>' for y in range(n) for x in range(n) if c.isDark(y, x))
    return f'<svg viewBox="0 0 {tot} {tot}" width="{px}" height="{px}" shape-rendering="crispEdges"><rect width="{tot}" height="{tot}" fill="#fff"/><g fill="{renk}">{rects}</g></svg>'

# ---------- maskot: Tane (özgün, yeşil tohum karakteri) ----------
def tane(px=120, ruh='mutlu', el=False):
    agiz = {'mutlu': '<path d="M38 62 Q50 74 62 62" stroke="#14532d" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'saskin': '<ellipse cx="50" cy="66" rx="6" ry="7" fill="#14532d"/>',
            'dusun': '<path d="M40 66 L60 64" stroke="#14532d" stroke-width="4" stroke-linecap="round"/>'}[ruh]
    kol = '<path d="M84 60 Q100 46 96 30" stroke="#16a34a" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="96" cy="28" r="6" fill="#22c55e"/>' if el else ''
    return f'''<svg viewBox="0 0 110 120" width="{px}" height="{px*120/110:.0f}">
<path d="M52 18 Q50 4 62 2 Q66 14 54 20" fill="#22c55e"/><path d="M52 18 Q40 6 30 12 Q38 22 52 20" fill="#4ade80"/>
<ellipse cx="52" cy="66" rx="38" ry="44" fill="#86efac" stroke="#16a34a" stroke-width="5"/>
<ellipse cx="40" cy="54" rx="6" ry="8" fill="#14532d"/><ellipse cx="64" cy="54" rx="6" ry="8" fill="#14532d"/>
<circle cx="42" cy="51" r="2.2" fill="#fff"/><circle cx="66" cy="51" r="2.2" fill="#fff"/>
<ellipse cx="30" cy="68" rx="6" ry="4" fill="#fda4af"/><ellipse cx="74" cy="68" rx="6" ry="4" fill="#fda4af"/>{agiz}{kol}
<ellipse cx="38" cy="108" rx="10" ry="5" fill="#16a34a"/><ellipse cx="66" cy="108" rx="10" ry="5" fill="#16a34a"/></svg>'''

# ---------- nokta kalıpları (anında tanıma / zar düzeni) ----------
ZAR = {1: [(.5, .5)], 2: [(.28, .28), (.72, .72)], 3: [(.25, .25), (.5, .5), (.75, .75)], 4: [(.28, .28), (.72, .28), (.28, .72), (.72, .72)],
       5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)], 6: [(.28, .2), (.72, .2), (.28, .5), (.72, .5), (.28, .8), (.72, .8)]}
def nokta_karti(n, px=150, renk='#ef4444', zemin='#fff', cerceve='#0f172a'):
    """1–10 arası nokta kartı. 6'dan büyükler 5 + kalan şeklinde iki zar (sayı hissi)."""
    assert 0 <= n <= 10
    def zar(k, x0, w):
        if k == 0: return ''
        pts = ZAR[k] if k <= 6 else []
        r = w * .1
        return ''.join(f'<circle cx="{x0 + x * w:.1f}" cy="{y * w:.1f}" r="{r:.1f}" fill="{renk}"/>' for x, y in pts)
    if n <= 6:
        return f'<svg viewBox="0 0 100 100" width="{px}" height="{px}"><rect x="2" y="2" width="96" height="96" rx="16" fill="{zemin}" stroke="{cerceve}" stroke-width="3"/>{zar(n, 0, 100)}</svg>'
    return (f'<svg viewBox="0 0 204 100" width="{px*2.04:.0f}" height="{px}"><rect x="2" y="2" width="96" height="96" rx="16" fill="{zemin}" stroke="{cerceve}" stroke-width="3"/>'
            f'<rect x="106" y="2" width="96" height="96" rx="16" fill="{zemin}" stroke="{cerceve}" stroke-width="3"/>{zar(5, 0, 100)}{zar(n - 5, 104, 100)}</svg>')

# ---------- beşlik / onluk çerçeve ----------
def cerceve(n_dolu=0, boyut=5, px=70, renk='#ef4444', ikinci=0, ikinci_renk='#3b82f6', bos_isaret=False):
    """boyut 5 veya 10 (2x5). n_dolu kırmızı sayaç, ardından 'ikinci' mavi sayaç (toplama için)."""
    assert boyut in (5, 10) and n_dolu + ikinci <= boyut
    sat = 1 if boyut == 5 else 2; s = 5
    h = []
    for i in range(boyut):
        r, c = divmod(i, 5); x = c * px; y = r * px
        h.append(f'<rect x="{x+2}" y="{y+2}" width="{px-4}" height="{px-4}" rx="8" fill="#fff" stroke="#0f172a" stroke-width="3"/>')
        if i < n_dolu: h.append(f'<circle cx="{x+px/2}" cy="{y+px/2}" r="{px*.32:.1f}" fill="{renk}"/>')
        elif i < n_dolu + ikinci: h.append(f'<circle cx="{x+px/2}" cy="{y+px/2}" r="{px*.32:.1f}" fill="{ikinci_renk}"/>')
        elif bos_isaret: h.append(f'<circle cx="{x+px/2}" cy="{y+px/2}" r="{px*.32:.1f}" fill="none" stroke="#cbd5e1" stroke-width="3" stroke-dasharray="6 6"/>')
    return f'<svg viewBox="0 0 {5*px} {sat*px}" width="{5*px}" height="{sat*px}">{"".join(h)}</svg>'

# ---------- nesne dizimi ----------
def nesneler(emoji, n, boy=54, sutun=None, duzen='izgara'):
    """n nesne; 'zar' düzeni n<=6 için anında tanımayı destekler."""
    if n == 0: return '<div class="nes bos">—</div>'
    if duzen == 'zar' and n <= 6:
        w = boy * 3.2
        it = ''.join(f'<span style="position:absolute;left:{x*w-boy/2:.0f}px;top:{y*w-boy/2:.0f}px;font-size:{boy}px;line-height:1">{emoji}</span>' for x, y in ZAR[n])
        return f'<div class="nes" style="position:relative;width:{w:.0f}px;height:{w:.0f}px">{it}</div>'
    sutun = sutun or (n if n <= 5 else 5)
    return f'<div class="nes" style="display:grid;grid-template-columns:repeat({sutun},{boy*1.25:.0f}px);font-size:{boy}px;line-height:1.2;justify-content:center">' + ''.join(f'<span>{emoji}</span>' for _ in range(n)) + '</div>'

# ---------- seçenek daireleri ----------
def secenek(liste, dogru, boy=64, renk='#0f172a'):
    """Çocuğun daire içine alacağı seçenekler. dogru listede olmalı."""
    assert dogru in liste, (liste, dogru)
    return '<div class="sec">' + ''.join(f'<span class="secc" style="font-size:{boy}px">{E(str(x))}</span>' for x in liste) + '</div>'

def iki_secenek(dogru, yanlis, seed=0):
    assert dogru != yanlis
    return [dogru, yanlis] if (seed % 2 == 0) else [yanlis, dogru]

# ---------- rakam izleme ----------
def rakam_izle(d, px=300, renk='#16a34a', tekrar=5):
    """Büyük içi boş rakam (izleme) + başlangıç noktası + noktalı tekrar satırı."""
    s = str(d)
    buyuk = (f'<svg viewBox="0 0 {120*len(s)} 160" width="{px*len(s)*.75:.0f}" height="{px:.0f}">'
             f'<text x="{60*len(s)}" y="138" text-anchor="middle" font-family="Inter" font-weight="800" font-size="160" '
             f'fill="none" stroke="{renk}" stroke-width="3" stroke-dasharray="10 7" stroke-linejoin="round" style="font-feature-settings:\'cv11\',\'cv01\'">{E(s)}</text></svg>')
    kucuk = ''.join(f'<svg viewBox="0 0 {80*len(s)} 100" width="{60*len(s)}" height="78"><text x="{40*len(s)}" y="86" text-anchor="middle" font-family="Inter" font-weight="700" font-size="100" fill="{"#cbd5e1" if i else "#0f172a"}" style="font-feature-settings:\'cv01\'">{E(s)}</text></svg>' for i in range(tekrar))
    return f'<div class="izle">{buyuk}</div><div class="izsat">{kucuk}<span class="bossat"></span></div>'

# ---------- sayı doğrusu ----------
def sayi_dogrusu(bas=0, son=10, isaret=None, bos=None, atla=None, w=900):
    """isaret: vurgulanan sayılar; bos: yerine boş kutu konan sayılar; atla: (baslangic, adimlar) yay okları."""
    bos = set(bos or []); isaret = set(isaret or []); n = son - bas; step = (w - 60) / n
    x = lambda v: 30 + (v - bas) * step
    h = [f'<line x1="10" y1="80" x2="{w-10}" y2="80" stroke="#0f172a" stroke-width="4"/>',
         f'<polygon points="{w-10},80 {w-24},72 {w-24},88" fill="#0f172a"/>']
    for v in range(bas, son + 1):
        h.append(f'<line x1="{x(v):.1f}" y1="68" x2="{x(v):.1f}" y2="92" stroke="#0f172a" stroke-width="4"/>')
        if v in bos: h.append(f'<rect x="{x(v)-20:.1f}" y="102" width="40" height="44" rx="8" fill="#fff" stroke="#ea580c" stroke-width="3"/>')
        else:
            c = '#dc2626' if v in isaret else '#0f172a'
            h.append(f'<text x="{x(v):.1f}" y="136" text-anchor="middle" font-family="Inter" font-weight="800" font-size="{34 if n<=10 else 24}" fill="{c}">{v}</text>')
    if atla:
        b, ad = atla
        for i in range(abs(ad)):
            a1 = b + (i if ad > 0 else -i); a2 = a1 + (1 if ad > 0 else -1)
            h.append(f'<path d="M{x(a1):.1f} 64 Q{(x(a1)+x(a2))/2:.1f} 14 {x(a2):.1f} 64" stroke="#2563eb" stroke-width="4" fill="none"/>')
            h.append(f'<circle cx="{x(a2):.1f}" cy="64" r="6" fill="#2563eb"/>')
    return f'<svg viewBox="0 0 {w} 160" width="{w}" height="160">{"".join(h)}</svg>'

# ---------- sayı bağı (parça–bütün) ----------
def sayi_bagi(butun, p1, p2, gizle=None, px=320, renk='#ea580c'):
    """gizle: 'butun' | 'p1' | 'p2' | None"""
    assert butun == p1 + p2
    def daire(cx, cy, r, v, gz):
        t = '' if gz else f'<text x="{cx}" y="{cy+r*.36:.0f}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="{r*1.0:.0f}" fill="#0f172a">{v}</text>'
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{renk}" stroke-width="6"/>{t}'
    return (f'<svg viewBox="0 0 320 300" width="{px}" height="{px*300/320:.0f}"><line x1="160" y1="80" x2="70" y2="215" stroke="{renk}" stroke-width="6"/>'
            f'<line x1="160" y1="80" x2="250" y2="215" stroke="{renk}" stroke-width="6"/>' + daire(160, 75, 62, butun, gizle == 'butun') + daire(70, 220, 55, p1, gizle == 'p1') + daire(250, 220, 55, p2, gizle == 'p2') + '</svg>')

# ---------- şekiller ----------
def sekil(ad, px=120, renk='#9333ea', dolu=True, kalin=6):
    f = renk if dolu else '#fff'; s = f'stroke="#0f172a" stroke-width="{kalin}" fill="{f}"'
    g = {'daire': f'<circle cx="50" cy="50" r="42" {s}/>', 'kare': f'<rect x="10" y="10" width="80" height="80" {s}/>',
         'üçgen': f'<polygon points="50,8 92,90 8,90" {s} stroke-linejoin="round"/>', 'dikdörtgen': f'<rect x="4" y="25" width="92" height="50" {s}/>',
         'yıldız': f'<polygon points="50,6 61,38 95,38 67,58 78,92 50,72 22,92 33,58 5,38 39,38" {s} stroke-linejoin="round"/>',
         'kalp': f'<path d="M50 88 C10 60 6 30 26 18 C40 10 50 22 50 30 C50 22 60 10 74 18 C94 30 90 60 50 88Z" {s}/>',
         'altıgen': f'<polygon points="27,8 73,8 96,50 73,92 27,92 4,50" {s}/>', 'oval': f'<ellipse cx="50" cy="50" rx="46" ry="30" {s}/>'}[ad]
    return f'<svg viewBox="0 0 100 100" width="{px}" height="{px}">{g}</svg>'

# ---------- sayfa iskeleti ----------
CSS = r'''
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;font-family:Inter,'Noto Color Emoji',sans-serif;font-feature-settings:'cv11','cv01';color:#0f172a}
.pg{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff;padding:14mm 14mm 22mm}
.pg:last-child{page-break-after:auto}
.ust{display:flex;align-items:center;gap:12px;border-radius:18px;padding:10px 16px;color:#fff;font-weight:800;font-size:19px}
.ust .no{background:#fff;border-radius:50%;width:42px;height:42px;display:grid;place-items:center;font-size:22px;font-weight:900}
.ust .kit{margin-left:auto;font-size:12px;font-weight:700;opacity:.9}
.yon{font-size:23px;font-weight:700;margin:14px 2px 6px;line-height:1.35}
.yon small{display:block;font-size:13px;font-weight:600;color:#64748b;margin-top:2px}
.alt{position:absolute;left:14mm;right:14mm;bottom:8mm;display:flex;align-items:center;gap:10px;font-size:10.5px;color:#64748b;border-top:1.5px solid #e2e8f0;padding-top:6px}
.alt b{color:#0f172a}.alt .sn{margin-left:auto}
.kutu{border:3px solid #e2e8f0;border-radius:22px;padding:18px;margin:12px 0;min-height:215px;display:flex;align-items:center;gap:18px;justify-content:space-around}
.sec{display:flex;gap:26px;justify-content:center}
.secc{display:inline-grid;place-items:center;min-width:1.45em;height:1.45em;border:4px dashed #94a3b8;border-radius:50%;font-weight:900;padding:0 .15em}
.izle{display:flex;justify-content:center;margin-top:6px}
.izsat{display:flex;gap:6px;align-items:flex-end;border-bottom:3px solid #94a3b8;margin:6px 0 14px;padding-bottom:2px}
.bossat{flex:1}
.cizgi{border-bottom:3px solid #94a3b8;height:62px;margin:6px 0}
.rozet{display:inline-block;border-radius:999px;padding:6px 14px;font-weight:800;font-size:14px;color:#fff}
.oyun{position:absolute;right:14mm;bottom:24mm;display:flex;align-items:center;gap:10px;background:#f8fafc;border:2px solid #e2e8f0;border-radius:16px;padding:8px 12px;font-size:12px;font-weight:700;max-width:320px}
.not{font-size:12.5px;color:#475569;background:#f8fafc;border-left:5px solid #cbd5e1;border-radius:8px;padding:8px 12px;margin-top:10px}
.buyuk{font-size:150px;font-weight:900;line-height:1}
.tbl{width:100%;border-collapse:collapse;font-size:13px}.tbl td,.tbl th{border:1.5px solid #cbd5e1;padding:6px 8px;text-align:left}.tbl th{background:#f1f5f9}
.kes{border:3px dashed #94a3b8;border-radius:12px}
'''

class Kitap:
    def __init__(s, kod, ad, alt, kitap_etiket, seviye):
        s.kod, s.ad, s.alt, s.etiket, s.seviye = kod, ad, alt, kitap_etiket, seviye
        s.renk, s.acik, s.koyu = TEMA[kod]
        s.sayfalar = []  # (tur, html)
        s.qr = qr_svg(SET_SAYFA, 54)

    def sayfa(s, govde, baslik=None, no=None, yonerge=None, alt_yonerge=None, oyun=None, zemin='#fff', ham=False):
        """oyun=(baslik, dosya) → sitedeki ilgili dijital oyuna QR."""
        h = []
        if not ham:
            if baslik:
                h.append(f'<div class="ust" style="background:{s.renk}">' + (f'<span class="no" style="color:{s.renk}">{E(str(no))}</span>' if no is not None else '') +
                         f'<span>{E(baslik)}</span><span class="kit">Tane Tane Matematik · {E(s.etiket)}</span></div>')
            if yonerge:
                h.append(f'<div class="yon">{yonerge}' + (f'<small>{alt_yonerge}</small>' if alt_yonerge else '') + '</div>')
        h.append(govde)
        if oyun:
            ob, dosya = oyun
            h.append(f'<div class="oyun">{qr_svg(SITE + dosya.replace(" ", "%20"), 62)}<div>Bu konunun dijital oyunu:<br><span style="color:{s.renk}">{E(ob)}</span></div></div>')
        s.sayfalar.append((zemin, ham, ''.join(h)))

    def html(s):
        N = len(s.sayfalar); out = []
        for i, (zemin, ham, g) in enumerate(s.sayfalar, 1):
            alt = '' if ham else (f'<div class="alt">{s.qr}<span>★ <b>Barış Öğretmen</b> tarafından hazırlanmıştır · {ADRES}</span>'
                                  f'<span class="sn">{E(s.ad)} · Sayfa {i}/{N}</span></div>')
            out.append(f'<section class="pg" style="background:{zemin}">{g}{alt}</section>')
        return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{E(s.ad)}</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>'

    def pdf(s, yol):
        h = s.html(); hp = yol.replace('.pdf', '.html'); open(hp, 'w', encoding='utf-8').write(h)
        async def go():
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                b = await p.chromium.launch(); pg = await b.new_page()
                await pg.goto('file://' + os.path.abspath(hp)); await pg.wait_for_timeout(500)
                await pg.pdf(path=yol, format='A4', print_background=True, prefer_css_page_size=True)
                await b.close()
        asyncio.run(go())
        return len(s.sayfalar)

    # ---- hazır sayfalar ----
    def kapak(s, aciklama, harfler_html=''):
        g = f'''<div style="position:absolute;inset:0;background:linear-gradient(160deg,{s.acik},#fff 55%,{s.acik})"></div>
<div style="position:relative;text-align:center;padding-top:18mm">
<div class="rozet" style="background:{s.renk};font-size:18px">Barış Öğretmen · Tane Tane Matematik</div>
<div style="font-size:64px;font-weight:900;color:{s.koyu};line-height:1.05;margin-top:18mm">{E(s.ad)}</div>
<div style="font-size:26px;font-weight:700;color:{s.renk};margin-top:8px">{E(s.alt)}</div>
<div style="margin:14mm auto 6mm;display:flex;justify-content:center;align-items:flex-end;gap:18px">{tane(150, 'mutlu', True)}{harfler_html}</div>
<div style="font-size:19px;color:#334155;max-width:150mm;margin:0 auto;line-height:1.5">{aciklama}</div>
<div style="margin-top:10mm;display:inline-flex;gap:10px"><span class="rozet" style="background:{s.koyu}">{E(s.seviye)}</span><span class="rozet" style="background:#0f172a">Yazdır · Kalemle çalış</span></div>
<div style="margin-top:12mm;display:flex;flex-direction:column;align-items:center;gap:6px;font-size:13px;color:#475569">{qr_svg(SET_SAYFA, 110)}<b>Setin tamamı ve dijital oyunlar:</b>{ADRES}</div></div>'''
        s.sayfa(g, ham=True)

    def basardim(s, metin):
        g = f'''<div style="text-align:center;padding-top:30mm">{tane(220, 'mutlu', True)}
<div style="font-size:64px;font-weight:900;color:{s.renk};margin-top:10mm">Başardım!</div>
<div style="font-size:24px;font-weight:700;margin-top:6mm;line-height:1.5">{metin}</div>
<div style="margin:16mm auto 0;width:140mm;border:4px dashed {s.renk};border-radius:24px;padding:12mm;font-size:22px;text-align:left;line-height:2.2">
Adım: ..............................................<br>Tarih: ..............................................<br>Öğretmenim / ailem: ..............................</div></div>'''
        s.sayfa(g, ham=True, zemin=s.acik)
