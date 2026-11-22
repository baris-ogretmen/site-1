#!/usr/bin/env python3
"""Kullanım: python3 dogrula.py dosya.json ...  → her metin yalnızca öğrenilmiş harflerle mi? (ders ve hikâye dosyaları)"""
import json,sys,re
S=json.load(open('/home/claude/aa/sira.json',encoding='utf-8'))
H=[d[0] for d in S['dersler']]
YASAK=['savaş','mete','enes','beyazıt','poyraz','sarp','mustafa','aras','metehan','resul','basara']
def kucuk(t): return t.replace('I','ı').replace('İ','i').lower()
def harfler(t): return set(c for c in kucuk(t).replace('â','a').replace('î','i').replace('û','u') if c.isalpha())
hata=0
def bak(n,tur,m):
    global hata
    izin=set(H[:n]); fazla=harfler(m)-izin
    if re.search(r'\d',m): fazla.add('rakam')
    if fazla: print(f'ders {n} [{tur}] "{m}" → öğrenilmemiş: {"".join(sorted(fazla))}'); hata+=1
    for y in YASAK:
        if re.search(r'\b'+y+r'\b',kucuk(m)): print(f'ders {n} yasak kelime/ad: {y}'); hata+=1
for f in sys.argv[1:]:
    for D in json.load(open(f,encoding='utf-8')):
        n=D['ders']
        if 'sahneler' in D:  # hikâye dosyası
            bak(n,'baslik',D['baslik'])
            for s in D['sahneler']:
                for x in s['cumleler']: bak(n,'hikaye',x)
            for q in D.get('sorular',[]): bak(n,'cevap',q['cevap'])
            continue
        for k in ('heceler','kelimeler','cumleler'):
            for x in D.get(k,[]): bak(n,k,x)
        bak(n,'resimli',D['resimli_kelime']['kelime'])
        if H[n-1] not in kucuk(' '.join(D['kelimeler'])): print(f'ders {n}: yeni harf "{H[n-1]}" kelimelerde yok'); hata+=1
        if n>=9 and len(D.get('cumleler',[]))<3: print(f'ders {n}: en az 3 cümle gerekli'); hata+=1
print('HATA:',hata); sys.exit(1 if hata else 0)
