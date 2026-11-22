#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hece Hece Okuma–Yazma Seti — PDF ve kapak görseli üreticisi (Barış Öğretmen)

Kullanım:
  python3 uret.py              # mevcut icerik_*.json dosyalarıyla üret
  python3 uret.py --bekle      # içerik dosyaları gelene kadar bekle (30 sn arayla, en çok 25 dk)
  python3 uret.py --deneme     # _deneme/icerik_deneme.json ile deneme üretimi

Çıktı: cikti/ altında 3 PDF + 4 PNG kapak + onizleme/ altında 60 dpi önizlemeler.
Yazı tipi: Andika (SIL International, SIL Open Font License 1.1) — fonts/ klasöründe.
"""
import json, os, sys, time, glob, subprocess, shutil, math

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.fonts import addMapping
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KOK = os.path.dirname(os.path.abspath(__file__))
CIKTI = os.path.join(KOK, 'cikti')
ONIZ = os.path.join(CIKTI, 'onizleme')
EMOJI_DIR = os.path.join(KOK, '_emoji')
# MEB dik temel harfe yakın (kuyruksuz a, d, u) okul yazısı: Didact Gothic (OFL). Kalın = dolgu + ince kontur.
FONT_R = os.path.join(KOK, 'fonts', 'DidactGothic-Regular.ttf')
FONT_B = FONT_R
FONT_SYM = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
SITE = 'https://baris-ogretmen.github.io/site-1/'
SITE_KISA = 'baris-ogretmen.github.io/site-1'
ICERIK_DOSYALARI = ['icerik_a.json', 'icerik_b.json']
HIKAYE_DOSYALARI = ['hikaye_a.json', 'hikaye_b.json']


def hikaye_yukle():
    out = []
    for d in HIKAYE_DOSYALARI:
        y = os.path.join(KOK, d)
        if os.path.exists(y):
            out += json.load(open(y, encoding='utf-8'))
    return sorted(out, key=lambda h: h['ders'])

pdfmetrics.registerFont(TTFont('Andika', FONT_R))
pdfmetrics.registerFont(TTFont('Andika-Bold', FONT_B))
pdfmetrics.registerFont(TTFont('Sym', FONT_SYM))
addMapping('Andika', 0, 0, 'Andika'); addMapping('Andika', 1, 0, 'Andika-Bold')
addMapping('Andika', 0, 1, 'Andika'); addMapping('Andika', 1, 1, 'Andika-Bold')

W, H = A4
M = 40                      # kenar boşluğu
ALT_SINIR = 54              # içerik bunun altına inmez (alt şerit)
XH = 468 / 1000             # Didact Gothic x-yüksekliği oranı

# Renkler
KIRMIZI = HexColor('#D62828')
LACIVERT = HexColor('#1D3557')
GRI_NOKTA = HexColor('#8C949D')
YESIL = HexColor('#2BA84A')
CIZGI_DIS = HexColor('#A8CBE6')
CIZGI_TABAN = HexColor('#5B9BD5')
CIZGI_ORTA = HexColor('#C9DDF0')
YUMUSAK = ['#2A9D8F', '#E9A23B', '#8E6FC9', '#E76F51', '#3A86C8', '#5BAE5B', '#D45D8C', '#2C9FB8']
ACIK = ['#E3F4F1', '#FCF0DC', '#EEE8F8', '#FCE7E1', '#E2EEF9', '#E6F4E6', '#F9E4EE', '#DFF2F6']


def tr_kucuk(t):
    return t.replace('I', 'ı').replace('İ', 'i').lower()


def tr_buyuk(t):
    return t.replace('i', 'İ').replace('ı', 'I').upper()


# ---------------------------------------------------------------- veri
def sira_yukle():
    with open(os.path.join(KOK, 'sira.json'), encoding='utf-8') as f:
        return json.load(f)


def icerik_yukle(deneme=False, bekle=False):
    if deneme:
        yollar = [os.path.join(KOK, '_deneme', 'icerik_deneme.json')]
    else:
        yollar = [os.path.join(KOK, d) for d in ICERIK_DOSYALARI]
        if bekle:
            bas = time.time()
            while True:
                eksik = [y for y in yollar if not os.path.exists(y)]
                if not eksik:
                    time.sleep(5)  # yazma tamamlansın
                    break
                if time.time() - bas > 25 * 60:
                    print('UYARI: 25 dk doldu; eksik dosyalar:', [os.path.basename(y) for y in eksik])
                    break
                print('bekleniyor:', [os.path.basename(y) for y in eksik], flush=True)
                time.sleep(30)
    dersler = {}
    for y in yollar:
        if not os.path.exists(y):
            print('UYARI: dosya yok:', y)
            continue
        try:
            with open(y, encoding='utf-8') as f:
                for d in json.load(f):
                    dersler[int(d['ders'])] = d
        except Exception as e:
            print('UYARI: okunamadı', y, e)
    return dersler


# ---------------------------------------------------------------- emoji
_emoji_cache = {}


def emoji_png(e, px=128):
    """Emojiyi Noto Color Emoji ile PNG'ye çizer (küçük çözünürlük). Yol döndürür ya da None."""
    key = (e, px)
    if key in _emoji_cache:
        return _emoji_cache[key]
    os.makedirs(EMOJI_DIR, exist_ok=True)
    ad = '_'.join('%x' % ord(c) for c in e) + '_%d.png' % px
    yol = os.path.join(EMOJI_DIR, ad)
    if not os.path.exists(yol):
        try:
            fnt = ImageFont.truetype(FONT_EMOJI, 109)
            img = Image.new('RGBA', (300, 200), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.text((20, 20), e, font=fnt, embedded_color=True)
            bb = img.getbbox()
            if not bb:
                raise ValueError('boş emoji')
            img = img.crop(bb)
            s = max(img.size)
            kare = Image.new('RGBA', (s, s), (0, 0, 0, 0))
            kare.paste(img, ((s - img.size[0]) // 2, (s - img.size[1]) // 2))
            kare = kare.resize((px, px), Image.LANCZOS)
            kare.save(yol, optimize=True)
        except Exception as ex:
            print('UYARI: emoji çizilemedi', repr(e), ex)
            _emoji_cache[key] = None
            return None
    _emoji_cache[key] = yol
    return yol


def emoji_ciz(c, e, x, y, boy, yedek_harf='?'):
    yol = emoji_png(e, 128 if boy < 140 else 160)
    if yol:
        c.drawImage(yol, x, y, boy, boy, mask='auto')
    else:
        c.setFillColor(HexColor('#F4D35E'))
        c.circle(x + boy / 2, y + boy / 2, boy / 2, stroke=0, fill=1)
        c.setFillColor(LACIVERT)
        c.setFont('Andika-Bold', boy * 0.5)
        c.drawCentredString(x + boy / 2, y + boy * 0.32, yedek_harf)


# ---------------------------------------------------------------- çizim yardımcıları
def sw(t, font, size):
    return pdfmetrics.stringWidth(t, font, size)


def renkli_yaz(c, x, y, metin, size, harf, font='Andika', ana=LACIVERT, vurgu=KIRMIZI):
    """Yeni harfi kırmızı, diğerlerini lacivert yazar. Genişliği döndürür."""
    x0 = x
    for ch in metin:
        c.setFillColor(vurgu if (harf and tr_kucuk(ch) == harf) else ana)
        c.setFont(font, size)
        c.drawString(x, y, ch)
        x += sw(ch, font, size)
    return x - x0


def renkli_ortala(c, xm, y, metin, size, harf, font='Andika', ana=LACIVERT):
    w = sw(metin, font, size)
    renkli_yaz(c, xm - w / 2, y, metin, size, harf, font, ana)


def noktali_yaz(c, x, y, metin, size, renk=GRI_NOKTA, kalinlik=None, aralik=None):
    """Metni kesik çizgili (noktalı) kontur olarak çizer — vektör."""
    kalinlik = kalinlik or max(1.1, size * 0.05)
    aralik = aralik or max(2.4, size * 0.105)
    c.saveState()
    c.setStrokeColor(renk)
    c.setLineWidth(kalinlik)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.setDash([0.01, aralik], 0)
    t = c.beginText(x, y)
    t.setFont('Andika', size)
    t.setTextRenderMode(1)
    t.textOut(metin)
    c.drawText(t)
    c.restoreState()


def baslangic_noktasi(c, x, taban, b):
    c.setFillColor(YESIL)
    c.circle(x - 6.5, taban + b * 0.5, max(2.6, b * 0.17), stroke=0, fill=1)


def dort_cizgi(c, x0, y0, gen, b):
    """4 çizgili ilkokul satırı. y0 = en alt çizgi; taban çizgisi y0+b."""
    c.saveState()
    c.setLineWidth(0.6)
    c.setStrokeColor(CIZGI_DIS)
    c.line(x0, y0, x0 + gen, y0)
    c.line(x0, y0 + 3 * b, x0 + gen, y0 + 3 * b)
    c.setStrokeColor(CIZGI_ORTA)
    c.setDash([3, 2.5], 0)
    c.line(x0, y0 + 2 * b, x0 + gen, y0 + 2 * b)
    c.setDash([], 0)
    c.setStrokeColor(CIZGI_TABAN)
    c.setLineWidth(1.0)
    c.line(x0, y0 + b, x0 + gen, y0 + b)
    c.restoreState()


def yuvarlak_kutu(c, x, y, w, h, r, dolgu, cizgi=None, lw=1):
    c.saveState()
    c.setFillColor(dolgu)
    if cizgi:
        c.setStrokeColor(cizgi); c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1 if cizgi else 0, fill=1)
    c.restoreState()


def qr_ciz(c, x, y, boy, url=SITE):
    w = QrCodeWidget(url, barLevel='M')
    b = w.getBounds()
    bw, bh = b[2] - b[0], b[3] - b[1]
    d = Drawing(boy, boy, transform=[boy / bw, 0, 0, boy / bh, 0, 0])
    d.add(w)
    renderPDF.draw(d, c, x, y)
    c.linkURL(url, (x, y, x + boy, y + boy), relative=0)


def alt_serit(c, n, toplam):
    c.saveState()
    c.setFillColor(white); c.rect(0, 0, W, 46, stroke=0, fill=1)
    c.setStrokeColor(HexColor('#D5DCE4')); c.setLineWidth(0.6)
    c.line(M, 40, W - M, 40)
    yuvarlak_kutu(c, M - 2, 9, 28, 28, 3, white)
    qr_ciz(c, M, 11, 24)
    tx = M + 32
    c.setFillColor(HexColor('#E9A23B')); c.setFont('Sym', 8.5)
    c.drawString(tx, 20, '★')
    c.setFillColor(LACIVERT); c.setFont('Andika', 8.5)
    s1 = ' Barış Öğretmen tarafından hazırlanmıştır · '
    c.drawString(tx + sw('★', 'Sym', 8.5), 20, s1)
    lx = tx + sw('★', 'Sym', 8.5) + sw(s1, 'Andika', 8.5)
    c.setFillColor(HexColor('#2C6FB7'))
    c.drawString(lx, 20, SITE_KISA)
    lw = sw(SITE_KISA, 'Andika', 8.5)
    c.linkURL(SITE, (tx, 15, lx + lw, 30), relative=0)
    c.setFillColor(HexColor('#6B7785'))
    c.drawRightString(W - M, 20, 'Sayfa %d/%d' % (n, toplam))
    # 🏠 Siteye dön düğmesi (dokununca siteyi açar)
    bt = 'Siteye dön'
    bw = sw(bt, 'Andika-Bold', 9) + 30
    bx = W - M - sw('Sayfa %d/%d' % (n, toplam), 'Andika', 8.5) - 14 - bw
    yuvarlak_kutu(c, bx, 11, bw, 20, 10, HexColor('#2C6FB7'))
    c.setFillColor(white); c.setFont('Sym', 9); c.drawString(bx + 8, 18, '◀')
    c.setFont('Andika-Bold', 9); c.drawString(bx + 21, 18, bt)
    c.linkURL(SITE, (bx, 11, bx + bw, 31), relative=0)
    c.restoreState()


def ust_bant(c, ders_no, harf, baslik, renk_i, kitap_adi):
    """Çalışma sayfası başlığı. İçeriğin başlayabileceği y'yi döndürür."""
    renk = HexColor(YUMUSAK[renk_i % len(YUMUSAK)])
    yuvarlak_kutu(c, M, H - 36 - 44, W - 2 * M, 44, 12, renk)
    # harf rozeti
    c.setFillColor(white)
    c.circle(M + 26, H - 36 - 22, 17, stroke=0, fill=1)
    c.setFillColor(KIRMIZI); c.setFont('Andika-Bold', 20)
    c.drawCentredString(M + 26, H - 36 - 29, harf)
    c.setFillColor(white); c.setFont('Andika-Bold', 17)
    c.drawString(M + 52, H - 36 - 28, 'Ders %d  ·  %s' % (ders_no, baslik))
    c.setFont('Andika', 9.5)
    c.drawRightString(W - M - 14, H - 36 - 27, kitap_adi)
    return H - 36 - 44


def yonerge(c, y, metin):
    c.setFillColor(HexColor('#4A5868')); c.setFont('Andika', 11.5)
    c.drawString(M + 4, y, metin)


# ---------------------------------------------------------------- çalışma sayfaları
class KalinCanvas(rl_canvas.Canvas):
    """'Andika-Bold' adıyla yazılan metni aynı yazı tipinde dolgu + konturla (kalın) çizer."""
    def _kalin(self, x, y, text):
        t = self.beginText(x, y); t.setFont(self._fontname, self._fontsize); t.setTextRenderMode(2)
        self.saveState(); self.setStrokeColor(self._fillColorObj); self.setLineWidth(self._fontsize * 0.045)
        t.textOut(text); self.drawText(t); self.restoreState()

    def drawString(self, x, y, text, *a, **k):
        if self._fontname == 'Andika-Bold':
            return self._kalin(x, y, text)
        return super().drawString(x, y, text, *a, **k)

    def drawCentredString(self, x, y, text, *a, **k):
        if self._fontname == 'Andika-Bold':
            return self._kalin(x - self.stringWidth(text) / 2, y, text)
        return super().drawCentredString(x, y, text, *a, **k)

    def drawRightString(self, x, y, text, *a, **k):
        if self._fontname == 'Andika-Bold':
            return self._kalin(x - self.stringWidth(text), y, text)
        return super().drawRightString(x, y, text, *a, **k)


SITE_DOSYA = 'https://baris-ogretmen.github.io/site-1/'
CALISMALAR = {  # derse göre "Tablette çalış" QR'ı (sitedeki okuma-yazma çalışmaları)
    'unlu': [('Harf Yolculuğu (ANETİL)', 'anetill okuma yazma.html'), ('Okuma Saati', 'anetil okuma saati.html'),
             ('Sihirli Parmaklar Yazı Atölyesi', 'sihirli-parmaklar.html'), ('Harf Topu', 'harf topu.html'),
             ('Konuşma Atölyesi', 'konusma-atolyesi.html')],
    'unsuz': [('Sihirli Heceler', 'hece-birlestirme.html'), ('Okuma Yazma Treni', 'okuma-yazma-v2.html'),
              ('Mega Dikte Seti', 'mega-dikte-seti.html'), ('Sonbahar Dikte', 'sonbahar_dikte.html'),
              ('Akıllı Okuma Asistanı', 'akilli-okuma.html'), ('İlk Okuma Akademisi', 'okuma-sifresi.html'),
              ('Harf Yolculuğu (ANETİL)', 'anetill okuma yazma.html'), ('Okuma Saati', 'anetil okuma saati.html')],
    'hikaye': [('5N1K Dedektifleri', '5n1k-okuma.html'), ('Akıllı Okuma Asistanı', 'akilli-okuma.html'),
               ('Sihirli Okuma Asistanı', 'disleksi-okuma.html')],
}


def calisma_sec(tur, i):
    from urllib.parse import quote
    ad, yol = CALISMALAR[tur][i % len(CALISMALAR[tur])]
    return ad, SITE_DOSYA + quote(yol)


def qr_bandi(c, y, ad, url, renk='#2A9D8F'):
    """Alt şeridin üstünde 'Tablette çalış' kutusu: QR + çalışma adı (dokununca da açılır)."""
    h = 66
    yuvarlak_kutu(c, M, y, W - 2 * M, h, 14, HexColor('#F2F7FB'), HexColor('#C9DDF0'), 1)
    yuvarlak_kutu(c, M + 8, y + 5, 56, 56, 6, white)
    qr_ciz(c, M + 10, y + 7, 52, url)
    c.setFillColor(HexColor(renk)); c.setFont('Andika-Bold', 13.5)
    c.drawString(M + 76, y + 38, 'Tablette çalış: ' + ad)
    c.setFillColor(HexColor('#4A5868')); c.setFont('Andika', 10.5)
    c.drawString(M + 76, y + 20, 'Telefonun kamerasıyla kare kodu okut ya da buraya dokun; çalışma açılır.')
    c.linkURL(url, (M, y, W - M, y + h), relative=0)


class SayfaDizisi:
    def __init__(self):
        self.sayfalar = []

    def ekle(self, fn):
        self.sayfalar.append(fn)

    def yaz(self, yol, baslik):
        c = KalinCanvas(yol, pagesize=A4, pageCompression=1)
        c.setTitle(baslik); c.setAuthor('Barış Öğretmen'); c.setSubject('Barış Öğretmen Setleri · Hece Hece Okuma–Yazma')
        c.setCreator('Barış Öğretmen · ' + SITE_KISA)
        N = len(self.sayfalar)
        for i, fn in enumerate(self.sayfalar):
            fn(c)
            alt_serit(c, i + 1, N)
            c.showPage()
        c.save()
        return N


def satir_sayfalari(dizi, ders, kitap_adi, baslik, yonerge_metni, satirlar, renk_i, bitis=None):
    """satirlar: [(yukseklik, cizfn(c, y_ust))]. Sığmayanları yeni sayfaya taşır.
    bitis: (yukseklik, cizfn) — son sayfanın sonuna eklenir."""
    harf = ders['harf']
    gruplar = []
    mevcut, kalan = [], None
    ust_y = H - 36 - 44 - 34
    kullanilir = ust_y - ALT_SINIR
    hepsi = list(satirlar) + ([bitis] if bitis else [])
    kalan = kullanilir
    for s in hepsi:
        if s[0] > kalan and mevcut:
            gruplar.append(mevcut); mevcut = []; kalan = kullanilir
        mevcut.append(s); kalan -= s[0]
    if mevcut:
        gruplar.append(mevcut)
    for gi, g in enumerate(gruplar):
        def fn(c, g=g, gi=gi):
            ust_bant(c, ders['ders'], harf, baslik + (' (devam)' if gi else ''), renk_i, kitap_adi)
            yonerge(c, H - 36 - 44 - 22, yonerge_metni)
            y = ust_y
            for h, ciz in g:
                ciz(c, y)
                y -= h
        dizi.ekle(fn)


def tekrar_satiri(metin, harf, b, kopya_max, kopya_min, bosluk=26):
    """Satır başında renkli örnek + noktalı kopyalar. (yükseklik, çizici) döndürür."""
    avail = W - 2 * M - 20
    bb = b
    while True:
        s = bb / XH
        tw = sw(metin, 'Andika', s)
        slot = tw + bosluk
        k = int((avail + bosluk) // slot) - 1
        if k >= kopya_min or bb < 8:
            break
        bb -= 0.5
    k = max(1, min(kopya_max, k))
    s = bb / XH
    tw = sw(metin, 'Andika', s)
    # kopyaları satıra eşit yay
    serbest = avail - (k + 1) * tw
    ara = serbest / (k + 1) if k else 0
    ara = min(ara, 60)
    yuk = 3 * b + 14

    def ciz(c, y_ust):
        y0 = y_ust - 3 * b - 4
        dort_cizgi(c, M, y0, W - 2 * M, b)
        taban = y0 + b
        x = M + 12
        renkli_yaz(c, x, taban, metin, s, harf)
        x += tw + ara
        for _ in range(k):
            baslangic_noktasi(c, x, taban, bb)
            noktali_yaz(c, x, taban, metin, s)
            x += tw + ara
    return yuk, ciz


def cumle_cifti(metin, harf, b):
    avail = W - 2 * M - 26
    bb = b
    while sw(metin, 'Andika', bb / XH) > avail and bb > 7:
        bb -= 0.5
    s = bb / XH
    yuk = 6 * b + 4 + 14

    def ciz(c, y_ust):
        y0 = y_ust - 3 * b - 4
        dort_cizgi(c, M, y0, W - 2 * M, b)
        renkli_yaz(c, M + 14, y0 + b, metin, s, harf)
        y1 = y0 - 4 - 3 * b
        dort_cizgi(c, M, y1, W - 2 * M, b)
        baslangic_noktasi(c, M + 14, y1 + b, bb)
        noktali_yaz(c, M + 14, y1 + b, metin, s)
    return yuk, ciz


def tanitim_sayfasi(dizi, ders, ipucu, kitap_adi, renk_i):
    harf = ders['harf']
    BUYUK = tr_buyuk(harf)
    rk = ders.get('resimli_kelime') or {}

    def fn(c):
        ust = ust_bant(c, ders['ders'], harf, 'Yeni harfimiz: %s  %s' % (harf, BUYUK), renk_i, kitap_adi)
        acik = HexColor(ACIK[renk_i % len(ACIK)])
        # büyük harf kutusu
        kx, ky, kw, kh = M, ust - 16 - 230, 300, 230
        yuvarlak_kutu(c, kx, ky, kw, kh, 18, acik)
        c.setFillColor(KIRMIZI)
        c.setFont('Andika-Bold', 132)
        c.drawCentredString(kx + kw * 0.30, ky + 98, harf)
        c.drawCentredString(kx + kw * 0.72, ky + 98, BUYUK)
        c.setFillColor(HexColor('#4A5868')); c.setFont('Andika', 11)
        c.drawCentredString(kx + kw * 0.30, ky + 50, 'küçük harf')
        c.drawCentredString(kx + kw * 0.72, ky + 50, 'büyük harf')
        # ses ipucu
        yuvarlak_kutu(c, kx + 12, ky + 10, kw - 24, 32, 10, white)
        c.setFillColor(LACIVERT); c.setFont('Andika-Bold', 12)
        ip = 'Sesi: ' + ipucu
        fs = 12
        while sw(ip, 'Andika-Bold', fs) > kw - 40 and fs > 8:
            fs -= 0.5
        c.setFont('Andika-Bold', fs)
        c.drawCentredString(kx + kw / 2, ky + 21, ip)
        # resimli kelime
        rx, rw = kx + kw + 16, W - M - (kx + kw + 16)
        yuvarlak_kutu(c, rx, ky, rw, kh, 18, HexColor('#FFF8E6'))
        emoji_ciz(c, rk.get('emoji', ''), rx + rw / 2 - 66, ky + 78, 132, tr_buyuk(harf))
        kel = rk.get('kelime', '')
        fs = 40
        while sw(kel, 'Andika', fs) > rw - 20 and fs > 16:
            fs -= 1
        renkli_ortala(c, rx + rw / 2, ky + 30, kel, fs, harf)
        # izleme satırları
        y = ky - 30
        c.setFillColor(LACIVERT); c.setFont('Andika-Bold', 14)
        c.drawString(M + 4, y, 'Harfin üzerinden geç. Yeşil noktadan başla, sesi uzatarak söyle.')
        y -= 10
        b = 22
        for ri, metin in enumerate((harf, harf, BUYUK, BUYUK)):
            s = b / XH
            y0 = y - 3 * b - 4
            dort_cizgi(c, M, y0, W - 2 * M, b)
            taban = y0 + b
            tw = sw(metin, 'Andika', s)
            avail = W - 2 * M - 24
            k = int(avail // (tw + 30))
            ara = (avail - k * tw) / k
            x = M + 14
            for i in range(k):
                if i == 0 and ri in (0, 2):
                    renkli_yaz(c, x, taban, metin, s, harf)
                else:
                    baslangic_noktasi(c, x, taban, b)
                    noktali_yaz(c, x, taban, metin, s)
                x += tw + ara
            y = y0 - 14
        n = ders['ders']
        ad, url = calisma_sec('unlu' if n <= 8 else 'unsuz', n - 1 if n <= 8 else n - 9)
        qr_bandi(c, max(ALT_SINIR + 4, min(y - 70, ALT_SINIR + 4)), ad, url)
    dizi.ekle(fn)


def dinle_bul_sayfasi(dizi, ders, kitap_adi, renk_i):
    import random
    harf = ders['harf']; n = ders['ders']
    dinle = [d for d in (ders.get('dinle') or []) if d.get('kelime')][:6]
    rnd = random.Random(n * 7 + 3)
    havuz = [d[0] for d in sira_yukle()['dersler'][:max(n, 8)] if d[0] != harf] or ['a']
    kut = [harf if rnd.random() < 0.34 else rnd.choice(havuz) for _ in range(40)]

    def fn(c):
        ust = ust_bant(c, n, harf, 'Dinle ve bul', renk_i, kitap_adi)
        acik = HexColor(ACIK[renk_i % len(ACIK)])
        y = ust - 24
        if dinle:
            yonerge(c, y, 'Öğretmen resmin adını söyler. Çocuk ilk sesi duyunca "%s" der ve harfi gösterir.' % harf)
            k = len(dinle); sut = 3; gw = (W - 2 * M - (sut - 1) * 12) / sut; gh = 118
            for i, d in enumerate(dinle):
                r, s_ = divmod(i, sut)
                x = M + s_ * (gw + 12); yy = y - 14 - (r + 1) * gh - r * 10
                yuvarlak_kutu(c, x, yy, gw, gh, 14, acik)
                emoji_ciz(c, d.get('emoji', ''), x + gw / 2 - 34, yy + 42, 68, tr_buyuk(harf))
                kel = d['kelime']; fs = 22
                while sw(kel, 'Andika', fs) > gw - 16 and fs > 12:
                    fs -= 1
                renkli_ortala(c, x + gw / 2, yy + 14, kel, fs, harf)
            y = y - 14 - math.ceil(k / sut) * (gh + 10) - 16
        yonerge(c, y, 'Harf avı: "%s" ve "%s" harflerini bul, daire içine al ya da boya.' % (harf, tr_buyuk(harf)))
        sut, sat = 8, 5; gw = (W - 2 * M) / sut
        gh = min(62, (y - 20 - ALT_SINIR - 40) / sat)
        for i, h in enumerate(kut):
            r, s_ = divmod(i, sut)
            x = M + s_ * gw + gw / 2; yy = y - 22 - (r + 1) * gh
            if rnd.random() < 0.4:
                h = tr_buyuk(h)
            c.setFillColor(LACIVERT); c.setFont('Andika', min(40, gh * 0.7))
            c.drawCentredString(x, yy + gh * 0.25, h)
    dizi.ekle(fn)


def ders_sayfalari(dizi, ders, ipucu, kitap_adi):
    renk_i = ders['ders'] - 1
    harf = ders['harf']
    tanitim_sayfasi(dizi, ders, ipucu, kitap_adi, renk_i)
    dinle_bul_sayfasi(dizi, ders, kitap_adi, renk_i)
    unlu = ders['ders'] <= 8
    # heceler
    heceler = [h for h in ders.get('heceler', []) if h.strip()]
    if heceler:
        b = max(13, min(16, (664 / len(heceler) - 14) / 3))
        satirlar = [tekrar_satiri(h, harf, b, 5, 4) for h in heceler]
        satir_sayfalari(dizi, ders, kitap_adi, 'Sesleri okuyalım' if unlu else 'Heceler',
                        'Renkli sesleri uzatarak oku. Sonra yeşil noktadan başlayıp üzerinden geç.' if unlu else
                        'Önce renkli heceyi sesli oku. Sonra yeşil noktadan başlayıp üzerinden geç.', satirlar, renk_i)
    kelimeler = [k for k in ders.get('kelimeler', []) if k.strip()]
    if kelimeler:
        b = max(11, min(16, (664 / len(kelimeler) - 14) / 3))
        satirlar = [tekrar_satiri(k, harf, b, 3, 2) for k in kelimeler]
        satir_sayfalari(dizi, ders, kitap_adi, 'Ses oyunu' if unlu else 'Kelimeler',
                        'Renkli yazıyı sesli oku, sonra üzerinden geç.' if unlu else
                        'Kelimeyi sesleri uzatarak oku, sonra üzerinden geç.', satirlar, renk_i)
    cumleler = [k for k in ders.get('cumleler', []) if k.strip()]
    if cumleler:
        n = len(cumleler)
        bos = 2 if n <= 5 else 1
        b = max(12.5, min(17, (656 - 46 - 18 * n) / (6 * n + 3 * bos)))
        satirlar = [cumle_cifti(k, harf, b) for k in cumleler]

        def bitis_ciz(c, y_ust):
            c.setFillColor(HexColor(YUMUSAK[renk_i % len(YUMUSAK)])); c.setFont('Andika-Bold', 14)
            c.drawString(M + 4, y_ust - 16, 'Şimdi kendin yaz ✎'.replace(' ✎', ''))
            c.setFillColor(HexColor('#6B7785')); c.setFont('Andika', 10.5)
            c.drawString(M + 4 + sw('Şimdi kendin yaz', 'Andika-Bold', 14) + 10, y_ust - 16,
                         '(Bir kelime ya da cümle seç, kendin yaz.)')
            for i in range(bos):
                y0 = y_ust - 26 - (i + 1) * (3 * b) - i * 10
                dort_cizgi(c, M, y0, W - 2 * M, b)
        satir_sayfalari(dizi, ders, kitap_adi, 'Cümleler', 'Cümleyi oku. Alttaki satırda üzerinden geç.', satirlar, renk_i,
                        bitis=(26 + 3 * bos * b + 10 * bos + 10, bitis_ciz))


# ---------------------------------------------------------------- kapak ve not
def harf_karosu(c, x, y, boy, harf, dolgu, yazi=white, font='Andika-Bold'):
    yuvarlak_kutu(c, x, y, boy, boy, boy * 0.22, dolgu)
    c.setFillColor(yazi); c.setFont(font, boy * 0.62)
    c.drawCentredString(x + boy / 2, y + boy * 0.27, harf)


def kapak_sayfasi(dizi, baslik, alt_baslik, harfler, emojiler, ana_renk='#2A9D8F'):
    def fn(c):
        c.setFillColor(HexColor('#FFF8EC')); c.rect(0, 0, W, H, stroke=0, fill=1)
        # yumuşak süs daireleri
        for (x, y, r, col) in [(60, H - 70, 90, '#FCE7E1'), (W - 40, H - 180, 120, '#E2EEF9'),
                               (W - 90, 230, 80, '#E6F4E6'), (30, 300, 60, '#FCF0DC')]:
            c.setFillColor(HexColor(col)); c.circle(x, y, r, stroke=0, fill=1)
        ana = HexColor(ana_renk)
        yuvarlak_kutu(c, M, H - 250, W - 2 * M, 170, 26, ana)
        c.setFillColor(white)
        fs = 40
        while sw(baslik, 'Andika-Bold', fs) > W - 2 * M - 40:
            fs -= 1
        c.setFont('Andika-Bold', fs); c.drawCentredString(W / 2, H - 150, baslik)
        c.setFont('Andika-Bold', 24); c.drawCentredString(W / 2, H - 190, alt_baslik)
        c.setFont('Andika', 14); c.drawCentredString(W / 2, H - 222, 'Barış Öğretmen Setleri')
        # emoji şeridi
        em = [e for e in emojiler if e][:6]
        if em:
            boy = 62; ara = 18
            tw = len(em) * boy + (len(em) - 1) * ara
            x = W / 2 - tw / 2
            for e in em:
                emoji_ciz(c, e, x, H - 340, boy); x += boy + ara
        # harf karoları
        c.setFillColor(LACIVERT); c.setFont('Andika-Bold', 15)
        c.drawCentredString(W / 2, H - 375, 'Bu kitaptaki harfler')
        boy, ara = 40, 9
        satir_n = 8
        satirlar = [harfler[i:i + satir_n] for i in range(0, len(harfler), satir_n)]
        y = H - 430
        for sat in satirlar:
            tw = len(sat) * boy + (len(sat) - 1) * ara
            x = W / 2 - tw / 2
            for j, h in enumerate(sat):
                harf_karosu(c, x, y, boy, h, HexColor(YUMUSAK[(harfler.index(h)) % len(YUMUSAK)]))
                x += boy + ara
            y -= boy + ara
        # büyük QR
        q = 132
        qx, qy = W / 2 - q / 2, 116
        yuvarlak_kutu(c, qx - 12, qy - 12, q + 24, q + 24, 14, white, HexColor('#D5DCE4'))
        qr_ciz(c, qx, qy, q)
        c.setFillColor(LACIVERT); c.setFont('Andika-Bold', 14)
        c.drawCentredString(W / 2, qy - 32 + q + 24 + 30 + 4 - 0, '')
        c.setFont('Andika', 12.5); c.setFillColor(HexColor('#4A5868'))
        c.drawCentredString(W / 2, 84, 'Daha fazlası için: ')
        c.setFont('Andika-Bold', 13); c.setFillColor(HexColor('#2C6FB7'))
        c.drawCentredString(W / 2, 66, SITE_KISA)
        c.linkURL(SITE, (W / 2 - 110, 60, W / 2 + 110, 98), relative=0)
    dizi.ekle(fn)


def paragraf(c, metin, x, y_ust, gen, size=11.5, renk='#1D3557', lead=None, font='Andika'):
    st = ParagraphStyle('p', fontName=font, fontSize=size, leading=lead or size * 1.38,
                        textColor=HexColor(renk))
    p = Paragraph(metin, st)
    w, h = p.wrap(gen, 1000)
    p.drawOn(c, x, y_ust - h)
    return y_ust - h


def not_sayfasi(dizi, sira, aralik, kitap_turu):
    a, b = aralik

    def fn(c):
        yuvarlak_kutu(c, M, H - 36 - 44, W - 2 * M, 44, 12, HexColor('#3A86C8'))
        c.setFillColor(white); c.setFont('Andika-Bold', 19)
        c.drawString(M + 18, H - 36 - 29, 'Öğretmen ve veliye not')
        y = H - 36 - 44 - 18
        y = paragraf(c, 'Bu set, ilk okuma-yazmaya başlayan çocuklar için <b>sesten harfe, harften heceye, heceden kelime ve cümleye</b> '
                        'ilerleyen bir çalışma dizisidir. Her derste yalnızca o güne kadar öğrenilmiş harfler kullanılır. '
                        'Her çocuğun hızı farklıdır; bir dersi birkaç gün tekrar etmek doğaldır.', M, y, W - 2 * M)
        y -= 12
        c.setFillColor(HexColor('#E76F51')); c.setFont('Andika-Bold', 14.5)
        c.drawString(M, y - 14, 'Harf sırası neye göre belirlendi?'); y -= 22
        for il in sira['ilkeler']:
            c.setFillColor(HexColor('#E76F51')); c.circle(M + 6, y - 8, 2.6, stroke=0, fill=1)
            y = paragraf(c, il, M + 16, y, W - 2 * M - 16, size=11) - 3
        y -= 10
        c.setFillColor(HexColor('#2A9D8F')); c.setFont('Andika-Bold', 14.5)
        c.drawString(M, y - 14, 'Harf sırası (bu kitaptakiler renkli)'); y -= 26
        # tablo: 10 sütun x 3 satır
        dersler = sira['dersler']
        sut = 10
        hw = (W - 2 * M) / sut
        hh = 40
        for i, (h, _) in enumerate(dersler):
            r, k = divmod(i, sut)
            x = M + k * hw; yy = y - (r + 1) * hh
            icinde = a <= i + 1 <= b
            dol = HexColor(YUMUSAK[i % len(YUMUSAK)]) if icinde else HexColor('#EEF1F4')
            yuvarlak_kutu(c, x + 2, yy + 2, hw - 4, hh - 4, 7, dol)
            c.setFillColor(white if icinde else HexColor('#8A95A3'))
            c.setFont('Andika', 8); c.drawString(x + 7, yy + hh - 13, str(i + 1))
            c.setFont('Andika-Bold', 17)
            c.drawCentredString(x + hw / 2 + 3, yy + 10, '%s %s' % (tr_buyuk(h), h))
        y -= math.ceil(len(dersler) / sut) * hh + 16
        c.setFillColor(HexColor('#8E6FC9')); c.setFont('Andika-Bold', 14.5)
        c.drawString(M, y - 14, 'Nasıl kullanılır?'); y -= 22
        if kitap_turu == 'calisma':
            maddeler = [
                'Günde <b>10–15 dakika</b> yeterlidir. Kısa ve düzenli çalışma, uzun ve yorucu çalışmadan daha verimlidir.',
                'Her ders dört adımdır: <b>harf tanıtımı → heceler → kelimeler → cümleler</b>.',
                'Önce sesi birlikte söyleyin. Sesi <b>uzatarak</b> okuyun: “mmm-aaa → ma”.',
                'Noktalı yazının üzerinden <b>önce parmakla</b>, sonra kalemle geçin. <font color="#2BA84A"><b>Yeşil nokta</b></font> başlama yeridir.',
                '<font color="#D62828"><b>Kırmızı</b></font> harf, o derste öğrenilen yeni harftir.',
                'Kalemi doğru tutmak ve yavaş yazmak, hızlı yazmaktan önemlidir. Çabayı övün; hataları sakince birlikte düzeltin.',
                'Okuma Hikâyeleri kitabı 11. dersten itibaren her derse bir hikâyeyle eşlik eder.',
            ]
        else:
            maddeler = []
        for md in maddeler:
            c.setFillColor(HexColor('#8E6FC9')); c.circle(M + 6, y - 8, 2.6, stroke=0, fill=1)
            y = paragraf(c, md, M + 16, y, W - 2 * M - 16, size=11) - 3
    dizi.ekle(fn)


# ---------------------------------------------------------------- hikâyeler
def sar(metin, font, size, gen):
    kel = metin.split()
    satirlar, mev = [], ''
    for k in kel:
        aday = (mev + ' ' + k).strip()
        if sw(aday, font, size) <= gen or not mev:
            mev = aday
        else:
            satirlar.append(mev); mev = k
    if mev:
        satirlar.append(mev)
    return satirlar


def hikaye_bolumleri(dizi, ders, sira, sayac):
    hk = ders['hikaye']
    harf = ders['harf']
    n = ders['ders']
    renk = HexColor(YUMUSAK[sayac % len(YUMUSAK)])
    acik = HexColor(ACIK[sayac % len(ACIK)])
    emoji = (ders.get('resimli_kelime') or {}).get('emoji', '')
    ogrenilen = [d[0] for d in sira['dersler'][:n]]

    # ayraç / kapak
    def kapak(c):
        c.setFillColor(renk); c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(Color(1, 1, 1, alpha=0.13))
        c.circle(W - 60, H - 80, 140, stroke=0, fill=1); c.circle(50, 180, 110, stroke=0, fill=1)
        c.setFillColor(white); c.setFont('Andika-Bold', 16)
        c.drawCentredString(W / 2, H - 90, 'Hikâye %d  ·  Ders %d  ·  Yeni harf: %s %s' % (sayac + 1, n, harf, tr_buyuk(harf)))
        yuvarlak_kutu(c, M + 10, H - 340, W - 2 * M - 20, 220, 30, white)
        emoji_ciz(c, emoji, W / 2 - 80, H - 320, 160, tr_buyuk(harf))
        fs = 44
        while sw(hk['baslik'], 'Andika-Bold', fs) > W - 2 * M - 30:
            fs -= 1
        yuvarlak_kutu(c, M + 10, H - 470, W - 2 * M - 20, 100, 30, white)
        renkli_ortala(c, W / 2, H - 435, hk['baslik'], fs, harf, font='Andika-Bold')
        c.setFillColor(white); c.setFont('Andika-Bold', 15)
        c.drawCentredString(W / 2, H - 510, 'Bu hikâyede okuyacağımız harfler')
        boy, ara, sn = 38, 8, 10
        satirlar = [ogrenilen[i:i + sn] for i in range(0, len(ogrenilen), sn)]
        y = H - 565
        for sat in satirlar:
            tw = len(sat) * boy + (len(sat) - 1) * ara
            x = W / 2 - tw / 2
            for h in sat:
                yeni = (h == harf)
                harf_karosu(c, x, y, boy, h, white, KIRMIZI if yeni else LACIVERT)
                x += boy + ara
            y -= boy + ara
    dizi.ekle(kapak)

    # sayfalar: 1–2 cümle
    FS = 40
    gen = W - 2 * M - 70
    cumleler = [s for s in hk.get('cumleler', []) if s.strip()]
    gruplar, i = [], 0
    while i < len(cumleler):
        s1 = sar(cumleler[i], 'Andika', FS, gen)
        if i + 1 < len(cumleler):
            s2 = sar(cumleler[i + 1], 'Andika', FS, gen)
            if len(s1) + len(s2) <= 4:
                gruplar.append([cumleler[i], cumleler[i + 1]]); i += 2; continue
        gruplar.append([cumleler[i]]); i += 1
    for gi, g in enumerate(gruplar):
        def fn(c, g=g, gi=gi):
            c.setFillColor(acik); c.rect(0, 46, W, H - 46, stroke=0, fill=1)
            c.setFillColor(renk); c.setFont('Andika-Bold', 13)
            c.drawString(M, H - 50, hk['baslik'])
            c.drawRightString(W - M, H - 50, '%d / %d' % (gi + 1, len(gruplar)))
            kx, ky, kw, kh = M, 150, W - 2 * M, H - 230
            yuvarlak_kutu(c, kx, ky, kw, kh, 30, white, renk, 2.5)
            emoji_ciz(c, emoji, W / 2 - 55, ky + kh - 150, 110, tr_buyuk(harf))
            satirlar = []
            for j, s in enumerate(g):
                if j:
                    satirlar.append(None)
                satirlar += sar(s, 'Andika', FS, gen)
            lead = FS * 1.55
            toplam = sum(lead if s else lead * 0.6 for s in satirlar)
            y = ky + (kh - 170) / 2 + toplam / 2
            for s in satirlar:
                if s is None:
                    y -= lead * 0.6; continue
                y -= lead
                renkli_ortala(c, W / 2, y + lead * 0.3, s, FS, harf)
            c.setFillColor(HexColor('#6B7785')); c.setFont('Andika', 11)
            c.drawCentredString(W / 2, 118, 'Parmağınla takip ederek oku. Kırmızı harf yeni harfimiz.')
        dizi.ekle(fn)

    # Hadi konuşalım
    sorular = hk.get('sorular') or []
    if sorular:
        def kon(c):
            c.setFillColor(acik); c.rect(0, 46, W, H - 46, stroke=0, fill=1)
            yuvarlak_kutu(c, M, H - 36 - 56, W - 2 * M, 56, 16, renk)
            c.setFillColor(white); c.setFont('Andika-Bold', 26)
            c.drawCentredString(W / 2, H - 36 - 38, 'Hadi konuşalım')
            y = H - 120
            for q in sorular:
                cev_sat = sar(q.get('cevap', ''), 'Andika', 30, W - 2 * M - 60)
                qh = 40 + len(cev_sat) * 44 + 18
                yuvarlak_kutu(c, M, y - qh, W - 2 * M, qh, 18, white, renk, 1.5)
                c.setFillColor(HexColor('#6B7785')); c.setFont('Andika', 11.5)
                c.drawString(M + 18, y - 24, 'Öğretmen sorar:  ' + q.get('soru', ''))
                yy = y - 40
                for s in cev_sat:
                    yy -= 44
                    renkli_yaz(c, M + 30, yy + 10, s, 30, harf)
                y -= qh + 16
        dizi.ekle(kon)


def hikaye_bolumleri2(dizi, hk, sira, sayac):
    n = hk['ders']
    harf = sira['dersler'][n - 1][0]
    renk = HexColor(YUMUSAK[sayac % len(YUMUSAK)])
    acik = HexColor(ACIK[sayac % len(ACIK)])
    ogrenilen = [d[0] for d in sira['dersler'][:n]]
    kem = [e for e in emoji_ayir(hk.get('kapak_emoji', ''))][:4]

    def kapak(c):
        c.setFillColor(renk); c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(Color(1, 1, 1, alpha=0.13))
        c.circle(W - 60, H - 80, 140, stroke=0, fill=1); c.circle(50, 180, 110, stroke=0, fill=1)
        c.setFillColor(white); c.setFont('Andika-Bold', 16)
        c.drawCentredString(W / 2, H - 90, 'Hikâye %d  ·  Ders %d sonrası  ·  Yeni harf: %s %s' % (sayac + 1, n, harf, tr_buyuk(harf)))
        yuvarlak_kutu(c, M + 10, H - 340, W - 2 * M - 20, 220, 30, white)
        boy = 130 if len(kem) <= 2 else 100
        tw = len(kem) * boy + (len(kem) - 1) * 14
        x = W / 2 - tw / 2
        for e in kem:
            emoji_ciz(c, e, x, H - 230 - boy / 2, boy); x += boy + 14
        fs = 44
        while sw(hk['baslik'], 'Andika-Bold', fs) > W - 2 * M - 40:
            fs -= 1
        yuvarlak_kutu(c, M + 10, H - 470, W - 2 * M - 20, 100, 30, white)
        renkli_ortala(c, W / 2, H - 435, hk['baslik'], fs, harf, font='Andika-Bold')
        c.setFillColor(white); c.setFont('Andika-Bold', 15)
        c.drawCentredString(W / 2, H - 510, 'Bu hikâyede okuyacağımız harfler')
        boy, ara, sn = 38, 8, 10
        y = H - 565
        for sat in [ogrenilen[i:i + sn] for i in range(0, len(ogrenilen), sn)]:
            tw = len(sat) * boy + (len(sat) - 1) * ara
            x = W / 2 - tw / 2
            for h in sat:
                harf_karosu(c, x, y, boy, h, white, KIRMIZI if h == harf else LACIVERT)
                x += boy + ara
            y -= boy + ara
    dizi.ekle(kapak)

    sahneler = [s for s in hk['sahneler'] if s.get('cumleler')]
    gen = W - 2 * M - 60
    for si, sh in enumerate(sahneler):
        def fn(c, sh=sh, si=si):
            c.setFillColor(acik); c.rect(0, 46, W, H - 46, stroke=0, fill=1)
            c.setFillColor(renk); c.setFont('Andika-Bold', 13)
            c.drawString(M, H - 50, hk['baslik'])
            c.drawRightString(W - M, H - 50, '%d / %d' % (si + 1, len(sahneler)))
            kx, ky, kw, kh = M, 70, W - 2 * M, H - 140
            yuvarlak_kutu(c, kx, ky, kw, kh, 30, white, renk, 2.5)
            em = emoji_ayir(sh.get('emoji', ''))[:4]
            boy = 96 if len(em) <= 3 else 80
            tw = len(em) * boy + max(0, len(em) - 1) * 18
            x = W / 2 - tw / 2
            for e in em:
                emoji_ciz(c, e, x, ky + kh - boy - 30, boy); x += boy + 18
            alan = kh - boy - 80
            FS = 32
            while FS > 18:
                sat = []
                for j, s_ in enumerate(sh['cumleler']):
                    if j: sat.append(None)
                    sat += sar(s_, 'Andika', FS, gen)
                lead = FS * 1.5
                top = sum(lead if t else lead * 0.45 for t in sat)
                if top <= alan:
                    break
                FS -= 1
            y = ky + 30 + alan / 2 + top / 2
            for t in sat:
                if t is None:
                    y -= lead * 0.45; continue
                y -= lead
                renkli_yaz(c, kx + 30, y + lead * 0.3, t, FS, harf)
        dizi.ekle(fn)

    sorular = hk.get('sorular') or []
    if sorular:
        def kon(c):
            c.setFillColor(acik); c.rect(0, 46, W, H - 46, stroke=0, fill=1)
            yuvarlak_kutu(c, M, H - 36 - 56, W - 2 * M, 56, 16, renk)
            c.setFillColor(white); c.setFont('Andika-Bold', 26)
            c.drawCentredString(W / 2, H - 36 - 38, 'Hadi konuşalım')
            y = H - 120
            fs = 26 if len(sorular) <= 3 else 22
            for q in sorular:
                cev_sat = sar(q.get('cevap', ''), 'Andika', fs, W - 2 * M - 60)
                qs = sar('Öğretmen sorar: ' + q.get('soru', ''), 'Andika', 11.5, W - 2 * M - 36)
                qh = 22 + len(qs) * 15 + len(cev_sat) * fs * 1.45 + 14
                yuvarlak_kutu(c, M, y - qh, W - 2 * M, qh, 18, white, renk, 1.5)
                c.setFillColor(HexColor('#6B7785')); c.setFont('Andika', 11.5)
                yy = y - 22
                for t in qs:
                    c.drawString(M + 18, yy, t); yy -= 15
                for t in cev_sat:
                    yy -= fs * 1.2
                    renkli_yaz(c, M + 30, yy + 6, t, fs, harf)
                    yy -= fs * 0.25
                y -= qh + 14
            ad, url = calisma_sec('hikaye', sayac)
            qr_bandi(c, ALT_SINIR + 4, ad, url, '#E76F51')
        dizi.ekle(kon)


def emoji_ayir(s):
    import regex
    return [g for g in regex.findall(r'\X', s or '') if g.strip()]


def hikaye_kapak(dizi, hikayeli, emojiler):
    def fn(c):
        c.setFillColor(HexColor('#FFF8EC')); c.rect(0, 0, W, H, stroke=0, fill=1)
        for (x, y, r, col) in [(70, H - 60, 100, '#E2EEF9'), (W - 50, H - 220, 110, '#FCE7E1'),
                               (W - 70, 240, 90, '#E6F4E6'), (40, 330, 70, '#EEE8F8')]:
            c.setFillColor(HexColor(col)); c.circle(x, y, r, stroke=0, fill=1)
        yuvarlak_kutu(c, M, H - 250, W - 2 * M, 170, 26, HexColor('#E76F51'))
        c.setFillColor(white)
        c.setFont('Andika-Bold', 40); c.drawCentredString(W / 2, H - 150, 'Hece Hece')
        c.setFont('Andika-Bold', 34); c.drawCentredString(W / 2, H - 192, 'Okuma Hikâyeleri')
        c.setFont('Andika', 14); c.drawCentredString(W / 2, H - 225, 'Barış Öğretmen Setleri')
        em = [e for e in emojiler if e][:12]
        boy, ara = 54, 14
        for r in range(2):
            sat = em[r * 6:(r + 1) * 6]
            if not sat:
                continue
            tw = len(sat) * boy + (len(sat) - 1) * ara
            x = W / 2 - tw / 2
            for e in sat:
                emoji_ciz(c, e, x, H - 330 - r * (boy + 16), boy); x += boy + ara
        c.setFillColor(LACIVERT); c.setFont('Andika-Bold', 16)
        c.drawCentredString(W / 2, H - 450, '%d hikâye · büyük harflerle, resimli' % len(hikayeli))
        c.setFont('Andika', 12.5); c.setFillColor(HexColor('#4A5868'))
        c.drawCentredString(W / 2, H - 472, 'Her hikâye, o derse kadar öğrenilen harflerle yazıldı.')
        q = 132
        qx, qy = W / 2 - q / 2, 116
        yuvarlak_kutu(c, qx - 12, qy - 12, q + 24, q + 24, 14, white, HexColor('#D5DCE4'))
        qr_ciz(c, qx, qy, q)
        c.setFont('Andika', 12.5); c.setFillColor(HexColor('#4A5868'))
        c.drawCentredString(W / 2, 84, 'Daha fazlası için: ')
        c.setFont('Andika-Bold', 13); c.setFillColor(HexColor('#2C6FB7'))
        c.drawCentredString(W / 2, 66, SITE_KISA)
        c.linkURL(SITE, (W / 2 - 110, 60, W / 2 + 110, 98), relative=0)
    dizi.ekle(fn)


def nasil_okunur(dizi, hikayeli):
    def fn(c):
        yuvarlak_kutu(c, M, H - 36 - 44, W - 2 * M, 44, 12, HexColor('#3A86C8'))
        c.setFillColor(white); c.setFont('Andika-Bold', 19)
        c.drawString(M + 18, H - 36 - 29, 'Nasıl okunur?')
        y = H - 36 - 44 - 18
        y = paragraf(c, 'Bu kitapçıktaki her hikâye, çalışma kitabındaki bir derse eşlik eder ve yalnızca o derse kadar öğrenilen '
                        'harflerle yazılmıştır. Hikâyeyi, ilgili dersin çalışma sayfaları bittikten sonra okuyun.', M, y, W - 2 * M, size=12)
        y -= 10
        adimlar = [
            ('1', 'Kapağa birlikte bakın', 'Resmi konuşun, başlığı siz okuyun. Kapakta o güne kadar öğrenilen harfler var.'),
            ('2', 'Kırmızı harfi bulun', 'Kırmızı harf, o derste öğrenilen yeni harftir. Çocuk sayfadaki kırmızı harfleri parmağıyla göstersin.'),
            ('3', 'Önce siz, sonra birlikte', 'Bir cümleyi siz okuyun, sonra birlikte okuyun, en son çocuk tek başına okusun.'),
            ('4', 'Parmakla takip', 'Çocuk okurken parmağını kelimenin altında soldan sağa kaydırsın. Sesleri uzatarak birleştirebilir.'),
            ('5', 'Hadi konuşalım', 'Sondaki soruları siz okuyun (küçük yazı). Büyük yazılı cevabı çocuk okusun ya da kendi sözleriyle anlatsın.'),
            ('6', 'Kısa ve keyifli', 'Günde bir hikâye ya da birkaç sayfa yeterlidir. Aynı hikâyeyi tekrar tekrar okumak akıcılığı destekler.'),
        ]
        for no, bas, ac in adimlar:
            renk = HexColor(YUMUSAK[int(no) % len(YUMUSAK)])
            c.setFillColor(renk); c.circle(M + 18, y - 22, 16, stroke=0, fill=1)
            c.setFillColor(white); c.setFont('Andika-Bold', 17); c.drawCentredString(M + 18, y - 28, no)
            c.setFillColor(renk); c.setFont('Andika-Bold', 15); c.drawString(M + 46, y - 18, bas)
            y2 = paragraf(c, ac, M + 46, y - 24, W - 2 * M - 46, size=11.5)
            y = min(y2, y - 44) - 14
        y -= 4
        c.setFillColor(HexColor('#2A9D8F')); c.setFont('Andika-Bold', 14.5)
        c.drawString(M, y - 14, 'Hikâyeler'); y -= 24
        c.setFont('Andika', 10.5)
        sut = 2; gen = (W - 2 * M) / sut
        satir_n = math.ceil(len(hikayeli) / sut)
        for i, d in enumerate(hikayeli):
            k, r = divmod(i, satir_n)
            c.setFillColor(LACIVERT)
            c.drawString(M + k * gen, y - r * 14.5, '%d. %s  (ders %d sonrası)' % (i + 1, d['baslik'], d['ders']))
    dizi.ekle(fn)


# ---------------------------------------------------------------- PNG kapaklar
def pdf_sayfa_png(pdf, sayfa, dpi, cikis):
    on = cikis[:-4]
    subprocess.run(['pdftoppm', '-png', '-r', str(dpi), '-f', str(sayfa), '-l', str(sayfa), '-singlefile', pdf, on],
                   check=True)
    return on + '.png'


def pil_emoji(e, boy):
    y = emoji_png(e, 160)
    if not y:
        return None
    return Image.open(y).convert('RGBA').resize((boy, boy), Image.LANCZOS)


def png_kapak(yol, baslik1, baslik2, sayfa_sayisi, onizlemeler, renk, ek_rozet=None):
    Wp, Hp = 1280, 720
    img = Image.new('RGB', (Wp, Hp), '#FFF8EC')
    d = ImageDraw.Draw(img)
    for (x, y, r, col) in [(80, 60, 160, '#FCE7E1'), (1220, 680, 200, '#E2EEF9'), (650, 760, 140, '#E6F4E6')]:
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    # önizlemeler (sağda, yelpaze)
    th = 410
    resimler = []
    for p in onizlemeler:
        im = Image.open(p).convert('RGB')
        oran = th / im.size[1]
        im = im.resize((int(im.size[0] * oran), th), Image.LANCZOS)
        resimler.append(im)
    acilar = [8, -4, 3, -7][:len(resimler)]
    merkezler = [(900, 395), (1010, 370), (1120, 395), (1060, 400)][:len(resimler)]
    if len(resimler) == 3:
        merkezler = [(895, 405), (1025, 380), (1150, 405)]
        acilar = [7, -2, -8]
    for im, a, (cx, cy) in zip(resimler, acilar, merkezler):
        golge = Image.new('RGBA', (im.size[0] + 40, im.size[1] + 40), (0, 0, 0, 0))
        gd = ImageDraw.Draw(golge)
        gd.rectangle((20, 26, 20 + im.size[0], 26 + im.size[1]), fill=(0, 0, 0, 70))
        golge = golge.filter(ImageFilter.GaussianBlur(9))
        kart = Image.new('RGBA', golge.size, (0, 0, 0, 0))
        kart.alpha_composite(golge)
        cer = Image.new('RGBA', (im.size[0] + 8, im.size[1] + 8), (255, 255, 255, 255))
        cer.paste(im, (4, 4))
        kart.alpha_composite(cer, (16, 16))
        kart = kart.rotate(a, resample=Image.BICUBIC, expand=True)
        img.paste(kart, (cx - kart.size[0] // 2, cy - kart.size[1] // 2), kart)
    d = ImageDraw.Draw(img)
    fB = lambda s: ImageFont.truetype(FONT_B, s)
    fR = lambda s: ImageFont.truetype(FONT_R, s)
    x0 = 58
    # üst etiket
    ust = 'Barış Öğretmen Setleri'
    d.rounded_rectangle((x0, 52, x0 + 48 + int(d.textlength(ust, font=fB(29))), 104), 26, fill=renk)
    d.text((x0 + 24, 57), ust, font=fB(29), fill='white')
    # başlık
    y = 140
    for s, fs in ((baslik1, 92), (baslik2, 66)):
        f = fB(fs)
        while d.textlength(s, font=f) > 610 and fs > 30:
            fs -= 2; f = fB(fs)
        d.text((x0, y), s, font=f, fill='#1D3557')
        y += int(fs * 1.18)
    # hedef kitle etiketi
    y += 14
    et = 'Okul öncesi · 1. sınıf · Özel eğitim'
    f = fB(34)
    tw = d.textlength(et, font=f)
    d.rounded_rectangle((x0, y, x0 + tw + 48, y + 62), 31, fill='#FFFFFF', outline=renk, width=4)
    d.text((x0 + 24, y + 8), et, font=f, fill=renk)
    y += 92
    # rozetler
    rozetler = [('✏️', 'Yazdır, kalemle yaz'), ('📖', '%d sayfa' % sayfa_sayisi)]
    if ek_rozet:
        rozetler.append(ek_rozet)
    x = x0
    f = fB(32)
    for e, t in rozetler:
        tw = d.textlength(t, font=f)
        wbox = 50 + 44 + tw + 24
        if x + wbox > 700:
            x = x0; y += 82
        d.rounded_rectangle((int(x), y, int(x + wbox), y + 66), 33, fill='#1D3557')
        em = pil_emoji(e, 44)
        if em:
            img.paste(em, (int(x + 20), int(y + 11)), em)
        d.text((x + 74, y + 10), t, font=f, fill='white')
        x += wbox + 16
    # alt: site adresi
    d.text((x0, 655), 'baris-ogretmen.github.io/site-1', font=fB(28), fill='#2C6FB7')
    img.save(yol, optimize=True)


# ---------------------------------------------------------------- ana
def main():
    deneme = '--deneme' in sys.argv
    bekle = '--bekle' in sys.argv
    sira = sira_yukle()
    dersler = icerik_yukle(deneme=deneme, bekle=bekle)
    if not dersler:
        print('HATA: hiç içerik yok'); sys.exit(1)
    ipuclari = {i + 1: d[1] for i, d in enumerate(sira['dersler'])}
    harfler_sira = [d[0] for d in sira['dersler']]
    os.makedirs(CIKTI, exist_ok=True); os.makedirs(ONIZ, exist_ok=True)
    eksik = [n for n in range(1, 30) if n not in dersler]
    if eksik:
        print('UYARI: içeriği olmayan dersler:', eksik)
    sonuc = {}
    kitaplar = [('1', sira['kitap1'], 'Hece_Hece_Okuma_Yazma_1_Kitap.pdf', '#2A9D8F'),
                ('2', sira['kitap2'], 'Hece_Hece_Okuma_Yazma_2_Kitap.pdf', '#8E6FC9')]
    sayfa_bilgi = {}
    for no, (a, b), ad, renk in kitaplar:
        dizi = SayfaDizisi()
        kitap_adi = 'Hece Hece Okuma–Yazma · %s. Kitap' % no
        harfler = harfler_sira[a - 1:b]
        emojiler = [(dersler.get(n) or {}).get('resimli_kelime', {}).get('emoji', '') for n in range(a, b + 1)]
        kapak_sayfasi(dizi, 'Hece Hece Okuma–Yazma', '%s. Kitap · Ders %d–%d' % (no, a, b), harfler, emojiler, renk)
        not_sayfasi(dizi, sira, (a, b), 'calisma')
        bilgi = {}
        for n in range(a, b + 1):
            if n not in dersler:
                continue
            bilgi[n] = len(dizi.sayfalar) + 1
            ders_sayfalari(dizi, dersler[n], ipuclari[n], kitap_adi)
        yol = os.path.join(CIKTI, ad)
        N = dizi.yaz(yol, 'Hece Hece Okuma–Yazma · %s. Kitap' % no)
        sonuc[ad] = N
        sayfa_bilgi[ad] = bilgi
    # hikâyeler
    dizi = SayfaDizisi()
    hikayeli = hikaye_yukle()
    hikaye_kapak(dizi, hikayeli, [(emoji_ayir(d.get('kapak_emoji', '')) or [''])[0] for d in hikayeli])
    nasil_okunur(dizi, hikayeli)
    hk_ilk = None
    for i, d in enumerate(hikayeli):
        if i == 0:
            hk_ilk = len(dizi.sayfalar) + 1
        hikaye_bolumleri2(dizi, d, sira, i)
    ad_h = 'Hece_Hece_Okuma_Hikayeleri.pdf'
    sonuc[ad_h] = dizi.yaz(os.path.join(CIKTI, ad_h), 'Hece Hece Okuma Hikâyeleri')

    # önizlemeler (60 dpi)
    on = []
    k1 = os.path.join(CIKTI, 'Hece_Hece_Okuma_Yazma_1_Kitap.pdf')
    k2 = os.path.join(CIKTI, 'Hece_Hece_Okuma_Yazma_2_Kitap.pdf')
    kh = os.path.join(CIKTI, ad_h)
    b1 = sayfa_bilgi['Hece_Hece_Okuma_Yazma_1_Kitap.pdf']
    b2 = sayfa_bilgi['Hece_Hece_Okuma_Yazma_2_Kitap.pdf']
    tanit1 = b1.get(5) or (list(b1.values())[-1] if b1 else 3)
    tanit2 = b2.get(19) or (list(b2.values())[0] if b2 else 3)
    istek = [(k1, 1, 'k1_kapak'), (k1, 2, 'k1_not'), (k1, tanit1, 'k1_tanitim'), (k1, tanit1 + 1, 'k1_hece'),
             (k1, tanit1 + 2, 'k1_kelime'), (k1, tanit1 + 3, 'k1_cumle'),
             (k2, 1, 'k2_kapak'), (k2, tanit2, 'k2_tanitim'), (k2, tanit2 + 2, 'k2_kelime'),
             (kh, 1, 'h_kapak'), (kh, 2, 'h_nasil'), (kh, 3, 'h_ayrac'), (kh, 4, 'h_sayfa'), (kh, 6, 'h_sayfa2')]
    for pdf, s, ad in istek:
        try:
            on.append(pdf_sayfa_png(pdf, s, 60, os.path.join(ONIZ, ad + '.png')))
        except Exception as e:
            print('önizleme yok', ad, e)
    # son sayfa: hadi konuşalım
    try:
        pdf_sayfa_png(kh, sonuc[ad_h], 60, os.path.join(ONIZ, 'h_konusalim.png'))
    except Exception:
        pass

    # PNG kapaklar için daha net küçük resimler
    tmp = os.path.join(CIKTI, '_tmp'); os.makedirs(tmp, exist_ok=True)
    def kucuk(pdf, s, ad):
        return pdf_sayfa_png(pdf, s, 90, os.path.join(tmp, ad + '.png'))
    p1 = [kucuk(k1, tanit1 + 2, 'a2'), kucuk(k1, tanit1, 'a1'), kucuk(k1, 1, 'a0')]
    p2 = [kucuk(k2, tanit2 + 2, 'b2'), kucuk(k2, tanit2, 'b1'), kucuk(k2, 1, 'b0')]
    ph = [kucuk(kh, 4, 'c2'), kucuk(kh, 3, 'c1'), kucuk(kh, 1, 'c0')]
    ps = [kucuk(kh, 1, 's2'), kucuk(k2, 1, 's1'), kucuk(k1, 1, 's0')]
    png_kapak(os.path.join(CIKTI, 'kapak_1_kitap.png'), 'Hece Hece', 'Okuma–Yazma · 1. Kitap',
              sonuc['Hece_Hece_Okuma_Yazma_1_Kitap.pdf'], p1, '#2A9D8F', ('🔤', '%d harf' % len(b1)))
    png_kapak(os.path.join(CIKTI, 'kapak_2_kitap.png'), 'Hece Hece', 'Okuma–Yazma · 2. Kitap',
              sonuc['Hece_Hece_Okuma_Yazma_2_Kitap.pdf'], p2, '#8E6FC9', ('🔤', '%d harf' % len(b2)))
    png_kapak(os.path.join(CIKTI, 'kapak_hikayeler.png'), 'Hece Hece', 'Okuma Hikâyeleri',
              sonuc[ad_h], ph, '#E76F51', ('🐣', '%d hikâye' % len(hikayeli)))
    png_kapak(os.path.join(CIKTI, 'kapak_set.png'), 'Hece Hece', 'Okuma–Yazma Seti',
              sum(sonuc.values()), ps, '#3A86C8', ('📚', '3 kitap · 29 harf'))
    shutil.rmtree(tmp, ignore_errors=True)

    print('\n=== SONUÇ ===')
    for ad, N in sonuc.items():
        yol = os.path.join(CIKTI, ad)
        print('%-40s %4d sayfa  %7.1f KB' % (ad, N, os.path.getsize(yol) / 1024))
    for ad in ('kapak_1_kitap.png', 'kapak_2_kitap.png', 'kapak_hikayeler.png', 'kapak_set.png'):
        print('%-40s %7.1f KB' % (ad, os.path.getsize(os.path.join(CIKTI, ad)) / 1024))
    print('Hikâye sayısı:', len(hikayeli))


if __name__ == '__main__':
    main()
