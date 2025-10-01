from math import gcd
import string
alfabe = string.ascii_lowercase

def encrypt(text, key):
    a,b = map(int,key.split(","))
    if gcd(a,26)!=1:
        raise ValueError("a ile 26 aralarında asal olmalı")
    sonuc=""
    for ch in text.lower():
        if ch in alfabe:
            x=alfabe.index(ch)
            sonuc+=alfabe[(a*x+b)%26]
        else:
            sonuc+=ch
    return sonuc

def decrypt(text, key):
    a,b = map(int,key.split(","))
    if gcd(a,26)!=1:
        raise ValueError("a ile 26 aralarında asal olmalı")
    a_inv = pow(a,-1,26)
    sonuc=""
    for ch in text.lower():
        if ch in alfabe:
            y=alfabe.index(ch)
            sonuc+=alfabe[(a_inv*(y-b))%26]
        else:
            sonuc+=ch
    return sonuc
