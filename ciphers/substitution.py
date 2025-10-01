import string
alfabe = string.ascii_lowercase

def encrypt(text, key):
    if len(key)!=26 or len(set(key))!=26:
        raise ValueError("Anahtar 26 farklı harf olmalı")
    sifre_map = dict(zip(alfabe,key.lower()))
    sonuc=""
    for ch in text.lower():
        sonuc+=sifre_map.get(ch,ch)
    return sonuc

def decrypt(text, key):
    if len(key)!=26 or len(set(key))!=26:
        raise ValueError("Anahtar 26 farklı harf olmalı")
    coz_map = dict(zip(key.lower(),alfabe))
    sonuc=""
    for ch in text.lower():
        sonuc+=coz_map.get(ch,ch)
    return sonuc
