#!/usr/bin/env python3
"""Sitede yayınlanacak ÖRNEK PDF: seçilmiş sayfalar + çapraz 'ÖRNEKTİR' damgası + iletişim kapağı."""
import io, subprocess, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color, HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
K = '/home/claude/aa'; C = K + '/cikti'
pdfmetrics.registerFont(TTFont('D', K + '/fonts/DidactGothic-Regular.ttf'))
W, H = A4
EPOSTA = 'barilkay466@gmail.com'


def bul(pdf, metin):
    import re
    out = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    hedef = re.sub(r'\s+', ' ', metin)
    for i, s in enumerate(out):
        if hedef in re.sub(r'\s+', ' ', s):
            return i
    sys.exit('bulunamadı: ' + metin)


def damga():
    b = io.BytesIO(); c = canvas.Canvas(b, pagesize=A4)
    c.saveState(); c.translate(W / 2, H / 2); c.rotate(38)
    c.setFillColor(Color(0.85, 0.16, 0.16, alpha=0.13)); c.setFont('D', 118)
    c.drawCentredString(0, -40, 'ÖRNEKTİR')
    c.setFont('D', 22); c.setFillColor(Color(0.85, 0.16, 0.16, alpha=0.25))
    c.drawCentredString(0, -90, 'Setin tamamı için: ' + EPOSTA)
    c.restoreState(); c.save(); b.seek(0)
    return PdfReader(b).pages[0]


def bilgi_kapagi(baslik, alt, icerik):
    b = io.BytesIO(); c = canvas.Canvas(b, pagesize=A4)
    c.setFillColor(HexColor('#FFF6E9')); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(HexColor('#2A9D8F')); c.roundRect(40, H - 260, W - 80, 190, 26, stroke=0, fill=1)
    c.setFillColor(white); c.setFont('D', 36); c.drawCentredString(W / 2, H - 150, baslik)
    c.setFont('D', 17); c.drawCentredString(W / 2, H - 190, alt)
    c.setFont('D', 13); c.drawCentredString(W / 2, H - 222, 'Barış Öğretmen Setleri · ÖRNEK SAYFALAR')
    y = H - 320
    c.setFillColor(HexColor('#1D3557')); c.setFont('D', 15)
    for s in icerik:
        c.drawString(70, y, '•  ' + s); y -= 28
    c.setFillColor(HexColor('#D62828')); c.roundRect(60, 150, W - 120, 110, 20, stroke=0, fill=1)
    c.setFillColor(white); c.setFont('D', 20)
    c.drawCentredString(W / 2, 222, 'Bu dosya tanıtım amaçlı örnektir.')
    c.setFont('D', 16); c.drawCentredString(W / 2, 190, 'Setin tamamı ve okul fiyatı için: ' + EPOSTA)
    c.linkURL('mailto:' + EPOSTA, (60, 150, W - 60, 260), relative=0)
    c.setFillColor(HexColor('#2C6FB7')); c.setFont('D', 14)
    c.drawCentredString(W / 2, 110, 'baris-ogretmen.github.io/site-1')
    c.linkURL('https://baris-ogretmen.github.io/site-1/', (W / 2 - 130, 100, W / 2 + 130, 130), relative=0)
    c.save(); b.seek(0)
    return PdfReader(b).pages[0]


def main():
    k1 = C + '/Hece_Hece_Okuma_Yazma_1_Kitap.pdf'; k2 = C + '/Hece_Hece_Okuma_Yazma_2_Kitap.pdf'
    kh = C + '/Hece_Hece_Okuma_Hikayeleri.pdf'
    R = {p: PdfReader(p) for p in (k1, k2, kh)}
    sec = [(k1, 0), (k1, 1), (k1, bul(k1, 'Ders 1  ·  Yeni harfimiz')), (k1, bul(k1, 'Ders 1  ·  Dinle ve bul')),
           (k1, bul(k1, 'Ders 9  ·  Yeni harfimiz')), (k1, bul(k1, 'Ders 9  ·  Cümleler')),
           (k2, 0), (k2, bul(k2, 'Ders 16  ·  Yeni harfimiz')), (k2, bul(k2, 'Ders 16  ·  Kelimeler')),
           (kh, 0)]
    hs = bul(kh, 'Ders 25 sonrası')  # bir uzun hikâyeden kapak + 3 sahne
    sec += [(kh, hs), (kh, hs + 1), (kh, hs + 3), (kh, hs + 7)]
    w = PdfWriter()
    w.add_page(bilgi_kapagi('Hece Hece Okuma–Yazma', 'Önce 8 ünlü, sonra hece hece okuma',
                            ['1. Kitap: 8 ünlü + l n k m t r y (15 ders, %d sayfa)' % len(R[k1].pages),
                             '2. Kitap: s d z b ç g ş p c h v f ğ j (14 ders, %d sayfa)' % len(R[k2].pages),
                             'Okuma Hikâyeleri: 19 resimli, nakaratlı hikâye (%d sayfa)' % len(R[kh].pages),
                             'Her derste: harf tanıtımı, Dinle ve bul, hece, kelime, cümle, yazma',
                             'Her derste kare kodla tablette oynanacak çalışma',
                             'Okul öncesi sonu, 1. sınıf ve özel gereksinimli çocuklar için']))
    dm = damga()
    for pdf, i in sec:
        p = R[pdf].pages[i]; p.merge_page(dm); w.add_page(p)
    w.add_metadata({'/Title': 'Hece Hece Okuma–Yazma · ÖRNEK', '/Author': 'Barış Öğretmen'})
    with open(C + '/Hece_Hece_Okuma_Yazma_ORNEK.pdf', 'wb') as f:
        w.write(f)
    print('örnek sayfa:', len(w.pages))


if __name__ == '__main__':
    main()
