import string

alfabe = string.ascii_lowercase

def vigenere_sifrele(metin, key):
    key = key.lower()
    sonuc = ""
    k = 0  
    for ch in metin.lower():
        if ch in alfabe:
            shift = alfabe.index(key[k % len(key)])
            e = (alfabe.index(ch) + shift) % 26
            sonuc += alfabe[e]
            k += 1
        else:
            sonuc += ch
    return sonuc

def vigenere_coz(sifreli, key):
    key = key.lower()
    sonuc = ""
    k = 0
    for ch in sifreli.lower():
        if ch in alfabe:
            shift = alfabe.index(key[k % len(key)])
            d = (alfabe.index(ch) - shift) % 26
            sonuc += alfabe[d]
            k += 1
        else:
            sonuc += ch
    return sonuc

metin = "selamin aleykum"
anahtar = "anahtar"  
sifreli = vigenere_sifrele(metin, anahtar)
cozulmus = vigenere_coz(sifreli, anahtar)

print("Şifreli :", sifreli)
print("Çözülmüş:", cozulmus)
