#!/usr/bin/env python3
"""Kullanım: python3 dogrula.py icerik_01-10.json  → her dersin her metni yalnızca öğrenilmiş harflerle mi?"""
import json,sys,re
S=json.load(open('/home/claude/aa/sira.json',encoding='utf-8'))
H=[d[0] for d in S['dersler']]
def kucuk(t): return t.replace('I','ı').replace('İ','i').lower()
def harfler(t): return set(c for c in kucuk(t) if c.isalpha())
hata=0
for f in sys.argv[1:]:
    for D in json.load(open(f,encoding='utf-8')):
        n=D['ders'];izin=set(H[:n])
        metinler=[]
        metinler+= [('heceler',x) for x in D['heceler']]+[('kelimeler',x) for x in D['kelimeler']]+[('cumleler',x) for x in D['cumleler']]
        metinler+= [('resimli',D['resimli_kelime']['kelime'])]
        hk=D.get('hikaye')
        if hk:
            metinler+=[('hikaye.baslik',hk['baslik'])]+[('hikaye',x) for x in hk['cumleler']]
            for q in hk.get('sorular',[]): metinler+=[('cevap',q['cevap'])]  # soruyu öğretmen okur
        if H[n-1] not in kucuk(' '.join(D['kelimeler'])): print(f'ders {n}: yeni harf "{H[n-1]}" kelimelerde yok'); hata+=1
        for tur,m in metinler:
            fazla=harfler(m)-izin
            if re.search(r'\d',m): fazla.add('rakam')
            if fazla: print(f'ders {n} [{tur}] "{m}" → öğrenilmemiş: {"".join(sorted(fazla))}'); hata+=1
print('HATA:',hata) ; sys.exit(1 if hata else 0)
