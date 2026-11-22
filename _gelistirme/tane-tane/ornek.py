# Tane Tane Matematik · ÖRNEKTİR damgalı örnek sayfalar PDF'i
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
pdfmetrics.registerFont(TTFont('DB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('D', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
C = '/home/claude/mat/cikti/Tane_Tane_Matematik_'
MAIL = 'barilkay466@gmail.com'
SEC = [('0_Ogretmen_Veli_Rehberi', [3]), ('1_Sayilarla_Tanisiyorum', [3, 4]), ('2_Ona_Kadar', [3, 30]),
       ('3_Toplama_Cikarma', [5, 18]), ('4_Sekiller_Oruntuler', [3, 23]), ('5_Kes_Kullan', [7])]
W, H = A4
def damga():
    b = io.BytesIO(); c = canvas.Canvas(b, pagesize=A4)
    c.saveState(); c.translate(W / 2, H / 2); c.rotate(35); c.setFillColorRGB(.86, .15, .15, alpha=.16)
    c.setFont('DB', 110); c.drawCentredString(0, -30, 'ÖRNEKTİR'); c.restoreState()
    c.setFillColorRGB(.86, .15, .15); c.roundRect(W - 172, H - 34, 160, 24, 12, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); c.setFont('DB', 11); c.drawCentredString(W - 92, H - 26, 'ÖRNEK SAYFA')
    c.save(); b.seek(0); return PdfReader(b).pages[0]
def kapak():
    b = io.BytesIO(); c = canvas.Canvas(b, pagesize=A4)
    c.setFillColorRGB(.94, .99, .96); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.drawImage('/home/claude/mat/kapaklar/tane-tane-kapak-set.png', 30, H - 360, width=W - 60, height=(W - 60) * 720 / 1280, preserveAspectRatio=True, mask='auto')
    c.setFillColorRGB(.06, .09, .16); c.setFont('DB', 30); c.drawCentredString(W / 2, H - 410, 'Örnek Sayfalar')
    c.setFont('D', 14)
    for i, s in enumerate(['Bu dosyada setin 6 kitabından seçilmiş birkaç örnek sayfa var.',
                           'Tam set: 6 kitap, 219 sayfa (okul öncesi · 1. sınıf · özel eğitim).',
                           'Okulunuz, sınıfınız ya da çocuğunuz için seti edinmek isterseniz:']):
        c.drawCentredString(W / 2, H - 450 - i * 24, s)
    c.setFillColorRGB(.09, .64, .29); c.roundRect(W / 2 - 160, H - 560, 320, 40, 20, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); c.setFont('DB', 16); c.drawCentredString(W / 2, H - 546, MAIL)
    c.setFillColorRGB(.2, .25, .33); c.setFont('D', 12)
    c.drawCentredString(W / 2, H - 600, 'Her çocuğun öğrenme profiline göre uyarlanmış setler de hazırlanır.')
    c.drawCentredString(W / 2, 60, 'Barış Öğretmen · baris-ogretmen.github.io/site-1')
    c.save(); b.seek(0); return PdfReader(b).pages[0]
w = PdfWriter(); w.add_page(kapak()); d = damga(); n = 1
for f, pages in SEC:
    r = PdfReader(C + f + '.pdf')
    for p in pages:
        pg = r.pages[p - 1]; pg.merge_page(d); w.add_page(pg); n += 1
w.add_metadata({'/Title': 'Tane Tane Matematik · Örnek Sayfalar', '/Author': 'Barış Öğretmen'})
out = '/home/claude/mat/cikti/Tane_Tane_Matematik_ORNEK.pdf'
w.write(out); print(out, n, 'sayfa')
