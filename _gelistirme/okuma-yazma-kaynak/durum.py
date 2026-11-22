#!/usr/bin/env python3
"""WhatsApp durumu için dikey tanıtım görseli (1080x1920)."""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
K = '/home/claude/aa'; C = K + '/cikti'
FB = ImageFont.truetype(K + '/fonts/Andika_700Bold.ttf', 10)
def f(s, b=True): return ImageFont.truetype(K + '/fonts/DidactGothic-Regular.ttf', s)
EM = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
def emoji(e, px):
    im = Image.new('RGBA', (160, 160)); d = ImageDraw.Draw(im)
    d.text((80, 80), e, font=ImageFont.truetype(EM, 109), embedded_color=True, anchor='mm')
    return im.resize((px, px), Image.LANCZOS)
def sayfa(pdf, s, gen):
    o = '/tmp/dur_%s_%d' % (os.path.basename(pdf)[:12], s)
    subprocess.run(['pdftoppm', '-png', '-r', '70', '-f', str(s), '-l', str(s), '-singlefile', pdf, o], check=True)
    im = Image.open(o + '.png').convert('RGB'); h = int(im.height * gen / im.width)
    return im.resize((gen, h), Image.LANCZOS)
def kart(im, r=22):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *im.size), r, fill=255)
    out = Image.new('RGBA', im.size); out.paste(im, (0, 0), m); return out

W, H = 1080, 1920
bg = Image.new('RGB', (W, H), '#FFF6E9'); d = ImageDraw.Draw(bg)
_t = d.text
def _kalin(xy, t, font=None, fill=None, anchor=None, **k):
    return _t(xy, t, font=font, fill=fill, anchor=anchor, stroke_width=max(1, font.size // 28), stroke_fill=fill)
d.text = _kalin
for x, y, r, c in [(90, 130, 220, '#E2EEF9'), (1010, 520, 200, '#FCE7E1'), (60, 1500, 180, '#E6F4E6'), (1030, 1700, 160, '#EEE8F8')]:
    d.ellipse((x - r, y - r, x + r, y + r), fill=c)
d.rounded_rectangle((60, 70, W - 60, 390), 40, fill='#2A9D8F')
d.text((W / 2, 150), 'Hece Hece', font=f(84), fill='white', anchor='mm')
d.text((W / 2, 250), 'Okuma–Yazma Seti', font=f(70), fill='white', anchor='mm')
d.text((W / 2, 335), 'Barış Öğretmen Setleri', font=f(36, False), fill='#E3F4F1', anchor='mm')
# ünlüler
d.text((W / 2, 455), 'Önce 8 ünlü, sonra hece hece okuma', font=f(42), fill='#1D3557', anchor='mm')
renk = ['#2A9D8F', '#E9A23B', '#8E6FC9', '#E76F51', '#3A86C8', '#5BAE5B', '#D45D8C', '#2C9FB8']
x0 = W / 2 - (8 * 100 + 7 * 14) / 2
for i, h in enumerate('aeiouıöü'):
    x = x0 + i * 114
    d.rounded_rectangle((x, 500, x + 100, 600), 22, fill=renk[i])
    d.text((x + 50, 546), h, font=f(66), fill='white', anchor='mm')
# sayfa önizlemeleri
k1 = C + '/Hece_Hece_Okuma_Yazma_1_Kitap.pdf'; kh = C + '/Hece_Hece_Okuma_Hikayeleri.pdf'
p = [sayfa(k1, 3, 300), sayfa(k1, 4, 300), sayfa(kh, 139, 300)]
for i, im in enumerate(p):
    x = 60 + i * 330; y = 650 + (30 if i == 1 else 0)
    sh = Image.new('RGBA', (im.width + 40, im.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 26, im.width + 20, im.height + 26), 22, fill=(0, 0, 0, 70))
    bg.paste(sh.filter(ImageFilter.GaussianBlur(10)), (x - 20, y - 20), sh.filter(ImageFilter.GaussianBlur(10)))
    k = kart(im); bg.paste(k, (x, y), k)
y = 1130
for e, t in [('📘', '1. Kitap: 8 ünlü + l n k m t r y'), ('📗', '2. Kitap: s d z b ç g ş p c h v f ğ j'),
             ('📚', '19 resimli hikâye: nakaratlı, eğlenceli'), ('✏️', 'Dinle-bul, hece, kelime, cümle, yazma')]:
    em = emoji(e, 62); bg.paste(em, (100, y - 31), em)
    d.text((185, y), t, font=f(40), fill='#1D3557', anchor='lm'); y += 86
d.text((W / 2, y + 10), 'Özel gereksinimli çocuklar ve 1. sınıf için', font=f(34, False), fill='#4A5868', anchor='mm')
d.text((W / 2, y + 58), 'Set için: barilkay466@gmail.com', font=f(36), fill='#D62828', anchor='mm')
# QR + adres
q = qrcode.make('https://baris-ogretmen.github.io/site-1/', box_size=9, border=2).convert('RGB').resize((260, 260))
d.rounded_rectangle((W / 2 - 150, 1555, W / 2 + 150, 1855), 30, fill='white', outline='#D5DCE4', width=3)
bg.paste(q, (int(W / 2 - 130), 1575))
d.rounded_rectangle((60, 1868, W - 60, 1915), 22, fill='#2C6FB7')
d.text((W / 2, 1891), 'baris-ogretmen.github.io/site-1', font=f(36), fill='white', anchor='mm')
bg.save(C + '/whatsapp_durum.png'); print('ok')
