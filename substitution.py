import string

alfabe = string.ascii_lowercase
anahtar = "qwertyuiopasdfghjklzxcvbnm" 

sifre_map = dict(zip(alfabe, anahtar))
coz_map   = dict(zip(anahtar, alfabe))

def sifrele(metin):
    sonuc = ""
    for ch in metin.lower():
        if ch in sifre_map:
            sonuc += sifre_map[ch]
        else:
            sonuc += ch 
    return sonuc

def coz(metin):
    sonuc = ""
    for ch in metin.lower():
        if ch in coz_map:
            sonuc += coz_map[ch]
        else:
            sonuc += ch
    return sonuc

orijinal = "selamin aleykum"
sifreli = sifrele(orijinal)
cozulmus = coz(sifreli)

print("Şifreli :", sifreli)
print("Çözülmüş:", cozulmus)
