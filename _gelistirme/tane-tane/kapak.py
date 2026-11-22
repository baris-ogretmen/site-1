# Her kitap için 1280x720 site kapağı + set kapağı (PNG)
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
C = '/home/claude/mat/cikti/'; O = '/home/claude/mat/kapaklar/'; os.makedirs(O, exist_ok=True)
F = lambda w, s: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{w}.otf', s)
KIT = [('0', 'Tane_Tane_Matematik_0_Ogretmen_Veli_Rehberi.pdf', 'Öğretmen ve\nVeli Rehberi', 'Seti en iyi nasıl kullanırım?', (219, 39, 119), [1, 3, 6]),
       ('1', 'Tane_Tane_Matematik_1_Sayilarla_Tanisiyorum.pdf', 'Sayılarla\nTanışıyorum', "1. Kitap · 1'den 5'e", (22, 163, 74), [1, 3, 4]),
       ('2', 'Tane_Tane_Matematik_2_Ona_Kadar.pdf', "On'a Kadar\nSayıyorum", "2. Kitap · 6'dan 10'a", (37, 99, 235), [1, 3, 6]),
       ('3', 'Tane_Tane_Matematik_3_Toplama_Cikarma.pdf', 'Toplama ve\nÇıkarma', "3. Kitap · 10'a, 20'ye kadar", (234, 88, 12), [1, 8, 20]),
       ('4', 'Tane_Tane_Matematik_4_Sekiller_Oruntuler.pdf', 'Şekiller, Örüntüler,\nÖlçme', '4. Kitap · Gör, karşılaştır', (147, 51, 234), [1, 4, 15]),
       ('5', 'Tane_Tane_Matematik_5_Kes_Kullan.pdf', 'Kes, Dokun,\nSay', '5. Kitap · Kartlar, materyaller', (8, 145, 178), [1, 3, 8])]
def sayfa(pdf, n):
    t = f'/tmp/kp_{os.path.basename(pdf)}_{n}'
    subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', '60', '-jpeg', '-singlefile', pdf, t], check=True)
    return Image.open(t + '.jpg').convert('RGB')
def golgeli(im, w, rot):
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    pad = 30; c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 10, pad + im.width, pad + im.height + 10], 14, fill=(0, 0, 0, 90))
    c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(14)))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 14, fill=255)
    c.paste(im, (pad, pad), m); return c.rotate(rot, Image.BICUBIC, expand=True)
def kapak(k, pdf, bas, alt, renk, pg, n_sayfa):
    W, H = 1280, 720; im = Image.new('RGBA', (W, H), (255, 251, 240, 255)); d = ImageDraw.Draw(im)
    acik = tuple(int(c + (255 - c) * .82) for c in renk)
    for (x, y, r) in [(80, 640, 160), (1180, 80, 140), (1100, 690, 120)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=acik + (255,))
    d.rounded_rectangle([60, 46, 60 + d.textlength('Barış Öğretmen · Tane Tane Matematik', font=F('ExtraBold', 24)) + 40, 92], 23, fill=renk)
    d.text((80, 55), 'Barış Öğretmen · Tane Tane Matematik', font=F('ExtraBold', 24), fill='white')
    y = 140
    for i, s in enumerate(bas.split('\n')):
        d.text((60, y), s, font=F('Black', 70 if len(bas) < 26 else 58), fill=(15, 23, 42)); y += 82 if len(bas) < 26 else 70
    d.text((62, y + 6), alt, font=F('Bold', 30), fill=renk); y += 66
    def hap(x, y, t, bg, fg='white', s=26):
        w = d.textlength(t, font=F('ExtraBold', s)) + 40; d.rounded_rectangle([x, y, x + w, y + 50], 25, fill=bg); d.text((x + 20, y + 10), t, font=F('ExtraBold', s), fill=fg); return x + w + 12
    x = hap(60, y + 10, 'Okul öncesi · 1. sınıf · Özel eğitim', (255, 255, 255), renk, 24)
    d.rounded_rectangle([60, y + 10, x - 12, y + 60], 25, outline=renk, width=3)
    x = hap(60, y + 82, f'📄', (15, 23, 42)) if False else hap(60, y + 82, f'{n_sayfa} sayfa', (15, 23, 42))
    hap(x, y + 82, 'Yazdır, kalemle çalış', (15, 23, 42))
    d.text((60, 660), 'baris-ogretmen.github.io/site-1', font=F('Bold', 24), fill=(37, 99, 235))
    sp = [sayfa(pdf, n) for n in pg]
    for i, (s, rot, xx, yy) in enumerate(zip(sp[::-1], [8, -4, 3], [840, 920, 1000], [90, 70, 60])):
        g = golgeli(s, 300, rot); im.alpha_composite(g, (xx - 120 + (i * 10), yy))
    im.convert('RGB').save(O + f'tane-tane-kapak-{k}.png', optimize=True)
def pcount(p): return int([l for l in subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages')][0].split()[-1])
if __name__ == '__main__':
    say = {}
    for k, f, b, a, r, pg in KIT:
        p = C + f
        if not os.path.exists(p): print('yok', f); continue
        n = pcount(p); say[k] = n; kapak(k, p, b, a, r, [min(x, n) for x in pg], n); print(k, n)
    # set kapağı: 6 kitap kapağı (pdf 1. sayfa) yelpaze
    W, H = 1280, 720; im = Image.new('RGBA', (W, H), (247, 253, 249, 255)); d = ImageDraw.Draw(im)
    for (x, y, r, c) in [(120, 620, 180, (220, 252, 231)), (1170, 110, 150, (224, 242, 254)), (1080, 680, 140, (243, 232, 255))]: d.ellipse([x - r, y - r, x + r, y + r], fill=c + (255,))
    d.text((60, 60), 'Tane Tane', font=F('Black', 92), fill=(22, 163, 74)); d.text((60, 160), 'Matematik', font=F('Black', 92), fill=(15, 23, 42))
    d.text((64, 280), 'Okul öncesi · 1. sınıf · Özel eğitim', font=F('Bold', 30), fill=(71, 85, 105))
    top = sum(say.values()); d.rounded_rectangle([60, 340, 470, 396], 28, fill=(15, 23, 42)); d.text((84, 351), f'6 kitap · {top} sayfa', font=F('ExtraBold', 30), fill='white')
    d.text((60, 430), 'Barış Öğretmen', font=F('ExtraBold', 34), fill=(234, 88, 12)); d.text((60, 660), 'baris-ogretmen.github.io/site-1', font=F('Bold', 24), fill=(37, 99, 235))
    ks = [k for k in KIT if os.path.exists(C + k[1])]
    for i, (k, f, *_r) in enumerate(ks):
        g = golgeli(sayfa(C + f, 1), 210, (i - len(ks) / 2) * 5)
        im.alpha_composite(g, (560 + i * 105, int(120 + abs(i - 2.5) * 22)))
    im.convert('RGB').save(O + 'tane-tane-kapak-set.png', optimize=True)
    import json; json.dump(say, open(O + 'sayfalar.json', 'w')); print('toplam', top)
