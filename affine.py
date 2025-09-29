import string
from math import gcd

alfabe = string.ascii_lowercase

def affine_sifrele(text, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("a ve 26 aralarında asal olmalı!")
    sonuc = ""
    for ch in text.lower():
        if ch in alfabe:
            x = alfabe.index(ch)
            e = (a * x + b) % 26
            sonuc += alfabe[e]
        else:
            sonuc += ch
    return sonuc

def affine_coz(cipher, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("a ve 26 aralarında asal olmalı!")
    a_inv = pow(a, -1, 26)
    sonuc = ""
    for ch in cipher.lower():
        if ch in alfabe:
            y = alfabe.index(ch)
            d = (a_inv * (y - b)) % 26
            sonuc += alfabe[d]
        else:
            sonuc += ch
    return sonuc

metin = "selamin aleykum"
a, b = 5, 8  
sifreli = affine_sifrele(metin, a, b)
cozulmus = affine_coz(sifreli, a, b)

print("Şifreli :", sifreli)
print("Çözülmüş:", cozulmus)
